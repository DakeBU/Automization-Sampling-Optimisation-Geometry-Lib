import os,sys,pathlib,json,hashlib,datetime,subprocess
sys.dont_write_bytecode=True;sys.stdout.reconfigure(encoding='utf8')
R=pathlib.Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-marginal-poincare57';O=B/'exposition-locator-overlay-review57';X=B/'exposition-seal57';A=B/'exposition-locator-overlay57'
SCIENCE='e8a9044ba5a945eaa4b4aecd110b63494fe6c68e';HEAD='f311e4296fb5295a2e56e3214d3bd2585f849dcf';ACTOR='whole_math52_operational_locator57'
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
  if ('/runs/' in s or '/.astis/' in s) and any(('58' in c or '59' in c) and any(k in c for k in ['pbps','preread','preproof','sourcegraph','future']) for c in s.split('/')):raise PermissionError('Operational57 excludes future58/59')
sys.addaudithook(guard)
O.mkdir(exist_ok=True)
opened=dict(status='OPEN',actor=ACTOR,opened_utc=utc(),actual_Python_PID=os.getpid(),read='OPEN',write='OPEN',Python='OPEN',compiler='NOT_STARTED_CLOSED',scope='Independent one-pointer exposition locator overlay57 only; no original CLOSED files/canonical/proof/source/formula edits, no compiler, no exposition/source/math promotion')
dump(O/'lease.json',opened)
inputs={};selfs=[];checks=[];processes=[]
def current(p):a=pin(p);inputs[a['path']]=a;return a
def verify(e):a=current(e['path']);assert same(e,a),(e,a);checks.append(dict(expected=e,actual=a));return a
def full(p,f):
 d=load(p);h=logical({k:v for k,v in d.items() if k!=f});assert h==d[f];selfs.append(dict(input=current(p),self_field=f,logical_sha256=h,recipe='Complete native object minus ONLY named top-level self field; sorted compact UTF8 JSON ensure_ascii=False allow_nan=False no newline'));return d
def git(*args):
 p=subprocess.Popen(['git',*args],cwd=R,stdout=subprocess.PIPE,stderr=subprocess.PIPE);b,e=p.communicate();assert p.returncode==0;processes.append(dict(command=['git',*args],actual_PID=p.pid,exit_code=p.returncode,resource='CLOSED'));return b
assert git('rev-parse','HEAD').decode().strip()==HEAD
ov=full(A/'locator-overlay.json','content_self_sha256');ver=full(X/'verification.json','complete_object_sha256');run=full(X/'reviewer.exposition.run.json','complete_object_sha256');lease=full(X/'lease.json','complete_object_sha256');full(X/'manifest.json','complete_object_sha256')
assert run['complete_object_sha256']=='2c1ed4cd2583df82a85907456b18ab0708aec12c1b5cf17cf5869c81e20ca5be'
assert pin(X/'lease.json')['raw_sha256']=='21f43b92af29555e1e9e0ee146111cd32485cba8abd41ea682553e30457d3359' and lease['status']=='CLOSED'
verify(ov['source_native']);verify(ov['source_closed_lease']);verify(ov['negative']['failed_root_script'])
assert ov['science_commit']==SCIENCE and ov['integration_commit']==HEAD and len(ov['mappings'])==1
m=ov['mappings'][0];assert m['json_pointer']=='/git_files/0/science_snapshot' and m['original']==ver['git_files'][0]['science_snapshot']
orig=m['original'];actual_collision=current(orig['path']);testrow=ver['git_files'][1]['science_snapshot']
assert path(orig['path'])==path(testrow['path']) and not same(orig,actual_collision) and same(testrow,actual_collision)
replacement=verify(m['exact_raw_snapshot']);assert same(orig,replacement)
assert m['exact_git_blob']['commit']==SCIENCE and m['exact_git_blob']['path']==ver['git_files'][0]['path']
git_bindings=[]
for row in ver['git_files'][:2]:
 a=verify(row['current']);sc=git('show',SCIENCE+':'+row['path']);it=git('show',HEAD+':'+row['path']);assert sc==it==path(row['current']['path']).read_bytes()
 assert sha(sc)==row['science_git_blob_sha256']==row['integration_git_blob_sha256']==a['raw_sha256']
 git_bindings.append(dict(path=row['path'],science_commit=SCIENCE,integration_commit=HEAD,science_git_bytes=len(sc),science_git_raw_sha256=sha(sc),integration_git_raw_sha256=sha(it),current=a))
