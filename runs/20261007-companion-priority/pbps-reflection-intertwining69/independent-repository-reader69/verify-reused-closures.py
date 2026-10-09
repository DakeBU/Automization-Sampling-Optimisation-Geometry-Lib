import hashlib,json,os,pathlib
out=pathlib.Path(__file__).resolve().parent;run=out.parent
def sha(b):return hashlib.sha256(b).hexdigest()
checks=[]
source=run/'independent-source69';lease=(source/'lease.final.json').read_bytes();assert sha(lease)=='ae74df4c28b149a46c0e28a4a87905b2585921b555fbac6abdbe375326f2444c'
m=json.loads((source/'owned-manifest.json').read_bytes());assert m['regular_file_count']==209
for e in m['regular_file_entries']:
 b=(source/e['name']).read_bytes();assert len(b)==e['RAW_bytes'] and sha(b)==e['RAW_sha256'] and sha(b.replace(b'\r\n',b'\n'))==e['LF_sha256']
assert len([p for p in source.rglob('*') if p.is_file()])==211
checks.append(dict(scope='source211',native_owned_count=211,regular_hashes_verified=209,lease_RAW_sha256=sha(lease),whole_logical_sha256='f1e5024fe6afdaedae4ac5f9b2dfc48bc86e09da51b490212c392bbc9bf2ce90'))
for folder,total,logical in [('independent-math69',112,'11dbc903eceb91f2d53fb58397299cfe74acd746e8dc6145b60f38ef2bcbe3e1'),('exact-science-verification69',159,'94460a9f1cd9a58d6f437e56a62f6ed578aa52ff299468d54a4be4ef4e43676d')]:
 p=run/folder;lease=(p/'lease.final.json').read_bytes();l=json.loads(lease);assert l['status']=='CLOSED_LAST' and l['owned_file_count_including_self']==total and l['whole_logical_run_sha256']==logical
 entries=l['all_owned_outputs_except_only_self'];assert len(entries)==total-1
 for e in entries:
  b=pathlib.Path(e['path']).read_bytes();lf=b.replace(b'\r\n',b'\n')
  assert len(b)==e['raw_bytes'] and sha(b)==e['raw_sha256'] and len(lf)==e['lf_bytes'] and sha(lf)==e['lf_sha256']
 assert len([x for x in p.rglob('*') if x.is_file()])==total
 checks.append(dict(scope=folder,native_owned_count=total,regular_hashes_verified=total-1,lease_RAW_sha256=sha(lease),whole_logical_sha256=logical,VERIFIED=l['VERIFIED']))
blind=run/'anonymous-decoder';l=json.loads((blind/'lease.json').read_bytes());m=json.loads((blind/'manifest.json').read_bytes());assert l['status']=='CLOSED_LAST' and l['owned_regular_file_count']==17
assert sha((blind/'manifest.json').read_bytes())==l['manifest_raw_sha256']
for e in m['entries']:
 b=(blind/e['path']).read_bytes();assert len(b)==e['raw_bytes'] and sha(b)==e['raw_sha256']
assert len(m['entries'])==15 and len(m['all_owned_files'])==17
checks.append(dict(scope='blind17 native subset of root adopted container',native_owned_count=17,regular_hashes_verified=15,lease_RAW_sha256=sha((blind/'lease.json').read_bytes()),whole_logical_sha256=l['whole_logical_sha256']))
result=dict(schema='repository-reader69-reused-native-integrity-v1',actual_pid=os.getpid(),all_reused_native_closures_unchanged=True,all_RAW_LF_or_native_RAW_hashes_verified=True,closure_checks=checks,math_and_source_verdicts_reused_not_reproved=True,no_old_native_writes=True,final_reader_aggregate_packet_not_yet_seen=True)
(out/'reused-native-closure-integrity.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,sort_keys=True))
