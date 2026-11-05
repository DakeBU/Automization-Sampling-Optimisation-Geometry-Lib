"""Admit actual independently owned evidence; never invent a review verdict."""
import hashlib
import json
from pathlib import Path
from tools import astis_publication as publication
from tools import astis_semantic_roundtrip_core as core

run=Path('runs/20261105-compact-gradient-sqrt-test')
path=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261105-CompactGradientSqrtTest.json')
draft=json.loads(path.read_text(encoding='utf-8'))
assert draft['state']=='blind-reconstructed' and draft['source_review']['state']=='pending'
packet_path=run/'reviewer-input-v2.json';packet=json.loads(packet_path.read_text(encoding='utf-8'))
report_path=run/'source-review-v2.json';report=json.loads(report_path.read_text(encoding='utf-8'))
assert hashlib.sha256(report_path.read_bytes()).hexdigest()=='375fc89fb02e9fbf83db1b6b071fd8b58d8e6d98b1cca5b05cce7c0b4ba1f72f'
assert report['reviewer']=='agent-task:/root/compact_sqrt_source_review_20261105'
assert report['independent_from_formalizer'] and report['independent_from_decoder']
assert report['reviewer_packet_sha256']==packet['packet_sha256']=='498bf99aead16c68c1849b3fcba8ceb22bf6f0d78bc4ee7dc9ae6a1d132448bc'
assert report['review_run_sha256']==core.sha256_json({k:v for k,v in report.items() if k!='review_run_sha256'})
assert report['verdict']=='equivalent-after-elaboration' and report['deltas']==[] and report['repairs']==[]
assert core.semantic_reviewer_packet(draft)==packet
item=json.loads(Path('website/content/publications/compact-gradient-sqrt-test.json').read_text(encoding='utf-8'))['items'][0]
assert publication.binding_digest(item,item['bindings'][0])==draft['publication_binding_sha256']=='5faadaee8e1beebd664c5edeee15375b52fba6b6d6647b637ae074e1a620cbbc'
fragment={'kind':'artifact-backed-audit','id':draft['id'],'state':'accepted',
    'reviewer_packet':packet_path.as_posix(),'decoder_packet':'runs/blind/ASTIS-BLIND-02ab380e11d7f911.json',
    'decoder_result':'runs/blind/ASTIS-BLIND-02ab380e11d7f911.result.json',
    'review_result':report_path.as_posix()}
core._write_packet(fragment,str(path))
publication.check_advance([item['bindings'][0]['declaration']],reviewed=True)
print('Actual v2 independent source/code/exposition review attached; target admission passes. No VERIFIED transition.')
