from pathlib import Path
import json,hashlib,subprocess,re,sys,datetime
R=Path('runs/20261007-companion-priority/positive-step-proximal-rgo');C='39c19947c6267141f39bcb2b64e0def30b00164e'
sha=lambda b:hashlib.sha256(b).hexdigest()
def rec(p):
 b=Path(p).read_bytes();return {'path':str(p).replace('\\','/'),'raw_sha256':sha(b),'lf_sha256':sha(b.replace(b'\r\n',b'\n')),'bytes':len(b)}
def read(p):return json.loads(Path(p).read_text(encoding='utf8'))
def delta(a,b,p=''):
 if type(a)!=type(b):return [{'path':p,'before':a,'after':b}]
 if isinstance(a,dict):
  z=[]
  for k in sorted(set(a)|set(b)):z+=delta(a.get(k),b.get(k),p+'/'+k)
  return z
 return [] if a==b else [{'path':p,'before':a,'after':b}]
def verify_rec(x,p=None):
 y=rec(p or x['path'])
 for k in ['raw_sha256','lf_sha256','bytes']:
  if k in x:assert x[k]==y[k],(p or x['path'],k,x[k],y[k])
 return y
def emit(name,data):
 p=R/name;assert not p.exists();p.write_bytes((json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode());return rec(p)
assert subprocess.check_output(['git','rev-parse','HEAD']).decode().strip()==C
M=read(R/'whole-math-review.json');assert rec(R/'whole-math-review.json')['raw_sha256']=='4a07bfc07ceccf8dd7424c5efae68d40c56081546b5135c8a281994f40e5b74e'
sys.path.insert(0,'tools');import astis,astis_publication as pub,astis_advance as adv
data=pub.inputs();claim=read(R/'claim.json');PL=read(R/'proved-local.json');assert PL['lean_declarations']==claim['declarations']==PL['publication_declarations']
state=adv.current_advances()[claim['advance_id']];assert state['state']=='PROVED_LOCAL' and state['owner_id']!='picard_commit_verifier_20261005'
diffs=[];stable=[];paths=set()
for x in M['frozen_inputs']:
 snap=Path(x['reviewer_snapshot']);verify_rec(x,snap)
 current=rec(x['path']);paths.add(x['path']);paths.add(str(snap).replace('\\','/'))
 if current['raw_sha256']==x['raw_sha256']:
  assert current['lf_sha256']==x['lf_sha256'];stable.append(current)
 else:
  a=read(snap);b=read(x['path']);changes=delta(a,b)
  if 'frontier-cells/' in x['path']:
   allowed={'/status','/evidence/proof_review','/evidence/development_boundary','/evidence/focused_checks','/graph_contribution/visual_review'}
   assert {q['path'] for q in changes}<=allowed
   assert b['status']=='proved_locally'
  else:
   assert '/audits/' in x['path']
   allowed={'/deltas','/reconstruction','/semantic_slots','/state','/verdict'}
   assert all(q['path'] in allowed or q['path'].startswith('/source_review/') for q in changes)
   assert b['state']=='accepted'
  diffs.append({'path':x['path'],'before':x,'current':current,'changes':changes,'classification':'administrative-lifecycle-only-no-math-or-binding-change'})
assert len(stable)==31 and len(diffs)==5
for x in M['reachable_source_inputs']+M['pinned_API_and_primary_inputs']:
 verify_rec(x);paths.add(x['path'])
fake=[]
for x in M['reachable_source_inputs']:
 for n,line in enumerate(astis.strip_lean_comments_and_strings(Path(x['path']).read_text(encoding='utf8')).splitlines(),1):
  if astis.FORBIDDEN_REGEX.search(line):fake.append([x['path'],n,line])
assert not fake and len(M['reachable_source_inputs'])==32
log=rec(R/'reviewer.exact.focused.log')
lt=(R/'reviewer.exact.focused.log').read_text(encoding='utf8')
assert 'Build completed successfully (3729 jobs)' in lt
axs=re.findall(r"'([^']+)' depends on axioms: \[([^\]]+)\]",lt)
assert len(axs)==12 and all(set(z.strip() for z in s.split(','))=={'propext','Classical.choice','Quot.sound'} for _,s in axs)
gates={}
for n,marker in [('publication','Publication PASS: 188'),('semantic','251 audits, 8 repair'),('frontier','251 registered cells'),('contributor','affected declarations=71; changed cells=67')]:
 p=R/f'reviewer.exact.{n}.log';assert marker in p.read_text(encoding='utf8')
 gates[n]=dict(rec(p),status='PASS',command={'publication':'python tools/astis_publication.py check --base origin/main','semantic':'python tools/astis_semantic_roundtrip.py check','frontier':'python tools/astis_frontier_cells.py check','contributor':'python tools/astis_contributor_contract.py check --base origin/main'}[n])
alltargets=claim['declarations']+['AutoSamplingTheory.TechnicalLemmas.Measure.AffineGibbs.map_affine_gibbs']
pub.check_advance(alltargets,reviewed=True)
source=[];union={};source_drift=[]
expected=['f3feeb53365fe8cd476607505c7a5ee2370a3ad2658c8666a35d0565597c53e6','7f93689aa30e42f2a21f1b2fcf4f10bdb015b7f36c34b157f8ae84313a0129e8','0bf75fcc2f040649463ebbdb9d5874746fad11703542d21743e5fa23bb0403c7']
for i,target in enumerate(alltargets):
 rp=R/f'source.{i}.review.json';rv=read(rp);p=read(R/f'source.{i}.reviewer-packet.json')
 assert rec(rp)['raw_sha256']==expected[i]
 assert rv['review_run_sha256']==pub.digest({k:v for k,v in rv.items() if k!='review_run_sha256'})
 assert p['packet_sha256']==pub.digest({k:v for k,v in p.items() if k!='packet_sha256'})
 assert rv['reviewer_packet_sha256']==p['packet_sha256']
 assert rv['verdict']=='equivalent-after-elaboration' and not rv['blocking'] and not rv['deltas'] and not rv['repairs'] and not rv['blocking_flags']
 assert rv['independent_from_formalizer'] and rv['independent_from_decoder'] and rv['writes_closed']
 assert rv['reviewer']!='picard_commit_verifier_20261005' and rv['reviewer']!=rv['formalizer'] and rv['reviewer']!=rv['decoder']
 item,binding=next((it,b) for it in pub.load() for b in it['bindings'] if b['declaration']==target)
 audit=data['audits'][binding['audit_id']]
 ctx=pub.review_context(item,binding,data);bd=pub.binding_digest(item,binding,data)
 assert audit['state']=='accepted' and audit['source_review']['state']=='accepted'
 assert bd==audit['publication_binding_sha256']==p['publication_binding_sha256']==rv['publication_binding_sha256']
 assert ctx==audit['publication_context']==p['candidate_publication_context']==rv['review_context']
 assert pub.digest(ctx)==rv['review_context_sha256']
 assert audit['source_review']['review_run_sha256']==rv['review_run_sha256']
 assert audit['source_review']['reviewer_packet_sha256']==p['packet_sha256']
 assert audit['source_review']['run_artifact']==str(rp).replace('\\','/')
 assert rv['whole_module_reviewed'] and rv['whole_module_lines']==[252,309,54][i]
 module=rec(p['lean']['file'])
 assert module['raw_sha256']==rv['whole_module_raw_sha256']
 assert module['lf_sha256']==rv['whole_module_lf_sha256']==rv['whole_module_file_sha256']==ctx['file']
 assert rv['source_text_sha256']==p['source']['text_sha256']==sha(p['source']['original_text'].encode())
 assert rv['lean_statement_sha256']==p['lean']['statement_sha256']==sha(p['lean']['statement'].encode())
 rr=audit['reconstruction'];d=read(rr['run_artifact'])
 assert not d['source_text_visible'] and not d['blocking'] and not d['ambiguities'] and d['allwrites_closed']
 assert d['decoder_run_sha256']==rr['decoder_run_sha256']==p['blind_reconstruction']['decoder_run_sha256']==rv['decoder_run_sha256']
 assert d['packet_sha256']==rr['decoder_packet_sha256']==p['blind_reconstruction']['decoder_packet_sha256']==rv['decoder_packet_sha256']
 assert d['reconstructed_theorem_text']==rr['text']==p['blind_reconstruction']['text']
 assert sha(rr['text'].encode())==rr['text_sha256']==rv['reconstructed_text_sha256']==d['reconstructed_text_sha256']
 assert d['lean_statement_sha256']==p['lean']['statement_sha256']
 original=d['administrative_extension']['original_result_snapshot'];verify_rec(original);od=read(original['path'])
 for k in ['reconstructed_theorem_text','reconstructed_text_sha256','semantic_slots','packet_sha256','lean_statement_sha256','decoder','source_text_visible','ambiguities','blocking']:
  assert od[k]==d[k],(i,k)
 verify_rec(d['input_artifacts'][0]['immutable_raw_snapshot'])
 obs=d['input_artifacts'][0];verify_rec(obs,obs['immutable_raw_snapshot']['path'])
 canonical=read(R/f'anonymous.{i}.decoder.json')
 assert canonical['packet_sha256']==d['packet_sha256']
 assert rr['input_artifacts']==['lean-statement','approved-definition-context']
 assert rr['observed_input_artifacts']==d['input_artifacts']
 before=read(R/f'canonical-projection-before.{i}.raw.snapshot.audit.json')
 assert before['reconstruction']['input_artifacts']==rr['observed_input_artifacts']
 preserved=dict(rr);preserved.pop('observed_input_artifacts');preserved.pop('administrative_schema_projection');preserved['input_artifacts']=rr['observed_input_artifacts']
 assert preserved==before['reconstruction']
 assert (R/f'source.{i}.reviewer-packet.before-canonical-projection.raw.snapshot.json').read_bytes()==(R/f'source.{i}.reviewer-packet.json').read_bytes()
 s_before=read(R/f'source-admission-before.{i}.raw.snapshot.audit.json')
 assert s_before['reconstruction']==rr and s_before['source']==audit['source'] and s_before['lean']==audit['lean'] and s_before['publication_context']==ctx
 for e in rv['review_evidence_artifacts']:
  verify_rec(e)
 for x in rv['input_artifacts']:
  if x['path'] in union:assert union[x['path']]==x
  union[x['path']]=x
  verify_rec(x,x.get('raw_snapshot',x['path']))
 for pth in [str(rp),str(R/f'source.{i}.reviewer-packet.json'),rr['run_artifact'],original['path'],obs['immutable_raw_snapshot']['path']]:paths.add(pth.replace('\\','/'))
 source.append({'declaration':target,'audit_id':audit['id'],'review':rec(rp),'review_run_sha256':rv['review_run_sha256'],'reviewer_packet':rec(R/f'source.{i}.reviewer-packet.json'),'packet_sha256':p['packet_sha256'],'publication_binding_sha256':bd,'review_context_sha256':pub.digest(ctx),'whole_module':module,'private_declarations_reviewed':rv['private_declarations_reviewed'],'source_reviewer':rv['reviewer'],'decoder_actor':rr['decoder'],'decoder_result':rec(rr['run_artifact']),'decoder_run_sha256':rr['decoder_run_sha256'],'original_decoder_result':original,'verdict':rv['verdict'],'semantic_slot_count':len(rv['semantic_slots']),'no_new_proof_credit':i==2})
lease=read('runs/20261007-companion-priority/anonymous-decoder-28/lease.json')
assert pub.digest(lease['extension_run_records'])==lease['extension_run_sha256']
assert lease['allwrites_closed'] and not lease['source_text_visible']
for x in union.values():
 current=rec(x['path'])
 if current['raw_sha256']!=x['raw_sha256']:
  assert '/audits/' in x['path'] or '/frontier-cells/' in x['path']
  a=read(x['raw_snapshot']);b=read(x['path']);ds=delta(a,b)
  assert all(q['path'] in {'/status','/state','/verdict','/deltas','/semantic_slots','/evidence/focused_checks','/evidence/proof_review','/evidence/development_boundary','/graph_contribution/visual_review'} or q['path'].startswith('/source_review/') for q in ds)
  source_drift.append({'path':x['path'],'source_observed':x,'live':current,'admin_diffs':ds})
 else:verify_rec(x)
 paths.add(x['path'])
assert len(union)==90
# Actual committed raw receipts in BOTH packet and decoder run, not JSON reserialization.
tracked=subprocess.check_output(['git','ls-tree','-r','--name-only',C,'--',str(R).replace('\\','/'),'runs/20261007-companion-priority/anonymous-decoder-28']).decode().splitlines()
paths.update(tracked)
tracked_all=set(subprocess.check_output(['git','ls-tree','-r','--name-only',C]).decode().splitlines())
gitpaths=sorted(p for p in paths if p in tracked_all)
requests=''.join(C+':'+p+'\n' for p in gitpaths).encode()
buf=subprocess.check_output(['git','cat-file','--batch'],input=requests);offset=0;gitchecks=[]
for p in gitpaths:
 end=buf.index(b'\n',offset);head=buf[offset:end].split();size=int(head[-1]);offset=end+1
 b=buf[offset:offset+size];offset+=size+1;live=Path(p).read_bytes()
 assert sha(b.replace(b'\r\n',b'\n'))==sha(live.replace(b'\r\n',b'\n')),p
 raw_required=p.startswith(str(R).replace('\\','/')) or p.startswith('runs/20261007-companion-priority/anonymous-decoder-28/')
 if raw_required:assert b==live,p
 gitchecks.append(dict(rec(p),git_blob_sha=head[0].decode(),git_raw_sha256=sha(b),git_lf_sha256=sha(b.replace(b'\r\n',b'\n')),immutable_raw_exact=raw_required))
agg=(R/'aggregate.log').read_text(encoding='utf8')
assert '9132 jobs' in agg and '9394 jobs' in agg
assert subprocess.check_output(['git','diff',claim['base_commit'],C,'--','AutoSamplingTheory.lean','Tests.lean','AutoSamplingTheory/ExampleCases.lean'])==b''
recon={'status':'passed-scoped','checked_commit':C,'math_receipt':rec(R/'whole-math-review.json'),'original_math_freeze':rec(R/'math-freeze.json'),'original36_current_raw_unchanged':len(stable),'administrative_changed_inputs':diffs,'source_input_union_count':len(union),'source_input_current_drift':source_drift,'all_source_observed_raw_snapshots_verified':True,'all_current_bindings_and_contexts_exact':True,'portable_decoder_extension_integrity_verified':True,'canonical_label_projection_only_no_decoder_mathematical_drift':True,'Git_checked_inputs':gitchecks,'excluded_other_current_worktree_files':['research-wiki/cited-results/SLT_reuse_audit.md','research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl','runs/substantive_discoveries.jsonl','research-wiki/cited-results/SPHMC_gaussian_functional_availability_20261007.md','runs/20261007-companion-priority/gaussian-functional-availability/'],'no_future_formal_credit':True}
recon_rec=emit('reviewer.exact.admission-reconciliation.json',recon)
source_rec=emit('reviewer.exact.source-binding.json',{'status':'passed-scoped','checked_commit':C,'source_reviews':source,'source_union':[dict(x,current=rec(x['path'])) for x in union.values()],'reviewed_publication_targets':alltargets,'check_advance_reviewed_true':'PASS','generic_affine_is_metadata_revalidation_only':True})
fake_rec=emit('reviewer.exact.fake-closure.json',{'checked_commit':C,'reachable_file_count':32,'files':M['reachable_source_inputs'],'canonical_scanner':'astis.strip_lean_comments_and_strings + FORBIDDEN_REGEX per line','hits':fake,'printed_axioms':[{'declaration':d,'axioms':[z.strip() for z in a.split(',')]} for d,a in axs]})
V={'schema_version':1,'advance_id':claim['advance_id'],'verifier_id':'picard_commit_verifier_20261005','reviewer_role':'independent_verifier','verification_status':'passed-scoped','status':'passed-scoped','verified_commit':C,'checked_commit':C,'owner_is_not_verifier':True,'lean_declarations':claim['declarations'],'publication_declarations':claim['declarations'],'gate':{'focused':dict(log,status='PASS',jobs=3729),'metadata':gates,'reviewed_publication_gate':'check_advance(all3,reviewed=True) PASS; SAU target set exact2','current_root_gate':dict(rec(R/'aggregate.log'),status='authoritative-root-PASS-reused',root_jobs=9132,test_jobs=9394,mathematical_inputs_identical=True,root_imports_unchanged=True),'base_origin_main':subprocess.check_output(['git','rev-parse','origin/main']).decode().strip()},'whole_math_review_reused':rec(R/'whole-math-review.json'),'whole_math_scope':M['mathematical_checks'],'math_freeze_36_chain':recon_rec,'source_audit':source_rec,'source_reviews':source,'fake_closure_scan':fake_rec,'standard_axioms':['propext','Classical.choice','Quot.sound'],'conceptual_mirror_audit':{'status':'none-found'},'Git_evidence':{'checked_inputs':len(gitchecks),'raw_immutable_artifacts':sum(x['immutable_raw_exact'] for x in gitchecks),'source_union':len(union),'source_observed_current_admin_drift_count':len(source_drift),'all_exact_normalized_Git':True},'ProofSeal':{'status':'focused-proof-and-source-passed-scoped','repository_admission':'pending-root-serialized-integration-and-independent-repository-ProofSeal','source_coverage':'Preproof exact2 signatures / source-only topology retained; only analytic allpositive3.2/4.4/4.5+true affine posterior/lastTWO4.6. No fullLemma/paper badge.'},'truth_boundary':claim['truth_boundary'],'remaining_boundary':['FIRST4.6 Gaussian Talagrand/LSI/W2,4.2 bias,4.3 centeredMGF and fullLemma4.2 OPEN.','Joint posterior Markov-family measurability/sampling, histories/Picard/Wp/warmness, initialization, main results and both papers OPEN.','Numericalprox cap eta<=1/(2beta), genuine expected queries/work and actual input-accuracy/cost composition OPEN; TV never transfers unbounded cost.','Serialized shared integration/registry/graphs/site, scoped repository ProofSeal, independent purification/Exposition/rendered QA/current remoteCI remain pending.'],'generic_affine_code_unchanged_no_new_credit':True,'sole_stabilization_owner_preserved':'ASTIS-SA-20261005-SPHMCImplementedPhaseKernel','permitted_mutations':'Only this verifier evidence, exact2 claim cells independent state/evidence, one independent VERIFIED ledger transition. No production/Test/lesson/publication/audit/shared/site/Goal edits.','leases':{'compiler':'CLOSED','sessions':'CLOSED','writes':'CLOSED','background_processes':False},'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
vp=emit('verified.json',V)
print(json.dumps({'status':V['verification_status'],'verified_receipt':vp,'git_inputs':len(gitchecks),'immutable_raw_artifacts':sum(x['immutable_raw_exact'] for x in gitchecks),'math_original31_unchanged5admin':True,'source_union':len(union),'source_admin_drifts':len(source_drift),'source_runs':[x['review_run_sha256'] for x in source],'no_transition_yet':True}))
