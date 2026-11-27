"""Install the local marketplace with a disposable Codex home; never run a model."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

from package import ENDPOINT, PLUGIN, ROOT, SKILLS, read, require

VERSION = "codex-cli 0.172.0"


def main():
    require(subprocess.check_output(["codex", "--version"], text=True, timeout=15).strip() == VERSION,
            "Unexpected Codex version")
    with tempfile.TemporaryDirectory(prefix="ecidadao-codex-") as temporary:
        env = dict(os.environ)
        env["CODEX_HOME"] = temporary  # child process only; HOME is never changed
        for key in ("OPENAI_API_KEY", "CODEX_API_KEY"):
            env.pop(key, None)
        def run(*args):
            return json.loads(subprocess.check_output(
                ["codex", "plugin", *args, "--json"], env=env, text=True, timeout=60))
        marketplace = run("marketplace", "add", str(ROOT))
        require(marketplace["marketplaceName"] == "ecidadao", "Wrong marketplace")
        result = run("add", "ecidadao@ecidadao")
        installed = Path(result["installedPath"]).resolve()
        require(installed.is_relative_to(Path(temporary).resolve()), "Install escaped temporary home")
        require(result["version"] == read(PLUGIN / "plugin.json")["version"], "Wrong installed version")
        require(read(installed / "plugin.json") == read(PLUGIN / "plugin.json"), "Installed manifest differs")
        require({p.parent.name for p in (installed / "skills").glob("*/SKILL.md")} == SKILLS,
                "Installed skills differ")
        for skill in SKILLS:
            relative = Path("skills") / skill / "SKILL.md"
            require((installed / relative).read_bytes() == (PLUGIN / relative).read_bytes(),
                    "Installed skill bytes differ")
        require(read(installed / "mcp.json") == read(PLUGIN / "mcp.json"), "Installed MCP differs")
        require(read(installed / "mcp.json")["mcpServers"]["ecidadao"]["url"] == ENDPOINT,
                "Wrong installed endpoint")
        print(json.dumps({"client": VERSION, "installed_version": result["version"],
                          "skills": sorted(SKILLS), "isolated_install": True,
                          "model_execution": False, "endpoint_connected": False}))


if __name__ == "__main__":
    main()

