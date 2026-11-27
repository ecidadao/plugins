import json
from pathlib import Path
import shutil
import stat
import sys
import tempfile
import unittest
import warnings
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import package
from jsonschema import ValidationError


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.plugin = self.base / "plugin"
        shutil.copytree(package.PLUGIN, self.plugin)
        self.manifest, self.files, self.standard = package.validate_source(self.plugin)

    def archive(self, entries):
        path = self.base / "bad.zip"
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            with zipfile.ZipFile(path, "w") as z:
                for name, value in entries:
                    z.writestr(name, value)
        return path

    def test_reproducible_build_and_byte_consistency(self):
        for variant in ["standard", "vibe"]:
            files = package.variant_files(self.files, self.standard, variant)
            first, second = self.base / "a.zip", self.base / "b.zip"
            package.build_zip(first, files)
            package.build_zip(second, files)
            self.assertEqual(first.read_bytes(), second.read_bytes())
            self.assertEqual(package.validate_zip(first, files), files)
        self.assertEqual(package.variant_files(self.files, self.standard, "vibe")["plugin.json"],
                         self.files["plugin.json"])

    def test_tampered_or_missing_zip_content_fails(self):
        for entries in [[("plugin.json", b"tampered")],
                        [(k, v) for k, v in self.files.items() if k != "mcp.json"]]:
            with self.assertRaisesRegex(ValueError, "differs"):
                package.validate_zip(self.archive(entries), self.files)

    def test_traversal_absolute_windows_and_duplicate_paths_fail(self):
        for name in ["../escape", "/escape", "a/../escape", "C:/escape", "a\\escape", "./escape"]:
            with self.subTest(name=name), self.assertRaises(ValueError):
                package.validate_zip(self.archive([(name, b"x")]))
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            package.validate_zip(self.archive([("a", b"1"), ("a", b"2")]))

    def test_zip_symlink_and_size_fail(self):
        link = zipfile.ZipInfo("link")
        link.create_system = 3
        link.external_attr = (stat.S_IFLNK | 0o777) << 16
        with self.assertRaisesRegex(ValueError, "Non-file"):
            package.validate_zip(self.archive([(link, b"../../outside")]))
        with self.assertRaisesRegex(ValueError, "too large"):
            package.validate_zip(self.archive([("large", b"x" * (package.MAX_ZIP_BYTES + 1))]))

    def test_divergent_adapter_fails(self):
        path = self.plugin / ".mcp.json"
        path.write_text('{"mcpServers":{}}')
        with self.assertRaisesRegex(ValueError, "Stale adapter"):
            package.validate_source(self.plugin)

    def test_schema_and_unknown_auth_extension_fail(self):
        bad = dict(self.manifest, name="Invalid Name")
        with self.assertRaises(ValidationError):
            package.validate_schema(bad, "plugin.schema.json")
        # The original OpenAI dialect is deliberately NOT declared strict-standard compliant.
        original = package.read(self.plugin / "mcp.json")
        with self.assertRaises(ValidationError):
            package.validate_schema(original, "mcp.schema.json")
        package.validate_schema(self.standard, "mcp.schema.json")
        original["mcpServers"]["ecidadao"]["extensions"]["com.openai"]["auth"]["type"] = "oauth"
        (self.plugin / "mcp.json").write_text(json.dumps(original))
        with self.assertRaisesRegex(ValueError, "authentication"):
            package.validate_source(self.plugin)

    def test_symlink_in_source_fails(self):
        (self.plugin / "escape").symlink_to(self.base)
        with self.assertRaisesRegex(ValueError, "Symlink"):
            package.validate_source(self.plugin)


if __name__ == "__main__":
    unittest.main()

