from pathlib import Path
import base64,hashlib,json,os,subprocess,sys
r=Path('runs/20261007-companion-priority/pbps-clock-preproof75');out=r/'root-prereviews75';out.mkdir(exist_ok=False)
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest();can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def check(z):
 p=Path(z['path']);b=p.read_bytes();assert len(b)==z['RAW_bytes'] and sha(b)==z['RAW_sha256'] and sha(b.replace(b'\r\n',b'\n'))==z['LF_sha256'],p
 return b
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
def write(p,x):
 p=Path(p);assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def readonly(label,p,*args):
 with (out/(label+'.stdout.log')).open('wb') as s,(out/(label+'.stderr.log')).open('wb') as e:
  q=subprocess.Popen([sys.executable,'-B','-X','utf8',str(p),*args],stdout=s,stderr=e);code=q.wait()
 record=dict(actual_PID=q.pid,exit_code=code,terminal_closed=True,stdout=pin(out/(label+'.stdout.log')),stderr=pin(out/(label+'.stderr.log')));write(out/(label+'.receipt.json'),record);assert code==0;return record
s=r/'independent-source-baseline75';lp=s/'lease.final.json';assert sha(lp.read_bytes())=='82b6e38e8fa1a84317f99ed52454877b34aca14c653403d2c374b3e58a13a042'
l=load(lp);rows=l['all_owned_outputs_except_only_self'];assert l['status']=='CLOSED_LAST' and l['owned_count']==len(rows)+1==53 and not l['candidate75_header_seen'] and l['all_sessions_closed'] and not l['postclose_owned_writes']
assert {p.resolve() for p in s.rglob('*') if p.is_file()}=={Path(z['path']).resolve() for z in rows}|{lp.resolve()}
for z in rows:check(z);assert Path(z['path']).stat().st_mtime_ns<=lp.stat().st_mtime_ns
run=load(s/'run75.json');h=sha(can({k:v for k,v in run.items() if k!='run_sha256'}));assert h==run['run_sha256']==l['whole_logical_run_sha256']=='b562088f2b0a91b75079377c1b457efe4943eb7f666575ac29cb2e963f062f75'
named=load(l['complete_named_RAW_payload']['path']);assert check(l['complete_named_RAW_payload']) and l['complete_named_RAW_payload']['RAW_sha256']=='d152639c3456073e6f04b18cadfa5e53727e9ef3896c55a20536f2c71a836309'
assert named['named_payload_count']==len(named['named_payloads'])==5
for z in named['named_payloads']:assert check(z['pin'])==base64.b64decode(z['complete_RAW_base64'],validate=True)
im=load(run['input_manifest']['path']);check(run['input_manifest']);assert im['input_count']==len(im['inputs'])==22
for z in im['inputs']:check(z)
d=load(s/'decision75.json');assert d['future_candidate_not_seen'] and d['not_a_source_fidelity_verdict_on75'] and d['counts']['source_items']==137 and d['counts']['source_nodes']==32 and d['counts']['source_edges']==67
sr=readonly('source-baseline-readonly',s/'check75.py')
write(r/'root.source-baseline75.adoption.json',dict(status='ACCEPTED_CLOSED_SOURCE_FIRST_BASELINE75_ONLY',actual_root_PID=os.getpid(),native_lease=pin(lp),native_files=53,native_run_sha256=h,complete_named=l['complete_named_RAW_payload'],current_inputs=22,coverage=d['counts'],readonly=sr,source_before_header=True,header_acceptance=False,proof_search=False,new_SAU=False,Goal_complete=False))
m=r/'independent-header-math75';lp=m/'lease.final.json';assert sha(lp.read_bytes())=='56940689a9ee576c23f088e358719816511480af2082408a9eac2b750717da3a'
l=load(lp);check(l['manifest']);manifest=load(l['manifest']['path']);rows=manifest['entries'];assert l['status']=='CLOSED_LAST' and l['owned_files']==len(rows)+2==51 and not l['VERIFIED'] and sha(can(rows))==manifest['logical_entries_sha256']==l['closure_logical_sha256']
assert {p.resolve() for p in m.rglob('*') if p.is_file()}=={Path(z['path']).resolve() for z in rows}|{lp.resolve(),(m/'native.manifest.json').resolve()}
for z in rows:check(z);assert Path(z['path']).stat().st_mtime_ns<=lp.stat().st_mtime_ns
run=load(m/'run.json');h=sha(can({k:v for k,v in run.items() if k!='run_sha256'}));assert h==run['run_sha256']==l['run_sha256']=='fb9df7234894979ef3fced9d69fdfa70ee13bda105c0930d213e7e9999a3973b'
payload=load(run['complete_named']['path']);assert check(run['complete_named']) and run['complete_named']['RAW_sha256']=='e2442141e113a389dc8ece36cf8fb4cdf1163882c41a77f6f0845cda88e3e9ec'
im=load(run['inputs_manifest']['path']);check(run['inputs_manifest']);assert im==run['input_manifest']==payload['input_manifest'] and im['input_count']==len(im['inputs'])==14
for z in im['inputs']:assert check(z['original'])==check(z['snapshot'])
d=load(m/'decision.json');assert d==run['decision']==payload['decision'] and d['ten_conclusion_groups_mathematically_correct_after_exact_repair'] and d['further_mathematical_repair']==[] and not d['new_callers'] and d['no_EXCESS_new_premises'] and not d['source_final_acceptance']
assert payload['exact_original_header_UTF8'].encode()==check(d['original_header']) and payload['exact_v2_header_UTF8'].encode()==check(d['proposed_v2_header']) and payload['rigorous_named_review_UTF8'].encode()==check(run['named_review'])
assert (r/'header75.v2.proposed.lean').read_bytes()==check(d['proposed_v2_header'])
mr=readonly('header-math-readonly',m/'math75.py','readonly')
write(r/'root.math75.adoption.json',dict(status='ACCEPTED_CLOSED_V2_PROSPECTIVE_MATH_AND_TYPE_CONTRACT_ONLY',actual_root_PID=os.getpid(),native_lease=pin(lp),native_files=51,native_run_sha256=h,complete_named=run['complete_named'],current_inputs=14,readonly=mr,proposed_header=pin(r/'header75.v2.proposed.lean'),exact_API_overlay_pending_distinct_source=True,original_negative_Lean_PID=17592,v2_predicate_Lean_PID=17148,v2_full_telescope_Lean_PID=28408,actual_theorem_proof=False,Statement_Seal=False,new_SAU=False,Goal_complete=False))
assert not Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHazardClock.lean').exists()
write(out/'receipt.json',dict(status='SOURCE_BASELINE53_AND_HEADER_MATH51_ADOPTED_ONLY',actual_root_PID=os.getpid(),source=sr,math=mr,source_header_review_pending=True,Statement_Seal=False,proof_search=False,new_SAU=False,Goal_complete=False))
print('PASS75 CLOSED53 source-first and CLOSED51 v2 mathematical/type contracts adopted; distinct source-header review/seal/claim/proof remain pending.')
