import verify as v
import json,re,subprocess,hashlib,gzip,pathlib,sys
R,B,O=v.R,v.B,v.O
def selfcheck(p,key):
 d=v.load(p);actual=v.logical({k:x for k,x in d.items() if k!=key});assert actual==d[key],(str(p),key);return dict(input=v.pin(p),self_field=key,recipe='SHA256 sorted compact ensure_ascii=False allow_nan=False UTF8 entire object minus named self field; no newline',logical_sha256=actual)
def allpins(obj):
 out=[]
 if isinstance(obj,dict):
  if {'path','raw_sha256','lf_sha256'}<=set(obj):out.append(obj)
  else:
   for x in obj.values():out+=allpins(x)
 elif isinstance(obj,list):
  for x in obj:out+=allpins(x)
 return out
native=[]
for p,key in [('whole-proof-review53/run.json','run_sha256'),('source.0.review.json','review_run_sha256'),('reviewer.source.run.json','run_sha256'),('reviewer.source.inventory.json','inventory_run_sha256'),('reviewer.source.lease.json','lease_run_sha256'),('source.review.lease.json','lease_run_sha256'),('anonymous-decoder/run.json','run_sha256')]:native.append(selfcheck(B/p,key))
math=v.load(B/'whole-proof-review53/run.json')
for e in math['actual_outputs']:assert v.equal(e)
assert v.load(B/'whole-proof-review53/lease.json')['status']=='CLOSED'
source=v.load(B/'source.0.review.json');sr=v.load(B/'reviewer.source.run.json');sl=v.load(B/'reviewer.source.lease.json');rootl=v.load(B/'source.review.lease.json')
assert source['status']=='ACCEPTED_SCOPED_SOURCE_FIDELITY' and source['verdict']=='equivalent-after-elaboration' and not source['blocking'] and source['deltas']==source['repairs']==source['source_excess']==[]
assert source['reviewer']=='phase_source_reviewer_20261005' and source['independent_from_formalizer'] and source['independent_from_decoder']
for d in [sr,sl,rootl]:
 for e in d.get('outputs',[]):assert v.equal(e),(e['path'],'native source output')
for e in source['additional_authorized_input_artifacts']:assert v.equal(e)
assert sl['status']==rootl['status']=='CLOSED' and all(sl[k]=='CLOSED' for k in ['read','write','Python']) and all(rootl[k]=='CLOSED' for k in ['read_lease','write_lease','Python_lease']) and not sl['compiler_started'] and not rootl['compiler_started']
decoder=v.load(B/'anonymous-decoder/run.json');result=v.load(B/'anonymous-decoder/result0.json');binding=v.load(B/'anonymous-decoder/binding-receipt.json');dl=v.load(B/'anonymous-decoder/lease.json')
for e in binding['output_artifacts']:assert v.equal(e)
assert v.equal(binding['actual_run']) and v.equal(binding['actual_closed_lease']) and v.equal(binding['opening_lease'])
assert decoder['decoder_run_sha256']==v.logical(decoder['run_binding_payload'])==result['decoder_run_sha256']
assert decoder['result_logical_sha256']==v.logical(result)
assert dl['status']=='CLOSED' and all(dl[k]=='CLOSED' for k in ['read_lease','write_lease','Python_lease']) and not dl['compiler_started']
assert isinstance(result['decoder'],str) and isinstance(result['reconstructed_theorem_text'],str) and v.sha(result['reconstructed_theorem_text'].encode())==result['reconstructed_text_sha256']
assert result['source_text_visible'] is False and decoder['exposures']['source_text_visible'] is False and decoder['exposures']['strict_source_identity_blindness'] is False and decoder['exposures']['inherited_context_source_identities_visible'] is True
packet=v.load(B/'source.0.reviewer-packet.json');assert v.logical({k:x for k,x in packet.items() if k!='packet_sha256'})==packet['packet_sha256']==source['reviewer_packet_sha256']
audit=v.load(v.AUDIT);assert audit['state']=='accepted' and audit['verdict']==source['verdict'] and audit['semantic_slots']==source['semantic_slots'] and audit['deltas']==[]
assert audit['source_review']['review_run_sha256']==source['review_run_sha256'] and audit['lean']['formalizer']!=source['reviewer']!=audit['reconstruction']['decoder']
assert audit['reconstruction']['decoder']==result['decoder'] and audit['reconstruction']['text']==result['reconstructed_theorem_text'] and audit['reconstruction']['text_sha256']==result['reconstructed_text_sha256']
assert audit['lean']['statement_sha256']==v.sha(audit['lean']['statement'].encode())==result['statement_sha256']
mapping=[]
for current,snapshot,allowed in [(v.AUDIT,'source-admission-before.0.raw.snapshot.audit.json',{'state','semantic_slots','verdict','deltas','source_review'}),(v.CELL,'source-admission-before.0.raw.snapshot.cell.json',{'status','evidence'})]:
 old=v.load(B/snapshot);new=v.load(current);changed={k for k in set(old)|set(new) if old.get(k)!=new.get(k)};assert changed==allowed
 mapping.append(dict(original_snapshot=v.pin(B/snapshot),current=v.pin(current),changed_top_fields=sorted(changed),mathematical_source_reconstruction_publication_context_and_learning_contract_unchanged=True))
