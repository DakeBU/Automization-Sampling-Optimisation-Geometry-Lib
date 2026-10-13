from pathlib import Path
import hashlib,json,sys
root=Path.cwd()
sys.path.insert(0,str(root/'tools'))
import astis_advance as adv
r=root/'runs/20261007-companion-priority/pbps-centered-root64'
def pin(p):
    b=p.read_bytes()
    return dict(path=p.as_posix(),bytes=len(b),raw_sha256=hashlib.sha256(b).hexdigest())
g=r/'square-order-draft-v5/receipt.json'
p=r/'prefix-diagnostic-v6/receipt.json'
assert json.loads(g.read_bytes())['exit_code']==0
assert json.loads(p.read_bytes())['exit_code']==1
errors=[s for s in (p.parent/'stdout.log').read_text(encoding='utf-8').splitlines() if ': error' in s]
assert len(errors)==1 and 'noProof64_PREFIX_DIAGNOSTIC_INTENTIONALLY_UNDEFINED' in errors[0]
out=r/'checkpoint64-v6.json'
assert not out.exists()
record=adv.checkpoint_advance(
 'ASTIS-SA-20261009-PBPSCenteredRootOrderInverse',worker_id='companion_root_20261005',
 route_fingerprint='three-canonical-complex-lifts/same-macro-energy-reuse/typed-application-congruence',
 progress_signature='generic-v5-EXIT0;sealed-actual-prefix-through-Gamma-q-zero-elaborated;full-candidate-not-proved',
 mathematical_delta='Shared arbitrary-real-L2 positive square-order scratch closes without sorryAx. Actual sealed theorem prefix now extracts same63 witnesses, derives constant/T preservation and same-root energy/Gamma q=0; prefix diagnostic has only its deliberately undefined tail. The full actual theorem remains unproved.',
 exact_residual='Close genuine production C4 from rough-gradient/Poincare parents, derive full scalar constant-complement square order, transport/restrict exact GammaP to HP0, then prove its unit and quantitative bounded inverse. Full combined-v6 is running; no production/proved/verified status yet.')
x=dict(checkpoint=record,generic_compiled_receipt=pin(g),prefix_type_diagnostic_receipt=pin(p),
 retired_routes=[dict(route='direct scalar adjoint-energy recomputation with unfolded actual A',diagnosis='global heartbeat and definitional matching; reuse independently accepted same-macro energy and typed application congruence instead',negative_evidence=['combined-draft-v2','combined-draft-v3','combined-draft-v4','prefix-diagnostic-v5'])],
 limitation='The intentionally undefined diagnostic body yields sorryAx; it is excluded from theorem evidence and retained only as elaboration diagnosis.',
 full_actual_theorem_compiled=False,production_files_created=False)
out.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Checkpoint64 v6 appended once; generic-only compile and typed-prefix diagnosis explicitly separated from full theorem.')
