from pathlib import Path
import json,hashlib,datetime,sys
ROOT=Path('E:/Samplinglib');O=Path(__file__).parent
def canon(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 b=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'bytes':len(b),'raw_sha256':sha(b),'lf_sha256':sha(b.replace(b'\r\n',b'\n'))}
assert len(sys.argv)==2
inputs=json.loads((O/'input-manifest.json').read_bytes());manifest=json.loads((O/'manifest.json').read_bytes());complete=json.loads((O/'complete.json').read_bytes())
for v in [inputs,manifest,complete]:assert sha(canon({k:x for k,x in v.items() if k!='content_self_sha256'}))==v['content_self_sha256']
for receipt in inputs['inputs']+manifest['outputs']:
 actual=pin(ROOT/receipt['path']);assert actual==receipt
outputpins=manifest['outputs']+[pin(O/'manifest.json'),pin(O/'complete.json')]
closed={'schema_version':1,'actor':'/root/next_primary56','status':'CLOSED','read_lease':'CLOSED','write_lease':'CLOSED','Python_lease':'CLOSED','compiler_lease':'NOT_STARTED_CLOSED','compiler_started':False,'closed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'original_open':pin(O/'lease.open.json'),'inputs':inputs['inputs'],'outputs':outputpins,'exact_native_input_count':inputs['input_count'],'all_input_and_output_readbacks_verified':True,'candidate57_math_proof_exposure':'NONE','no_candidate_statement_or_SAU_claim_or_proof':True,'previous56_finalpacket_body_exposure':'Historical disclosed; no57 body exists/read; no hypothetical Gamma-resolvent theorem admitted.','process_evidence':{'primary_freeze':{'chunk_id':'56566b','exit_code':0},'public_contract_and_blueprint':{'chunk_id':'af7197','exit_code':0},'seal':{'chunk_id':sys.argv[1],'exit_code':0},'finalizer':'This synchronous Python process writes final lease LAST then actual readback, and enclosing tool must observe EXIT0. No compiler, helpers, detached or background processes; handles closed after each operation.'},'hash_contract':'Complete native object minus only content_self_sha256; UTF8 ensure_ascii=False sorted compact JSON comma/colon no newline. No named-payload subset. Raw/LF finallease hashes external after readback to avoid circularity.','formal_source_math_admission':False,'scope':'Independent exact primary-first source contract and reuse blueprint only; all sourceweakH1/Gamma/root/inverse/halfturn/main/cost/composition residuals preserved.'}
closed['content_self_sha256']=sha(canon(closed));p=O/'lease.json';p.write_bytes((json.dumps(closed,ensure_ascii=False,indent=2)+'\n').encode());j=json.loads(p.read_bytes());assert j==closed;assert sha(canon({k:v for k,v in j.items() if k!='content_self_sha256'}))==j['content_self_sha256']
print(json.dumps({'status':'CLOSED','lease':pin(p),'complete_self_sha256':j['content_self_sha256'],'input_count':inputs['input_count'],'output_count':len(outputpins),'compiler':'NOT_STARTED_CLOSED'}))
