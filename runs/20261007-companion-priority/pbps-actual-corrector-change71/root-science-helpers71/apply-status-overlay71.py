from pathlib import Path
import hashlib,json,os,sys
root=Path.cwd();sys.path.insert(0,str(root/'tools'));import astis_publication as pub,astis_semantic_roundtrip as rt
r=Path('runs/20261007-companion-priority/pbps-actual-corrector-change71');o=r/'reader-status-overlay71'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
decision=r/'independent-source71/stageB.reader-status-overlay71.decision.json';assert sha(decision.read_bytes())=='1623f010364dda0cc38b19e8040859435539d9687c106e8198b9c5b1e514010c'
d=load(decision);assert d['decision']=='accept_exact_reader_status_overlay_only' and d['application_authorized_only_for_exact_three_proposed_RAW_hashes_and_derived_exact_audit_packet']
q=load(o/'proposal.json');assert sha((o/'proposal.json').read_bytes())==d['proposal']['RAW_sha256']=='baa9d0fc8bcacd071b3b9902b2dd0f8bf35fdf872497ee31d8b272e3443611bf'
ap=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSActualCorrectorChange.json');audit=load(ap)
assert rt.semantic_reviewer_packet(audit)==load(r/'source-review.packet.0.json') and audit['publication_binding_sha256']==d['binding_before']
for i,z in enumerate(d['three_exact_proposed_files']):
 assert Path(z['current_path']).read_bytes()==Path(z['before']['path']).read_bytes()
 assert sha(Path(z['proposed']['path']).read_bytes())==z['proposed']['RAW_sha256']==q['rows'][i]['proposed_RAW_sha256']
before=o/'audit.before.exactraw.json';assert not before.exists();before.write_bytes(ap.read_bytes())
for z in d['three_exact_proposed_files']:Path(z['current_path']).write_bytes(Path(z['proposed']['path']).read_bytes())
ap.write_bytes((o/'audit.1.proposed.json').read_bytes());audit=load(ap)
packet=rt.semantic_reviewer_packet(audit);assert packet==load(o/'source-review.packet.1.proposed.json') and packet['packet_sha256']==d['official_packet_proposed']
p=r/'source-review.packet.1.json';assert not p.exists();p.write_bytes((o/'source-review.packet.1.proposed.json').read_bytes())
pub.inputs.cache_clear();pub.load.cache_clear();item=load('website/content/publications/pbps-actual-corrector-change.json')['items'][0]
assert pub.binding_digest(item,item['bindings'][0],pub.inputs())==d['binding_proposed']==audit['publication_binding_sha256']
assert pub.review_context(item,item['bindings'][0],pub.inputs())==audit['publication_context']
decl=load(r/'claim.json')['target_declarations'];pub.check_advance(decl,reviewed=False)
x=dict(status='EXACT_INDEPENDENTLY_REVIEWED_READER_STATUS_OVERLAY_APPLIED_SOURCE_NATIVE_CLOSE_PENDING',actual_root_PID=os.getpid(),decision=pin(decision),proposal=pin(o/'proposal.json'),exact_three_current=[pin(z['current_path']) for z in d['three_exact_proposed_files']],audit=pin(ap),official1=pin(p),official_packet_sha256=packet['packet_sha256'],mathematical_context_unchanged=True,source_verdict=False,VERIFIED=False)
p=r/'root.reader-status-overlay71.adoption.json';assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
x=dict(status='FINAL_CURRENT71_OFFICIAL1_INPUTS_FROZEN_SOURCE_VERDICT_PENDING',packet=pin(r/'source-review.packet.1.json'),audit=pin(ap),source_body=pin(audit['lean']['file']),publication=pin('website/content/publications/pbps-actual-corrector-change.json'),lesson=pin('website/content/declaration_lessons/pbps-actual-corrector-change.json'),frontier=pin('research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-corrector-change.json'),source_review=False,VERIFIED=False)
p=r/'source-review.freeze71.v1.json';assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('PASS exact3 proposed RAW files and audit/official1 applied after independent48304 approval; only4 status fields; math/context/Lean/decoder unchanged; source CLOSE/VERIFIED pending.')
