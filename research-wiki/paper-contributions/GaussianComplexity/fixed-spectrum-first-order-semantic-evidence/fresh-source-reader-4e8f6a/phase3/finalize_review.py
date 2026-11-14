from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess,shutil,sys
sys.dont_write_bytecode=True
ROOT=Path('/Users/zhouhuanjian/ASTIS-GC')
BASE=ROOT/'.astis/semantic-neutral-20261108/src_4e8f6a'
OUT=BASE/'phase3'
HEAD='9d306d837fbddf1518b0035494baaf5c21c24488'
PUB='51d5a5e9390a0d66c2d5b72d042a042eec8d3d60433043ea3909bf9320ccb31e'
H=lambda b:hashlib.sha256(b).hexdigest()
def dump(name,obj):
 (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')

packet=json.loads((OUT/'inputs/full-anti-anchored-reviewer-packet.json').read_text())
pins=json.loads((OUT/'inputs/full-review-input-pins.json').read_text())
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==HEAD
assert H((BASE/'phase1/freeze_manifest.json').read_bytes())=='cf4dd57dc05d19cb3ca6938032a7730d402aba6220a200ae4a3afe2aca721fac'
assert H((BASE/'phase2/freeze_manifest.json').read_bytes())=='85a0e1542ce93bd0f65203f136fbe8879f2f9be1713f0c05861ab3885af5971c'
for rel,sha in pins['exact_inputs'].items():
 assert H((ROOT/rel).read_bytes())==sha,rel
source=ROOT/'.astis/huanjian-resume-20261103/2610.20492v1.html'
assert len(source.read_bytes())==951991
assert H(source.read_bytes())=='6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915'
compile_receipt=json.loads((OUT/'fresh_compile_receipt.json').read_text())
assert len(compile_receipt['runs'])==4 and all(r['returncode']==0 for r in compile_receipt['runs'])
kernel=json.loads((OUT/'kernel_application_receipt.json').read_text())
assert kernel['returncode']==0
assert 'REVIEW_REFLECTION_ASSERTIONS_PASSED' in (OUT/'logs/IndependentKernelApplication.log').read_text()
assert json.loads((OUT/'focused_fake_closure_receipt.json').read_text())['scan_passed']
literal=json.loads((OUT/'reader_literal_codepoint_receipt.json').read_text())
assert literal['formula_leading_backslash_count']==1
assert literal['any_adjacent_backslashes_in_decoded_lesson_string'] is False
assert literal['main_equation_exactly_single_delimiters_plus_decoded_formula']

meaning_inputs=[
 ('.lake/packages/mathlib/Mathlib/Analysis/Calculus/Gradient/Basic.lean',[[52,105],[168,177]],'HasGradientAt is genuine Frechet/Riesz differentiability; gradient is totalized and its identification theorem requires the genuine witness.'),
 ('.lake/packages/mathlib/Mathlib/Analysis/Calculus/FDeriv/Defs.lean',[[97,166]],'Derivative is a little-o condition; differentiability is existence; fderiv has zero fallback outside existence.'),
 ('.lake/packages/mathlib/Mathlib/Analysis/Calculus/FDeriv/Basic.lean',[[228,239]],'Non-differentiability yields zero fderiv, distinct from a genuine derivative witness.'),
 ('.lake/packages/mathlib/Mathlib/LinearAlgebra/UnitaryGroup.lean',[[282,307]],'Full real orthogonal group, not special orthogonal; transpose is inverse.'),
 ('.lake/packages/mathlib/Mathlib/LinearAlgebra/Matrix/PosDef.lean',[[50,70],[154,173]],'PosDef contains Hermitian symmetry; taking .1.1 of actual admissibility produces that proof internally.'),
 ('.lake/packages/mathlib/Mathlib/Analysis/CStarAlgebra/Matrix.lean',[[94,128]],'The star-algebra equivalence to continuous linear maps preserves coordinates and inner products.'),
 ('.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Adjoint.lean',[[376,385]],'Self-adjoint continuous linear maps are symmetric.'),
 ('.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Symmetric.lean',[[72,80]],'Symmetric map inner-product exchange used in hlin.'),
 ('.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Calculus.lean',[[45,55],[94,102]],'Actual derivative formula for a pair of inner-product factors.'),
 ('.lake/packages/mathlib/Mathlib/Analysis/Calculus/FDeriv/Mul.lean',[[345,359]],'Multiplication by 1/2 preserves derivative existence with scalar derivative.'),
 ('/Users/zhouhuanjian/.elan/toolchains/leanprover--lean4---v4.33.0/src/lean/Lean/Util/CollectAxioms.lean',[[1,176]],'Kernel-environment axiom collection and imported axiom caching; reflection is not a proof of source fidelity.')
]
meaning_manifest=[]
for rel,ranges,meaning in meaning_inputs:
 path=Path(rel) if rel.startswith('/') else ROOT/rel
 raw=path.read_bytes()
 dest=OUT/'inputs/standard-meanings'/path.name
 # Avoid ambiguous duplicate Basic.lean snapshots.
 dest=OUT/'inputs/standard-meanings'/(H(rel.encode())[:10]+'-'+path.name)
 dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw)
 meaning_manifest.append({'original_path':str(path),'snapshot':str(dest.relative_to(OUT)),
   'whole_file_sha256':H(raw),'semantic_read_line_ranges':ranges,'checked_meaning':meaning,
   'semantic_read_scope':'Only the listed necessary definitions/theorems, not an audit of the entire copied file.'})