seal=v.load(R/'runs/20261007-companion-priority/pbps-reflected-density-preproof53/statement-seals.accepted.json')['signatures'][0]
prod='AutoSamplingTheory/ExampleCases/ProximalBPS/LiteralReflectedMean.lean';test='Tests/ProximalBPSReflectedMeanRegularity.lean'
sourcebind=[]
for p in [prod,test]:
 blob=subprocess.check_output(['git','show',v.COMMIT+':'+p],cwd=R);cur=v.path(p).read_bytes();assert blob.replace(b'\r\n',b'\n')==cur.replace(b'\r\n',b'\n')
 snapshot=B/'whole-proof-review53'/('production.actual.raw.snapshot.lean' if p==prod else 'Tests.actual.raw.snapshot.lean');assert cur==snapshot.read_bytes()
 sourcebind.append(dict(current=v.pin(p),git_blob_raw_sha256=v.sha(blob),git_blob_lf_sha256=v.sha(blob.replace(b'\r\n',b'\n')),same_complete_math_review_raw=True,Git_LF_equal=True,LF_lines=len(cur.replace(b'\r\n',b'\n').splitlines())))
bb=v.path(prod).read_bytes();ss=bb[bb.index(b'theorem reflected_gibbs_mean_c1'):bb.index(b' := by',bb.index(b'theorem reflected_gibbs_mean_c1'))].replace(b'\r\n',b'\n');assert ss.decode()==seal['signature_text'] and len(ss)==758 and v.sha(ss)==seal['signature_lf_sha256']
owned=v.load(O/'commit-ownedpaths.json')['paths'];gitpins=[]
for p in owned:
 blob=subprocess.check_output(['git','show',v.COMMIT+':'+p],cwd=R);cur=v.path(p).read_bytes();same=blob.replace(b'\r\n',b'\n')==cur.replace(b'\r\n',b'\n');assert same,p
 gitpins.append(dict(current=v.pin(p),git_blob_raw_sha256=v.sha(blob),git_blob_lf_sha256=v.sha(blob.replace(b'\r\n',b'\n')),Git_LF_equal=same))
v.dump('git-owned-file-bindings.json',dict(commit=v.COMMIT,count=len(gitpins),bindings=gitpins))
wd=v.load(B/'whitespace-diagnosis53/diagnosis.json');gz=v.path(wd['gzip']['path']);gzbytes=gz.read_bytes();negative=gzip.decompress(gzbytes);assert v.sha(gzbytes)==wd['gzip']['raw_sha256'] and v.sha(negative)==wd['full_negative_raw_sha256'] and int.from_bytes(gzbytes[4:8],'little')==0
assert wd['full_staged_exit']==2 and wd['findings']==646 and len(wd['immutable_raw_artifacts'])==195
for e in wd['immutable_raw_artifacts']:assert v.equal(e)
actual_negative=subprocess.run(['git','-c','core.quotePath=false','diff','--check',v.PARENT,v.COMMIT],cwd=R,capture_output=True);assert actual_negative.returncode==2 and actual_negative.stdout==negative
exclusions=[e['path'] for e in wd['immutable_raw_artifacts']];args=['git','-c','core.quotePath=false','diff','--check',v.PARENT,v.COMMIT,'--','.']+[':(exclude)'+p for p in exclusions]
authored=subprocess.run(args,cwd=R,capture_output=True);(O/'authored-whitespace.log').write_bytes(authored.stdout+authored.stderr);assert authored.returncode==0
v.dump('whitespace.checks.json',dict(preserved_full_negative=v.pin(gz),lossless_negative_sha256=v.sha(negative),gzip_mtime=0,full_diff_exit=2,findings=646,exact_immutable_path_count=195,exact_exclusions=exclusions,authored_command=args,authored_exit=0,no_full_staged_PASS_claim=True))
log=v.path(O/'focused.log').read_text();ax=re.findall(r"'([^']+)' depends on axioms: \[([^\]]+)\]",log);assert len(ax)==3 and all(set(map(str.strip,a.split(',')))=={'propext','Classical.choice','Quot.sound'} for _,a in ax) and 'sorryAx' not in log and 'Build completed successfully (3895 jobs).' in log
for n in ['prod.0','prod.1','Tests.0','Tests.1']:
 st=v.load(B/(n+'.status.json'));assert v.sha(v.path(B/(n+'.log')).read_bytes())==st['log_raw_sha256'] and v.load(B/(n+'.compiler.lease.json'))['status']=='CLOSED';assert st['exit_code']==(1 if n.endswith('.0') else 0)
assert 'sorryAx' in v.path(B/'Tests.0.log').read_text() and 'sorryAx' not in v.path(B/'Tests.1.log').read_text()
v.dump('native.checks.json',dict(status='PASS',checked_commit=v.COMMIT,native_logical_checks=native,source_review_status=source['status'],source_review_verdict=source['verdict'],native_decoder_complete_run_sha256=decoder['run_sha256'],native_decoder_binding_payload_sha256=decoder['decoder_run_sha256'],native_decoder_result_logical_sha256=decoder['result_logical_sha256'],decoder_plain_string_exact_verbatim_text=True,source_text_blind=True,strict_source_identity_blind=False,inherited_source_identity_exposure_disclosed=True,reviewed_admission_mapping=mapping,production_Test_Git_and_whole_math_bindings=sourcebind,statement_LF_bytes=758,statement_LF_sha256=v.sha(ss),standard_axiom_closures=[dict(declaration=n,axioms=list(map(str.strip,a.split(',')))) for n,a in ax],all_native_source_math_decoder_leases_CLOSED=True,remaining_boundary=v.load(B/'whole-proof-review53/receipt.json')['remaining_boundary']))
print(json.dumps(dict(status='PASS',native_logical_checks=len(native),owned_Git_LF_checks=len(gitpins),source506_original_snapshots_pass=True,standard_axiom_closures=len(ax),authored_whitespace_exit=0,preserved_negative_findings=646)))
