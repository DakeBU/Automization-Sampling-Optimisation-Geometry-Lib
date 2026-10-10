import datetime,hashlib,json,os,pathlib
out=pathlib.Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
canonical=lambda d:json.dumps(d,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8')
load=lambda n:json.loads((out/n).read_bytes())
assert not (out/'lease.final.json').exists()
for n in ['freeze-expectations-v2','review-overlay','readback-review']:assert load(n+'.receipt.json')['actual_exit']==0
r=load('review-run.json');v=dict(r);h=v.pop('run_sha256');assert sha(canonical(v))==h
entries=[]
for p in sorted(out.iterdir()):
    if p.is_file() and p.name not in ['manifest.final.json','lease.final.json']:
        b=p.read_bytes();lf=b.replace(b'\r\n',b'\n')
        entries.append(dict(name=p.name,RAW_bytes=len(b),RAW_sha256=sha(b),LF_bytes=len(lf),LF_sha256=sha(lf),LF_recipe='CRLF-to-LF only'))
m=dict(schema='type-ascription70-finite-native-manifest-v1',entries=entries,regular_file_count=len(entries),owned_file_count=len(entries)+2,
    finite_owned_closure_sha256=sha(canonical(entries)),excludes_exactly=['manifest.final.json','lease.final.json'])
(out/'manifest.final.json').write_text(json.dumps(m,sort_keys=True,indent=2)+'\n',encoding='utf-8')
d=load('decision.json')
lease=dict(schema='type-ascription70-CLOSED_LAST-native-lease-v1',status='CLOSED_LAST',owner='/root/independent_primary69',
    verdict=d['verdict'],owned_file_count=len(entries)+2,regular_file_count=len(entries),
    actual_lease_writer_pid=os.getpid(),closed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    whole_logical_run_sha256=h,whole_logical_deletes_ONLY_top_level_run_sha256=True,
    finite_owned_closure_sha256=m['finite_owned_closure_sha256'],manifest_RAW_sha256=sha((out/'manifest.final.json').read_bytes()),
    original_header_RAW_sha256=d['original_header_RAW_sha256'],proposed_header_RAW_sha256=d['proposed_header_RAW_sha256'],
    source_repairs=0,compiler_fix=False,root_reported_diagnostic_PID39696_EXIT1=True,old_CLOSED83_unchanged=True,
    input_count=12,finite_checks=6,original_lines=116,candidate_lines=118,
    no_Lean_compile_proofsearch_canonical_Git_ledger_Goal_edits=True,new_full_source_VERIFIED_credit=False,
    last_owned_write=True,postclose_writes_permitted=False,actual_writer_exit_observed_externally=True)
for label,key in [('freeze-expectations-v2','freeze'),('review-overlay','review'),('readback-review','readback')]:
    rr=load(label+'.receipt.json');lease['actual_'+key+'_pid']=rr['actual_pid'];lease['actual_'+key+'_exit']=rr['actual_exit']
for name,key in [('decision.json','decision'),('review-run.json','review_run'),('RAW-LF-input-payload.json','RAW_LF_input_payload'),('complete-named-review-decision-input.json','complete_named_payload')]:
    b=(out/name).read_bytes();lease[key]=dict(name=name,RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
(out/'lease.final.json').write_text(json.dumps(lease,sort_keys=True,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(actual_lease_writer_pid=os.getpid(),owned_files=len(entries)+2,decision_RAW_sha256=lease['decision']['RAW_sha256'],
    whole_logical_run_sha256=h,manifest_RAW_sha256=lease['manifest_RAW_sha256'],finite_owned_closure_sha256=lease['finite_owned_closure_sha256'],
    lease_RAW_sha256=sha((out/'lease.final.json').read_bytes())),sort_keys=True))
