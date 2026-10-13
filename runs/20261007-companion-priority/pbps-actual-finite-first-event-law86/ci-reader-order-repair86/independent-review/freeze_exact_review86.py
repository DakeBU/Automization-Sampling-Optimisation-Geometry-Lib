"""Freeze independent CI-only repair decision, without shared mutations."""
from __future__ import annotations
import ast
import datetime
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / 'runs/20261007-companion-priority/pbps-actual-finite-first-event-law86/ci-reader-order-repair86'
OUT = BASE / 'independent-review'

def sha(raw): return hashlib.sha256(raw).hexdigest()
def rel(p): return p.relative_to(ROOT).as_posix()
def desc(p, kind):
    raw=p.read_bytes()
    return {'path':rel(p),'raw_sha256':sha(raw),'sha256':sha(raw),'bytes':len(raw),'kind':kind}
def put(name,value):
    path=OUT/name
    assert not path.exists(), 'Preserve immutable prior files'
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return desc(path,'native-review-output')

proposal=BASE/'proposal86.json'
before=BASE/'test.before.exactraw.snapshot'
proposed=BASE/'test.proposed.exactraw.snapshot'
canonical=ROOT/'tools/tests/test_astis_publication.py'
assert sha(proposal.read_bytes())=='5c3e267e7ca45921265b299a74892e9840d5c511112a06bc3c3ad9c54bab7e0c'
assert sha(before.read_bytes())=='740bfb80b97284283d0d2243f4d6033349cc8cf3ba610cccf9e4a93dd04e2014'
assert sha(proposed.read_bytes())=='a40f288d05d1e63ca8b75f95e1ebf96f19d182adff1aaebcdbc7e87a3c7a2d73'
assert canonical.read_bytes()==before.read_bytes()
inputs=[desc(proposal,'exact-root-proposal'),desc(before,'exact-before-tests'),desc(proposed,'exact-proposed-tests'),desc(canonical,'unchanged-canonical-tests')]
protected={
 'website/scripts/declaration_lessons.py':'671dc0d177856b9c0f91f8acc6922f1e0e0cf57de5656b44cf8dbdea51cb9cdc',
 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteFirstEventLaw.lean':'d6667ccbb917d6463e96b2082a5a26089950889fd20af4859052cd7a9a1db776',
 'website/content/declaration_lessons/pbps-actual-finite-first-event-law.json':'9cb0da1316872b2484404316211a9378310656b61ceb02b455793d055e5fb033',
 'website/content/publications/pbps-actual-finite-first-event-law.json':'f1408d45a5bfe5aa5875b73786460296e451da94074a40335aad2d75a5392bb1'
}
for name,expected in protected.items():
    d=desc(ROOT/name,'hash-only-protected-current-input')
    assert d['raw_sha256']==expected,(name,d['raw_sha256'])
    inputs.append(d)

a=ast.parse(before.read_text(encoding='utf-8'));b=ast.parse(proposed.read_text(encoding='utf-8'))
def methods(t):
    return {n.name+'.'+f.name:ast.dump(f,include_attributes=False) for n in t.body if isinstance(n,ast.ClassDef) for f in n.body if isinstance(f,(ast.FunctionDef,ast.AsyncFunctionDef))}
x,y=methods(a),methods(b)
added=list(y.keys()-x.keys());changed=sorted(n for n in x.keys()&y.keys() if x[n]!=y[n]);removed=list(x.keys()-y.keys())
assert added==['PublicationTest.test_literal_proposition_and_proof_helpers_keep_distinct_reader_positions']
assert changed==['PublicationTest.test_each_proof_keeps_its_own_assumptions_and_provenance_adjacent']
assert not removed
for c in b.body:
    if isinstance(c,ast.ClassDef): c.body=[f for f in c.body if not (isinstance(f,ast.FunctionDef) and f.name==added[0].split('.')[1])]
