from pathlib import Path
import copy, hashlib, json, os, sys
root=Path.cwd();sys.path.insert(0,'tools')
import astis_publication as pub, astis_semantic_roundtrip as rt
r=root/'runs/20261007-companion-priority/pbps-root-commutation67'
load=lambda p:json.loads(p.read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def pin(p):
 b=p.read_bytes();return dict(path=p.resolve().as_posix(),raw_bytes=len(b),raw_sha256=sha(b),lf_sha256=sha(b.replace(b'\r\n',b'\n')))
def write(p,x):
 assert not p.exists(),p
 p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def closed(folder,leasehash,count,rowskey,runfile,whole):
 d=r/folder;l=load(d/'lease.final.json');run=load(d/runfile)
 assert sha((d/'lease.final.json').read_bytes())==leasehash and l['status']=='CLOSED_LAST' and l['last_owned_write']
 files={p.relative_to(d).as_posix():p for p in d.rglob('*') if p.is_file()};rows=l[rowskey]
 names=set()
 for x in rows:
  p=Path(x['path']) if 'path' in x else d/x['name'];name=p.relative_to(d).as_posix();names.add(name);b=p.read_bytes()
  rawhash=x.get('raw_sha256',x.get('RAW_sha256'));rawlen=x.get('raw_bytes',x.get('RAW_bytes'))
  lf=b.replace(b'\r\n',b'\n')
  assert sha(b)==rawhash and len(b)==rawlen,name
  assert sha(lf)==x.get('lf_sha256',x.get('LF_sha256')) and len(lf)==x.get('lf_bytes',x.get('LF_bytes')),name
 assert set(files)==names|{'lease.final.json'} and len(files)==count
 assert (d/'lease.final.json').stat().st_mtime_ns>=max(p.stat().st_mtime_ns for p in files.values())
 assert sha(can({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']==l['whole_logical_run_sha256']==whole
 return d,l,run
od,ol,orr=closed('independent-attribution-overlay67','83c8b40b4b90dda7a5cfab108fe895d980a8f6a13204ab0770bbbcaac227118c',67,'owned_files_except_this_final_lease','review-run.json','2a304db0151148ae089cd6899096b73a21b40161332f904e22f09a075263e9a1')
md,ml,mr=closed('independent-math67','e98cc7a699edf6827583c6d40a00505445cd033588693788b152afddc9b66425',164,'all_owned_except_this_final_lease','run.json','aae02feef75125ca6f9b1bceba7c1c00300b41f347020ef0013831525b5131cb')
assert sha((md/'mathematical-review.named.raw.json').read_bytes())=='f36dbc2b0ff266839d4606ec66832e0e82d457ca41320b47047b52b17f5ceff5'
decision=load(od/'complete-RAW-decision.json')
assert sha((od/'complete-RAW-decision.json').read_bytes())=='7b629193956f8acccd1e06a58158ab1cf87ccb7f248065c89233dba6ece61084'
assert decision['verdict']=='APPROVE_EXACT_PROPOSED_ATTRIBUTION_OVERLAY_ONLY' and decision['source_mathematical_repair'] is False
pdir=r/'presentation-attribution-overlay67';proposal=load(pdir/'proposal.json')
assert sha((pdir/'proposal.json').read_bytes())=='61b585a8148530cd203ea28b33034b75c32ba02dc665c9f4f27a7f9de88b3088'
assert (r/'root.decoder67.adoption.json').exists()
dest=r/'applied-reviewed-attribution-overlay67';dest.mkdir(exist_ok=False);maps=[]
for i,row in enumerate(proposal['changes']):
 p=root/row['path'];b=p.read_bytes();before=load(pdir/row['before_snapshot']);after=load(pdir/row['after_snapshot'])
 assert sha((pdir/row['before_snapshot']).read_bytes())==row['before_raw_sha256']
 assert sha((pdir/row['after_snapshot']).read_bytes())==row['after_raw_sha256']
 (dest/f'{i}.current-before.exactraw.snapshot.json').write_bytes(b)
 if i<2:
  assert sha(b)==row['before_raw_sha256'];a=(pdir/row['after_snapshot']).read_bytes()
 else:
  current=json.loads(b)
  assert {k:v for k,v in current.items() if k not in ['state','reconstruction']}=={k:v for k,v in before.items() if k not in ['state','reconstruction']}
  assert current['state']=='blind-reconstructed'
  y=copy.deepcopy(current)
  for k in ['source','publication_binding_sha256','publication_context']:y[k]=after[k]
  assert y['reconstruction']==current['reconstruction'] and rt.decoder_packet(y)==rt.decoder_packet(current)
  a=(json.dumps(y,ensure_ascii=False,indent=2)+'\n').encode()
 p.write_bytes(a);(dest/f'{i}.current-after.exactraw.snapshot.json').write_bytes(a)
 maps.append(dict(canonical_path=row['path'],root_current_before=pin(dest/f'{i}.current-before.exactraw.snapshot.json'),root_current_after=pin(dest/f'{i}.current-after.exactraw.snapshot.json'),independently_approved_after=pin(pdir/row['after_snapshot']),decoder_state_preserved=(i==2)))
pub.inputs.cache_clear();pub.load.cache_clear();data=pub.inputs();item=next(x for x in pub.load() if x['id']=='pbps-actual-root-inverse-commutation');ap=root/proposal['changes'][2]['path'];audit=load(ap)
assert pub.binding_digest(item,item['bindings'][0],data)==audit['publication_binding_sha256']==proposal['proposed_binding']==decision['publication_binding_proposed_after']
oldpacket=r/'source.1.reviewer-packet.json';(dest/'source.1.before-overlay.reviewer-packet.exactraw.snapshot.json').write_bytes(oldpacket.read_bytes())
oldpacket.write_text(json.dumps(rt.semantic_reviewer_packet(audit),ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
write(r/'root.attribution-overlay67.adoption.json',dict(status='INDEPENDENTLY_APPROVED_ATTRIBUTION_ONLY_OVERLAY_APPLIED',actual_root_writer_pid=os.getpid(),reviewer='/root/independent_source64',native_whole_logical_run_sha256=orr['run_sha256'],native_owned_files=67,native_final_lease=pin(od/'lease.final.json'),native_complete_decision=pin(od/'complete-RAW-decision.json'),finite_application_maps=maps,final_binding=audit['publication_binding_sha256'],Lean_headers_BODY_private_values_unchanged=True,decoder_packet_unchanged=True,source_mathematical_repair=False,final_whole_module_source_review_pending=True))
write(r/'root.math67.adoption.json',dict(status='INDEPENDENT_MATHEMATICS67_ACCEPTED_ATTRIBUTION_RESOLVED_SEPARATELY_SOURCE_PENDING',actual_read_only_adopter_pid=os.getpid(),native_owned_files=164,native_whole_logical_run_sha256=mr['run_sha256'],native_final_lease=pin(md/'lease.final.json'),native_complete_named_RAW_payload=pin(md/'mathematical-review.named.raw.json'),native_mathematical_verdict=ml['mathematical_verdict'],finite_label_maps='retrieval-label-metadata67/repair.json',finite_decoder_maps='root.decoder67.adoption.json',separate_reviewed_attribution_resolution='root.attribution-overlay67.adoption.json',final_source_verdict=False,VERIFIED_transition=False,whole_paper_complete=False))
print('PASS independent closed overlay67(67 files) and math67(164 files); exact reviewed phrase applied, decoder preserved, final source packet refreshed.')
