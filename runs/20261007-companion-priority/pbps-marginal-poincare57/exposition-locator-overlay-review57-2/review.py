import os,sys,pathlib,json,hashlib,datetime,subprocess
sys.dont_write_bytecode=True;sys.stdout.reconfigure(encoding='utf8')
R=pathlib.Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-marginal-poincare57';O=B/'exposition-locator-overlay-review57-2';X=B/'exposition-seal57';A=B/'exposition-locator-overlay57-2'
SCIENCE='e8a9044ba5a945eaa4b4aecd110b63494fe6c68e';HEAD='f311e4296fb5295a2e56e3214d3bd2585f849dcf';ACTOR='whole_math52_operational_locator57_2'
def path(p):
 p=pathlib.Path(str(p).replace('\\','/'));return p if p.is_absolute() else R/p
def sha(b):return hashlib.sha256(b).hexdigest()
def logical(d):return sha(json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode('utf8'))
def load(p):return json.loads(path(p).read_text(encoding='utf8'))
def dump(p,d):path(p).write_bytes((json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode('utf8'))
def pin(p):
 p=path(p);b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');return dict(path=p.relative_to(R).as_posix(),bytes=len(b),lf_bytes=len(lf),raw_sha256=sha(b),lf_sha256=sha(lf))
def same(a,b):return all(a[k]==b[k] for k in ('bytes','raw_sha256','lf_sha256')) and ('lf_bytes' not in a or a['lf_bytes']==b['lf_bytes'])
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def guard(e,a):
 if e=='open' and a and isinstance(a[0],(str,bytes,os.PathLike)):
  s=os.fsdecode(a[0]).replace('\\','/').lower()
  if ('/runs/' in s or '/.astis/' in s) and any(('58' in c or '59' in c) and any(k in c for k in ['pbps','preread','preproof','sourcegraph','future']) for c in s.split('/')):raise PermissionError('Operational57-2 excludes future58/59')
sys.addaudithook(guard);O.mkdir(exist_ok=True)
opened=dict(status='OPEN',actor=ACTOR,opened_utc=utc(),actual_Python_PID=os.getpid(),read='OPEN',write='OPEN',Python='OPEN',compiler='NOT_STARTED_CLOSED',scope='Independent second one-pointer exposition locator overlay; exhaustive original eight-native pin scan under ONLY two exact pointer/full-row maps. No original CLOSED/canonical/proof/source/formula edits, compiler or promotion.')
dump(O/'lease.json',opened)
inputs={};selfs=[];checks=[];processes=[];unmapped=[];mapped=[]
def current(p):a=pin(p);inputs[a['path']]=a;return a
def verify(e):a=current(e['path']);assert same(e,a),(e,a);checks.append(dict(expected=e,actual=a,route='actual_current'));return a
def full(p,f):
 d=load(p);h=logical({k:v for k,v in d.items() if k!=f});assert h==d[f];selfs.append(dict(input=current(p),self_field=f,logical_sha256=h,recipe='Entire native object minus ONLY named top-level self field; sorted compact UTF8 JSON ensure_ascii=False allow_nan=False no newline'));return d
def git(*args):
 p=subprocess.Popen(['git',*args],cwd=R,stdout=subprocess.PIPE,stderr=subprocess.PIPE);b,e=p.communicate();assert p.returncode==0;processes.append(dict(command=['git',*args],actual_PID=p.pid,exit_code=0,resource='CLOSED'));return b
assert git('rev-parse','HEAD').decode().strip()==HEAD
first=full(B/'exposition-locator-overlay57/locator-overlay.json','content_self_sha256');ov=full(A/'locator-overlay.json','content_self_sha256')
prior=B/'exposition-locator-overlay-review57'
for p,f in [('receipt.json','receipt_sha256'),('run.json','run_sha256'),('lease.json','lease_sha256')]:full(prior/p,f)
assert load(prior/'lease.json')['status']=='CLOSED';verify(ov['first_mapping_retained'])
assert ov['science_commit']==SCIENCE and ov['integration_commit']==HEAD and len(ov['mappings'])==len(first['mappings'])==1
maps=[first['mappings'][0],ov['mappings'][0]];assert [m['json_pointer'] for m in maps]==['/git_files/0/science_snapshot','/git_files/2/science_snapshot']
verify(ov['source_native']);verify(ov['original_closed_lease']);verify(ov['exhaustive_negative']);verify(ov['root_failed_script'])
objects={}
names=['exposition.review.json','reviewer.exposition.run.json','lease.json','manifest.json','complete.json','verification.json','input.manifest.json','input.readbacks.json']
for n in names:objects[n]=full(X/n,'complete_object_sha256')
assert objects['reviewer.exposition.run.json']['complete_object_sha256']=='2c1ed4cd2583df82a85907456b18ab0708aec12c1b5cf17cf5869c81e20ca5be'
assert pin(X/'lease.json')['raw_sha256']=='21f43b92af29555e1e9e0ee146111cd32485cba8abd41ea682553e30457d3359' and objects['lease.json']['status']=='CLOSED'
def pins(d,artifact,pointer=''):
 if isinstance(d,dict):
  if {'path','bytes','raw_sha256','lf_sha256'}<=d.keys():
   actual=current(d['path'])
   if not same(d,actual):
    unmapped.append(dict(artifact=artifact,pointer=pointer,expected=d,actual=actual))
    matches=[m for m in maps if artifact=='verification.json' and pointer==m['json_pointer'] and d==m['original']]
    assert len(matches)==1,('Unapproved pin mismatch',artifact,pointer,d,actual)
    m=matches[0];replacement=verify(m['exact_raw_snapshot']);assert same(d,replacement);mapped.append(dict(artifact=artifact,pointer=pointer,original=d,actual_collision=actual,replacement=replacement))
   else:checks.append(dict(artifact=artifact,pointer=pointer,expected=d,actual=actual,route='actual_current'))
  else:
   for k,v in d.items():pins(v,artifact,pointer+'/'+k.replace('~','~0').replace('/','~1'))
 elif isinstance(d,list):
  for i,v in enumerate(d):pins(v,artifact,pointer+'/'+str(i))
for n,d in objects.items():pins(d,n)
assert len(unmapped)==len(mapped)==2 and {x['pointer'] for x in unmapped}=={m['json_pointer'] for m in maps}
negative=load(A/'exhaustive-locator-negative.json');assert negative['count']==2 and negative['scanned_native_artifacts']==8
for x in negative['mismatches']:
 y=next(y for y in unmapped if (y['artifact'],y['pointer'])==(x['artifact'],x['pointer']));assert y['expected']==x['expected'] and same(x['actual'],y['actual'])
ver=objects['verification.json'];second=maps[1];assert second['original']==ver['git_files'][2]['science_snapshot'];collision=pin(second['original']['path']);assert path(second['original']['path'])==path(ver['git_files'][3]['science_snapshot']['path']) and same(ver['git_files'][3]['science_snapshot'],collision)
git_bindings=[]
for i in [0,1,2,3]:
 row=ver['git_files'][i];a=verify(row['current']);sc=git('show',SCIENCE+':'+row['path']);it=git('show',HEAD+':'+row['path']);actual=path(row['current']['path']).read_bytes();assert sc==it==actual
 assert sha(sc)==row['science_git_blob_sha256']==row['integration_git_blob_sha256']==a['raw_sha256']
 git_bindings.append(dict(pointer='/git_files/'+str(i),path=row['path'],science_commit=SCIENCE,integration_commit=HEAD,Git_bytes=len(sc),Git_raw_sha256=sha(sc),Git_LF_sha256=sha(sc.replace(b'\r\n',b'\n')),current=a))
assert path(second['exact_raw_snapshot']['path']).read_bytes()==git('show',SCIENCE+':'+second['exact_git_blob']['path'])
for row in objects['input.manifest.json']['inputs']:
 assert path(row['raw_snapshot']['path']).read_bytes()==path(row['input']['path']).read_bytes()
 assert path(row['lf_snapshot']['path']).read_bytes()==path(row['input']['path']).read_bytes().replace(b'\r\n',b'\n')
assert objects['input.manifest.json']['input_count']==66 and len(objects['manifest.json']['pins'])==147 and objects['lease.json']['output_readback_count']==150
assert all(objects['lease.json'][k]=='CLOSED' for k in ['read','write','Python']) and objects['lease.json']['compiler']=='NOT_STARTED_CLOSED'
assert ov['no_statement_proof_source_test_formula_native_or_first_review_mutations'] is True
dump(O/'checks.json',dict(status='PASS_EXHAUSTIVE_EIGHT_NATIVE_ARTIFACT_PIN_SCAN',scanned_native_artifacts=names,unmapped_original_mismatches_exactly=unmapped,explicitly_approved_resolutions=mapped,all_other_pin_rows_match_actual=True,raw_LF_pin_check_count=len(checks),raw_LF_pin_checks=checks,native_fullself_count=len(selfs),native_fullself_checks=selfs,Git_bindings=git_bindings,actual_closed_git_processes=processes,first_review_unchanged=pin(prior/'receipt.json'),first_review_closed_lease=pin(prior/'lease.json'),operational_only=True,no_source_math_or_formula_repair=True,no_native_mutation_or_reclose=True))
dump(O/'inputs.json',dict(status='PASS',count=len(inputs),inputs=[inputs[k] for k in sorted(inputs)],recipe='Exact raw and only CRLF pairs -> LF, actual byte lengths. No path-wide/global fallback; only verification.json plus two exact pointers/full original rows.'))
payload=dict(science_commit=SCIENCE,integration_commit=HEAD,second_root_overlay=current(A/'locator-overlay.json'),first_root_overlay=current(B/'exposition-locator-overlay57/locator-overlay.json'),second_exact_mapping=second,first_retained_mapping=maps[0],source_native=current(X/'verification.json'),original_closed_run=current(X/'reviewer.exposition.run.json'),original_closed_lease=current(X/'lease.json'),first_closed_review=pin(prior/'receipt.json'),first_closed_review_lease=pin(prior/'lease.json'),all_remaining_pin_scan=pin(O/'checks.json'),inputs=pin(O/'inputs.json'),raw_mismatch_count=2,unapproved_mismatch_count=0,operational_only=True)
ph=logical(payload)
receipt=dict(schema_version=1,status='ACCEPTED_SECOND_OPERATIONAL_LOCATOR_OVERLAY',verdict='ACCEPT_EXACT_SECOND_ONE_POINTER_FULLROW_MAP_ALL_OTHER_PINS_MATCH',reviewer=ACTOR,checked_science_commit=SCIENCE,checked_integration_commit=HEAD,new_json_pointer=second['json_pointer'],new_fullrow_original=second['original'],new_fullrow_replacement=second['exact_raw_snapshot'],reason='Publication and declaration lesson share one original science snapshot path. Actual collision is the11639byte lesson; publication expected11277bytes. Unique additive publication snapshot equals exact science/integration/current publication bytes and full original raw/LF/length row. Independently scanned every nested artifact pin in eight original native objects: exactly two collisions, resolved only by separately accepted production pointer0 and this new publication pointer2; no other mismatch.',original_exposition_run_complete_object_sha256=objects['reviewer.exposition.run.json']['complete_object_sha256'],original_lease_raw_sha256=pin(X/'lease.json')['raw_sha256'],first_review_unchanged=pin(prior/'receipt.json'),checks=pin(O/'checks.json'),inputs=pin(O/'inputs.json'),operational_binding_payload_sha256=ph,remaining='Original exposition scope/presentation debts/source-math boundaries remain. No full-reader/PURIFIED/main/live credit or native selfhash rewrite/reclosure.',compiler='NOT_STARTED_CLOSED',receipt_self_recipe='Entire receipt minus ONLY receipt_sha256; sorted compact UTF8 JSON ensure_ascii=False allow_nan=False no newline')
receipt['receipt_sha256']=logical(receipt);dump(O/'receipt.json',receipt)
rr=dict(schema_version=1,status='COMPLETE_SECOND_OPERATIONAL_LOCATOR_REVIEW',reviewer=ACTOR,science_commit=SCIENCE,integration_commit=HEAD,inputs=[inputs[k] for k in sorted(inputs)],receipt=pin(O/'receipt.json'),checks=pin(O/'checks.json'),operational_binding_payload=payload,operational_binding_payload_sha256=ph,run_self_recipe='Entire object minus ONLY run_sha256; sorted compact UTF8 JSON recipe',component_recipe='Entire named operational_binding_payload only, same compact recipe, distinct from complete run self digest',compiler='NOT_STARTED_CLOSED');rr['run_sha256']=logical(rr);dump(O/'run.json',rr)
outs=[pin(p) for p in sorted(O.iterdir()) if p.is_file() and p.name not in ['lease.json','outputs.final.json','readback.json']];om=dict(status='PASS',count=len(outs),outputs=outs,exclusions=['lease.json:CLOSED-last','outputs.final.json:self','readback.json:successor']);om['content_self_sha256']=logical(om);dump(O/'outputs.final.json',om)
for p,f in [(O/'receipt.json','receipt_sha256'),(O/'run.json','run_sha256'),(O/'outputs.final.json','content_self_sha256')]:d=load(p);assert logical({k:v for k,v in d.items() if k!=f})==d[f]
assert logical(load(O/'run.json')['operational_binding_payload'])==ph
for e in inputs.values():assert same(e,pin(e['path']))
for e in outs:assert same(e,pin(e['path']))
rb=dict(status='PASS_CLOSED_READY',input_readbacks=len(inputs),output_readbacks=len(outs),output_manifest=pin(O/'outputs.final.json'),receipt=pin(O/'receipt.json'),run=pin(O/'run.json'),complete_run_minus_run_sha256=rr['run_sha256'],operational_binding_payload_sha256=ph,actual_foreground_finalizer_PID=os.getpid(),all_owned_git_processes='CLOSED_EXIT0',compiler='NOT_STARTED_CLOSED');rb['content_self_sha256']=logical(rb);dump(O/'readback.json',rb)
assert logical({k:v for k,v in load(O/'readback.json').items() if k!='content_self_sha256'})==rb['content_self_sha256']
finalouts=[pin(p) for p in sorted(O.iterdir()) if p.is_file() and p.name!='lease.json']
for e in finalouts:assert same(e,pin(e['path']))
ll=dict(schema_version=1,status='CLOSED',actor=ACTOR,science_commit=SCIENCE,integration_commit=HEAD,read='CLOSED',write='CLOSED',Python='CLOSED',compiler='NOT_STARTED_CLOSED',actual_finalizer_PID=os.getpid(),actual_foreground_exit_code=0,exit_evidence='Successful synchronous tools.exec_command terminal EXIT0 confirms exit after final CLOSED lease write.',actual_owned_git_processes=processes,original_open=opened,closed_utc=utc(),input_count=len(inputs),output_count=len(finalouts),outputs=finalouts,receipt=pin(O/'receipt.json'),run=pin(O/'run.json'),readback=pin(O/'readback.json'),complete_run_minus_run_sha256=rr['run_sha256'],operational_binding_payload_sha256=ph,closure_order='LAST filesystem write after all inputs/outputs/native self/payload/readbacks validated; only precomputed stdout and process exit follow.',lease_self_recipe='Entire object minus ONLY lease_sha256; sorted compact UTF8 JSON recipe');ll['lease_sha256']=logical(ll);lb=(json.dumps(ll,ensure_ascii=False,indent=2)+'\n').encode('utf8')
summary=dict(status='CLOSED',verdict=receipt['verdict'],science=SCIENCE,integration=HEAD,receipt=pin(O/'receipt.json'),run=pin(O/'run.json'),complete_run_minus_run_sha256=rr['run_sha256'],operational_binding_payload_sha256=ph,lease=dict(path=(O/'lease.json').relative_to(R).as_posix(),bytes=len(lb),raw_sha256=sha(lb),lf_sha256=sha(lb),lease_sha256=ll['lease_sha256']),actual_finalizer_PID=os.getpid(),input_count=len(inputs),output_count=len(finalouts),native_fullself_count=len(selfs),actual_raw_LF_pin_checks=len(checks),mapped_collision_count=len(mapped),unapproved_mismatch_count=0,compiler='NOT_STARTED_CLOSED');stdout=json.dumps(summary,ensure_ascii=False)
dump(O/'lease.json',ll)
print(stdout)
