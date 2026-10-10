from pathlib import Path
import json, hashlib, copy, sys, re
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path('E:/Samplinglib')
R=ROOT/'runs/20261007-companion-priority/pbps-rough-mean-gradient56'
O=R/'source-review56'
def sha(b): return hashlib.sha256(b).hexdigest()
def canon(v): return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def receipt(p):
    b=p.read_bytes(); return {'path':p.relative_to(ROOT).as_posix(),'bytes':len(b),'raw_sha256':sha(b),'lf_sha256':sha(b.replace(b'\r\n',b'\n'))}
def save(name,v):
    p=O/name;p.write_bytes((json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode()); assert json.loads(p.read_bytes())==v; return receipt(p)
lease=json.loads((O/'initial-source-lease.raw.snapshot.json').read_bytes())
assert len(lease['input_artifacts'])==432
inputs=[]; snapshots=O/'inputs';snapshots.mkdir(exist_ok=True)
for i,pin in enumerate(lease['input_artifacts']):
    p=ROOT/pin['path']; b=p.read_bytes(); actual=receipt(p)
    assert all(actual[k]==pin[k] for k in ['bytes','raw_sha256','lf_sha256']), (i,pin,actual)
    raw=snapshots/f'{i:03}.exactraw.snapshot'; lf=snapshots/f'{i:03}.crlf-to-lf.snapshot'
    raw.write_bytes(b);lf.write_bytes(b.replace(b'\r\n',b'\n'))
    assert raw.read_bytes()==b and lf.read_bytes()==b.replace(b'\r\n',b'\n')
    inputs.append({'ordinal':i,'input':actual,'exactraw_snapshot':receipt(raw),'crlf_to_lf_snapshot':receipt(lf)})
packet=json.loads((R/'source.0.reviewer-packet.json').read_bytes())
assert sha(canon({k:v for k,v in packet.items() if k!='packet_sha256'}))==packet['packet_sha256']==lease['reviewer_packet_sha256']
for obj,key,hashkey in [(packet['source'],'original_text','text_sha256'),(packet['lean'],'statement','statement_sha256'),(packet['blind_reconstruction'],'text','text_sha256')]: assert sha(obj[key].encode())==obj[hashkey]
pub=json.loads((ROOT/'website/content/publications/pbps-rough-mean-gradient.json').read_bytes())['items'][0]
lessonfile=json.loads((ROOT/'website/content/declaration_lessons/pbps-rough-mean-gradient.json').read_bytes())
units=lessonfile.get('units',lessonfile.get('lessons',[]));assert len(units)==1
context=packet['candidate_publication_context']; payload=copy.deepcopy(context);del payload['candidate_assumptions'];payload['lesson']=units[0]
binding=pub['bindings'][0];payload['binding']={k:v for k,v in binding.items() if k not in ['audit_id','legacy_audit_debt']}
assert sha(canon(payload))==packet['publication_binding_sha256']
module=(ROOT/packet['lean']['file']).read_text(encoding='utf-8');assert module==context['current_lean_module'];assert sha(module.encode())==context['file']
start=module.index('theorem actual_rough_mean_gradient');end=module.index(':= by',start)
header=module[start:end];(O/'production.header.lf.snapshot.lean').write_text(header,encoding='utf-8',newline='\n')
prospective=(ROOT/'runs/20261007-companion-priority/pbps-rough-mean-gradient-preproof56/prospective-statement.txt').read_bytes().replace(b'\r\n',b'\n')
assert len(prospective)==1755 and sha(prospective)=='fea2c3ade170bc0526d659f8c51abedaa0ce1a6186e75f0d8a2532b6608e94d8'
assert (header.rstrip()+'\n').encode()==prospective
(O/'production.header.seal.normalized.lf.snapshot.lean').write_bytes((header.rstrip()+'\n').encode())
for parent in ['SourceMeanGradientDomain','L2MacroscopicMean','MacroscopicEnergy']:
    source=(ROOT/f'AutoSamplingTheory/ExampleCases/ProximalBPS/{parent}.lean').read_text(encoding='utf-8')
    name={'SourceMeanGradientDomain':'literal_source_mean_in_closed_gradient','L2MacroscopicMean':'actual_macroscopic_l2_mean','MacroscopicEnergy':'actual_macroscopic_gradient_energy_blocks'}[parent]
    a=source.index('theorem '+name); b=source.index(':= by',a);h=source[a:b]
    (O/f'{parent}.header.lf.snapshot.lean').write_text(h,encoding='utf-8',newline='\n')
    old=(ROOT/f'runs/20261007-companion-priority/pbps-rough-mean-gradient-sourcegraph56/{name}.lf.contract.lean').read_text(encoding='utf-8')
    assert h.strip()==old.strip(),parent
test=(ROOT/'Tests/ProximalBPSRoughMeanGradient.lean').read_text(encoding='utf-8')
for m in re.finditer(r'theorem\s+(\w+)',test):
    h=test[m.start():test.index(':= by',m.start())];(O/f'{m.group(1)}.header.lf.snapshot.lean').write_text(h,encoding='utf-8',newline='\n')
save('input-verification.json',{'schema_version':1,'status':'PASS','exact_input_count':432,'packet_complete_minus_packet_sha256':packet['packet_sha256'],'publication_binding_sha256':packet['publication_binding_sha256'],'header1755_sha256':sha(prospective),'inputs':inputs,'hash_recipe':'Raw bytes and CRLF-to-LF bytes; complete packet minus only packet_sha256. Publication binding includes whole lesson and complete binding minus audit_id/legacy_audit_debt, as native binding_payload does.'})
# The malformed native lease stays untouched. A virtual copy is used ONLY to check exact locator operations.
overlay=json.loads((R/'decoder-locator-repair56/overlay.json').read_bytes())
native=json.loads((R/'anonymous-decoder/lease.json').read_bytes()); run=json.loads((R/'anonymous-decoder/run.json').read_bytes()); result=json.loads((R/'anonymous-decoder/result0.json').read_bytes())
assert sha(canon({k:v for k,v in native.items() if k!='closure_record_sha256'}))==native['closure_record_sha256']
assert sha(canon({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']==result['decoder_run_sha256']
assert sha(canon(result))==native['output_artifacts'][1]['native_complete_sha256']
assert result['reconstructed_theorem_text']==packet['blind_reconstruction']['text']
assert sha(result['reconstructed_theorem_text'].encode())==result['reconstructed_text_sha256']
dp=json.loads((R/'anonymous-decoder/packet0.json').read_bytes());assert sha(canon({k:v for k,v in dp.items() if k!='packet_sha256'}))==dp['packet_sha256']==packet['blind_reconstruction']['decoder_packet_sha256']
assert not run['source_text_visible'] and not native['source_text_visible']
assert json.loads((R/'anonymous-decoder/initial-lease.raw.snapshot.json').read_bytes())['status']=='OPEN'
virtual=copy.deepcopy(native); operations=[]
def walk(v,pointer):
    tokens=pointer.strip('/').split('/');obj=v
    for t in tokens[:-1]: obj=obj[int(t)] if isinstance(obj,list) else obj[t]
    last=int(tokens[-1]) if isinstance(obj,list) else tokens[-1];return obj,last
malformed=[]
def find(v,path=''):
    if isinstance(v,dict):
        if set(v)=={'Length'}: malformed.append(path)
        else:
            for k,x in v.items():find(x,path+'/'+k)
    elif isinstance(v,list):
        for i,x in enumerate(v):find(x,path+'/'+str(i))
find(native)
assert len(malformed)==6 and set(malformed)=={x['pointer'] for x in overlay['operations']}
for op in overlay['operations']:
    obj,key=walk(virtual,op['pointer']);assert obj[key]==op['before'];assert len(op['after'])==op['before']['Length']
    actual=receipt(ROOT/op['actual_artifact']['path']);assert all(actual[k]==op['actual_artifact'][k] for k in ['bytes','raw_sha256','lf_sha256'])
    assert (ROOT/op['actual_artifact']['path']).read_bytes()==(R/'anonymous-decoder'/Path(op['actual_artifact']['path']).name).read_bytes()
    pointer=op['pointer']
    if pointer=='/original_open_lease_mapping/original_path': assert op['after']==run['open_lease_input_preserved_as']['original_path']
    elif pointer=='/original_open_lease_mapping/preserved_path': assert op['after']==run['open_lease_input_preserved_as']['preserved_path']
    elif pointer=='/input_artifacts/0/path': assert op['after']==run['inputs'][0]['path']
    elif pointer=='/input_artifacts/1/path': assert op['after']==run['inputs'][2]['path']
    else: assert op['after'] in run['outputs']
    obj[key]=op['after'];operations.append({'pointer':pointer,'before':op['before'],'after':op['after'],'actual':actual})
originals=[]
for name in ['packet0.json','result0.json','run.json','lease.json','initial-lease.raw.snapshot.json']:
    a=ROOT/'.astis/decoder-56'/name;b=R/'anonymous-decoder'/name;assert a.read_bytes()==b.read_bytes();originals.append({'original':receipt(a),'preserved':receipt(b)})
assert native['status']=='CLOSED' and native['compiler_lease']=='NOT_STARTED_CLOSED'
save('decoder-locator-verification.json',{'schema_version':1,'status':'PASS_EXACT_SIX_LOCATOR_OPERATIONS_ONLY','operations':operations,'unchanged_originals':originals,'native_complete_run_sha256':run['run_sha256'],'native_complete_closure_sha256':native['closure_record_sha256'],'native_complete_result_sha256':sha(canon(result)),'source_text_visible':False,'strict_identity_blindness':False,'original_lease_malformed_locators':malformed,'original_lease_remains_native_closed_bytes':True,'opening_snapshot_actual_status':'OPEN','original_open_input_semantics':'run inputs[1] names original lease path but pins initial OPEN bytes; exact preserved snapshot supplies these, not current CLOSED bytes.','mathematics_or_source_or_reconstruction_change':False})
print(json.dumps({'status':'PASS','pins':432,'header':len(prospective),'locator_operations':len(operations),'packet':packet['packet_sha256'],'publication':packet['publication_binding_sha256']}))
