"""Shared graph model API with merged semantic-audit fragment support.

The historical graph model lives in `underlying_lean_graph_model_core.py`.
This public surface still owns loading of the semantic round-trip registry; the
new fragment layer only prevents collaborators from rewriting one multi-MB JSON
file. All graph identities, colours, statuses and edge semantics remain owned by
the unchanged core.
"""
from __future__ import annotations

from pathlib import Path

try:
    import underlying_lean_graph_model_core as _core
    from underlying_lean_graph_model_core import *  # noqa: F401,F403
except ImportError:
    from . import underlying_lean_graph_model_core as _core
    from .underlying_lean_graph_model_core import *  # type: ignore # noqa: F401,F403

_core_load = _core.load


def load(path: Path):
    if Path(path).resolve() == Path(SEMANTIC_REGISTRY).resolve():  # type: ignore[name-defined]
        try:
            import astis_semantic_roundtrip as semantic
        except ImportError:
            from tools import astis_semantic_roundtrip as semantic
        return semantic.load_registry(Path(path))
    return _core_load(Path(path))


_core.load = load
