from pathlib import Path
import json, hashlib, subprocess, sys, datetime, os
ROOT=Path('/Users/zhouhuanjian/ASTIS-GC')
sys.path.insert(0,str(ROOT))
from tools import astis_advance
BASE=ROOT/'research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-normalizer-semantic-evidence'
PUB=BASE/'fresh-source-reader-640251/verification-transition'
PRIV=ROOT/'.astis/huanjian-fixed-spectrum-normalizer-20261108/fresh-source-640251/verification-transition'
H=lambda b:hashlib.sha256(b).hexdigest()
auth=json.loads((PUB/'root-normal-source-V-authorization.exact.json').read_text())
baseline=json.loads((PUB/'preflight-baseline.json').read_text())
ledger=ROOT/'runs/substantive_advances.jsonl'
canonical=ROOT/'research-wiki/semantic-roundtrip/audits/huanjian-fixed-spectrum-normalizer.json'
proposal=(BASE/'fresh-source-reader-640251/phase3/proposed-accepted-canonical-audit.json').read_bytes()
evidence=json.loads((PUB/'normal-V-evidence.json').read_text())
assert not (PRIV/'normal-V-API-attempted.json').exists(),'One-shot API attempt already recorded: never repeat'
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==auth['checked_immutable_commit']
assert H(ledger.read_bytes())==auth['advance_ledger_before_sha256']
assert H(canonical.read_bytes())==auth['canonical_audit_before_sha256']
assert H(proposal)==auth['authorized_exact_accepted_audit_sha256']
assert all(H((ROOT/p).read_bytes())==h for p,h in baseline['all_raw_frontier_hashes'].items())
assert all(H((ROOT/p).read_bytes())==h for p,h in baseline['frozen_review_file_hashes'].items())
assert all(H((ROOT/p).read_bytes())==h for p,h in baseline['protected_README_config_model_file_hashes'].items())
assert H((ROOT/'runs/substantive_discoveries.jsonl').read_bytes())==baseline['discovery_ledger_sha256']
assert evidence['verifier_id']==auth['authorized_actor']
assert evidence['verified_commit']==auth['checked_immutable_commit']
assert evidence['lean_declarations']==evidence['publication_declarations']==baseline['own_before']['publication_declarations']
attempt={'actor':auth['authorized_actor'],'advance_id':auth['advance_id'],'call_count':1,'attempted_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'operation':'normal astis_advance.transition_advance PROVED_LOCAL->VERIFIED; no retry authorized'}
attempt_bytes=(json.dumps(attempt,ensure_ascii=False,indent=2)+'\n').encode()
for out in [PRIV,PUB]:
    with (out/'normal-V-API-attempted.json').open('xb') as handle:
        handle.write(attempt_bytes);handle.flush();os.fsync(handle.fileno())
canonical.write_bytes(proposal)
assert canonical.read_bytes()==proposal
print('EXACT_CANONICAL_ADOPTION_SHA256 '+H(proposal),flush=True)
print('NORMAL_V_API_BEGIN '+datetime.datetime.now(datetime.timezone.utc).isoformat(),flush=True)
astis_advance.transition_advance(
    auth['advance_id'],'VERIFIED',worker_id=auth['authorized_actor'],
    modes=baseline['own_before'].get('modes',[]),evidence=evidence)
success={'actor':auth['authorized_actor'],'advance_id':auth['advance_id'],'normal_V_API_returned_success':True,'exactly_one_call':True,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'normal_API':'tools.astis_advance.transition_advance','from_state':'PROVED_LOCAL','to_state':'VERIFIED','proof_owner_preserved':baseline['own_before']['owner_id'],'STAB_entered':False}
success_bytes=(json.dumps(success,ensure_ascii=False,indent=2)+'\n').encode()
for out in [PRIV,PUB]:
    with (out/'normal-V-API-success.json').open('xb') as handle:
        handle.write(success_bytes);handle.flush();os.fsync(handle.fileno())
print('NORMAL_V_API_RETURNED_SUCCESS '+success['completed_utc'],flush=True)
