"""Compact the completed local shared cycle without claiming delivery or whole-Goal closure."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
sys.dont_write_bytecode=True
sys.path.insert(0,'tools')
import astis_advance as advance
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
E=Path('research-wiki/technical-lemmas/real-matrix-positive-integral-semantic-evidence')
sha=lambda raw:hashlib.sha256(raw).hexdigest()
dump=lambda obj:(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode()
git=lambda *args:subprocess.check_output(['git',*args])
def create(p,raw):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(raw)
head=git('rev-parse','HEAD').decode().strip()
assert head=='b1d21f07e9cfb4029eb32fc381bb560d0a8096ec'
assert not git('diff','HEAD','--name-only') and not git('diff','--cached','--name-only')
raw=Path('runs/substantive_advances.jsonl').read_bytes()
states=advance._replay_advances([json.loads(x) for x in raw.splitlines()])
assert states['ASTIS-SA-20261112-RealMatrixPositiveIntegral']['state']=='VERIFIED'
assert states['ASTIS-SA-20261112-GaussianComplexitySourceMatrixVariance']['state']=='EXPLORING'
events=[json.loads(x) for x in raw.splitlines()]
vs=[e for e in events if e.get('advance_id')=='ASTIS-SA-20261112-RealMatrixPositiveIntegral' and e.get('to_state')=='VERIFIED']
assert len(vs)==1 and vs[0]['worker_id']=='/root/mv_fresh_source_6e28'
owner=json.loads((W/'latest-original-owner-after-shared-cycle.json').read_bytes())
assert all(x['original_owner_state']=='STABILIZING' for x in owner['refs'])
v=json.loads((W/'actual-original-VERIFIED-commit.json').read_bytes())
draft=json.loads(Path('.astis/huanjian-gc-source-matrix-variance-20261112/centered-draft-progress.json').read_bytes())
memory={
    'advance_id':'ASTIS-SA-20261112-RealMatrixPositiveIntegral',
    'state':'VERIFIED; local independent mathematics only',
    'mathematical_candidate':'9964c33c4599f85d27dc8687e8bd6fdb5c44ff49',
    'source_review_metadata_commit':'e24a33db711eb3c45308da128fbd681be0917c28',
    'normal_local_proof_carrier':'9687ebe5bd3691c5b4b45125fb6ce428822ea092',
    'native_reader_metadata_commit':'762ea453a3dea70136ff902a1cc1203baa8d283e',
    'failed_final_gate_HEAD':'7d6d61f298e882f54c4bc36b1fb67502d2801e77',
    'corrected_four_gate_and_normalV_metadata_HEAD':'5f69ac83737e497210d8d8ad9628c45d83089458',
    'sole_original_V_carrier':head,
    'exact_original_V_append_sha256':v['exact_original_append_sha256'],
    'full_original_V_payload_sha256':v['complete_V_payload_sha256'],
    'actual_independent_normalV_calls':1,'actual_normalV_API_failures':0,'root_VERIFIED_calls':0,
    'PL_original20_fields_preserved_inline':True,'original_V_payload_fields':28,
    'mathematics':'One canonical finite-real-matrix Bochner probability integral positivity theorem, with full AE PSD/Hermitian meaning and empty index permitted, materially called in the actual original-product Gaussian uncentered squared-moment bound.',
    'source_boundary':'Explicit ASTIS-authored background, not a printed arbitrary-f theorem or source repair. P actual Yi squares are integrable and sum E[Yi²] <= 2r(r+2)/d I; no extra source certificate inputs.',
    'independent_acceptance':'Raw/type/topology, full9-module source code reading,2 original anonymous decoders, fresh two-packet seven-slot source review; independent empty-output9-module/46 full-declaration kernel audit,4 proof-value probes and4 production pages at1440/390 with actual Chrome/MathJax/source/download/visual checks.',
    'guard':'309 full foreign advances,43 full discoveries+raw,469 foreign regular frontiers inclREADME,132567 tracked paths bytes/modes/index and117409 qualified historical/control paths preserved by independent before/precall/after comparisons. Full snapshots stay local/private.',
    'failures_and_limits':'First S proof needed existing Real StarOrderedRing import; P v1 reader variance wording corrected without math change. Native kernel/tooling/fixture failures and bootstrap missing raw capture qualified. First real final publication gate failed on ROOT canonical target metadata; one field corrected, old failed phase retained, changed-input v2 four gates all0. Independent normal verifier input/image/script failures and direct initial-guard receipt limits retained, no forged missing output.',
    'conceptual_mirror':'Original independent per-SAU none-found. Existing symmetry mirror identities/status unchanged; canonical shared reuse is not conceptual implication.',
    'integration_publication_purification':'HOLD. Original owner remains STABILIZING on latest fetched formal main and release ref; no takeover/root imports/Registry/globalgraph/public site/clean-port/push. Shared reader inventory refresh and older private-cone canonicalization remain serialized purification work.',
    'latest_owner_observation':owner,
    'next_existing_SAU':{
        'advance':'ASTIS-SA-20261112-GaussianComplexitySourceMatrixVariance',
        'status':'EXPLORING; public P compiled/source/native accepted, fullsource consumer acceptance pending',
        'same_original_T_signature_sha256':draft['original_signature_sha256'],
        'local_draft':draft,
        'next_action':'Move the exact already sealed centered/weighted consumer draft into final Tests module, final-path build and kernel audit, then independent whole-code/anonymous reconstruction/fresh source/native/reader acceptance. Reuse unchanged P and canonical S; no duplicate public declaration or repeated S normalV.',
    },
    'whole_Goal':'Unfinished. Both main lower bounds, exact oracle/precision/dimension/kappa/deterministic cap/TV/cost adapters, canonical website/source-index/globalgraph integration and final purification/reader acceptance remain required.',
}
create(E/'local-cycle-memory.json',dump(memory))
readme='''# Real matrix expectation positivity: locally independently verified

One canonical shared theorem now proves that the probability Bochner integral
of an integrable, almost-everywhere full-PSD finite real matrix map is full PSD.
The finite matrix index may be empty. This is explicitly authored background,
specializing the pinned convex-integral provider; it is not a printed general
theorem in the Gaussian paper.

Its actual consumer uses the original Gaussian column-product experiment and
proves genuine integrability and the source uncentered comparison
`sum_i E[Y_i^2] <= (2r(r+2)/d) I`. Generic application premises are proved
inside that consumer, never added to the source theorem.

The sole normal independent V event and all original source/native/reader/gate
evidence are carried by `b1d21f07e9cfb4029eb32fc381bb560d0a8096ec`.
See `local-cycle-memory.json`, `actual-original-VERIFIED-root-custody.json`,
`normal-verification/mv_src_6e28/originals/normal-verification-v2/REPORT.md`,
and `native-review/psd_native_7b31/originals/REPORT.md`.
The real failed final gate, metadata correction and bootstrap/receipt limits
remain visible. No failed mathematical route is invented from tooling errors.

The actual centered and cosine-weighted variance consumer has an exact-seal
local draft with true real operator-norm bounds, but is outside this immutable
shared packet. Final-module and independent source/native/reader acceptance
belong to the still-EXPLORING Gaussian source-variance SAU.

Local V is separate from serialized main integration, publication, purification
and whole-Goal completion. The original stabilization owner is still active;
older queues/frontiers/results were preserved and no global takeover occurred.
'''
create(E/'README.md',readme.encode())
originals=[]
for p in sorted(W.iterdir()):
    if p.is_file() and not p.is_symlink() and '.private.' not in p.name:
        dest=E/'root-local-process-originals'/p.name
        create(dest,p.read_bytes()); originals.append(dest)
for p in sorted(Path('.astis/huanjian-resume-20261103').glob('*-real-matrix-positive-integral-*.receipt.json')):
    r=json.loads(p.read_bytes()); log=Path(r['log'])
    assert sha(log.read_bytes())==r['log_sha256']
    for q in [p,log]:
        dest=E/'root-local-process-originals/actual-runs'/q.name
        create(dest,q.read_bytes()); originals.append(dest)
paths=[E/'local-cycle-memory.json',E/'README.md',*originals]
assert all('.private.' not in p.name for p in paths)
subprocess.run(['git','add','-f','--',*map(str,paths)],check=True)
assert set(git('diff','--cached','--name-only').decode().splitlines())==set(map(str,paths))
subprocess.run(['git','diff','--cached','--check','--',str(E/'local-cycle-memory.json'),str(E/'README.md')],check=True)
subprocess.run(['git','commit','--quiet','-m','Record verified real PSD integral and next actual centered variance boundary'],check=True)
commit=git('rev-parse','HEAD').decode().strip()
assert Path('runs/substantive_advances.jsonl').read_bytes()==raw
assert not git('diff','HEAD','--name-only')
record={'cycle_memory_commit':commit,'original_V_carrier':head,'state':'S locally independently VERIFIED; full Goal unfinished','root_VERIFIED_calls':0,'exact_memory_and_own_process_originals':len(paths),'next_existing_R9_final_consumer':True}
create(W/'actual-cycle-memory-commit.json',dump(record))
print(json.dumps(record))
