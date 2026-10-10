from pathlib import Path
import json,hashlib,datetime
r=Path(__file__).parent;file=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualSmallTimeContinuity.lean')
header=(r/'header82.proposed.lean').read_text(encoding='utf8');s=file.read_text(encoding='utf8');name='private def actual_small_time_stochastic_continuity_statement'
assert header.split(name,1)[1].split('\nend\n',1)[0].rstrip()==s.split(name,1)[1].split('\n\nset_option',1)[0].rstrip()
receipt=r/'focused82-attempt5/receipt.json';p=json.loads(receipt.read_bytes());assert p['exit_code']==0 and p['terminal_closed']
hh=hashlib.sha256(file.read_bytes()).hexdigest();assert hh==p['source_RAW_sha256'];assert file.read_bytes()==(r/'focused82-attempt5/source.snapshot.lean').read_bytes()
f=dict(status='STATEMENT_AND_IMPLEMENTATION_FROZEN_FOR_INDEPENDENT_MATH_REVIEW',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),module_path=file.as_posix(),module_RAW_sha256=hh,statement_header_RAW_sha256=hashlib.sha256((r/'header82.proposed.lean').read_bytes()).hexdigest(),literal_prop_unchanged=True,focused_final_receipt=receipt.as_posix(),PROVED_LOCAL=False,VERIFIED=False)
target=r/'mathematics-freeze82.json';assert not target.exists();target.write_text(json.dumps(f,indent=2)+'\n',encoding='utf8',newline='\n')
print(hh)
