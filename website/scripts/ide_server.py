#!/usr/bin/env python3
"""Serve Samplinglib with loopback-only formalization and Lean compilation."""

from __future__ import annotations

import argparse
import base64
import hmac
import json
import os
import re
import subprocess
import sys
import tempfile
import threading
import time
from functools import partial
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.astis_formalizer import (  # noqa: E402
    MAX_LATEX_CHARACTERS,
    formalize,
    request_from_dict,
)


DEFAULT_SITE = ROOT / "_site"
MAX_SOURCE_BYTES = 200_000
MAX_REQUEST_BYTES = 240_000
COMPILE_LOCK = threading.Lock()
ASSIST_LOCK = threading.Lock()
ASSIST_ACTIONS = {"explain", "assumptions", "lemmas", "lean", "graph"}
MAX_QUESTION_CHARACTERS = 4_000


def repository_lean_environment() -> dict[str, str]:
    """Return a child environment in which the repository toolchain wins."""
    environment = os.environ.copy()
    try:
        toolchain = (ROOT / "lean-toolchain").read_text(encoding="utf-8").strip()
    except OSError:
        toolchain = ""
    if toolchain:
        environment["ELAN_TOOLCHAIN"] = toolchain
    else:
        environment.pop("ELAN_TOOLCHAIN", None)
    return environment


def workspace_context(
    payload: dict[str, object], workspace_id: str, theorem_id: str, step_id: str
) -> tuple[dict[str, object], dict[str, object], dict[str, object]]:
    """Resolve one exact source-backed step; fail closed on stale identifiers."""
    workspaces = payload.get("workspaces", [])
    if not isinstance(workspaces, list):
        raise ValueError("research workspace data is malformed")
    workspace = next(
        (row for row in workspaces if isinstance(row, dict) and row.get("id") == workspace_id),
        None,
    )
    if workspace is None:
        raise ValueError("unknown research workspace")
    theorem = next(
        (
            row
            for row in workspace.get("theorems", [])
            if isinstance(row, dict) and row.get("id") == theorem_id
        ),
        None,
    )
    if theorem is None:
        raise ValueError("unknown theorem in research workspace")
    step = next(
        (
            row
            for row in theorem.get("steps", [])
            if isinstance(row, dict) and row.get("id") == step_id
        ),
        None,
    )
    if step is None:
        raise ValueError("unknown proof step in research workspace")
    return workspace, theorem, step


def assistant_prompt(
    workspace: dict[str, object],
    theorem: dict[str, object],
    step: dict[str, object],
    action: str,
    question: str,
) -> tuple[str, str]:
    """Construct a bounded prompt that preserves the ASTIS evidence boundary."""
    sources = "\n".join(
        f"- {row.get('title')} ({row.get('version')}): {row.get('url')}"
        for row in workspace.get("source_records", [])
    )
    assumptions = "\n".join(f"- {item}" for item in theorem.get("assumptions", []))
    support = "\n".join(
        f"- {item}" for item in step.get("compiled_support", [])
    ) or "- none attached; this proof step remains open"
    instructions = (
        "You are the source-grounded research assistant inside the Samplinglib proof "
        "workspace. Explain mathematics clearly for a sampling researcher. Preserve "
        "the exact theorem assumptions and truth boundary. Label paper/source facts, "
        "ASTIS-authored expansion, ASTIS-owned compiled support, Mathlib/external facts, "
        "and your own inference separately. Never claim that an open source theorem is "
        "formalized. Generated Lean is only a candidate until the exact snippet compiles; "
        "compilation is still not source-fidelity review. Do not invent declarations, "
        "source anchors, constants, consumers, or completion status."
    )
    user = f"""Requested action: {action}

Workspace: {workspace.get('title')} ({workspace.get('id')})
Primary sources:
{sources}

Theorem: {theorem.get('title')} ({theorem.get('id')})
Source anchor: {theorem.get('source_anchor')}
Statement: {theorem.get('statement')}
Formula: {theorem.get('formula')}
Assumptions:
{assumptions}

Selected proof step: {step.get('title')} ({step.get('id')})
Step source anchor: {step.get('source_anchor')}
Step formula: {step.get('formula')}
ASTIS explanation: {step.get('explanation')}
Step status: {step.get('status')}
Compiled reusable support:
{support}
Support note: {step.get('support_note')}

Strict theorem boundary: {theorem.get('boundary')}
Researcher question: {question or '(none; perform the requested action only)'}

Return a concise mathematical answer with these headings: Source-backed reasoning;
What Lean already checks; Remaining verification obligations. If action is `lean`,
give one minimal theorem-shaped candidate and explain every additional assumption;
do not present it as compiled."""
    return instructions, user


