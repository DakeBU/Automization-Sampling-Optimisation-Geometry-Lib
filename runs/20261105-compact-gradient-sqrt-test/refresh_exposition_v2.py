"""Pin one unaccepted exposition-only successor; preserve v1 review bytes."""
import hashlib
import json
from pathlib import Path
from tools import astis_publication as publication
from tools import astis_semantic_roundtrip_core as core

run=Path('runs/20261105-compact-gradient-sqrt-test')
old_report=run/'source-review.json'
old_raw=old_report.read_bytes()
assert hashlib.sha256(old_raw).hexdigest()=='74bc0c04e2b484ef722794f38c42827d825dabf824a73341570b45202d9baf0c'
path=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261105-CompactGradientSqrtTest.json')
audit=json.loads(path.read_text(encoding='utf-8'))
assert audit['state']=='blind-reconstructed' and audit['source_review']['state']=='pending'
assert audit['publication_binding_sha256']=='3443cb2d74ccc935fd8df4b91514126fbb5a4db71dbf7f43f6cd5ccdff0136a0'
item=json.loads(Path('website/content/publications/compact-gradient-sqrt-test.json').read_text(encoding='utf-8'))['items'][0]
binding=item['bindings'][0]
audit['publication_binding_sha256']=publication.binding_digest(item,binding)
audit['publication_context']=publication.review_context(item,binding)
core._write_packet(audit,str(path))
packet=core.semantic_reviewer_packet(audit)
output=run/'reviewer-input-v2.json';assert not output.exists()
core._write_packet(packet,str(output))
assert old_report.read_bytes()==old_raw
print(json.dumps({'reviewer_input':output.as_posix(),'packet_sha256':packet['packet_sha256'],
    'publication_binding_sha256':audit['publication_binding_sha256'],
    'change':'Only lesson step3 now says generally not compactly supported. No source/theorem/definition/test/code change; independent v2 review required.'}))
