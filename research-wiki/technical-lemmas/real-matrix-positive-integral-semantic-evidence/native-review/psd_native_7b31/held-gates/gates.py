import json,sys
from record import ROOT,REPO,EXPECTED_HEAD,run
preflight=json.loads((ROOT/'preflight-results.json').read_text());assert preflight['expected_held_HEAD']==EXPECTED_HEAD and preflight['tracked_clean']
commands=[
('publication',['python3','-B','tools/astis_publication.py','check','--base','441d54ee96a6182374d2df3bf4d2fb096d5b7e14']),
('semantic',['python3','-B','tools/astis_semantic_roundtrip.py','check']),
('contributor',['python3','-B','tools/astis_contributor_contract.py','check','--base','441d54ee96a6182374d2df3bf4d2fb096d5b7e14']),
('frontier',['python3','-B','tools/astis_frontier_cells.py','check'])]
assert not (ROOT/'gate-results.json').exists(),'Refusing a second gate run in this phase'
results=[]
for label,argv in commands:
    p,path=run('FINAL-GATE-'+label,argv)
    receipt=json.loads(path.read_text())
    results.append({'gate':label,'argv':argv,'exit':p.returncode,'receipt':str(path.relative_to(ROOT)),'stdout_sha256':receipt['stdout_sha256'],'stderr_sha256':receipt['stderr_sha256'],'HEAD_before':receipt['shared_HEAD_before'],'HEAD_after':receipt['shared_HEAD_after']})
    (ROOT/'gate-results.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps({'gate':label,'exit':p.returncode,'stdout_bytes':len(p.stdout),'stderr_bytes':len(p.stderr),'receipt':str(path)}),flush=True)
    if p.returncode or receipt['shared_HEAD_before']!=EXPECTED_HEAD or receipt['shared_HEAD_after']!=EXPECTED_HEAD:
        print('STOPPED_AFTER_FIRST_REAL_GATE_FAILURE_OR_HEAD_CHANGE',flush=True);sys.exit(p.returncode or 1)
print('ALL_FOUR_FINAL_HELD_GATES_EXIT_ZERO_ON_EXPECTED_HEAD',flush=True)
