from source71 import *
from collections import Counter

def expectations():
 stable(); raw=PRIMARY.read_bytes(); graph=read(PRI/'source-proof-graph.json'); inventory=get('source.math.inventory.json'); nodes={x['id']:x for x in graph['nodes']}; byid={x['id']:x for x in inventory['items']}
 # Supplement only necessary exact source anchors outside the four stored regions.
 supplements=[]
 for nid in ['P0','P1','P2','P3','P5','P6','P7','P8']:
  for q in nodes[nid]['primary_math']:
   if q['id'] in byid or any(x['id']==q['id'] for x in supplements):continue
   a,b=q['source_RAW_range_end_exclusive']; part=raw[a:b]; assert len(part)==q['RAW_bytes'] and sha(part)==q['RAW_sha256']
   rp=O/('source/anchor-'+q['id']+'.RAW.html');rp.write_bytes(part);lp=rp.with_name(rp.name.replace('.RAW.','.LF.'));lp.write_bytes(part.replace(b'\r\n',b'\n'))
   row=dict(q,RAW=pin(rp),LF=pin(lp),source_node=nid);supplements.append(row)
 save('source.supplemental-anchors.json',dict(count=len(supplements),items=supplements,authority='Exact fixed-primary substrings at independently frozen graph offsets; not reconstructed HTML or Lean proof.'))
 for row in inventory['items']:
  a,b=row['start_byte'],row['end_byte_exclusive'];assert sha(raw[a:b])==row['RAW_sha256']
 # Every selected math element has a finite role; contextual inventory is not theorem coverage.
 assumptions={'S1.p1.m1','S1.p1.m2','S1.p1.m3','S1.p1.m4','S1.E1.m1'}
 coverage=[]
 for q in inventory['items']:
  n=q['id'];region=q['region']
  if region=='global-assumptions': role='original-analytic-hypotheses' if n in assumptions else 'introductory-context-excluded-from-B21-target';reason='Only original potential, space, C2 and Hessian assumptions bind B21; surrounding motivation/comparison is not a new premise.'
  elif region=='real-L2-spectral-conventions-D1':role='real-Hilbert-AE-adjoint-spectral-conventions';reason='Convention and background definition support; no independent proof or full Appendix D credit.'
  elif region=='corrector-change-B4-consumer-proof':role='downstream-B4-consumer-and-explicit-residual';reason='B27/B28 consume the same B21; B17 error/Young/Lyapunov steps remain separate and are not supplied by B21.'
  elif n.startswith(('A2.SS3.p1.','A2.SS3.p3.','A2.Ex6.','A2.Ex8.')):role='actual-components-centered-domain';reason='Actual Pf, Pperp f and V*Pperp f; contraction does not imply onto V.'
  elif n.startswith(('A2.SS3.p2.','A2.Ex7.','A2.E18.')):role='downstream-actual-chain-microscopic-decrement';reason='rho/H/K contraction applies downstream; not a caller or proof ingredient of ideal B21.'
  elif n.startswith(('A2.SS3.p4.','A2.E19.','A2.E20.')):role='B19-B20-same-corrector-definition';reason='Minus sign, factor one-half and centered inverse only; omega belongs to Lyapunov definition, not B21.'
  elif n.startswith(('A2.SS3.p5.','A2.Ex9.','A2.Ex10.','A2.Ex11.','A2.Ex12.','A2.Ex13.','A2.Ex14.','A2.Ex15.','A2.Ex16.','A2.Ex17.','A2.E21.')):role='P13-P17-actual-ideal-rotation-corrector-change';reason='Actual g/projections precede RHS rotation; final omega/rho motivation in this paragraph is a downstream application, not an extra B21 assumption.'
  elif n.startswith('A2.Ex18.'):role='downstream-ideal-coercivity-motivation';reason='Uses B21 plus 0<omega<rho; not part of B21 statement.'
  elif n.startswith(('A2.SS3.p6.','A2.SS3.p7.','A2.Thmtheorem3.','A2.Ex19.','A2.Ex20.','A2.Ex21.','A2.Ex22.','A2.E22.','A2.E23.','A2.E24.')):role='independent-B23-sharp-bound-and-B3-norm-equivalence';reason='Shared corrector and centered operators, but not a dependency needed for the exact B21 difference identity.'
  elif n.startswith(('A2.Thmtheorem4.','A2.E25.','A2.E26.')):role='B4-statement-consumer-and-stronger-small-step-context';reason='B4-specific universal constants, rho/Lambda/omega/small c0; no promotion into B21 callers.'
  else:role='section-real-L2-context';reason='Section notation only, not a new statement premise or completed proof.'
  coverage.append(dict(id=n,RAW_sha256=q['RAW_sha256'],role=role,reason=reason))
 save('source.coverage.json',dict(selected_math_count=len(coverage),supplemental_math_count=len(supplements),selected_roles=dict(Counter(x['role'] for x in coverage)),items=coverage,finite_scope='Four exact regions plus explicitly listed necessary anchors; not all344 previous primary items or whole paper.',all_selected_items_classified=True))
 formula_ids=['A2.E20.m1','A2.E19.m1','A2.Ex10.m1','A2.SS3.p5.m7','A2.Ex11.m1','A2.Ex12.m1','A2.Ex16.m1','A2.Ex17.m1','A2.E21.m1','A2.E23.m1','A2.E22.m1','A2.Ex27.m1','A2.E27.m1','A2.Ex36.m1','A2.E28.m1','A2.E25.m1','A2.E31X.m2','A2.E26.m1']
 save('source.formulas.exact.json',dict(count=len(formula_ids),formulas=[byid[n] for n in formula_ids],formula_text_is='Decoded original HTML alttext; exact RAW span hash/offset is authoritative.',source_B21_link_offset=926328,source_B21_link_RAW_context=raw[926220:926450].decode()))
 e=dict(schema='independent-source-first71-expectations-v1',actor=ACTOR,actual_PID=os.getpid(),utc=now(),status='SOURCE_EXPECTATIONS_SEALED_BEFORE_CURRENT70_INTERFACE_READ',visibility=get('visibility-declaration.json'),source_id='arXiv:2609.06905v1',primary=pin(PRIMARY),source_graph=dict(pin(PRI/'source-proof-graph.json'),nodes=22,edges=49,edge_contract='Source proof-ingredient graph, not certified Lean dependency.'),
 original_callers=dict(analytic=['V in C2(R^d)','0<alpha<=beta','for every x: alpha I<=Hess V(x)<=beta I','eta>0 and beta eta<=1'],representation='Finite-dimensional real Euclidean input with Borel space in original Lean caller; real joint L2 itself may be infinite dimensional. No nonzero-rank/nontrivial hypothesis.',actual_input='mu proportional exp(-V); SAME pi_eta joint density proportional exp(-V(x)-||x-y||^2/(2eta)); actual reflection F(x,y)=(x,2x-y), Uf=f composed with F.',no_extra=['rho','omega','small c0','H/halfturn error bounds','mean_g assumption','onto V','gap/inverse/commutation premises','68 sharp-bound premise','full L2 finite-dimensionality']),
 typed_objects=dict(H='real L2(pi_eta), AE equivalence classes',HP='range P',HP0='macro range intersect mean-zero, exact subtype',A0='SAME compression U_PP restricted to HP0',Gamma0='SAME canonical nonnegative sqrt(I-U_PP^2) restricted to HP0',Inv='SAME bounded two-sided Gamma0 inverse on HP0 only; no inverse across constants',V='SAME isometry HP0 -> ker P, with V* : ker P -> HP0; no onto-V assertion'),
 definitions=dict(corrector='C(u,v)=(1/2)*(||u||^2-||v||^2)-<A0(Inv u),v>',components='fP=Pf in HP0; fperp=(I-P)f in kerP; fV=V* fperp; ||fV||<=||fperp||',actual_rotation_input='g=U(P-(I-P))f for original globally centered f; derive mean g=0 internally',actual_output_components='gP=Pg and gV=V*((I-P)g), typed into HP0; do not define components as rotation RHS',rotation='gP=A0 fP-Gamma0 fV; gV=Gamma0 fP+A0 fV',energy_pair='||gP||^2+||gV||^2=||fP||^2+||fV||^2; sum norm, not product max norm'),
 delta=dict(P15='B20 defines this corrector with minus sign and exact coefficient 1/2.',P16='Coefficient computation: C(A0u-Gamma0v,Gamma0u+A0v)-C(u,v)=-||u||^2+||v||^2.',P16_generalization='All-pairs HP0 formulation is the explicit source-graph mathematical abstraction of the displayed actual pair; not a separately printed theorem.',P16_ingredients=['selfadjoint A0 and Gamma0','A0 Gamma0=Gamma0 A0','A0^2+Gamma0^2=I on SAME HP0','SAME two-sided Inv and A0 Inv=Inv A0'],P17='B21 actual delta: C(gP,gV)-C(fP,fV)=-||fP||^2+||fV||^2 for every original centered f.',source_support=['A2.E20.m1','A2.Ex10.m1','A2.Ex11.m1','A2.Ex12.m1','A2.Ex16.m1','A2.Ex17.m1','A2.E21.m1'],endpoint='rank0 and alpha eta=1 remain legal; algebra does not require logarithm, rho or strict alpha eta<1.'),
 dependencies=dict(accepted_source_ingredients='Same-root/inverse/commutation and full kerP intertwining produce actual rotation; no replacement existential witnesses.',prospective70='Actual pair rotation is required for P17; current70 header may match it only prospectively, never as proved/VERIFIED truth.',independent68='B23 sharp |C| <= (1/(2gamma))*(||fP||^2+||fV||^2) and B22/B24 norm equivalence for 0<omega<=gamma share SAME definition but are NOT needed for exact B21.',same_witness_rule='All P/U/Gamma/A0/Inv/V/fP/fV/gP/gV in B20/P16/P17 must be the single actual inherited tuple. Do not combine independent existential tuples from68 and70 without equality transport; preferably define C from the70 tuple and invoke generic algebra on it.'),
 B4_consumer=dict(context='0<rho<=1/2; universal c_hyp,c0,c>0; beta eta<=c0, proof chooses c0<=1/16. Lambda=log(1/gamma)+(rho/gamma)^2; omega=c_hyp*rho/Lambda. These are B4-specific.',comparator='SAME g=Kid f and actual Kf; r_rho=V*[I+(1-rho)Hperpperp]fperp=rho fV+(1-rho)r; r=V*(I+Hperpperp)fperp.',B27='(Kf)P=gP+Gamma0 r_rho; (Kf)V=gV-A0 r_rho.',perturbation='C((Kf)P,(Kf)V)-C(gP,gV)=<gP,Inv r_rho>+(1/2)||r_rho||^2.',B28='Delta C_actual=-||fP||^2+||fV||^2+<gP,Inv r_rho>+(1/2)||r_rho||^2.',B21_contribution='Exactly the first two signed terms in B28; explicit source link at RAW offset926328.',remaining=['B17 halfturn estimate, Appendix C2/C3 outside this selection','B29/B30 error bounds and Young inequality -> B31','B18 microscopic decrement plus B31 and chosen omega -> Lyapunov decrement','B3/B22 upper norm comparison after omega<=gamma -> B26'],no_completion='No B4/full convergence/cost/composition result supplied by B21.'),
 minimum_next_single_SAU=dict(proposal_only=True,claim=False,target='Actual original-input SAME-witness B20 definition plus B21 ideal corrector-change.',genuine_new_math='P16 coefficient cancellation on the original70 rotation tuple, then P17 actual substitution. No wrapper assuming B21 or supplied range/rotation premise in public caller.',prerequisite='Accept/verify actual70 independently before calling it a Lean parent; otherwise keep this edge planned.',scope_preservation='Retain original6 analytic caller binders, SAME12 witnesses and inherited original conclusions; append corrector definition and exact actual B21. Generic coefficient leaf may be useful but is not actual consumer completion.'),
 boundaries=dict(source_blind=False,anti_anchored_final_source_review=False,Lean_proof=False,SAU_claim=False,VERIFIED=False,whole_paper=False,PURIFIED=False,Goal=False,no70BODY_read=True,no69_native_package_copy=True),coverage=pin(O/'source.coverage.json'),formulas=pin(O/'source.formulas.exact.json'))
 save('source.expectations.json',e)
 save('source-first.seal.json',dict(actor=ACTOR,utc=now(),actual_PID=os.getpid(),expectations=pin(O/'source.expectations.json'),formulas=pin(O/'source.formulas.exact.json'),coverage=pin(O/'source.coverage.json'),inputs=pin(O/'inputs.manifest.json'),current70_interface_not_read=True,prior70_visibility_disclosed=True))
 print(json.dumps(dict(status=e['status'],actual_PID=os.getpid(),selected_math=255,supplemental_math=len(supplements),expectations_RAW=pin(O/'source.expectations.json')['raw_sha256'])))

