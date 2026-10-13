import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,hashlib,os,datetime
O=pathlib.Path(__file__).resolve().parent
R=O.parent
H=lambda b:hashlib.sha256(b).hexdigest()
C=lambda v:json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
J=lambda p:json.loads(p.read_bytes())
def save(n,v):
 p=O/n;assert not p.exists();p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def snapshot(path,name,expected=None):
 raw=path.read_bytes();lf=raw.replace(b'\r\n',b'\n');assert expected is None or H(raw)==expected
 p=O/name;assert not p.exists();p.write_bytes(raw);(O/(name+'.LF')).write_bytes(lf)
 return {'original_path':str(path),'snapshot':name,'RAW_bytes':len(raw),'RAW_sha256':H(raw),'LF_snapshot':name+'.LF','LF_bytes':len(lf),'LF_sha256':H(lf),'LF_recipe':'replace ONLY CRLF with LF; preserve other bytes','original_mtime_ns':path.stat().st_mtime_ns}
freeze=J(R/'source-review.freeze70.json');packet=J(R/'source-review.packet.0.json')
inputs=[snapshot(R/'source-review.packet.0.json','current70.official-source-review.packet.0.exactraw.json',freeze['packet']['raw_sha256']),snapshot(R/'source-review.freeze70.json','current70.official-source-review.freeze.exactraw.json','a1ec5505ecabd84bf26b11030f37ac4441e3f2134b1eb9ca0517e7458d67b9e8')]
for key in ['audit','source_body','publication','lesson','frontier']:
 row=freeze[key];p=pathlib.Path(row['path']);n='current70.'+key+('.exactraw.lean' if key=='source_body' else '.exactraw.json');inputs.append(snapshot(p,n,row['raw_sha256']));assert inputs[-1]['RAW_bytes']==row['raw_bytes']
for p,n in [(R/'root.named-literal70.adoption.json','current70.named-literal.adoption.exactraw.json'),(R/'reader-helper-contract70/repair.notes.json','current70.reader-helper.repair.notes.exactraw.json'),(pathlib.Path('E:/Samplinglib/tools/inline_lean.py'),'current70.inline_lean.exactraw.py'),(pathlib.Path('E:/Samplinglib/tools/check_cross_domain_browser.py'),'current70.check_cross_domain_browser.exactraw.py')]:inputs.append(snapshot(p,n))
expected=packet['packet_sha256'];d=dict(packet);d.pop('packet_sha256');assert H(C(d))==expected
assert packet['anti_anchoring']=={'prior_semantic_slots_included':False,'prior_deltas_included':False,'prior_verdict_included':False,'prior_repairs_included':False}
assert packet['lean']['compiled'] is True
save('stageB.current-input-manifest.json',{'schema':'source70-stageB-official-fixed-current-inputs-v1','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_pid':os.getpid(),'StageA_expectation_RAW_sha256':H((O/'stageA.source-expectations70.before-current-BODY.frozen.json').read_bytes()),'StageA_was_frozen_before_this_BODY_read':True,'official_packet_canonical_sha256':expected,'inputs':inputs,'input_count':len(inputs),'no_compile_run_by_reviewer':True})
print(json.dumps({'actual_pid':os.getpid(),'packet_id':packet['packet_id'],'packet_canonical_sha256':expected,'packet_RAW_sha256':inputs[0]['RAW_sha256'],'packet_keys':list(packet),'blind_reconstruction_keys':list(packet['blind_reconstruction']),'publication_context_keys':list(packet.get('publication_context',{})),'audit_keys':list(J(O/'current70.audit.exactraw.json')),'input_count':len(inputs),'module_lines':len((O/'current70.source_body.exactraw.lean').read_bytes().splitlines()),'module_RAW_sha256':freeze['source_body']['raw_sha256']},ensure_ascii=True))
print('READ reader-helper repair notes\n'+(O/'current70.reader-helper.repair.notes.exactraw.json').read_text(encoding='utf-8'))
print('READ source_body lines1-200\n'+'\n'.join(str(i+1)+': '+s for i,s in enumerate((O/'current70.source_body.exactraw.lean').read_text(encoding='utf-8').splitlines()) if i<200))
