from pathlib import Path
import json,hashlib,datetime
R=Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-actual-physical-time-cover79';O=B/'independent-math79'
def info(p):
 b=p.read_bytes();return dict(path=str(p),RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest())
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def save(n,v):
 p=O/n;assert not p.exists();p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
summary=load(O/'fresh-compiler-dependency-summary79.json');assert summary['status']=='PASS_FULL_SOURCE_STANDARD_THREE_EXACT_ACTUAL_PARENTS'
assert info(R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualNonaccumulation.lean')['RAW_sha256']=='e6d71cb969b30f6ac8e6be65e5cd067166b4f29213d9328ed9edc0971fd026fc'
assert info(R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteJumpRecursion.lean')['RAW_sha256']=='1f1ebc187676e0481247bc2f58ec0bf94b2fc6f02a563b87009a0fe7bfb4910c'
M=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhysicalTimeCover.lean'
assert info(M)==summary['module']
checks=[
 dict(lines=[16,73],case='sealed target',finding='Complete literal private Prop equals independently reviewed sealed original byte-for-byte. Six analytic source binders retained, no iid/support/nonexplosion/clock/selected-index/cap/measurability providers. Public theorem result invokes this private complete specification, so compilation cannot hide a weakened replacement proposition.'),
 dict(lines=[89,123],case='actual body definitions',finding='All eleven literal BODY definitions agree with private Prop and actual78. Nine recurrence/flow/rate/hazard objects agree with actual76. Sample k is the zero-based source E_(k+1); record n has consumed n thresholds. No numerical surrogate clock or phase at top occurs.'),
 dict(lines=[124,136],case='parents and common AE event',finding='The actual76 call consumes the original six hypotheses and extracts guarded live-step, initialization and monotonicity. The actual78 call consumes the same data and provides finite-horizon escape. Fix y/xRef/z0 first, then filter_upwards over a single input event supports both conclusions simultaneously for all finite t. No uncountable intersection or selected-index premise is introduced.'),
 dict(lines=[138,147],case='first crossing exists',finding='Actual escape at finite horizon t supplies N with t<T_N, hence an inhabited predicate for Nat.find. This permits finite or top crossing clocks, including stopping. It does not assert eventual top or strict positivity of every increment.'),
 dict(lines=[146,157],case='initialized predecessor',finding='The least crossing k cannot be0 since T0=0<=t. Thus k>0 and n=k-1 has n+1=k. Nat.find_min gives not(t<T_n), yielding T_n<=t in the linear extended order. Finite t then guarantees a finite left endpoint, even when right endpoint is top.'),
 dict(lines=[158,167],case='half-open uniqueness and zero waits',finding='If m>n then n+1<=m, so monotonicity gives T_(n+1)<=T_m<=t, contradicting t<T_(n+1). The symmetric case excludes m<n. Hence m=n. Equal consecutive times/zero waits make empty intervals rather than duplicate containing intervals; no strict-wait assumption is needed.'),
 dict(lines=[168,179],case='stopped left endpoint impossible',finding='A stopped record has eventTime=top. This contradicts eventTime<=finite t. The branch is rejected before any attempt to use an elapsed phase, so no arbitrary state or untopD0 top value is manufactured.'),
 dict(lines=[180,187],case='actual live record and elapsed nonnegativity',finding='A live record a has eventTime=(a.time:WithTop NNReal); coe-order reflection derives a.time<=t. The elapsed NNReal subtraction t-a.time is therefore the ordinary nonnegative finite elapsed offset, not truncation of a negative duration. The stored phase is actual post-record phase.'),
 dict(lines=[187,190],case='infinite next wait and last active arc',finding='If actual tau(a.phase,epsilon_n)=top, every finite elapsed offset coerced into WithTop is below it. The proof retains current live a, rather than selecting later absorbed records; all finite physical horizons after that last clock are admissible offsets.'),
 dict(lines=[191,207],case='finite next wait',finding='Only after tau!=top, q=untop(tau) is introduced with its exact coercion equality. Actual76 guarded next recursion supplies next time=a.time+q; the same actual tau is used in both recurrence and target. From t<a.time+q and a.time<=t, pinned tsub_lt_iff_right proves t-a.time<q. This handles finite q=0 honestly: interval hypotheses would be inconsistent; no division/positivity assertion is added.'),
 dict(lines=[208,210],case='unique stored record',finding='The dependent record case split rewrites record n to Sum.inl a. Any candidate b satisfies Sum.inl a=Sum.inl b. Constructor injectivity, oriented symmetrically, yields b=a. The extra timing/wait properties cannot introduce another stored record.'),
 dict(lines=[16,210],case='rank0, stopping and truth boundary',finding='Dimension zero/zero cap remain legal. Actual78 may yield a first top clock with initial live arc covering every finite t. Continuing nonaccumulating paths also remain legal. Finite jump endpoints use half-open intervals; this theorem does not independently assert n(0)=0 on exceptional zero thresholds, Phi0 interpolation, a chosen measurable global phase map, process uniqueness in law, Markov/invariance/kernel/main/cost/composition results.')]
save('whole-proof-mathematics79.json',dict(status='ACCEPTED_WHOLE_IMPLEMENTATION_MATHEMATICS_ONLY',reviewer='/root/exact_verify77',module=info(M),
 mathematical_cases=checks,no_mathematical_repair_required=True,no_new_public_premises=True,
 fixed_local_API=dict(path='.lake/packages/mathlib/Mathlib/Algebra/Order/Sub/Unbundled/Basic.lean',line=210,
 theorem='tsub_lt_iff_right (hbc : b<=a) : a-b<c iff a<c+b',use='a=t,b=a.time,c=q; record-derived a.time<=t is passed explicitly'),
 proof_dependencies=summary['direct_ASTIS_dependencies'],blockers=[],repairs=[],
 purification_notes=['Explicit UnitExponentialProduct import is unused directly; actual78 carries the stochastic event. Optional later minimal-import cleanup, no mathematical defect.'],
 independent_source_review=False,source_blind_decoder=False,exact_commit_verification=False,VERIFIED=False,Goal_complete=False,
 provenance='Complete source proof was directly inspected; literal definitions and seal compared mechanically; fresh full-source Lean and dependency/axiom receipts recorded. This is not a fabricated native reasoning trajectory.'))
decision=dict(status='ACCEPTED_INDEPENDENT_WHOLE_MATHEMATICS79_ONLY',reviewer='/root/exact_verify77',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),module=info(M),
 whole_proof=info(O/'whole-proof-mathematics79.json'),statement_definition_audit=info(O/'statement-definition-audit79.json'),input_freeze=info(O/'input-freeze79.json'),
 fresh_complete_source_receipt=info(O/'fresh-whole-module.receipt.json'),compiler_dependency_summary=info(O/'fresh-compiler-dependency-summary79.json'),
 fake_closure_scan=info(O/'fake-closure-scan79.json'),axioms=summary['axioms'],direct_ASTIS_dependencies=summary['direct_ASTIS_dependencies'],
 no_repair_required=True,production_edits=False,ledger_or_cell_edits=False,proof_authoring=False,
 limits='Independent mathematical acceptance only. Fresh source-blind reconstruction, final source review/publication and later exact-commit VERIFIED admission remain separate; no global-process/main/merge/purification/Goal credit.')
save('decision79.json',decision)
save('closed-manifest79.json',dict(status=decision['status'],module=info(M),artifacts=[info(p) for p in sorted(O.iterdir()) if p.is_file()],no_production_edits=True,no_VERIFIED_transition=True))
print(decision['status']);print('MODULE',info(M)['RAW_sha256']);print('DECISION',info(O/'decision79.json')['RAW_sha256'])
