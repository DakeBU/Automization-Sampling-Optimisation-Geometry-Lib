"""Bounded statement lookup from one replayable, eligible compiler-graph slice.

The query operates on frozen in-memory records only. It has no path, URL,
proof-body, or graph-answer interface. This is public-dev library assistance,
not a held-out corpus, a formal entailment claim, or measured search ability.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

import sog_bench_compiled_graph as compiled
import sog_bench_lean_workspace as workspace
import sog_bench_review as review

bench = workspace.runtime.bench
PROFILE = 'transport-statements-v1'
BASELINE = 'provided-prompt-template-only'
TARGET_ID = 'sogb-018'
MAX_SEARCHES = 4
MAX_QUERY_BYTES = 240
MAX_CORPUS_BYTES = 32768
MAX_SIGNATURE_BYTES = 1800
MAX_HITS = 3
# Manually reviewed owned source scope. Do not replace by a repository glob,
# all graph nodes, all target parents, an external index, or the full task ZIP.
PREFIX = 'AutoSamplingTheory.TechnicalLemmas.Measure.'
ALLOW = {PREFIX + name for name in (
    'TransportGluing.exists_gluing_of_isCoupling',
    'TransportGluing.fst_gluingMeasure',
    'TransportGluing.map_snd_fst_gluingMeasure',
    'WassersteinSpace.exists_isCoupling_sqrt_lintegral_lt_of_wassersteinDistance_lt',
    'WassersteinSpace.wassersteinDistance_le_sqrt_lintegral_of_isCoupling',
    'WassersteinTriangleMarginals.isCoupling_map_pair13_of_pair12_pair23',
    'WassersteinTriangleMarginals.l2Seminorm_edge12_eq_pairCost',
    'WassersteinTriangleMarginals.l2Seminorm_edge23_eq_pairCost',
    'WassersteinTriangleMarginals.l2Seminorm_edge13_eq_pairCost',
    'WassersteinTriangleCore.l2_edge_triangle',
    'WassersteinTriangleCore.l2Seminorm_mono',
    'WassersteinTriangleCore.l2Seminorm_add_le',
)}
TOOL = {'type': 'function', 'name': 'lookup_lean_statements', 'strict': True,
    'description': 'Look up up to three Lean theorem signatures in a fixed public transport library slice. Use topic words or a theorem name, never a path or URL.',
    'parameters': {'type': 'object', 'properties': {
        'query': {'type': 'string', 'description': 'A short topic query or Lean theorem name.'}},
        'required': ['query'], 'additionalProperties': False}}


def build() -> dict:
    """Project a committed graph snapshot; the trusted CI also replays it in Lean."""
    spec, core, snapshot = compiled.recorded()
    if (core['id'] != TARGET_ID or core['split'] != 'public-dev'
            or not review.accepted(bench.editorial_review([core])['items'][TARGET_ID])
            or snapshot['graph']['kind'] != compiled.KIND):
        raise ValueError('Lookup is limited to its exact admitted public Lean target')
    # Exclude every task's answer module even if another family currently owns
    # it. Reference-bearing support modules are excluded as well.
    catalog = bench.materialize()
    excluded = {c['source_file'] for c in catalog}
    for c in catalog:
        excluded.update(d['source_file'] for d in c.get('supporting_declarations', []))
        excluded.update(d['source_file']
                        for d in c.get('textbook_exercise', {}).get('answer_declarations', []))
    graph = snapshot['graph']
    nodes = {r['id'] for r in snapshot['rows']}
    if not ALLOW <= nodes:
        raise ValueError('An approved lookup declaration is absent from the compiled slice')
    imports = set(workspace.runtime.local_imports(core['imports']))
    rows = []
    for name in sorted(ALLOW):
        decl = bench.astis_site._SOURCE_BY_NAME[name]
        if (decl.source_file in excluded or decl.module not in imports
                or decl.has_placeholder or decl.kind not in {'theorem', 'lemma'}):
            raise ValueError('Lookup allowlist contains an answer module or unavailable theorem')
        code = bench.astis_site.sanitize_lean(decl.source_text)
        statement, proof = bench.inline_lean.split_statement(code)
        statement = '\n'.join(line.rstrip() for line in statement.strip().splitlines())
        if (not proof.startswith(':=') or not re.match(r'^(theorem|lemma)\s', statement)
                or not 1 <= len(statement.encode()) <= MAX_SIGNATURE_BYTES
                or re.search(r'\b(?:by|sorry|admit|axiom|unsafe|atlas)\b', statement, re.I)):
            raise ValueError('Cannot isolate an eligible bounded theorem signature: ' + name)
        rows.append({'declaration': name, 'title': spec['nodes'][name],
                     'statement': statement, 'module': decl.module,
                     'source_file': decl.source_file, 'source_line': decl.source_line,
                     'source_sha256_lf': graph['source_sha256_lf'][decl.source_file]})
    corpus = {'schema_version': 1, 'profile': PROFILE, 'track': 'lean',
        'task_id': TARGET_ID, 'task_binding_sha256': core['binding_sha256'],
        'split': core['split'], 'graph_sha256': snapshot['graph_sha256'],
        'toolchain': snapshot['provenance']['toolchain'],
        'mathlib_manifest_sha256_lf': snapshot['provenance']['mathlib_manifest_sha256_lf'],
        'license': 'Apache-2.0; Samplinglib original declaration signatures only',
        'rights_scope_sha256_lf': bench.text_hash(bench.ROOT/'LICENSE_SCOPE.md'),
        'lookup_source_sha256_lf': bench.text_hash(Path(__file__)),
        'rows': rows}
    if len(bench.encoded(corpus)) > MAX_CORPUS_BYTES:
        raise ValueError('Lookup corpus exceeds the byte budget')
    return corpus


def words(text: str) -> set[str]:
    split = re.sub(r'(?<=[a-z0-9])(?=[A-Z])', ' ', text)
    return set(re.findall(r'[a-z0-9]+', split.lower()))


def valid_query(query: object) -> bool:
    return (isinstance(query, str) and 1 <= len(query) <= MAX_QUERY_BYTES
            and re.fullmatch(r"[A-Za-z0-9_. '\-]+", query) is not None
            and 1 <= len(words(query)) <= 24 and '..' not in query)


def search(corpus: dict, query: str) -> dict:
    if not valid_query(query):
        raise ValueError('Lookup needs a bounded word query or Lean name')
    tokens = words(query)
    ranked = []
    for row in corpus['rows']:
        name = row['declaration']
        short = name.rsplit('.', 1)[-1]
        score = len(tokens & words(short + ' ' + row['title']))
        if query.strip() in {name, short}:
            score += 100
        if score:
            ranked.append((-score, name, row))
    return {'kind': 'lean-signature-lookup', 'profile': corpus['profile'],
            'corpus_sha256': bench.sha(bench.encoded(corpus)),
            'hits': [row for _, _, row in sorted(ranked)[:MAX_HITS]]}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    corpus = build()
    workspace.write_new(args.output, corpus)
    print(json.dumps({'profile': PROFILE, 'task_id': TARGET_ID, 'rows': len(corpus['rows']),
                      'corpus_sha256': bench.sha(bench.encoded(corpus))}))


if __name__ == '__main__':
    main()
