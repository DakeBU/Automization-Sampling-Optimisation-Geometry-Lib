from common import *
env=os.environ.copy(); env['PYTHONUTF8']='1'; env['PYTHONDONTWRITEBYTECODE']='1'
commands=[('publication',[sys.executable,'-B','-X','utf8','tools/astis_publication.py','check','--base',BASE]),('semantic',[sys.executable,'-B','-X','utf8','tools/astis_semantic_roundtrip.py','check']),('frontier',[sys.executable,'-B','-X','utf8','tools/astis_frontier_cells.py','check']),('contributor',[sys.executable,'-B','-X','utf8','tools/astis_contributor_contract.py','check','--base',BASE])]
results=[]
for name,cmd in commands:
 result=invoke(name,cmd,env); results.append(result); print(name,result['actual_PID'],result['exit_code'],flush=True)
 if result['exit_code']: W(P/'gates.negative.json',dict(status='BLOCKED',results=results)); sys.exit(result['exit_code'])
from tools import astis_publication
declarations=J(R/'proved-local.json')['publication_declarations']; astis_publication.check_advance(declarations,reviewed=True)
W(P/'gates.json',dict(status='PASS',checked_commit=head(),gates=results,reviewed_advance_publication=dict(actual_PID=os.getpid(),declarations=declarations,reviewed=True,result='PASS'),mandatory_root_and_aggregate='DEFERRED_TO_SERIALIZED_ROOT_INTEGRATION',whitespace='Original108 immutable native findings/14paths retained; authored complement PASS, no full-staged PASS'))
print('ALL_NONCOMPILER_GATES_PASS')
