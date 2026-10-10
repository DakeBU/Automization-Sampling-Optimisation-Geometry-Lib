from pathlib import Path
import datetime,hashlib,json
R=Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-actual-bounded-test-continuity83';O=B/'header-review83';H=B/'header83.proposed.lean'
def info(p):
 b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest())
def load(p):return json.loads(p.read_text(encoding='utf8'))
def save(n,d):
 with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
freeze=load(O/'input-freeze83.json')
for e in freeze['inputs']:assert info(R/e['path'])==e
receipt=load(O/'typecheck83.receipt.json');assert receipt['exit_code']==0 and receipt['terminal_closed'] and receipt['proof_BODY']==False
findings=[
 dict(id='H83-01',status='PASS',finding='Full private proposition is genuinely an extension of actual82: original six analytic binders, eleven actual literal definitions, joint measurable phase, deterministic covered arcs, uncovered-z0 fallback, per-fixed-parameter common AE allfinite/init, measurable defect estimate and positive-threshold stochastic continuity are byte-text preserved. No new analytic or public process/provider premise.'),
 dict(id='H83-02',status='PASS',finding='The same existential Z is chosen before all parameters and tests; later universal y,xRef,z0,f,M quantifiers act on that actual witness. The new output applies to each fixed deterministic parameter triple. No uncountable uniform nullset or limit and no arbitrary correlated parameter substitution is asserted.'),
 dict(id='H83-03',status='PASS',finding='Every continuous real-valued phase test and every real M>=0 with global |f|<=M is explicitly quantified before every finite t and the limit. M is not free or existentially hidden in the estimate. Negative-valued tests are allowed. M=0 forces f=0 and produces the valid zero estimate/limit.'),
 dict(id='H83-04',status='PASS',finding='Continuity of f gives Borel measurability, and section measurability follows from the retained joint actual Z. Global bound M over the actual finite probability P gives integrability at all finite times, including after jumps and on the exceptional total representative. No moment bound, uniform integrability or unbounded-test conclusion is being assumed.'),
 dict(id='H83-05',status='PASS',finding='The quantitative estimate has the correct constant2M and actual hazard Lambda: the discrepancy against deterministic f(Phi_tz0) is zero outside the actual phase-flow defect and bounded by2M on it. Hence the intended absolute expectation estimate is mathematically valid. It needs internal integrability/measure comparison, not a supplied estimate or a defect=jump-event equality.'),
 dict(id='H83-06',status='PASS',finding='Continuity of f at z0 and actual harmonic continuity/identity at0, with actual Lambda continuity and Lambda0=0, make the comparison term and its2M bound converge appropriately. Ordinary nonpunctured NNReal neighborhood0 is correct: retained AE Z0=z0 and P probability give the correct integral at0. Probability convergence is not promoted to AS sample convergence or used in ordinary samplewise DCT.'),
 dict(id='H83-07',status='PASS',finding='rank0 is allowed: singleton phase gives constant tests and exact zero defect. Zero rate/energy/cap and infinity firstwait need no division by a cap or finite-wait premise. Half-open endpoint conventions, infinite last-live arcs, stopped records without phase, raw zero/nonpositive exceptional inputs and uncovered-z0 fallback are exactly inherited. At-event equality with no-jump flow is not claimed.'),
 dict(id='H83-08',status='PASS',finding='Source uses C_c real tests. The header correctly specifies the explicitly labelled ASTIS C_b pointwise extension; source C_c tests qualify because continuity plus compact support implies global boundedness. It does not assert Feller/C0 preservation, continuity in initial phase for positive time, arbitrary unbounded expectations, full L2 or Markov/semigroup/invariance consequences.'),
 dict(id='H83-09',status='PASS',finding='Complete named private Prop elaborated fresh, not a reduced fragment/wrapper/equivalence theorem. Original section/namespace ends are already correct. Sole local overlay adds #check commands before the existing section end; no mathematical or syntax repair, proof placeholder or theorem BODY.'),
 dict(id='H83-10',status='PASS',finding='Four intended basic APIs are available under the proposed exact imports and fixed pinned Mathlib: Integrable.of_bound requires finite measure and AE strongly measurable bounded composition; integral_mono_ae requires both integrals exist; norm_integral_le_integral_norm is available; integral_indicator_const requires a measurable defect set. These conditions are obtainable internally from actual82/actual probability and the test contract; no API-driven binder repair identified.'),
 dict(id='H83-11',status='PASS',finding='Reviewed-effective source graph mechanically equals original graph plus supplement and the exact independently proposed overlay: E29/E30 AND inside optional branch, branch-output OR, E28 nondependency boundary association. Nodes and original frozen files remain unchanged. This comparison is not a new source BODY review or statement seal.')]
