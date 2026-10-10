from pathlib import Path
import json,subprocess
r=Path(__file__).parent;out=r/'integration84/cell-admission-correction'
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
note=json.loads((r/'integration.corrected.notes.json').read_bytes())
assert note['state_distinctions']['independently_verified'] and not note['Goal_complete']
q=subprocess.run(['git','push','origin','HEAD:refs/heads/codex/sphmc-standardized-rgo'],capture_output=True)
p=out/'push-observed84.corrected.json';assert not p.exists()
p.write_text(json.dumps(dict(commit=head,exit_code=q.returncode,stdout=q.stdout.decode(errors='replace'),stderr=q.stderr.decode(errors='replace'),normal_push=True,Goal_complete=False),indent=2)+'\n',encoding='utf8',newline='\n');assert q.returncode==0
original=(r/'integration84/pr315-body84.md').read_text(encoding='utf8')
body=original.replace('Integration commit: 5186f92607df617c4e4a8a90d0c5e6b5fc611090.',f'Integration commit: {head}.')
body+='\nAdmission correction: includes the independently verified84 Frontier Cell omitted by the previous staging list and reruns graph-check on84. The generated graph contains incomplete name-scanned reference signals, not elaborated proof dependencies. Exactly four actual producer parents are certified separately by the independent kernel audit. Cell display wording and reference-graph freshness were independently reviewed; no theorem, proof, source assumption or formula-proof HTML changed. Earlier observations are retained.\n'
p=out/'pr315-body84.corrected.md';assert not p.exists();p.write_text(body,encoding='utf8',newline='\n')
subprocess.run(['gh','pr','edit','315','--body-file',str(p)],check=True)
q=subprocess.run(['gh','pr','view','315','--json','url,state,headRefOid,baseRefName'],capture_output=True);assert q.returncode==0
observed=json.loads(q.stdout);assert observed['headRefOid']==head
p=out/'pr315-observed84.corrected.json';assert not p.exists();p.write_text(json.dumps(observed,indent=2)+'\n',encoding='utf8',newline='\n')
print('NORMAL_PUSH_AND_EXISTING_PR_UPDATED',head,observed['url'])
