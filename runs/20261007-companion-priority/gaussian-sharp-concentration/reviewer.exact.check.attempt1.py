from pathlib import Path
import json, hashlib, subprocess, re, sys, datetime
sys.path.insert(0, 'tools')
import astis, astis_publication as pub, astis_advance as adv
R=Path('runs/20261007-companion-priority/gaussian-sharp-concentration')
D=Path('runs/20261007-companion-priority/anonymous-decoder-30')
C='2f4e0ba92d7233f07e93822897d2d275da46799e'
V='picard_commit_verifier_20261005'
def sha(b): return hashlib.sha256(b).hexdigest()
def read(p): return json.loads(Path(p).read_bytes())
def fp(p):
 b=Path(p).read_bytes(); return dict(path=str(p).replace('\\','/'),raw_sha256=sha(b),lf_sha256=sha(b.replace(b'\r\n',b'\n')),bytes=len(b))
def verify(x,p=None):
 y=fp(p or x['path'])
 for k in ('raw_sha256','lf_sha256','bytes'):
  if k in x: assert x[k]==y[k],(y['path'],k,x[k],y[k])
 return y
def diff(a,b,p=''):
 if isinstance(a,dict) and isinstance(b,dict):
  return sum([diff(a.get(k),b.get(k),p+'/'+k) for k in sorted(set(a)|set(b))],[])
 return [] if a==b else [dict(path=p,before=a,after=b)]
def emit(n,d):
 p=R/n; body=(json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode()
 if p.exists(): assert p.read_bytes()==body, str(p)
 else: p.write_bytes(body)
 return fp(p)
def admin_changes(delta):
 return all(x['path'] in ['/state','/verdict','/deltas','/semantic_slots'] or x['path'].startswith('/source_review/') for x in delta)
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==C
assert not subprocess.check_output(['git','diff','--name-only']).strip()
claim=read(R/'claim.json'); plan=read(R/'publication-plan.json'); PL=read(R/'proved-local.json')
assert plan['mathematical_declarations']==claim['declarations']==PL['lean_declarations']==PL['publication_declarations']
assert plan['active_cells']==PL['active_cells']
targets=plan['mathematical_declarations']; all_targets=targets+plan['metadata_only_revalidated_declarations']
states=adv.current_advances(); sa=states[claim['advance_id']]
assert sa['state']=='PROVED_LOCAL' and sa['owner_id']!=V
assert [k for k,v in states.items() if v['state']=='STABILIZING']==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
paths=set(); admin=[]; mathematical=[]
M=read(R/'whole-math-review.json'); MF=read(R/'math-freeze.json'); RF=read(R/'math-freeze.exposition-repaired.json')
assert M['status']=='pass-scoped-whole-mathematical-proof' and not M['blockers']
assert fp(R/'math-freeze.json')['raw_sha256']==M['math_freeze_raw_sha256']
assert fp(R/'reviewer.math.run.json')['raw_sha256']==M['run_raw_sha256']
verify(RF['original_math_freeze']); verify(RF['original_independent_whole_math']);verify(RF['repair']);verify(RF['focused_compile'])
assert RF['mathematical_statement_or_proof_changed'] is False
for i,x in enumerate(M['frozen_files']):
 snapshot=R/f'reviewer.math.frozen.{i}.lean'; verify(x,snapshot)
 current=fp(x['path']); old=snapshot.read_text(encoding='utf8'); new=Path(x['path']).read_text(encoding='utf8')
 if current['raw_sha256']!=x['raw_sha256']:
  assert i==1
  assert re.sub(r'/\-!.*?\-/', '',old,count=1,flags=re.S)==re.sub(r'/\-!.*?\-/', '',new,count=1,flags=re.S)
  assert astis.strip_lean_comments_and_strings(old)==astis.strip_lean_comments_and_strings(new)
 mathematical.append(dict(frozen=x,current=current,snapshot=fp(snapshot),comment_only_delta=(current['raw_sha256']!=x['raw_sha256']),noncomment_math_identical=True))
 paths.update([x['path'],snapshot.as_posix()])
for x in RF['inputs']: verify(x);paths.add(x['path'])
assert len(M['frozen_files'])==5 and len(M['new_private_inventory']['names'])==50
for x in M['compilation']['commands']: verify(x,x['log']);assert x['exit_code']==0;paths.add(x['log'])
assert all(x['status']=='pass' for x in M['seven_mathematical_slots']) and len(M['seven_mathematical_slots'])==7
assert M['binder_and_definition_check']['excess_public_binders']==[]
dep=read(R/'reviewer.math.dependencies.json'); sup=read(R/'reviewer.math.dependencies.supplement.json')
dependencies=[]
for x in dep['files']+sup:
 verify(x); verify(x,x['snapshot']);paths.add(x['snapshot']); dependencies.append(fp(x['path']))
assert subprocess.check_output(['git','-C','.lake/packages/mathlib','rev-parse','HEAD'],text=True).strip()==dep['mathlib_commit']=='db584cd6d46c92f209a44c0f1c829460d327499d'
assert Path('lean-toolchain').read_text().strip()=='leanprover/lean4:v4.33.0'
paths.update(['lean-toolchain','lake-manifest.json'])
overlay=read(R/'source.repair.overlay-review.json'); proposal=read(R/'exposition-repair.proposal.json')
assert overlay['verdict']=='accepted-scoped-exposition-provenance-only' and not overlay['blocking']
assert overlay['review_run_sha256']==pub.digest({k:v for k,v in overlay.items() if k!='review_run_sha256'})
assert overlay['R1']['only_module_header_comment_changed'] and overlay['R1']['all_imports_and_noncomment_raw_bytes_identical']
assert proposal['mathematical_signatures_or_proofs_changed'] is False
for x in proposal['before']: verify(x,x['snapshot']); paths.add(x['snapshot'])
for x in proposal['after']: verify(x); paths.add(x['path'])
seals=read(R/'preproof/statement-seals.accepted.json')
for i,s in enumerate(seals['signatures']):
 text=Path(claim['lean_files'][i]).read_text(encoding='utf8')
 assert s['signature_text'] in text and sha(s['signature_text'].encode())==s['signature_lf_sha256']
 assert s['full_declaration']==targets[i]
sr=read(R/'preproof/reviewer.statement-review.json');top=read(R/'preproof/reviewer.source-topology-review.json')
assert sr['verdict']=='accepted-statement-only' and top['verdict']=='accepted-scoped'
assert sr['independent_from_graph_author'] and top['independent_from_graph_author']
assert fp(top['graph_path'])['raw_sha256']==top['graph_raw_sha256']
paths.add(top['graph_path'])
gates=read(R/'reviewer.exact.gates.json'); assert gates['commit']==C and len(gates['results'])==5
for g in gates['results']: assert g['returncode']==0;g['fingerprint']=fp(g['log'])
focused=Path(gates['results'][0]['log']).read_text(encoding='utf8')
assert 'Build completed successfully (3747 jobs)' in focused
axioms=[]
for n,b in re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]",focused):
 a=[x.strip() for x in b.split(',')];assert set(a)=={'propext','Classical.choice','Quot.sound'};axioms.append(dict(declaration=n,axioms=a))
