from pathlib import Path
import hashlib,json,datetime,re
ROOT=Path('E:/Samplinglib')
OUT=ROOT/'runs/20261007-companion-priority/pbps-actual-physical-time-measurability80/header-review80'
def raw(p):
 b=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'RAW_bytes':len(b),'RAW_sha256':hashlib.sha256(b).hexdigest()}
def write(n,d):
 p=OUT/n
 with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
 return raw(p)
freeze=json.loads((OUT/'input-freeze80.json').read_text(encoding='utf-8'))
for item in freeze['inputs']:assert raw(ROOT/item['path'])==item
receipt=json.loads((OUT/'typecheck80.receipt.json').read_text(encoding='utf-8'))
assert receipt['exit_code']==0 and receipt['repair_overlay'] is None
header=ROOT/freeze['inputs'][0]['path'];s=header.read_text(encoding='utf-8')
assert s.count('private def ')==1 and not re.search(r'^\s*(theorem|axiom|sorry|admit)\b',s,re.M)
assert not (ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhysicalTimeMeasurability.lean').exists()
review=write('independent-header-math-review80.json',{
 'status':'ACCEPTED_PROSPECTIVE_HEADER_NO_REPAIR',
 'reviewer':'/root/exact_verify77','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'candidate':raw(header),'typecheck':raw(OUT/'typecheck80.receipt.json'),
 'definition_readback':raw(OUT/'definition-readback80.json'),
 'scope':'Independent prospective mathematical/interface and source-topology preservation review only. Not a Statement Seal, proof, blind decoder, final source review, VERIFIED admission, reader acceptance or paper completion.',
 'source_first_review':{'path':'runs/20261007-companion-priority/pbps-physical-time-measurability-preread80/independent-scope-review80/review-manifest80-final.json','RAW_sha256':'9d537ef2b0da03114e3adaaee7d1fa1f4ee3bfd790c18499ee53e8a9ddfa768e','method':'Primary Appendix A.1 initialization, finite/stopped recurrence, between-jump formula, and post-Example9 all-time clause were independently read before extractor/candidate in the preceding scope review. This header was compared against that accepted graph, not used to invent it.'},
 'binders':{'six_analytic_conditions':'hα positive alpha; hαβ alpha <= beta; hV C2; hH two-sided Hessian; hη positive eta; hβη beta*eta <=1. Exact original texts preserved.','ambient':'Same finite-dimensional real inner-product/Borel E, fixed V/alpha/beta/eta as 79/76. y/xRef/z0/t/sample vary jointly; no parameter law is assumed.','new_provider_premises':[],'private_visibility':True,'linter':'Six unused-condition warnings are expected for a Prop definition; no source hypothesis is removed.'},
 'definition_semantics':[
 'All 11 lets P, epsilon, c, Phi, S, rate, Lambda, tau, next, record, eventTime are text-identical to79 modulo line endings and block-end whitespace; nine common physical/recursive lets equal76. P is the canonical countable product Exp(1), epsilon_n is Real.toNNReal(sample n), matching source threshold E_(n+1).',
 'tau retains the full literal hittingAfter expression, next retains top-test before untopD, record starts inl(0,z0), stopped inr carries no phase at infinity, eventTime maps inr to top. No substitute recursion or certificate is introduced.',
 'The right-associated tuple is ((y,xRef),z0),(t,sample). All five projections match the claimed joint measurable coordinates.'
 ],
 'quantifiers_and_cases':[
 'One total function Z is chosen for all y/xRef/z0/t/sample, with joint Borel measurability. Its deterministic agreement clause applies to every covered half-open interval and every actual live record, on all samples. This stronger deterministic glue does not consume a probability event.',
 'Actual76 monotone eventTime makes nonempty half-open intervals disjoint even when some waits are zero. A finite lower endpoint forces a live record. NNReal elapsed subtraction is the true elapsed time since a.1 <= t follows from that endpoint. Thus multiple intervals or records cannot impose conflicting covered values.',
 'Every uncovered input explicitly has value z0. This is an ASTIS total representative convention on the uncovered complement, not a source assertion of physical motion beyond an accumulation point. It is measurable since coordinate z0 is measurable.',
 'When the next waiting time is top, all finite later times remain in the last live half-open interval. They receive Phi on that arc, never the fallback; finite elapsed < top is valid. No phase at infinite physical time is asserted.',
 'For each fixed y/xRef/z0, one P-almost-everywhere sample event contains both forall finite t existence of an actual live arc with elapsed < actual tau and the identity Z(0)=z0. This is not forall t AE with varying null sets, and not one AE event uniform in all parameters.',
 'AE initialization uses positive actual epsilon0 (Exp1) with actual76 initial record/positive finite first wait or infinite first wait, plus actual73 Phi0 identity. Bare79 coverage alone would not establish interval index0 at t0. Zero/nonpositive real thresholds are allowed in the total deterministic extension; all-sample initialization is intentionally not claimed.',
 'Per-parameter AE agreement does not license substituting arbitrary sample-correlated random y/xRef/z0. Future random-reference/init consumers still require their separate independence/conditional-law or joint-kernel/Fubini argument.'
 ],
 'distinct_topology_review':{'status':'PRESERVES_ACCEPTED_SOURCE_GRAPH','strict_dependencies':[
 'Coordinatewise epsilon map measurability.',
 'Actual76 joint record_n and eventTime_n measurability pulled back along epsilon.',
 'Bare interval measurable sets use clocks/order comparisons only; disjointness additionally uses monotone clocks. Neither step uses nonaccumulation.',
 'Measurable live-record extraction/NNReal elapsed/Phi evaluation uses actual73 and76.',
 'Countable disjoint interval gluing and uncovered z0 complement produce one total joint map, without nonexplosion.',
 'Actual79 AE all-finite-time coverage supplies per-fixed-parameter source agreement.',
 'Positive Exp epsilon0 +76 initialization/strict finite increment or top +73 Phi0 supply AE initialization.'
 ],'no_extra_edges':'No cap, nonexplosion, interval-index, positivity, measurable process or source law is accepted as an additional public premise. These are dependencies to be proved/consumed from parents, not hypotheses.'},
 'excluded_claims':['uniform-parameter AE event','arbitrary correlated random parameter law','random initialization distribution','Markov or strong Markov property','invariance/stationarity','algorithm cost or accuracy','whole Example9/main theorem/paper completion'],
 'repair_required':False,'production_file_exists':False,'proof_BODY_reviewed_or_created':False,
 'actions':'Only owned review artifacts and exact header snapshot were written; no production/shared/cell/ledger/Seal modification.'
})
for item in freeze['inputs']:assert raw(ROOT/item['path'])==item
files=sorted([p for p in OUT.iterdir() if p.is_file()],key=lambda p:p.name)
manifest=write('closed-manifest80.json',{'status':'CLOSED_PROSPECTIVE_REVIEW','reviewer':'/root/exact_verify77','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'input_freeze':raw(OUT/'input-freeze80.json'),'all_frozen_inputs_unchanged_after_typecheck_and_review':True,'candidate_unchanged':raw(header),'typecheck_exit_code':0,'repair_overlay':None,'review':review,'artifacts':[raw(p) for p in files],'not_credits':['Statement Seal','proof','final source acceptance','VERIFIED','stabilization','whole-Goal completion']})
print(json.dumps({'review':review,'closed_manifest':manifest},ensure_ascii=False))
