"""External checks, intentionally separate from deterministic PR/package tests."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
import urllib.request

from package import ENDPOINT, ROOT, require, validate_zip

TOOLS = {
    "siga_visit_guidance", "financas_service_guidance", "prepare_financas_ebalcao",
    "prepare_street_report", "prepare_complaint", "official_submission_guidance",
    "sns24_service_guidance", "municipal_service_search",
    "municipal_appointment_availability", "public_support_guidance",
}


def fetch(url, payload=None, max_bytes=5_000_000):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, headers={
        "User-Agent": "ecidadao-plugin-compatibility",
        "Accept": "application/json, text/event-stream",
        "Content-Type": "application/json",
    })
    with urllib.request.urlopen(req, timeout=35) as response:
        require(response.status == 200, f"HTTP status: {response.status}")
        content = response.read(max_bytes + 1)
        require(len(content) <= max_bytes, "HTTP response too large")
        return content


def published():
    release = json.loads(fetch("https://api.github.com/repos/ecidadao/plugins/releases/latest"))
    require(not release["draft"] and not release["prerelease"], "Release is not public stable")
    tag = release["tag_name"]
    require(re.fullmatch(r"v\d+\.\d+\.\d+", tag), "Unexpected release tag")
    version = tag[1:]
    assets = [a for a in release["assets"] if a["name"] == f"ecidadao-plugin-{version}.zip"]
    require(len(assets) == 1, "Expected exactly one standard release ZIP")
    asset = assets[0]
    expected_url = f"https://github.com/ecidadao/plugins/releases/download/{tag}/{asset['name']}"
    require(asset["browser_download_url"] == expected_url, "Unexpected asset origin")
    data = fetch(expected_url)
    digest = hashlib.sha256(data).hexdigest()
    require(asset.get("digest") == "sha256:" + digest, "GitHub asset digest mismatch")
    subprocess.run(["git", "fetch", "--no-tags", "origin", f"refs/tags/{tag}"],
                   cwd=ROOT, check=True, timeout=60)
    def git(*args):
        return subprocess.check_output(["git", *args], cwd=ROOT, timeout=30)
    commit = git("rev-parse", "FETCH_HEAD^{commit}").decode().strip()
    paths = git("ls-tree", "-r", "--name-only", commit, "plugins/ecidadao").decode().splitlines()
    expected = {p.removeprefix("plugins/ecidadao/"): git("show", f"{commit}:{p}") for p in paths}
    with tempfile.TemporaryDirectory(prefix="ecidadao-release-") as tmp:
        path = Path(tmp) / "release.zip"
        path.write_bytes(data)
        files = validate_zip(path, expected)
    for manifest in ("plugin.json", ".claude-plugin/plugin.json"):
        require(json.loads(files[manifest])["version"] == version, "Tag/manifest version mismatch")
    mcp = json.loads(files["mcp.json"])
    require(mcp["mcpServers"]["ecidadao"]["url"] == ENDPOINT, "Release endpoint mismatch")
    return {"release": release["html_url"], "version": version, "tag_commit": commit,
            "sha256": digest, "files": len(files), "zip_matches_tag": True}


def endpoint(version):
    def rpc(method, params=None):
        payload = {"jsonrpc": "2.0", "id": 1, "method": method}
        if params is not None:
            payload["params"] = params
        response = json.loads(fetch(ENDPOINT, payload))
        require("error" not in response and "result" in response, "MCP error")
        return response["result"]
    init = rpc("initialize", {"protocolVersion": "2025-06-18", "capabilities": {},
                             "clientInfo": {"name": "plugin-compatibility", "version": version}})
    require(init["serverInfo"]["version"] == version, "Published package/server version mismatch")
    require(init["protocolVersion"] == "2025-06-18", "Unexpected MCP protocol")
    tools = rpc("tools/list")["tools"]
    require(len(tools) == len(TOOLS) and {t["name"] for t in tools} == TOOLS,
            "Public tool catalogue mismatch")
    return {"endpoint": ENDPOINT, "version": version, "tools": sorted(TOOLS),
            "model_execution": False, "external_municipal_calls": False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("check", choices=["release", "endpoint"])
    parser.add_argument("--version")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.check == "endpoint":
        require(bool(args.version), "--version is required for endpoint check")
        result = endpoint(args.version)
    else:
        result = published()
    output = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(output)
    print(output, end="")


if __name__ == "__main__":
    main()

