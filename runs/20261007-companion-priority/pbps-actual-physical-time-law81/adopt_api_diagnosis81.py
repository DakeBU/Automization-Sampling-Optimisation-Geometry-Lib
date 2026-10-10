from pathlib import Path
import json,hashlib,sys
r=Path('runs/20261007-companion-priority/pbps-actual-physical-time-law81');d=r/'api-diagnosis81'
load=lambda p:json.loads(Path(p).read_bytes())
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest())
def verify(x):
 if isinstance(x,dict):
  if 'path' in x and ('RAW_sha256' in x or 'raw_sha256' in x):assert pin(x['path'])['RAW_sha256']==x.get('RAW_sha256',x.get('raw_sha256')),x
  for v in x.values():verify(v)
 elif isinstance(x,list):
  for v in x:verify(v)
assert pin(d/'closed-manifest81.json')['RAW_sha256']=='48e759c1a7c485f1676a570ca9774543e37bfa00fd5e46b6101b8ae544929cba'
verify(load(d/'closed-manifest81.json'));a=load(d/'diagnosis81.json');verify(a)
assert a['status']=='API_BOUNDARY_REPRODUCED_AND_COMPILING_ALTERNATIVE' and not a['heartbeat_escalation'] and not a['source_statement_repair']
assert load(a['positive_terminal_receipt']['path'])['exit_code']==0
assert load(a['negative_terminal_receipt']['path'])['exit_code']!=0
p=r/'root.api-diagnosis81.adoption.json';assert not p.exists();p.write_text(json.dumps(dict(status='INDEPENDENT_API_DIAGNOSIS_ADOPTED',native_manifest=pin(d/'closed-manifest81.json'),native_decision=pin(d/'diagnosis81.json'),source_statement_changed=False,positive_and_negative_native_receipts_verified=True,full_production_focused=pin(r/'focused81-attempt5/receipt.json'),scope='Implementation elaboration direction only; independent full proof/semantic review remains separate.'),indent=2)+'\n')
sys.path.insert(0,str(Path.cwd()/'tools'));import astis_advance as adv
adv.checkpoint_advance('ASTIS-SA-20261010-PBPSIdealHalfTurnKernel',worker_id='companion_root_20261005',route_fingerprint='inferred-typed-wait-composition/measurable-live-range/product-Fubini/initial-marginal',progress_signature='3227jobs-EXIT0-exact-sealed-header-ten-formulaBODY-regions',mathematical_delta='Full sealed ideal H_y initialized returned-position probability kernel focused compiled, genuine exact q_y and actual product-input terminal/origin agreement. API freeze retired by independent negative/positive contrast.',exact_residual='Independent full mathematics, blind reconstruction and final source/BODY coverage pending; no PROVED_LOCAL/VERIFIED or full-paper credit. Actual Markov/invariance/mixing/cost/composition remain open.')
print('API route diagnosis adopted; full theorem focused PASS; independent whole-body reviews remain pending')