def response_text(payload: dict[str, object]) -> str:
    """Extract public output text from a Responses API result."""
    parts: list[str] = []
    for item in payload.get("output", []):
        if not isinstance(item, dict):
            continue
        for content in item.get("content", []):
            if (
                isinstance(content, dict)
                and content.get("type") == "output_text"
                and isinstance(content.get("text"), str)
            ):
                parts.append(content["text"])
    text = "\n".join(part.strip() for part in parts if part.strip()).strip()
    if not text:
        raise ValueError("assistant returned no output text")
    return text


def lean_version() -> str:
    toolchain = ""
    try:
        toolchain = (ROOT / "lean-toolchain").read_text(encoding="utf-8").strip()
    except OSError:
        pass
    command = (
        ["elan", "run", toolchain, "lean", "--version"]
        if toolchain
        else ["lake", "env", "lean", "--version"]
    )
    try:
        result = subprocess.run(
            command,
            cwd=ROOT,
            env=repository_lean_environment(),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=30,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        return f"Lean unavailable: {error}"
    output = "\n".join(item for item in (result.stdout, result.stderr) if item)
    version_line = next(
        (line.strip() for line in output.splitlines() if "Lean (version " in line),
        "",
    )
    if version_line:
        return version_line
    return output.strip().splitlines()[0] if output.strip() else "Lean unavailable"


def pinned_lean_version() -> str:
    """Read the exact Lean release required by the repository toolchain file."""
    try:
        toolchain = (ROOT / "lean-toolchain").read_text(encoding="utf-8").strip()
    except OSError:
        return ""
    match = re.search(r"(?:^|:)v?(\d+\.\d+\.\d+)(?:$|\s)", toolchain)
    return match.group(1) if match else ""


def lean_toolchain_state() -> tuple[str, str, bool]:
    """Return actual version, pinned version, and an exact fail-closed match flag."""
    actual = lean_version()
    pinned = pinned_lean_version()
    matches = bool(pinned and re.search(rf"\bversion\s+{re.escape(pinned)}\b", actual))
    return actual, pinned, matches


class SamplinglibIDEHandler(SimpleHTTPRequestHandler):
    server_version = "SamplinglibLocalIDE/0.1"
    lean_version_text = "Lean version not checked"
    pinned_lean_version_text = "unknown"
    toolchain_matches_pin = False
    compile_timeout = 120
    auth_user = ""
    auth_password = ""
    ai_api_key = ""
    ai_model = ""
    ai_base_url = "https://api.openai.com/v1"
    ai_timeout = 90

    def authorized(self) -> bool:
        if not self.auth_user and not self.auth_password:
            return True
        value = self.headers.get("Authorization", "")
        if not value.startswith("Basic "):
            return False
        try:
            decoded = base64.b64decode(value[6:], validate=True).decode("utf-8")
            user, password = decoded.split(":", 1)
        except (ValueError, UnicodeDecodeError):
            return False
        return hmac.compare_digest(user, self.auth_user) and hmac.compare_digest(
            password, self.auth_password
        )

    def require_authorization(self) -> bool:
        if self.authorized():
            return False
        body = b"Authentication required.\n"
        self.send_response(HTTPStatus.UNAUTHORIZED)
        self.send_header("WWW-Authenticate", 'Basic realm="Samplinglib preview"')
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)
        return True

    def send_json(self, status: int, payload: dict[str, object]) -> None:
        body = (json.dumps(payload, ensure_ascii=False) + "\n").encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.end_headers()
        self.wfile.write(body)

    def read_json(self, maximum: int) -> dict[str, object] | None:
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            length = 0
        if length <= 0 or length > maximum:
            self.send_json(
                HTTPStatus.REQUEST_ENTITY_TOO_LARGE,
                {"ok": False, "error": f"request must be between 1 and {maximum} bytes"},
            )
            return None
        try:
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            self.send_json(
                HTTPStatus.BAD_REQUEST,
                {"ok": False, "error": "request body is not valid UTF-8 JSON"},
            )
            return None
        if not isinstance(payload, dict):
            self.send_json(
                HTTPStatus.BAD_REQUEST,
                {"ok": False, "error": "request JSON must be an object"},
            )
            return None
        return payload

    def do_GET(self) -> None:  # noqa: N802
        if self.require_authorization():
            return
        if urlsplit(self.path).path == "/api/health":
            self.send_json(
                HTTPStatus.OK,
                {
                    "ok": True,
                    "mode": "local_verified",
                    "lean_version": self.lean_version_text,
                    "pinned_lean_version": self.pinned_lean_version_text,
                    "toolchain_matches_pin": self.toolchain_matches_pin,
                    "formalizer": "deterministic_astis_adapter",
                    "general_semantic_provider": (
                        "openai_responses"
                        if self.ai_api_key and self.ai_model
                        else "not_configured"
                    ),
                    "ai_assistant_configured": bool(self.ai_api_key and self.ai_model),
                    "source_writes": False,
                    "public_execution": False,
                },
            )
            return
        super().do_GET()

    def do_POST(self) -> None:  # noqa: N802
        if self.require_authorization():
            return
        path = urlsplit(self.path).path
        if path == "/api/compile":
            self.handle_compile()
            return
        if path == "/api/formalize":
            self.handle_formalize()
            return
        if path == "/api/assist":
            self.handle_assist()
            return
        self.send_json(HTTPStatus.NOT_FOUND, {"ok": False, "error": "unknown API endpoint"})

    def handle_assist(self) -> None:
        if not self.ai_api_key or not self.ai_model:
            self.send_json(
                HTTPStatus.SERVICE_UNAVAILABLE,
                {
                    "ok": False,
                    "error": "source-grounded assistant is not configured; export the bounded prompt instead",
                },
            )
            return
        payload = self.read_json(MAX_REQUEST_BYTES)
        if payload is None:
            return
        action = payload.get("action")
        question = payload.get("question", "")
        identifiers = [
            payload.get("workspace_id"),
            payload.get("theorem_id"),
            payload.get("step_id"),
        ]
        if action not in ASSIST_ACTIONS:
            self.send_json(HTTPStatus.BAD_REQUEST, {"ok": False, "error": "unknown assistant action"})
            return
        if not all(isinstance(value, str) and value for value in identifiers):
            self.send_json(HTTPStatus.BAD_REQUEST, {"ok": False, "error": "workspace, theorem and step ids are required"})
            return
        if not isinstance(question, str) or len(question) > MAX_QUESTION_CHARACTERS:
            self.send_json(HTTPStatus.BAD_REQUEST, {"ok": False, "error": "question exceeds the bounded workspace limit"})
            return
        try:
            data_path = Path(self.directory) / "data" / "research-workspaces.json"
            workspace_data = json.loads(data_path.read_text(encoding="utf-8"))
            workspace, theorem, step = workspace_context(
                workspace_data, identifiers[0], identifiers[1], identifiers[2]
            )
            instructions, user_input = assistant_prompt(
                workspace, theorem, step, action, question.strip()
            )
        except (OSError, json.JSONDecodeError, ValueError) as error:
            self.send_json(HTTPStatus.BAD_REQUEST, {"ok": False, "error": str(error)})
            return
        if not ASSIST_LOCK.acquire(blocking=False):
            self.send_json(
                HTTPStatus.TOO_MANY_REQUESTS,
                {"ok": False, "error": "another assistant request is running"},
            )
            return
        request_payload = {
            "model": self.ai_model,
            "instructions": instructions,
            "input": user_input,
            "max_output_tokens": 2400,
        }
        request = Request(
            self.ai_base_url.rstrip("/") + "/responses",
            data=json.dumps(request_payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.ai_api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urlopen(request, timeout=self.ai_timeout) as response:
                result = json.load(response)
                answer = response_text(result)
                request_id = response.headers.get("x-request-id", "")
        except HTTPError as error:
            self.send_json(
                HTTPStatus.BAD_GATEWAY,
                {"ok": False, "error": f"assistant provider returned HTTP {error.code}"},
            )
            return
        except (URLError, TimeoutError, OSError, json.JSONDecodeError, ValueError) as error:
            self.send_json(
                HTTPStatus.BAD_GATEWAY,
                {"ok": False, "error": f"assistant provider failed: {error}"},
            )
            return
        finally:
            ASSIST_LOCK.release()
        self.send_json(
            HTTPStatus.OK,
            {
                "ok": True,
                "answer": answer,
                "status": "ai_explanation_unverified",
                "workspace_id": identifiers[0],
                "theorem_id": identifiers[1],
                "step_id": identifiers[2],
                "request_id": request_id,
                "certificate_boundary": "no_lean_or_source_fidelity_certificate",
            },
        )

    def handle_formalize(self) -> None:
        payload = self.read_json(MAX_REQUEST_BYTES)
        if payload is None:
            return
        try:
            request = request_from_dict(payload)
            if len(request.latex) > MAX_LATEX_CHARACTERS:
                raise ValueError("LaTeX request exceeds the formalizer limit")
            result = formalize(request)
        except ValueError as error:
            self.send_json(HTTPStatus.BAD_REQUEST, {"ok": False, "error": str(error)})
            return
        self.send_json(
            HTTPStatus.OK,
            {"ok": result.status == "candidate", "result": result.as_dict()},
        )

    def handle_compile(self) -> None:
        if not self.toolchain_matches_pin:
            self.send_json(
                HTTPStatus.SERVICE_UNAVAILABLE,
                {
                    "ok": False,
                    "output": (
                        "Lean execution is disabled because the active compiler does not "
                        f"match the repository pin {self.pinned_lean_version_text}. "
                        f"Detected: {self.lean_version_text}"
                    ),
                    "certificate_boundary": "toolchain_mismatch_no_compilation",
                },
            )
            return
        payload = self.read_json(MAX_SOURCE_BYTES)
        if payload is None:
            return
        code = payload.get("code")
        if not isinstance(code, str) or not code.strip():
            self.send_json(
                HTTPStatus.BAD_REQUEST,
                {"ok": False, "output": "the `code` field must be a nonempty string"},
            )
            return
        if len(code.encode("utf-8")) > MAX_SOURCE_BYTES:
            self.send_json(
                HTTPStatus.REQUEST_ENTITY_TOO_LARGE,
                {"ok": False, "output": "Lean source exceeds the local size limit"},
            )
            return
        if not COMPILE_LOCK.acquire(blocking=False):
            self.send_json(
                HTTPStatus.TOO_MANY_REQUESTS,
                {"ok": False, "output": "another Lean snippet is compiling"},
            )
            return
        started = time.perf_counter()
        try:
            with tempfile.TemporaryDirectory(prefix="samplinglib-lean-") as temporary:
                source = Path(temporary) / "Main.lean"
                source.write_text(code, encoding="utf-8", newline="\n")
                try:
                    result = subprocess.run(
                        ["lake", "env", "lean", str(source)],
                        cwd=ROOT,
                        env=repository_lean_environment(),
                        capture_output=True,
                        text=True,
                        encoding="utf-8",
                        errors="replace",
                        timeout=self.compile_timeout,
                        check=False,
                    )
                    output = "\n".join(
                        item for item in (result.stdout.strip(), result.stderr.strip()) if item
                    )
                    output = output.replace(str(source), "Main.lean").replace(
                        temporary, "<temporary>"
                    )
                    ok = result.returncode == 0
                    if not output:
                        output = "Lean accepted the snippet." if ok else f"Lean exited with code {result.returncode}."
                    status = HTTPStatus.OK
                except subprocess.TimeoutExpired:
                    ok = False
                    output = f"Lean compilation exceeded the {self.compile_timeout}-second timeout."
                    status = HTTPStatus.REQUEST_TIMEOUT
                except OSError as error:
                    ok = False
                    output = f"Could not start the pinned Lean toolchain: {error}"
                    status = HTTPStatus.SERVICE_UNAVAILABLE
        finally:
            COMPILE_LOCK.release()
        self.send_json(
            status,
            {
                "ok": ok,
                "output": output,
                "duration_ms": round((time.perf_counter() - started) * 1000),
                "certificate_boundary": "elaboration_or_compilation_only",
            },
        )

    def log_message(self, format_string: str, *args: object) -> None:
        # Request bodies contain user mathematics and are never logged.
        super().log_message(format_string, *args)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8088)
    parser.add_argument("--directory", type=Path, default=DEFAULT_SITE)
    parser.add_argument("--compile-timeout", type=int, default=120)
    args = parser.parse_args()
    if args.host not in {"127.0.0.1", "localhost", "::1"}:
        raise SystemExit("ide_server.py is intentionally loopback-only")
    directory = args.directory.resolve()
    if not (directory / "index.html").exists():
        raise SystemExit(f"built site not found at {directory}")
    actual_lean, pinned_lean, toolchain_matches = lean_toolchain_state()
    SamplinglibIDEHandler.lean_version_text = actual_lean
    SamplinglibIDEHandler.pinned_lean_version_text = pinned_lean or "unknown"
    SamplinglibIDEHandler.toolchain_matches_pin = toolchain_matches
    SamplinglibIDEHandler.compile_timeout = max(1, args.compile_timeout)
    SamplinglibIDEHandler.auth_user = os.environ.get("ASTIS_PREVIEW_USER", "")
    SamplinglibIDEHandler.auth_password = os.environ.get("ASTIS_PREVIEW_PASSWORD", "")
    SamplinglibIDEHandler.ai_api_key = os.environ.get("OPENAI_API_KEY", "")
    SamplinglibIDEHandler.ai_model = os.environ.get("ASTIS_OPENAI_MODEL", "")
    if bool(SamplinglibIDEHandler.auth_user) != bool(SamplinglibIDEHandler.auth_password):
        raise SystemExit("set both ASTIS_PREVIEW_USER and ASTIS_PREVIEW_PASSWORD, or neither")
    handler = partial(SamplinglibIDEHandler, directory=str(directory))
    server = ThreadingHTTPServer((args.host, args.port), handler)
    print(f"Samplinglib local research mode: http://{args.host}:{args.port}/live/")
    if not toolchain_matches:
        print(
            "Lean compiler gate: disabled; active compiler "
            f"{actual_lean!r} does not match repository pin {pinned_lean or 'unknown'!r}."
        )
    print("Security: loopback only; snippets are temporary and never written to repository source.")
    print(
        "Basic Auth: enabled from environment."
        if SamplinglibIDEHandler.auth_user
        else "Basic Auth: disabled for loopback-only development."
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
