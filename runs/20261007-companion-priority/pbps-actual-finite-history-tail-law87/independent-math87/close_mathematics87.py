from pathlib import Path
import datetime,hashlib,json,re,subprocess
R=Path('E:/Samplinglib');O=Path(__file__).parent;B=O.parent
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):
 p=Path(p); b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def read(p):return json.loads(Path(p).read_text('utf8'))
def put(n,d):
 with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
M=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteHistoryTailLaw.lean';s=M.read_text('utf8');mr='01fcff944f1dbd42be2af30063b9baf4e191e2cde959e008724387cadb4fc899'
assert pin(M)['raw_sha256']==mr
seal=read(B/'root.statement-seal87.json');assert seal['expanded_literal_Prop'] in s
private=s[s.index('private def '):s.index('\n\n\nset_option maxHeartbeats')]
body=s[s.index(' := by\n  classical')+len(' := by\n'):s.index('\nend\nend ')]
def ds(x,indent):
 first=x.index(' '*indent+'let c :');last=x.index(' '*indent+'∀ y xRef : E',first) if indent==4 else x.index('  change',first)
 x=x[first:last];starts=list(re.finditer(r'^'+(' '*indent)+r'let ([^\s:]+).*',x,re.M));out={}
 for i,m in enumerate(starts):
  v=x[m.start():starts[i+1].start() if i+1<len(starts) else len(x)].rstrip()
  out[m.group(1)]='\n'.join(line[indent:] for line in v.splitlines())
 return out