dump('necessary_standard_meanings.json',{'toolchain':'Lean 4.33.0','dependency_manifest_sha256':H((ROOT/'lake-manifest.json').read_bytes()),'inputs':meaning_manifest})

semantic_slots={
 'objects':{
  'original':'Frozen P2-04 exact first-order pair for f_A=xᵀAx/2, instantiated by the H4-02 cosine-grid precision. Frozen H4-04 gives matched A_2,A_κ replies using the same O.',
  'reconstructed':'Anonymous reconstruction retains the literal local constructor, Euclidean quadratic, Ax query, genuine derivative and pair. Actual private Test constructs A_η with that same O and the forward reply g.',
  'relation':'equivalent',
  'evidence':'Actual source bytes, Phase1/2 freezes, complete producer/Test, kernel type log, and exact code extraction agree. No A⁻¹x or primitive Ox oracle is substituted.'},
 'domains':{
  'original':'Real R^d, d≥2, κ≥2, full O(d), one-based source indices 1,…,d.',
  'reconstructed':'EuclideanSpace R (Fin d), all real orthogonalGroup matrices, zero-based Fin values; WithLp maps keep coordinates.',
  'relation':'equivalent',
  'evidence':'j=i.val+1 identifies the grid exactly. Actual orthogonalGroup meanings and explicit Fin2 determinant +1 and −1 applications were checked. No determinant-sign premise is added.'},
 'quantifiers':{
  'original':'For each local d≥2,κ≥2 and every full orthogonal O and query x, the first-order formula; for the affine component both matrices share this O.',
  'reconstructed':'Kernel types show exactly d,hd,κ,hκ,O then local lets then all x. Actual Test retains the same O across A_η and applies actual providers at that x.',
  'relation':'same',
  'evidence':'Independent anonymous application and kernel type reflection succeed. No δ,d₀,q,ε,Haar,seed,transcript or algorithm quantifier is silently appended or advertised.'},
 'assumptions':{
  'original':'Local family bounds, literal quadratic and orthogonal membership. Symmetry/admissibility and gradient existence are mathematical source facts, not convenience premises.',
  'reconstructed':'The public and private signatures have only the local source bounds and O carrier. Actual producer takes symmetry from the actual admissibility theorem internally; it constructs HasGradientAt before using total gradient.',
  'relation':'explicit-elaboration',
  'evidence':'Whole files and reflected types contain no supplied derivative, gradient certificate, affine identity, reply correctness, regularity or nonzero-reciprocal premise. The source bounds can be nonminimal for bare quadratic calculus without being an excess assumption.'},
 'conclusion':{
  'original':'P2-04 gradient Ax and centered value ⟨x,Ax⟩/2; C4-02 supplies ordinary differentiability context. H4-04 forward substitution composes with that formula.',
  'reconstructed':'Public theorem returns actual HasGradientAt and exact value/gradient pair. Private Test returns these for g=(κ−1)A_2x−(κ−2)x=A_κx.',
  'relation':'equivalent',
  'evidence':'hraw directly differentiates the actual quadratic, hlin uses actual symmetry, hasGradientAt_iff_hasFDerivAt constructs hgrad, and hg.gradient is used only afterward. Test .1 forward identity is substituted into actual hfirst. All four actual sources freshly compile with only standard three axioms.'},
 'scopes':{
  'original':'A pointwise component of the local family and same-O algebraic reply relation; neither all C.4 nor either full lower-bound theorem.',
  'reconstructed':'Official module, authored six-step lesson and publication boundary identify the exact local result and actual private consumer, keeping higher calculus/minimizer/normalizer/algorithm/TV/cost/remote/purification tasks separate.',
  'relation':'same',
  'evidence':'Phase2 matched only the anonymous producer; H4-04 forward consumer is newly inspected only in authorized Phase3. Frozen source claims remain unchanged. Owned STATIC reader is source-review-only; runtime/pixels/deployed canonical delivery are explicitly not accepted here.'},
 'constant_dependencies':{
  'original':'Local d≥2,κ≥2, coefficient 1/2, reference condition-number 2; main-theorem δ-dependent thresholds and all query/accuracy constants are outside this component.',
  'reconstructed':'Exactly these parameters/constants. No extra regularity, tolerance, nonzero scalar or hidden bound appears in reflected types.',
  'relation':'same',
  'evidence':'Private consumer uses only the forward conjunct of the actual affine provider. That existing provider internally also proves reverse conversion with κ−1≠0, but this is not a new consumer premise or selected inverse-reply obligation. Reference 2 is not a call count.'}
}
dump('independent_source_semantic_verdict.json',{
 'schema_version':1,'reviewer':'/root/source_reader_4e8f6a',
 'independent_from_formalizer':True,'independent_from_decoder':True,
 'checked_candidate_commit':HEAD,'publication_binding_sha256':PUB,
 'semantic_slots':semantic_slots,
 'verdict':'equivalent-after-elaboration',
 'verdict_scope':'Selected local producer and actual same-O forward private consumer; actual whole modules, necessary ancestors/standard meanings, fresh Lean/kernel/application checks and owned STATIC reader.',
 'deltas':[
  {'kind':'explicit-elaboration','blocking':False,'detail':'Zero-based finite indices, Euclidean coordinate wrappers and genuine Frechet/Riesz derivative witness make source meaning explicit without adding premises.'},
  {'kind':'scope-limitation','blocking':False,'detail':'The local family instance does not cover arbitrary admissible A or all d≥1,κ≥1 of §2. No whole C.4/main theorem/query-complexity completion is claimed.'}
 ],
 'repairs':[],
 'source_scope_claims':['P2-04','P2-05 algebraic response component','H4-02','H4-04 forward pointwise composition','C4-02 ordinary derivative context; not entire C∞/Hessian claim'],
 'supporting_proof_component':'H4-16/C4-01 actual admissibility provides symmetry internally; this review awards no new admissibility completion.',
 'source_review_supports_acceptance_in_this_scope':True,
 'canonical_audit_modified':False,'normal_VERIFIED_API_run':False,
 'runtime_pixel_site_acceptance':False,
 'reader_runtime_boundary':'No visible browser result exists. Browser transport failures remain preserved. They are outside the originally authorized STATIC source-review acceptance and remain integration work.'
})