assert len(axioms)==20, len(axioms)
assert 'Publication PASS: 190' in Path(gates['results'][1]['log']).read_text()
assert '256 audits, 8 repair' in Path(gates['results'][2]['log']).read_text()
assert '253 registered cells' in Path(gates['results'][3]['log']).read_text()
assert 'affected declarations=73; changed cells=69' in Path(gates['results'][4]['log']).read_text()
# Reconstruct actual canonical ASTIS/Test import closure independently of prior scans.
pending=claim['lean_files']+claim['test_files']; closure=set()
while pending:
 p=pending.pop()
 if p in closure: continue
 closure.add(p);text=Path(p).read_text(encoding='utf8')
 for mod in re.findall(r'^import\s+([\w.]+)',text,re.M):
  q=mod.replace('.','/')+'.lean'
  if (q.startswith('AutoSamplingTheory/') or q.startswith('Tests/')) and Path(q).exists():pending.append(q)
hits=[]
for p in sorted(closure):
 for n,line in enumerate(astis.strip_lean_comments_and_strings(Path(p).read_text(encoding='utf8')).splitlines(),1):
  if astis.FORBIDDEN_REGEX.search(line):hits.append(dict(path=p,line=n,text=line))
assert not hits
fake=emit('reviewer.exact.fake-closure.json',dict(checked_commit=C,status='passed',method='Independent recursive canonical production/Test import closure; astis stripped-source FORBIDDEN_REGEX',files=len(closure),inputs=[fp(p) for p in sorted(closure)],hits=hits,standard_axioms=axioms))
paths.update(closure)
pub.check_advance(all_targets,reviewed=True);data=pub.inputs();source=[];union={};drifts=[]
decs=[read(D/f'result{i}.json') for i in range(2)];dp=[read(D/f'packet{i}.json') for i in range(2)];dl=read(D/'lease.json')
assert dl['status']=='CLOSED' and dl['source_text_visible'] is False and dl['compiler_started'] is False
for i,dec in enumerate(decs):
 assert not dec['source_text_visible'] and not dec['blocking'] and not dec['ambiguities']
 assert dec['decoder_run_sha256']==dl['decoder_run_sha256']
 assert dec['packet_sha256']==pub.digest({k:v for k,v in dp[i].items() if k!='packet_sha256'})
 assert dp[i]==read(R/f'anonymous.{i}.decoder.json')
 verify(dec['observed_input_artifacts'][0],D/f'packet{i}.json')
 assert fp(D/f'result{i}.json')['raw_sha256']==dl['output_receipts'][i]['raw_sha256']
 assert sha(dec['reconstructed_theorem_text'].encode())==dec['reconstructed_text_sha256']
