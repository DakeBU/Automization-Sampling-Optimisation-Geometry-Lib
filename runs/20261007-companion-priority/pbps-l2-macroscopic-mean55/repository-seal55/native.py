from common import *
assert git('rev-parse','HEAD')==HEAD and git('rev-parse','HEAD^')==SCI and git('status','--porcelain','--untracked-files=no')==''
maps={}
def add(p,s):maps.setdefault(str(path(p)),[]).append(str(path(s)))
for p,s in load(B/'source-metadata-repair55/overlay.json')['original_source_input_snapshot_mapping'].items():add(p,s)
for p,s in [(AUDIT,B/'source-admission-before.0.raw.snapshot.audit.json'),(CELL,B/'source-admission-before.0.raw.snapshot.cell.json'),(CELL,B/'exact-verification55/before.cell.raw.snapshot.json'),('runs/substantive_advances.jsonl',B/'exact-verification55/before.ledger.raw.snapshot.jsonl')]:add(p,s)
for row in load(B/'verified-inputs.before-shared-integration.json')['mappings']:
 assert equal(row['snapshot']) and equal(row['original'],row['snapshot']['path']);add(row['original']['path'],row['snapshot']['path'])
for e in load(B/'exact-verification55/native-input-checks.json')['exact_historical_mappings']:add(e['expected']['path'],e['actual']['path'])
checks=[];unresolved=[]
def check(e,ctx):
 if equal(e):checks.append(dict(context=ctx,original=e,actual=pin(e['path']),mapping=None));return
 for s in maps.get(str(path(e['path'])),[]):
  if equal(e,s):checks.append(dict(context=ctx,original=e,actual=pin(s),mapping=dict(original_path=e['path'],snapshot_path=pin(s)['path'],both_raw_LF_exact=True)));return
 unresolved.append(dict(context=ctx,original=e,current=pin(e['path']),authorized_candidates=maps.get(str(path(e['path'])),[])))
counts={}
for p,k in [('math-freeze.json','inputs'),('whole-math55/run.json','actual_inputs'),('whole-math55/outputs.json','actual_output_pins'),('reviewer.source.run.json','inputs'),('reviewer.source.run.json','outputs'),('independent-review55/run.json','inputs'),('independent-review55/run.json','outputs'),('exact-verification55/run.json','actual_inputs'),('exact-verification55/outputs.json','actual_output_pins')]:
 rows=load(B/p)[k];counts[p+':'+k]=len(rows)
 for e in rows:check(e,p+':'+k)
for e in load(B/'exact-verification55/committed-inputs.json')['bindings']:check(e['current'],'scientific1821 exact original current pin')
selfs=[]
for p,f in [('whole-math55/run.json','run_sha256'),('reviewer.source.run.json','run_sha256'),('source.0.review.json','review_run_sha256'),('reviewer.source.lease.json','lease_run_sha256'),('source.review.lease.json','lease_run_sha256'),('independent-review55/run.json','run_sha256'),('independent-review55/source.1.review.json','review_run_sha256'),('independent-review55/reviewer.source.repair.lease.json','lease_run_sha256'),('source-metadata-repair55/source.repair.review.lease.json','lease_run_sha256'),('exact-verification55/run.json','run_sha256'),('exact-verification55/lease.json','lease_run_sha256'),('exact-verification55/receipt.json','receipt_sha256'),('verified.json','verified_payload_sha256')]:selfs.append(selfcheck(B/p,f))
for p in ['whole-math55/run.json','exact-verification55/run.json']:
 d=load(B/p);assert logical(d['run_binding_payload'])==d['review_run_binding_sha256']
assert logical(load(B/'independent-review55/payload.json'))==load(B/'independent-review55/run.json')['run_payload_sha256']
for p,n,h in [('result0.json','decoder_payload','decoder_payload_sha256'),('run.json','run_payload','run_payload_sha256'),('lease.json','closure_payload','closure_payload_sha256')]:
 d=load(B/'anonymous-decoder'/p);selfs.append(selfcheck(B/'anonymous-decoder'/p,'logical_sha256'));assert logical(d[n])==d[h]