dump('whole_module_and_lesson_review.json',{
 'checked_candidate_commit':HEAD,
 'production_inventory':'Exactly one public theorem in the new production module; no hidden private implementation declarations or project-owned meaning-changing definitions.',
 'binder_audit':[
  {'binder':'d:Nat,κ:Real','classification':'TYPING'},
  {'binder':'hd:2≤d,hκ:2≤κ','classification':'SOURCE','note':'Local family bounds retained even where a narrower derivative argument could use fewer facts.'},
  {'binder':'O:full real orthogonalGroup','classification':'SOURCE/TYPING','note':'Both determinant signs; no special-orthogonal premise.'},
  {'binder':'x:EuclideanSpace R (Fin d)','classification':'SOURCE/TYPING'}
 ],
 'excess_binders':[],
 'definition_audit':'Literal local θ,A,f,query; exact zero additive constant; standard coordinate-preserving WithLp and genuine standard gradient definitions. No off-source fallback definition is introduced.',
 'actual_proof_regions':[
  {'region':'literal θ,A,f,query/E/H','result':'Same source objects, no substituted potential or oracle.'},
  {'region':'hA,hself,hH','result':'Canonical actual admissibility produces symmetry internally. The direct ASTIS producer parent is exactly actual_precision_admissible.'},
  {'region':'hquery,hf','result':'Matrix action and Euclidean CLM coordinates coincide; actual f is rewritten only by the exact inner-product identity and ring algebra.'},
  {'region':'hraw,hlin,hgrad','result':'Frechet derivative exists from identity/CLM/inner/half calculus; symmetry identifies its Riesz functional. No total-gradient fallback closes existence.'},
  {'region':'intro x,hg,Prod.ext','result':'Actual pointwise derivative precedes hg.gradient; pair value and gradient share the same query.'},
  {'region':'private Test hforward,hfirst,simpa','result':'Same-O affine .1 and actual new theorem are applied to actual x; two canonical direct ASTIS parents, no supplied affine or derivative premise.'}
 ],
 'critical_ancestor_review':{
  'admissibility':'Read in full. Real cosine envelope gives diagonal bounds, orthogonal conjugation gives PSD differences, adding positive identity gives PosDef and Hermitian symmetry. No special determinant assumption or external proof premise.',
  'affine':'Read in full. Exact same-O diagonal affine identity is lifted to matrices and matvec. Reverse scalar nonzero is proved internally. Consumer selects .1; do not misstate this as removal of the reverse proof from the existing provider itself.'
 },
 'authored_proof_review':'All six official steps match actual proof regions and private consumer. The official boundary keeps remaining C4/global sampling/cost tasks separate. The visible formula and code are unchanged from pinned lesson/module.',
 'coverage_limit':'This is bounded source/module/lesson coverage for the selected local result, not a new Source Proof Graph, global topology review, old audit reapproval, full C4 acceptance, canonical root gate, deployed site acceptance or postmerge Exposition Seal.'
})

