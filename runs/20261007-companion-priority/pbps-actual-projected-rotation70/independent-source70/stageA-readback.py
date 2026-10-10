import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,hashlib,base64,datetime,os,re,html
O=pathlib.Path(__file__).resolve().parent
J=lambda p:json.loads(p.read_bytes())
H=lambda b:hashlib.sha256(b).hexdigest()
C=lambda v:json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def save(n,v):
 p=O/n;assert not p.exists();p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
exp=J(O/'stageA.source-expectations70.before-current-BODY.frozen.json')
for key in ['source_graph','finite_primary_coverage','finite_obligations','prior_exposure_disclosure']:
 e=exp[key];b=(O/e['name']).read_bytes();assert len(b)==e['RAW_bytes'] and H(b)==e['RAW_sha256']
graph=J(O/exp['source_graph']['name']);coverage=J(O/exp['finite_primary_coverage']['name']);obligations=J(O/exp['finite_obligations']['name'])
assert len(graph['nodes'])==22 and len(graph['edges'])==49
assert len(coverage['entries'])==419 and coverage['counts']=={'NODE':175,'EXCLUDED':244} and coverage['unclassified']==0
assert len(obligations['obligations'])==24 and len(exp['canonical_semantic_slots_source_expectations'])==7
inv=J(O/'stageA.primary419.reparsed-inventory.json');byid={m['id']:m for m in inv['math_items']};primary=(O/'primary-pbps.exactraw.snapshot.html').read_bytes()
for e in coverage['entries']:
 a,z=e['source_RAW_range_end_exclusive'];b=primary[a:z];assert H(b)==e['RAW_sha256']; assert e['id'] in byid and e['alttext']==byid[e['id']]['alttext'];assert e['classification'] in ['NODE','EXCLUDED'] and e['reason']
for n in graph['nodes']:
 for m in n['primary_math']: assert byid[m['id']]==m
for r in inv['regions']:
 text=(O/('stageA.primary-readview-v2.'+r['name']+'.txt')).read_text(encoding='utf-8')
 entries=[m for m in inv['math_items'] if m['region']==r['name']]
 assert text.count('\nMATH ')==len(entries)
 for e in entries:
  a,z=e['source_RAW_range_end_exclusive'];expected='\nMATH '+e['id']+' RAW['+str(a)+','+str(z)+') '+e['alttext']+'\n';assert expected in text
manifest=J(O/'stageA.complete-primary-input-manifest.frozen.json');payload=[]
for e in manifest['inputs']:
 raw=(O/e['snapshot']).read_bytes();lf=(O/e['LF_snapshot']).read_bytes();assert H(raw)==e['RAW_sha256'] and len(raw)==e['RAW_bytes'];assert lf==raw.replace(b'\r\n',b'\n') and H(lf)==e['LF_sha256']
 source=pathlib.Path(e['original_path']);current=source.read_bytes()
 if 'original_RAW_range_end_exclusive' in e:
  a,z=e['original_RAW_range_end_exclusive'];assert H(current)==e['original_whole_RAW_sha256'];current=current[a:z]
 assert current==raw
 payload.append({**e,'RAW_base64':base64.b64encode(raw).decode('ascii'),'LF_materialization':{'recipe':'replace only CRLF with LF','RAW_input_entry':e['snapshot'],'result_RAW_bytes':len(lf),'result_sha256':H(lf),'separate_exact_LF_snapshot':e['LF_snapshot']}})
