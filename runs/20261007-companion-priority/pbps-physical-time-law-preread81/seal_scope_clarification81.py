from pathlib import Path
import json,hashlib,datetime
OWN=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
base=OWN/'source_freeze81.raw-manifest.json'
assert sha(base)=='682bce5a5aac096afd0d86ec94f119423100326e137642af5fe02c589a37b3f1'
m=json.loads(base.read_text(encoding='utf-8'))
for x in m['raw_outputs']:assert sha(Path(x['path']))==x['raw_sha256']
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
clarification={
 'schema':'additive-source-scope-clarification-v1','created_utc':now,
 'original_source_freeze_unchanged':True,
 'original_manifest_raw_sha256':sha(base),
 'source_ids':['alg1','alg1.l2','alg1.l8','S2.E8','S3.Thmtheorem2.p1.1','A1.SS2.p4.1'],
 'source_algorithm1':'Algorithm1 is captioned simulation of the ideal conditional half-turn process. Its exact conditional-reference draw is part of the ideal prescription, not evidence of an implemented approximate-reference sampler or established runtime/query producer.',
 'source_H_y':'H_y is exactly the ideal auxiliary returned-position probability kernel induced by source Algorithm1 with the exact q_y reference and Gaussian momentum and independent Exp clocks. Naming a derived measure-valued kernel H_y does not establish executable exact sampling, a path Markov property, reversibility, stationarity, or cost.',
 'source_q_y':'q_y is the normalized Gibbs quadratic tilt in(2.8). Constructing this mathematical probability measure/kernel and proving its Borel dependence differs from constructing an algorithm that produces exact q_y samples. The candidate only requests the former law-integration prerequisite.',
 'implementation_boundary':'Any implemented approximate reference sampler, gradient-only algorithm, restricted-Gaussian oracle implementation, acceptance/error guarantees and actual expected-query/runtime cost remains OPEN and excluded. An approximate qhat_y cannot silently replace q_y in H_y.',
 'graph_interpretation':'Frozen G81-02/G81-09/G81-12/G81-14 all refer to ideal exact-reference law semantics. No graph node or edge claims an implemented producer. Original inventory and graph bytes remain unchanged.',
 'proof_or_verification_credit':False
}
p=OWN/'source_scope_clarification81.json';p.write_text(json.dumps(clarification,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
out={'schema':'noncircular-additive-source-freeze-manifest-v1','created_utc':now,'original_manifest_raw_sha256':sha(base),'original_manifest_path':str(base),'raw_inputs':m['raw_inputs'],'raw_outputs':m['raw_outputs']+[{'path':str(base),'raw_sha256':sha(base)},{'path':str(OWN/'seal_scope_clarification81.py'),'raw_sha256':sha(OWN/'seal_scope_clarification81.py')},{'path':str(p),'raw_sha256':sha(p)}],'self_hash_omitted':True,'original_freeze_unchanged':True}
f=OWN/'source_freeze81.complete-raw-manifest.json';f.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(p.name,sha(p));print(f.name,sha(f))
