from pathlib import Path
import json,subprocess
r=Path(__file__).parent;out=r/'integration84';head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();note=json.loads((r/'integration.notes.json').read_bytes())
assert note['state_distinctions']['independently_verified'] and not note['Goal_complete']
q=subprocess.run(['git','push','origin','HEAD:refs/heads/codex/sphmc-standardized-rgo'],capture_output=True)
(out/'push-observed84.json').write_text(json.dumps(dict(commit=head,exit_code=q.returncode,stdout=q.stdout.decode(errors='replace'),stderr=q.stderr.decode(errors='replace'),normal_push=True,Goal_complete=False),indent=2)+'\n',encoding='utf8',newline='\n');assert q.returncode==0
body=f'''The actual PBPS event recursion covers every finite physical time and gives a jointly Borel phase, with an ideal exact-reference half-turn returned-position probability kernel and its actual independent input law.

The latest change derives the exact conditional Gibbs position and Gaussian-product initial phase probabilities from the original six analytic hypotheses. For every bounded continuous real test, the actual exponential-clock expectation is Borel measurable in the initial phase; its squared discrepancy from the initial test is integrable, bounded by4M², and has outer integral tending to zero at ordinary nonpunctured NNReal0. It consumes the already verified pointwise clock-expectation limit and applies finite-probability dominated convergence. All eleven actual algorithm definitions and prior phase clauses remain. The C_b class and explicit4M² are attributed ASTIS elaborations of source C_c; no phase-invariance premise is added.

Independent whole-source mathematics, fresh source-blind decoding and anti-anchored primary-source review accepted the exact sealed statement and eight contiguous formula/BODY regions. All47source items/23nodes/39relations are mapped; five future OPEN dependency edges and two excluded associations receive no proof credit. Normalization alternatives stay OR routes, their ingredients stay AND, and future density is separate from contraction.

Validation passed: pinned Lean4.33.0 focused compile and exact-science-commit independent verification, full local root/Tests ({note['root_jobs']}/{note['test_jobs']} jobs), tools/astis.py check, py_compile and contributor/publication/semantic/frontier/graph/site/whitespace gates. Integration uses the existing sole lane and preserves collaborator modifications. Generated HTML contains adjacent initially folded exact Lean; the current affected static SVG was rendered and actually viewed. Actual browser page/interactive visual acceptance, main merge, full Exposition Seal/PURIFIED and live delivery remain separate.

This is the bounded-test outer square-integral ingredient of AppendixA1 Ex22. Full all-L2 equivalence-class operators, invariant phase law, Jensen/contraction/density, actual Markov/restart/semigroup/hypocoercivity, implementation error/unbounded expected oracle cost, PBPS/SPHMC/composition, Gaussian Cloud and midpoint remain open. TV does not transfer unbounded expected costs. Current evidence and next boundaries are in the Frontier Cells and docs/companion-papers-handoff.md. Integration commit: {head}.
'''
p=out/'pr315-body84.md';p.write_text(body,encoding='utf8',newline='\n')
subprocess.run(['gh','pr','edit','315','--title','Formalize actual PBPS physical phase and bounded-test outer continuity','--body-file',str(p)],check=True)
v=subprocess.run(['gh','pr','view','315','--json','url,state,headRefOid,baseRefName'],capture_output=True);assert v.returncode==0;x=json.loads(v.stdout);assert x['headRefOid']==head
(out/'pr315-observed84.json').write_text(json.dumps(x,indent=2)+'\n',encoding='utf8',newline='\n');print('NORMAL_PUSH_AND_EXISTING_PR_UPDATED',head,x['url'])