reader_build=json.loads((OUT/'owned_reader_build_receipt.json').read_text())
for d in reader_build['downloads']:
 assert (OUT/'reader'/d['download']).read_bytes()==(ROOT/d['source_file']).read_bytes()
dump('static_reader_review.json',{
 'entry':'reader/index.html','checked_candidate_commit':HEAD,
 'scope':'Owned STATIC source-review artifact made by official declaration_lessons.render_unit and actual inline_lean extraction, with scoped source inventory only.',
 'checks':{
  'all_17_details_initially_closed':True,
  'correct_single_backslash_decoded_formula_and_delimiters':True,
  'complete_source_assumptions_and_boundaries_in_folds':True,
  'exact_statement_adjacent_to_claim':True,
  'exact_complete_declaration_adjacent_to_mathematical_proof':True,
  'imports_and_namespace_available_in_full_module_link':True,
  'all_4_full_module_downloads_byte_identical_to_pinned_sources':True,
  'source_review_only_label_and_no_current_rootGate_or_deployment_claim':True
 },
 'encoding_concern_resolution':'Earlier apparent double escaping was the JSON/repr display layer. Independently checked numeric codepoints and HTML text show one literal slash and no adjacent doubled slash in any of 61 lesson strings. No lesson/renderer correction is required or made.',
 'runtime_transport_history':[
  'Sandbox localhost bind failed; escalated same command awaited a result then root interrupted. No successful OS approval or server execution receipt.',
  'iab unavailable; Chrome file URL explicitly blocked by browser policy. No workaround was attempted.',
  'Root clarified this phase requires owned STATIC source review; actual desktop/mobile/pixel/runtime acceptance remains a later integration boundary.'
 ],
 'static_scope_verdict':'passed',
 'runtime_pixel_site_verdict':'not-performed/deferred',
 'historical_hold_note':'reader_browser_block_receipt.json records the HOLD at that preview-transport boundary. It does not convert into a full current-delivery claim; final source-review scope is STATIC as originally authorized.'
})

