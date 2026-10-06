from pathlib import Path
import json,hashlib,subprocess,re,sys,datetime
sys.path.insert(0,'tools')
import astis,astis_publication as pub,astis_advance as adv
R=Path('runs/20261007-companion-priority/gaussian-laplace-domain')
D=Path('runs/20261007-companion-priority/anonymous-decoder-29')
C='1f746dc634b95f780b7f5bffe04c50f9bb4f21e3'; V='picard_commit_verifier_20261005'
def sha(b):return hashlib.sha256(b).hexdigest()
def fp(p):
 b=Path(p).read_bytes();return dict(path=str(p).replace('\\','/'),raw_sha256=sha(b),lf_sha256=sha(b.replace(b'\r\n',b'\n')),bytes=len(b))
def read(p):return json.loads(Path(p).read_bytes())
def verify(x,p=None):
 y=fp(p or x['path'])
 for k in ('raw_sha256','lf_sha256','bytes'):
  if k in x:assert x[k]==y[k],(y['path'],k)
 return y
def diff(a,b,path=''):
 if isinstance(a,dict) and isinstance(b,dict):
  return sum([diff(a.get(k),b.get(k),path+'/'+k) for k in sorted(set(a)|set(b))],[])
 return [] if a==b else [dict(path=path,before=a,after=b)]
def emit(name,obj):
 p=R/name;body=(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode()
 if p.exists():assert p.read_bytes()==body, 'Immutable owned receipt mismatch: '+str(p)
 else:p.write_bytes(body)
 return fp(p)
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==C
assert not subprocess.check_output(['git','diff','--name-only']).strip()
claim=read(R/'claim.json');PL=read(R/'proved-local.json');M=read(R/'whole-math-review.json')
assert fp(R/'whole-math-review.json')['raw_sha256']=='7e669c59a1ebe9a4f8ab48a47463b3ca6674afe7bbd823b770fc3c17835dd276'
assert M['status']=='passed-scoped'
assert claim['declarations']==PL['lean_declarations']==PL['publication_declarations']
state=adv.current_advances();item=state[claim['advance_id']]
assert item['state']=='PROVED_LOCAL' and item['owner_id']!=V
assert [k for k,v in state.items() if v['state']=='STABILIZING']==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
paths=set();stable=[]
for x in M['frozen_inputs']:
 stable.append(verify(x));verify(x,x['reviewer_snapshot']);paths.update([x['path'],x['reviewer_snapshot']])
for x in M['reachable_source_inputs']+M['pinned_API_inputs']+M['primary_raw_inputs']:
 verify(x);paths.add(x['path'])
assert len(stable)==14
gate_results=read(R/'reviewer.exact.gate-results.json');assert len(gate_results)==5
for g in gate_results:assert g['exit_code']==0;verify(g)
focused=Path(gate_results[0]['path']).read_text(encoding='utf-8')
assert 'Build completed successfully (3731 jobs)' in focused
axioms=[]
for name,body in re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]",focused):
 ax=[x.strip() for x in body.split(',')];assert set(ax)=={'propext','Classical.choice','Quot.sound'}
 axioms.append(dict(declaration=name,axioms=ax))
assert len(axioms)==16
for g,marker in zip(gate_results[1:],['Publication PASS: 189','253 audits, 8 repair','252 registered cells','affected declarations=72; changed cells=68']):
 assert marker in Path(g['path']).read_text(encoding='utf-8')
fake=[]
for x in M['reachable_source_inputs']:
 for n,line in enumerate(astis.strip_lean_comments_and_strings(Path(x['path']).read_text(encoding='utf-8')).splitlines(),1):
  if astis.FORBIDDEN_REGEX.search(line):fake.append(dict(path=x['path'],line=n,text=line))
