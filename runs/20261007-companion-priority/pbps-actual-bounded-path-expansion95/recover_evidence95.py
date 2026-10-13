"""Recover historical lesson by reversing its sole recorded edit and hash-checking."""
from pathlib import Path
import ast, copy, gzip, hashlib, json
root=Path(__file__).resolve().parents[3]
run=Path(__file__).resolve().parent
lesson=root/'website/content/declaration_lessons/pbps-actual-bounded-path-expansion.json'
raw=lesson.read_bytes()
assert hashlib.sha256(raw).hexdigest()=='03865149346ac52dba583e0cea2f369e4355ffc2ae8be708173d0b22abd7c0cc'
tree=ast.parse((run/'prepare_review95.py').read_text(encoding='utf8'))
calls=[n for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='step' and isinstance(n.args[0],ast.Constant) and n.args[0].value=='Sum the measurable count partition']
assert len(calls)==1
old_text=ast.literal_eval(calls[0].args[1])
obj=json.loads(raw)
obj['units'][0]['steps'][3]['text']=old_text
recovered=(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode()
expected=json.loads((run/'exposition-revision95.json').read_bytes())['old_lesson_raw_sha256']
assert hashlib.sha256(recovered).hexdigest()==expected
p=run/'pre-step4-lesson95.recovered.exactraw.json.gz'
assert not p.exists()
p.write_bytes(gzip.compress(recovered,mtime=0))
cell=root/'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-bounded-path-expansion.json'
c=json.loads(cell.read_bytes())
assert 'conceptual_mirror_audit' not in c
evidence=json.loads((run/'proved-local-evidence95.json').read_bytes())
c['conceptual_mirror_audit']=copy.deepcopy(evidence['conceptual_mirror_audit'])
cell.write_bytes((json.dumps(c,ensure_ascii=False,indent=2)+'\n').encode())
receipt=dict(kind='exact-hash-checked-historical-recovery',archive=p.relative_to(root).as_posix(),decoded_raw_sha256=expected,archive_raw_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),method='Reverse only step4.text using original prepare_review95.py literal; canonical JSON serialization exactly matches pre-existing independent historical RAW pin.',historical_archive_created_now=True,current_lesson_unchanged=True,conceptual_mirror_audit_transfer='Copied existing proved-local-evidence95.json audit to canonical cell; no new review verdict.')
(run/'evidence-recovery95.json').write_bytes((json.dumps(receipt,indent=2)+'\n').encode())
print(json.dumps(receipt))