dump('failure_and_interruption_history.json',{
 'candidate_mathematics_failures':[],
 'verification_scaffolding_failures':[
  {'attempt':'v1','failure_class':'ENV_BLOCKED','evidence':['probes/IndependentKernelApplication.v1-unavailable-extra-import.lean','logs/IndependentKernelApplication.v1-unavailable-extra-import.log','kernel_application_receipt.v1-unavailable-extra-import.json'],'actual_failure':'Unnecessary extra Mathlib.Data.Matrix.Notation import lacked an installed .olean.','correction':'Remove that extra import and express reflection with the already available Matrix.diagonal. Production/Test/ancestors unchanged.'},
  {'attempt':'v2','failure_class':'IMPLEMENTATION_FAILED','evidence':['probes/IndependentKernelApplication.v2-private-name-construction.lean','logs/IndependentKernelApplication.v2-private-name-construction.log','kernel_application_receipt.v2-private-name-construction.json'],'actual_failure':'Name.mkSimple treated the dotted private kernel name as one segment.','correction':'Construct its hierarchical name with Name.str over Name.num 0. Actual private theorem and proof unchanged.'}
 ],
 'current_actual_outcome':'All four fresh actual compilations pass. Corrected independent reflection/application probe passes exact 1/2 canonical parent assertions, standard three axioms, anonymous signature application and both determinant-sign instances.',
 'warnings':'Only reviewer anonymous-application unused-source-bound variable lint warnings appear in its successful probe; the retained bounds are source-local assumptions, not mathematical defects.',
 'preview_transport_failures':['reader_server_interruption_receipt.json','reader_browser_block_receipt.json'],
 'interruption_actor':'Root reports collaboration.interrupt_agent after no surfaced status. Raw provider aborted-by-user wording is not an explicit human stop instruction.',
 'pending_child_escalation':False,
 'source_encoding_concern':'Resolved by reader_literal_codepoint_receipt.json; it was not a candidate formula defect.',
 'failure_routing_effect':'No source claim or mathematical route retired; no candidate code changed and no unchanged Lean check rerun.'
})

dump('phase3_exposure_record.json',{
 'reviewer':'/root/source_reader_4e8f6a','ambient_exposure_nonzero':True,
 'phase1_and_phase2_preserved':True,
 'new_authorized_context':[
  'Official complete anti-anchored packet, immutable pins, actual declaration/module/Test identities, complete new producer/private Test, exact Admissibility/Affine ancestors, official lesson/publication.',
  'Necessary standard Mathlib/Lean definitions and reflection machinery; exact ranges/snapshots in necessary_standard_meanings.json.',
  'Current HEAD, pinned toolchain/dependency manifest and input hashes. Canonical audit/ledger bytes hashed and checked against HEAD only, not decoded as guidance.',
  'Official renderer/extraction source and static local assets; owned source-review artifact and exact source download bytes.',
  'Browser capability inventory exposed Chrome profile label Zhou. No unrelated tab contents or reader page contents were observed.',
  'Root process-only messages about later lifecycle preparation, interruption cause, unchanged pins and literal codepoint evidence were visible. Codepoints were independently checked; mathematical verdict formed from frozen source/actual code, not desired acceptance.'
 ],
 'phase3_read_scope':'All selected actual producer/Test/critical ancestors read in full; necessary standard definitions read by bounded line ranges; original frozen source clauses revisited. No expansion to unfinished C4/full mains or old-source-audit debts.',
 'browser_policy':'Explicit file-protocol rejection preserved. No workaround or further child escalation pending.',
 'writes':'Evidence, independent overlay .oleans, probes, static preview and reports under own phase3 directory. No canonical mathematical source, audit, ledger, frontier, model, README or remote mutation.',
 'automatic_interpreter_note':'Python imports of official local renderer modules may use ordinary interpreter caches; no such cache is treated as mathematical or publication state.',
 'not_claimed':['Global zero exposure','Independent re-audit of original private decoder files','Normal VERIFIED transition','Canonical accepted audit','Current rootGate/full-site/Chrome acceptance','Browser screenshot/pixel/runtime/mobile acceptance','Full C4/main-theorem/cost/TV completion']
})

