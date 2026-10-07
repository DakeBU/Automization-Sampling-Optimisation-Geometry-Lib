from pathlib import Path
import json,hashlib,subprocess,sys,re,datetime
sys.path.insert(0,'tools')
import astis_publication as pub,astis,astis_advance as advance
R=Path('runs/20261007-companion-priority/standardized-rgo-relative-entropy')
C='171acfcefee8fee3f2858e8550d3c4b393f7a10c';P='3f01c4be14739067fc458033a74fa3937367fa61';V='picard_commit_verifier_20261005'
def j(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
def d(p):
 b=Path(p).read_bytes();return {'path':Path(p).as_posix(),'raw_sha256':sha(b),'lf_sha256':sha(b.replace(b'\r\n',b'\n')),'bytes':len(b)}
def w(p,x):Path(p).write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode())
def diff(a,b,p=''):
 if type(a)!=type(b):return [p]
 if isinstance(a,dict):return [q for k in sorted(set(a)|set(b)) for q in ([p+'/'+k] if k not in a or k not in b else diff(a[k],b[k],p+'/'+k))]
 if isinstance(a,list):
  if len(a)!=len(b):return [p]
  return [q for n,(x,y) in enumerate(zip(a,b)) for q in diff(x,y,p+'/'+str(n))]
 return [] if a==b else [p]
def blob(c,p):return subprocess.check_output(['git','show',c+':'+p])
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==C
verified=j(R/'verified.json');prior=j(R/'reviewer.exact.checks.json');integration=j(R/'integration.json');plan=j(R/'publication-plan.json')
assert verified['verification_status']=='passed-scoped' and verified['verified_commit']==P
assert d(R/'reviewer.exact.checks.json')['raw_sha256']==verified['owned_exact_checks']['raw_sha256']
assert integration['verified_proof_commit']==P
changed=subprocess.check_output(['git','diff','--name-only',P,C],text=True).splitlines()
allowed={'AutoSamplingTheory/ExampleCases.lean','Tests.lean','research-wiki/frontier-cells/'+plan['active_cells'][0]+'.json','docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json','runs/substantive_advances.jsonl'}
assert all(p in allowed or p.startswith(R.as_posix()+'/') for p in changed),changed
shared=[]
for path,line in [('AutoSamplingTheory/ExampleCases.lean','import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.StandardizedRGORelativeEntropy'),('Tests.lean','import Tests.StandardizedRGORelativeEntropy')]:
 old=blob(P,path).replace(b'\r\n',b'\n');new=blob(C,path).replace(b'\r\n',b'\n');assert line.encode()+b'\n' in new
 assert new.replace(line.encode()+b'\n',b'',1)==old
 assert Path(path).read_bytes().replace(b'\r\n',b'\n')==new
 shared.append(d(path))
cellpath='research-wiki/frontier-cells/'+plan['active_cells'][0]+'.json'
oldcell=json.loads(blob(P,cellpath));newcell=j(cellpath);cellchanges=diff(oldcell,newcell)
admin=['/status','/graph_contribution/visual_review','/evidence/execution_boundary','/evidence/independent_verification','/evidence/independent_verification_details','/evidence/integration_receipt']
assert all(any(x==a or x.startswith(a+'/') for a in admin) for x in cellchanges),cellchanges
assert newcell['status']=='independently_verified' and newcell['evidence']['independent_verification']==(R/'verified.json').as_posix()
# Preserve and match the whole earlier exact audit, rather than replay historical proofs.
rows=next(x['inputs'] for x in prior['checks'] if x['name']=='exact_Git_raw_LF_inputs')
selected={r['path'] for r in rows}|set(changed)|{'lean-toolchain','lake-manifest.json'}
tracked=set(subprocess.check_output(['git','ls-tree','-r','--name-only',C],text=True).splitlines());selected=sorted(selected&tracked)
proc=subprocess.Popen(['git','cat-file','--batch'],stdin=subprocess.PIPE,stdout=subprocess.PIPE);out,_=proc.communicate(('\n'.join(C+':'+p for p in selected)+'\n').encode());assert proc.returncode==0
pos=0;gitrows=[];gitblobs={}
for p in selected:
 stop=out.index(b'\n',pos);size=int(out[pos:stop].split()[-1]);pos=stop+1;b=out[pos:pos+size];pos+=size+1;gitblobs[p]=b;live=Path(p).read_bytes()
 raw=p.startswith(R.as_posix()+'/')
 assert (b==live if raw else b.replace(b'\r\n',b'\n')==live.replace(b'\r\n',b'\n')),(p,'current Git/live')
 gitrows.append({**d(p),'git_blob_sha256':sha(b),'comparison':'raw-exact' if raw else 'LF-exact'})
