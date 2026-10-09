from pathlib import Path
import json,hashlib,os,subprocess,datetime
ROOT=Path('E:/Samplinglib');R=ROOT/'runs/20261007-companion-priority/pbps-root-commutation67';O=R/'independent-repository-exposition67'
sha=lambda b:hashlib.sha256(b).hexdigest()
def cj(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def ld(p):return json.loads(Path(p).read_bytes())
def wr(n,x):
 assert not (O/'lease.final.json').exists();(O/n).write_bytes((json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode())
def pin(p):
 p=Path(p);b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return {'path':p.as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_bytes':len(l),'LF_sha256':sha(l)}
def vpin(x):
 p=Path(x['path']);a=pin(p);expect=x.get('RAW_sha256',x.get('raw_sha256'));assert a['RAW_sha256']==expect,p
 for key in ['RAW_bytes','raw_bytes','bytes']:
  if key in x:assert a['RAW_bytes']==x[key],p
 if x.get('LF_sha256',x.get('lf_sha256')):assert a['LF_sha256']==x.get('LF_sha256',x.get('lf_sha256')),p
 return a
commit='3da29415011a971a65f749502a625e416213f487';parent=subprocess.check_output(['git','rev-parse',commit+'^'],cwd=ROOT).decode().strip();assert parent=='eb3d5ffbb6853f2a0aa4a8c66aefce19d8050176'
adopts={k:ld(R/n) for k,n in [('source','root.source67.adoption.json'),('math','root.math67.adoption.json'),('decoder','root.decoder67.adoption.json'),('exact','root.exact-verification67.adoption.json')]};checks=[]
for kind,folder,listkey,countkey,runname in [('source','independent-source67','owned_files_except_this_final_lease','owned_file_count_including_self','review-run.json'),('math','independent-math67','all_owned_except_this_final_lease','final_owned_file_count','run.json'),('exact','exact-science-verification67','all_owned_except_final_lease','owned_file_count_including_lease','run.json')]:
 D=R/folder;lease=ld(D/'lease.final.json');assert lease['status']=='CLOSED_LAST';rows=lease[listkey];actual={p.relative_to(D).as_posix() for p in D.rglob('*') if p.is_file()};expected={Path(x['path']).relative_to(D).as_posix() for x in rows}|{'lease.final.json'};assert actual==expected and len(actual)==lease[countkey];stamp=(D/'lease.final.json').stat().st_mtime_ns
 for x in rows:vpin(x);assert Path(x['path']).stat().st_mtime_ns<=stamp
 run=ld(D/runname);r=dict(run);declared=r.pop('run_sha256');assert sha(cj(r))==declared==lease['whole_logical_run_sha256'];assert declared==adopts[kind]['native_whole_logical_run_sha256'];assert len(actual)==adopts[kind]['native_owned_files']
 if kind=='source':assert pin(D/'lease.final.json')['RAW_sha256']==adopts[kind]['native_lease']['RAW_sha256'];assert pin(D/'review-run.json')['RAW_sha256']==adopts[kind]['native_complete_RAW_review_sha256']
 if kind=='math':vpin(adopts[kind]['native_final_lease']);vpin(adopts[kind]['native_complete_named_RAW_payload'])
 if kind=='exact':assert pin(D/'lease.final.json')['RAW_sha256']==adopts[kind]['native_lease_RAW_sha256'];assert lease['exact_commit']==commit;assert adopts[kind]['native_verified'] and adopts[kind]['native_verifier']=='/root/exact_science63';assert adopts[kind]['proper_non_owner_transition']['actor']=='/root/exact_science63'
 checks.append({'kind':kind,'native_folder':D.as_posix(),'owned_files_verified':len(actual),'all_owned_bytes_and_LF_verified':True,'exhaustive_no_extra_owned_files':True,'postclose_mtime_last_lease':True,'whole_logical_run_sha256':declared,'whole_logical_hash_deletion':'ONLY top-level run_sha256','lease':pin(D/'lease.final.json'),'native_run':pin(D/runname),'proof_or_source_math_replay':False})
# Decoder original native scope is25;29 explicit root maps also include original anonymous inputs/parent lease.
a=adopts['decoder'];D=Path('E:/Samplinglib/.astis/decoder-67/independent');lease=ld(D/'lease.json');assert lease['status']=='CLOSED_LAST';closure=ld(D/'closure_manifest.json');expected={x['path'] for x in closure['artifacts']}|{'closure_manifest.json','lease.json'};actual={p.relative_to(D).as_posix() for p in D.rglob('*') if p.is_file()};assert actual==expected and len(actual)==a['native_owned_files']==25
for x in closure['artifacts']:assert pin(D/x['path'])['RAW_sha256']==x['raw_sha256'] and pin(D/x['path'])['RAW_bytes']==x['bytes']
for x in a['raw_snapshot_mappings']:vpin(x['original']);vpin(x['explicit_exact_raw_snapshot']);assert x['original']['raw_sha256']==x['explicit_exact_raw_snapshot']['raw_sha256']
run=ld(D/'final_run.json');r=dict(run);declared=r.pop('run_sha256');assert sha(cj(r))==declared==a['native_whole_run_sha256']==lease['run_sha256'];assert pin(D/'reconstruction_payload.json')['RAW_sha256']==a['native_complete_named_RAW_sha256'];assert pin(D/'closure_manifest.json')['RAW_sha256']==lease['closure_manifest_raw_sha256']
checks.append({'kind':'decoder','native_original_owned_files':25,'root_explicit_map_count':len(a['raw_snapshot_mappings']),'all_native_and_explicit_copy_RAW_LF_pins_verified':True,'whole_logical_run_sha256':declared,'lease':pin(D/'lease.json'),'named_RAW':pin(D/'reconstruction_payload.json'),'whole_logical_hash_deletion':'ONLY top-level run_sha256','blindness':{'source_text_visible':False,'source_identity_visible':False},'compiler_started':False})
# Exact Git science bytes remain pinned separately from evolving integration metadata.
paths=['AutoSamplingTheory/TechnicalLemmas/Measure/L2RealSquareCommute.lean','AutoSamplingTheory/ExampleCases/ProximalBPS/ActualRootCommutation.lean','Tests/ProximalBPSActualRootCommutation.lean']+[p+'/'+n+'.json' for p in ['website/content/publications','website/content/declaration_lessons'] for n in ['real-l2-positive-square-commutation','pbps-actual-root-inverse-commutation']]+['research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261009-RealL2PositiveSquareCommutation.json','research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261009-PBPSActualRootInverseCommutation.json']
science=[]
for i,n in enumerate(paths):
 gitraw=subprocess.check_output(['git','show',commit+':'+n],cwd=ROOT);current=(ROOT/n).read_bytes();assert gitraw==current,n;gp=O/('SCI67.%02d.Git.RAW.snapshot'%i);lp=O/('SCI67.%02d.Git.LF.snapshot'%i);gp.write_bytes(gitraw);lp.write_bytes(gitraw.replace(b'\r\n',b'\n'));science.append({'repository_path':n,'exact_commit':commit,'Git_RAW':pin(gp),'Git_LF':pin(lp),'current_pin_at_precheck':pin(ROOT/n),'current_equals_exact_Git_RAW':True})
wr('SCI67-native-immutable-precheck.json',{'schema':'repository67-exact-SCI-native-closure-precheck-v1','actual_PID':os.getpid(),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'SCI_commit':commit,'parent_INT66':parent,'closed_native_packages':checks,'nine_science_Lean_publication_lesson_audit_Git_bytes':science,'verified_nonowner_transition_PID':adopts['exact']['proper_non_owner_transition']['actual_transition_PID'],'final_metadata_or_reader_or_graph_acceptance':False,'await_explicit_final_inputs_ready':True,'canonical_Git_ledger_site_writes':False})
inputs=[]
for p in [R/'root.source67.adoption.json',R/'root.math67.adoption.json',R/'root.decoder67.adoption.json',R/'root.exact-verification67.adoption.json',R/'verified.json']+[R/d/'lease.final.json' for d in ['independent-source67','independent-math67','exact-science-verification67']]+[D/'lease.json']:
 i=len(inputs);b=p.read_bytes();rp=O/'inputs'/('%03d.RAW.snapshot'%i);lp=O/'inputs'/('%03d.LF.snapshot'%i);rp.write_bytes(b);lp.write_bytes(b.replace(b'\r\n',b'\n'));inputs.append({'original':pin(p),'RAW_snapshot':pin(rp),'LF_snapshot':pin(lp),'stage':'stable-SCI-native-binding-before-final-integration'})
wr('inputs.manifest.initial-SCI.json',{'schema':'repository67-finite-original-RAW-LF-map-v1','inputs':inputs})
wr('observer-negatives.initial.json',{'schema':'repository67-initial-observer-negatives-v1','overbroad_console_diff_display':{'tool_chunk':'c20238','typed':'observability/output scope; not integration or proof failure','details':'SCI commit includes many run evidence artifacts; unfiltered name-status output was truncated. Subsequent science checks use nine explicit Lean/publication/lesson/audit paths; no whole-history copy or directory exclusion used.'},'canonical_writes':False,'final_inputs_not_yet_ready':True})
print(json.dumps({'actual_PID':os.getpid(),'SCI_commit':commit,'native_counts':[262,164,25,102],'exact_Git_science_paths':len(science),'initial_finite_inputs':len(inputs),'status':'PASS_STABLE_SCI_PRECHECK_PENDING_FINAL_INTEGRATION_INPUTS'}))