for e in load(B/'whole-math55/checks.json')['preproof_complete_native_runs']:assert equal(e['input']);selfs.append(selfcheck(e['input']['path']))
leases=[]
for p in ['whole-math55/lease.json','exact-verification55/lease.json','reviewer.source.lease.json','source.review.lease.json','independent-review55/reviewer.source.repair.lease.json','source-metadata-repair55/source.repair.review.lease.json','anonymous-decoder/lease.json','root.integration.0.lease.json','root.desktop-capture55.lease.json']:
 d=load(B/p);assert d['status']=='CLOSED'
 for k in ['read','write','Python','compiler','read_lease','write_lease','Python_lease','compiler_lease']:
  if k in d:assert d[k] in ['CLOSED','NOT_STARTED_CLOSED'],(p,k,d[k])
 leases.append(dict(input=pin(B/p),actual_native_fields=d))
source=load(B/'independent-review55/source.1.review.json');assert source['status']=='ACCEPTED_SCOPED_SOURCE_FIDELITY_AFTER_METADATA_REPAIR' and not source['source_or_math_change'] and load(B/'source.0.review.json')['status']=='BLOCKED_METADATA_LOCATOR_ONLY'
# Exact integration changes only explicitly owned shared/files55; no future files.
raw=subprocess.check_output(['git','diff-tree','--no-commit-id','--name-only','-r','-z',HEAD],cwd=R);names=[x.decode() for x in raw.split(b'\0') if x]
shared={e['path'] for e in load(B/'integration.notes.json')['shared_files']}
assert all(n in shared or n.startswith(B.relative_to(R).as_posix()+'/') for n in names) and not any('/repository-seal55/' in n or re.search(r'(?:56|57)(?:/|\.)',n) for n in names)
cp=subprocess.Popen(['git','cat-file','--batch'],cwd=R,stdin=subprocess.PIPE,stdout=subprocess.PIPE);data,_=cp.communicate(''.join(HEAD+':'+n+'\n' for n in names).encode());assert cp.returncode==0;pos=0;entries=[]
for n in names:
 end=data.index(b'\n',pos);h=data[pos:end].decode().split();size=int(h[2]);b=data[end+1:end+1+size];pos=end+size+2;actual=pin(n);assert sha(b.replace(b'\r\n',b'\n'))==actual['lf_sha256'];entries.append(dict(path=n,Git_blob=h[0],Git_raw_sha256=sha(b),Git_LF_sha256=sha(b.replace(b'\r\n',b'\n')),current=actual))
assert pos==len(data)
for p in ['AutoSamplingTheory/ExampleCases/ProximalBPS/L2MacroscopicMean.lean','Tests/ProximalBPSL2MacroscopicMean.lean','website/content/publications/pbps-l2-macroscopic-mean.json','website/content/declaration_lessons/pbps-l2-macroscopic-mean.json',AUDIT]:
 old=subprocess.check_output(['git','show',SCI+':'+p],cwd=R);new=subprocess.check_output(['git','show',HEAD+':'+p],cwd=R);assert old==new and sha(new.replace(b'\r\n',b'\n'))==pin(p)['lf_sha256']
dump('native-inputs.json',dict(status='PASS' if not unresolved else 'BLOCKED',checked_science=SCI,checked_integration=HEAD,counts=counts,checks=checks,mapped_count=sum(e['mapping'] is not None for e in checks),unresolved=unresolved,full_native_self_recipes=selfs,actual_closed_native_leases=leases,science_original_git_bindings=1821,integration_owned_git_entries=entries,integration_owned_count=len(entries),scientific_production_Test_audit_lesson_publication_unchanged=True,tracked_tree_clean=True,compiler_started=False))
print(json.dumps(dict(status='PASS' if not unresolved else 'BLOCKED',counts=counts,pin_checks=len(checks),mapped=sum(e['mapping'] is not None for e in checks),unresolved=unresolved,integration_entries=len(entries),complete_native_selfs=len(selfs)),ensure_ascii=False));assert not unresolved