class ExactOrderReplacement(ast.NodeTransformer):
    def visit_Assign(self,n):
        if any(isinstance(t,ast.Name) and t.id=='markers' for t in n.targets) and isinstance(n.value,ast.List) and any(isinstance(v,ast.Constant) and v.value=='Mathlib API called (external library)' for v in n.value.elts):
            n.value=ast.List(elts=[ast.Constant(v) for v in ['Lean statement ·','Proof roadmap','Full assumptions and notation','Mathematical proof','Lean proof ·','Source assumptions versus formal assumptions','proof-reader-provenance','Mathlib API called (external library)']],ctx=ast.Load())
        return self.generic_visit(n)
a=ExactOrderReplacement().visit(a)
assert ast.dump(a,include_attributes=False)==ast.dump(b,include_attributes=False)

results={v:json.loads((OUT/f'{v}.isolated.result.json').read_text(encoding='utf-8')) for v in ['before','proposed']}
assert results['before']['tests_run']==44 and not results['before']['success']
assert len(results['before']['failures'])==1 and 'test_each_proof_keeps_its_own_assumptions_and_provenance_adjacent' in results['before']['failures'][0]['test']
assert results['proposed']['tests_run']==45 and results['proposed']['success']
for v in results:
    assert not results[v]['errors'] and not results[v]['skipped'] and results[v]['expected_failures']==0 and results[v]['unexpected_successes']==0
    assert (OUT/f'test_{v}_isolated86.py').read_bytes()==(BASE/f'test.{v}.exactraw.snapshot').read_bytes()
