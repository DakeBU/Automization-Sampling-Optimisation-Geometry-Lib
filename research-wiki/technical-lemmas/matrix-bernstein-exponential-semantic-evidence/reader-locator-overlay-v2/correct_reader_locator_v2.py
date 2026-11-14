"""Separate metadata-only source locator overlay; preserve all v1 evidence."""
from pathlib import Path
import hashlib, json, subprocess, sys
sys.path.insert(0, 'tools')
import astis_publication as pub
W = Path(__file__).resolve().parent.relative_to(Path.cwd())
E = Path('research-wiki/technical-lemmas/matrix-bernstein-exponential-semantic-evidence')
ident = 'huanjian-matrix-bernstein-exponential'
LP = Path('website/content/declaration_lessons') / (ident + '.json')
A = Path('research-wiki/semantic-roundtrip/audits') / (ident + '.json')
T = Path('Tests/GaussianComplexityBernsteinMgf.lean')
P = Path('AutoSamplingTheory/TechnicalLemmas/Probability/MatrixBernsteinExponential.lean')
sha = lambda b: hashlib.sha256(b).hexdigest()
dump = lambda o: (json.dumps(o, ensure_ascii=False, indent=2) + '\n').encode()
git = lambda *a: subprocess.check_output(['git', *a])
def create(p, b):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('xb') as f:
        f.write(b)
head = git('rev-parse', 'HEAD').decode().strip()
assert head == '578e139eb2bf253188a0aeb8b7de14d82264e0a7'
assert not git('diff', 'HEAD', '--name-only') and not git('diff', '--cached', '--name-only')
orig = LP.read_bytes()
lesson = json.loads(orig)
sources = lesson['units'][0]['sources']
target = next(s for s in sources if s.get('path') == str(T))
assert target['line'] == 54
assert T.read_text().splitlines()[56].startswith('private theorem actual_source_normalized_single_summand_mgf')
target['line'] = 57
LP.write_bytes(dump(lesson))
data = pub.inputs()
live = next(x for x in pub.load() if x['id'] == ident)
binding = live['bindings'][0]
ctx = pub.review_context(live, binding, data)
bh = pub.binding_digest(live, binding, data)
a = json.loads(A.read_bytes())
assert a['source_review']['state'] == 'pending'
oldp = a['publication_binding_sha256']
a['publication_context'] = ctx
a['publication_binding_sha256'] = bh
A.write_bytes(dump(a))
ta = json.loads((W / 'private-consumer-audit.reconstructed.v1.json').read_bytes())
oldt = ta['publication_binding_sha256']
ta['publication_context']['canonical_public_producer_context'] = ctx
ta['publication_binding_sha256'] = sha(json.dumps(ta['publication_context'], ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode())
create(W / 'private-consumer-audit.reconstructed.v2.json', dump(ta))
create(W / 'private-consumer-registry.reconstructed.v2.json', dump({'schema_version': 1, 'audits': [ta]}))
subprocess.run(['python3', 'tools/astis_semantic_roundtrip.py', 'reviewer-packet', '--audit-id',
                'ASTIS-RT-20261114-HuanjianMatrixBernsteinExponential', '--output', str(W / 'P.reviewer-packet.v2.json')], check=True)
subprocess.run(['python3', 'tools/astis_semantic_roundtrip.py', '--registry', str(W / 'private-consumer-registry.reconstructed.v2.json'),
                'reviewer-packet', '--audit-id', 'ASTIS-RT-20261114-HuanjianMatrixBernsteinExponentialPrivateConsumer',
                '--output', str(W / 'T.reviewer-packet.v2.json')], check=True)
dest = E / 'reader-locator-overlay-v2'
create(dest / 'lesson.v1.original.json', orig)
record = {'kind': 'METADATA_ONLY_LOCATOR_CORRECTION;INDEPENDENT_V2_PACKET_REVIEW_PENDING',
          'original_reader_commit': head, 'source_review_note': 'Complete private theorem starts at line57; original lesson pointed at line54 inside the preceding helper.',
          'only_authored_lesson_delta': {'path': str(LP), 'json_field': 'units[0].sources[path=Tests/GaussianComplexityBernsteinMgf.lean].line', 'before': 54, 'after': 57},
          'lesson_before_sha256': sha(orig), 'lesson_after_sha256': sha(LP.read_bytes()),
          'P_binding_before': oldp, 'P_binding_after': bh,
          'T_binding_before': oldt, 'T_binding_after': ta['publication_binding_sha256'],
          'P_sha256_unchanged': sha(P.read_bytes()), 'T_sha256_unchanged': sha(T.read_bytes()),
          'unchanged': 'All theorem signatures, code, assumptions, mathematical text/formulas, seven exact source folds, anonymous packets and reconstructions, primary source and source-map bytes.',
          'not_source_repair': 'No mathematical statement/definition alteration; only a source reader locator changed. V1 static review originals and minor note retained.'}
create(dest / 'correction.json', dump(record))
for name in ['correct_reader_locator_v2.py', 'private-consumer-audit.reconstructed.v2.json',
             'private-consumer-registry.reconstructed.v2.json', 'P.reviewer-packet.v2.json', 'T.reviewer-packet.v2.json']:
    create(dest / name, (W / name).read_bytes())
paths = [LP, A, *[p for p in sorted(dest.rglob('*')) if p.is_file()]]
spec = W / 'reader-locator-v2-paths.private.nul'
create(spec, b'\0'.join(str(p).encode() for p in paths) + b'\0')
subprocess.run(['git', 'add', '-f', '--pathspec-from-file=' + str(spec), '--pathspec-file-nul'], check=True)
assert set(git('diff', '--cached', '--name-only').decode().splitlines()) == set(map(str, paths))
subprocess.run(['git', 'diff', '--cached', '--check', '--', str(LP), str(A)], check=True)
subprocess.run(['git', 'commit', '--quiet', '-m', 'Correct private MGF reader locator with separately reviewable metadata overlay'], check=True)
out = {'reader_locator_candidate_commit': git('rev-parse', 'HEAD').decode().strip(),
       'mathematical_code_changes': 0, 'normal_API_calls': 0, 'P_binding': bh, 'T_binding': ta['publication_binding_sha256']}
create(W / 'actual-reader-locator-v2-commit.json', dump(out))
print(json.dumps(out))
