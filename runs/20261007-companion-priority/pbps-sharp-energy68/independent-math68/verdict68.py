import json,sys,os,re,subprocess,traceback
from pathlib import Path
import final68 as F
import review68 as R
O=R.O;P=R.P;ROOT=R.ROOT;pin=R.pin;sha=R.sha;save=R.save;get=R.get;read=R.read;now=R.now

def verdict():
 F.stable()
 for q in ['exact-axioms.audit.json','fake-closure-import.audit.json','statement-caller-parent.audit.json']:
  assert get(q)['status']=='PASS'
 formula=get('formula-BODY.audit.json');assert formula['original_strict_RAW_matches']==9 and formula['exact_terminal_empty_LF_maps']==2
 overlay=get('presentation-overlay.decision.json') if (O/'presentation-overlay.decision.json').exists() else None
 v=dict(schema_version=1,status='MATHEMATICS_ACCEPTED_WITH_EXPLICIT_PRESENTATION_RESOLUTIONS',actor=R.ACTOR,actual_review_PID=os.getpid(),utc=now(),advance_id='ASTIS-SA-20261009-PBPSSharpCorrectorEnergy',checked_base_commit=R.BASE,checked_SCI68_commit=None,candidates_uncommitted=True,
  exact_modules=[pin(R.LEAF),pin(F.MAIN),pin(F.TEST)],final_original_input_rows=get('final.inputs.manifest.json')['input_count'],stage1_original_input_rows=get('leaf.inputs.manifest.json')['input_count'],auxiliary_input_rows=get('audit.inputs.manifest.json')['input_count'],
  accepted_delta=[
   'One generic complete-real-Hilbert quadratic estimate from bounded selfadjoint K,D, I+K²=D², c≥0 and ||D||≤c, valid for zero H and c=0, with exact c/2 times the SUM of squared component norms.',
   'One original-input production theorem uses the SAME actual67 witnesses and centered HP0, rederives K=A0 Inv selfadjoint and I+K²=Inv² internally, then proves the pair bound1/(2γ) and the actual globally centered f norm-budget corrector bound.',
   'One genuine original-input Test calls that production theorem and proves for EVERY real0<omegaWeight≤γ the half/three-halves modified-energy inequalities and both quantitative perturbation bounds, retaining the same fP and all preceding witnesses.'],
  substantive_mathematical_audit=dict(
   generic=get('shared-leaf.mathematical-review.json')['proof_audit'],
   actual=[
    'The public original caller remains finite-dimensional real Hilbert/Borel E, C² V, positive α≤β, both global Hessian bounds, positive η and βη≤1. The literal private Prop contains every probability/range/kernel/root/inverse fact as a CONCLUSION, and public theorem adds no provider or binder.',
    'The single actual67 parent invocation is at exactly the original parameters. Bounded conjunction projections and12 atomic existential eliminations select S,e,U,T,Γ,q,ΓP0,Inv,A0,B0,V0,R from this SAME invocation. Reconstruction returns those witnesses; no independent choices of Gamma/inverse/polar/global geometry are substituted.',
    'HP0 is exactly ker(innerSL qP) in the macroscopic HP, with inherited complete Hilbert structure; Hperp is exactly ker P in joint real L². The complete structures are internally available from closed kernels. L² is never assumed finite-dimensional and neither centered space is assumed nonzero.',
    'IsSelfAdjoint.commute_iff supplies selfadjoint A0 Inv from same selfadjoint A0,Inv and their inherited commutation. The coefficient proof uses ΓP0 Inv=I twice, rearranges A0 Inv A0 Inv by the inherited A0/Inv commutation, multiplies A0²+ΓP0²=I by Inv², and derives I+(A0 Inv)²=Inv². No commutation/gap/CFC premise is added.',
    'Apply the generic leaf on EXACT HP0 with K=A0 Inv,D=Inv,c=1/γ. Inherited positivity γ>0 and ||Inv||≤1/γ discharge all leaf hypotheses. field_simp gives exact coefficient1/(2γ); no strict endpoint, c≥1 or vector-nontriviality argument occurs.',
    'For each actual globally centered joint f, select the SAME fP given by inherited hGlobal f hf. Retain fperp=Rf and fV=V0.adjoint fperp. Squaring ||fV||≤||fperp|| is justified by nonnegative norms; combine with actual Pythagoras to prove ||fP||²+||fV||²≤||f||². Divide by positive2γ and compose the pair bound.',
    'The explicitly typed hFinal is a local proof of the exact required global tail, not a new theorem/provider/assumption. The outer witnesses are reconstructed only after that proof. Every ambient/intrinsic adjoint and conditional centering identity is preserved.'],
   genuine_Test=[
    'Test imports production only, invokes actual_sharp_corrector_bound at unchanged original potential/step assumptions, and keeps the same chosen parent objects and actual fP. The modified-energy conclusion is not a supplied premise.',
    'For arbitrary0<omegaWeight≤γ define L=||f||²+omegaWeight C(fP,fV). Algebra gives L−||f||²=omegaWeight C. Absolute value and positive weight multiply the internally derived actual corrector bound; ring yields exact omegaWeight/(2γ) factor.',
    'Since2γ>0, division preserves omegaWeight/(2γ)≤1/2. Multiplication by nonnegative ||f||² gives the second perturbation inequality. Both sides of abs_le then give1/2||f||²≤L≤3/2||f||².',
    'The weight is universally quantified INSIDE the concluded globally centered implication, after the fixed original PBPS witnesses. It does not restrict the potential, change gamma, or become a new public provider. The global mean-zero observable condition is an honest quantified consumer domain.'],
   edge_cases=dict(rank_zero_E='Legal original caller and inherited parent; no vector selection or Nontrivial hypothesis.',alpha_eta_one='Legal βη≤1 endpoint; γ=1, no division by1−αη, strict cap or gamma<1.',zero_H_and_c_zero='Generic proof uses nonnegative squares only; no division byc or norm.'),
   same_object_inventory=['μ,J,ν and the exact reflected law/kernel','P=conditional expectation given Y and onto e','U,T,Γ and transported ΓP','HP0,qP,ΓP0,Inv,A0 and coefficient K','Hperp=kerP,B0,V0,R','same actual f,fP,Rf,V0.adjoint(Rf)'],
   no_new_premises=['probability','range/onto e','root/CFC','spectral gap/order','unit/inverse','commutation/selfadjoint coefficient','finite-dimensional L²','Nontrivial','onto Hperp/coisometry','energy/norm-budget certificate']),
  library_and_provider_audit=get('fake-closure-import.audit.json'),caller_seal_parent_audit=get('statement-caller-parent.audit.json'),axiom_audit=get('exact-axioms.audit.json'),formula_BODY_audit=formula,
  independent_fresh_compilers={q:get(f'{q}.compiler.result.json') for q in ['leaf','main','test']},
  root_focused_evidence=dict(receipt=pin(P/'focused-build68-v1/receipt.json'),stdout=pin(P/'focused-build68-v1/stdout.log'),reported_jobs=3950,classification='Root focused compiler supports final producer bytes; own fresh Lean source compilers are separately retained, not cache replay.'),
  retained_negative_evidence=dict(leaf_API_failures=get('shared-leaf.mathematical-review.json')['retained_typed_API_negatives'],root_route_records=[pin(P/'compiler-diagnosis68'/x) for x in ['parent-projection-route.json','atomic-existential-route.json','atomic-global-route.json','local-global-proof-route.json','redundant-ring-repair.json','diagnostics-removed.json','test-atomic-route.json','test-local-global-proof-route.json']],root_failed_stopped_recovery_sorryAx_not_proof=True,own_original_region_audit_failure=dict(receipt=pin(O/'audit-v1.terminal.json'),diagnosis=pin(O/'audit-v1.failure.json'),class_='LITERAL_SOURCE_REGION_METADATA_OFF_BY_ONE_EMPTY_LINE',not_math_failure=True),observer_reporting_and_renderer_corrections=get('statement-caller-parent.audit.json')['observer_corrections']),
  presentation_findings=dict(original_step2_text='use both inverse identities',BODY_uses='hRight twice, no hLeft call in coefficient proof',original_region_defects=[q for q in formula['steps'] if not q['literal_BODY_match']],independently_reviewed_proposed_overlay=overlay,canonical_overlay_applied_during_review=False,full_reader_Exposition_Seal=False,private_full_Prop_renderer_placement='Separate repository/reader admission; prose explanation field is not itself Lean code.'),
  mathematical_blockers=[],mathematical_repairs_required=[],source_review_or_decoder_verdicts_consumed=False,whole_module_anti_anchored_source_review_completed_by_this_actor=False,
  remaining_truth_boundary=['B21 rotation','weak H1/B2','B4 event dynamics','hypocoercivity/main theorem','invariance/nonexplosion','numerical errors and caps','expected query costs','actual-input composition','aggregate repository/reader/remote CI/main/live admission','full Exposition Seal and PURIFIED','whole paper and Goal completion'],
  canonical_Lean_Git_ledger_writes=False,VERIFIED=False,PURIFIED=False,full_Exposition=False,whole_paper_complete=False,Goal_complete=False)
 save('mathematical-review.json',v);print(json.dumps(dict(status=v['status'],actual_PID=os.getpid(),mathematical_blockers=0,private_Props=2,uncommitted_candidates=True,proposed_overlay_decision=overlay['decision'] if overlay else 'PENDING')))
if __name__=='__main__':
 try:verdict()
 except Exception as e:
  if not (O/'lease.final.json').exists():save((sys.argv[2] if len(sys.argv)>2 else 'verdict')+'.failure.json',dict(actual_PID=os.getpid(),utc=now(),error=repr(e),traceback=traceback.format_exc()))
  raise