assert not fake and len(M['reachable_source_inputs'])==34
fake_receipt=emit('reviewer.exact.fake-closure.json',dict(checked_commit=C,status='passed',files=34,hits=fake,scope='Actual recursive canonical ASTIS/Test import closure of both production and all three Tests; canonical stripped scanner',standard_axioms=axioms))
pub.check_advance(claim['declarations'],reviewed=True);data=pub.inputs()
decoder_results=[read(D/f'result{i}.json') for i in range(2)]
decoder_packets=[read(D/f'packet{i}.json') for i in range(2)]
envelope=dict(reviewed_input_packets=decoder_packets,observed_input_artifacts=decoder_results[0]['observed_input_artifacts'],reviewed_outputs=[{k:v for k,v in d.items() if k!='decoder_run_sha256'} for d in decoder_results])
decoder_run=pub.digest(envelope)
assert decoder_run=='6d35f593139f5e411a0e2b196c0410e390877e2e73c610d4f96b9cbb2d87b563'
assert read(D/'lease.json')['status']=='CLOSED'
source=[];union={};administrative=[]
for i,target in enumerate(claim['declarations']):
 rv=read(R/f'source.{i}.review.json');packet=read(R/f'source.{i}.reviewer-packet.json')
 assert rv['review_run_sha256']==pub.digest({k:v for k,v in rv.items() if k!='review_run_sha256'})
 assert packet['packet_sha256']==pub.digest({k:v for k,v in packet.items() if k!='packet_sha256'})
 assert rv['reviewer_packet_sha256']==packet['packet_sha256']
 assert rv['verdict']=='equivalent-after-elaboration' and not rv['blocking'] and not rv['deltas'] and not rv['repairs'] and rv['source_excess_count']==0
 assert rv['independent_from_formalizer'] and rv['independent_from_decoder'] and rv['reviewer'] not in [rv['formalizer'],rv['decoder'],V]
 assert rv['exposure_attestation']['current_primary_before_packet'] and not rv['exposure_attestation']['current_math_verdict_read']
 item,binding=next((item,b) for item in pub.load() for b in item['bindings'] if b['declaration']==target)
 audit=data['audits'][binding['audit_id']];ctx=pub.review_context(item,binding,data)
 assert audit['state']=='accepted' and audit['source_review']['state']=='accepted'
 assert pub.binding_digest(item,binding,data)==audit['publication_binding_sha256']==packet['publication_binding_sha256']==rv['publication_binding_sha256']
 assert ctx==audit['publication_context']==packet['candidate_publication_context']==rv['review_context']
 assert audit['source_review']['review_run_sha256']==rv['review_run_sha256'] and audit['source_review']['reviewer_packet_sha256']==packet['packet_sha256']
 assert audit['source_review']['run_artifact']==str(R/f'source.{i}.review.json').replace('\\','/')
 assert rv['whole_module_reviewed'];module=fp(packet['lean']['file'])
 assert module['raw_sha256']==rv['whole_module_raw_sha256'] and module['lf_sha256']==rv['whole_module_lf_sha256']==rv['whole_module_file_sha256']==ctx['file']
 assert rv['whole_module_private_helpers_reviewed']==[[],['actual_gradient_bounds','parameterized_damped_point','actual_quadratic_minimum']][i]
 assert sha(packet['source']['original_text'].encode())==packet['source']['text_sha256']==rv['source_statement_sha256']
 assert sha(packet['lean']['statement'].encode())==packet['lean']['statement_sha256']==rv['lean_statement_sha256']
 rr=audit['reconstruction'];d=decoder_results[i]
 assert not d['source_text_visible'] and not d['blocking'] and not d['ambiguities'] and d['independent_from_formalizer']
 assert d['decoder_run_sha256']==rr['decoder_run_sha256']==rv['decoder_run_sha256']==decoder_run
 assert d['packet_sha256']==rr['decoder_packet_sha256']==packet['blind_reconstruction']['decoder_packet_sha256']==rv['decoder_packet_sha256']
 assert sha(d['reconstructed_theorem_text'].encode())==d['reconstructed_text_sha256']==rr['text_sha256']==rv['reconstructed_text_sha256']
 assert d['reconstructed_theorem_text']==rr['text']==packet['blind_reconstruction']['text']
 assert d['lean_statement_sha256']==packet['lean']['statement_sha256']
 assert rr['input_artifacts']==['lean-statement','approved-definition-context'] and rr['observed_input_artifacts']==d['observed_input_artifacts']
 assert len(rv['semantic_slots'])==7
 dp=fp(D/f'packet{i}.json');obs=d['observed_input_artifacts'][i]
 assert dp['raw_sha256']==obs['sha256_raw'] and dp['bytes']==obs['byte_length']
 assert decoder_packets[i]==read(R/f'anonymous.{i}.decoder.json')
 assert decoder_packets[i]['packet_sha256']==pub.digest({k:v for k,v in decoder_packets[i].items() if k!='packet_sha256'})
 audit_path=Path('research-wiki/semantic-roundtrip/audits')/(audit['id']+'.json')
 before=read(R/f'source-admission-before.{i}.raw.snapshot.audit.json');current=read(audit_path)
 changes=diff(before,current)
 assert all(x['path'] in ['/state','/verdict','/deltas','/semantic_slots'] or x['path'].startswith('/source_review/') for x in changes)
 administrative.append(dict(path=audit_path.as_posix(),before=fp(R/f'source-admission-before.{i}.raw.snapshot.audit.json'),current=fp(audit_path),classification='accepted-source administrative only; context/binding/source/Lean/decoder immutable',changes=changes))
 # Draft-to-blind reconstruction also preserves the whole publication contract.
 draft=read(R/f'decoder-binding-before.{i}.raw.snapshot.audit.json')
 delta=diff(draft,before)
 assert all(x['path']=='/state' or x['path']=='/reconstruction' or x['path'].startswith('/reconstruction/') for x in delta)
 administrative.append(dict(path=audit_path.as_posix(),phase='draft-to-blind',before=fp(R/f'decoder-binding-before.{i}.raw.snapshot.audit.json'),current=fp(R/f'source-admission-before.{i}.raw.snapshot.audit.json'),changes=delta))
 for x in rv['input_artifacts']:
  verify(x,x['immutable_snapshot_path'])
  union[x['path']]=x
 source.append(dict(declaration=target,audit_id=audit['id'],review=fp(R/f'source.{i}.review.json'),review_run_sha256=rv['review_run_sha256'],reviewer_packet=fp(R/f'source.{i}.reviewer-packet.json'),packet_sha256=packet['packet_sha256'],publication_binding_sha256=rv['publication_binding_sha256'],review_context_sha256=pub.digest(ctx),whole_module=module,private_helpers=rv['whole_module_private_helpers_reviewed'],source_reviewer=rv['reviewer'],decoder_actor=d['decoder'],decoder_result=fp(D/f'result{i}.json'),decoder_run_sha256=decoder_run,semantic_slots=7,verdict=rv['verdict'],source_excess=0))