assert len(payload)==22
save('stageA.complete-exact-RAW-LF-input-payload.json',{'schema':'source70-stageA-complete-exact-input-payload-v1','all_22_named_inputs_complete':True,'input_count':22,'inputs':payload,'no_decoder_or_current70_BODY_input':True,'LF_bytes_recoverable_from_explicit_recipe_and_exact_LF_snapshots':True})
review='''Stage A independent primary-source expectation freeze for actual projected rotation70.

This is primary-source preparation only. No current70 full BODY, publication candidate or blind decoder reconstruction has been read. No final source admission, theorem verification or compiler credit is issued.

Authority: fixed PBPS v1 full RAW HTML (1,482,128 bytes; d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760), seven exact RAW regions and419 MathML tags with alttext/annotation TeX equality. CLOSED83 source-only expectations, graph and header coverage are reused read-only after all81regular hashes and manifest/lease identities were verified. The source graph topology is reused rather than claimed to have been created afresh; current70 roles and the direct primary argument have been reread independently of the implementation.

The current target is actual P12/P13/P14. For each globally centered original f, the SAME actual U and condExp P give g=U(Pf-(f-Pf)). Its actual components are gP=Pg and gV=V0*Rg on the centered macro space, not definitions by coefficient formulas. Required formulas are gP=A0fP-GammaP0fV, gV=GammaP0fP+A0fV and pair squared-norm conservation. The macro minus and micro plus signs are exact. Internal proof obligations include actual pullback/AE and conditional expectation/integral transport, producing mean(g)=0 before the centered gP witness.

The mean completion is necessary source detail, not an extra caller. Since F preserves J, integral(Uh)=integral(h) for integrable L2 h; integral(Ph)=integral(h). Thus integral(g)=2integral(Pf)-integral(f)=integral(f)=0. J is a probability law; representative/AE links and L2 integrability must be established internally. A formalizer may use an equivalent U1/selfadjoint route only while retaining those exact actual-law semantics.

The full original69 contract and twelve common witnesses precede the universal centered f, and all six analytic conditions remain the sole analytic callers. D is canonical R U inclusion on all kerP. The same root and centered inverse/polar V0 are retained, with no onto-V, coisometry, global inverse, positive rank, extra regularity, rho/omega/small-c0 or68sharp-energy premise. Endpoints rank0 andalphaeta=1 remain included.

P16/P17 are real B20/B21 downstream consumers; P19 is the actual B4 comparator and error pair; P21 contains the explicit pair-energy consumer A2.SS3.p9.m2. These source consumers are not70 theorem conclusions or invented proof parents. B21, B4, main result, composition, full paper and Goal completion remain unestablished by this stage.

The finite419-item classification has175NODE/244EXCLUDED. It reuses the immutable173NODE header coverage with all419 identities revalidated; two exact B4 actual-component definitions are independently promoted to P19 consumer anchors. Every exclusion has a scoped reason. NODE denotes source membership only. The graph has22nodes49source-ingredient edges, and24typed obligations are pending implementation comparison. No source ingredient is legalized as a public caller binder.

Prior exposure is disclosed separately: earlier representation reviews did opaque whole-byte BODY equality and displayed only minimal post-header syntax, without mathematical BODY reading. This is not claimed to be byte-unexposed. A first generated plain-text reading aid could swallow TeX less-than inequalities during HTML stripping; it is retained as retired, replaced by a placeholder-protected v2 aid, and all419 formulas were checked against RAW. RAW source inputs were never changed.

Next permitted stage starts only after the official source reviewer packet. Compare the exact full current module, private literal/public callers, all BODY formulas/publication context and the blind seven-slot reconstruction against this frozen source expectation. Named-literal representation requires the exact complete statement adjacent to folded reader code and must not be described as a provider. Finish with current native decision schema, full named review/input payload and last-write CLOSED lease only after that comparison.
'''
(O/'stageA.complete-RAW-review.txt').write_text(review,encoding='utf-8',newline='\n')
checks=[{'id':'primary-fixed-authority','status':'PASS','evidence':'full RAW and exact region maps'}, {'id':'prior83-read-only-integrity','status':'PASS','evidence':'81regular+manifest+lease hashed'}, {'id':'math419-reparse','status':'PASS','evidence':'all ids/raw offsets/sha/alttext/annotation match'}, {'id':'reading-aid-v2','status':'PASS','evidence':'all419 full math formula strings intact'}, {'id':'graph-and-current-role-freeze','status':'PASS','evidence':'22nodes49edges source only'}, {'id':'finite-coverage','status':'PASS','evidence':'419items175NODE244EXCLUDED0unclassified'}, {'id':'mean-completion-and-public-binders','status':'EXPECTED_PENDING_BODY','evidence':'24obligations and seven source slots frozen'}, {'id':'current70-full-source-review','status':'PENDING_OFFICIAL_PACKET','evidence':'no BODY/publication/decoder mathematical read'}]
save('stageA.preparation-only.checks.json',{'schema':'source70-stageA-preparation-checks-v1','actual_pid':os.getpid(),'checks':checks,'source_admission':None,'mathematical_proof_admission':None,'no_final_verdict':True})
run={'schema':'source70-stageA-native-preparation-run-v1','actual_pid':os.getpid(),'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'StageA-primary-only-expectation-freeze','status':'OPEN_PENDING_OFFICIAL_PACKET','source_verdict':None,'review':{'name':'stageA.complete-RAW-review.txt','RAW_sha256':H((O/'stageA.complete-RAW-review.txt').read_bytes())},'frozen_expectations':{'name':'stageA.source-expectations70.before-current-BODY.frozen.json','RAW_sha256':H((O/'stageA.source-expectations70.before-current-BODY.frozen.json').read_bytes())},'input_payload':{'name':'stageA.complete-exact-RAW-LF-input-payload.json','RAW_sha256':H((O/'stageA.complete-exact-RAW-LF-input-payload.json').read_bytes())},'input_count':22,'no_Lean_compile_or_canonical_write':True,'whole_logical_rule':'delete ONLY top-level run_sha256; sorted compact UTF-8 JSON; ensure_ascii=False'}
run['run_sha256']=H(C(run));save('stageA.preparation-only.run.json',run)
print(json.dumps({'actual_pid':os.getpid(),'preparation_run_sha256':run['run_sha256'],'frozen_expectations_RAW_sha256':run['frozen_expectations']['RAW_sha256'],'source_verdict':None,'official_packet_pending':True,'input_count':22,'all_checks_readback':True},ensure_ascii=True))
