import hashlib,json,os,pathlib,datetime,subprocess
R=pathlib.Path('E:/Samplinglib');r=R/'runs/20261007-companion-priority/pbps-actual-corrector-change71';OWN=r/'independent-repository-reader71';LEASE=OWN/'lease.final71.json'
assert not LEASE.exists(),'Already CLOSED; no owned writes permitted'
def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(a):return json.dumps(a,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def get(p):return json.loads(pathlib.Path(p).read_text(encoding='utf-8'))
def pin(p):
 p=pathlib.Path(p);b=p.read_bytes();return {'path':p.as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_bytes':len(b.replace(b'\r\n',b'\n')),'LF_sha256':sha(b.replace(b'\r\n',b'\n'))}
def dump(n,a):(OWN/n).write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
packet=get(r/'final-reader-repository-packet71.json');assert pin(r/'final-reader-repository-packet71.json')['RAW_sha256']=='ce23377e2799a9617f19cf7bceefd69bc7b2078e47ad16a463a3950adb8cad06'
e=get(OWN/'evidence71.json');v=get(OWN/'visual-review71.json');fresh=get(OWN/'fresh-checks71.json');assert fresh['all_terminal_EXIT0'] and len(fresh['checks'])==4
SCI=packet['checked_science_commit'];assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()==SCI
for a in fresh['checks']:
 assert a['exit_code']==0 and a['terminal_closed']
 for k in ['stdout','stderr']:assert all(pin(a[k]['path'])[j]==a[k][j] for j in ['RAW_bytes','RAW_sha256','LF_sha256'])
inputs={}
def add(p):
 a=pin(p);inputs[a['path']]=a
for x in packet['inputs']:
 a=pin(x['path']);assert all(a[k]==x[k] for k in ['RAW_bytes','RAW_sha256','LF_sha256']);add(x['path'])
add(r/'final-reader-repository-packet71.json')
for a in e['extra_finite_input_pins']:
 assert pin(a['path'])==a;add(a['path'])
for a in get(OWN/'protocol-inputs71.json')['protocol_inputs']:
 z=pin(a['path']);assert z['RAW_sha256']==a['RAW_sha256'] and z['LF_sha256']==a['LF_only_sha256'] and z['RAW_bytes']==a['raw_byte_count'];add(a['path'])
finite={'schema':'reader71-final-finite-input-manifest-v1','actual_writer_PID':os.getpid(),'RAW_authority':'Exact file bytes','LF_rule':'Only byte CRLF to LF; no other normalization','frozen_packet_input_count':127,'additional_finite_and_protocol_count':len(inputs)-127,'input_count':len(inputs),'all127_rechecked_after_fresh_gates':True,'all_current_inputs_match_frozen_final_packet':True,'inputs':sorted(inputs.values(),key=lambda a:a['path'])};dump('input-manifest71.json',finite)
notes=[
'Final packet received before final site review; RAW/LF pinned; all127 match twice.',
'HEAD SCI71 exact; module/publication/lesson/audit four RAW inputs unchanged. CLOSED116/95/277/10 adoptions reused; sole source actor independent_primary69.',
'Exact C half and negative mixed term, actual B21 -norm(fP)^2+norm(fV)^2, same actual conditional/polar components and inverse preserved.',
'Six callers, twelve common witnesses, parent conclusions and rank0/alphaeta1 endpoints retained in unchanged SCI and complete reader. No onto/extra regularity/provider/mean/68 premise.',
'Eight exact contiguous source BODY spans147-523 total377 lines. Complete module528 lines; preparation wording corrected to distinguish BODY from module.',
'119-line full literal private Prop,7358UTF8bytes, matches source/render; initiallyclosed adjacent helper, representation not proof provider.',
'14details initiallyclosed;3codepanels+8stepfolds. Three exact callback copies and3RAW downloads26489UTF8bytes. JS24587characters is distinct count, not truncated RAW.',
'Actualfocus five incident relations:1declares,2scannerreferences,1audit,1sourcecorrespondence. No Test consumer or conceptual formal edge; source graph not completion.',
'Fresh publication-reviewed/graph/site/contributor allterminalEXIT0; reuse19rootgates,ASTISroot9181/Tests9481,224Python+6JS. No rebuild.',
'All10 finalPNGpixels actually viewed:statement,proof1..8,actualbranch. CopyPNGduplicate not11th. Visual debt explicit.',
'ActualH/K/r_rho/B27/B28/B4/H1/dynamics/cost/composition/fullExposition/PURIFIED/main/live/Goal remainopen.',
'Only scoped aggregate/reader; source-exposed actor discloses blind71/sourceplan72. No newsource/VERIFIED/wholepageSeal orcanonical writes.',
'Complete named smallpayload,finiteRAW/LFpins andallownedmanifest. Leasefinal islastownedwrite; separate externalreadonly hash/count/terminalEXIT required.'
]
checks=[{'id':a['id'],'expected':a['check'],'status':'pass','finding':notes[i]} for i,a in enumerate(get(OWN/'preparation71.json')['expected_checks'])]
open_boundary=['Actual H,K,r_rho perturbation inputs and B27/B28/B4.','Weak H1/B2,dynamics,invariance,nonexplosion,B17 cost and estimates.','Implementation errors/caps,actual-input expected-query costs and PBPS/SPHMC composition.','Full PBPS/SPHMC results,GaussianCloud Section6 andmidpoint bounds/initialization.','Whole-paper Chapter1.3 ExpositionSeal,postmerge purification/PURIFIED,main/live andexisting four-paperGoal.']
decision={'schema':'repository-reader71-independent-scoped-decision-v1','actor':'/root/anonymous_decoder71','actual_decision_writer_PID':os.getpid(),'decision':['accept_scoped_aggregate','accept_scoped_reader'],'accept_scoped_aggregate':True,'accept_scoped_reader':True,'checked_science_commit':SCI,'reviewed_packet':pin(r/'final-reader-repository-packet71.json'),'blocking_findings':[],'required_repairs':[],'prepared13checks':checks,'source_credit':'Only reuse /root/independent_primary69 CLOSED277 unchanged source review via root adoption. No new source-fidelity verdict.','reused_native_counts':{'exactscience':116,'math':95,'source':277,'blind':10},'role_exposure':e['exposures'],'independent_fresh_gates':[{k:a[k] for k in ['label','actual_foreground_PID','exit_code','terminal_closed']} for a in fresh['checks']],'reused_root_terminal_gate_count':19,'reader_debt':v['reader_debt'],'remaining_truth_boundary':open_boundary,'whole_page_or_Goal_Exposition_Seal':False,'PURIFIED':False,'new_VERIFIED_or_SAU_claim':False,'main_live':False,'Goal_complete':False,'root_is_sole_canonical_writer':True,'native_current_pin_validators_rerun':False,'bounded_synthesis':'Exact SCI mathematics and accepted source/decoder bindings unchanged. Authorized finite shared aggregation,actual graph branch,lesson/fullProp/copy/download and actual10PNG pixels support only scoped aggregate and reader acceptance. Final127 inputs remain exact after fresh read-only gates; whole-paper mathematics and publication boundaries remainopen.'};dump('decision71.json',decision)
review='''Independent repository + scoped-reader71 review

Decision: accept_scoped_aggregate; accept_scoped_reader. Blocking findings: none. Required repairs: none.
SCI71=4e7ce5d2996ffe1d1b0ab570778e02425c6be34e.
Final packet RAW/LF=ce23377e2799a9617f19cf7bceefd69bc7b2078e47ad16a463a3950adb8cad06.

All127 final current inputs match RAW and CRLF-to-LF-only pins, rechecked after four independent read-only gates. Science module,publication,lesson andsemantic audit RAW are unchanged from SCI. Authorized Registry/import/Test519,cell sharedgate/visual/admin,handoff/execution/conversion/modulegraph differences are bounded and retain priorfrontiers. Native exactscience116,math95,source277,blind10 evidence reused. Sourcecredit only /root/independent_primary69; no old native current-pin validator rerun after administration.

Reader retains same C(u,v)=(norm(u)^2-norm(v)^2)/2-inner(A0(Inv u),v) and actual C(gP,gV)-C(fP,fV)=-norm(fP)^2+norm(fV)^2. Six callers,twelve witnesses,actual conditional/polar semantics andparent clauses persist. Eight formula/BODY steps cover377 lines of528-line module. Full119-line private Prop appears initiallyclosed adjacentproofhelper as representation,notproofprovider.14details startclosed.3callbackcopies+3RAWdownloads agree26489UTF8bytes;24587JScharacters is encodingcount.

All10 finalPNGpixels were actually viewed:statement,proof1..8,actualbranch. Actual graph labels1declares,2incomplete scannedreferences,1audit,1sourcecorrespondence; sourcegraph,wrappers andbuildcounts acquire no theoremcompletion. Fresh publication-reviewed51928,contributor51980,graph18740,site51600 allEXIT0. Reuse19rootterminalchecks,ASTISroot9181/Tests9481,224Python+6JS; no rebuild.

Dense inherited graphlabels,Unicode/underscore notation andlongscrolling remain readerdebt. Copy probes are isolated callbacks,notphysicalOSclipboard/live. ActualH/K/r_rho/B27/B28/B4,H1/B2/dynamics/invariance/nonexplosion,B17cost,errors/caps/expectedquerycost andcomposition remainopen. FullExposition/PURIFIED/main/live,wholepapers andfourpaperGoal remainopen.

Actor authored CLOSEDblind71 andlater CLOSEDsource-first72 andisnow source-exposed. This verdict adds no sourceblind/fidelity,SAU orVERIFIED credit. Root solecanonicalwriter. One local collector failed an unsupported121-line helper expectation; exactfailedhelper retained andactual119-line countcorrected before evidenceoutput. No input/science changed. One sealing-wrapper parsefailed before script/outputwrite; corrected quoting only.
'''
(OWN/'review71.RAW.utf8.txt').write_text(review,encoding='utf-8',newline='\n')
run={'schema':'reader71-native-scoped-run-v1','actor':'/root/anonymous_decoder71','actual_final_writer_PID':os.getpid(),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checked_science_commit':SCI,'reviewed_packet':pin(r/'final-reader-repository-packet71.json'),'decision':pin(OWN/'decision71.json'),'review':pin(OWN/'review71.RAW.utf8.txt'),'evidence':pin(OWN/'evidence71.json'),'visual_review':pin(OWN/'visual-review71.json'),'finite_inputs':pin(OWN/'input-manifest71.json'),'fresh_checks':pin(OWN/'fresh-checks71.json'),'status':'SCOPED_AGGREGATE_AND_READER_ACCEPTED_ONLY','whole_logical_recipe':'Canonical sorted compact ensure_ascii=False UTF8 JSON deleting ONLY top-level run_sha256; same-named nested fields remain.','canonical_Git_ledger_Goal_old_CLOSED_writes':0,'source_credit_actor':'/root/independent_primary69','source_or_VERIFIED_verdict':False};run['run_sha256']=sha(canonical(run));dump('review-run71.json',run)
payload={'schema':'reader71-small-complete-named-payload-v1','review_RAW_utf8_complete':review,'decision_complete':decision,'bounded_evidence_complete':e,'actual_pixel_review_complete':v,'finite_current_and_protocol_inputs_complete':finite,'fresh_terminal_checks_complete':fresh,'native_run_complete':run,'historical_native_payloads':'Exact finite pins/adoptions only; no recursive/base64 copies.'};dump('complete-named-review-decision-input-payload71.json',payload)
existing=sorted([a for a in OWN.rglob('*') if a.is_file()],key=lambda a:a.as_posix());assert not any(a.name in ['owned-manifest71.json','lease.final71.json'] for a in existing)
manifest={'schema':'reader71-owned-native-manifest-v1','owned_directory':OWN.as_posix(),'entry_count':len(existing),'owned_count_including_manifest_and_lease':len(existing)+2,'RAW_LF_recipe':'Exact RAW and ONLY byte CRLF to LF','self_hash_binding':'This manifest natively pinned by final CLOSED_LAST lease; no self-hash cycle.','entries':[pin(a) for a in existing]};dump('owned-manifest71.json',manifest)
bindings=[pin(a) for a in sorted(OWN.rglob('*'),key=lambda a:a.as_posix()) if a.is_file()]
lease={'schema':'reader71-native-final-lease-v1','status':'CLOSED_LAST','owned_directory':OWN.as_posix(),'actor':'/root/anonymous_decoder71','actual_last_writer_PID':os.getpid(),'terminal_exit_observed_externally_required':True,'expected_exit_code_after_last_write':0,'last_owned_write':'lease.final71.json','owned_count':len(bindings)+1,'bound_layer_count':len(bindings),'all_owned_outputs_except_only_self':bindings,'owned_manifest':pin(OWN/'owned-manifest71.json'),'complete_named_payload':pin(OWN/'complete-named-review-decision-input-payload71.json'),'whole_logical_run_sha256':run['run_sha256'],'reviewed_packet':pin(r/'final-reader-repository-packet71.json'),'decision':['accept_scoped_aggregate','accept_scoped_reader'],'no_more_owned_writes':True,'postclose_policy':'Separate external readonly native RAW/LF,finiteinput/exactcount verification; zeroownedwrites.','canonical_Git_ledger_Goal_old_CLOSED_writes':0,'source_credit_actor':'/root/independent_primary69','new_source_fidelity_or_VERIFIED':False};dump('lease.final71.json',lease)
print(json.dumps({'actual_last_writer_PID':os.getpid(),'EXIT':0,'status':'CLOSED_LAST','owned_count':lease['owned_count'],'bindings':len(bindings),'manifest_entries':manifest['entry_count'],'input_count':len(inputs),'native_run_sha256':run['run_sha256'],'lease':pin(LEASE),'manifest':pin(OWN/'owned-manifest71.json'),'complete_payload':pin(OWN/'complete-named-review-decision-input-payload71.json')},ensure_ascii=False))