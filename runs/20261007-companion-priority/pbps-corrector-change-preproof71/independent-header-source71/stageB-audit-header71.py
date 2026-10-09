import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,hashlib,re,os,base64,datetime
O=pathlib.Path(__file__).resolve().parent;ROOT=pathlib.Path('E:/Samplinglib');H=lambda b:hashlib.sha256(b).hexdigest()
C=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def J(n):return json.loads((O/n).read_bytes())
def put(n,x):assert not (O/n).exists();(O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
raw=(O/'candidate71.header.exactraw.lean').read_bytes();c=raw.splitlines(keepends=True);p=(O/'parent70.compiled-module.exactraw.lean').read_bytes().splitlines(keepends=True)
assert len(c)==147
restored=b''.join(c[26:132])+c[132].replace(' ∧\n'.encode(),b')\n')
assert restored==b''.join(p[26:133])
assert b''.join(c[18:25])==b''.join(p[18:25])==b''.join(c[138:145])
assert c[25].split(b' : Prop :=')[0]==c[145].split(b' : actual_corrector_change_statement')[0]
assert b''.join(c[137:146])==b''.join(p[134:143]).replace(b'actual_projected_rotation',b'actual_corrector_change')
common=re.findall(r'∃\s+(\S+)\s*:',b''.join(c[26:116]).decode());assert common==['S','e','U','T','Γ','q','ΓP0','Inv','A0','B0','V0','R']
expected_tail='''                                let C : HP0 → HP0 → ℝ := fun u v =>
                                  (‖u‖^2-‖v‖^2)/2-inner ℝ (A0 (Inv u)) v
                                C gP gV-C fP fV= -‖fP‖^2+‖fV‖^2)
'''.encode()
assert b''.join(c[133:136])==expected_tail
assert c[0]==b'import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualProjectedRotation\n'
assert c[146]==b'  unfold actual_corrector_change_statement\n'
put('stageB.exact-parent-and-new-C-clause-audit.json',{'schema':'prospective-header71-exact-structural-comparison-v1','actual_pid':os.getpid(),'candidate_header_RAW_bytes':len(raw),'candidate_header_RAW_sha256':H(raw),'candidate_header_lines':147,'parent70_module_RAW_sha256':H(b''.join(p)),'parent70_literal_value_lines':[27,133],'candidate_literal_value_lines':[27,136],'delete_only_new_lines':[134,136],'restore_parent_terminal_line':133,'restored_complete_parent_literal_exact_byte_equal':True,'same_six_public_private_parent_binders':True,'public_signature_equal_after_exact_name_reversal':True,'common12_witnesses':common,'new_C_expression_exact':'(‖u‖^2-‖v‖^2)/2-inner ℝ (A0 (Inv u)) v','new_actual_change_exact':'C gP gV-C fP fV= -‖fP‖^2+‖fV‖^2','only_added_mathematical_conclusion':True,'no_added_public_binder_or_existential_provider':True,'tail147_representation_unfold_only':'Incomplete prospective proof starter, not a compiled71 proof or mathematical provider. No proof search or compile performed.'})
reas={
'H00':([19,26,139,146],'accepted','Six original analytic caller groups and structural finite real Hilbert/Borel input binders byte-equal to parent70; no new caller.'),
'H01':([45,108,117,136],'accepted','Exact common12 witness introduction order before global ∀f, with same original result prefix.'),
'H02':([134,135],'accepted','C typed HP0→HP0→ℝ; SAME A0(Inv u), real inner product, factor1/2 and minus cross term match B20. Division by2 equals source1/2 coefficient over ℝ.'),
'H03':([85,97,135,135],'accepted','Same retained ΓP0, centered two-sided Inv and selfadjoint/commute data; C does not introduce full-space inverse or choose alternate operators.'),
'H04':([117,124],'accepted','Original global f zero-mean, actual conditional fP and Rf/V0*Rf, all old adjoint and norm clauses preserved exactly.'),
'H05':([125,130],'accepted','g=U(Pf-(f-Pf)); its zero mean retained as conclusion; gP actual condExp and gV=V0*Rg. No RHS-defined vector or mean_g binder.'),
'H06':([131,133],'accepted','Both exact rotation formulas and pair-energy equality retained unchanged, now followed by new C clause.'),
'H07':([134,136],'accepted','Corrector uses same A0 and Inv and actual same gP,gV,fP,fV. Exact B21 -||fP||²+||fV||² conclusion, not a bound or swapped sign.'),
'H08':([27,136],'accepted','Removing only localC definition/newchange tail and restoring parent line133 terminal parenthesis recovers full parent70 literal value byte-for-byte.'),
'H09':([19,26,139,146],'accepted','No new caller/provider/existential; sole import parent70. No ontoV/coisometry, positive rank,68sharpenergy,H1/extra derivatives orρ/ω/c0 parameter.'),
'H10':([19,26,78,97],'accepted','No rank-positive requirement; βη≤1 remains non-strict, αη=1 legal. Centered zero space admits inherited inverse contract; C and identity degenerate to zero.'),
'H11':([134,136],'accepted-boundary-only','Primary B4/B28 adds exact B21 actual correction, so real consumer present. Header does not add Kf/rρ/B4error/dynamics/main/cost/composition result.'),
'H12':([18,136,138,147],'accepted-prospective-reader-obligation','Private literal is complete proposition definition, public theorem asserts it with unchanged callers. Unfold147 supplies no proof. Future reader must expose complete exact literal adjacent; no current reader/publication delivery claimed.'),
'H13':([1,147],'accepted-header-only-boundary','Header fragment ends after representation unfold and has no finished proof/compilation claim. No71 implementation, blind decoder, whole source or SAU VERIFIED credit inferred.')}
obs=[]
for q in J('stageA.source-expectations71.before-header.frozen.json')['obligations']:
 a,st,r=reas[q['id']];obs.append({**q,'status':st,'header_line_anchors':a,'independent_reason':r})
put('stageB.all14-header-obligation-decisions.json',{'schema':'prospective-header71-exhaustive-obligation-decisions-v1','count':14,'unclassified':0,'obligations':obs})
lineitems=[]
for i,b in enumerate(c,1):
 node=(18<=i<=136 or 138<=i<=146)
 lineitems.append({'line':i,'RAW_sha256':H(b),'classification':'NODE' if node else 'EXCLUDED','reason':('Complete retained parent literal/header or exact new C definition/change' if node else 'Module/import/comment/options/namespace context, blank, or unproved representation-only unfold starter; no independent71 proof assertion')})
put('stageB.header147-finite-line-coverage.json',{'count':147,'NODE':128,'EXCLUDED':19,'unclassified':0,'entries':lineitems,'not_implementation_BODY_coverage':True})

# Reuse parent70 actual compile receipt read-only; no prior math verdict.
src=O.parents[1]/'pbps-actual-projected-rotation70/independent-source70/root70.focused-canonical-v2.receipt.exactraw.json';b=src.read_bytes();n='parent70.focused-compile.receipt.exactraw.json';(O/n).write_bytes(b);(O/(n+'.LF')).write_bytes(b.replace(b'\r\n',b'\n'))
receipt=json.loads(b);assert receipt['actual_foreground_PID']==9524 and receipt['exit_code']==0
inputs=J('stageA.primary-input-manifest.json')['inputs']+J('stageB.candidate-input-manifest.json')['inputs']+[{'original_path':str(src),'snapshot':n,'RAW_bytes':len(b),'RAW_sha256':H(b),'LF_snapshot':n+'.LF','LF_bytes':len(b.replace(b'\r\n',b'\n')),'LF_sha256':H(b.replace(b'\r\n',b'\n')),'LF_recipe':'replace ONLY CRLF bytes with LF','original_mtime_ns':src.stat().st_mtime_ns}]
assert len(inputs)==14
for q in inputs:
 assert pathlib.Path(q['original_path']).read_bytes()==(O/q['snapshot']).read_bytes()
put('complete-exact-input-manifest.json',{'schema':'prospective-header71-complete-exact-inputs-v1','input_count':14,'inputs':inputs,'RAW_LF_recipe':'replace ONLY CRLF bytes with LF; no other normalization','original_closed319_portable14_sourcefirst116_unchanged':True})
put('complete-RAW-LF-input-payload.json',{'input_count':14,'inputs':[{**q,'RAW_base64':base64.b64encode((O/q['snapshot']).read_bytes()).decode(),'LF_base64':base64.b64encode((O/q['LF_snapshot']).read_bytes()).decode()} for q in inputs]})
decision={'schema':'prospective-header71-independent-source-decision-v1','reviewer':'independent_primary69 / independent-header-source71','status':'ACCEPT_PROSPECTIVE_HEADER_SOURCE_ONLY','candidate_header_RAW_sha256':H(raw),'proposal_RAW_sha256':H((O/'candidate71.proposal.exactraw.json').read_bytes()),'expectation_before_header_RAW_sha256':H((O/'stageA.source-expectations71.before-header.frozen.json').read_bytes()),'source_shape':'Exact B20 same-centered-C applied to actual retained70 projected components gives exact B21 C-change; real B4/B28 consumer retained as boundary.','all14_expectations_satisfied':True,'all6_callers12_common_witnesses_and_complete70_result_retained':True,'required_mathematical_or_header_repairs':[],'source_ingredients_are_internal_edges_not_new_public_binders':True,'reader_requirement':'Future unit must expose exact complete private literal definition adjacent and label it proposition storage/nonprovider.','independence':{'from_formalizer':True,'prior_header_math_verdict_read':False,'sourcefirst71_verdict_or_interface_read':False,'primary_expectations_frozen_before_candidate':True,'unchanged70_background_reuse_disclosed':True},'coverage':{'primary_regions':4,'primary_math_items':255,'source_NODE':11,'source_EXCLUDED':244,'exact_target_formulas':18,'header_lines':147,'header_NODE':128,'header_EXCLUDED':19,'obligations':14},'parent70_compile_evidence_only':{'PID':9524,'EXIT':0,'module_RAW_sha256':'03a0721ae952f744d0bfdf568039b77f7035bec0a50642f8bc8ebc895273b998'},'no71_compile_or_proof_search':True,'remaining_boundary':['71proof implementation and independent math/source-blind roundtrip','B4errors/dynamics/main/query costs/composition','wholepaper/fullExposition/PURIFIED/VERIFIED/main/live'],'canonical_applied':False}
put('header-source71.decision.json',decision)
review='''Prospective71 header source review only. ACCEPT_PROSPECTIVE_HEADER_SOURCE_ONLY; no mathematical/header repair required.
StageA source expectations froze before first reading exact candidate71 header/proposal. Root task disclosed intended delta; reviewer knows full parent70 from prior own source audit and honestly reuses unchanged background. No old header-math verdict or source-first71 decision/interface read. Source-first71 closure114opaque file hashes checked; its verdict is not authority.
Primary RAW1482128B d81e929... and four regions independently verified. All255 MathML items re-parsed with alttext=TeX annotation;18target formulas matched exact RAW ranges/hashes. B20 explicitly restricts inverse to HP0. B21 substitutes actual parent70 rotation into SAME C and yields -||fP||²+||fV||². B4 source wording explicitly says combined with B21 and B28 adds this actual correction to residual error term. This is a real future consumer, not a new71 conclusion or dependency premise.
Candidate147lines/8727B2bef0d5c... retains the complete parent70 literal result: delete lines134-136 and restore line133 terminal parenthesis to obtain exact old literal27-133 byte-for-byte. Six original caller groups/private+public binders exact;12common witnesses identical before every globally centered f. Same actual U,root,centered Inv,A0,V0,R,D,all-kerP intertwining and all old global clauses retained. Mean_g remains a concluded internal parent fact. gP actual condExp and gV V0*Rg; neither is defined as coefficient RHS. Actual old rotation and pair energy preserved.
New local C:HP0→HP0→ℝ is `(||u||²-||v||²)/2-inner(A0(Inv u),v)`. This is the exact source B20 functional, with SAME centered A0/Inv. New sole mathematical conclusion is C(gP,gV)-C(fP,fV)=-||fP||²+||fV||². Private literal is proposition storage, not a provider. Public theorem has unchanged six callers and asserts it. Final unfold147 is an incomplete proof starter, not71 proof or compile success.
No ontoV,VV*=I,global inverse,positive rank,sharpenergy68,extra regularity/H1 observable,ρ/ω/c0 or certificate premise. Rank0 and αη=1 retained. B4/main/errors/cost/composition remain open. Future reader must fold complete literal adjacent with definition/nonprovider label; no reader delivery or full Exposition claimed now.
Finite coverage:255source items11NODE244EXCLUDED,18explicit target formulas11NODE7EXCLUDED; unrelated/global/D1 and prior70 background exclusions are explicit reuse, not full source replay. Header147lines128NODE19EXCLUDED,14pre-frozen obligations individually accepted. No implementation BODY/source completion, decoder result, SAU claim/VERIFIED or canonical edits.
Retired own reading-aid issue: v1 numeric placeholders were replaced by prefix and distorted formula10+; v2 single-pass regex repaired derived reading aid before expectations freeze. RAW inputs/all formula hashes unchanged. Both helpers/results retained. No terminal failure occurred; all current foreground stage receipts EXIT0.
'''
review+='\nComplete independent14obligation decisions:\n'+json.dumps(obs,ensure_ascii=False,indent=2)+'\n'
(O/'header-source71.complete-RAW-review.txt').write_text(review,encoding='utf-8',newline='\n')
run={'schema':'prospective-header71-independent-source-run-v1','actual_author_pid':os.getpid(),'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'decision':decision,'complete_RAW_review_text':review,'exact_input_manifest':J('complete-exact-input-manifest.json'),'source_expectation_before_header':J('stageA.source-expectations71.before-header.frozen.json'),'anti_anchoring':J('stageA.anti-anchoring-exposure.frozen.json'),'parent_retention':J('stageB.exact-parent-and-new-C-clause-audit.json'),'coverage':decision['coverage'],'logical_recipe':'Delete ONLY top-level run_sha256; sorted compact ensure_ascii=False UTF8 JSON.','run_sha256':''};run['run_sha256']=H(C({k:v for k,v in run.items() if k!='run_sha256'}));put('header-source71.run.json',run)
layers=['header-source71.decision.json','header-source71.run.json','header-source71.complete-RAW-review.txt','stageA.source-expectations71.before-header.frozen.json','stageA.anti-anchoring-exposure.frozen.json','stageA.finite-source255-and-target18-coverage.frozen.json','stageB.exact-parent-and-new-C-clause-audit.json','stageB.all14-header-obligation-decisions.json','stageB.header147-finite-line-coverage.json','complete-exact-input-manifest.json','complete-RAW-LF-input-payload.json']
put('complete-named-review-decision-input-payload.json',{'schema':'prospective-header71-complete-named-native-payload-v1','whole_logical_run_sha256':run['run_sha256'],'layers':[{'name':n,'RAW_bytes':len((O/n).read_bytes()),'RAW_sha256':H((O/n).read_bytes()),'RAW_base64':base64.b64encode((O/n).read_bytes()).decode()} for n in layers],'scope':'Prospective header only; no proof/full-source/VERIFIED credit.'})
print(json.dumps({'actual_pid':os.getpid(),'status':decision['status'],'all14accepted':True,'candidate_RAW_sha256':H(raw),'whole_logical_run_sha256':run['run_sha256'],'decision_RAW_sha256':H((O/'header-source71.decision.json').read_bytes()),'exact_inputs':14,'named_payload_RAW_bytes':(O/'complete-named-review-decision-input-payload.json').stat().st_size},ensure_ascii=False))