save('independent-header-mathematics83.json',dict(schema_version=1,status='ACCEPTED_PROSPECTIVE_HEADER_MATHEMATICS_AND_TYPE',
 reviewer_id='/root/exact_verify77',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),header=info(H),
 definition_readback=info(O/'definition-readback83.json'),typecheck=info(O/'typecheck83.receipt.json'),findings=findings,
 required_repairs=[],new_analytic_hypotheses=[],new_public_provider_premises=[],
 source_class='Explicit bounded continuous real test extension of source compactly supported continuous pointwise ingredient.',
 source_scope_review='Own prior primary-first topology review and separately reviewed exact-overlay effective graph; no83 implementation used to decide source topology.',
 API_type_checks=[dict(declaration='MeasureTheory.Integrable.of_bound',conditions=['IsFiniteMeasure P','AEStronglyMeasurable composition','AE norm<=M']),dict(declaration='MeasureTheory.integral_mono_ae',conditions=['Integrable f','Integrable g','AE comparison']),dict(declaration='MeasureTheory.norm_integral_le_integral_norm',conditions=['Bochner real integral, available under given imports']),dict(declaration='MeasureTheory.integral_indicator_const',conditions=['MeasurableSet defect'])],
 proof_not_started_by_reviewer=True,proof_API_implementation_or_tactics_added=False,
 warnings='Native private-definition unused-binder linter warnings are retained. Source assumptions must stay exact; linter suggestions to remove them are not adopted.',
 role_limits=dict(StatementSeal=False,theorem_BODY=False,proof_implemented=False,production_shared_state_changed=False,SAU_claim=False,VERIFIED=False,source_final_BODY_acceptance=False),
 remaining_obligations=['Root StatementSeal only after independent header/source decisions are admitted','Future actual proof must derive composition integrability, exact2M indicator estimate, and expectation limit internally from actual parents','Independent full BODY mathematics, blind decoder, source review and committed exact verifier remain future gates','Outer initial-state L2 DCT, invariance/Jensen contraction, representative independence/density, Markov/restart/semigroup, hypocoercivity, implementation, cost/main/composition and reader/purification/Goal completion remain open']))
save('decision83.json',dict(status='ACCEPTED_PROSPECTIVE_COMPLETE_HEADER_NO_REPAIR',reviewer_id='/root/exact_verify77',header=info(H),
 mathematical_review=info(O/'independent-header-mathematics83.json'),typecheck_receipt=info(O/'typecheck83.receipt.json'),
 original_six_binders_eleven_definitions_all82_clauses_exact=True,quantified_all_valid_M=True,
 complete_private_Prop_typechecked=True,required_repairs=[],StatementSeal=False,proof=False,VERIFIED=False))
save('closed-RAW-manifest83.json',dict(status='CLOSED_NONCIRCULAR_INDEPENDENT_HEADER_REVIEW',reviewer_id='/root/exact_verify77',
 header_RAW_sha256=info(H)['RAW_sha256'],fixed_mathlib_commit=freeze['fixed_mathlib_commit'],
 inputs=freeze['inputs'],owned_artifacts=[info(p) for p in sorted(O.iterdir()) if p.is_file()],
 self_hash_excluded=True,dependency_direction='Manifest binds closed decision, complete-source typecheck probe/logs/receipt and literal readback. None hashes this manifest.',
 all_foreground_children_terminal_closed=True,StatementSeal=False,proof=False,VERIFIED=False))
print(json.dumps({n:info(O/n)['RAW_sha256'] for n in ['decision83.json','independent-header-mathematics83.json','typecheck83.receipt.json','closed-RAW-manifest83.json']},indent=2))
