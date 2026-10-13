from pathlib import Path
import hashlib,json,datetime
R=Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-actual-physical-time-measurability80';O=B/'independent-math80'
def raw(p):
 b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest())
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def save(n,v):
 p=O/n
 with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
 return raw(p)
M=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhysicalTimeMeasurability.lean';s=M.read_text(encoding='utf-8');lines=s.splitlines()
def ln(needle):return next(i+1 for i,v in enumerate(lines) if needle in v)
freeze=load(O/'input-freeze80.json')
for e in freeze['inputs']:assert raw(R/e['path'])==e
assert load(O/'fresh-whole-module.receipt.json')['exit_code']==0
deps=load(O/'kernel-dependency-summary80.json');assert deps['status']=='PASS'
assert load(O/'fake-closure-scan80.json')['hits']==[]
mathlib=R/'.lake/packages/mathlib/Mathlib/MeasureTheory/MeasurableSpace/Constructions.lean'
proof=save('whole-proof-mathematics80.json',{
 'status':'ACCEPTED_INDEPENDENT_MATHEMATICS','reviewer':'/root/exact_verify77','module':raw(M),
 'sealed_statement':raw(B/'root.statement-seal80.json'),'exact_statement_audit':raw(O/'statement-definition-audit80.json'),
 'method':'Read the complete production file independently. Check literal binders/definitions and mathematical semantics, fresh elaborate the complete exact source, inspect kernel proof-value closure and transitive axioms. This is mathematical review only, not a source-blind decoder/final source acceptance or VERIFIED transition.',
 'steps':[
 {'start_line':ln('  have h76 :='),'finding':'Actual76 supplies initial record, joint record/clock measurability, monotonic clocks and positive live first increments; actual73 supplies joint Phi measurability and Phi0 identity. These are genuine parent theorem consumers with unchanged local actual definitions, not new public assumptions.'},
 {'start_line':ln('  have hεM'),'finding':'The epsilon map is coordinatewise Real.toNNReal composed with each sample projection. args selects ((y,xRef),z0,epsilon sample) from the correctly associated full tuple. hrecordM/htimeM composition gives joint record_n/clock_n measurability in all finite parameters, time and sample; ignoring the time coordinate does not remove any parameter dependence.'},
 {'start_line':ln('  let D :'),'finding':'D_n is the intersection T_n <= finite t and finite t < T_(n+1), hence measurable by order-comparison of measurable clocks. This step contains no nonexplosion or AE input. The natural-index trichotomy and actual monotonicity force n=m for any two occupied D sets; zero waiting times merely yield empty intervals, so strict global clock growth is unnecessary.'},
 {'start_line':ln('  let L :'),'finding':'Sum.elim id (constant zero record) is a total measurable auxiliary extraction. If a record is stopped then eventTime_n=top, contradicting D_n lower comparison with finite t. Thus the dummy zero branch never supplies a source phase on a covered interval. On a real inl a, reduction gives exactly a; its time <=t follows from the finite lower endpoint, so NNReal tsub is genuine nonnegative elapsed time.'},
 {'start_line':ln('  let branch :'),'finding':'branch_n composes the literal joint Phi with measurable parameter projections, NNReal subtraction, real coercion and L_n phase. Joint Borel measurability holds on the full domain even though branch values outside D_n need not describe physical motion.'},
 {'start_line':ln('  let sets :'),'finding':'Option Nat is countable/nonempty. none denotes exactly the complement of the countable covered union and values none is coordinate z0; some n denotes D_n and branch_n. Each set/value is measurable. none/some intersections are empty by complement, and distinct some/some intersections are empty by hdisj. Mathlib exists_measurable_piecewise (local pinned source lines548-551) gives one measurable f agreeing on every piece. These pieces cover the entire domain, so no arbitrary outside-union default is left unconstrained.'},
 {'start_line':ln('  have hZ '),'finding':'Z curries f with the exact tuple order. hf(some n) and the actual record equality reduce L to that record and prove the requested arc formula on every covered interval for all samples. hf none proves exactly the uncovered z0 fallback. Neither conclusion requires a probability event or positivity, and infinite-next-wait last live arcs lie in some n rather than none.'},
 {'start_line':ln('    have hc :='),'finding':'For each fixed y/xRef/z0, actual79 supplies a single sample event on which all finite t have the actual live record and elapsed < actual tau. Intersect this with actual77 positive exponential-input event once, before introducing t. The proof retains all79 inequalities/record equalities and adds deterministic hZ. Quantifier order remains per-parameter AE sample forall finite t, never a uniform-parameter AE statement.'},
 {'start_line':ln('    · have hi0'),'finding':'At index0 the record is (0,z0), the clock is0 and positive sample0 implies positive epsilon0. For record1 stopped, eventTime1=top and 0<top. For record1 live b, actual76 hstrict at index0 gives 0<b.time, hence 0<T1. Thus t0 belongs to interval0; deterministic hZ then Phi0 gives Z0=z0. This explicitly includes a first infinite wait/rank0/zero-hazard path; no division by an energy cap, no finite first-wait premise, and no claim of initialization on exceptional zero-threshold samples.'}
 ],
 'Mathlib_piecewise_API':raw(mathlib),
 'boundary':{
 'fallback':'On every uncovered input the total representative equals z0 by specification; this is an explicit ASTIS convention, not source physical dynamics beyond a possible accumulation point.',
 'stopping':'The final live arc continues at every finite elapsed time if its next actual waiting time is top. Stopped records have no source phase and never belong to D_n.',
 'zero_waits':'Permitted deterministically; empty half-open intervals do not invalidate disjointness. Positive Exp input is consumed only for AE initialization and actual79 coverage through its parents.',
 'random_parameters':'V/alpha/beta/eta remain fixed. y/xRef/z0/t/sample are joint measurable coordinates, but fixed-parameter AE conclusions do not establish arbitrary correlated random-parameter law substitution.',
 'pending':'Path regularity/adaptedness, process/kernel/random-init laws, Markov/invariance, errors/cost/composition, final decoder/source audit, commit-bound verification, integration/publication/purification/main and whole Goal remain separate.'},
 'repair_required':False,'new_public_premises':[],'own_native_negative_runs':[],'native_failures_policy':'No negative occurred in this independent run. Existing root diagnostics were not edited or overwritten. No native reasoning trajectory is claimed.',
 'production_edited':False,'source_blind_decode_credit':False,'final_source_review_credit':False,'VERIFIED_credit':False
})
decision=save('decision80.json',{'status':'ACCEPTED_INDEPENDENT_MATHEMATICS','reviewer':'/root/exact_verify77','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'module':raw(M),'statement_definition_audit':raw(O/'statement-definition-audit80.json'),'whole_proof_review':proof,'fresh_whole_source_receipt':raw(O/'fresh-whole-module.receipt.json'),'axioms':deps['axioms'],'kernel_closure':raw(O/'kernel-dependency-summary80.json'),'fakeclosure':raw(O/'fake-closure-scan80.json'),'repair_required':False,'truth_boundary':'Only the exact total joint finite-time measurable realization and per-fixed-parameter common-AE actual arc/init theorem. No source/blind/VERIFIED/integration/reader/purification/whole-Goal admission.','checked_commit':None})
for e in freeze['inputs']:assert raw(R/e['path'])==e
files=sorted([p for p in O.iterdir() if p.is_file()],key=lambda p:p.name)
manifest=save('closed-manifest80.json',{'status':'CLOSED_INDEPENDENT_MATHEMATICAL_REVIEW','reviewer':'/root/exact_verify77','module':raw(M),'decision':decision,'all_frozen_inputs_unchanged':True,'additional_consulted_API':raw(mathlib),'artifacts':[raw(p) for p in files],'manifest_self_hash_omitted_to_avoid_cycle':True,'no_production_shared_ledger_cell_edits':True})
print(json.dumps({'decision':decision,'closed_manifest':manifest},ensure_ascii=False))
