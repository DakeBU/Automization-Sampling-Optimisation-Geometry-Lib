import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,hashlib,os,collections
O=pathlib.Path(__file__).resolve().parent
def J(n):return json.loads((O/n).read_bytes())
def H(b):return hashlib.sha256(b).hexdigest()
def save(n,x):assert not (O/n).exists();(O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
ls=(O/'final70.source_body.exactraw.lean').read_bytes().splitlines(keepends=True)
par=(O/'parent69.ReflectionIntertwining.exactraw.lean').read_bytes().splitlines(keepends=True)
stripped=b''.join(ls[26:123])+ls[123].replace(' ∧\n'.encode(),b')\n')
assert stripped==b''.join(par[25:123])
assert ls[18:25]==ls[135:142]
save('stageB.parent69-retention.exact.json',{'schema':'exact-complete-parent-retention-v1','same_six_public_and_private_binders':True,'parent69_literal_value_RAW_range_lines':[26,123],'current70_literal_value_RAW_range_lines':[27,133],'delete_only_new_rotation_tail_lines':[125,133],'terminal_old_conjunct_restoration':'current line124 terminal conjunction restored to parent closing parenthesis','recovered_parent_value_exact_byte_equal':True,'retained12_common_witnesses':True,'no_old_parent_global_f_clause_lost':True,'proof_reassembly_lines':[480,539],'not_reusing_old_source_verdict_as_current_decision':True})

node_map={
'P0':([19,26,136,143],'original-six-callers-and-geometric-conventions'),
'P1':([27,32,146,151,480,488],'actual-law-retained-parent-contract'),
'P2':([51,53,314,325],'same-actual-reflection-AE-and-internal-integral-adapter'),
'P3':([33,44,326,360],'actual-condExp-projection-complement-and-inclusions'),
'P4':([60,66,337,360],'same-actual-compressions-retained-and-transported'),
'P5':([67,73,366,381],'same-positive-root-square-sum-selfadjoint-commutation'),
'P6':([74,88,480,539],'centered-gap-retained-parent-contract'),
'P7':([89,97,480,539],'same-centered-inverse-retained-parent-contract'),
'P8':([102,107,361,365],'same-polar-into-isometry-no-onto-premise'),
'P9':([108,111,339,411],'ambient-intrinsic-adjoint-transport'),
'P10':([117,124,400,411],'same-actual-centered-global-f-decomposition'),
'P11':([112,116,310,313,449,455],'same-canonical-D-all-kerP-intertwining-retained-and-consumed'),
'P12':([117,124,400,411],'actual-input-components-produced-from-parent'),
'P13':([125,130,314,335,412,422],'actual-g-internal-mean-and-actual-g-components'),
'P14':([131,133,423,458],'actual-projected-rotation-and-pair-energy-current-delta'),
'P15':([], 'corrector-definition-source-only-next-edge-not70-result'),
'P16':([], 'corrector-algebra-real-next-consumer-not70-result-or-parent'),
'P17':([], 'B21-corrector-change-real-next-consumer-not70-result'),
'P18':([], 'leading-term-norm-source-consumer-not70-result'),
'P19':([], 'B4-actual-comparator-source-consumer-not70-result'),
'P20':([], 'B28-adds-B21-source-consumer-not70-result'),
'P21':([], 'explicit-B4-pair-energy-budget-consumer-not70-decay-result')}
source=J('stageA.primary419-NODE-EXCLUDED70.frozen.json'); entries=[]
primary=(O/'primary-pbps.exactraw.snapshot.html').read_bytes()
for e in source['entries']:
 a,z=e['source_RAW_range_end_exclusive'];assert H(primary[a:z])==e['RAW_sha256']
 x=dict(e);x['current_review_node_dispositions']=[{'node':n,'module_line_anchors':node_map[n][0],'role':node_map[n][1]} for n in e['source_nodes']]
 x['current_decision']='source-excluded-with-original-reason' if e['classification']=='EXCLUDED' else 'source-node-accounted-for-with-explicit-current-role'
 x['not_automatic_Lean_proof_credit']=True;entries.append(x)
assert len(entries)==419 and collections.Counter(e['classification'] for e in entries)=={'NODE':175,'EXCLUDED':244}
save('stageB.primary419-current-exhaustive-decisions.json',{'schema':'source70-419-item-exhaustive-decisions-v1','count':419,'counts':{'NODE':175,'EXCLUDED':244},'unclassified':0,'source_regions':7,'source_nodes':22,'source_edges':49,'every_RAW_formula_revalidated':True,'entries':entries,'all_classified_does_not_mean_proved':True,'B21_B4_fullpaper_not_complete':True})

blocks=[(18,26,'literal-original-callers','P0'),(27,50,'literal-actual-laws-projection-kernel','P1/P3'),(51,66,'literal-actual-reflection-compressions','P2/P4'),(67,97,'literal-same-root-centered-inverse','P5/P6/P7'),(98,116,'literal-same-polar-all-micro-intertwining','P8/P9/P11'),(117,124,'literal-old-global-f-result','P10/P12'),(125,133,'literal-new-actual-g-rotation-energy','P13/P14'),(135,143,'public-original-six-callers-assert-literal','P0'),(144,159,'unfold-same-parent-actual-geometry','P0/P1/P2/P3'),(160,309,'destructure-retain-all-parent-clauses-and-common-witnesses','P4/P5/P6/P7/P8/P9/P10/P11/P12'),(310,313,'canonical-D-and-all-micro-intertwining','P11'),(314,335,'internal-mean-preservation-integrability-AE-condExp-adapters','P2/P3/P13'),(336,365,'actual-inclusion-compression-adjoint-factorization-transport','P3/P4/P8/P9'),(366,381,'same-root-real-Hilbert-energy-and-cross-term-identities','P5/P14'),(382,411,'actual-fP-Rf-VadjRf-intrinsic-adjoint','P10/P12'),(412,422,'actual-g-internal-zero-mean-actual-condExp-gP','P13'),(423,448,'actual-macro-rotation-by-inner-separation','P14'),(449,455,'actual-micro-rotation-from-all-kerP-negative-intertwining','P11/P14'),(456,458,'actual-pair-energy-cross-cancellation','P14'),(459,479,'retain-old-global-f-and-new-actual-output-conclusions','P10/P12/P13/P14'),(480,539,'reassemble-all-old-parent-clauses-and-common-witnesses','P0/P1/P2/P3/P4/P5/P6/P7/P8/P9/P10/P11/P12/P13/P14')]
lineitems=[]
for i,b in enumerate(ls,1):
 text=b.decode().rstrip('\n');hit=[q for q in blocks if q[0]<=i<=q[1]]
 if text.strip() and hit:
  assert len(hit)==1;q=hit[0];kind='NODE';reason=q[2];nodes=q[3].split('/')
 else:
  kind='EXCLUDED';nodes=[];reason=('blank source line' if not text.strip() else 'module context/import/comment/options/namespace closure or #print axioms diagnostic; no independent mathematical assertion')
 lineitems.append({'line':i,'RAW_sha256':H(b),'text':text,'classification':kind,'source_nodes':nodes,'reason':reason})
lc=dict(collections.Counter(e['classification'] for e in lineitems))
save('stageB.whole-module544-line-coverage.json',{'schema':'source70-whole-module-finite-line-coverage-v1','count':544,'counts':lc,'unclassified':0,'module_RAW_sha256':H(b''.join(ls)),'all_lines_read':True,'literal_lines':[18,133],'public_signature_lines':[135,143],'BODY_lines':[144,539],'diagnostic_line':544,'blocks':blocks,'entries':lineitems})

reasons={
'O00':('accepted-current-header',[19,26,136,143],'Only hα,hαβ,hV,hH,hη,hβη; structural real finite-dimensional Borel conventions explicit. No positive-rank or strict βη<1 binder.'),
'O01':('accepted-same-actual-definitions',[27,53,146,159,316,325],'J is actual Gibbs-Gaussian augmentation; same U and F pulled back AE per L2 input. Internal integral transport uses exactly hU from that common witness.'),
'O02':('accepted-internal-production',[314,325],'Probability J and L2 integrability established internally. F measurable and F#J=J from reflection_preserves_augmentation; hU AE plus integral_map yield integralU.'),
'O03':('accepted-internal-production',[326,338],'Actual P=HP.subtypeL∘condExpL2. integral_condExpL2_eq on univ yields integralP. Orthogonal projection identity produces selfadjoint P; hR is canonical complement.'),
'O04':('accepted-retained-and-consumed',[108,116,310,313,354,360,449,455],'D definition exactly R∘U∘kerP inclusion; semantic equality retained for every h:kerP, never restricted to rangeV.'),
'O05':('accepted-exact-parent-retention',[27,124,158,309,480,539],'Deleting only70 tail and closing old conjunction recovers complete69 literal value byte-for-byte. All12 witnesses common before ∀f; source ingredients remain produced dependencies/conclusions.'),
'O06':('accepted-same-centered-data',[67,97,366,381],'Same nonnegative root ΓP0 restricted to HP0, centered two-sided Inv, A0 restrictions and commutation retained; energy uses hRoot from same witnesses.'),
'O07':('accepted-no-onto-strengthening',[104,107,120,124,361,365],'Only V*V=I and norm-preserving embedding; e is onto but V is not. No V V*=I or fperp=VfV inferred.'),
'O08':('accepted-actual-input-production',[117,124,400,411],'For every centered L2 f, parent global decomposition supplies actual condExp fP. fperp=Rf and fV=V*Rf are definitions with old adjoint/norm clauses retained.'),
'O09':('accepted-actual-update-definition',[125,125,412,422],'g is literally U(Pf-(f-Pf)); input split is proved from actual hPfp and hR, not chosen abstract coefficient data.'),
'O10':('accepted-internal-production',[126,126,413,416],'Mean(g)=0 follows integralU, integralP, integralLp_sub, hf. No mean_g binder, premise, supplied witness property or unproved adapter.'),
'O11':('accepted-actual-output-production',[127,128,417,418],'Parent global decomposition applied to g using internally proved hgMean produces gP satisfying actual condExpL2 g; rotation RHS proved later.'),
'O12':('accepted-actual-output-definition',[129,130,449,455],'gperp=Rg and gV=V*Rg are actual definitions on kerP/HP0, not rotation RHS definitions.'),
'O13':('accepted-actual-macro-proof',[423,448],'hPg=actual Pg, P selfadjoint, U selfadjoint, Uι decomposition, orthogonality and intrinsic adjoint yield gP=A0 fP-ΓP0 fV by inner separation.'),
'O14':('accepted-actual-micro-proof',[449,455],'R Uι=B0; V*B0=ΓP0; inherited operator identity on all kerP gives V*D fperp=-A0 V*fperp. Subtraction changes this to plus.'),
'O15':('accepted-exact-signs',[131,132,423,455],'Macro minus ΓP0 fV; micro plus A0 fV. Both actual equations derived with source signs.'),
'O16':('accepted-internal-algebra',[366,381,456,458],'Same-root square-sum and real selfadjoint commutation give hEnergy and hCross. norm_sub_sq_real+norm_add_sq_real cancel mixed terms; no new inverse premise used.'),
'O17':('accepted-actual-energy-conclusion',[133,133,456,459],'Actual gP,gV substituted into energy; proof retains actual f components and original semantics. Arbitrary-vector algebra is only internal ingredient.'),
'O18':('accepted-downstream-boundary-only',[],'P16/P17 corrector algebra and B21 corrector change are real source consumers;70 does not prove C-change or take sharp-energy68 as parent.'),
'O19':('accepted-downstream-boundary-only',[],'P19/B27 actual comparator and P20/B28 real consumers recorded; no70 B4/full dynamical/error result and no new ρ,ω,c0 caller.'),
'O20':('accepted-downstream-boundary-only',[],'P21 source A2.SS3.p9.m2 explicitly consumes pair-energy equality as an inequality bound. B17/B30/B31/decay/errors/cost remain outside70.'),
'O21':('accepted-endpoints-and-no-new-premises',[19,26,136,143],'No Finrank-positive, ontoV, global Inv, extra higher derivative/H1 f or ρ/ω/c0 premise. βη≤1 includes αη=1 given α≤β; rank0 remains admitted.'),
'O22':('accepted-bounded-static-reader-contract',[18,133,135,143,144,539],'Full exact private literal is adjacent nested helper with definition/nonprovider label; public signature and8 exact contiguous folded BODY steps. Frozen StageA prose mentioned six steps from69; current exact70 has8, explicitly corrected here without modifying freeze. Full browser/visual/Exposition not claimed.'),
'O23':('accepted-current-anti-anchored-comparison',[1,544],'Primary freeze before current BODY; current full module, source419, blind7 fields, public/literal/body and exact8 lesson formulas compared. Official final packet1 bound; no independent math verdict read/substituted.')}
obs=[]
for ob in J('stageA.exhaustive-finite-obligations70.frozen.json')['obligations']:
 x=dict(ob);st,anchors,r=reasons[x['id']];x['current70_implementation_status']=st;x['module_line_anchors']=anchors;x['independent_decision_reason']=r;obs.append(x)
save('stageB.all24-obligation-decisions.json',{'schema':'source70-exhaustive-finite-obligation-decisions-v1','count':24,'unclassified':0,'all':obs,'no_new_public_source_ingredient_binders':True})
save('stageB.reader-overlay-and-failed-check-disposition.json',{'schema':'source70-reader-overlay-and-reviewer-check-disposition-v1','accepted_reader_overlay':'Only /purification/dead_code_audit in cell and /items/0/purification/dead_code_audit in publication; full literal definition, no provider. Root actualPID21704 EXIT0.','root_adoption_RAW_sha256':H((O/'final70.root.metadata-repair.adoption.exactraw.json').read_bytes()),'independent_formula_alarm':'WITHDRAWN: nested repr string was mistaken for actual double backslashes. Direct decoded UTF8 bytes contain single92 before TeX commands; scoped renderer checks all8 correct. No formula edit applied.','retained_failed_checks':[{'label':'stageB-finite-audit','PID':47340,'EXIT':1,'reason':'reviewer incorrectly removed trailing newline from exact lesson code; actual code includes it exactly'},{'label':'stageB-finite-audit-v2','PID':14512,'EXIT':1,'reason':'reviewer false double-backslash assertion; actual formulas correct'}],'corrected_check':{'label':'stageB-finite-audit-v3','PID':41528,'EXIT':0},'exploratory_failures_without_PID_receipt':'One exploratory Python console print in this continuation failed GBK encoding before useful content; exec exit1; no actual child PID captured, not invented. Earlier StageA/StageB exploratory paths/encoding failures disclosed in raw review.','old_packet0_and_final_packet1_identical_RAW':(O/'current70.official-source-review.packet.0.exactraw.json').read_bytes()==(O/'final70.official-source-review.packet.1.exactraw.json').read_bytes(),'audit_bytes_unchanged':(O/'current70.audit.exactraw.json').read_bytes()==(O/'final70.audit.exactraw.json').read_bytes(),'reason_packet_binding_unchanged':'Two changed purification prose fields are outside current binding/context projection; regenerate produced same official content. Actual cell/publication RAW changed and separately verified.','no_mathematical_repair_required':True})
print(json.dumps({'actual_pid':os.getpid(),'source419':{'NODE':175,'EXCLUDED':244},'module544':lc,'obligations':24,'parent69_exact':True,'canonical_writes':False},ensure_ascii=False))
