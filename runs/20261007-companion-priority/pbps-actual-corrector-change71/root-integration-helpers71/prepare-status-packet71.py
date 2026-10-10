from pathlib import Path
import copy,hashlib,json,os,sys
root=Path.cwd();sys.path.insert(0,str(root/'tools'));import astis_semantic_roundtrip as rt
r=Path('runs/20261007-companion-priority/pbps-actual-corrector-change71');o=r/'reader-status-overlay71'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
q=load(o/'proposal.json');ap=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSActualCorrectorChange.json');audit=load(ap)
assert audit['state']=='blind-reconstructed' and audit['publication_binding_sha256']==q['old_publication_binding_sha256']
for i,z in enumerate(q['rows']):assert Path(z['path']).read_bytes()==(o/f'{i}.before.exactraw.json').read_bytes()
oldpacket=rt.semantic_reviewer_packet(audit);assert oldpacket==load(r/'source-review.packet.0.json')
proposed=copy.deepcopy(audit);proposed['publication_binding_sha256']=q['proposed_publication_binding_sha256'];packet=rt.semantic_reviewer_packet(proposed)
allowed={'publication_binding_sha256','packet_sha256'};assert {k:v for k,v in packet.items() if k not in allowed}=={k:v for k,v in oldpacket.items() if k not in allowed}
for name,x in [('audit.1.proposed.json',proposed),('source-review.packet.1.proposed.json',packet)]:
 p=o/name;assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
x=dict(status='PROPOSED_ONLY_CANONICAL_UNCHANGED',actual_root_PID=os.getpid(),proposal_RAW_sha256=sha((o/'proposal.json').read_bytes()),old_official_packet_sha256=oldpacket['packet_sha256'],proposed_official_packet_sha256=packet['packet_sha256'],changed_packet_fields=sorted(allowed),all_other_packet_fields_identical=True,new_decoder_not_needed=True,mathematical_change=False,approval=False)
p=o/'packet-mapping.json';assert not p.exists();p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf8',newline='\n')
print('PASS proposed official packet differs only in binding digest and own packet hash; canonical unchanged; independent approval pending.')
