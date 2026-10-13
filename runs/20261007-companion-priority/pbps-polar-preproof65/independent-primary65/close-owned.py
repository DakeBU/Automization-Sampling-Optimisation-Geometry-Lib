import os,json,hashlib,datetime
from pathlib import Path
O=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def load(n):return json.loads((O/n).read_text(encoding='utf-8-sig'))
def write(n,v):(O/n).write_bytes((json.dumps(v,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode())
assert not (O/'lease.final.json').exists()
fr=load('foreground-finalizer.receipt.json');rr=load('foreground-readback.receipt.json');assert fr['exit_code']==rr['exit_code']==0 and fr['foreground_waited'] and rr['foreground_waited'];assert fr['pid']!=rr['pid']
r=load('review-run.json');v=dict(r);del v['run_sha256'];assert sha(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())==r['run_sha256'];rb=load('raw-review-binding.json');assert sha((O/'review-run.json').read_bytes())==rb['raw_sha256']
files=[]
for p in sorted(O.iterdir()):
 assert p.is_file(),'No hidden directory outside full manifest'
 b=p.read_bytes();lf=b.replace(b'\r\n',b'\n').replace(b'\r',b'\n');files.append({'filename':p.name,'raw_bytes':len(b),'raw_sha256':sha(b),'lf_bytes':len(lf),'lf_sha256':sha(lf)})
m={'schema':'primary65-full-owned-manifest-v1','all_preclosure_owned_files':files,'preclosure_file_count':len(files),'final_owned_file_count':len(files)+2,'closure_files':[{'filename':'owned-manifest.json','role':'this complete manifest; exact RAW/LF bytes externally pinned by postclose terminal readback, not self-hashed'},{'filename':'lease.final.json','role':'final owned write; exact RAW/LF bytes externally pinned by postclose terminal readback; pins manifest RAW hash'}],'all_negative_files_included':True,'complete_raw_review':rb,'finalization_receipts':{'finalizer_pid':fr['pid'],'readback_pid':rr['pid'],'both_exit_code':0},'close_pid':os.getpid(),'status_at_manifest':'READY_TO_CLOSE'}
write('owned-manifest.json',m)
lease={'schema':'primary65-owned-lease-v1','status':'CLOSED_LAST','owner':'/root/independent_source64','owned_root':O.as_posix(),'closed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_close_pid':os.getpid(),'actual_close_parent_pid':os.getppid(),'actual_finalizer_pid':fr['pid'],'actual_readback_pid':rr['pid'],'finalizer_and_readback_exit_code':0,'run_sha256':r['run_sha256'],'complete_RAW_REVIEW_sha256':rb['raw_sha256'],'owned_manifest_raw_sha256':sha((O/'owned-manifest.json').read_bytes()),'final_owned_file_count':len(files)+2,'this_is_last_owned_write':True,'postclose':'READ_ONLY_NO_OWNED_WRITES'}
write('lease.final.json',lease)
print(json.dumps({'status':'CLOSED_LAST','close_pid':os.getpid(),'close_parent_pid':os.getppid(),'files':len(files)+2,'manifest_RAW_sha256':sha((O/'owned-manifest.json').read_bytes()),'lease_RAW_sha256':sha((O/'lease.final.json').read_bytes()),'run_sha256':r['run_sha256'],'complete_RAW_REVIEW_sha256':rb['raw_sha256']},sort_keys=True))
