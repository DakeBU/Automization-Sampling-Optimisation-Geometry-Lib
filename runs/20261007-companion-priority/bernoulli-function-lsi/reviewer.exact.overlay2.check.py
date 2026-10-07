from pathlib import Path
import json,subprocess,hashlib,sys,re,datetime
sys.path.insert(0,'tools')
import astis_publication as pub,astis_contributor_contract as contributor,astis,astis_advance as advance
R=Path('runs/20261007-companion-priority/bernoulli-function-lsi');O=R/'cell-mirror-metadata-overlay2'
C='6d5df34cdb124e28022f16f566ff549145eb7e65';P='a83ce789bd4f3ce22c3757129282c9ad488c2ccf';V='picard_commit_verifier_20261005'
def j(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
def desc(p):
 b=Path(p).read_bytes();return {'path':Path(p).as_posix(),'raw_sha256':sha(b),'lf_sha256':sha(b.replace(b'\r\n',b'\n')),'bytes':len(b)}
def diff(a,b,p=''):
 if type(a)!=type(b):return [p]
 if isinstance(a,dict):return [q for k in sorted(a.keys()|b.keys()) for q in ([p+'/'+k] if k not in a or k not in b else diff(a[k],b[k],p+'/'+k))]
 if isinstance(a,list):return [p] if len(a)!=len(b) else [q for i,(x,y) in enumerate(zip(a,b)) for q in diff(x,y,p+'/'+str(i))]
 return [] if a==b else [p]
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==C
plan=j(R/'publication-plan.json');A=j(R/'claim.json')['advance_id'];decls=plan['mathematical_declarations']
old=j(R/'reviewer.exact.failed-admission.json');assert old['checked_commit']==P and not old['VERIFIED_transition_published']
assert desc(R/'reviewer.exact.failed-admission.json')['raw_sha256']=='f21c844e341faebf5f7629e86fe0433b04e8e686c95d1757372de6755ab9dc42'
review=j(O/'overlay2.review.json');lease=j(O/'reviewer.overlay2.lease.json')
assert pub.digest({k:v for k,v in review.items() if k!='review_run_sha256'})==review['review_run_sha256']
assert pub.digest({k:v for k,v in lease.items() if k!='lease_run_sha256'})==lease['lease_run_sha256']
assert review['independent_from_overlay_author'] and not review['blocking'] and not review['deltas'] and not review['repairs'] and review['verdict']=='accepted-scoped-metadata-only'
assert lease['status']=='CLOSED' and lease['compiler_started'] is False
cells=[]
for i,c in enumerate(plan['active_cells']):
 p=Path('research-wiki/frontier-cells')/(c+'.json');before=O/f'cell.{i}.before.raw.snapshot.json';after=O/f'cell.{i}.after.raw.snapshot.json'
 assert p.read_bytes()==after.read_bytes()
 assert diff(j(before),j(after))==['/graph_contribution/functor_view']
 assert before.read_bytes().replace(b'"functor_view": "none-found"',b'"functor_view": "candidate-published"')==after.read_bytes()
 assert subprocess.check_output(['git','show',P+':'+p.as_posix()]).replace(b'\r\n',b'\n')==before.read_bytes().replace(b'\r\n',b'\n')
 cells.append({'path':p.as_posix(),'before':desc(before),'current':desc(p),'exact_pointer':'/graph_contribution/functor_view','old':'none-found','new':'candidate-published'})
changed=subprocess.check_output(['git','diff','--name-only',P,C],text=True).splitlines()
assert [p for p in changed if not p.startswith(R.as_posix()+'/')]==[x['path'] for x in cells]
row_checks=[]
for row in review['input_artifacts']:
 assert desc(row['raw_snapshot'])['raw_sha256']==row['raw_sha256'] and desc(row['raw_snapshot'])['lf_sha256']==row['lf_sha256']
 if row['path'].startswith('.astis/'):
  row_checks.append({'path':row['path'],'checked_immutable_snapshot':row['raw_snapshot'],'ignored_original_not_used_as_formal_truth':True});continue
 assert desc(row['path'])['raw_sha256']==row['raw_sha256'] and desc(row['path'])['lf_sha256']==row['lf_sha256']
 row_checks.append({'path':row['path'],'raw_sha256':row['raw_sha256'],'lf_sha256':row['lf_sha256']})
reused=[]
for check in old['checks']:
 if check['name']=='exact_Git_current_raw_LF':
  for row in check['inputs']:
   actual=desc(row['path'])
   if row['path'] in [x['path'] for x in cells]:continue
   assert actual['raw_sha256']==row['raw_sha256'] and actual['lf_sha256']==row['lf_sha256'],row['path']
  reused.append({'prior_Git_inputs':check['count'],'unchanged_non_cell_inputs':check['count']-2})
data=pub.inputs();items={i['id']:i for i in pub.load()};sources=[]
for i,decl in enumerate(decls):
 item=items[plan['slugs'][i]];b=next(b for b in item['bindings'] if b['declaration']==decl);a=data['audits'][plan['audit_ids'][i]]
 s=j(R/f'source.{i}.review.overlay1.json');packet=j(R/f'source.{i}.reviewer-packet.overlay1.json')
 assert pub.digest({k:v for k,v in s.items() if k!='review_run_sha256'})==s['review_run_sha256']==a['source_review']['review_run_sha256']
 assert pub.binding_digest(item,b,data)==s['publication_binding_sha256']==packet['publication_binding_sha256']==a['publication_binding_sha256']
 assert pub.review_context(item,b,data)==packet['candidate_publication_context'] and a['state']=='accepted'
 sources.append({'declaration':decl,'review_run_sha256':s['review_run_sha256'],'binding_sha256':s['publication_binding_sha256'],'current_accepted':True})
pub.check_advance(decls,reviewed=True)
discovery=advance.current_discoveries()['ASTIS-DISC-20261007-BernoulliGaussianEntropyEnergyMirror']
assert discovery['status']=='validated' and discovery['latest_actor']=='phase_source_reviewer_20261005'
oldlog=(R/'reviewer.exact.contributor.log').read_text(encoding='utf-8')
targets=set(re.findall(r'^- declaration: (.+)$',oldlog,re.M));changed_cells=set(re.findall(r'^- cell: (.+)$',oldlog,re.M))
assert len(targets)==80 and len(changed_cells)==76
assert not contributor.validate_targets(targets,pub.load(),pub.inputs(),changed_cells)
scope={'status':'PASS exact committed34 contributor target scope only','targets':len(targets),'cells':len(changed_cells),'base':subprocess.check_output(['git','rev-parse','origin/main'],text=True).strip(),'scope_derivation':'Retained actual a83 base-to-working-tree 80/76 inventory, same base HEAD, successor has only two canonical cell field replacements and task receipts. Untracked35 not in either34 commit. validate_targets executed against exact unchanged mapped declarations/lessons and repaired current cells. This is not the live all-workspace CLI PASS.'}
scopepath=R/'reviewer.exact.overlay2.contributor-scoped.json';scopepath.write_bytes((json.dumps(scope,ensure_ascii=False,indent=2)+'\n').encode())
gates=j(R/'reviewer.exact.overlay2.gates.json');assert gates['checked_commit']==C and len(gates['results'])==5
assert [(x['name'],x['returncode']) for x in gates['results'] if x['returncode']]==[('publication',1)]
for row in gates['results']:assert desc(row['path'])['raw_sha256']==row['raw_sha256']
for name in ['publication','contributor']:
 log=(R/f'reviewer.exact.overlay2.{name}.log').read_text(encoding='utf-8')
 assert 'BalancedRademacherCLT.lean: private implementation has no fresh, accepted whole-module public theorem review' in log
assert not astis.forbidden_pattern_hits()
current_fake={'canonical_files':len(astis.lean_source_files()),'hits':[],'scope_note':'Live scan includes untracked35 only as placeholder check, not admitted mathematics. Prior exact34 closure3/877-file scan and six direct standard3 prints reused by unchanged34 inputs.'}
selected=subprocess.check_output(['git','ls-tree','-r','--name-only',C,'--',R.as_posix()],text=True).splitlines()+[x['path'] for x in cells]
proc=subprocess.Popen(['git','cat-file','--batch'],stdin=subprocess.PIPE,stdout=subprocess.PIPE);out,_=proc.communicate(('\n'.join(C+':'+p for p in selected)+'\n').encode());assert proc.returncode==0
offset=0;gitrows=[]
for p in selected:
 end=out.index(b'\n',offset);n=int(out[offset:end].split()[-1]);offset=end+1;blob=out[offset:offset+n];offset+=n+1;live=Path(p).read_bytes();raw=p.startswith('runs/')
 assert (blob==live if raw else blob.replace(b'\r\n',b'\n')==live.replace(b'\r\n',b'\n'))
 gitrows.append({**desc(p),'git_blob_sha256':sha(blob),'mode':'raw-exact' if raw else 'LF-exact'})
assert advance.current_advances()[A]['state']=='PROVED_LOCAL'
report={'schema_version':1,'verification_status':'bounded34-ready-global-workspace-admission-blocked','checked_commit':C,'failed_parent_commit':P,'advance_id':A,'verifier_id':V,'two_cell_overlay':cells,'independent_overlay2_review':desc(O/'overlay2.review.json'),'overlay2_run_sha256':review['review_run_sha256'],'overlay2_41_input_chain':row_checks,'reused_prior_exact_math_source_focused6standard3_evidence':reused,'current_reviewed2source_bindings':sources,'current_exact_committed_contributor_scope':scope,'live_gates':gates,'current_fake_scan':current_fake,'exact_currentGit_inputs':gitrows,'exact_currentGit_input_count':len(gitrows),'untracked35_excluded_from_proof_credit':True,'blocking_global_checks':['Live publication --base origin/main and contributor --base origin/main include untracked35 with no fresh accepted whole-module review; both terminal failures preserved. No live all-workspace PASS or VERIFIED claimed.'],'VERIFIED_transition_published':False,'remaining_boundary':['34 signed scalar and actual finite Bool LSI only, coefficient1/2, alln including0.','Gaussian law/entropy/flip-energy limits, GaussianLSI/T2/W2/FIRST4.6/bias/fullLemma/main/work/composition open.','Shared integration/ProofSeal/ExpositionSeal/currentCI separate.'],'leases':{'read':'CLOSED','write':'CLOSED','compiler':'CLOSED','Python':'CLOSED'},'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
dest=R/'reviewer.exact.overlay2.ready.json';assert not dest.exists();dest.write_bytes((json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode())
(R/'reviewer.exact.overlay2.lease.json').write_bytes((json.dumps({'status':'CLOSED','checked_commit':C,'verifier_id':V,'read':'CLOSED','write':'CLOSED','compiler':'CLOSED','Python':'CLOSED','receipt':desc(dest),'VERIFIED_transition_published':False},ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps({'status':report['verification_status'],'receipt':desc(dest),'Git_inputs':len(gitrows),'leases':'CLOSED'}))
