"""Validate source/adapters and build reproducible, byte-checked plugin ZIPs."""
import argparse
import copy
import json
from pathlib import Path, PurePosixPath
import stat
import zipfile

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins/ecidadao"
ENDPOINT = "https://ecidadao.pt/mcp/public"
SKILLS = {"financas-assistido", "siga-assistido"}
MAX_ZIP_BYTES = 5_000_000


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read(path):
    return json.loads(path.read_text())


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()


def validate_schema(value, name):
    schema = read(ROOT / "schemas" / name)
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(value)


def adapters(manifest, servers):
    compatibility = {k: manifest[k] for k in
                     ("name", "version", "description", "author", "homepage", "license", "keywords")}
    compatibility["repository"] = "https://github.com/ecidadao/plugins"
    compatibility["privacyPolicyUrl"] = manifest["extensions"]["com.openai"]["interface"]["privacyPolicyURL"]
    return {
        ".claude-plugin/plugin.json": compatibility,
        ".mcp.json": {"mcpServers": {
            name: {"type": "http", "url": server["url"]}
            for name, server in servers.items()
        }},
    }


def source_files(plugin):
    files = {}
    for path in sorted(plugin.rglob("*")):
        require(not path.is_symlink(), f"Symlink in package: {path}")
        if path.is_file():
            name = path.relative_to(plugin).as_posix()
            require(not any(part.startswith(".env") or part in {".git", "__pycache__", ".DS_Store"}
                            for part in path.relative_to(plugin).parts),
                    f"Unexpected private/generated path: {name}")
            files[name] = path.read_bytes()
    return files


def validate_source(plugin=PLUGIN, sync=False):
    manifest = read(plugin / "plugin.json")
    validate_schema(manifest, "plugin.schema.json")
    require(manifest["name"] == "ecidadao", "Unexpected plugin name")
    mcp = read(plugin / "mcp.json")
    # Preserve the published OpenAI auth extension. Validate that single explicit
    # dialect difference, then validate the standard projection (not the original).
    require(set(mcp) == {"$schema", "mcpServers"}, "Unexpected MCP root keys")
    servers = mcp["mcpServers"]
    require(set(servers) == {"ecidadao"}, "Unexpected MCP servers")
    server = servers["ecidadao"]
    require(set(server) == {"type", "url", "extensions"}, "Unexpected OpenAI MCP fields")
    require(server["extensions"] == {"com.openai": {"auth": {"type": "none"}}},
            "Unexpected authentication extension")
    standard = copy.deepcopy(mcp)
    del standard["mcpServers"]["ecidadao"]["extensions"]
    validate_schema(standard, "mcp.schema.json")
    require(server["url"] == ENDPOINT, "Unexpected endpoint")
    require(server["type"] == "streamable-http", "Unexpected transport")
    for name, expected in adapters(manifest, servers).items():
        path = plugin / name
        if sync:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(encoded(expected))
        require(read(path) == expected, f"Stale adapter: {name}; run --sync")
    require({p.parent.name for p in (plugin / "skills").glob("*/SKILL.md")} == SKILLS,
            "Expected exactly two skills")
    files = source_files(plugin)
    require(sum(map(len, files.values())) <= MAX_ZIP_BYTES, "Package too large")
    return manifest, files, standard


def variant_files(files, standard, variant):
    require(variant in {"standard", "vibe"}, "Unknown package variant")
    result = dict(files)
    if variant == "vibe":
        result["mcp.json"] = encoded(standard)
    return result


def validate_zip(path, expected=None):
    """Reject dangerous paths/links/duplicates/size before reading or extracting."""
    with zipfile.ZipFile(path) as archive:
        entries = archive.infolist()
        names = [entry.filename for entry in entries]
        require(len(names) == len(set(names)), "Duplicate ZIP entry")
        require(sum(entry.file_size for entry in entries) <= MAX_ZIP_BYTES, "ZIP too large")
        for entry in entries:
            name = entry.filename
            parts = PurePosixPath(name).parts
            require(parts and not name.startswith("/") and "\\" not in name
                    and ":" not in name and all(part not in {"..", "."} for part in parts)
                    and PurePosixPath(name).as_posix() == name,
                    f"Unsafe ZIP path: {name}")
            mode = (entry.external_attr >> 16) & 0xFFFF
            require(stat.S_IFMT(mode) in {0, stat.S_IFREG}, f"Non-file ZIP entry: {name}")
            require(not entry.is_dir() and not entry.flag_bits & 1,
                    f"Directory/encrypted ZIP entry: {name}")
        require(archive.testzip() is None, "Corrupt ZIP")
        files = {name: archive.read(name) for name in names}
    if expected is not None:
        require(files == expected, "ZIP content differs from expected source bytes")
    return files


def build_zip(path, files):
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, data in sorted(files.items()):
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            archive.writestr(info, data)
    validate_zip(path, files)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sync", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--build", action="store_true")
    parser.add_argument("--variant", choices=["standard", "vibe"], default="standard")
    parser.add_argument("--zip", type=Path, help="Validate ZIP against source/selected variant")
    args = parser.parse_args()
    manifest, files, standard = validate_source(sync=args.sync)
    for file in (ROOT / ".agents/plugins/marketplace.json", ROOT / ".claude-plugin/marketplace.json"):
        for entry in read(file)["plugins"]:
            source = entry["source"]
            path = source["path"] if isinstance(source, dict) else source
            require(path == "./plugins/ecidadao" and entry["name"] == manifest["name"],
                    "Unexpected marketplace source")
    expected = variant_files(files, standard, args.variant)
    if args.build:
        suffix = "-vibe" if args.variant == "vibe" else ""
        out = ROOT / "dist" / f"ecidadao-plugin-{manifest['version']}{suffix}.zip"
        build_zip(out, expected)
        print(out)
    if args.zip:
        validate_zip(args.zip, expected)
    print(f"Package validated: {manifest['version']} ({args.variant})")


if __name__ == "__main__":
    main()
