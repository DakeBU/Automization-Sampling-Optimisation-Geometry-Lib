from pathlib import Path
import json,subprocess,sys
r=Path(__file__).parent;phase=sys.argv[1];assert phase in {'science','integration'}
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
if phase=='science':
 assert json.loads((r/'root.source85.adoption.json').read_bytes())['publication_binding_unchanged']
 out=r
else:
 note=json.loads((r/'integration.notes.json').read_bytes());assert note['state_distinctions']['independently_verified'] and not note['Goal_complete'];out=r/'integration85'
p=out/(phase+'-push-observed85.json');assert not p.exists()
q=subprocess.run(['git','push','origin','HEAD:refs/heads/codex/sphmc-standardized-rgo'],capture_output=True)
p.write_text(json.dumps(dict(commit=head,exit_code=q.returncode,stdout=q.stdout.decode(errors='replace'),stderr=q.stderr.decode(errors='replace'),normal_push=True,Goal_complete=False),indent=2)+'\n',encoding='utf8',newline='\n');assert q.returncode==0
print('NORMAL_PUSH',phase,head)
if phase=='integration':
 body=f'''The actual PBPS physical-time construction now supplies a full-phase probability kernel jointly indexed by reference parameters, initial phase and finite time. Each fiber is exactly the actual exponential-clock pushforward, the zero-time law is Dirac, and every bounded Borel real test has integrability on both sides and exact integral transfer. This extends the previously verified finite-time coverage, joint measurability and bounded-test zero-time continuity.

Independent mathematics, fresh source-blind reconstruction, anti-anchored primary-source review and exact-commit verification passed. Six formula-proof steps retain all original analytic assumptions and algorithm definitions. Fixed Lean4.33.0 root/Tests, ASTIS check/fake-closure, contributor/publication/semantic/frontier/targeted graph/site gates, py_compile and whitespace checks passed locally. Integration commit: {head}. Science commit: {note['science_commit']}.

Probability fibers do not prove a temporal Markov property. Actual path-law/reversal/invariance, all-L2 operators/contraction/density, restart/semigroup/hypocoercivity, implementation errors, unbounded expected oracle cost, complete paper main results and PBPS-SPHMC composition remain open. The actual kernel and ideal half-period position law retain separate boundaries. Generated reference graphs and independently certified kernel dependencies remain distinct. Static SVG was viewed; actual page/interactive visual, remote CI, main merge, purification and live deployment are separate from local acceptance. The existing four-paper Goal remains active; collaborator modifications and prior work are preserved.
'''
 p=out/'pr315-body85.md';assert not p.exists();p.write_text(body,encoding='utf8',newline='\n')
 subprocess.run(['gh','pr','edit','315','--body-file',str(p)],check=True)
 q=subprocess.run(['gh','pr','view','315','--json','url,state,headRefOid,baseRefName'],capture_output=True);assert q.returncode==0
 observed=json.loads(q.stdout);assert observed['headRefOid']==head
 p=out/'pr315-observed85.json';assert not p.exists();p.write_text(json.dumps(observed,indent=2)+'\n',encoding='utf8',newline='\n')
 print('EXISTING_PR_UPDATED',observed['url'])
