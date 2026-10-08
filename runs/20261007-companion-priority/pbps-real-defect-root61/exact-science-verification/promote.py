from common import *
from tools import astis_advance
assert head()==SCI
payload=J(P/'payload.json'); core=payload['named_verification_payload']; assert payload['named_verification_payload_sha256']==H(C(core))
before=J(P/'inputs.before.json')['ledger_before']; matches(before['original']); matches(before['raw_snapshot'])
state=astis_advance.current_advances(); assert state[SAU]['state']=='PROVED_LOCAL'; assert state[SAU]['owner_id']!=ACTOR
evidence=dict(verifier_id=ACTOR,verified_commit=SCI,checked_commit=SCI,gate=core['gate'],source_audit=core['source_audits'],fake_closure_scan=core['fake_closure_scan'],publication_declarations=core['declarations'],exact_scope=core['scope'],named_verification_payload_sha256=payload['named_verification_payload_sha256'],verification_payload=str((P/'payload.json').relative_to(ROOT)).replace('\\','/'),verification_receipt=str((P/'receipt.json').relative_to(ROOT)).replace('\\','/'),verification_run=str((P/'run.json').relative_to(ROOT)).replace('\\','/'),all_691_science_entries_matched_current_LF=True,mandatory_aggregate='Deferred to sole serialized root integration; no credit granted by this focused verification')
astis_advance.transition_advance(SAU,'VERIFIED',worker_id=ACTOR,modes=['independent-exact-science-verification'],evidence=evidence)
after=(ROOT/'runs/substantive_advances.jsonl').read_bytes(); old=path(before['raw_snapshot']['path']).read_bytes(); assert after.startswith(old)
added=after[len(old):]; rows=[json.loads(l) for l in added.splitlines() if l.strip()]; assert len(rows)==1 and rows[0]['to_state']=='VERIFIED' and rows[0]['worker_id']==ACTOR
state=astis_advance.current_advances(); assert state[SAU]['state']=='VERIFIED'; lanes=[k for k,v in state.items() if v.get('state')=='STABILIZING']; assert lanes==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
W(P/'promotion.json',dict(status='VERIFIED',checked_commit=SCI,actual_promotion_PID=os.getpid(),worker_id=ACTOR,ledger_before=before,ledger_after=pin(ROOT/'runs/substantive_advances.jsonl'),appended_record=rows[0],appended_bytes=len(added),exactly_one_append=True,sole_STABILIZING=lanes,canonical_cells_audits_proofs_modified=False))
print('INDEPENDENT_VERIFIED',SAU,SCI,'actual_PID',os.getpid())
