from common import *
data=J(P/'strict-inputs.json')
for row in data['rows']:matches(row['expected'],row['resolved_path'])
out=J(P/'outputs.manifest.json')
for q in out['artifacts']:matches(q)
run=J(P/'run.json');assert H(C({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']
assert H((P/'named-exact-verification.payload.json').read_bytes())==run['named_payload_raw_sha256']
receipt=J(P/'receipt.json');assert receipt['run_sha256']==run['run_sha256'];matches(receipt['run']);matches(receipt['named_payload']);matches(receipt['strict_inputs']);matches(receipt['outputs_manifest'])
for q in [run['inputs'],run['outputs'],run['transition'],run['gates'],run['native_review']]:matches(q)
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()==SCI
import tools.astis_advance as adv
state=adv.current_advances();assert state['ASTIS-SA-20261009-PBPSPositiveRealRootUniqueness']['state']=='VERIFIED'
assert [k for k,v in state.items() if v['state']=='STABILIZING']==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
print('FINAL_NATIVE_READBACK_PASS',os.getpid(),'inputs',data['unique_pin_count'],'outputs',out['count'],'whole',run['run_sha256'],'payload',run['named_payload_raw_sha256'])
