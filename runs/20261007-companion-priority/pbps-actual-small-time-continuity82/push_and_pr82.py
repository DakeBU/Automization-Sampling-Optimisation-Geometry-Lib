from pathlib import Path
import json,subprocess
r=Path(__file__).parent;out=r/'integration82';head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();note=json.loads((r/'integration.notes.json').read_bytes())
assert note['state_distinctions']['independently_verified'] and not note['Goal_complete']
q=subprocess.run(['git','push','origin','HEAD:refs/heads/codex/sphmc-standardized-rgo'],capture_output=True)
(out/'push-observed82.json').write_text(json.dumps(dict(commit=head,exit_code=q.returncode,stdout=q.stdout.decode(errors='replace'),stderr=q.stderr.decode(errors='replace'),normal_push=True,Goal_complete=False),indent=2)+'\n',encoding='utf8',newline='\n');assert q.returncode==0
body=f'''The actual PBPS construction needs a physical phase across every finite time, rather than only an event-index recursion. This branch supplies actual interval coverage and a joint Borel phase, then constructs the ideal exact-reference half-turn returned-position probability kernel with its actual independent input and initialization law.

The latest bounded edge controls the actual phase-flow defect by the exact first-event probability, P[Z_t != Phi_t(z0)] <= 1-exp(-Lambda_t), and derives zero-time stochastic continuity for every fixed initial tuple and positive norm threshold. All original six analytic conditions and literal physical-phase/clock definitions remain. Independent mathematics, a fresh source-blind decoder and primary-first source review accepted all nine exact proof regions; a docstring and formula-order clarification changed no statement or BODY.

Validation: focused pinned Lean4.33.0, independent exact science verification, full local root/Tests ({note['root_jobs']}/{note['test_jobs']} jobs), tools/astis.py check, py_compile, contributor/publication/semantic/frontier/graph/site and whitespace gates passed. Existing sole stabilization lane; prior collaborator work preserved. Generated HTML contains adjacent initially folded exact Lean; the current affected static SVG was rendered and actually viewed with exact RAW pins. Actual browser page/interactive visual acceptance, main merge, Exposition Seal/PURIFIED and live delivery remain separate.

Full PBPS/SPHMC and actual-input composition, Gaussian Cloud recursion/error/cost and midpoint bounds/initialization remain open. The latest theorem is only the pointwise smalltime ingredient of source Ex22: it proves no full L2 strong continuity, process Markov/restart/semigroup/invariance/hypocoercivity, implemented reference sampler or query-cost result. TV proximity does not transfer unbounded expected cost. See docs/companion-papers-handoff.md and current Frontier Cells for exact accepted/open boundaries. Integration commit: {head}.
'''
p=out/'pr315-body82.md';p.write_text(body,encoding='utf8',newline='\n')
subprocess.run(['gh','pr','edit','315','--title','Formalize actual PBPS physical-time phase, ideal kernel and short-time continuity','--body-file',str(p)],check=True)
v=subprocess.run(['gh','pr','view','315','--json','url,state,headRefOid,baseRefName'],capture_output=True);assert v.returncode==0;x=json.loads(v.stdout);assert x['headRefOid']==head
(out/'pr315-observed82.json').write_text(json.dumps(x,indent=2)+'\n',encoding='utf8',newline='\n');print('NORMAL_PUSH_AND_EXISTING_PR_UPDATED',head,x['url'])