for i,target in enumerate(all_targets):
 rv=read(R/f'source.repaired.{i}.review.json'); packet=read(R/f'source.repaired.{i}.reviewer-packet.json')
 assert rv['review_run_sha256']==pub.digest({k:v for k,v in rv.items() if k!='review_run_sha256'})
 assert packet['packet_sha256']==pub.digest({k:v for k,v in packet.items() if k!='packet_sha256'})
 assert rv['reviewer_packet_sha256']==packet['packet_sha256']
 assert rv['verdict']=='equivalent-after-elaboration' and not rv['blocking'] and not rv['deltas'] and not rv['repairs'] and not rv['EXCESS']
 assert rv['independent_from_formalizer'] and rv['independent_from_decoder'] and rv['reviewer'] not in [sa['owner_id'],rv['decoder'],V]
 item,b=next((it,b) for it in pub.load() for b in it['bindings'] if b['declaration']==target)
 audit=data['audits'][b['audit_id']];ctx=pub.review_context(item,b,data)
 assert audit['state']==audit['source_review']['state']=='accepted'
 assert pub.binding_digest(item,b,data)==audit['publication_binding_sha256']==rv['publication_binding_sha256']==packet['publication_binding_sha256']
 assert ctx==audit['publication_context']==packet['candidate_publication_context']==rv['review_context']
 assert audit['source_review']['review_run_sha256']==rv['review_run_sha256']
 assert audit['source_review']['reviewer_packet_sha256']==packet['packet_sha256']
 assert audit['source_review']['run_artifact']==str(R/f'source.repaired.{i}.review.json').replace('\\','/')
 module=fp(packet['lean']['file'])
 assert module['raw_sha256']==rv['whole_module_raw_sha256']
 assert module['lf_sha256']==rv['whole_module_lf_sha256']==rv['whole_module_file_sha256']==ctx['file']
 assert sha(packet['lean']['statement'].encode())==rv['lean_statement_sha256']==packet['lean']['statement_sha256']
 assert sha(packet['source']['original_text'].encode())==rv['source_text_sha256']==packet['source']['text_sha256']
 rec=audit['reconstruction']
 assert rec['text']==packet['blind_reconstruction']['text'] and rec['text_sha256']==rv['reconstructed_text_sha256']==sha(rec['text'].encode())
 assert rec['decoder_run_sha256']==rv['decoder_run_sha256'] and rec['decoder_packet_sha256']==rv['decoder_packet_sha256']
 assert rec['input_artifacts']==['lean-statement','approved-definition-context']
 if i<2:
  assert rec['text']==decs[i]['reconstructed_theorem_text'] and rec['decoder_run_sha256']==decs[i]['decoder_run_sha256']
  assert rec['observed_input_artifacts']==decs[i]['observed_input_artifacts']
 else:
  old=read('runs/20261007-companion-priority/anonymous-decoder-29/result0.json')
  assert rec['text']==old['reconstructed_theorem_text'] and rec['decoder_run_sha256']==old['decoder_run_sha256']
 assert len(rv['semantic_slots'])==7
 for x in rv['review_evidence'].values():
  if isinstance(x,dict) and 'path' in x and 'raw_sha256' in x:verify(x);paths.add(x['path'])
 snapshots={x['input']:x for x in rv['immutable_input_snapshots']}
 for x in rv['input_artifacts']:
  if x['path'] in snapshots:
   ss=snapshots[x['path']];verify(x,ss['snapshot']);paths.add(ss['snapshot'])
  else:verify(x)
  if x['path'] in union:assert union[x['path']]['raw_sha256']==x['raw_sha256']
  union[x['path']]=dict(x,snapshot=snapshots.get(x['path'],{}).get('snapshot'))
 ap=Path('research-wiki/semantic-roundtrip/audits')/(audit['id']+'.json')
 before=R/f'source-admission-before.{i}.raw.snapshot.audit.json';delta=diff(read(before),read(ap));assert admin_changes(delta)
 admin.append(dict(path=ap.as_posix(),before=fp(before),current=fp(ap),changes=delta,classification='Source accepted administration only; binding/current context unchanged'))
 source.append(dict(declaration=target,mathematical_credit=(i<2),audit_id=audit['id'],review=fp(R/f'source.repaired.{i}.review.json'),packet=fp(R/f'source.repaired.{i}.reviewer-packet.json'),review_run_sha256=rv['review_run_sha256'],packet_sha256=packet['packet_sha256'],publication_binding_sha256=rv['publication_binding_sha256'],review_context_sha256=pub.digest(ctx),whole_module=module,semantic_slots=7,source_reviewer=rv['reviewer'],decoder=rv['decoder'],decoder_run_sha256=rv['decoder_run_sha256'],verdict=rv['verdict'],exposure=rv['review_evidence']['exposure']))
