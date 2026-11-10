"""Deterministic setup boundary tests; the actual archive is checked in CI."""

from contextlib import redirect_stdout
import hashlib
import io
from pathlib import Path
import stat
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import install as setup


class PinnedLeanSetupTests(unittest.TestCase):
    def setUp(self):
        scratch = tempfile.TemporaryDirectory()
        self.addCleanup(scratch.cleanup)
        self.root = Path(scratch.name)
        self.archive = self.root / setup.ARCHIVE
        self.github_path = self.root / "path-env"
        self.project_pin = self.root / "lean-toolchain"
        self.project_pin.write_text(setup.TOOLCHAIN + "\n", encoding="utf-8")
        self.enterContext(redirect_stdout(io.StringIO()))

    def test_transport_failure_retries_only_an_official_endpoint(self):
        payload = b"controlled checksum fixture"

        def curl(argv, **kwargs):
            self.assertEqual(argv[0], "curl")
            self.assertTrue(kwargs["check"])
            if argv[-1] == setup.URLS[0]:
                raise subprocess.CalledProcessError(22, argv)
            self.assertEqual(argv[-1], setup.URLS[1])
            self.assertEqual(argv[argv.index("--proto-redir") + 1], "=https")
            Path(argv[argv.index("--output") + 1]).write_bytes(payload)

        with patch.object(setup, "SHA256", hashlib.sha256(payload).hexdigest()), \
                patch.object(setup.subprocess, "run", side_effect=curl) as run:
            self.assertEqual(setup.download(self.archive), setup.URLS[1])
        self.assertEqual(run.call_count, 2)

    def test_both_failed_endpoints_fail_closed(self):
        with patch.object(setup.subprocess, "run",
                          side_effect=subprocess.CalledProcessError(22, ["curl"])) as run:
            with self.assertRaisesRegex(RuntimeError, "Neither official"):
                setup.download(self.archive)
        self.assertEqual(run.call_count, 2)

    def test_wrong_pin_and_architecture_precede_download(self):
        with patch.object(setup.sys, "platform", "linux"), \
                patch.object(setup.platform, "machine", return_value="aarch64"), \
                patch.object(setup, "download") as download:
            with self.assertRaisesRegex(ValueError, "Linux x86_64"):
                setup.install(self.root, self.root, self.github_path)
            download.assert_not_called()
        self.project_pin.write_text("leanprover/lean4:v4.32.0\n", encoding="utf-8")
        with patch.object(setup.sys, "platform", "linux"), \
                patch.object(setup.platform, "machine", return_value="x86_64"), \
                patch.object(setup, "download") as download:
            with self.assertRaisesRegex(ValueError, "Toolchain pin changed"):
                setup.install(self.root, self.root, self.github_path)
            download.assert_not_called()

    def test_corrupt_bytes_never_extract_or_publish_a_path(self):
        def corrupt(argv, **kwargs):
            self.assertEqual(argv[0], "curl")
            Path(argv[argv.index("--output") + 1]).write_bytes(b"not the official archive")

        with patch.object(setup.sys, "platform", "linux"), \
                patch.object(setup.platform, "machine", return_value="x86_64"), \
                patch.object(setup.subprocess, "run", side_effect=corrupt) as run:
            with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
                setup.install(self.root, self.root, self.github_path)
        self.assertEqual(run.call_count, 1)
        self.assertFalse(self.github_path.exists())
        self.assertEqual(list(self.root.glob("astis-lean-*")), [])

    def simulated_archive(self, version: str, different_prefix: bool = False):
        def capture(executable: str, flag: str) -> str:
            exe = Path(executable)
            self.assertEqual(exe.parent.parent.parent, self.root.resolve())
            if flag == "--print-prefix":
                return str(self.root if different_prefix else exe.parent.parent)
            return version if exe.name == "lean" else "Lake version fixture"

        with patch.object(setup.sys, "platform", "linux"), \
                patch.object(setup.platform, "machine", return_value="x86_64"), \
                patch.object(setup, "download", return_value=setup.URLS[0]), \
                patch.object(setup.subprocess, "run") as tar, \
                patch.object(setup, "capture", side_effect=capture):
            setup.install(self.root, self.root, self.github_path)
        self.assertEqual(tar.call_args.args[0][0], "tar")

    def test_path_is_added_after_the_release_and_sysroot_checks(self):
        version = f"Lean (version 4.33.0, x86_64-unknown-linux-gnu, commit {setup.LEAN_COMMIT}, Release)"
        self.simulated_archive(version)
        path = Path(self.github_path.read_text(encoding="utf-8").strip())
        self.assertEqual(path.name, "bin")
        self.assertEqual(path.parent.parent, self.root.resolve())
        if setup.os.name == "posix":
            self.assertTrue(stat.S_IMODE(path.parent.stat().st_mode) & stat.S_IXOTH)

    def test_version_or_sysroot_mismatch_cannot_publish_a_path(self):
        with self.assertRaisesRegex(ValueError, "Unexpected official Lean version"):
            self.simulated_archive("Lean (version 4.32.0)")
        self.assertFalse(self.github_path.exists())
        version = f"Lean (version 4.33.0, x86_64-unknown-linux-gnu, commit {setup.LEAN_COMMIT}, Release)"
        with self.assertRaisesRegex(ValueError, "different sysroot"):
            self.simulated_archive(version, different_prefix=True)
        self.assertFalse(self.github_path.exists())