for r in rows:
 p=r['path']
 if p==cellpath:continue
 assert d(p)['raw_sha256']==r['raw_sha256'] and d(p)['lf_sha256']==r['lf_sha256'],(p,'prior proof footprint drift')
 assert sha(gitblobs[p])==r['git_blob_sha256'],(p,'prior Git drift')
# Current admission recomputed; whole source/decoder records exactly preserved.
data=pub.inputs();items={x['id']:x for x in pub.load()};item=items[plan['slugs'][0]];target=plan['mathematical_declarations'][0];binding=next(b for b in item['bindings'] if b['declaration']==target)
a=data['audits'][plan['audit_ids'][0]];s=verified['source_audit'];review=j(R/'source.0.review.json')
assert a['state']=='accepted' and a['source_review']['state']=='accepted'
assert pub.binding_digest(item,binding,data)==s['binding_sha256']
assert pub.review_context(item,binding,data)==review['current_review_context']
assert pub.digest({k:v for k,v in review.items() if k!='review_run_sha256'})==s['source_review_run_sha256']
assert d(R/'source.0.review.json')['raw_sha256']==verified['source_review']['raw_sha256']
pub.check_advance([target],reviewed=True)
assert Path('lean-toolchain').read_text().strip()==verified['Lean']
assert next(x for x in j('lake-manifest.json')['packages'] if x['name']=='mathlib')['rev']==verified['Mathlib']
rootchecks=[]
for check in integration['checks']:
 assert check['exit_code']==0 and d(check['log'])['raw_sha256']==check['raw_sha256']
 rootchecks.append({**check,'current_log':d(check['log'])})
# Fresh canonical and current reachable fake scans; prior axioms reused only on matching bodies.
closure=next(x for x in prior['checks'] if x['name']=='fresh_reachable_and_canonical_fake_scan')
fake=[]
for r in closure['reachable_inputs']:
 assert d(r['path'])['raw_sha256']==r['raw_sha256']
 for n,line in enumerate(astis.strip_lean_comments_and_strings(Path(r['path']).read_text(encoding='utf-8')).splitlines(),1):
  if astis.FORBIDDEN_REGEX.search(line):fake.append({'path':r['path'],'line':n,'text':line})
assert not fake and not astis.forbidden_pattern_hits()
assert advance.current_advances()[verified['advance_id']]['state']=='VERIFIED'
static_gap='Test theorem tails are not inline in companion HTML' in integration['reader_inspection']['rendered_visual_qa'];assert static_gap
# Fresh foreground gates must have genuine current shared root imports.
gates=j(R/'reviewer.repository.gates.json');assert gates['checked_commit']==C and len(gates['results'])==7 and all(x['returncode']==0 for x in gates['results'])
for r in gates['results']:assert d(r['path'])['raw_sha256']==r['raw_sha256']
log=(R/'reviewer.repository.aggregate.log').read_text(encoding='utf-8');assert '9138 jobs' in log and '9406 jobs' in log and 'ASTIS check passed' in log
axioms=[]
for name,vals in re.findall(r"'([^']+)' depends on axioms: \[([^\]]+)\]",log,re.S):
 if 'StandardizedRGORelativeEntropy' in name:
  aa={x.strip() for x in vals.split(',')};assert aa=={'propext','Classical.choice','Quot.sound'};axioms.append({'declaration':name,'axioms':sorted(aa)})
