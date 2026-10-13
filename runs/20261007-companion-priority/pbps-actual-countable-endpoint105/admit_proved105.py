from pathlib import Path
import hashlib,json,sys
r=Path(__file__).resolve().parent
sys.path[:0]=[str(Path.cwd()),str(Path.cwd()/'tools')]
from tools.astis_advance import current_advances,transition_advance
from tools import astis_publication as pub
load=lambda p:json.loads(Path(p).read_bytes())
c=load(r/'claim.json');assert current_advances()[c['advance_id']]['state']=='EXPLORING'
for p in [r/'focused105/production1/receipt.json',r/'checks105/science-focused/receipt.json']:
 q=load(p);assert q['exit_code']==0 and q['terminal_closed']
math=r/'independent-whole-math105/whole-math-decision105.native.json';q=load(math);assert q['decision']=='ACCEPT_WHOLE_MATHEMATICS_AND_EXACT_SEALED_KERNEL'
assert hashlib.sha256(Path(c['proposed_files'][0]).read_bytes()).hexdigest()==q['production']['raw_sha256']
pub.check_advance(c['target_declarations'],reviewed=False)
cp=Path('research-wiki/frontier-cells')/(c['frontier_cell']+'.json');cell=load(cp)
snap=r/'cell-before-proved-local105.json';assert not snap.exists();snap.write_bytes(cp.read_bytes())
e=dict(result_kind='integration-node',theorem_delta=c['theorem_delta'],lean_declarations=c['target_declarations'],publication_declarations=c['target_declarations'],lean_files=c['proposed_files'],focused_checks=[str(r/'focused105/production1/receipt.json'),str(r/'checks105/science-focused/receipt.json')],truth_boundary=c['truth_boundary'],conceptual_mirror_audit=cell['conceptual_mirror_audit'],independent_math=str(math),source_review='Fresh blind reconstruction complete; primary-first final source/exposition review pending.',remaining='Final source verdict, independent exact-commit verification, sole-lane aggregate integration and reader delivery.')
transition_advance(c['advance_id'],'PROVED_LOCAL',worker_id='companion_root_20261005',modes=['faithfulPaper'],evidence=e)
cell['status']='proved_locally';cell['evidence']['independent_whole_math']=str(math);cell['evidence']['focused_checks']=e['focused_checks'];cell['blocked']['reason']=e['remaining'];cp.write_text(json.dumps(cell,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
(r/'admission-status105.json').write_text(json.dumps(dict(focused_build='PASS',whole_mathematics='independently accepted',blind_decoder='closed independent',source_review='pending',PROVED_LOCAL=True,VERIFIED=False),indent=2)+'\n',encoding='utf8')
print('PROVED_LOCAL only; exact independent commit and source admission remain pending.')
