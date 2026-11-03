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

DATA = ROOT / 'benchmarks/samplingoptimisationgeometrybench/cores.json'
RECEIPT = ROOT / '.astis/sog-bench/reference-check.json'
TRACKS = ('natural-language', 'lean')


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def encoded(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode('utf-8')


def text_hash(path: Path) -> str:
    return sha(path.read_text(encoding='utf-8').replace('\r\n', '\n').encode('utf-8'))


def load() -> dict:
    data = json.loads(DATA.read_text(encoding='utf-8'))
    if data['schema_version'] != 1 or data['split'] != 'public-dev':
        raise ValueError('This pilot supports schema 1 and public-dev only')
    if data['review_status'] != 'independent-semantic-review-pending':
        raise ValueError('Reviewed admission needs a future evidence-backed schema, not an edited badge')
    ids, families = set(), set()
    for core in data['cores']:
        if not re.fullmatch(r'sogb-\d{3}', core['id']) or core['id'] in ids:
            raise ValueError('Invalid or duplicate core identity')
        ids.add(core['id'])
        if core['family'] in families:
            raise ValueError('Pilot reserves one shared core per family')
        families.add(core['family'])
        if core['domain'] not in {'sampling', 'optimisation', 'geometry'}:
            raise ValueError('Invalid pilot domain')
        for key in ('title', 'question', 'context', 'lean_explanation', 'boundary', 'source_note'):
            if not isinstance(core[key], str) or not core[key].strip():
                raise ValueError('Missing prose: ' + key)
        if not core['assumptions'] or not core['steps'] or len(core['rubric']) != 4:
            raise ValueError('Missing assumptions, proof steps or four-point rubric')
        if any(row['points'] != 1 or not row['criterion'] for row in core['rubric']):
            raise ValueError('Each rubric criterion has one point')
        source = Path(core['source_file'])
        if source.is_absolute() or '..' in source.parts or '\\' in core['source_file']:
            raise ValueError('Source path must be repository-relative')
        if not core['source_file'].startswith('AutoSamplingTheory/TechnicalLemmas/'):
            raise ValueError('Only the local technical-lemma owner is supported')
    return data


def materialize(data: dict | None = None) -> list[dict]:
    data = data or load()
    known = astis_site._SOURCE_BY_NAME or {d.full_name: d for d in astis_site.scan_project_sources()[1]}
    result = []
    for core in data['cores']:
        declaration = known.get(core['declaration'])
        if declaration is None or declaration.source_file != core['source_file'] or declaration.has_placeholder:
            raise ValueError('Unresolved or unfinished reference declaration: ' + core['declaration'])
        # The canonical scanner retains trailing namespace closures; these are
        # not part of the target example. Preserve the theorem itself verbatim.
        code = re.split(r'\nend(?:\s|$)', declaration.source_text, maxsplit=1)[0]
        code = inline_lean.display_source(code).strip()
        signature, proof = inline_lean.split_statement(code)
        if not proof.startswith(':= by') or declaration.kind not in {'theorem', 'lemma'}:
            raise ValueError('Pilot requires an explicit tactic-proof theorem')
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
        reference = prefix + target + ' ' + proof + '\n'
        task = prefix + target + ' := by\n  -- Replace this comment with your proof.\n'
        if re.search(r'\b(sorry|admit|axiom|unsafe)\b', astis_site.sanitize_lean(reference)):
            raise ValueError('Forbidden reference proof token')
        bound = {**core, 'split': data['split'], 'source_sha256_lf': text_hash(ROOT / core['source_file']),
                 'source_line': declaration.source_line, 'imports': imports,
                 'lean_task': task, 'lean_reference': reference}
        bound['binding_sha256'] = sha(encoded(bound))
        result.append(bound)
    return result


def prompts(cores: list[dict]) -> list[dict]:
    rows = []
    for core in cores:
        common = {k: core[k] for k in ('id', 'family', 'domain', 'title', 'split', 'assumptions', 'binding_sha256')}
        for track in TRACKS:
            question = core['question'] if track == 'natural-language' else (
                'Complete the fixed Lean target below. Keep its imports, context and proposition unchanged. '
                'Use the repository-pinned Lean/Mathlib. This is open-library reconstruction; '
                'the target module is not imported directly.\n\n' + core['lean_task'])
            rows.append({**common, 'track': track, 'question': question})
    return rows


def environment_digest() -> str:
    """Conservatively invalidate a trusted receipt after any local Lean edit."""
    paths = [ROOT / 'lean-toolchain', ROOT / 'lake-manifest.json', ROOT / 'lakefile.lean',
             *sorted((ROOT / 'AutoSamplingTheory').rglob('*.lean'))]
    return sha(encoded([(p.relative_to(ROOT).as_posix(), text_hash(p)) for p in paths]))


def receipt_current(cores: list[dict]) -> bool:
    if not RECEIPT.is_file():
        return False
    try:
        receipt = json.loads(RECEIPT.read_text(encoding='utf-8'))
        return (receipt['schema_version'] == 1 and receipt['passed'] is True
                and receipt['environment_sha256'] == environment_digest()
                and receipt['bindings'] == {c['id']: c['binding_sha256'] for c in cores}
                and receipt['reference_sha256'] == {c['id']: sha(c['lean_reference'].encode()) for c in cores}
                and re.search(r'version 4\.33\.0(?:[, )])', receipt['compiler_version']) is not None
                and len(receipt['commands']) == len(cores) + 2
                and all(r['returncode'] == 0 for r in receipt['commands']))
    except (ValueError, KeyError, TypeError):
        return False


def export(output: Path, cores: list[dict] | None = None) -> None:
    cores = cores or materialize()
    expected = {'questions.jsonl', 'reference.jsonl', 'manifest.json', 'README.md',
                *project_licensing.LICENSE_FILES,
                *('lean/' + c['id'] + suffix for c in cores for suffix in ('-task.lean.txt', '-reference.lean'))}
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
    write('questions.jsonl', jsonl(prompts(cores)))
    write('reference.jsonl', jsonl(cores))
    (output / 'lean').mkdir(exist_ok=True)
    for c in cores:
        write('lean/' + c['id'] + '-task.lean.txt', c['lean_task'].encode())
        write('lean/' + c['id'] + '-reference.lean', c['lean_reference'].encode())
    for name in project_licensing.LICENSE_FILES:
        write(name, (ROOT / name).read_bytes())
    write('README.md', (DATA.parent / 'README.md').read_bytes())
    manifest = {'name': 'SamplingOptimisationGeometryBench', 'version': load()['version'],
                'split': 'public-dev', 'cores': len(cores), 'qa_views': 2 * len(cores),
                'independent_semantic_review': 'pending', 'hidden_test': False,
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
    """Trusted references only. Never accepts or executes submitted code."""
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT.unlink(missing_ok=True)  # Invalidate only this generated receipt before any attempt.
    before = environment_digest()
    commands = []
    compiler_version = ''
    def run(command):
        nonlocal compiler_version
        print('Checking:', ' '.join(command), flush=True)
        result = subprocess.run(command, cwd=ROOT, text=True, encoding='utf-8', errors='replace',
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=600)
        print(result.stdout, end='', flush=True)
        if command == ['lake', 'env', 'lean', '--version']:
            compiler_version = result.stdout.strip()
        commands.append({'command': command, 'returncode': result.returncode})
        return result.returncode
    if (ROOT / 'lean-toolchain').read_text().strip() != 'leanprover/lean4:v4.33.0':
        raise ValueError('Pilot requires the repository-pinned Lean 4.33.0')
    if run(['lake', 'env', 'lean', '--version']) or not re.search(r'version 4\.33\.0(?:[, )])', compiler_version):
        raise ValueError('Effective compiler differs from Lean 4.33.0; check ELAN_TOOLCHAIN/overrides')
    imports = sorted({m for c in cores for m in c['imports']})
    if run(['lake', 'build', *imports]):
        return 1
    with tempfile.TemporaryDirectory(prefix='trusted-', dir=RECEIPT.parent) as tmp:
        for core in cores:
            path = Path(tmp) / (core['id'] + '.lean')
            path.write_text(core['lean_reference'], encoding='utf-8', newline='\n')
            if run(['lake', 'env', 'lean', path.relative_to(ROOT).as_posix()]):
                return 1
    if environment_digest() != before:
        raise ValueError('Lean sources changed during checking; no receipt written')
    receipt = {'schema_version': 1, 'passed': True, 'environment_sha256': before,
               'compiler_version': compiler_version,
               'bindings': {c['id']: c['binding_sha256'] for c in cores},
               'reference_sha256': {c['id']: sha(c['lean_reference'].encode()) for c in cores},
               'commands': commands, 'scope': 'trusted reference compilation only; no semantic or submission certification'}
    RECEIPT.write_bytes(encoded(receipt))
    print('Three trusted references checked; independent QA semantic review remains pending.')
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('check', 'export', 'check-lean'))
    parser.add_argument('--output', type=Path, default=ROOT / '.astis/sog-bench-export')
    args = parser.parse_args()
    cores = materialize()
    if args.command == 'check-lean':
        return check_lean(cores)
    if args.command == 'export':
        export(args.output, cores)
    print(f'{len(cores)} public development cores / {len(prompts(cores))} QA views; independent semantic review pending.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