assert path(m['exact_raw_snapshot']['path']).read_bytes()==git('show',SCIENCE+':'+m['exact_git_blob']['path'])
for row in ov['unchanged'].values():verify(row)
assert ov['no_statement_proof_source_test_formula_or_native_receipt_changes'] is True
for p in [X/'verification.json',X/'reviewer.exposition.run.json',X/'lease.json',X/'manifest.json']:current(p)
dump(O/'checks.json',dict(status='PASS_OPERATIONAL_ONE_POINTER_LOCATOR',science=SCIENCE,integration=HEAD,json_pointer=m['json_pointer'],original_expected=orig,original_actual_collision=actual_collision,collision_is_actual_Test_bytes=True,one_fullrow_mapping=m,exact_replacement=replacement,git_bindings=git_bindings,native_selfchecks=selfs,actual_raw_LF_pin_checks=checks,actual_processes=processes,root_initial_negative=ov['negative'],no_native_rewrite_or_reclose=True,no_mathematical_source_statement_formula_repair=True,scope='Operational locator map only, keyed by exact JSON pointer plus complete expected original row. Every other original byte and self digest remains native. No path-wide/global fallback or alias.'))
dump(O/'inputs.json',dict(status='PASS',count=len(inputs),inputs=[inputs[k] for k in sorted(inputs)],raw_LF_recipe='Actual bytes and only CRLF pairs -> LF; exact lengths; no JSON reserialization substitutes'))
payload=dict(science_commit=SCIENCE,integration_commit=HEAD,root_overlay=current(A/'locator-overlay.json'),one_exact_mapping=m,source_native=current(X/'verification.json'),original_closed_run=current(X/'reviewer.exposition.run.json'),original_closed_lease=current(X/'lease.json'),original_collision=actual_collision,correct_unique_replacement=replacement,checks=pin(O/'checks.json'),inputs=pin(O/'inputs.json'),operational_only=True,no_original_native_change=True,no_source_math_or_exposition_credit=True)
ph=logical(payload)
receipt=dict(schema_version=1,status='ACCEPTED_OPERATIONAL_LOCATOR_OVERLAY',verdict='ACCEPT_EXACT_ONE_POINTER_FULLROW_LOCATOR_MAP_ONLY',reviewer=ACTOR,checked_science_commit=SCIENCE,checked_integration_commit=HEAD,original_native_run_sha256=run['complete_object_sha256'],original_closed_lease=pin(X/'lease.json'),json_pointer=m['json_pointer'],fullrow_original=orig,fullrow_replacement=replacement,reason='The production and Test snapshot locators collide exactly. The actual shared snapshot is the unchanged6252byte Test, while the original production row expects10017bytes. The additive unique production snapshot equals exact science/integration/current production bytes and the complete original expected raw/LF row. Admit only this pointer/full-row mapping; original run/verification/lease self hashes remain unchanged.',checks=pin(O/'checks.json'),inputs=pin(O/'inputs.json'),operational_binding_payload_sha256=ph,remaining='Original bounded exposition scope and presentation debts remain; this does not repair/prove mathematical/source claims or promote full-reader/main/live/PURIFIED.',compiler='NOT_STARTED_CLOSED',receipt_self_recipe='Complete receipt minus ONLY receipt_sha256; sorted compact UTF8 JSON')
receipt['receipt_sha256']=logical(receipt);dump(O/'receipt.json',receipt)
rr=dict(schema_version=1,status='COMPLETE_OPERATIONAL_LOCATOR_REVIEW',reviewer=ACTOR,science_commit=SCIENCE,integration_commit=HEAD,inputs=[inputs[k] for k in sorted(inputs)],receipt=pin(O/'receipt.json'),checks=pin(O/'checks.json'),operational_binding_payload=payload,operational_binding_payload_sha256=ph,run_self_recipe='Complete object minus ONLY run_sha256; sorted compact UTF8 ensure_ascii=False allow_nan=False no newline',component_recipe='Entire named operational_binding_payload only, same compact recipe; distinct from complete run self digest',actual_git_processes=processes,compiler='NOT_STARTED_CLOSED')
rr['run_sha256']=logical(rr);dump(O/'run.json',rr)
outs=[pin(p) for p in sorted(O.iterdir()) if p.is_file() and p.name not in ['lease.json','outputs.final.json','readback.json']]
om=dict(status='PASS',outputs=outs,count=len(outs),exclusions=['lease.json:last closure','outputs.final.json:self','readback.json:successor']);om['content_self_sha256']=logical(om);dump(O/'outputs.final.json',om)
for p,f in [(O/'receipt.json','receipt_sha256'),(O/'run.json','run_sha256'),(O/'outputs.final.json','content_self_sha256')]:d=load(p);assert logical({k:v for k,v in d.items() if k!=f})==d[f]
assert logical(load(O/'run.json')['operational_binding_payload'])==ph
for e in inputs.values():assert same(e,pin(e['path']))
for e in outs:assert same(e,pin(e['path']))
rb=dict(status='PASS_CLOSED_READY',input_readbacks=len(inputs),output_readbacks=len(outs),output_manifest=pin(O/'outputs.final.json'),receipt=pin(O/'receipt.json'),run=pin(O/'run.json'),complete_run_minus_run_sha256=rr['run_sha256'],operational_binding_payload_sha256=ph,actual_foreground_finalizer_PID=os.getpid(),all_owned_git_processes='CLOSED_EXIT0',compiler='NOT_STARTED_CLOSED');rb['content_self_sha256']=logical(rb);dump(O/'readback.json',rb)
assert logical({k:v for k,v in load(O/'readback.json').items() if k!='content_self_sha256'})==rb['content_self_sha256']
finalouts=[pin(p) for p in sorted(O.iterdir()) if p.is_file() and p.name!='lease.json']
for e in finalouts:assert same(e,pin(e['path']))
ll=dict(schema_version=1,status='CLOSED',actor=ACTOR,science_commit=SCIENCE,integration_commit=HEAD,read='CLOSED',write='CLOSED',Python='CLOSED',compiler='NOT_STARTED_CLOSED',actual_finalizer_PID=os.getpid(),actual_foreground_exit_code=0,exit_evidence='Successful synchronous tools.exec_command terminal EXIT0 confirms exit after final CLOSED lease write.',actual_owned_git_processes=processes,original_open=opened,closed_utc=utc(),input_count=len(inputs),output_count=len(finalouts),outputs=finalouts,receipt=pin(O/'receipt.json'),run=pin(O/'run.json'),readback=pin(O/'readback.json'),complete_run_minus_run_sha256=rr['run_sha256'],operational_binding_payload_sha256=ph,closure_order='LAST filesystem write after all input/output/native self/payload/readback checks; only precomputed stdout and process exit follow.',lease_self_recipe='Complete object minus ONLY lease_sha256; sorted compact UTF8 JSON ensure_ascii=False allow_nan=False no newline')
ll['lease_sha256']=logical(ll);lb=(json.dumps(ll,ensure_ascii=False,indent=2)+'\n').encode('utf8')
summary=dict(status='CLOSED',verdict=receipt['verdict'],science=SCIENCE,integration=HEAD,receipt=pin(O/'receipt.json'),run=pin(O/'run.json'),complete_run_minus_run_sha256=rr['run_sha256'],operational_binding_payload_sha256=ph,lease=dict(path=(O/'lease.json').relative_to(R).as_posix(),bytes=len(lb),raw_sha256=sha(lb),lf_sha256=sha(lb),lease_sha256=ll['lease_sha256']),actual_finalizer_PID=os.getpid(),input_count=len(inputs),output_count=len(finalouts),native_fullself_count=len(selfs),actual_raw_LF_pin_checks=len(checks),compiler='NOT_STARTED_CLOSED')
stdout=json.dumps(summary,ensure_ascii=False)
dump(O/'lease.json',ll)
print(stdout)
