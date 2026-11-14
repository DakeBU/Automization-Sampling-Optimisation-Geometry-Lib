"""Validate original independent preproof source artifacts without intake or proof credit."""
from pathlib import Path
import hashlib
import json
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
SG=Path('.astis/semantic-neutral-20261113/radius_sg_2c71')
TC=Path('.astis/semantic-neutral-20261113/radius_tc_8b40')
sha=lambda raw:hashlib.sha256(raw).hexdigest()
pins=[
    (SG,'output-manifest-v1.json','bf457c70aa05ea5fa777a8daa61eaa8fe7c715be93240536c21ad0fbb6f08a82'),
    (SG/'successor-v2','successor-manifest-v2.json','ba673e7949af9fe138cebb1d6dfe8a8111748109f13a3eedfd7c9bda58fcabba'),
    (TC,'artifact-manifest-v1.json','ebc7eefac25f65c077c312bedf903e81598361d5e775072824f5b1c2ae000e7c'),
    (TC/'incremental-v2','incremental-manifest-v2.json','fc7e61af5188c0e4b4d60a9e5dffa902a8c301b10dbfb00aefa74134f8705662'),
]
originals={}; manifests=[]
for root,name,digest in pins:
    p=root/name;raw=p.read_bytes();assert sha(raw)==digest
    entries=json.loads(raw)['files']
    for item in entries:
        q=root/item['path'];assert '..' not in Path(item['path']).parts and q.is_relative_to(root) and not q.is_symlink()
        body=q.read_bytes();assert len(body)==item['bytes'] and sha(body)==item['sha256'],str(q)
        originals[str(q)]={'bytes':len(body),'sha256':sha(body)}
    originals[str(p)]={'bytes':len(raw),'sha256':digest}
    manifests.append({'path':str(p),'sha256':digest,'listed_originals_verified':len(entries)})
extras=[
    (SG/'packet-seal-v1.json','ce59761f511cc2c9399fda45c04907e4cc87d33484fc90e30a7b9a63cbd57be0'),
    (SG/'successor-v2/successor-seal-v2.json','4abd59d11302e74b16c484f8c1ac813c18c7988197e865721e0d94c2b6cfe1d1'),
    (TC/'final-receipt-v1.json','323bfefecb4dad2532be57d1b3e4bf45de6d43664f38e7d2ac17fa7e4c89b929'),
    (TC/'incremental-v2/incremental-review-seal-v2.json','b33c4051db45ef20f0d42eda6084876317eb85d5f58196aeb48c5d651644ed17'),
]
for p,h in extras:
    raw=p.read_bytes();assert sha(raw)==h
    originals[str(p)]={'bytes':len(raw),'sha256':h}
audit=json.loads((SG/'binder-definition-audit-v1.json').read_bytes())
delta=json.loads((TC/'incremental-v2/incremental-independent-challenge-v2.json').read_bytes())
assert audit['seal_sha256']=='49d5fa00c9ae90d65878d955fab59d6a4bc03e942501677719881f3d26bf1a72'
assert audit['public_excess']==[] and audit['q0']['retained'] is True
assert audit['verdict']['binders']=='NO_EXCESS_DETECTED'
assert delta['verdict']['remaining_topology_blocks']==[]
assert delta['verdict']['TC_F1']==delta['verdict']['TC_F2']=='CLOSED_AT_SOURCE_TOPOLOGY_LEVEL'
assert delta['verdict']['target_proof_or_kernel_acceptance']=='NONE'
ports=json.loads((SG/'successor-v2/internal-port-obligations-v2.json').read_bytes())
assert len(ports['ports'])==9 and ports['target_proof_or_API_search_attempts']==0
record={
    'kind':'Unclaimed exact statement and independent source-type/graph/topology admission readback only',
    'statement_seal_sha256':audit['seal_sha256'],'source_sha256':audit['source_sha256'],
    'signature_hashes':audit['signature_hashes'],
    'source_type_verdict':audit['verdict'],'independent_topology_verdict':delta['verdict'],
    'current_topology_blocks':[],'unproved_internal_ports':ports['ports'],
    'remaining_omitted_source_derivations':'Five SOURCE_GAP records remain proof obligations; neither source falsehood nor extra hypotheses.',
    'independent_original_manifests':manifests,'all_original_files':originals,
    'formalizer_API_pristine':False,'target_formal_proof_or_implementation_attempts':0,
    'new_SAU_frontier_ledger_intake_calls':0,
    'post_admission_reuse_search':'ROOT has now performed read-only ASTIS/Mathlib norm/provider retrieval after independent topology acceptance. This does not change the historical preproof seal or declare any new proof/API successful.',
    'capture_qualifications':[
        'SG initial inline extractor scripts were not archived verbatim. Its frozen report discloses exact available raw inputs/outputs/readtrace and reproducible builder without inventing raw command history. TC independently verified all locators and actual successor diff.',
        'SG failed unnecessary Matrix MeasurableSpace/BorelSpace diagnostic and parser text extraction v1 are preserved; v2 succeeds. TC preserves its overly broad definition locator exposure. No source/target failure inferred.',
        'Initial ROOT read-only floor rg calls are in conversation tool chunks6b75bb/24afd(empty exit1)/5ba3f0(frame code). No raw receipt is fabricated. Subsequent focused searches use actual run_check receipts/logs.',
        'One later retrieval guessed nonexistent Mathlib/Analysis/CStarAlgebra/Order.lean (actualsearch exit2); real CFC/Order path matches are retained. This is a locator failure, not mathematical negative evidence.'
    ],
    'truth_boundary':'Statement/source preparation only. No new theorem, source/Lean equivalence, API provider success, canonical status, proof integration or website acceptance. Current R9 verification remains separate; all original source/statement/code boundaries preserved.'
}
p=W/'reviewed-preproof-inputs.json'
with p.open('x') as f:f.write(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'original_files_verified':len(originals),'statement_seal_sha256':record['statement_seal_sha256'],'remaining_topology_blocks':[],'open_internal_ports':9,'target_proof_attempts':0,'new_intake_calls':0,'readback_sha256':sha(p.read_bytes())}))
