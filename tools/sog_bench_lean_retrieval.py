"""Project an admitted public compiler slice onto fixed-target Lean imports."""
from __future__ import annotations

import json
from pathlib import Path
import re

import sog_bench_graph_search as search
import sog_bench_lean as runtime

bench = runtime.bench
PROFILE = 'fixed-target-lean-graph-jsonl-v1'
RETRIEVAL = 'same-family-imported-compiled-slice-v1'
TOOLS = ['lean_workspace', 'compiled_graph_lookup']
BOUNDARY = (
    'Names are selected from the fixed target’s imported local modules. '
    'Edges are selected constant occurrences in compiled proof bodies, not '
    'mathematical necessity or a complete dependency closure. No full source, '
    'Lean statement, proof body, graph task answer, or external search is provided.')


def validate(provenance: dict) -> None:
    if (provenance.get('retrieval_profile') != RETRIEVAL
            or provenance.get('tools') != TOOLS
            or not isinstance(provenance.get('graph_task_id'), str)
            or not re.fullmatch(r'sogb-g[0-9]{3}', provenance['graph_task_id'])
            or type(provenance.get('max_graph_lookups')) is not int
            or not 1 <= provenance['max_graph_lookups'] <= 16):
        raise ValueError('Freeze an explicit compiled graph task and a 1–16 lookup budget')


def project(core: dict, item: dict, source_by_name: dict[str, str]) -> dict:
    """Return metadata only; resolve ownership by source file, not namespace."""
    graph = item['context']
    if (item['family'] != core['family'] or item['split'] != 'public-dev'
            or core['split'] != 'public-dev' or graph['kind'] != search.KIND):
        raise ValueError('Graph lookup requires an admitted same-family public-dev compiler slice')
    imported = {name.replace('.', '/') + '.lean' for name in runtime.local_imports(core['imports'])}
    if core['source_file'] in imported:
        raise ValueError('The answer owner must be outside the fixed local import closure')
    if any(source_by_name.get(node) not in graph['source_sha256_lf'] for node in graph['nodes']):
        raise ValueError('Could not resolve every selected declaration to an eligible compiler source')
    kept = {node for node in graph['nodes'] if source_by_name[node] in imported
            and node != core['declaration']}
    nodes = sorted(kept)
    if not nodes:
        raise ValueError('The selected slice has no declarations in the target’s fixed import closure')
    return {'nodes': nodes, 'node_labels': {node: graph['node_labels'][node] for node in nodes},
            'edges': sorted([child, parent] for child, parent in graph['edges']
                            if child in kept and parent in kept),
            'statement_profiles': {node: graph['statement_profiles'][node] for node in nodes}}


def checked_stage(manifest: dict, core: dict) -> str:
    """Prevent live graph hints from claiming availability in a stale stage."""
    stage = Path(manifest['paths']['stage'])
    raw = (stage / 'stage.json').read_bytes()
    descriptor = json.loads(raw)
    modules = runtime.local_imports(core['imports'])
    names = {name.replace('.', '/') + '.lean' for name in modules}
    project_root = stage / 'project'
    present = {path.relative_to(project_root).as_posix()
               for path in (project_root / 'AutoSamplingTheory').rglob('*.lean')}
    if (descriptor['id'] != core['id'] or descriptor['binding_sha256'] != core['binding_sha256']
            or descriptor['owned_ancestor_modules'] != modules or present != names
            or core['source_file'] in names or descriptor['target_module_absent'] is not True
            or descriptor['oracle_included'] is not False):
        raise ValueError('Staged Lean import inventory differs from the fixed graph-assisted target')
    for name in sorted(names):
        path = project_root / name
        if path.is_symlink() or not path.resolve().is_relative_to(project_root.resolve()):
            raise ValueError('Unsafe staged Lean source: ' + name)
        data = path.read_bytes()
        lf = data.decode('utf-8').replace('\r\n', '\n').replace('\r', '\n').encode('utf-8')
        if (descriptor['files'].get('project/' + name) != bench.sha(data)
                or bench.text_hash(runtime.ROOT / name) != bench.sha(lf)):
            raise ValueError('Staged Lean source differs from the current graph import closure: ' + name)
    return bench.sha(raw)


def prepare(manifest: dict) -> tuple[dict, dict]:
    p = manifest['provenance']
    validate(p)
    core = next((c for c in bench.materialize() if c['id'] == manifest['id']), None)
    if not core or not bench.has_lean(core) or core['binding_sha256'] != manifest['binding_sha256']:
        raise ValueError('Graph lookup requires the exact current fixed Lean target')
    stage_digest = checked_stage(manifest, core)
    item = search.admitted(p['graph_task_id'])
    # Admission validated the actual graph declaration owners and source hashes.
    known = bench.astis_site._SOURCE_BY_NAME
    projected = project(core, item, {node: known[node].source_file for node in item['context']['nodes']
                                     if node in known})
    metadata = {'graph_task_id': item['id'], 'graph_sha256': item['graph_sha256'],
                'snapshot_sha256': item['context']['snapshot_sha256'],
                'stage_sha256': stage_digest,
                'projection_sha256': bench.sha(bench.encoded(projected)),
                'projection_source_sha256_lf': bench.text_hash(Path(__file__)),
                'lookup_source_sha256_lf': bench.text_hash(Path(search.__file__)),
                'max_graph_lookups': p['max_graph_lookups']}
    return projected, metadata


def lookup(projected: dict, call: dict, wire_size: int) -> dict:
    if wire_size > search.MAX_REQUEST:
        return {'kind': 'invalid-lookup'}
    return search.lookup({'context': projected}, call)