assert len(union)==46
source_drift=[]
for path,x in union.items():
 current=fp(path)
 if current['raw_sha256']==x['raw_sha256']:verify(x)
 else:
  delta=diff(read(x['immutable_snapshot_path']),read(path))
  if '/audits/' in path:
   assert all(d['path'] in ['/state','/verdict','/deltas','/semantic_slots'] or d['path'].startswith('/source_review/') for d in delta)
  else:
   assert 'frontier-cells/' in path
   assert {d['path'] for d in delta}=={'/status','/evidence/execution_boundary','/evidence/proof_review'}
  source_drift.append(dict(path=path,frozen=x,current=current,changes=delta))
assert len(source_drift)==4
for i,cid in enumerate(claim['cells']):
 path=f'research-wiki/frontier-cells/{cid}.json';old=read(R/f'{cid}.before-proved-local.raw.snapshot.json');new=read(path)
 changes=diff(old,new);assert {d['path'] for d in changes}=={'/status','/evidence/execution_boundary','/evidence/proof_review'}
 assert new['status']=='proved_locally'
 snapshot=R/f'reviewer.exact.cell{i}.before-verification.raw.snapshot.json';assert not snapshot.exists();snapshot.write_bytes(Path(path).read_bytes())
 administrative.append(dict(path=path,before=fp(R/f'{cid}.before-proved-local.raw.snapshot.json'),current=fp(path),changes=changes,classification='PROVED_LOCAL admin evidence only, original mathematical contract immutable'))
lease=read(R/'source.review.lease.json');assert lease['write_lease']=='CLOSED' and not lease['compiler_started'] and lease['production_shared_metadata_writes'] is False
assert lease['lease_run_sha256']==pub.digest({k:v for k,v in lease.items() if k!='lease_run_sha256'})
paths.update(union);paths.update(claim['lean_files']+claim['test_files'])
for root in [R,D]:
 paths.update(p.as_posix() for p in root.rglob('*') if p.is_file())
