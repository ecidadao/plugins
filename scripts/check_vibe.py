"""Exercise Vibe's real native loader offline, in disposable directories."""
import importlib.metadata
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

from package import PLUGIN, SKILLS, ENDPOINT, require, validate_source, variant_files


def main():
    # Parent imports only our checker; VIBE_HOME is set before any Vibe import.
    with tempfile.TemporaryDirectory(prefix="ecidadao-vibe-") as temporary:
        env = dict(os.environ, VIBE_HOME=temporary)
        env.pop("MISTRAL_API_KEY", None)
        subprocess.run([sys.executable, __file__, "--child", temporary],
                       env=env, check=True, timeout=90)


def child(temporary):
    require(importlib.metadata.version("mistral-vibe") == "3.1.5", "Unexpected Vibe version")
    from vibe.core.plugins import PluginResolver
    manifest, original, standard = validate_source()
    base = Path(temporary)
    def resolve(label, files):
        target = base / label / "ecidadao"
        for name, data in files.items():
            path = target / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        return PluginResolver(plugin_dirs=[target], data_root_base=base / "data" / label,
                              apply_switches=False).resolve()
    incompatible = resolve("original", original)
    require(not incompatible.mcp_servers, "Original OpenAI dialect unexpectedly accepted")
    require(any("extensions" in issue.message for issue in incompatible.issues),
            "Expected extension rejection was not observed")
    loaded = resolve("vibe", variant_files(original, standard, "vibe"))
    require(not loaded.issues, f"Vibe loader issues: {loaded.issues}")
    require([(p.name, p.version) for p in loaded.plugins] == [("ecidadao", manifest["version"])],
            "Plugin identity/version not loaded")
    require(set(loaded.skills) == {f"ecidadao:{s}" for s in SKILLS}, "Skills not loaded")
    require(len(loaded.mcp_servers) == 1, "Expected one loaded MCP server")
    server = loaded.mcp_servers[0]
    require(server.source_id == "ecidadao" and server.server.url == ENDPOINT,
            "Wrong loaded endpoint")
    require(server.server.transport == "streamable-http", "Wrong loaded transport")
    print(json.dumps({"client": "mistral-vibe 3.1.5", "loader": "PluginResolver",
                      "version": manifest["version"], "skills": sorted(loaded.skills),
                      "mcp_servers_loaded": 1, "original_dialect_rejected": True,
                      "model_execution": False, "endpoint_connected": False}))


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--child":
        child(sys.argv[2])
    else:
        main()

