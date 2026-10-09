import hashlib,json,os,pathlib
out=pathlib.Path(__file__).resolve().parent;repo=pathlib.Path(r'E:\Samplinglib')
def sha(b):return hashlib.sha256(b).hexdigest()
checks=[]
for rel,leasehash,total in [
 ('runs/20261007-companion-priority/pbps-reflection-rotation-preproof69/independent-primary69','2d168d568a260f2cc18fba260a5bd7c1ac45cb41602f6a359df3d16b387aec93',82),
 ('runs/20261007-companion-priority/pbps-reflection-intertwining69/independent-source69','ae74df4c28b149a46c0e28a4a87905b2585921b555fbac6abdbe375326f2444c',211)]:
 p=repo/rel;assert sha((p/'lease.final.json').read_bytes())==leasehash
 m=json.loads((p/'owned-manifest.json').read_bytes());entries=m['regular_file_entries'];assert len(entries)==total-2
 for e in entries:
  b=(p/e['name']).read_bytes();assert len(b)==e['RAW_bytes'] and sha(b)==e['RAW_sha256'] and sha(b.replace(b'\r\n',b'\n'))==e['LF_sha256']
 assert len([x for x in p.rglob('*') if x.is_file()])==total
 checks.append(dict(path=str(p),owned_file_count=total,regular_hashes_verified=len(entries),lease_RAW_sha256=leasehash,manifest_RAW_sha256=sha((p/'owned-manifest.json').read_bytes()),opaque_hash_only=True,no_prior_candidate_verdict_or_review_used=True))
parent=repo/'AutoSamplingTheory/ExampleCases/ProximalBPS/ReflectionIntertwining.lean';b=parent.read_bytes();fm=json.loads((out/'parent69.literal-Prop.fragment-map.json').read_bytes());a,z=fm['source_RAW_range_end_exclusive']
assert sha(b)==fm['full_parent_RAW_sha256']
assert b[a:z]==(out/'parent69.literal-Prop.exactraw.fragment.lean').read_bytes()
result=dict(schema='header-source70-opaque-prior-closure-validation-v1',actual_pid=os.getpid(),closures=checks,full_parent_opaque_hash_verified=True,parent_fragment_is_literal_exact_RAW_slice=True,no_proof_body_used=True,no_closed_file_writes=True)
(out/'opaque-prior-closures70.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,sort_keys=True))
