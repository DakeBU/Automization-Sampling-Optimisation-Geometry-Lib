"""Install the checksum-pinned official Linux toolchain on a hosted CI runner."""

import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import tempfile


TOOLCHAIN = "leanprover/lean4:v4.33.0"
LEAN_COMMIT = "d8b18978322de05a8f3dba51ef03cf5461676c17"
# https://github.com/leanprover/lean4/releases/expanded_assets/v4.33.0
ARCHIVE = "lean-4.33.0-linux.tar.zst"
SHA256 = "4b3fb03c29a1e0a253fb1d11f9bae3725f19a0dc6fc09b3ea16d2c9df3349e2c"
URLS = (
    f"https://github.com/leanprover/lean4/releases/download/v4.33.0/{ARCHIVE}",
    f"https://releases.lean-lang.org/lean4/v4.33.0/{ARCHIVE}",
)


def download(destination: Path) -> str:
    """Switch endpoints only on a download failure, not an integrity failure."""
    for url in URLS:
        try:
            subprocess.run(
                ["curl", "-q", "--fail", "--silent", "--show-error", "--location",
                 "--proto", "=https", "--proto-redir", "=https", "--connect-timeout", "15",
                 "--max-time", "180", "--retry", "1", "--retry-max-time", "210",
                 "--max-filesize", "600000000",
                 "--output", str(destination), url],
                check=True, timeout=420,
            )
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            print(f"Official Lean download failed: {url}", flush=True)
            continue
        with destination.open("rb") as stream:
            digest = hashlib.file_digest(stream, "sha256").hexdigest()
        if digest != SHA256:
            raise ValueError("Official Lean archive SHA-256 mismatch; refusing extraction")
        return url
    raise RuntimeError("Neither official Lean download endpoint succeeded")


def capture(*command: str) -> str:
    return subprocess.run(command, check=True, capture_output=True, text=True,
                          timeout=30).stdout.strip()


def install(project: Path, runner_temp: Path, github_path: Path) -> None:
    if sys.platform != "linux" or platform.machine() != "x86_64":
        raise ValueError("This binary pin applies only to Linux x86_64 CI")
    if (project / "lean-toolchain").read_text(encoding="utf-8").strip() != TOOLCHAIN:
        raise ValueError("Toolchain pin changed; update and verify the official archive pin first")
    with tempfile.TemporaryDirectory(prefix="astis-lean-download-", dir=runner_temp) as scratch:
        archive = Path(scratch) / ARCHIVE
        endpoint = download(archive)
        # Use a fresh directory, never overwrite an existing toolchain.
        prefix = Path(tempfile.mkdtemp(prefix="astis-lean-4.33.0-", dir=runner_temp)).resolve()
        subprocess.run(
            ["tar", "--zstd", "--no-same-owner", "--strip-components=1",
             "--extract", "--file", str(archive), "--directory", str(prefix)],
            check=True, timeout=180,
        )
    # The isolated native verifier mounts this exact directory read-only
    # under a separate UID; mkdtemp's default 0700 would deny that UID access.
    prefix.chmod(0o755)
    binary = prefix / "bin"
    version = capture(str(binary / "lean"), "--version")
    if (not version.startswith("Lean (version 4.33.0, ")
            or not version.endswith(f", commit {LEAN_COMMIT}, Release)")):
        raise ValueError(f"Unexpected official Lean version: {version}")
    if Path(capture(str(binary / "lean"), "--print-prefix")).resolve() != prefix:
        raise ValueError("Lean reports a different sysroot")
    lake_version = capture(str(binary / "lake"), "--version")
    if "\n" in str(binary) or "\r" in str(binary):
        raise ValueError("Unsafe path for the GitHub PATH command file")
    with github_path.open("a", encoding="utf-8") as output:
        output.write(f"{binary}\n")
    print(json.dumps({"toolchain": TOOLCHAIN, "archive_sha256": SHA256,
                      "endpoint": endpoint, "lean": version, "lake": lake_version}))


if __name__ == "__main__":
    install(Path.cwd(), Path(os.environ["RUNNER_TEMP"]), Path(os.environ["GITHUB_PATH"]))
