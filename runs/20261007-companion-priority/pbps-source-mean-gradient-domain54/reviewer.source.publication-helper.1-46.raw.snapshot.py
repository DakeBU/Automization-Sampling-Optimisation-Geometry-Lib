#!/usr/bin/env python3
"""Incremental theorem → reader → semantic-audit publication contract.

This is an index of correspondence edges, never a second proof-status registry.
Compilation remains the Lean gate's job; semantic equivalence remains an
independent reviewer's job. No model calls or background sessions are started.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from functools import lru_cache
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
sys.path.insert(0, str(ROOT / 'website/scripts'))
import astis_site
import astis_frontier_cells
import astis_semantic_roundtrip as roundtrip

CONTENT = ROOT / 'website/content/publications'
MIGRATION_BASE = '5c6adf3b812f3ba9315c92ba78a4ff59ccc2a53e'
LEGACY_FILE_SHA = '6efa3254bc53f8bd93423d56c79f38b90af35f0097e1223940c328861b336c17'
REGISTRY_DATA_NAMES = frozenset(('sltSourceAnchor analysisMemory gaussianMemory taylorMemory '
    'calculusMemory measureMemory probabilityMemory functionalInequalityMemory stochasticProcessMemory '
    'klDensityMemory renyiDensityMemory variationalMemory geometryMemory saldExtractedMemory '
    'portQueueMemory technicalLemmaMemory formalizedTechnicalLemmaCount').split())
REGISTRY_METADATA_TYPES = frozenset({
    ('inductive', 'AutoSamplingTheory.TechnicalLemmas.LemmaMemoryStatus'),
    ('structure', 'AutoSamplingTheory.TechnicalLemmas.LemmaMemoryEntry'),
})
LEGACY_NAMES = frozenset(
    'AutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexFirstOrder.' + name
    for name in ('firstOrder_lower_bound_of_strongConvexOn',
                 'gradient_inner_lower_bound_of_strongConvexOn')
)
PRIVATE_IMPLEMENTATION_COVERAGE: list[dict] = []


