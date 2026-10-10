from pathlib import Path
import json,subprocess
r=Path(__file__).parent;out=r/'integration83';head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();note=json.loads((r/'integration.notes.json').read_bytes())
assert note['state_distinctions']['independently_verified'] and not note['Goal_complete']
q=subprocess.run(['git','push','origin','HEAD:refs/heads/codex/sphmc-standardized-rgo'],capture_output=True)
(out/'push-observed83.json').write_text(json.dumps(dict(commit=head,exit_code=q.returncode,stdout=q.stdout.decode(errors='replace'),stderr=q.stderr.decode(errors='replace'),normal_push=True,Goal_complete=False),indent=2)+'\n',encoding='utf8',newline='\n');assert q.returncode==0
body=f'''The actual PBPS event recursion now covers every finite physical time and gives a jointly Borel phase, with an ideal exact-reference half-turn returned-position probability kernel and its actual independent input law.

The latest bounded edge proves that every globally bounded continuous real phase test has measurable integrable pullbacks under the actual clock law. It derives |E f(Z_t)-f(Phi_t z0)|<=2M(1-exp(-Lambda_t)) from the actual first-event defect bound, then E f(Z_t)->f(z0) at ordinary NNReal0 for each fixed initial tuple. All six original analytic conditions, eleven literal actual definitions and previous physical-phase clauses remain. The C_b test class and explicit2M estimate are attributed ASTIS elaborations of the source C_c pointwise step.

Independent mathematics, fresh source-blind reconstruction and exhaustive primary-first source review accepted the sealed statement and all eight exact formula/BODY regions. The source graph's optional epsilon/delta branch has conjunctive ingredients; the excluded-boundary association is not a theorem dependency.

Validation passed: pinned Lean4.33.0 focused compile, independent exact science verification, full local root/Tests ({note['root_jobs']}/{note['test_jobs']} jobs), tools/astis.py check, py_compile and contributor/publication/semantic/frontier/graph/site/whitespace gates. The existing sole stabilization lane preserves collaborator files. Generated HTML has adjacent initially folded exact Lean; the current affected static SVG was rendered and actually viewed. Actual browser page/interactive visual acceptance, main merge, full Exposition Seal/PURIFIED and live delivery remain separate.

This is a bounded clock-expectation prerequisite of AppendixA1 Ex22. Outer L2 continuity, invariant phase law/Jensen/contraction/density, process Markov/restart/semigroup/hypocoercivity, implementation error/unbounded expected oracle cost, full PBPS/SPHMC/composition, Gaussian Cloud and midpoint remain open. TV proximity does not transfer unbounded expected cost. See the current Frontier Cells and docs/companion-papers-handoff.md. Integration commit: {head}.
'''
p=out/'pr315-body83.md';p.write_text(body,encoding='utf8',newline='\n')
subprocess.run(['gh','pr','edit','315','--title','Formalize actual PBPS physical phase and bounded-test clock expectation','--body-file',str(p)],check=True)
v=subprocess.run(['gh','pr','view','315','--json','url,state,headRefOid,baseRefName'],capture_output=True);assert v.returncode==0;x=json.loads(v.stdout);assert x['headRefOid']==head
(out/'pr315-observed83.json').write_text(json.dumps(x,indent=2)+'\n',encoding='utf8',newline='\n');print('NORMAL_PUSH_AND_EXISTING_PR_UPDATED',head,x['url'])
