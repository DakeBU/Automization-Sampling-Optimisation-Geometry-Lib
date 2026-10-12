from pathlib import Path
import hashlib, json, sys

r = Path(__file__).parent
sys.path.insert(0, str(Path.cwd() / 'tools'))
from astis_advance import current_advances, transition_advance
import astis_publication as pub
load = lambda p: json.loads(Path(p).read_bytes())
save = lambda p,d: p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
c = load(r/'claim.json')
assert current_advances()[c['advance_id']]['state']=='EXPLORING'
receipt = r/'focused108/full2/receipt.json'
q = load(receipt)
assert q['exit_code']==0 and q['terminal_closed']
math = r/'independent-whole-math108/whole-math-decision108.native.json'
q = load(math)
assert q['decision']=='ACCEPT_WHOLE_MATHEMATICS_AND_EXACT_SEALED_KERNEL'
assert hashlib.sha256(Path(c['proposed_files'][0]).read_bytes()).hexdigest()==q['production']['raw_sha256']
assert (r/'decoder-admission108.json').exists()
pub.check_advance(c['target_declarations'],reviewed=False)
cp = Path('research-wiki/frontier-cells')/(c['frontier_cell']+'.json')
cell = load(cp)
assert cell['conceptual_mirror_audit']['reason'].startswith('Post-proof audit:')
snap = r/'cell-before-proved-local108.json'
assert not snap.exists()
snap.write_bytes(cp.read_bytes())
e = dict(result_kind='integration-node',theorem_delta=c['theorem_delta'],lean_declarations=c['target_declarations'],publication_declarations=c['target_declarations'],lean_files=c['proposed_files'],focused_checks=[receipt.as_posix()],truth_boundary=c['truth_boundary'],conceptual_mirror_audit=cell['conceptual_mirror_audit'],independent_math=math.as_posix(),source_review='Fresh independent blind reconstruction closed; final source/exposition review pending. Selected density topology unchanged and independently admitted.',remaining='Final source verdict, independent exact-commit verification, sole-lane aggregate integration and reader delivery.')
transition_advance(c['advance_id'],'PROVED_LOCAL',worker_id='companion_root_20261005',modes=['faithfulPaper'],evidence=e)
cell['status']='proved_locally'
cell['evidence']['independent_whole_math']=math.as_posix()
cell['evidence']['focused_checks']=e['focused_checks']
cell['blocked']['reason']=e['remaining']
save(cp,cell)
save(r/'admission-status108.json',dict(focused_build='PASS',whole_mathematics='independently accepted',blind_decoder='closed independent',source_review='pending',PROVED_LOCAL=True,VERIFIED=False))
print('PROVED_LOCAL only; final source and exact-commit admission remain pending.')
