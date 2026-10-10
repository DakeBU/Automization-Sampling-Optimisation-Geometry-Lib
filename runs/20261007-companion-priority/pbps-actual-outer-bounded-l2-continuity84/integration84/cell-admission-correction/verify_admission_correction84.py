"""Validate native review without changing its frozen commit helper."""
from pathlib import Path
import hashlib,json
out=Path(__file__).parent
review=out/'independent-repair/closed-RAW-manifest.json'
assert hashlib.sha256(review.read_bytes()).hexdigest()=='1014ecd79685ef9ccd74fd40c7333ba5e7767967a484e444967a5a3d9bac59ce'
assert hashlib.sha256((out/'independent-repair/decision.json').read_bytes()).hexdigest()=='2a2c001e457212144119d29ffea73b980bcf19e6fe3e38f930339a5c6e453aa7'
manifest=json.loads(review.read_bytes())
entries=manifest['frozen_current_inputs']+manifest['owned_artifacts']
for entry in entries:
 raw=Path(entry['path']).read_bytes()
 assert hashlib.sha256(raw).hexdigest()==entry['RAW_sha256'],entry['path']
 assert len(raw)==entry['RAW_bytes'],entry['path']
p=out/'root-native-review-validation.json';assert not p.exists()
p.write_text(json.dumps(dict(status='PASS',entries_checked=len(entries),manifest_RAW_sha256=hashlib.sha256(review.read_bytes()).hexdigest(),prior_guard_failure='An attempted in-helper validation changed the already reviewed helper RAW. Guard rejected before staging; helper restored exactly and all native inputs now rehashed externally.',no_native_review_changed=True,no_staging_on_failed_guard=True),indent=2)+'\n',encoding='utf8',newline='\n')
print('All',len(entries),'native RAW pins PASS; reviewed helper restored exact')