bindings={
 'checked_candidate_commit':HEAD,'publication_binding_sha256':PUB,
 'source_original_raw_sha256':'6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d045d6ad1c7baa4a113c37915',
 'source_original_raw_sha256_actual':H(source.read_bytes()),
 'source_original_bytes':951991,
 'statement_sha256':packet['lean']['statement_sha256'],
 'producer_module_sha256':pins['exact_inputs'][packet['lean']['file']],
 'test_module_sha256':pins['exact_inputs']['Tests/GaussianComplexityFixedSpectrumFirstOrder.lean'],
 'anonymous_packet_sha256':packet['blind_reconstruction']['decoder_packet_sha256'],
 'blind_reconstruction_text_sha256':packet['blind_reconstruction']['text_sha256'],
 'blind_decoder_run_sha256':packet['blind_reconstruction']['decoder_run_sha256'],
 'phase1_manifest_sha256':H((BASE/'phase1/freeze_manifest.json').read_bytes()),
 'phase2_manifest_sha256':H((BASE/'phase2/freeze_manifest.json').read_bytes()),
 'full_reviewer_packet_raw_sha256':H((OUT/'inputs/full-anti-anchored-reviewer-packet.json').read_bytes()),
 'full_reviewer_packet_canonical_sha256':packet['packet_sha256']
}
# Keep a single unambiguous exact original-source digest.
bindings['source_original_raw_sha256']=bindings.pop('source_original_raw_sha256_actual')
dump('review_run.json',{
 'schema_version':1,'reviewer':'/root/source_reader_4e8f6a',
 'formalizer':packet['roles']['formalizer'],'blind_decoder':packet['roles']['blind_decoder'],
 'independent_from_formalizer':True,'independent_from_decoder':True,
 'completed_utc':datetime.now(timezone.utc).isoformat(),
 'bindings':bindings,
 'verdict':'equivalent-after-elaboration',
 'review_result':'Completed selected-scope independent source/module/fresh-Lean/owned-STATIC-reader review; supports source fidelity for the local producer and actual private same-O forward consumer.',
 'review_evidence':['independent_source_semantic_verdict.json','whole_module_and_lesson_review.json','fresh_compile_receipt.json','kernel_application_receipt.json','logs/IndependentKernelApplication.log','focused_fake_closure_receipt.json','static_reader_review.json','reader_literal_codepoint_receipt.json','failure_and_interruption_history.json','phase3_exposure_record.json'],
 'runtime_pixel_site_acceptance':False,'normal_VERIFIED_API_run':False,'canonical_audit_modified':False,
 'successor_audit_rule':'Any later accepted canonical audit must be a separately authorized successor artifact after this review, never a retroactive mutation of checked candidate HEAD/audit bytes.'
})

(OUT/'final_capsule.md').write_text("""# Independent Phase 3 capsule

Checked immutable candidate: 9d306d837fbddf1518b0035494baaf5c21c24488.
Publication binding: 51d5a5e9390a0d66c2d5b72d042a042eec8d3d60433043ea3909bf9320ccb31e.

Independent mathematical/source verdict: equivalent-after-elaboration for the
selected local fixed-spectrum first-order producer and actual same-O forward
private consumer. No excess convenience premise, changed potential, inverse
covariance/hidden-rotation oracle substitution or determinant-sign restriction
was found. Actual Frechet derivative existence precedes total-gradient use.
The frozen source was revisited; the author packet was checked, not accepted as
its own source certificate. The seven slots are in the verdict JSON.

All four actual pinned sources were freshly compiled into an owned Lean
overlay. The independent kernel/reflection/application probe passed exact
direct ASTIS parents: producer 1 (actual admissibility), private Test 2 (new
producer and actual affine provider). Both and critical ancestors use only
propext, Classical.choice and Quot.sound. The exact anonymous statement
application and full-O determinant +1 and −1 instances pass. Focused
comment/string-stripped fake-closure checks pass.

The producer is an instance of §2 Eq. (1) using §4.1 Eq. (11). The private
consumer composes its proved result with Remark 4.2's matched-O forward
precision identity. It consumes the affine provider's first conjunct; the
existing provider also proves its reverse direction internally, with no
reciprocal/nonzero premise added to the selected consumer. No adaptive
simulation, cap/expected-cost, Gaussian/TV, whole-C4, main-bound or remote
completion follows.

The owned STATIC reader uses the official lesson and exact code extraction:
17 details default closed; statement/proof adjacent and exact; assumptions,
remaining boundary and full imports/namespace source available; 4 module
downloads byte-identical. Independent literal codepoints resolve the apparent
TeX escaping concern: commands/delimiters have one slash, with no doubled slash
in any decoded lesson string. No encoding correction was made or is proposed.

Two reviewer-scaffolding failures are preserved: unavailable unnecessary
Matrix.Notation olean (removed in favor of a diagonal reflection) and a private
Name.mkSimple construction error (corrected to a hierarchical numeric name).
Neither changed producer mathematics. The final actual probe passes; lint-only
unused source bounds remain visible.

Preview transport attempts are also preserved: sandbox localhost bind failure,
same-command escalation awaiting a result then root interruption, unavailable
iab and explicit browser file-protocol rejection. No workaround followed.
Root caused the interruption; raw provider wording is not a human stop request.
There is no pending child escalation. Browser runtime/pixels/mobile and current
canonical site/rootGate/Chrome acceptance were not performed or claimed, and
belong to later integration. The source-review stage is STATIC as authorized.

Phase 1 and Phase 2 originals remain unchanged. HEAD, canonical audit and both
ledgers remain byte-pinned. No normal VERIFIED API or canonical audit copy was
run. Any accepted canonical audit must be a separately authorized successor;
the checked 9d306d candidate cannot be retroactively rewritten.
""")