for p,x in union.items():
 paths.add(p)
 if fp(p)['raw_sha256']==x['raw_sha256']:verify(x);continue
 assert x['snapshot'],p
 delta=diff(read(x['snapshot']),read(p))
 if '/audits/' in p:assert admin_changes(delta)
 else:
  assert '/frontier-cells/' in p,p
  assert all(z['path']=='/status' or z['path'].startswith('/evidence/') or z['path'].startswith('/reuse_plan/') or z['path'].startswith('/learning_contract/reader_backpressure/') for z in delta),(p,[z['path'] for z in delta])
 drifts.append(dict(path=p,frozen=x,current=fp(p),changes=delta))
for i,cid in enumerate(plan['active_cells']):
 p=Path('research-wiki/frontier-cells')/(cid+'.json');old=R/f'{cid}.before-proved-local.raw.snapshot.json'
 delta=diff(read(old),read(p));assert all(z['path']=='/status' or z['path'].startswith('/evidence/') for z in delta)
 assert read(p)['status']=='proved_locally'
 admin.append(dict(path=p.as_posix(),before=fp(old),current=fp(p),changes=delta,classification='PROVED_LOCAL only'))
 snap=R/f'reviewer.exact.cell{i}.before-verification.raw.snapshot.json'
 if not snap.exists():snap.write_bytes(p.read_bytes())
 else:assert snap.read_bytes()==p.read_bytes()
mirror=read(R/'conceptual-mirror.gaussian-symmetry.repaired.review.json')
assert mirror['verdict']=='validated-conceptual-mirror' and mirror['independent_of_creator'] and mirror['formal_credit'] is False and mirror['solid_lean_dependency_edge'] is False
assert PL['conceptual_mirror_audit']['discovery_ids']==[mirror['discovery_id']]
# All raw committed snapshots, source/decoder receipts and prior blocked evidence remain exact Git objects.
for root in [R,D]: paths.update(p.as_posix() for p in root.rglob('*') if p.is_file())
tracked=set(subprocess.check_output(['git','ls-files','-z']).decode().split('\0'));check_paths=sorted(paths&tracked)
proc=subprocess.Popen(['git','cat-file','--batch'],stdin=subprocess.PIPE,stdout=subprocess.PIPE);gitchecks=[]
for p in check_paths:
 proc.stdin.write(f'{C}:{p}\n'.encode());proc.stdin.flush();h=proc.stdout.readline().decode().split();assert h[1]=='blob',p
 blob=proc.stdout.read(int(h[2]));assert proc.stdout.read(1)==b'\n';cur=Path(p).read_bytes();raw=p.startswith('runs/')
 assert blob==cur if raw else blob.replace(b'\r\n',b'\n')==cur.replace(b'\r\n',b'\n'),p
 gitchecks.append(dict(path=p,git_blob_sha256=sha(blob),raw_exact_required=raw,raw_match=blob==cur,lf_match=sha(blob.replace(b'\r\n',b'\n'))==sha(cur.replace(b'\r\n',b'\n'))))
