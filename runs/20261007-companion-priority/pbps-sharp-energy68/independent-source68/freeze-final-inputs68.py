from pathlib import Path
import json,hashlib,os,datetime
R=Path('E:/Samplinglib');O=R/'runs/20261007-companion-priority/pbps-sharp-energy68/independent-source68';B=R/'runs/20261007-companion-priority/pbps-sharp-energy68'
def sha(b):return hashlib.sha256(b).hexdigest()
def write(n,o):(O/n).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
assert json.loads((O/'lease.open.json').read_text())['status']=='OPEN';assert not(O/'lease.final.json').exists();assert sha((O/'primary-first-expectations.json').read_bytes())=='ced1c679be92f94e8fa0edd8ed06935c5ef5dace0596f0e8b547a6d019afa997'
files=[B/f for f in ['source.0.reviewer-packet.json','source.1.reviewer-packet.json','source.consumer.reviewer-packet.json','consumer.semantic-audit68.blind.json','publication-plan.json']];files += [R/'lean-toolchain',R/'lake-manifest.json',R/'tools/astis_semantic_roundtrip_core.py']
entries=[];(O/'final-inputs').mkdir(exist_ok=True)
for i,p in enumerate(files):
 b=p.read_bytes();lf=b.replace(b'\r\n',b'\n').replace(b'\r',b'\n');a=f'final-inputs/{i:03d}.RAW.snapshot';z=f'final-inputs/{i:03d}.LF.snapshot';(O/a).write_bytes(b);(O/z).write_bytes(lf);entries.append({'path':p.relative_to(R).as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_bytes':len(lf),'LF_sha256':sha(lf),'raw_snapshot':a,'lf_snapshot':z})
write('final-inputs.initial.manifest.json',{'schema':1,'phase':'AFTER_ROOT_FINAL_INPUTS_READY68','actual_pid':os.getpid(),'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_expectations_precede_candidates':True,'entries':entries,'prior_source_expectations_SHA256':sha((O/'primary-first-expectations.json').read_bytes()),'prior_first_input_order_SHA256':sha((O/'first-input-order.json').read_bytes())})
for i in range(5):
 p=json.loads((O/entries[i]['raw_snapshot']).read_text());print('INPUT',i,'RAW',entries[i]['RAW_sha256'],'KEYS',list(p));print('SMALL_SCHEMA',{k:v for k,v in p.items() if k in ['audit_id','source','lean','original','reconstruction','publication_binding_sha256','publication_context','source_reviewer_packet_sha256','reviewer_packet_sha256'] and k!='publication_context'});print('CONTEXT_KEYS',list(p.get('publication_context',{})))
print('INITIAL_FINAL_INPUTS_FROZEN_EXIT_0',os.getpid(),len(entries))
