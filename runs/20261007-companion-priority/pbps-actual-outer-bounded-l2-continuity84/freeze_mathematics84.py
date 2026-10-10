from pathlib import Path
import datetime,hashlib,json
r=Path(__file__).parent;p=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualOuterBoundedL2Continuity.lean');raw=p.read_bytes();receipt=r/'focused84-attempt2/receipt.json';x=json.loads(receipt.read_bytes());assert x['terminal_closed'] and x['exit_code']==0 and x['source_RAW_sha256']==hashlib.sha256(raw).hexdigest()
s=raw.decode();h=(r/'header84.reviewed.lean').read_text(encoding='utf8')
def prop(t):
 return t.split('private def actual_outer_bounded_l2_continuity_statement',1)[1].split('\nend\n',1)[0].split('\n\nset_option',1)[0].rstrip()
assert prop(s)==prop(h)
out=r/'mathematics-freeze84.json';assert not out.exists();out.write_text(json.dumps(dict(status='FOCUSED_COMPILED_EXACT_SEALED_PROP_PENDING_INDEPENDENT_BODY_REVIEW',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),module=p.as_posix(),module_RAW_sha256=hashlib.sha256(raw).hexdigest(),module_RAW_bytes=len(raw),header_RAW_sha256=hashlib.sha256((r/'header84.reviewed.lean').read_bytes()).hexdigest(),focused_final_receipt=receipt.as_posix(),full_private_Prop_matches_seal=True,only_header_docstring_change='Prospective heading replaced by actual prerequisite heading; no change in Prop/binders/definitions.',failed_attempts=['focused84-attempt1'],failed_route_diagnostics=['compiler-route-diagnosis84.json'],mathematical_route_unchanged=True,PROVED_LOCAL=False,VERIFIED=False),indent=2)+'\n',encoding='utf8',newline='\n');print('84 whole-source mathematics frozen',hashlib.sha256(raw).hexdigest())