tracked=set(subprocess.check_output(['git','ls-files','-z']).decode().split('\0'));check_paths=sorted(paths&tracked)
proc=subprocess.Popen(['git','cat-file','--batch'],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
git_checks=[]
for path in check_paths:
 proc.stdin.write(f'{C}:{path}\n'.encode());proc.stdin.flush();header=proc.stdout.readline().decode().split()
 assert header[1]=='blob',path
 blob=proc.stdout.read(int(header[2]));assert proc.stdout.read(1)==b'\n';current=Path(path).read_bytes()
 raw_required=path.startswith('runs/')
 assert (blob==current if raw_required else blob.replace(b'\r\n',b'\n')==current.replace(b'\r\n',b'\n')),path
 git_checks.append(dict(path=path,git_blob_sha256=sha(blob),raw_exact_required=raw_required,raw_match=blob==current,lf_match=sha(blob.replace(b'\r\n',b'\n'))==sha(current.replace(b'\r\n',b'\n'))))
proc.stdin.close();assert proc.wait()==0
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==C
assert not subprocess.check_output(['git','diff','--name-only']).strip()
admin_receipt=emit('reviewer.exact.admission-reconciliation.json',dict(status='passed-scoped',checked_commit=C,math14allunchanged=True,source_input_union=46,current_admin_drifts=source_drift,lifecycle=administrative,Git=dict(files=len(git_checks),raw_artifacts=sum(x['raw_exact_required'] for x in git_checks),checks=git_checks),no_mathematical_or_statement_change=True))
source_receipt=emit('reviewer.exact.source-binding.json',dict(status='passed-scoped',checked_commit=C,source_reviews=source,source_union=list(union.values()),source_drifts=source_drift,decoder_joint_envelope_hash=decoder_run,reviewed_publication_targets=claim['declarations'],check_advance_reviewed_true='passed',source_actor_exposure_disclosed=True))
receipt=dict(schema_version=1,advance_id=claim['advance_id'],verifier_id=V,reviewer_role='independent_verifier',verification_status='passed-scoped',status='passed-scoped',verified_commit=C,checked_commit=C,owner_is_not_verifier=True,lean_declarations=claim['declarations'],publication_declarations=claim['declarations'],gate=dict(focused=gate_results[0],metadata=gate_results[1:],publication_base='origin/main',base_commit=subprocess.check_output(['git','rev-parse','origin/main'],text=True).strip(),root_aggregate='Not run/current packet29 aggregate pending; do not reuse packet28 aggregate as a current gate'),whole_math_review_reused=fp(R/'whole-math-review.json'),whole_math_scope=M['whole_body_review'],math14frozen=stable,parent_checks_28_reused=M['unchanged_parent_checks'],source_audit=source_receipt,source_reviews=source,fake_closure_scan=fake_receipt,standard_axioms=axioms,conceptual_mirror_audit=PL['conceptual_mirror_audit'],Git_evidence=dict(receipt=admin_receipt,files=len(git_checks),raw_artifacts=sum(x['raw_exact_required'] for x in git_checks)),truth_boundary=PL['truth_boundary'],remaining_boundary=['Sharp dimensionfree coefficient eta*norm(u)^2/2 for (4.3), bias, FIRST W2/LSI/T2/fullLemma4.2, posterior jointkernel, higher smoothing/Picard/Wp/warmness/initialization/main/querywork/composition remain open.','Exact independent source+mathematical verification completed here; serialized shared imports/root Tests/current repository aggregate/ProofSeal/site/graphs/Exposition/postmerge purification/renderedQA/ownheadremoteCI and merge remain pending.','This is necessary domain membership for same actual Gaussian-gradient-output kernel and its own Bochner center; no posterior reinterpretation or mean=smoothedgradient certificate.'],ProofSeal=dict(focused='accepted-scoped exact two declarations',repository='pending serialized aggregate/integration; no full-paper badge'),sole_stabilization_owner_preserved=True,prior_full_range_versions_preserved=claim['prior_versions'],authorized_mutations='Only own exact receipts, one advance VERIFIED transition, and two claimed cell independent status/evidence; no production/shared/audit changes',leases=dict(compiler='CLOSED; fresh focused terminal exit0; previous exact-byte direct+stress evidence reused',write='CLOSED after independent transition/cell evidence',sessions='CLOSED'),created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
result=emit('verified.json',receipt)
print(json.dumps(dict(status='passed-scoped',verified=result,checked_commit=C,Git_files=len(git_checks),source_union=len(union),source_admin_drifts=len(source_drift),fake_files=34,axioms=len(axioms),transition='not yet appended')))
