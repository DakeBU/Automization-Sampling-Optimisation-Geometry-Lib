"""Small public paired-QA pilot; never an untrusted Lean execution service."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / 'tools'), str(ROOT / 'website/scripts')]
import astis_site
import inline_lean
import project_licensing
import sog_bench_curriculum as curriculum

DATA = ROOT / 'benchmarks/samplingoptimisationgeometrybench/cores.json'
SOURCE_APPROVALS = DATA.parent / 'source-approvals'
RECEIPT = ROOT / '.astis/sog-bench/reference-check.json'
TRACKS = ('natural-language', 'lean')
OWNED_EXERCISE_EXAMPLE_ROOT = 'AutoSamplingTheory/ExampleCases/LowerBounds/'
ORIGINAL_EXAMPLE_ANSWERS = {
    'AutoSamplingTheory/ExampleCases/DiscreteSampling/OrderedHeatBath.lean':
        'AutoSamplingTheory.ExampleCases.DiscreteSampling.OrderedHeatBath.ordered_heat_bath_invariant_not_reversible',
}
GAUSSIAN_SINGLE_BLOCK_SCOPE = {
    'scope': 'bench-paired-example-source-scope-v1',
    'id': 'sogb-053',
    'family': 'zhou-suzuki-gaussian-determinant-sign',
    'split': 'public-dev',
    'source_file': 'AutoSamplingTheory/ExampleCases/GaussianComplexity/SingleBlockSeparation.lean',
    'declaration': ('AutoSamplingTheory.ExampleCases.GaussianComplexity.'
                    'SingleBlockSeparation.single_block_separation'),
}


def check_gaussian_single_block_source(core: dict, split: str) -> None:
    """Admit one original paired core only under its exact audited closure."""
    scope = GAUSSIAN_SINGLE_BLOCK_SCOPE
    if (split != scope['split']
            or any(core.get(key) != scope[key] for key in ('id', 'family', 'source_file', 'declaration'))
            or not has_lean(core) or set(core.get('track_levels', {})) != set(TRACKS)
            or {'textbook_exercise_id', 'support_source_view', 'additional_source_declarations',
                'reference_helpers'} & core.keys()):
        raise ValueError('The Gaussian example source approval is for one exact public paired core')
    import sog_bench_review

    audit_path = SOURCE_APPROVALS / 'sogb-053.json'
    if not audit_path.is_file():
        raise ValueError('Missing Gaussian source approval')
    audit = json.loads(audit_path.read_text(encoding='utf-8'))
    pins = audit['pin_sha256_lf']
    required_pins = {'LICENSE', 'NOTICE', 'LICENSE_SCOPE.md', 'lean-toolchain', 'lake-manifest.json'}
    if (audit['schema_version'] != 1 or audit['identity'] != scope
            or audit['external_import_roots'] != ['Mathlib'] or set(pins) != required_pins
            or any(text_hash(ROOT / path) != digest for path, digest in pins.items())):
        raise ValueError('Gaussian source approval or its licensing/toolchain pins changed')
    local_context = {}
    for row in audit['modules']:
        rel = row['path']
        if (rel in local_context or re.fullmatch(r'AutoSamplingTheory/[A-Za-z0-9_/]+\.lean', rel) is None
                or not (ROOT / rel).resolve().is_relative_to(ROOT / 'AutoSamplingTheory')):
            raise ValueError('Gaussian source approval has an invalid local module')
        local_context[rel] = row['sha256_lf']
    scope_sha = sha(encoded(scope))
    expected = sha(encoded({'binding_sha256': scope_sha, 'local_context': local_context,
                             'toolchain': pins['lean-toolchain'], 'mathlib': pins['lake-manifest.json']}))
    actual = sog_bench_review.context_binding({'source_file': scope['source_file'],
                                               'binding_sha256': scope_sha})
    if expected != audit['context_sha256'] or actual != expected:
        raise ValueError('Gaussian source/import closure changed; renew the exact approval before reuse')


def owned_exercise_example_source(source_file: str) -> bool:
    """Allow route-specific original answers without widening Lean task inputs."""
    return (source_file.startswith(OWNED_EXERCISE_EXAMPLE_ROOT)
            and re.fullmatch(r'[A-Za-z0-9_/]+\.lean', source_file) is not None
            and (ROOT / source_file).resolve().is_relative_to(
                ROOT / OWNED_EXERCISE_EXAMPLE_ROOT))


def check_core_source(core: dict, split: str) -> None:
    """Enforce the owned source scopes without widening Lean task inputs."""
    source = core['source_file']
    path = Path(source)
    if path.is_absolute() or '..' in path.parts or '\\' in source:
        raise ValueError('Source path must be repository-relative')
    if source.startswith('AutoSamplingTheory/TechnicalLemmas/'):
        return
    if source == GAUSSIAN_SINGLE_BLOCK_SCOPE['source_file']:
        check_gaussian_single_block_source(core, split)
        return
    if owned_exercise_example_source(source):
        if core.get('textbook_exercise_id') and core.get('support_source_view') is True and not has_lean(core):
            return
        raise ValueError('Owned example answers are not independent Lean tasks')
    original = ORIGINAL_EXAMPLE_ANSWERS.get(source)
    if (original is not None and core.get('declaration') == original
            and split == 'public-dev' and core.get('lean_enabled') is False
            and core.get('support_source_view') is True
            and set(core.get('track_levels', {})) == {'natural-language'}
            and 'textbook_exercise_id' not in core
            and (ROOT / path).resolve().is_relative_to(ROOT / 'AutoSamplingTheory/ExampleCases')):
        return
    raise ValueError('Non-technical source requires an approved owned supporting answer')


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def encoded(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode('utf-8')


def text_hash(path: Path) -> str:
    return sha(path.read_text(encoding='utf-8').replace('\r\n', '\n').encode('utf-8'))


def load() -> dict:
    data = json.loads(DATA.read_text(encoding='utf-8'))
    if data['schema_version'] != 2 or data['split'] != 'public-dev':
        raise ValueError('This development catalog supports schema 2 and public-dev only')
    if data['review_status'] != 'independent-semantic-review-pending':
        raise ValueError('Overall catalog badge cannot replace derived per-item review evidence')
    ids = set()
    policy = curriculum.curriculum()
    for core in data['cores']:
        if not re.fullmatch(r'sogb-\d{3}', core['id']) or core['id'] in ids:
            raise ValueError('Invalid or duplicate core identity')
        ids.add(core['id'])
        if not core['family'].strip():
            raise ValueError('Missing mathematical family')
        if ('support_source_view' in core and
                (not isinstance(core['support_source_view'], bool) or
                 (core['support_source_view'] and has_lean(core)))):
            raise ValueError('Supporting-source view is Boolean and reserved for unpaired prose tasks')
        curriculum.classify(core, policy)
        for key in ('title', 'question', 'lean_explanation', 'boundary', 'source_note'):
            if not isinstance(core[key], str) or not core[key].strip():
                raise ValueError('Missing prose: ' + key)
        if not core['assumptions'] or not core['steps'] or len(core['rubric']) != 4:
            raise ValueError('Missing assumptions, proof steps or four-point rubric')
        if any(row['points'] != 1 or not row['criterion'] for row in core['rubric']):
            raise ValueError('Each rubric criterion has one point')
        check_core_source(core, data['split'])
    return data


def assigned_theorem(declaration) -> tuple[str, str]:
    """Preserve an explicit source proof (term or tactic), not an equation block."""
    # The canonical scanner can retain trailing namespace closures or the next docstring.
    code = re.split(r'\nend(?:\s|$)', declaration.source_text, maxsplit=1)[0]
    signature, proof = inline_lean.split_statement(inline_lean.display_source(code).strip())
    if (declaration.kind not in {'theorem', 'lemma'} or not proof.startswith(':=')
            or not astis_site.sanitize_lean(proof[2:]).strip()):
        raise ValueError('Bench requires a theorem with an explicit assigned proof')
    return signature, proof


def reference_helper_source(core: dict, target, known: dict) -> str:
    """Exact earlier same-namespace proofs, in the trusted answer only."""
    if 'reference_helpers' not in core:
        return ''
    names = core['reference_helpers']
    if (not isinstance(names, list) or not names or not all(isinstance(n, str) and n in known for n in names)
            or len(names) != len(set(names))):
        raise ValueError('Reference helpers must name distinct known declarations')
    helpers = [known[n] for n in names]
    lines = [d.source_line for d in helpers]
    namespace = target.full_name.rsplit('.', 1)[0]
    if (lines != sorted(set(lines)) or lines[-1] >= target.source_line
            or any(d.source_file != target.source_file or d.full_name.rsplit('.', 1)[0] != namespace
                   or d.has_placeholder for d in helpers)):
        raise ValueError('Reference helpers must be earlier checked source in the same file and namespace')
    pieces = []
    for d in helpers:
        signature, proof = assigned_theorem(d)
        if not re.match(r'^(?:private\s+)?(?:theorem|lemma)\s+' + re.escape(d.short_name) + r'\b', signature):
            raise ValueError('Unsupported reference helper declaration form')
        pieces.append(('' if signature.startswith('private ') else 'private ') + signature + ' ' + proof)
    return '\n\n'.join(pieces) + '\n\n'


def materialize(data: dict | None = None) -> list[dict]:
    data = data or load()
    known = astis_site._SOURCE_BY_NAME or {d.full_name: d for d in astis_site.scan_project_sources()[1]}
    result = []
    for core in data['cores']:
        check_core_source(core, data['split'])
        declaration = known.get(core['declaration'])
        if declaration is None or declaration.source_file != core['source_file'] or declaration.has_placeholder:
            raise ValueError('Unresolved or unfinished reference declaration: ' + core['declaration'])
        extra = {}
        if 'textbook_exercise_id' in core:
            import sog_bench_exercises
            exercise = sog_bench_exercises.resolve(core['textbook_exercise_id'], known)
            if (core['family'] != exercise['id'] or core['declaration'] not in
                    {d['declaration'] for d in exercise['answer_declarations']}):
                raise ValueError('Numbered exercise variants share their source family and actual answer anchor')
            extra['textbook_exercise'] = exercise
        if 'additional_source_declarations' in core:
            names = core['additional_source_declarations']
            if (not isinstance(names, list) or not names or
                    not all(isinstance(n, str) for n in names) or len(names) != len(set(names))):
                raise ValueError('Additional source declarations must be distinct nonempty names')
            sources = []
            for name in names:
                support = known.get(name)
                if support is None or support.has_placeholder:
                    raise ValueError('Unresolved or unfinished supporting declaration: ' + name)
                sources.append({'declaration': name, 'source_file': support.source_file,
                                'source_line': support.source_line,
                                'source_sha256_lf': text_hash(ROOT / support.source_file)})
            extra['supporting_declarations'] = sources
        if not has_lean(core):
            if 'reference_helpers' in core:
                raise ValueError('Reference helpers require an aligned Lean task')
            bound = {**core, **extra, 'split': data['split'], 'source_sha256_lf': text_hash(ROOT / core['source_file']),
                     'source_line': declaration.source_line, 'imports': [], 'lean_task': '', 'lean_reference': ''}
            if core.get('support_source_view'):
                # Exact supporting module, not another task/reference certificate.
                # Keep its original notices and namespace/ancestor context intact.
                bound['support_lean_source'] = (ROOT / core['source_file']).read_text(encoding='utf-8')
            bound['binding_sha256'] = sha(encoded(bound))
            result.append(bound)
            continue
        signature, proof = assigned_theorem(declaration)
        target = re.sub(r'^(?:theorem|lemma)\s+' + re.escape(declaration.short_name), 'example', signature, count=1)
        if target == signature:
            raise ValueError('Could not form the fixed anonymous target')
        original = (ROOT / core['source_file']).read_text(encoding='utf-8')
        imports = re.findall(r'^import ([\w.]+)\s*$', original, re.M)
        if declaration.module in imports:
            raise ValueError('Target module must not be an allowed direct import')
        header = ('/- SamplingOptimisationGeometryBench public-dev reference.\n'
                  '   Reuses the existing project proof; retain LICENSE and NOTICE. -/\n')
        prefix = header + ''.join('import ' + name + '\n' for name in imports) + '\n' + core['context'] + '\n'
        reference = prefix + reference_helper_source(core, declaration, known) + target + ' ' + proof + '\n'
        task = prefix + target + ' := by\n  -- Replace this comment with your proof.\n'
        if re.search(r'\b(sorry|admit|axiom|unsafe)\b', astis_site.sanitize_lean(reference)):
            raise ValueError('Forbidden reference proof token')
        bound = {**core, **extra, 'split': data['split'], 'source_sha256_lf': text_hash(ROOT / core['source_file']),
                 'source_line': declaration.source_line, 'imports': imports,
                 'lean_task': task, 'lean_reference': reference}
        bound['binding_sha256'] = sha(encoded(bound))
        result.append(bound)
    return result


def prompts(cores: list[dict]) -> list[dict]:
    rows = []
    for core in cores:
        common = {k: core[k] for k in ('id', 'family', 'domain', 'library_domains', 'skills', 'title', 'split', 'assumptions', 'binding_sha256')}
        if core.get('textbook_exercise'):
            import sog_bench_exercises
            common['exercise_source'] = sog_bench_exercises.source_prompt(core['textbook_exercise'])
        for track, level in core['track_levels'].items():
            question = core['question'] if track == 'natural-language' else (
                'Complete the fixed Lean target below. Keep its imports, context and proposition unchanged. '
                'Use the repository-pinned Lean/Mathlib. This is open-library reconstruction; '
                'the target module is not imported directly.\n\n' + core['lean_task'])
            rows.append({**common, 'track': track, 'level': level, 'question': question})
    return rows


def has_lean(core: dict) -> bool:
    return core.get('lean_enabled', True) is True


def editorial_review(cores: list[dict]) -> dict:
    import sog_bench_review
    return sog_bench_review.summary(cores)


def coverage(cores: list[dict], graphs: list[dict]) -> dict:
    return curriculum.coverage(cores, graphs, editorial_review(cores)['items'])


def environment_digest(cores: list[dict] | None = None) -> str:
    """Bind the actual task/source import closures, not unrelated live work."""
    import sog_bench_review
    selected = [c for c in (materialize() if cores is None else cores) if has_lean(c)]
    payload = {'scope': 'selected-source-import-closure',
               'contexts': {c['id']: sog_bench_review.context_binding(c) for c in selected},
               'lakefile_sha256_lf': text_hash(ROOT / 'lakefile.lean')}
    import sog_bench_exercises
    answer_contexts = sog_bench_exercises.compile_contexts(materialize() if cores is None else cores)
    if answer_contexts:
        payload['owned_exercise_answers'] = answer_contexts
    return sha(encoded(payload))


def receipt_current(cores: list[dict]) -> bool:
    all_cores = cores
    cores = [c for c in cores if has_lean(c)]
    import sog_bench_exercises
    answers = sog_bench_exercises.answers(all_cores)
    if not RECEIPT.is_file():
        return False
    try:
        receipt = json.loads(RECEIPT.read_text(encoding='utf-8'))
        return (receipt['schema_version'] == 1 and receipt['passed'] is True
                and receipt['environment_scope'] == 'selected-source-import-closure'
                and receipt['environment_sha256'] == environment_digest(all_cores)
                and receipt['bindings'] == {c['id']: c['binding_sha256'] for c in cores}
                and receipt['reference_sha256'] == {c['id']: sha(c['lean_reference'].encode()) for c in cores}
                and re.search(r'version 4\.33\.0(?:[, )])', receipt['compiler_version']) is not None
                and len(receipt['commands']) == len(cores) + 2 + bool(answers)
                and (not answers or (
                    receipt.get('exercise_answer_declarations') == sorted(answers)
                    and set(receipt.get('exercise_answer_axioms', {})) == set(answers)
                    and all(set(a) <= {'propext', 'Classical.choice', 'Quot.sound'}
                            for a in receipt['exercise_answer_axioms'].values())))
                and all(r['returncode'] == 0 for r in receipt['commands']))
    except (ValueError, KeyError, TypeError):
        return False


def graph_anchor(declaration: str, source_file: str, graph_ids: set[str] | None) -> tuple[str, str | None]:
    """Resolve a location against an actual graph, never against the proof status."""
    if graph_ids is None:
        return 'not-checked', None
    node = 'decl:' + declaration
    if node in graph_ids:
        return 'declaration', node
    module = 'module:' + source_file.removesuffix('.lean').replace('/', '.')
    if module in graph_ids:
        return 'owning-module', module
    return 'not-indexed', None


def graph_index_ids(path: Path) -> set[str]:
    data = json.loads(path.read_text(encoding='utf-8'))
    nodes = data.get('nodes') if isinstance(data, dict) else None
    if not isinstance(nodes, list) or any(not isinstance(n, dict) or not isinstance(n.get('id'), str)
                                         or not n['id'] for n in nodes):
        raise ValueError('Expected a generated Lean graph with node identifiers')
    ids = {n['id'] for n in nodes}
    if len(ids) != len(nodes):
        raise ValueError('Generated Lean graph contains duplicate node identifiers')
    return ids


def mathematical_scope(core: dict) -> str:
    """Keep historical staging text out of current reader and expert scope.

    The frozen input still carries the exact author's note. Admission is
    derived from reviews, never from prose in that input.
    """
    return core['boundary'].removesuffix(
        ' Draft pending independent editorial review; never include in canonical exports yet.')


def task_assets(cores: list[dict], graphs: list[dict], *, graph_ids: set[str] | None = None) -> dict[str, bytes]:
    """Portable agent inputs, separate training pairs and expert-only anchors.

    This packages existing admitted tasks; it neither invents an execution
    sandbox nor turns public-dev families into a held-out evaluation dataset.
    """
    from urllib.parse import quote
    import io
    assets, index, training, positions = {}, [], [], []
    by_id = {c['id']: c for c in cores}
    rows = prompts(cores) + curriculum.graph_prompts(graphs)
    evaluators = {'natural-language': 'tools/sog_bench_prose.py',
                  'lean': 'tools/sog_bench_lean.py',
                  'graph-json': 'tools/sog_bench_curriculum.py'}
    evaluator_hashes = {track: text_hash(ROOT / path) for track, path in evaluators.items()}
    lean_policy_hash = text_hash(DATA.parent / 'lean-runtime/policy.json')
    for row in rows:
        track = row.get('track', 'graph-json')
        stem = 'tasks/' + row['id'] + '/' + track
        prompt_path = stem + '/prompt.json'
        identity_key = 'prompt_sha256' if track == 'graph-json' else 'binding_sha256'
        identity = {identity_key: row[identity_key]}
        response = {'id': row['id'], **identity, 'attempt': 1}
        if track == 'graph-json':
            response['answer'] = {'nodes': [], 'entails_mathematical_necessity': False}
            verifier = 'exact-snapshot-json; Python3.11+; no submission code execution'
        else:
            response.update(track=track, response='')
            verifier = ('actual-human-rubric' if track == 'natural-language'
                        else 'isolated-fixed-target-lean; operator-provisioned Linux Docker/Landrun')
        environment = {'python': '3.11+', 'lean_toolchain': (ROOT / 'lean-toolchain').read_text().strip(),
                       'mathlib_manifest_sha256_lf': text_hash(ROOT / 'lake-manifest.json'),
                       'runner_source_sha256_lf': text_hash(ROOT / 'tools/sog_bench.py'),
                       'evaluator_source_sha256_lf': evaluator_hashes[track],
                       'arbitrary_submission_execution': False,
                       'retrieval_policy': 'declare before collection; not enforced by this package'}
        if track == 'lean':
            environment.update(verifier_policy_sha256_lf=lean_policy_hash,
                               verifier_included=False, hosted_execution=False)
        descriptor = {'schema_version': 2 if track == 'graph-json' else 1, 'id': row['id'], 'track': track,
                      'family': row['family'], 'split': row['split'], **identity,
                      'prompt_file': 'prompt.json', 'response_template': 'response-template.json',
                      'environment': environment, 'verifier': verifier,
                      'hidden_test': False, 'measured_model_result': False}
        assets[prompt_path] = encoded(row)
        assets[stem + '/task.json'] = encoded(descriptor)
        assets[stem + '/response-template.json'] = encoded(response)
        assets[stem + '/instruction.md'] = (
            '# ' + row['title'] + '\n\nRead prompt.json. Preserve the task identity and ' + identity_key
            + '. Write your first unedited answer using response-template.json; keep any assumptions and fixed target.\n\n'
            'No gold answer is included in this task package.\n'
            + ('The operator must provision the isolated Linux Docker/Landrun fixed-target verifier separately. '
               'It is not included in this ZIP or hosted by the site. Never run untrusted Lean on the host.\n'
               if track == 'lean' else '')
        ).encode('utf-8')
        index.append({'id': row['id'], 'track': track, 'family': row['family'],
                      'level': row['level'], 'library_domains': row['library_domains'],
                      **identity, 'task_file': stem + '/task.json',
                      'prompt_file': prompt_path, 'verifier': verifier})
        if track != 'graph-json':
            core = by_id[row['id']]
            answer = '\n\n'.join(core['steps']) if track == 'natural-language' else core['lean_reference']
            training.append({'id': row['id'], 'track': track, 'family': row['family'],
                             'split': 'public-dev', 'binding_sha256': row['binding_sha256'],
                             'usage': 'public curriculum reuse; never an unseen test',
                             'messages': [{'role': 'user', 'content': encoded(row).decode('utf-8')},
                                          {'role': 'assistant', 'content': answer}]})
    for core in cores:
        kind, node = graph_anchor(core['declaration'], core['source_file'], graph_ids)
        related = [{'declaration': d['declaration'], 'role': 'additional-formal-support-not-aligned-QA'}
                   for d in core.get('supporting_declarations', [])]
        related += [{'declaration': d['declaration'], 'role': 'owned-textbook-core-answer', 'supports': d['supports']}
                    for d in core.get('textbook_exercise', {}).get('answer_declarations', [])]
        positions.append({'id': core['id'], 'node_id': node, 'source_file': core['source_file'],
                          'anchor_kind': kind,
                          'declaration': core['declaration'], 'binding_sha256': core['binding_sha256'],
                          'graph_url': ('../../../underlying-lean-graph/index.html?focus=' + quote(node, safe='')
                                        if node is not None else None),
                          'aligned_fixed_lean_task': has_lean(core), 'audience': 'expert-review-not-model-input',
                          'related_owned_results': related,
                          'boundary': mathematical_scope(core),
                          'edge_semantics': 'position only; no inferred proof-dependency or necessity'})
    assets['task-index.json'] = encoded({'schema_version': 2, 'name': 'SamplingOptimisationGeometryBench',
        'catalog_version': load()['version'], 'split': 'public-dev', 'hidden_test': False,
        'tasks': index, 'note': 'Only currently editorially admitted tasks. Family identity is not a train/test split.'})
    # The model-facing ZIP contains no gold, expert source anchors or review reports.
    payload = io.BytesIO()
    model_files = {**assets, **{name: (ROOT / name).read_bytes() for name in project_licensing.LICENSE_FILES}}
    assets['task-files.sha256.json'] = encoded({'schema_version': 1,
        'scope': 'prompt-only agent package; no gold answers or expert source anchors',
        'files': {name: sha(value) for name, value in sorted(model_files.items())}})
    model_files['task-files.sha256.json'] = assets['task-files.sha256.json']
    with zipfile.ZipFile(payload, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for name, content in sorted(model_files.items()):
            member = zipfile.ZipInfo(name, date_time=(2020, 1, 1, 0, 0, 0))
            member.compress_type = zipfile.ZIP_DEFLATED
            member.external_attr = 0o100644 << 16
            archive.writestr(member, content)
    assets['agent-tasks.zip'] = payload.getvalue()
    # Full operator package includes oracle/verifier answers. Add it only AFTER
    # sealing the prompt-only archive, never to model-facing files or manifests.
    import sog_bench_harbor
    assets['harbor-graph-tasks.zip'] = sog_bench_harbor.archive(graphs)
    assets['training-pairs.jsonl'] = ''.join(json.dumps(r, ensure_ascii=False, sort_keys=True)+'\n' for r in training).encode('utf-8')
    assets['expert-graph-positions.json'] = encoded(positions)
    assets['examples/graph-run.json'] = encoded({
        'run_id': 'REPLACE_WITH_YOUR_RUN_ID', 'model': 'REPLACE_WITH_ACTUAL_MODEL',
        'model_version': 'REPLACE_WITH_ACTUAL_VERSION', 'created_at': 'REPLACE_WITH_ISO8601_TIME_AND_TIMEZONE',
        'track': 'graph-json', 'prompt_profile': 'given-snapshot', 'attempt_policy': 'first-attempt',
        'tools': [], 'seed': None, 'task_ids': [g['id'] for g in graphs]})
    return assets


def selected_graph_tasks(graphs: list[dict], metadata: dict) -> list[dict]:
    """Predeclared subsets retain a fixed denominator; legacy runs use all tasks."""
    identities = metadata.get('task_ids')
    if identities is None:
        return graphs
    known = {g['id']: g for g in graphs}
    if (not isinstance(identities, list) or not identities
            or not all(isinstance(i, str) and i in known for i in identities)
            or len(set(identities)) != len(identities)):
        raise ValueError('task_ids must be a nonempty, unique list of current graph IDs declared before collection')
    return [known[i] for i in identities]


def export(output: Path, cores: list[dict] | None = None, *, graph_ids: set[str] | None = None) -> None:
    cores = cores or materialize()
    graphs = curriculum.graph_items()
    review = editorial_review(cores)
    import sog_bench_graph_review
    graph_review = sog_bench_graph_review.summary(graphs)
    reviewed_graphs=[g for g in graphs if graph_review['items'][g['id']]['editorial'] in {'accepted','accepted-after-repair'}]
    reviewed = [c for c in cores if review['items'][c['id']]['editorial'] in {'accepted', 'accepted-after-repair'}]
    task_files = task_assets(reviewed, reviewed_graphs, graph_ids=graph_ids)
    import sog_bench_graph_slices
    compiler_snapshots = sog_bench_graph_slices.snapshots()
    expected = {'questions.jsonl', 'reference.jsonl', 'manifest.json', 'README.md',
                'editorial-review.json', 'graph-editorial-review.json', 'reviewed-questions.jsonl', 'reviewed-reference.jsonl',
                'curriculum.json', 'coverage.json', 'graph-questions.jsonl', 'graph-reference.jsonl', 'GOAL.md',
                'reviewed-graph-questions.jsonl','reviewed-graph-reference.jsonl',
                'EVALUATION.md', 'FAMILY_ISOLATION.md', 'ECOSYSTEM.md', 'HARBOR.md', 'TEXTBOOK_EXERCISES.md',
                'textbook-exercise-map.json', 'examples/prose-run.json',
                *compiler_snapshots,
                *project_licensing.LICENSE_FILES, *task_files,
                *('lean/' + c['id'] + '-support.lean' for c in cores if c.get('support_source_view')),
                *('lean/' + c['id'] + suffix for c in cores if has_lean(c) for suffix in ('-task.lean.txt', '-reference.lean'))}
    if output.exists() and any(output.iterdir()):
        manifest = output / 'manifest.json'
        if not manifest.is_file() or json.loads(manifest.read_text(encoding='utf-8')).get('name') != 'SamplingOptimisationGeometryBench':
            raise ValueError('Use an empty output directory or an existing managed Bench export')
        if any(p.is_symlink() or (p.is_file() and p.relative_to(output).as_posix() not in expected)
               for p in output.rglob('*')):
            raise ValueError('Unexpected export files; use a fresh directory (nothing was deleted)')
    output.mkdir(parents=True, exist_ok=True)
    write = lambda path, value: (output / path).write_bytes(value)
    jsonl = lambda rows: ''.join(json.dumps(r, ensure_ascii=False, sort_keys=True) + '\n' for r in rows).encode()
    def operator_guide(name):
        # Keep repository-only setup and audit links useful after download.
        # None of these operator guides are inside the prompt-only ZIP.
        url = 'https://github.com/DakeBU/Automization-Sampling-Optimisation-Geometry-Lib/blob/main/'
        text = (DATA.parent / name).read_text(encoding='utf-8')
        text = re.sub(r'\]\(((?:reviews|lean-runtime)/[^)]+)\)',
                      lambda m: f']({url}benchmarks/samplingoptimisationgeometrybench/{m[1]})', text)
        text = re.sub(r'\]\(\.\./\.\./((?:docs|runs)/[^)]+)\)', r'](' + url + r'\1)', text)
        return text.encode('utf-8')
    write('questions.jsonl', jsonl(prompts(cores)))
    for name, content in task_files.items():
        (output / name).parent.mkdir(parents=True, exist_ok=True)
        write(name, content)
    write('reference.jsonl', jsonl(cores))
    write('editorial-review.json', encoded(review))
    write('graph-editorial-review.json', encoded(graph_review))
    for name, snapshot in compiler_snapshots.items():
        write(name, encoded(snapshot))
    write('reviewed-questions.jsonl', jsonl(prompts(reviewed)))
    write('reviewed-reference.jsonl', jsonl(reviewed))
    write('graph-questions.jsonl', jsonl(curriculum.graph_prompts(graphs)))
    write('graph-reference.jsonl', jsonl(graphs))
    write('reviewed-graph-questions.jsonl',jsonl(curriculum.graph_prompts(reviewed_graphs)))
    write('reviewed-graph-reference.jsonl',jsonl(reviewed_graphs))
    write('curriculum.json', encoded(curriculum.curriculum()))
    write('coverage.json', encoded(coverage(cores, graphs)))
    write('GOAL.md', (DATA.parent / 'GOAL.md').read_bytes())
    write('EVALUATION.md', (DATA.parent / 'EVALUATION.md').read_bytes())
    # Public operator instructions only; never enumerate or read reservations.
    write('FAMILY_ISOLATION.md', (DATA.parent / 'FAMILY_ISOLATION.md').read_bytes())
    write('ECOSYSTEM.md', operator_guide('ECOSYSTEM.md'))
    write('HARBOR.md', (DATA.parent / 'HARBOR.md').read_bytes())
    # Source intake is documentation, not an admitted QA or copied source text.
    write('TEXTBOOK_EXERCISES.md', (DATA.parent / 'TEXTBOOK_EXERCISES.md').read_bytes())
    import sog_bench_exercises
    exercises = sog_bench_exercises.projection(cores, review['items'], receipt_current(cores))
    write('textbook-exercise-map.json', encoded(exercises))
    (output / 'examples').mkdir(exist_ok=True)
    write('examples/prose-run.json', (DATA.parent / 'examples/prose-run.json').read_bytes())
    (output / 'lean').mkdir(exist_ok=True)
    for c in cores:
        if c.get('support_source_view'):
            write('lean/' + c['id'] + '-support.lean', c['support_lean_source'].encode())
        if not has_lean(c):
            continue
        write('lean/' + c['id'] + '-task.lean.txt', c['lean_task'].encode())
        write('lean/' + c['id'] + '-reference.lean', c['lean_reference'].encode())
    for name in project_licensing.LICENSE_FILES:
        write(name, (ROOT / name).read_bytes())
    write('README.md', operator_guide('README.md'))
    manifest = {'name': 'SamplingOptimisationGeometryBench', 'version': load()['version'],
                'split': 'public-dev', 'cores': len(cores), 'qa_views': len(prompts(cores)), 'graph_tasks': len(graphs),
                'track_counts': {t: sum(t in c['track_levels'] for c in cores) for t in TRACKS},
                'difficulty_calibration': 'author-assigned; not empirically calibrated',
                'independent_semantic_review': 'see content-bound mathematical and structural editorial reports; not empirical calibration',
                'hidden_test': False,
                'textbook_exercise_programme': 'See textbook-exercise-map.json and TEXTBOOK_EXERCISES.md; source intake is not QA admission or full exercise formalization',
                'numbered_textbook_exercises': len(exercises),
                'editorial_admitted_numbered_exercises': sum(
                    any(q['editorial'] in {'accepted', 'accepted-after-repair'} for q in e['questions']) for e in exercises),
                'prose_scoring': 'offline human-attested single or panel rubric records; execution and judgments not automatically verified',
                'editorial_accepted_cores': len(reviewed),
                'editorial_review_complete_for_current_mathematical_cores': bool(cores) and len(reviewed) == len(cores),
                'review_kind': 'AI editorial review, not full Lean coverage or canonical theorem publication',
                'editorial_accepted_graph_tasks': graph_review['accepted_tasks'],
                'graph_evidence_kinds':sorted({g['context']['kind'] for g in graphs}),
                'compiled_graph_scope':'recorded source-bound proof-body occurrences and whitelisted unexpanded-statement profiles; fresh replay is separate, not full closure, binder-role analysis or mathematical necessity',
                'toolchain': (ROOT / 'lean-toolchain').read_text().strip(),
                'mathlib_manifest_sha256_lf': text_hash(ROOT / 'lake-manifest.json'),
                'files': {p.relative_to(output).as_posix(): sha(p.read_bytes())
                          for p in sorted(output.rglob('*')) if p.is_file() and p.name != 'manifest.json'}}
    write('manifest.json', encoded(manifest))


def archive_bytes(directory: Path, destination: Path) -> None:
    """Stable member order, timestamps and permissions; no machine paths."""
    with zipfile.ZipFile(destination, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(directory.rglob('*')):
            if path.is_file():
                info = zipfile.ZipInfo(path.relative_to(directory).as_posix(), (1980, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o644 << 16
                archive.writestr(info, path.read_bytes())


def check_lean(cores: list[dict]) -> int:
    """Trusted references and named owned answers, never submitted code."""
    all_cores = cores
    import sog_bench_exercises
    answers = sog_bench_exercises.answers(all_cores)
    cores = [c for c in cores if has_lean(c)]
    if not cores and not answers:
        raise ValueError('No trusted Lean tasks or named owned exercise answers to compile')
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT.unlink(missing_ok=True)  # Invalidate only this generated receipt before any attempt.
    before = environment_digest(all_cores)
    commands = []
    compiler_version = ''
    last_output = ''
    def run(command):
        nonlocal compiler_version, last_output
        print('Checking:', ' '.join(command), flush=True)
        result = subprocess.run(command, cwd=ROOT, text=True, encoding='utf-8', errors='replace',
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=600)
        print(result.stdout, end='', flush=True)
        last_output = result.stdout
        if command == ['lake', 'env', 'lean', '--version']:
            compiler_version = result.stdout.strip()
        commands.append({'command': command, 'returncode': result.returncode})
        return result.returncode
    if (ROOT / 'lean-toolchain').read_text().strip() != 'leanprover/lean4:v4.33.0':
        raise ValueError('Pilot requires the repository-pinned Lean 4.33.0')
    if run(['lake', 'env', 'lean', '--version']) or not re.search(r'version 4\.33\.0(?:[, )])', compiler_version):
        raise ValueError('Effective compiler differs from Lean 4.33.0; check ELAN_TOOLCHAIN/overrides')
    imports = sorted({m for c in cores for m in c['imports']} |
                     {r['source_file'].removesuffix('.lean').replace('/', '.') for r in answers.values()})
    if run(['lake', 'build', *imports]):
        return 1
    with tempfile.TemporaryDirectory(prefix='trusted-', dir=RECEIPT.parent) as tmp:
        for core in cores:
            path = Path(tmp) / (core['id'] + '.lean')
            path.write_text(core['lean_reference'], encoding='utf-8', newline='\n')
            if run(['lake', 'env', 'lean', path.relative_to(ROOT).as_posix()]):
                return 1
        answer_axioms = {}
        if answers:
            path = Path(tmp) / 'owned-exercise-answers.lean'
            path.write_text(sog_bench_exercises.probe(all_cores), encoding='utf-8', newline='\n')
            if run(['lake', 'env', 'lean', path.relative_to(ROOT).as_posix()]):
                return 1
            answer_axioms = sog_bench_exercises.checked_axioms(last_output, answers)
    if environment_digest(all_cores) != before:
        raise ValueError('Selected source/import contexts changed during checking; no receipt written')
    receipt = {'schema_version': 1, 'passed': True, 'environment_sha256': before,
               'environment_scope': 'selected-source-import-closure',
               'compiler_version': compiler_version,
               'bindings': {c['id']: c['binding_sha256'] for c in cores},
               'reference_sha256': {c['id']: sha(c['lean_reference'].encode()) for c in cores},
               'commands': commands, 'scope': 'trusted reference compilation only; no semantic or submission certification'}
    if answers:
        receipt['exercise_answer_declarations'] = sorted(answers)
        receipt['exercise_answer_axioms'] = answer_axioms
        receipt['scope'] = 'trusted QA references plus named owned exercise-answer modules; not equivalent QA or full source alignment'
    RECEIPT.write_bytes(encoded(receipt))
    print(f'{len(cores)} trusted references checked; compilation does not certify editorial review or full explanatory coverage.')
    if answers:
        print(f'{len(answers)} named owned exercise-answer declarations checked separately; no aligned challenge or new leaf credit.')
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('check', 'export', 'check-lean', 'coverage', 'grade-graph'))
    parser.add_argument('--output', type=Path, default=ROOT / '.astis/sog-bench-export')
    parser.add_argument('--graph-index', type=Path, help='For export: actual generated underlying-lean-graph.json')
    parser.add_argument('--submissions', type=Path, help='First-attempt structured graph responses only; never executable code')
    parser.add_argument('--run-metadata', type=Path, help='Required provenance for a graph score report')
    parser.add_argument('--legacy-graph-bindings', action='store_true',
                        help='Replay archived graph responses with the old operator binding, not a new trial')
    args = parser.parse_args()
    if args.graph_index is not None and args.command != 'export':
        parser.error('--graph-index applies only to export')
    if args.legacy_graph_bindings and args.command != 'grade-graph':
        parser.error('--legacy-graph-bindings applies only to grade-graph')
    cores = materialize()
    graphs = curriculum.graph_items()
    if args.command == 'coverage':
        print(encoded(coverage(cores, graphs)).decode('utf-8'))
        return 0
    if args.command == 'grade-graph':
        if not args.submissions or not args.run_metadata:
            parser.error('grade-graph requires --submissions and --run-metadata')
        metadata = curriculum.parse_graph_record(args.run_metadata.read_text(encoding='utf-8'))
        curriculum.validate_run_metadata(metadata)
        graphs = selected_graph_tasks(graphs, metadata)
        rows = [curriculum.parse_graph_record(line)
                for line in args.submissions.read_text(encoding='utf-8').splitlines() if line.strip()]
        bound = curriculum.bind_graph_submissions(graphs, rows, allow_legacy=args.legacy_graph_bindings)
        report = {**curriculum.grade_graph(graphs, bound), 'run_metadata': metadata,
                  'catalog_version': load()['version'], 'raw_submissions': rows,
                  'frozen_graph_items': graphs,
                  'question_bindings': {g['id']: g['binding_sha256'] for g in graphs},
                  'public_prompt_bindings': {g['id']: curriculum.graph_prompt(g)['prompt_sha256'] for g in graphs},
                  'legacy_graph_binding_used': any('binding_sha256' in row for row in rows),
                  'grader_sha256_lf': text_hash(ROOT / 'tools/sog_bench_curriculum.py'),
                  'execution_policy_verified': False}
        report['selection_scope'] = ('predeclared-task-subset; not a full-suite score'
                                     if metadata.get('task_ids') is not None else 'all-current-graph-tasks')
        args.output.mkdir(parents=True, exist_ok=True)
        destination = args.output / 'graph-score.json'
        if destination.exists():
            raise ValueError('Refusing to overwrite an existing run report; choose a fresh output directory')
        destination.write_bytes(encoded(report))
        print('Wrote structured-graph-only score; not a prose or Lean correctness score.')
        return 0
    if args.command == 'check-lean':
        return check_lean(cores)
    if args.command == 'export':
        export(args.output, cores, graph_ids=graph_index_ids(args.graph_index) if args.graph_index else None)
    reviewed = editorial_review(cores)['accepted_cores']
    import sog_bench_graph_review
    graph_accepted=sog_bench_graph_review.summary(graphs)['accepted_tasks']
    print(f'{len(cores)} public development cores / {len(prompts(cores))} mathematical QA views / {len(graphs)} graph tasks; {reviewed} mathematical cores and {graph_accepted} graph tasks editorially accepted; empirical calibration pending.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
