"""Independent exact four-field control metadata consistency review."""
from __future__ import annotations
import copy
import datetime
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[5]
BASE=ROOT/'runs/20261007-companion-priority/pbps-actual-finite-history-tail-law87/frontier-label-repair87'
OUT=BASE/'independent-review'
def sha(raw):return hashlib.sha256(raw).hexdigest()
def desc(p,kind):
 raw=p.read_bytes()
 return {'path':p.relative_to(ROOT).as_posix(),'raw_sha256':sha(raw),'bytes':len(raw),'kind':kind}
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def put(name,value):
 p=OUT/name
 assert not p.exists(),'Preserve immutable review records'
 p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 return desc(p,'native-independent-output')
def delta(x,y,p=''):
 if type(x)!=type(y):return [p]
 if isinstance(x,dict):
  assert set(x)==set(y)
  return sum((delta(x[k],y[k],p+'/'+k) for k in x),[])
 if isinstance(x,list):
  assert len(x)==len(y)
  return sum((delta(v,w,p+'/'+str(i)) for i,(v,w) in enumerate(zip(x,y))),[])
 return [] if x==y else [p]
def at(x,pointer):
 for key in pointer.strip('/').split('/'):x=x[int(key)] if isinstance(x,list) else x[key]
 return x
def set_at(x,pointer,value):
 keys=pointer.strip('/').split('/')
 for key in keys[:-1]:x=x[int(key)] if isinstance(x,list) else x[key]
 x[int(keys[-1]) if isinstance(x,list) else keys[-1]]=value

proposal_path=BASE/'proposal87.json'
assert sha(proposal_path.read_bytes())=='845ddb5fba1310b28ac31405b8d28eeeadc2e7fd634c4630375c26b93aa0aac2'
p=load(proposal_path);before_path=Path(p['original']['path']);after_path=Path(p['proposed']['path'])
inputs=[desc(proposal_path,'exact-root-proposal')]
for path,d,kind in [(before_path,p['original'],'exact-before-snapshot'),(after_path,p['proposed'],'exact-proposed-successor')]:
 v=desc(path,kind);assert v['raw_sha256']==d['raw_sha256'] and v['bytes']==d['bytes'];inputs.append(v)
canonical=ROOT/p['target']
assert canonical.read_bytes()==before_path.read_bytes()
inputs.append(desc(canonical,'unchanged-current-canonical-cell'))
before=load(before_path);after=load(after_path);expected=copy.deepcopy(before)
assert p['required_changes']==4 and len(p['changes'])==4
actual_delta=delta(before,after)
required=['/shared_floor_audit/reason','/reuse_plan/decision_reason','/purification/duplicate_semantics_audit','/purification/canonicalization']
assert sorted(actual_delta)==sorted(required)
raw_expected=before_path.read_bytes().replace(b'\r\n',b'\n')
for c in p['changes']:
 assert c['pointer'] in required
 assert at(before,c['pointer'])==c['before'] and at(after,c['pointer'])==c['after']
 assert c['after']==c['before'].replace('78','76')
 set_at(expected,c['pointer'],c['after'])
 # Canonicalization sentence appears three times. Each occurrence is replaced by
 # its identical accepted successor; exact structural comparison constrains scope.
 old=json.dumps(c['before'],ensure_ascii=False).encode('utf-8')
 new=json.dumps(c['after'],ensure_ascii=False).encode('utf-8')
 raw_expected=raw_expected.replace(old,new)
assert after==expected and raw_expected==after_path.read_bytes()

publication_path=ROOT/p['publication']['path']
assert sha(publication_path.read_bytes())==p['publication']['raw_sha256']=='a8088607020c8685a5d675e7e5cce4de212aafb473e6a4877393d4da27c3a030'
purification=load(publication_path)['items'][0]['purification']
for c in p['changes']:
 key='duplicate_semantics_audit' if c['pointer'].endswith('duplicate_semantics_audit') else 'canonicalization'
 assert c['after']==purification[key]
