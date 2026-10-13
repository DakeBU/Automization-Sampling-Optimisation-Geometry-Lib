import pathlib, json, hashlib, datetime
O=pathlib.Path('E:/Samplinglib/runs/20261007-companion-priority/pbps-source-mean-gradient-domain-topology-overlay54')
B=O.parent/'pbps-source-mean-gradient-domain-sourcegraph54'
def sha(b):return hashlib.sha256(b).hexdigest()
def lf(b):return b.replace(b'\r\n',b'\n')
def encode(d):return (json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode('utf8')
def write(name,d):(O/name).write_bytes(encode(d))
def desc(p):
    b=p.read_bytes();assert b'\r' not in lf(b),str(p)
    return {'path':str(p),'raw_bytes':len(b),'lf_bytes':len(lf(b)),'raw_sha256':sha(b),'lf_sha256':sha(lf(b))}
inputs=json.loads((O/'input-bindings.json').read_text(encoding='utf8'))
for name in ['input-bindings.json','creation-dependencies.json']:
    d=desc(B/name);d['role']='immutable original native input/dependency manifest';inputs.append(d)
for d in inputs:
    actual=desc(pathlib.Path(d['path']));assert actual['raw_sha256']==d['raw_sha256'] and actual['lf_sha256']==d['lf_sha256'],d['path']
write('input-bindings.json',inputs)
deps={'schema':'representation-overlay54-creation-dependencies/v1','current_actual_opening_lease_snapshot':desc(O/'lease.open.snapshot.json'),'historical_creator_closed_lease':desc(B/'lease.json'),'historical_reviewer_closed_lease':next(x for x in inputs if x['path'].endswith('reviewer.topology.lease.json')),'opening_scope':'Only owned overlay; historical CLOSED leases are provenance, never reopened','source_proof_compiler':'NOT_STARTED_CLOSED','original_candidate_and_all_metadata':'unchanged; exact1448 LF19de42336148aa900917e6c77753325145d6010dfd1718c1625b2b9a8f7ce595'}
write('creation-dependencies.json',deps)
counts=json.loads((O/'counts.json').read_text(encoding='utf8'))
g=desc(O/'source-proof-graph.json');op=desc(O/'overlay-operations.json')
capsule='''# Minimal representation overlay54

Successor copies repair only independent negative T54-1, T54-2 and T54-3. Exact1448 statement, mathematics, source hypotheses, original graph and CLOSED negative remain unchanged. This is not topology admission or theorem credit.

- T54-1: actual global UniformSpace class header193 extends TopologicalSpace. Original Core129 fragment is retained as incidental EXCLUDED exposure and cannot supply the UniformSpace class.
- T54-2: actual Support213–217 to_additive carrier generates HasCompactSupport from HasCompactMulSupport. Generation provenance and inherited207–208 context are explicit. Pinned RHS217 is EXCLUDED from implementation expansion; compact-support semantics remain compact closure of additive support, with Zero replacing One.
- T54-3: actual LinearPMap66–67 ContinuousAdd E/F, TopologicalSpace R and ContinuousSMul R E/F are bound to primitive public class headers. All closability/closure consumers inherit these slots. Standard real/Lp normed topology supplies instances internally through an explicit external-unexpanded boundary; no public theorem premise is added and Lp is not assumed finite-dimensional.

Files: source-proof-graph.json; selected-providers.json; source-coverage.json; caller-inventory.json; lexical-inventory.json; selected-token-inventory.json. overlay-operations.json gives exact before/after affected records and appended records. Unaffected source-contract/hypothesis/formula inventories are inherited by original raw hashes, not regenerated.

Counts: 129 nodes (+3), 574 edges (+27), 125 providers (+5), 454 physical coverage rows (+12), 505 caller occurrences (+11), 2426 lexemes (+111). Actual header/context byte coordinates are zero-based half-open UTF8; physical lines are one-based. Every selected successor-provider row has NODE/EXCLUDED coverage. Graph edges describe source/provider ingredients, not compiled54 calls.

Historical49/50 proof exposure and original54 source/API exposure remain disclosed. New reads were restricted to the negative, affected original inventories and selected public header/generation/context. No primary reread, private proof copy, compiler, proof54, claim, canonical edit or creator admission. Failed read-only locator/stdout operations and the corrected declaration-name bookkeeping guard are retained.

Raw hashes bind exact bytes. Overlay LF normalization replaces CRLF with LF ONLY; every bound original and output is checked for absence of lone CR. Native run logical hash is SHA256 of UTF8 sorted compact JSON (ensure_ascii=False), whole run object minus run_sha256. Current opening lease is distinguished from historical CLOSED creator/reviewer leases. Own actual read/write/Python leases close as the final filesystem operation; compiler remains NOT_STARTED_CLOSED. Separate independent repair review is required.
'''
(O/'capsule.md').write_bytes(capsule.encode('utf8'))
write('final-input-consistency.json',{'all_current_input_raw_LF_exact':True,'input_count':len(inputs),'originals_preserved':True,'statement_changed':False,'LF_recipe':'CRLF -> LF only; lone CR rejected','creator_topology_admission':False})
lease=json.loads((O/'lease.json').read_text(encoding='utf8'))
lease.update({'read':'CLOSED','write':'CLOSED','python':'CLOSED','compiler':'NOT_STARTED_CLOSED','closed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'closure_order':'Last filesystem operation after all input/output/native run binding; no filesystem reads/writes after closing','topology_admitted':False})
leasebytes=encode(lease);leasedesc={'path':str(O/'lease.json'),'raw_bytes':len(leasebytes),'lf_bytes':len(lf(leasebytes)),'raw_sha256':sha(leasebytes),'lf_sha256':sha(lf(leasebytes))}
outputs=[desc(p) for p in sorted(O.rglob('*')) if p.is_file() and p.name not in ['run.json','lease.json']]
run={'schema':'minimal-representation-overlay54-native-run/v1','creator':'/root/gaussian_noncompact_preread_42','scope':'T54-1/T54-2/T54-3 ONLY; no mathematical/header changes','status':'CLOSED_SOURCE_ONLY_AWAITING_INDEPENDENT_REPAIR_REVIEW','inputs':inputs,'outputs':outputs,'successor_graph':g,'operations':op,'counts':counts,'expected_actual_closed_lease':leasedesc,'compiler':'NOT_STARTED_CLOSED','topology_admitted':False,'hash_recipes':{'raw':'SHA256 exact bytes','LF':'CRLF replaced with LF only; no lone CR accepted','logical':'SHA256 UTF8 sorted compact JSON ensure_ascii=False of whole run excluding run_sha256'}}
run['run_sha256']=sha(json.dumps(run,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf8'))
runbytes=encode(run);(O/'run.json').write_bytes(runbytes)
summary={'graph_sha256':g['raw_sha256'],'operations_sha256':op['raw_sha256'],'run_raw_sha256':sha(runbytes),'run_logical_sha256':run['run_sha256'],'actual_closed_lease_sha256':leasedesc['raw_sha256'],'counts':counts,'outputs':len(outputs),'inputs':len(inputs)}
# FINAL filesystem operation. No file/stat/glob/subprocess calls follow.
(O/'lease.json').write_bytes(leasebytes)
print(json.dumps(summary))
