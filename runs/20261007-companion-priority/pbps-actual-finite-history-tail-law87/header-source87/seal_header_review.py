from pathlib import Path
import hashlib
import json
import datetime

root = Path('E:/Samplinglib')
out = Path(__file__).resolve().parent
pre = root/'runs/20261007-companion-priority/pbps-clock-tail-preread87'
candidate = out.parent/'header87.proposed.lean'
expected = '1048a4bf0d171d52a2eb834f4281621e0101c8d4700c7eae60edc5e64cd3c39b'
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
assert digest(candidate) == expected, 'Header changed: rereview required'
assert digest(pre/'independent-source-first87/source-first.freeze.native.json') == 'd8e37422b5597b0a5761282bcf88b94453a7b21a5176ef0cb71c2363f5ab87d7'
snapshot = out/'header87.exactraw.snapshot.txt'
snapshot.write_bytes(candidate.read_bytes())
decision_path = out/'exact-header.source-decision.native.json'
decision = json.loads(decision_path.read_text(encoding='utf-8'))
decision['decision_recorded_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
topology_path = out/'source-slice87.v2.topology-decision.native.json'
decision['separate_bounded_source_topology_review'] = dict(path=str(topology_path),raw_sha256=digest(topology_path),
    accepted_slice_raw_sha256='7c9873ef87bfb75c7a2ec86ecbb40b589384bc41bc197030acf7fa088fd611d9')
decision_path.write_text(json.dumps(decision,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
inputs = [candidate, pre/'independent-source-first87/source-first.freeze.native.json',
    pre/'independent-source-first87/primary-source.raw-manifest.native.json',
    pre/'independent-source-first87/chronology.native.jsonl',
    pre/'source-slice87.json',pre/'source-slice87.v2.json',pre/'retrieval87.json']
assert digest(pre/'source-slice87.v2.json') == '7c9873ef87bfb75c7a2ec86ecbb40b589384bc41bc197030acf7fa088fd611d9'
primary_manifest = json.loads(inputs[2].read_text(encoding='utf-8'))
source = Path(primary_manifest['source']['local_path'])
assert digest(source) == primary_manifest['source']['raw_sha256']
source_bytes = source.read_bytes()
for span in primary_manifest['anchors']:
    assert hashlib.sha256(source_bytes[span['byte_start_zero_based']:span['byte_end_exclusive']]).hexdigest() == span['raw_span_sha256']
inputs.append(source)
slice_record = json.loads((pre/'source-slice87.v2.json').read_text(encoding='utf-8'))
retrieval_record = json.loads((pre/'retrieval87.json').read_text(encoding='utf-8'))
indirect = []
for key in ['global_source_graph','global_source_inventory']:
    item = slice_record[key]
    path = root/item['path']
    assert digest(path)==item['raw_sha256']
    indirect.append(dict(path=str(path),raw_sha256=digest(path),bytes=path.stat().st_size,inspection='RAW hash checked only; no semantic/global topology review'))
for item in retrieval_record['actual_compiled_parents']:
    path = root/item['path']
    assert digest(path)==item['raw_sha256']
    indirect.append(dict(path=str(path),raw_sha256=digest(path),bytes=path.stat().st_size,inspection='RAW hash checked only; implementation not read'))
for check in retrieval_record['checks']:
    for channel in ['stdout','stderr']:
        item=check[channel]
        path=root/item['path']
        assert digest(path)==item['raw_sha256']
        indirect.append(dict(path=str(path),raw_sha256=digest(path),bytes=path.stat().st_size,inspection='RAW hash checked only; retrieval log contents not read'))
events = [dict(sequence=1,event='Primary-first source freeze complete',artifact=str(inputs[1]),raw_sha256=digest(inputs[1])),
    dict(sequence=2,event='Root authorized exact-header-only comparison after primary freeze'),
    dict(sequence=3,event='Exact candidate header read; no implementation bodies or earlier verdicts read',artifact=str(candidate),raw_sha256=digest(candidate)),
    dict(sequence=4,event='Root authorized separate bounded source-slice validation',artifact=str(pre/'source-slice87.json'),raw_sha256=digest(pre/'source-slice87.json')),
    dict(sequence=5,event='Source-slice v1 label identity refinement requested; accepted v2 independently reviewed',artifact=str(pre/'source-slice87.v2.json'),raw_sha256=digest(pre/'source-slice87.v2.json')),
    dict(sequence=6,event='Exact-header source decision and separate bounded topology decision completed; not body acceptance',artifact=str(decision_path),raw_sha256=digest(decision_path))]
chronology = out/'chronology.header-source87.native.jsonl'
chronology.write_text(''.join(json.dumps(dict(event,recorded_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()))+'\n' for event in events),encoding='utf-8')
outputs = [p for p in sorted(out.iterdir()) if p.is_file() and p.name != 'closed-raw-manifest.header-source87.native.json']
def pin(path):
    return dict(path=str(path.resolve()),raw_sha256=digest(path),bytes=path.stat().st_size)
manifest = dict(schema=1,kind='closed-raw-exact-header-source-review-manifest',reviewer_identity='/root/fresh_source87',
    stage='HEADER_ONLY_BEFORE_PROOF_SEARCH',inputs=[pin(p) for p in inputs],outputs=[pin(p) for p in outputs],
    indirect_raw_inputs=indirect,primary_anchor_spans_reverified=True,
    global_topology_reused_by_root_only=True,body_source_acceptance=False)
manifest_path=out/'closed-raw-manifest.header-source87.native.json'
manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for path in [decision_path,manifest_path,chronology]:
    print(path.name,digest(path))