inputs.append(desc(publication_path,'selected-already-accepted-purification-text'))
module=ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteHistoryTailLaw.lean'
assert sha(module.read_bytes())=='01fcff944f1dbd42be2af30063b9baf4e191e2cde959e008724387cadb4fc899'
producer=ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteJumpRecursion.lean'
producer_text=producer.read_text(encoding='utf-8')
assert 'Prospective header76' in producer_text and 'theorem actual_fixed_reference_finite_jump_recursion' in producer_text
parent='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteJumpRecursion.actual_fixed_reference_finite_jump_recursion'
assert parent in before['parents'] and before['parents']==after['parents']
assert 'ActualFiniteJumpRecursion.actual_fixed_reference_finite_jump_recursion' in module.read_text(encoding='utf-8')
assert before['reuse_plan']['reused_declarations']==after['reuse_plan']['reused_declarations']
assert before['status']==after['status']=='independently_verified'
inputs.extend([desc(module,'hash-and-consumed-parent-only'),desc(producer,'producer-identity-header-and-declaration-only')])
checks={
 'structural':'Exactly the four specified JSON string paths differ; all keys, list elements, real declaration parents, target statement, seals, source graph/source evidence, verification status and other fields are identical.',
 'wording':'Each of the four changed strings differs only by78→76. The three canonicalization sentences exactly reuse current publication purification.canonicalization; duplicate_semantics_audit exactly reuses current publication purification.duplicate_semantics_audit.',
 'parent':'Current01fc history-tail Lean consumes ActualFiniteJumpRecursion.actual_fixed_reference_finite_jump_recursion. Its producer source identifies header76. Existing actual77 product declaration and every real parent identity remain unchanged.',
 'raw_delta':'Original has229 CRLF line endings; exact proposed successor has229 LF line endings. After this explicit serialization normalization, the entire RAW difference is precisely the four78→76 substitutions. No hidden content or semantic rewrite.',
 'scope':'Metadata consistency only; independently_verified status is an unchanged input value, never a status transition made by this reviewer. No new theorem/SAU credit, compilation claim, full mathematics/source re-audit, canonical mutation or VERIFIED transition.'
}
chronology=put('frontier-label-repair87.chronology.json',{
 'reviewer':'/root/fresh_source86','proposal_creator':'/root','scope':'Exact control metadata four-field repair only',
 'sequence':['Read pinned proposal and exact before/after snapshots.','Reconstructed entire JSON delta: exactly four named string paths.','Independently checked unchanged actual parent declaration in current01fc Lean and producer76 source identity.','Compared every after string to current accepted publication a808 purification text.','Diagnosed229-byte size difference as229 CRLF→LF conversions; reconstructed exact successor bytes using newline normalization plus four labels.','Rehashed unchanged canonical before and all bound inputs; emitted native proposal-only acceptance.'],
 'diagnostics':[{'kind':'nonsemantic-serialization-difference','before_bytes':len(before_path.read_bytes()),'after_bytes':len(after_path.read_bytes()),'CRLF_to_LF_count':229,'blocking':False}],
 'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()
})
run=put('frontier-label-repair87.run.json',{
 'schema':'astis.independent.exact-control-metadata-repair-run87.v1','reviewer':'/root/fresh_source86',
 'proposal_raw_sha256':sha(proposal_path.read_bytes()),'inputs':inputs,'chronology':chronology,
 'actual_changed_paths':actual_delta,'changes':p['changes'],'checks':checks,'canonical_mutations':False,
 'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()
})
decision=put('frontier-label-repair87.decision.json',{
 'schema':'astis.independent.exact-control-metadata-repair-decision87.v1',
 'reviewer':'/root/fresh_source86','proposal_creator':'/root','independent_from_proposer':True,
 'verdict':'ACCEPTED_EXACT_FOUR_FIELD_CONTROL_METADATA_REPAIR','decision':'accepted',
 'reason':'All four stale prose labels78→76 match the actual consumed producer and the already accepted publication strings. Whole JSON delta is exactly four paths; real declaration parents, mathematical/source payloads, seals and verification status are unchanged. Explicit CRLF→LF normalization is nonsemantic.',
 'proposal':desc(proposal_path,'accepted-exact-proposal'),'proposal_sha256':sha(proposal_path.read_bytes()),
 'before':desc(before_path,'exact-original'),'after':desc(after_path,'exact-accepted-successor'),
 'publication':desc(publication_path,'unchanged-accepted-publication'),'full_module_sha256':sha(module.read_bytes()),
 'review_run_sha256':run['raw_sha256'],'changed_fields':p['changes'],'changed_field_count':4,
 'checks':checks,'blocking_deltas':[],
 'application':'Root sole integration writer may apply only the exact proposed successor bound here. Reviewer made no canonical edits.',
 'boundary':'Control metadata consistency acceptance only; no repeated mathematical/source audit, theorem verification transition or SAU credit.',
 'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()
})
outputs=[desc(z,'native-independent-output') for z in sorted(OUT.iterdir()) if z.is_file()]
manifest=put('frontier-label-repair87.closed-RAW-manifest.json',{
 'schema':'astis.independent.closed-raw-manifest87.v1','hash_mode':'RAW exact bytes','hash_algorithm':'SHA256',
 'inputs':inputs,'outputs':outputs,'closed':True,'decision_sha256':decision['raw_sha256'],'review_run_sha256':run['raw_sha256'],
 'closure':'All newly created outputs listed; only this manifest excludes itself to avoid recursive hashing. Its own RAW hash is reported externally.',
 'canonical_mutations':False,'source_extracts':[],'private_exclusion_list':[]
})
for d in inputs+outputs:
 z=ROOT/d['path'];assert sha(z.read_bytes())==d['raw_sha256'] and len(z.read_bytes())==d['bytes']
print(json.dumps({'decision':decision,'run':run,'manifest':manifest,'chronology':chronology},indent=2))
