from pathlib import Path
import hashlib,json
BASE=Path(__file__).resolve().parent
ROOT=Path('/Users/zhouhuanjian/ASTIS-GC')
PRIVATE=BASE.parent/'PRIVATE-normal-sourceV-baseline'
def sha(b):return hashlib.sha256(b).hexdigest()
inputs=[]
for rel in ['tools/astis_advance.py','tools/astis_harness.py','tools/astis_publication.py','research-wiki/semantic-roundtrip/audits/huanjian-zero-query-separation.json']:
 b=(ROOT/rel).read_bytes();inputs.append({'path':rel,'bytes':len(b),'sha256':sha(b)})
 # Whole foreign/control-plane snapshots stay PRIVATE, including API source.
 if rel.startswith('tools/'):(PRIVATE/(rel.replace('/','__')+'.actual-input')).write_bytes(b)
(BASE/'actual-API-input-hashes.json').write_text(json.dumps(inputs,ensure_ascii=False,indent=2)+'\n')
baseline=json.loads((PRIVATE/'baseline.json').read_text())
policy={'private_directory':'PRIVATE-normal-sourceV-baseline/','never_export':True,'portable_directory':'normal-sourceV/','private_baseline_sha256':sha((PRIVATE/'baseline.json').read_bytes()),'private_ledger_before_sha256':sha((PRIVATE/'ledger.before.raw.jsonl').read_bytes()),'private_ledger_after_sha256':sha((PRIVATE/'ledger.after-api.raw.jsonl').read_bytes()),'protected_entries':len(baseline['protected']),'full_foreign_snapshots_in_portable_directory':False,'nested_repository_exception':'Directory/Git HEAD/refs metadata and Git index stat only; no ATLAS body/semantic inventory/index/projections read/hash/glob. This exception is not source/math authority.','failures_preserved':2,'actual_API_invocations':1,'permanent_marker_sha256':sha((BASE/'PERMANENT-API-ONCE.marker.json').read_bytes())}
(BASE/'private-baseline-policy.json').write_text(json.dumps(policy,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'actual_API_inputs':inputs,'private_policy':policy},ensure_ascii=False,indent=2))
