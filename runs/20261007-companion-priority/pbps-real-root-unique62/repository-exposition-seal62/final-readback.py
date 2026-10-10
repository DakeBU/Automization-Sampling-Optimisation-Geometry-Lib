from common import *
manifest=J(P/'inputs.manifest.json')
for q in manifest['rows']:matches(q['expected'],q['resolved_path'])
output=J(P/'outputs.manifest.json')
for q in output['artifacts']:matches(q)
run=J(P/'run.json');assert H(C({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256'];assert H((P/'named-repository-exposition.payload.json').read_bytes())==run['named_payload_raw_sha256']
receipt=J(P/'receipt.json');assert receipt['run_sha256']==run['run_sha256']
for key in ['run','named_payload','inputs','outputs']:matches(receipt[key])
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()==INT
# Never check new63 scratch/source/ledger against this scoped snapshot.
assert J(P/'repository.checks.json')['status']=='PASS' and J(P/'graph.check.json')['status']=='PASS'
assert J(P/'exposition.check.json')['all_eight_images_viewed']
print('FINAL_READBACK62_PASS',os.getpid(),'inputs',manifest['count'],'outputs',output['count'],run['run_sha256'],run['named_payload_raw_sha256'])
