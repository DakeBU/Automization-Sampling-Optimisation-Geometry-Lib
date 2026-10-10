from pathlib import Path
import json,hashlib,datetime,sys
ROOT=Path('E:/Samplinglib');O=Path(__file__).parent
def canon(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 b=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'bytes':len(b),'raw_sha256':sha(b),'lf_sha256':sha(b.replace(b'\r\n',b'\n'))}
assert len(sys.argv)==2
inputs=json.loads((O/'input-verification.json').read_bytes());manifest=json.loads((O/'manifest.json').read_bytes());complete=json.loads((O/'complete.json').read_bytes())
for p in inputs['inputs']:
 for v in p.values():assert pin(ROOT/v['path'])==v
for v in manifest['outputs']:assert pin(ROOT/v['path'])==v
for f in ['input-verification.json','statement.review.json','reviewer.statement.run.json','manifest.json','complete.json']:
 v=json.loads((O/f).read_bytes());assert sha(canon({k:x for k,x in v.items() if k!='content_self_sha256'}))==v['content_self_sha256']
closed={'schema_version':1,'actor':'/root/next_primary56','status':'CLOSED','read_lease':'CLOSED','write_lease':'CLOSED','Python_lease':'CLOSED','compiler_lease':'NOT_STARTED_CLOSED','compiler_started':False,'closed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'original_open':pin(O/'lease.open.json'),'input_count':inputs['input_count'],'inputs':inputs['inputs'],'outputs':manifest['outputs']+[pin(O/'manifest.json'),pin(O/'complete.json')],'all_input_output_readbacks_actual_verified':True,'verdict':'ACCEPT_SCOPED_STATEMENT_ONLY','compiler_rerun_or_proof_or_sourcegraph_review':False,'process_evidence':{'actual_review_emission':{'chunk_id':sys.argv[1],'exit_code':0},'current_finalizer':'Synchronous Python, all handles closed before return, enclosing exec must observeEXIT0. This lease is final write LAST; no compiler, detached/background helper or process launched.'},'hash_recipe':'COMPLETE native object minus only content_self_sha256; UTF8 ensure_ascii=False sorted compact comma/colon JSON no newline. Raw/LF externally printed to avoid circular self raw hash. No named selected payload.'}
closed['content_self_sha256']=sha(canon(closed));p=O/'lease.json';p.write_bytes((json.dumps(closed,ensure_ascii=False,indent=2)+'\n').encode());j=json.loads(p.read_bytes());assert j==closed;assert sha(canon({k:v for k,v in j.items() if k!='content_self_sha256'}))==j['content_self_sha256'];print(json.dumps({'status':'CLOSED','lease':pin(p),'native_complete_self_sha256':j['content_self_sha256'],'input_count':inputs['input_count'],'output_count':len(closed['outputs']),'compiler':'NOT_STARTED_CLOSED'}))