checks={
 'exact_delta':'Entire test-module AST unchanged after precisely substituting the order marker list and removing the one new regression test; no removed methods or weakened existing assertions.',
 'statement_adjacency':'The old test required Mathematical proof before Lean statement. The replacement requires signature before roadmap, assumptions, mathematical proof and exact Lean proof, matching the independently reviewed V4 statement-first reader contract.',
 'provenance':'Existing per-declaration source-comparison uniqueness, matching declaration identity, source/formal assumption comparison, provenance, external-library annotation, initially closed details and no generic Source/reuse fold assertions are all retained.',
 'expanded_prop':'The new actual86 test requires the literal full proposition once, after the public signature closes and before roadmap; V4 sibling disclosure remains reachable independently of the statement fold.',
 'proof_regions':'Every listed helper is checked once, all genuine proof helpers after the public proof, and corresponding Lean step folds equal authored step count (the current accepted eleven-region lesson). No authored proof, source region, Lean code or mathematical assumption changes.',
 'folding':'Both existing article regression and new real86 regression forbid initially open details. The new test adds coverage rather than accepting unfolded or duplicate content.',
 'evidence_boundary':'Local isolated before/proposed execution diagnoses and repairs this test contract only. It does not certify rerun remote CI, Lean compilation, mathematical SAU87, theorem VERIFIED, site deployment or live verification.'
}
chronology=put('independent-ci-review86.chronology.json',{
 'reviewer':'independent-primary-source-reviewer86','scope':'Independent exact CI regression repair only; distinct from SAU87 mathematics',
 'sequence':[
  'Read exact proposal and before/proposed snapshots; retained initial large tool-output truncation without treating it as evidence of omission.',
  'Focused raw hash and unified diff inspection; canonical test equals before; renderer equals accepted V4.',
  'AST comparison found precisely one changed method and one added method; normalized whole-module AST equality established for those exact changes.',
  'Copied each exact snapshot into owned independent-review directory; importlib loaded copies in separate processes with bytecode disabled. Standard fixture loading was exercised only as tests, not as new mathematical/source verdict evidence.',
  {'before':results['before']['started_utc'],'finished':results['before']['finished_utc'],'result':'44 tests, sole expected outdated-order failure, no errors/skips'},
  {'proposed':results['proposed']['started_utc'],'finished':results['proposed']['finished_utc'],'result':'45 tests pass, no errors/skips'},
  'Rehashed protected canonical test, V4 renderer, PBPS86 module, lesson and publication against pre-existing exact pins; no shared file mutation.'
 ],
 'diagnostics':[
  {'kind':'tool-output-truncation','detail':'Initial combined full snapshot print exceeded output budget; complete exact bytes subsequently hashed, diffed, AST-compared and executed from isolated copies.'},
  {'kind':'nonessential-path-lookup','detail':'Attempted own earlier fifth-edge-review86.RAW-manifest.json lookup found no file; no evidence relied on that lookup or foreign verdict.'},
  {'kind':'runtime-description','detail':'Used the explicitly pinned dependency executable path. It reports Python3.12.14, rather than the earlier contextual description Python3.11; actual version is retained in both execution results.'},
  {'kind':'expected-before-failure','detail':results['before']['failures'][0]}
 ],
 'prohibited_actions':'No shared edits, anonymous packet content read, registry/source verdict adoption, renderer change, mathematical repair, status transition or network use.'
})
run=put('independent-ci-review86.run.json',{
 'schema':'astis.independent.exact-proposal-ci-repair-run86.v1',
 'reviewer':'independent-primary-source-reviewer86','proposal_creator':'root sole stabilization writer',
 'proposal_raw_sha256':sha(proposal.read_bytes()),'inputs':inputs,
 'chronology':chronology,'ast_delta':{'changed_methods':changed,'added_methods':added,'removed_methods':removed,'whole_module_equal_after_exact_delta_normalization':True},
 'isolated_tests':{v:desc(OUT/f'{v}.isolated.result.json','native-isolated-test-result') for v in results},
 'checks':checks,'shared_changes':False,'remote_ci_rerun':'not performed',
 'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()
})
decision=put('independent-ci-review86.decision.json',{
 'schema':'astis.independent.exact-proposal-ci-repair-decision86.v1',
 'reviewer':'independent-primary-source-reviewer86','proposal_creator':'root sole stabilization writer',
 'independent_from_proposal_creator':True,'proposal_sha256':sha(proposal.read_bytes()),
 'before_test_sha256':sha(before.read_bytes()),'candidate_test_sha256':sha(proposed.read_bytes()),
 'renderer_sha256':protected['website/scripts/declaration_lessons.py'],
 'review_run_sha256':run['raw_sha256'],'verdict':'ACCEPTED_EXACT_CI_READER_ORDER_REPAIR','decision':'accepted',
 'reason':'The old order contradicts the accepted statement-adjacency contract. Exact replacement retains all existing provenance and folding checks, adds real86 full-proposition/helper/step-fold coverage, and changes no mathematical or source evidence. Isolated current44 tests show only the stale-order failure; proposed45 pass.',
 'blocking_deltas':[],'checks':checks,
 'application':'Root sole stabilization writer may apply only the exact proposed test bytes. Canonical test remained unchanged during independent review.',
 'boundary':'Exact test proposal acceptance only; remote CI rerun and root integration pending. No mathematical, source theorem, SAU87, VERIFIED, deployed or live claim.',
 'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()
})
outputs=[desc(p,'native-review-output') for p in sorted(OUT.iterdir()) if p.is_file()]
manifest=put('independent-ci-review86.RAW-manifest.json',{
 'schema':'astis.independent.closed-raw-manifest86.v1','hash_algorithm':'SHA256','hash_mode':'RAW exact bytes',
 'inputs':inputs,'outputs':outputs,'closed':True,
 'closure':'All files created by this independent review are listed. This manifest excludes only itself to avoid recursive self-hashing; its own RAW SHA is reported externally.',
 'decision_sha256':decision['raw_sha256'],'review_run_sha256':run['raw_sha256'],
 'source_extracts':[],'private_exclusion_list':[]
})
for d in inputs+outputs:
    raw=(ROOT/d['path']).read_bytes()
    assert len(raw)==d['bytes'] and sha(raw)==d['raw_sha256']
print(json.dumps({'decision':decision,'run':run,'manifest':manifest,'chronology':chronology},indent=2))