dump('final_pin_receipt.json',{
 'checked_utc':datetime.now(timezone.utc).isoformat(),
 'HEAD':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
 'all_9_exact_inputs_still_match_pins':True,
 'phase1_and_phase2_manifest_hashes_unchanged':True,
 'original_source_hash_rechecked':H(source.read_bytes()),
 'no_unchanged_Lean_checks_rerun':True,
 'all_4_owned_downloads_still_equal_current_pinned_input_bytes':True,
 'fresh_compile_success':True,'kernel_reflection_application_success':True,
 'static_reader_success':True,'runtime_pixel_site_acceptance':False,
 'canonical_audit_modified':False,'normal_VERIFIED_API_run':False
})
artifacts=[]
for p in sorted(OUT.rglob('*')):
 if p.is_file() and p.relative_to(OUT).as_posix() not in {'freeze_manifest.json','freeze_manifest.sha256'}:
  b=p.read_bytes();artifacts.append({'path':p.relative_to(OUT).as_posix(),'bytes':len(b),'sha256':H(b)})
dump('freeze_manifest.json',{
 'schema':'phase3-independent-full-context-review-freeze-v1',
 'phase':'PHASE3_SOURCE_MODULE_FRESH_LEAN_OWNED_STATIC_READER',
 'reviewer':'/root/source_reader_4e8f6a',
 'status':'FROZEN_SELECTED_SCOPE_REVIEW_COMPLETE',
 'frozen_utc':datetime.now(timezone.utc).isoformat(),
 'bindings':bindings,
 'independent_source_verdict':'equivalent-after-elaboration',
 'acceptance_scope':'Selected local producer + actual same-O forward private Test; source/module/fresh Lean/kernel/application/fake-closure/owned STATIC reader only.',
 'unaccepted_scope':['Browser runtime/pixels/desktop/mobile','Current canonical rootGate/site/Chrome delivery','Normal VERIFIED transition','Canonical accepted audit','Full C4/main theorem/algorithm/cost/TV completion'],
 'review_run':'review_run.json','review_run_sha256':H((OUT/'review_run.json').read_bytes()),
 'semantic_verdict':'independent_source_semantic_verdict.json',
 'capsule':'final_capsule.md','artifacts':artifacts
})
b=(OUT/'freeze_manifest.json').read_bytes()
(OUT/'freeze_manifest.sha256').write_text(H(b)+'  freeze_manifest.json\n')
print(json.dumps({'phase3_status':'FROZEN_SELECTED_SCOPE_REVIEW_COMPLETE','verdict':'equivalent-after-elaboration',
 'freeze_manifest_sha256':H(b),'review_run_sha256':H((OUT/'review_run.json').read_bytes()),
 'artifact_count':len(artifacts),'runtime_or_site_acceptance':False,'normal_VERIFIED_API_run':False},indent=2))
