import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,hashlib,os
O=pathlib.Path(__file__).resolve().parent; R=O.parent
H=lambda b:hashlib.sha256(b).hexdigest()
C=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
freeze=json.loads((R/'source-review.freeze70.metadata-overlay1.json').read_bytes())
packet=json.loads((R/'source-review.packet.1.json').read_bytes())
inputs=[]
def snap(p,n):
 raw=p.read_bytes();lf=raw.replace(b'\r\n',b'\n');assert not (O/n).exists()
 (O/n).write_bytes(raw);(O/(n+'.LF')).write_bytes(lf)
 row={'original_path':str(p),'snapshot':n,'RAW_bytes':len(raw),'RAW_sha256':H(raw),'LF_snapshot':n+'.LF','LF_bytes':len(lf),'LF_sha256':H(lf),'LF_recipe':'replace ONLY CRLF with LF; preserve every other byte','original_mtime_ns':p.stat().st_mtime_ns};inputs.append(row);return row
snap(R/'source-review.packet.1.json','final70.official-source-review.packet.1.exactraw.json')
snap(R/'source-review.freeze70.metadata-overlay1.json','final70.official-source-review.freeze.metadata-overlay1.exactraw.json')
snap(R/'root.metadata-repair70.adoption.json','final70.root.metadata-repair.adoption.exactraw.json')
snap(R/'representation-metadata-repair70/proposal.json','final70.root.reader-metadata.proposal.exactraw.json')
for key in ['audit','source_body','publication','lesson','frontier']:
 row=freeze[key];p=pathlib.Path(row['path']);n='final70.'+key+('.exactraw.lean' if key=='source_body' else '.exactraw.json')
 q=snap(p,n);assert q['RAW_sha256']==row['raw_sha256'] and q['RAW_bytes']==row['raw_bytes']
 if key in ['source_body','lesson']:assert (O/n).read_bytes()==(O/('current70.'+key+('.exactraw.lean' if key=='source_body' else '.exactraw.json'))).read_bytes()
d=dict(packet);expected=d.pop('packet_sha256');assert H(C(d))==expected
assert packet['anti_anchoring']=={'prior_semantic_slots_included':False,'prior_deltas_included':False,'prior_verdict_included':False,'prior_repairs_included':False}
out={'schema':'independent-source70-final-metadata-overlay1-inputs-v1','actual_pid':os.getpid(),'inputs':inputs,'input_count':len(inputs),'official_packet_canonical_sha256':expected,'packet_id':packet['packet_id'],'publication_binding_sha256':packet['publication_binding_sha256'],'module_and_lesson_unchanged':True,'old_packet0_preserved':True,'no_source_math_or_Lean_change':True}
(O/'stageB.final-input-manifest.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(out,ensure_ascii=False));print('ADOPTION\n'+(O/'final70.root.metadata-repair.adoption.exactraw.json').read_text(encoding='utf-8'))