def interface():
 stable();seal=get('source-first.seal.json');checkpin(seal['expectations']);checkpin(seal['formulas']);checkpin(seal['coverage']);assert get('expectations.terminal.json')['exit_code']==0
 pre=ROOT/'runs/20261007-companion-priority/pbps-actual-projected-rotation-preproof70';paths=[pre/'root.statement-seal70.json',pre/'header0-proposed-expanded.lean'];rows=[]
 for i,p in enumerate(paths):
  q=dict(original=pin(p),read_after_source_first_seal=True)
  for kind,b in [('RAW',p.read_bytes()),('LF',p.read_bytes().replace(b'\r\n',b'\n'))]:
   dest=O/f'inputs/interface-{i}.{kind}.snapshot';dest.write_bytes(b);q[kind+'_snapshot']=pin(dest)
  rows.append(q)
 save('interface.inputs.manifest.json',dict(input_count=2,inputs=rows,LF_recipe=get('inputs.manifest.json')['LF_recipe'],authority='Current sealed expanded70 header and seal ONLY; no70 BODY or whole70 review package.',no_proof_credit=True))
 rs=read(paths[0]);t=paths[1].read_text(encoding='utf-8');assert pin(paths[1])['raw_sha256']=='9261f488432664370ae1b1146b098bf86c17dfd476bfe2e149d3024a77529e19'==rs['statement_seal']['RAW_sha256'];assert not rs['proved'] and not rs['VERIFIED'];assert ':= by' not in t and 'sorry' not in t and 'axiom' not in t
 outer=re.findall(r'∃ (S|e|U|T|Γ|q|ΓP0|Inv|A0|B0|V0|R)\s*:',t);assert outer==['S','e','U','T','Γ','q','ΓP0','Inv','A0','B0','V0','R']
 callers=re.findall(r'\((hα|hαβ|hV|hH|hη|hβη)\s*:',t);assert callers==['hα','hαβ','hV','hH','hη','hβη']
 checks=[
 ('original analytic callers', '(hβη : (β : ℝ)*η ≤ 1)', 'Original six analytic binders; no rho/omega/mean_g/onto/corrector-change caller.'),
 ('same actual U', '(∀ g : Lp ℝ 2 J, (U g : E × E → ℝ) =ᵐ[J] g ∘ F)', 'AE pullback with SAME actual reflection; not free U unrelated to joint law.'),
 ('centered inverse left', 'Inv*ΓP0=(1 : HP0 →L[ℝ] HP0)', 'Inverse only exact HP0.'),
 ('centered inverse right', 'ΓP0*Inv=(1 : HP0 →L[ℝ] HP0)', 'Same Inv, no separate coefficient operator.'),
 ('same inverse selfadjoint', 'IsSelfAdjoint Inv', 'Inherited conclusion, not caller.'),
 ('same A0-Gamma0 square', 'A0*A0+ΓP0*ΓP0=(1 : HP0 →L[ℝ] HP0)', 'Coefficient algebra ingredient on exact same domain.'),
 ('same A0-Inv commute', 'Commute A0 Inv', 'Inherited coefficient algebra ingredient, not new premise.'),
 ('same fullker intertwining', 'V0.adjoint ∘L D = -(A0 ∘L V0.adjoint)', 'Full Hperp identity; no onto V required.'),
 ('original global f', '(∀ f : Lp ℝ 2 J, (∫ z, f z ∂J)=0 →', 'Source centered f quantified; no supplied range-V or mean-g premise.'),
 ('actual fP conditional', 'HP0.subtypeL fP=condExpL2 ℝ ℝ (μ:=J) measurable_snd.comap_le f', 'fP is the actual macro projection, not an arbitrary supplied coefficient.'),
 ('actual fV', 'let fV : HP0 := V0.adjoint fperp', 'fperp=R f, SAME polar coefficient.'),
 ('actual g', 'let g : Lp ℝ 2 J := U (P f-(f-P f))', 'SAME ideal Kid input; Pperp=I-P.'),
 ('derived g mean', '(∫ z, g z ∂J)=0 ∧', 'Conclusion after actual g definition, not analytic caller.'),
 ('actual gP conditional', 'HP0.subtypeL gP=condExpL2 ℝ ℝ (μ:=J) measurable_snd.comap_le g', 'Actual Pg semantics precede rotation RHS.'),
 ('actual gperp', 'let gperp : Hperp := R g', 'Actual complement projection of g.'),
 ('actual gV', 'let gV : HP0 := V0.adjoint gperp', 'Actual adjoint component, not defined as the desired RHS.'),
 ('macro rotation', 'gP=A0 fP-ΓP0 fV', 'Matches A2.Ex12/Ex13 on the same witnesses.'),
 ('micro rotation', 'gV=ΓP0 fP+A0 fV', 'Matches A2.Ex12/Ex15 on the same witnesses.'),
 ('sum energy', '‖gP‖^2+‖gV‖^2=‖fP‖^2+‖fV‖^2', 'Sum of squares, never product max norm.')]
 results=[]
 for name,literal,meaning in checks:
  assert literal in t, name;results.append(dict(check=name,literal=literal,meaning=meaning,pass_result=True))
 assert 'mathsf' not in t and 'SharpCorrectorEnergy' not in t and '𝒞' not in t
 save('interface.match.json',dict(status='MATCHED_PROSPECTIVE70_HEADER_ONLY',actual_PID=os.getpid(),utc=now(),source_expectations_RAW_sha256=seal['expectations']['raw_sha256'],header=pin(paths[1]),seal=pin(paths[0]),outer_witness_count=12,outer_witnesses=outer,original_caller_count=6,original_callers=callers,checks=results,source_match='Header realizes P12/P13/P14 geometry prospectively; P15 definition/P16 algebra/P17 B21 remain genuine new delta.',same_witness_caution='Quantified one inherited tuple is usable only after its theorem is proved/admitted. Do not take arbitrary existential tuple from68 and a different one from70.',status_qualification='Root seal says not claimed/not proved/not VERIFIED. This review neither reads70 BODY nor assesses any later proof/status; no callable theorem credit.',header_math_check='No fresh type elaboration repeated: exact expanded-header RAW equals the previously independently typechecked header. This is source/interface comparison only.',no_70_BODY_read=True,no_69_native_reaudit=True))
 checkpin(seal['expectations']);print(json.dumps(dict(status='MATCHED_PROSPECTIVE70_HEADER_ONLY',actual_PID=os.getpid(),checks=len(results),original_callers=6,outer_witnesses=12,source_expectations_unchanged=True)))

