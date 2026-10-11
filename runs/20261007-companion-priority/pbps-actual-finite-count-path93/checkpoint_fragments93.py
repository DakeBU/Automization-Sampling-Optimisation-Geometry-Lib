"""Record compiled internal progress without promoting the sealed SAU."""
from pathlib import Path
import json, hashlib, sys, subprocess

root=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(root))
from tools.astis_advance import checkpoint_advance
run=Path(__file__).resolve().parent
def load(p): return json.loads(p.read_bytes())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x): p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
baseline=load(root/'runs/20261007-companion-priority/pbps-actual-ordered-prefix92/exact-commit-verification92/closed-RAW-manifest92.json')
for x in baseline['preserved_collaborator_inputs']:
    assert sha(root/x['path'])==x['raw_sha256'],x['path']
assert sha(run.parent/'pbps-finite-count-path-preread93/Header93.lean')=='90bca17fbb11d9a8fea226bd0dca6494ef9a61f3db31beaf52c0ef2999cf9cfe'
pairs=[('WeightedPrefix93.lean','weighted-prefix6-small-eliminator'),
 ('CountInterfaces93.lean','count-interfaces7-instance-transport'),
 ('InterpolationFormula93.lean','interpolation-formula1'),
 ('ActualPathIdentification93.lean','actual-path-identification2-scalar-api'),
 ('ActualEndpointNullity93.lean','actual-endpoint-nullity2-explicit-api')]
checks=[]
for source,label in pairs:
    p=run/'focused93'/label/'receipt.json'; r=load(p)
    assert r['exit_code']==0 and r['source_unchanged'] and r['source_raw_sha256']==sha(run/source)
    text=(p.parent/'stdout.log').read_text(encoding='utf8')
    assert 'sorryAx' not in text and ': error' not in text
    checks.append(dict(source=(run/source).relative_to(root).as_posix(),raw_sha256=sha(run/source),
                       receipt=p.relative_to(root).as_posix(),status='focused-pass-private-fragment'))
diagnosis=dict(scope='Internal implementation routes only; sealed six assumptions and source proposition unchanged.',
    retained_failures=[dict(route='Nat.find definitional instance identification',failure='IMPLEMENTATION_FAILED',
      evidence='focused93/count-interfaces4-cardinality/stdout.log',
      diagnosis='Dependent Nat.find carries distinct decidability instances; explicit Subsingleton transport replaces invalid definitional conversion.',
      repair='focused93/count-interfaces7-instance-transport/receipt.json'),
    dict(route='Dependent Sum cases in large actual density context',failure='IMPLEMENTATION_FAILED',
      evidence='focused93/weighted-prefix5-typed-joint-map/process-before-route-repair.json',
      diagnosis='Observed >10GB working set; independent static diagnosis suggests dependent abstraction explosion. Confirmed owned Lean process stopped; no success claimed.',
      repair='Small constructor identity outside the actual context, explicit function equality; weighted-prefix6-small-eliminator PASS.')],
    salvage='Compiled private proofs retained with exact input snapshots; no new SAU or public premise.',
    independent_partial_review='independent-fragment-math93/fragment-math-review93.native.json')
# Use actual retained label discovered on disk for the negative kernel receipt.
for p in (run/'focused93').glob('count-interfaces4*/stdout.log'):
    diagnosis['retained_failures'][0]['evidence']=p.relative_to(run).as_posix()
save(run/'implementation-route-diagnosis93.json',diagnosis)
cell=root/'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-finite-count-path.json'
c=load(cell); c['evidence']['focused_checks']=checks
c['evidence']['implementation_diagnosis']=(run/'implementation-route-diagnosis93.json').relative_to(root).as_posix()
save(cell,c)
signature=hashlib.sha256(json.dumps(checks,sort_keys=True).encode()).hexdigest()
event=checkpoint_advance('ASTIS-SA-20261011-PBPSActualFiniteCountPath',worker_id='companion_root_20261005',
 route_fingerprint='actual-count-path/terminal-weight/total-history-interpolation',progress_signature=signature,
 mathematical_delta='Private compiled actual terminally weighted joint history/interpolation law, joint Psi/Gamma/rho measurability, measurable count selector, prescribed interpolation, actual path identification on raw C, and fixed-T actual endpoint atomlessness via prefix law92. Only six source analytic hypotheses; no whole SAU admission.',
 exact_residual='Derive AE C_k iff N=k and count cardinalities, raw C disjointness/full union, substitute actual path/count in the weighted law, assemble exact sealed target; full independent math/decoder/source review and unique-lane reader stabilization remain.')
save(run/'compiled-fragments-checkpoint93.json',dict(event=event,focused_checks=checks,preserved_collaborator_count=len(baseline['preserved_collaborator_inputs']),status='EXPLORING'))
handoff=root/'docs/companion-papers-handoff.md'; s=handoff.read_text(encoding='utf8')
start=s.index('Initial private finite-fold measurability')
end=s.index('\n## Actual PBPS ordered finite-prefix law',start)
s=s[:start]+'''Private actual-input fragments now compile: joint history/path interpolation
and terminal density measurability; the terminally weighted prefix joint law;
count-selector measurability; exact prescribed interpolation; whole-path
identification on raw terminal-survival events; and fixed-T endpoint nullity.
The last uses actual positive clocks and the92 prefix density on a coordinate
hyperplane of Lebesgue measure zero. It is forall fixed T, AE, not AE forall T.
Exact focused receipts and retained implementation diagnoses are bound in the
existing Frontier Cell and compiled-fragments-checkpoint93.json. These remain
private ingredients, not a completed or independently VERIFIED SAU93.
Next: derive AE count/event equivalence and cardinalities, raw disjointness and
full union; join actual count/path with the weighted measure and seal the whole
proof. Independent final math/decoder/source audits and publication follow.
Hazard stitching, left limits, full A7, restart/Markovness, invariance,
hypocoercivity, errors, expected cost, main results, actual-input composition
and the four-paper Goal remain OPEN.
\n'''+s[end:]
handoff.write_text(s,encoding='utf8',newline='\n')
print(json.dumps(dict(status='EXPLORING',compiled_fragments=len(checks),signature=signature)))