proc.stdin.close();assert proc.wait()==0
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==C
assert not subprocess.check_output(['git','diff','--name-only']).strip()
reconciliation=emit('reviewer.exact.admission-reconciliation.json',dict(status='passed-scoped',checked_commit=C,full_math_five_files=mathematical,pinned_API_dependencies=dependencies,exposition_overlay=fp(R/'source.repair.overlay-review.json'),original_freeze=fp(R/'math-freeze.json'),repaired_freeze=fp(R/'math-freeze.exposition-repaired.json'),active_cells=plan['active_cells'],historic_claim_cells_preserved=claim['cells'],publication_routing=fp(R/'publication-routing-reconciliation.json'),current_source_admin_drift=drifts,lifecycle=admin,Git=dict(files=len(gitchecks),raw_artifacts=sum(x['raw_exact_required'] for x in gitchecks),checks=gitchecks),no_statement_or_proof_change_after_math_review=True))
binding=emit('reviewer.exact.source-binding.json',dict(status='passed-scoped',checked_commit=C,reviewed_publication_targets=all_targets,source_reviews=source,source_union=len(union),source_inputs=list(union.values()),source_administrative_drifts=drifts,current_reviewed_true_admission='passed',decoder30_lease=fp(D/'lease.json'),decoder_run_attestation='Canonical run ID matched both immutable decoder results, lease and current audit/source bindings; preserved raw result digests independently checked.',independent_source_overlay=fp(R/'source.repair.overlay-review.json')))
receipt=dict(schema_version=1,advance_id=claim['advance_id'],verifier_id=V,reviewer_role='independent_verifier',verification_status='passed-scoped',status='passed-scoped',verified_commit=C,checked_commit=C,owner_is_not_verifier=True,lean_declarations=targets,publication_declarations=targets,metadata_only_revalidation=all_targets[2:],active_cells=plan['active_cells'],gate=dict(focused=gates['results'][0],metadata=gates['results'][1:],publication_base='origin/main',base_commit=subprocess.check_output(['git','rev-parse','origin/main'],text=True).strip(),repository_aggregate='Pending root serialized packet30 shared integration; packet29 aggregate is not reused as current packet30 gate'),whole_math_review_reused=fp(R/'whole-math-review.json'),whole_math_review_scope='Complete 930-line generic/50 new private providers, same actual proximal oracle/3 retained private producers, three genuine Tests and seven proof slots independently reviewed by gaussian_domain_preproof_reviewer_29; exact five reviewed files preserved except independently reconciled header-only comment.',math_freeze=fp(R/'math-freeze.json'),repaired_freeze=fp(R/'math-freeze.exposition-repaired.json'),source_audit=binding,source_reviews=source,fake_closure_scan=fake,standard_axioms=axioms,conceptual_mirror_audit=PL['conceptual_mirror_audit'],conceptual_mirror_review=fp(R/'conceptual-mirror.gaussian-symmetry.repaired.review.json'),Git_evidence=dict(receipt=reconciliation,files=len(gitchecks),raw_artifacts=sum(x['raw_exact_required'] for x in gitchecks)),truth_boundary=claim['truth_boundary'],remaining_boundary=['Exact source-scoped (4.3) sharp centered Gaussian-gradient-output bound with its own actual Bochner mean; all positive eta, signed t, zero dimension/direction and nonsmooth scalar Lipschitz cases. Retained (4.4)-(4.5) exact proximal/input/noise semantics and moments/domains.','No own mean=smoothed-gradient/bias (4.2), first W2 in (4.6)/LSI/T2/full Lemma4.2, RGO/HMC reinterpretation, higher smoothing/Picard/Wp/proxy-warmness/initialization, PBPS obligations, main results/work/composition. TV cannot transfer unbounded expected work.','Independent mathematical/blind/source/exact focused verification completed here. Current repository aggregate/ProofSeal/shared imports/Registry/site/graphs/purification/Exposition/rendered QA/current-head remote CI/merge remain separate pending stabilization.'],ProofSeal=dict(focused='accepted-scoped exact two mathematical declarations',repository='pending serialized current-packet aggregate and repository admission',statement_seals=fp(R/'preproof/statement-seals.accepted.json'),source_coverage=fp(R/'preproof/reviewer.source-topology-review.json'),no_full_source_or_paper_completion=True),sole_stabilization_owner_preserved=True,authorized_mutations='Own exact evidence plus independent VERIFIED for one advance and only two current active cells; no mathematical/source/audit/shared edits',compiler_lease='CLOSED',write_lease='Closes after independent transition and cells; root waits for final closure',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
vr=emit('verified.json',receipt)
print(json.dumps(dict(status='passed-scoped',verified=vr,checked_commit=C,Git_files=len(gitchecks),source_union=len(union),source_drifts=len(drifts),fake_files=len(closure),axiom_reports=len(axioms),transition='not yet appended')))