def review():
 stable();seal=get('source-first.seal.json');checkpin(seal['expectations']);match=get('interface.match.json');assert get('interface.terminal.json')['exit_code']==0
 for q in get('interface.inputs.manifest.json')['inputs']:checkpin(q['original'])
 p=dict(schema='independent-source-first71-complete-review-v1',status='ACCEPTED_BOUNDED_SOURCE_EXTRACTION_AND_PROSPECTIVE_INTERFACE_MATCH',actor=ACTOR,actual_PID=os.getpid(),utc=now(),source_expectations=get('source.expectations.json'),source_first_seal=seal,coverage=get('source.coverage.json'),formulas=get('source.formulas.exact.json'),interface=match,input_manifest=get('inputs.manifest.json'),interface_input_manifest=get('interface.inputs.manifest.json'),supplemental_anchors=get('source.supplemental-anchors.json'),retained_negative=dict(kind='observer-runtime-dependency',receipt=get('extract.terminal.json'),failure=get('extract.failure.json'),repair='Replaced unavailable bs4 with standard-library HTMLParser in a new executed helper; no source/canonical bytes changed.',recovery=get('extract-v2.terminal.json')),decision=dict(accepted='Source B20/B21 exact definitions/signs/callers and actual B4 consumption, with prospective70 header match.',not_accepted=['No71 SAU claim, Lean proof or VERIFIED','No70 proof/VERIFIED credit','No B4 completion or B17 proof','No new68->70 or68->B21 formal dependency','No full-paper/Goal/PURIFIED result','Not source-blind or fresh anti-anchored final review'],smallest_next_delta='Actual original-input SAME-witness corrector-change B21, proving the coefficient cancellation and substituting actual70 projections after70 independent admission.',repair_required='None identified at source/header interface; same-witness proof obligation and current70 non-proved status remain explicit.'),observer_correction='Parent progress message used a temporary 2? hash placeholder; exact native expectations SHA 0f7296e9555a62b939f67409f5c89fef044870c2a0cf635461fffb5419014d6d was immediately supplied in a correction. Native source seal has always had the exact hash.',source_input_count=3,interface_input_count=2,selected_region_count=4,selected_math_count=255,supplemental_math_count=20,all_selected_items_have_finite_classification=True,primary_regions_total_RAW_bytes=218827,source_graph_node_count=22,source_graph_edge_count=49,proof_or_source_claims_limited=True)
 save('named-review.payload.json',p)
 save('decision.json',dict(status=p['status'],actor=ACTOR,named_complete_RAW_payload=pin(O/'named-review.payload.json'),decision=p['decision'],source_expectations=pin(O/'source.expectations.json'),source_first_seal=pin(O/'source-first.seal.json'),no_canonical_Git_ledger_writes=True,no_70_BODY_read=True))
 print(json.dumps(dict(status=p['status'],actual_PID=os.getpid(),named_complete_RAW=pin(O/'named-review.payload.json'))))

if __name__=='__main__':
 try:globals()[sys.argv[1]]()
 except Exception as e:
  if not(O/'lease.final.json').exists():save((sys.argv[2] if len(sys.argv)>2 else sys.argv[1])+'.failure.json',dict(actual_PID=os.getpid(),utc=now(),error=repr(e),traceback=traceback.format_exc()))
  raise
