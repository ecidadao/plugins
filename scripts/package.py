"""Generate compatibility files, validate package consistency and build a ZIP."""
import argparse
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins/ecidadao"

def read(path):
    return json.loads(path.read_text())

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sync", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--build", action="store_true")
    args = parser.parse_args()
    manifest = read(PLUGIN / "plugin.json")
    servers = read(PLUGIN / "mcp.json")["mcpServers"]
    compatibility = {k: manifest[k] for k in ("name", "version", "description", "author", "homepage", "license", "keywords")}
    compatibility["repository"] = "https://github.com/ecidadao/plugins"
    compatibility["privacyPolicyUrl"] = manifest["extensions"]["com.openai"]["interface"]["privacyPolicyURL"]
    http_servers = {}
    for name, server in servers.items():
        assert server["type"] == "streamable-http", "Unsupported transport"
        assert server["url"].startswith("https://"), "Public MCP must use HTTPS"
        http_servers[name] = {"type": "http", "url": server["url"]}
    generated = {".claude-plugin/plugin.json": compatibility, ".mcp.json": {"mcpServers": http_servers}}
    for name, content in generated.items():
        path = PLUGIN / name
        if args.sync:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(content, ensure_ascii=False, indent=2) + "\n")
        assert read(path) == content, f"Stale adapter: {name}; run --sync"
    for file in ROOT.rglob("*.json"):
        if ".git" not in file.parts:
            read(file)
    for file in (ROOT / ".agents/plugins/marketplace.json", ROOT / ".claude-plugin/marketplace.json"):
        for entry in read(file)["plugins"]:
            source = entry["source"]
            path = source["path"] if isinstance(source, dict) else source
            assert path.startswith("./") and ".." not in Path(path).parts
            target = ROOT / path
            assert read(target / "plugin.json")["name"] == entry["name"]
    assert list((PLUGIN / "skills").glob("*/SKILL.md")), "Missing skills"
    if args.build:
        out = ROOT / "dist" / f"ecidadao-plugin-{manifest['version']}.zip"
        out.parent.mkdir(exist_ok=True)
        with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as archive:
            for file in sorted(PLUGIN.rglob("*")):
                if file.is_file():
                    archive.write(file, file.relative_to(PLUGIN))
        print(out)
    print("Package validated:", manifest["version"])

if __name__ == "__main__":
    main()