# Fresh cached Lake can replay or omit print statements; exact earlier3 checks still bound to unchanged bodies.
proof={'schema_version':1,'artifact_kind':'independent-scoped-repository-ProofSeal','verification_status':'passed-scoped','status':'accepted-scoped','checked_commit':C,'verified_proof_commit':P,'verifier_id':V,'advance_id':verified['advance_id'],'lean_declarations':[target],'source_audit':s,'Lean':verified['Lean'],'Mathlib':verified['Mathlib'],'independent_proof_receipt':d(R/'verified.json'),'independent_exact_checks':d(R/'reviewer.exact.checks.json'),'integration_receipt':d(R/'integration.json'),'shared_delta':shared,'changed_files':changed,'cell_admin_only':{'fields':cellchanges,'before_proof_commit':P,'current':d(cellpath)},'preserved_prior_input_count':len(rows)-1,'Git_raw_LF_checked_inputs':gitrows,'fresh_gates':gates,'root_integration_log_hash_checks':rootchecks,'fresh_aggregate_jobs':[9138,9406],'focused_reuse':{'count':3759,'basis':'Exact earlier independent whole mathematical and focused proof evidence reused by raw/LF/Git bytes; fresh repository root and Tests now include actual33imports.'},'standard_axioms':verified['standard_axioms'],'reused_standard_axiom_declarations':verified['reachable_axioms'],'fresh_aggregate_axiom_prints':axioms,'fake_closure_scan':{'canonical_files':len(astis.lean_source_files()),'canonical_hits':[],'reachable_modules':closure['reachable_modules'],'reachable_hits':[]},'ProofSeal':{'statement_and_mathematical_conditions':'Previously independently VERIFIED exact proof preserved','current_repository_conditions':'Fresh mandatory ASTIS and current source/publication/semantic/frontier/contributor/process/graph checks passed; actual33 source and Test now included','coverage':'Actual canonical finite KL, unique stationary proximal witness, L1 and AE formulas only; preproof source topology is scoped obligation inventory, not completion of FIRST4.6 or source paper'},'remaining_boundary':['Canonical llr equality is AE only; no pointwise RN differentiability/canonical Fisher/weak Sobolev certificate.','Gaussian LSI/T2/FIRST4.6 W2/bias/fullLemma/main/work/composition remain open.','STATIC_READER_DELIVERY_GAP retained: new Test theorem tails not inline; full Test source/link/CopyDownload/rendered visual/interaction/live delivery acceptance remains open.','Independent ExpositionSeal/postmerge purification and current33 remote CI/main merge/live admission remain separate; draftPR313 not merged.'],'no_new_VERIFIED_or_STABILIZING_transition':True,'sole_STABILIZING_lane':verified['sole_original_STABILIZING_lane'],'compiler_lease':'CLOSED','Python_lease':'CLOSED on final process exit','read_lease':'CLOSED','write_lease':'CLOSED','completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
w(R/'reviewer.repository.ProofSeal.json',proof)
w(R/'reviewer.repository.lease.json',{'status':'CLOSED','checked_commit':C,'verifier_id':V,'compiler':'CLOSED','Python':'CLOSED on process exit','read':'CLOSED','write':'CLOSED','receipt':d(R/'reviewer.repository.ProofSeal.json'),'canonical_inputs_modified':False,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
print(json.dumps({'status':'accepted-scoped','checked_commit':C,'receipt':d(R/'reviewer.repository.ProofSeal.json'),'Git_inputs':len(gitrows),'proof_inputs_preserved':len(rows)-1,'fresh_aggregate':[9138,9406],'fake_reachable':closure['reachable_modules'],'canonical_fake_files':len(astis.lean_source_files()),'all_leases':'CLOSED'}))
