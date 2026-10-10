from common import *
assert git('rev-parse','HEAD')==SCI
overlay=load(B/'source-metadata-repair55/overlay.json');maps={}
for p,s in overlay['original_source_input_snapshot_mapping'].items():maps.setdefault(p,[]).append(s)
for p,s in [(AUDIT,B/'source-admission-before.0.raw.snapshot.audit.json'),(CELL,B/'source-admission-before.0.raw.snapshot.cell.json')]: maps.setdefault(p,[]).append(str(s))
for p,s in [(str(B/'source-metadata-repair55/source.repair.review.lease.json'),B/'independent-review55/provided.opening.lease.raw.snapshot.json'),(str(B/'anonymous-decoder/lease.json'),B/'anonymous-decoder/initial-lease.raw.snapshot.json')]:maps.setdefault(path(p).relative_to(R).as_posix(),[]).append(str(s))
checked=[];failed=[];mapped=[]
def check(e,context):
 if not isinstance(e,dict) or not all(k in e for k in ['path','raw_sha256','lf_sha256']):return
 pp=path(e['path']);label=pp.relative_to(R).as_posix() if pp.is_relative_to(R) else pp.as_posix()
 if equal(e):checked.append(dict(context=context,expected=e,actual=pin(pp),mapping=None));return
 for s in maps.get(label,[]):
  if path(s).exists() and equal(e,s):
   row=dict(context=context,expected=e,actual=pin(s),mapping=dict(original_path=label,snapshot_path=pin(s)['path'],reason='Exact reviewed historical metadata/open lease before bytes; raw AND LF AND bytes matched'))
   checked.append(row);mapped.append(row);return
 failed.append(dict(context=context,expected=e,current=pin(pp),authorized_candidates=maps.get(label,[])))
def rows(p,key):
 d=load(p)
 for e in d[key]:check(e,str(p)+':'+key)
 return len(d[key])
counts={}
counts['math_freeze']=rows(B/'math-freeze.json','inputs');assert counts['math_freeze']==282
counts['whole_math_inputs']=rows(B/'whole-math55/run.json','actual_inputs');assert counts['whole_math_inputs']==1753
counts['whole_math_outputs']=rows(B/'whole-math55/outputs.json','actual_output_pins');assert counts['whole_math_outputs']==29
native=[]
native.append(selfcheck(B/'whole-math55/run.json'))
w=load(B/'whole-math55/run.json');assert logical(w['run_binding_payload'])==w['review_run_binding_sha256']
assert logical(load(B/'whole-math55/outputs.json')['actual_output_pins'])==load(B/'whole-math55/outputs.json')['output_list_logical_sha256']
wl=load(B/'whole-math55/lease.json');assert wl['status']=='CLOSED' and wl['exit_code']==0
for k in ['receipt','run','actual_compiler_CLOSED_lease','actual_outputs_manifest','readback']:check(wl[k],'whole_math_CLOSED_lease:'+k)
for p,field in [('source.0.review.json','review_run_sha256'),('reviewer.source.run.json','run_sha256'),('reviewer.source.lease.json','lease_run_sha256'),('independent-review55/source.1.review.json','review_run_sha256'),('independent-review55/run.json','run_sha256'),('independent-review55/reviewer.source.repair.lease.json','lease_run_sha256'),('source-metadata-repair55/source.repair.review.lease.json','lease_run_sha256')]:native.append(selfcheck(B/p,field))
for p,ik,ok in [('reviewer.source.run.json','inputs','outputs'),('independent-review55/run.json','inputs','outputs')]:
 counts[p+'_inputs']=rows(B/p,ik);counts[p+'_outputs']=rows(B/p,ok)
assert counts['reviewer.source.run.json_inputs']==297 and counts['independent-review55/run.json_inputs']==321
for p in ['source.0.review.json','independent-review55/source.1.review.json']:rows(B/p,'input_artifacts')
sr=load(B/'independent-review55/source.1.review.json');sn=load(B/'source.0.review.json');rr=load(B/'independent-review55/run.json')
assert sr['status']=='ACCEPTED_SCOPED_SOURCE_FIDELITY_AFTER_METADATA_REPAIR' and sr['verdict']=='equivalent-after-elaboration' and not sr['blocking'] and not sr['source_or_math_change']
assert sn['status']=='BLOCKED_METADATA_LOCATOR_ONLY' and sn['mathematical_source_verdict']=='equivalent-after-elaboration'
assert rr['review_run_sha256']==sr['review_run_sha256'] and logical(load(B/'independent-review55/payload.json'))==rr['run_payload_sha256']
assert len(overlay['operations'])==2
for op in overlay['operations']:
 for k in ['before_pin','after_pin']:check(op[k],'overlay:'+k)
 before=path(op['before_pin']['path']).read_bytes();after=path(op['after_pin']['path']).read_bytes();assert before.replace(op['before'].encode(),op['after'].encode())==after
for p in ['reviewer.source.lease.json','source.review.lease.json','independent-review55/reviewer.source.repair.lease.json','source-metadata-repair55/source.repair.review.lease.json']:
 d=load(B/p);assert d['status']=='CLOSED'
 for k in ['read','write','Python','compiler','read_lease','write_lease','Python_lease','compiler_lease']:
  if k in d:assert d[k] in ['CLOSED','NOT_STARTED_CLOSED'],(p,k,d[k])
# Actual committed file entries via stdin cat-file batch (no long argv).
raw=subprocess.check_output(['git','diff-tree','--no-commit-id','--name-only','-r','-z',SCI],cwd=R);names=[x.decode('utf-8') for x in raw.split(b'\0') if x];assert len(names)==1821
cp=subprocess.Popen(['git','cat-file','--batch'],cwd=R,stdin=subprocess.PIPE,stdout=subprocess.PIPE);payload=''.join(SCI+':'+n+'\n' for n in names).encode();data,_=cp.communicate(payload);assert cp.returncode==0
pos=0;bindings=[]
for n in names:
 end=data.index(b'\n',pos);head=data[pos:end].decode().split();size=int(head[2]);bb=data[end+1:end+1+size];pos=end+size+2
 current=pin(n);assert sha(bb.replace(b'\r\n',b'\n'))==current['lf_sha256'],n
 bindings.append(dict(path=n,git_blob=head[0],git_type=head[1],git_bytes=size,git_raw_sha256=sha(bb),git_lf_sha256=sha(bb.replace(b'\r\n',b'\n')),current=current,LF_matches=True))
assert pos==len(data)
dump('committed-inputs.json',dict(status='PASS',checked_commit=SCI,parent=BASE,count=1821,bindings=bindings,bindings_logical_sha256=logical(bindings)))
dump('native-input-checks.json',dict(status='PASS' if not failed else 'BLOCKED',counts=counts,checks=checked,exact_historical_mappings=mapped,unresolved=failed,complete_native_runs=native,whole_math_named_payload_sha256=w['review_run_binding_sha256'],source_named_payload_sha256=rr['run_payload_sha256']))
print(json.dumps(dict(counts=counts,matching=len(checked),historical_mappings=len(mapped),unresolved=failed,committed=1821),ensure_ascii=False))
assert not failed
