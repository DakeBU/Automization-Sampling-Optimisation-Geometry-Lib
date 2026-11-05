"""Attach the independent unchanged reconstruction; no source verdict."""
import json
from pathlib import Path
from tools import astis_semantic_roundtrip_core as core

path=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261105-CompactGradientSqrtTest.json')
audit=json.loads(path.read_text(encoding='utf-8'))
report_path=Path('runs/blind/ASTIS-BLIND-02ab380e11d7f911.result.json')
report=json.loads(report_path.read_text(encoding='utf-8'))
assert audit['state']=='draft' and audit['source_review']['state']=='pending'
assert report['decoder']=='agent-task:/root/blind_02ab380e11d7f911'
assert report['source_text_visible'] is False
assert report['packet_sha256']==core.decoder_packet(audit)['packet_sha256']
assert report['reconstructed_text_sha256']==core.sha256_text(report['reconstructed_theorem_text'])
assert report['decoder_run_sha256']==core.sha256_json({k:v for k,v in report.items() if k!='decoder_run_sha256'})
audit['state']='blind-reconstructed'
audit['reconstruction']={'text':report['reconstructed_theorem_text'],
    'text_sha256':report['reconstructed_text_sha256'],'decoder':report['decoder'],
    'source_text_visible':False,'decoder_run_sha256':report['decoder_run_sha256'],
    'decoder_packet_sha256':report['packet_sha256'],'lean_statement_sha256':audit['lean']['statement_sha256'],
    'input_artifacts':report['input_artifacts'],'run_artifact':report_path.as_posix()}
core._write_packet(audit,str(path))
output=Path('runs/20261105-compact-gradient-sqrt-test/reviewer-input.json')
assert not output.exists()
packet=core.semantic_reviewer_packet(audit)
core._write_packet(packet,str(output))
print(json.dumps({'reviewer_input':output.as_posix(),'reviewer_packet_sha256':packet['packet_sha256']}))
