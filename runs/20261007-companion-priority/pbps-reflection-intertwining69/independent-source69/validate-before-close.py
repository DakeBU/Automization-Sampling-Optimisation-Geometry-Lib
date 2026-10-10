import base64,copy,datetime,hashlib,json,os,pathlib
out=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def load(n):return json.loads((out/n).read_bytes())
assert not (out/'lease.final.json').exists() and not (out/'owned-manifest.json').exists()
for n in ['finalize-review.receipt.json','readback-review.receipt.json','author-review.receipt.json','official-binding-v3.receipt.json']:
 assert load(n)['actual_exit']==0 and load(n)['completed'] is True
assert load('official-binding.receipt.json')['actual_exit']==1 and load('official-binding-v2.receipt.json')['actual_exit']==1
run=load('review-run.json');core=copy.deepcopy(run);del core['run_sha256'];assert sha(canon(core))==run['run_sha256']
decision=load('source.0.decision.json');assert decision['review_run_sha256']==run['run_sha256'] and decision['reviewer_packet_sha256']==run['reviewer_packet_sha256']
assert load('current-input-manifest.json')['count']==62
for e in load('current-input-manifest.json')['inputs']:
 b=(out/e['name']).read_bytes();assert len(b)==e['RAW_bytes'] and sha(b)==e['RAW_sha256']
 assert b.replace(b'\r\n',b'\n')==(out/(e['name']+'.LF')).read_bytes() and sha(b.replace(b'\r\n',b'\n'))==e['LF_sha256']
source=load('primary419-NODE-EXCLUDED.json');line=load('whole-module446-line-coverage.json');coverage=load('finite-current-source-review-coverage.json')
assert source['count']==len(source['entries'])==419 and source['unclassified']==0
assert len({e['id'] for e in source['entries']})==419 and source['counts']=={'NODE':161,'EXCLUDED':258}
assert line['count']==len(line['entries'])==446 and line['unclassified']==0
assert sha(canon(source['entries']))==source['entries_canonical_sha256'] and sha(canon(line['entries']))==line['entries_canonical_sha256']
assert coverage['BODY']['steps']==6 and coverage['BODY']['lines']==308 and coverage['semantic_slots']['count']==7 and coverage['semantic_deltas']['blocking']==0
assert len(decision['semantic_slots'])==7 and len(decision['deltas'])==12 and not decision['repairs']
assert decision['publication_binding_sha256']=='571c2916738f1981c5074a9a5f4e1cdf3efce3f94fafd26670566c70c3b25152'
assert sha((out/'current.ReflectionIntertwining.RAW.lean').read_bytes())=='7bbaae1abd67305749d385153019061eb055a7968a707f919e7d9ac9fc21846d'
scripts=[p.name for p in out.glob('*.py')];assert 'write-CLOSED_LAST.py' in scripts and 'postclose-readonly.py' in scripts
result=dict(schema='source69-final-close-validation-v1',actual_pid=os.getpid(),utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),validated=True,whole_logical_run_sha256=run['run_sha256'],source_decision_RAW_sha256=sha((out/'source.0.decision.json').read_bytes()),reviewer_packet_canonical_sha256=decision['reviewer_packet_sha256'],source_math=419,module_lines=446,BODY_steps=6,slots=7,deltas=12,blocking=0,complete_input_count=62,helpers_and_failures_preserved=True,complete_named_payload_RAW_sha256=sha((out/'complete-named-review-decision-input-payload.json').read_bytes()),no_postclose_owned_writes_permitted=True)
(out/'close-validation-result.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,sort_keys=True))