pd=ds(private,4);bd=ds(body,2);assert pd==bd and len(pd)==13
parent=(R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteJumpRecursion.lean').read_text('utf8')
def sig(x):return x[x.index('    {E : Type*}'):x.index(' : Prop :=')]
assert sig(private)==sig(parent)
ps=parent[parent.index('private def '):parent.index('\nset_option maxHeartbeats')]
# The original parent has the same eight literal actual algorithm definitions.
starts=list(re.finditer(r'^    let ([^\s:]+).*',ps,re.M));par={}
for i,m in enumerate(starts):
 if i+1==len(starts):break
 v=ps[m.start():starts[i+1].start()].rstrip();par[m.group(1)]='\n'.join(line[4:] for line in v.splitlines())
actual=['c','Φ','S','rate','Λ','τ','next','record']
for n in actual: assert pd[n]==par[n],n
put('statement-definition-audit87.json',dict(status='PASS_EXACT_SEALED_FULL_PROP_AND_ACTUAL_LITERAL_IDENTITIES',module=pin(M),seal=pin(B/'root.statement-seal87.json'),header=pin(B/'header87.proposed.lean'),full_private_Prop_byte_substring_unchanged=True,six_analytic_binders_identical_to_actual76=True,six_binders=['hα','hαβ','hV','hH','hη','hβη'],definition_count=13,definition_names=list(pd),all_thirteen_private_and_public_BODY_definitions_identical_after_indentation_only=True,eight_actual_parent76_definitions_identical_after_line_ending_and_indentation_read_normalization=actual,per_definition_normalized_text_sha256={n:hashlib.sha256(v.encode()).hexdigest() for n,v in pd.items()},raw_file_hashes_preserved_without_normalization=True,public_provider_premises=[],quantifiers='For every fixed deterministic y,xRef,z0,n and every Borel history event A; pointwise causality all raw samples; eight-conjunct exact conclusion.',no_past_ambient_or_tail_association_drift=True))
audit=[
 dict(region=[87,147],claim='Actual definitions, exact goal and internal producers',reason='The public theorem reintroduces all thirteen sealed literal definitions and changes to the complete eight-conjunct target, not a weaker helper. Parent76 supplies each joint record map with association ((y,xRef),(z0,e)); UnitExp77 supplies probability and mutual coordinate independence. Neither ingredient is supplied by caller.'),
 dict(region=[148,171],claim='Actual finite-prefix causality and ambient measurability',reason='Induction on record depth m: base is initial live record; successor uses only e m and the prior record. Agreement below n includes every clock below each j<=n. Fin(n+1) includes recordn but does not consume clockn. Clipping is Borel, record parent is jointly measurable, and countable tail coordinates are ambient measurable.'),
 dict(region=[172,186],claim='Past measurable factorization input',reason='truncated w k is epsilon(w,k) for k<n and 0 otherwise. Each used coordinate has comap below past n; clipping preserves measurability, unused coordinates constant. Local MeasurableSpace instance is scoped within htruncated. This auxiliary stream is never substituted into the algorithm or P as a new definition.'),
 dict(region=[187,201],claim='Actual history is past-measurable',reason='For each j<=n, causality equates record(truncated w,j) with original record(epsilon w,j). Compose actual jointly measurable record with deterministic parameters and the past-measurable auxiliary stream; transport via this pointwise equality and finite Pi measurability. This proves a real measurable factorization, not an invalid inference from set-theoretic causality alone.'),
 dict(region=[202,218],claim='Disjoint complete past and future sigma algebras',reason='future n is join of coordinate comaps for k>=n. tail coordinate n+k lies there. The future local instance ends before hblocks; all coordinate comap bounds there use ambient product sigma. Actual full iid yields independence of joins over disjoint Iio n/Ici n by Mathlib indep_iSup_of_disjoint. Monotonicity through hHp/hTf then gives independence of the two complete random objects.'),
 dict(region=[219,237],claim='Whole countable-tail law, product law and unnormalized restriction',reason='Mathlib infinitePi reindex under injective k↦n+k yields the entire tail law P. IndepFun.map_prod_eq_prod_map_map yields ordered joint law history×tail, then substitute tail=P. On every Borel B, map/restrict evaluation, independence and tail law give restricted-tail mass P(history∈A)P(B). ENNReal measure scalar and Measure.ext conclude without division or a positive-probability condition.')]
cases=[
 dict(case='n=0',finding='Fin1 history is constant initial live record, past0=bottom and tail0=id. The induction/factorization and disjoint-sigma proof include this case. Restricted identity has event mass0 or1, no empty-history convention change.'),
 dict(case='P(history in A)=0 / A empty / A whole',finding='No normalized conditional law is asserted. Restriction has mass0 /0 /1 and right side is the corresponding scalar P, so no division-by-zero or positive-event premise.'),
 dict(case='stopped or first wait infinity',finding='Sum.inr absorbs in actual next; stopped tags remain records, without a fictional phase at infinity. Causality and measurability handle the actual Sum definition. Unused raw inputs remain defined independently of whether algorithm uses them.'),
 dict(case='zero or negative raw thresholds',finding='Real.toNNReal supplies a total ambient Borel extension. The deterministic causality statement quantifies every raw sample and uses no positivity. Under actual Exp1 inputs nonpositive samples are null, but that fact is unnecessary for this probability substrate.'),
 dict(case='rank0 / zero normal / zero or flat intensity',finding='No nondegeneracy, strictly increasing hazard, finite wait or cap is needed. Existing total division and top-guarded untopD are literal parent semantics. The proof never silently projects a stopped phase.'),
 dict(case='full countable tail versus marginals',finding='Full iIndepFun and generated sigma algebra independence, not pairwise independence, are consumed. The infinitePi pushforward theorem identifies the whole countable law, not only cylinder marginals.'),
 dict(case='deterministic parameters and deterministic depth',finding='No random stopping index, correlated random parameters, physical-time residual clock, conditional random hazard density, CK/Markov restart or uniform-parameter AE event is claimed.')]
put('whole-mathematics-review87.json',dict(status='ACCEPTED_INDEPENDENT_MATHEMATICS_ONLY',reviewer_id='/root/exact_verify77',created_utc=now(),module=pin(M),whole_BODY_read_and_audited=True,not_reusing_header_verdict_as_final=True,proof_audit=audit,counterexample_and_exceptional_case_audit=cases,hidden_hypotheses_found=[],required_mathematical_repairs=[],actual_ASTIS_bridge='New actual finite-recursion prefix causality and past-sigma measurable factorization connect literal source dynamics to iid full-tail independence/laws. A meaningful deterministic-history consumer of existing producers; no supplied general measurable-map wrapper.',generic_reuse_boundary='Disjoint sigma algebra independence, infinitePi injective reindex and generic IndepFun joint law are existing pinned Mathlib results, not newly proved ASTIS generic independence theorems.',source_slice_alignment='Frozen independently accepted source-slice87.v2 I1/I2/I3 substrate consumed; I4 conditional random-hazard next-wait survival and I5 finite-density/final-survival/fullA7 remain OPEN. No source topology inferred or approved from Lean BODY.',exposition='All six contiguous BODY regions and complete attributed restatement inspected; three exposition-only fields require distinct exact-proposal review. This does not alter mathematical acceptance.',required_exposition_repairs=pin(O/'proposed-exposition-overlay87.json'),not_source_or_blind_verdict=True))
inputs={x['path']:x for x in read(O/'input-freeze87.json')['actual_inputs']}
extra=[B/'publication-freeze87.json',B/'header-math87/definition-readback87.json',B/'header-math87/mathematical-review87.json',B/'header-math87/review_header87.attempt2.py',R/'.agents/skills/astis-semantic-roundtrip/SKILL.md',R/'.agents/skills/astis-substantive-advance/SKILL.md',R/'tools/astis.py']
for p in extra:inputs[p.relative_to(R).as_posix()]=pin(p)
for i in read(O/'transitive-kernel-source-binding87.json')['distinct_project_source_files']:inputs[i['path']]=i
for i in inputs.values():assert pin(R/i['path'])==i
for i in read(O/'collaborator-preservation87.json')['RAWs']:assert pin(R/i['path'])==i
kernel=read(O/'kernel-dependency-summary87.json')
receipts=[pin(O/(n+'.receipt.json')) for n in ['fresh-focused-build','fresh-whole-source-kernel']]
put('decision87.json',dict(status='ACCEPTED_INDEPENDENT_MATHEMATICS_ONLY',reviewer_id='/root/exact_verify77',created_utc=now(),checked_module=pin(M),observed_pre_science_commit=read(O/'input-freeze87.json')['observed_head'],checked_commit_is_not_future_science_commit=True,whole_maths=pin(O/'whole-mathematics-review87.json'),literal_definition_audit=pin(O/'statement-definition-audit87.json'),kernel=pin(O/'kernel-dependency-summary87.json'),kernel_source_binding=pin(O/'transitive-kernel-source-binding87.json'),fake_closure_scan=pin(O/'fake-closure-scan87.json'),terminal_receipts=receipts,standard_axioms_only=True,required_mathematical_repairs=[],required_exposition_repairs=pin(O/'proposed-exposition-overlay87.json'),exposition_status='Original full restatement and all six BODY regions checked; exact three-field overlay awaits distinct review, separate from Lean mathematical acceptance.',all21collaborator_RAWs_preserved=True,VERIFIED=False,PROVED_LOCAL=False,remaining_truth_boundary='Conditional random-hazard next-wait survival/density, final survival and fullA7 finite-event iteration/path law, reversal/invariance/restart/Markov/CK/allL2/cost/main/composition/wholepaper/Goal remain OPEN. Final independent source review, blind decoding and named science commit admission are separate.'))
put('run-manifest87.json',dict(status='CLOSED_INDEPENDENT_MATHEMATICS_ORIGINAL_EXPOSITION_REVIEW',reviewer_id='/root/exact_verify77',created_utc=now(),observed_head=read(O/'input-freeze87.json')['observed_head'],frozen_current_inputs=list(inputs.values()),original_exposition_inputs_resolve_immutable_snapshots=pin(O/'original-exposition-snapshot-index87.json'),terminal_receipts=receipts,decision=pin(O/'decision87.json'),exposition_overlay=pin(O/'exposition-overlay87.closed-RAW-manifest.json'),no_production_or_shared_mutation=True,no_final_source_or_blind_verdict_read=True,native_reasoning_trajectory_claimed=False,full_math_review_not_source_acceptance=True))
artifacts=[pin(p) for p in sorted(O.iterdir()) if p.is_file() and p.name!='closed-RAW-manifest87.json']
put('closed-RAW-manifest87.json',dict(status='CLOSED_RAW_NONCIRCULAR',created_utc=now(),reviewer_id='/root/exact_verify77',frozen_current_inputs=list(inputs.values()),historical_exposition_snapshots=read(O/'original-exposition-snapshot-index87.json')['snapshots'],owned_artifacts=artifacts,self_hash_intentionally_omitted=True,all21collaborator_RAWs_preserved=True,exposition_overlay_requires_distinct_review=True,independent_science_commit_admission=False))
for i in artifacts:assert pin(R/i['path'])==i
for i in inputs.values():assert pin(R/i['path'])==i
print(json.dumps(dict(status='ACCEPTED_MATHEMATICS_NATIVE_CLOSED_REHASH_PASS',decision=pin(O/'decision87.json'),manifest=pin(O/'closed-RAW-manifest87.json'),receipts=receipts),indent=2))
