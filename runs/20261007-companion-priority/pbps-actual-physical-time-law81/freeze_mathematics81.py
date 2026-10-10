from pathlib import Path
import json,hashlib,datetime
r=Path('runs/20261007-companion-priority/pbps-actual-physical-time-law81');file=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/IdealHalfTurnKernel.lean')
header=(r/'header81.proposed.lean').read_text(encoding='utf8');s=file.read_text(encoding='utf8')
name='private def ideal_half_turn_returned_position_kernel_statement'
assert header.split(name,1)[1].split('\nend\n',1)[0].rstrip()==s.split(name,1)[1].split('\n\nset_option',1)[0].rstrip()
receipt=r/'focused81-attempt5/receipt.json';p=json.loads(receipt.read_bytes())
assert p['exit_code']==0 and p['terminal_closed']
hh=hashlib.sha256(file.read_bytes()).hexdigest();assert hh==p['source_RAW_sha256']
assert file.read_bytes()==(r/'focused81-attempt5/source.snapshot.lean').read_bytes()
f=dict(status='STATEMENT_AND_IMPLEMENTATION_FROZEN_FOR_INDEPENDENT_MATH_REVIEW',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),module_path=file.as_posix(),module_RAW_sha256=hh,statement_header_RAW_sha256=hashlib.sha256((r/'header81.proposed.lean').read_bytes()).hexdigest(),literal_prop_unchanged=True,focused_final_receipt=receipt.as_posix(),PROVED_LOCAL=False,VERIFIED=False)
target=r/'mathematics-freeze81.json';assert not target.exists();target.write_text(json.dumps(f,indent=2)+'\n')
print(hh)
