from pathlib import Path
import json, hashlib, subprocess, sys, re, datetime
sys.path.insert(0, 'tools')
import astis_publication as pub, astis_advance as advance, astis
R=Path('runs/20261007-companion-priority/balanced-rademacher-clt')
R34=Path('runs/20261007-companion-priority/bernoulli-function-lsi')
C='4d9e71a6b835b54453a5cfd2d132f9a51f66f69c'; C34='6d5df34cdb124e28022f16f566ff549145eb7e65'
V='picard_commit_verifier_20261005'
def j(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(b): return hashlib.sha256(b).hexdigest()
def desc(p):
 b=Path(p).read_bytes(); return {'path':Path(p).as_posix(),'raw_sha256':sha(b),'lf_sha256':sha(b.replace(b'\r\n',b'\n')),'bytes':len(b)}
def pin(row,path=None):
 d=desc(path or row['path']); assert d['raw_sha256']==row['raw_sha256'],(d,row)
 if row.get('lf_sha256') is not None: assert d['lf_sha256']==row['lf_sha256'],(d,row)
 if 'bytes' in row: assert d['bytes']==row['bytes'],(d,row)
 return d
def diff(a,b,p=''):
 if type(a)!=type(b): return [p]
 if isinstance(a,dict): return [q for k in sorted(a.keys()|b.keys()) for q in ([p+'/'+k] if k not in a or k not in b else diff(a[k],b[k],p+'/'+k))]
 if isinstance(a,list): return [p] if len(a)!=len(b) else [q for i,(x,y) in enumerate(zip(a,b)) for q in diff(x,y,p+'/'+str(i))]
 return [] if a==b else [p]
def hash_object(d,k): assert pub.digest({x:y for x,y in d.items() if x!=k})==d[k]
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==C
assert subprocess.check_output(['git','-C','.lake/packages/mathlib','rev-parse','HEAD'],text=True).strip()=='db584cd6d46c92f209a44c0f1c829460d327499d'
assert Path('lean-toolchain').read_text().strip()=='leanprover/lean4:v4.33.0'
gates=j(R/'reviewer.exact.gates.json'); assert gates['checked_commit']==C and len(gates['results'])==8
for row in gates['results']: assert row['returncode']==0; pin(row)
assert 'ASTIS check passed' in (R/'reviewer.exact.aggregate.log').read_text(encoding='utf-8')
assert re.findall(r'Build completed successfully \((\d+) jobs\)',(R/'reviewer.exact.aggregate.log').read_text(encoding='utf-8'))==['9138','9406']
axioms=re.findall(r"'([^']+)' depends on axioms: \[([^\]]+)\]",(R/'reviewer.exact.direct-axioms.log').read_text(encoding='utf-8'),re.S)
assert len(axioms)==3 and all(set(x.strip() for x in a.split(','))=={'propext','Classical.choice','Quot.sound'} for _,a in axioms)
prior=j(R34/'reviewer.exact.overlay2.ready.json');assert prior['checked_commit']==C34 and not prior['VERIFIED_transition_published']
assert desc(R34/'reviewer.exact.overlay2.ready.json')['raw_sha256']=='54be7b9a72f26ff01f423483ff067337941d4a3839b95b77e7aa2da8fac4fd61'
for row in prior['exact_currentGit_inputs']: pin(row)
assert len(prior['exact_currentGit_inputs'])==468
math=j(R/'whole-proof-review/math.review.json');assert math['actor']!=V and math['verdict']=='ACCEPTED_SCOPED_WHOLE_MATHEMATICAL_PROOF' and not math['blockers'] and math['all_private_providers_reviewed']==14
pin(math['input_bindings']); bindings=j(math['input_bindings']['path']); assert len(bindings['inputs'])==35
mathrows=[]
for row in bindings['inputs']:
 pin(row)
 if 'raw_snapshot' in row:
  snap=R/'whole-proof-review'/row['raw_snapshot']; pin(row,snap)
  assert (R/'whole-proof-review'/row['lf_snapshot']).read_bytes()==Path(row['path']).read_bytes().replace(b'\r\n',b'\n')
 else: assert row['role']=='fresh independent foreground compilation evidence'
 mathrows.append(desc(row['path']))
freeze=j(R/'math-freeze.json');assert len(freeze['inputs'])==14
for row in freeze['inputs']: pin(row)
mr=j(R/'whole-proof-review/run.json');assert pub.digest({k:v for k,v in mr.items() if k not in {'deterministic_run_sha256','status'}})==mr['deterministic_run_sha256'];assert mr['status']=='CLOSED' and mr['compiler_terminal']
for key in ['bindings','parent_API','reachability_scan','review']:pin(mr[key])
parents=j(math['actual_parent_API_review']['path']);pin(math['actual_parent_API_review'])
for row in parents['regions']:
 assert sha(Path(row['path']).read_bytes())==row['source_file_raw_sha256']
 pin(row,R/'whole-proof-review'/row['snapshot'])
 lo,hi=row['lines'];assert b''.join(Path(row['path']).read_bytes().splitlines(keepends=True)[lo-1:hi])==(R/'whole-proof-review'/row['snapshot']).read_bytes()
seal=R/'whole-proof-review/exact-sealed-header.lf.snapshot';assert desc(seal)['raw_sha256']==math['exact_statement']['production_extracted_LF_sha256']=='271595fa838cf28466cf90591d2c6aaa1024b42a1af73d85eee25cfc32e04777'
assert len(seal.read_bytes())==573
module=Path(freeze['inputs'][0]['path']).read_bytes().replace(b'\r\n',b'\n')
assert seal.read_bytes().rstrip()+b' := by' in module
data=pub.inputs();items={x['id']:x for x in pub.load()};sourcechecks=[]
for run,number,suffix in [(R34,0,'.overlay1'),(R34,1,'.overlay1'),(R,0,'')]:
 plan=j(run/'publication-plan.json');decl=plan['mathematical_declarations'][number];item=items[plan['slugs'][number]]
 b=next(x for x in item['bindings'] if x['declaration']==decl);audit=data['audits'][plan['audit_ids'][number]]
 source=j(run/f'source.{number}.review{suffix}.json');packet=j(run/f'source.{number}.reviewer-packet{suffix}.json')
 hash_object(source,'review_run_sha256');hash_object(packet,'packet_sha256')
 assert source['reviewer']!=V and source['independent_from_formalizer'] and source['independent_from_decoder']
 assert source['verdict']=='equivalent-after-elaboration' and not source['blocking'] and source['deltas']==[] and source['repairs']==[]
 assert set(source['semantic_slots'])=={'objects','domains','quantifiers','assumptions','conclusion','scopes','constant_dependencies'}
 assert pub.binding_digest(item,b,data)==source['publication_binding_sha256']==packet['publication_binding_sha256']==audit['publication_binding_sha256']
 assert pub.review_context(item,b,data)==packet['candidate_publication_context']
 assert audit['state']=='accepted' and audit['source_review']['review_run_sha256']==source['review_run_sha256']
 sourcechecks.append({'declaration':decl,'source_receipt':desc(run/f'source.{number}.review{suffix}.json'),'packet':desc(run/f'source.{number}.reviewer-packet{suffix}.json'),'review_run_sha256':source['review_run_sha256'],'binding_sha256':source['publication_binding_sha256'],'audit_id':plan['audit_ids'][number],'reviewed':True})
for run in [R34,R]:
 plan=j(run/'publication-plan.json');pub.check_advance(plan['mathematical_declarations'],reviewed=True)
 A=j(run/'claim.json')['advance_id'];assert advance.current_advances()[A]['state']=='PROVED_LOCAL' and advance.current_advances()[A]['owner_id']!=V
source=j(R/'source.0.review.json');drifts=[];sourceunion=[]
for row in source['input_artifacts']:
 pin(row,row['reviewer_raw_snapshot'])
 if row.get('reviewer_lf_snapshot'):assert Path(row['reviewer_lf_snapshot']).read_bytes()==Path(row['reviewer_raw_snapshot']).read_bytes().replace(b'\r\n',b'\n')
 if desc(row['path'])['raw_sha256']!=row['raw_sha256']:
  ds=diff(j(row['reviewer_raw_snapshot']),j(row['path']))
  if '/audits/' in row['path']:
   allowed={'/verdict','/semantic_slots','/state','/source_review/evidence','/source_review/run_artifact','/source_review/independent_from_formalizer','/source_review/reviewer_packet_sha256','/source_review/review_run_sha256','/source_review/state','/source_review/reviewer','/source_review/independent_from_decoder','/deltas'}
   assert set(ds)==allowed
  else:assert set(ds)=={'/status','/evidence/proof_review','/evidence/source_review','/evidence/execution_boundary'}
  drifts.append({'path':row['path'],'before':pin(row,row['reviewer_raw_snapshot']),'current':desc(row['path']),'exact_admin_pointers':ds})
 else:pin(row)
 sourceunion.append(desc(row['path']))
assert len(sourceunion)==77 and len(drifts)==2
overlay=j(R/'source-evidence-representation-overlay1/overlay.review.json');hash_object(overlay,'review_run_sha256')
assert overlay['verdict']=='accepted-scoped-metadata-only' and not overlay['blocking'] and overlay['projection_entire_list_roundtrip_exact']
assert overlay['exact_allowed_dict_diff']==['/source_review/evidence']
for row in overlay['input_artifacts']:pin(row,row['reviewer_raw_snapshot'])
audit=data['audits'][j(R/'publication-plan.json')['audit_ids'][0]]
expected=json.dumps(source['review_evidence'],ensure_ascii=False,sort_keys=True,separators=(',',':'))
assert audit['source_review']['evidence']==expected and sha(expected.encode())==overlay['projected_evidence_sha256']
decode=j(R/'anonymous-decoder/run.json');assert pub.digest(decode['basis'])==decode['decoder_run_sha256']==source['decoder_run_sha256']
assert decode['status']=='CLOSED' and not decode['compiler_started'] and not decode['source_text_visible']
dp=j(R/'anonymous-decoder/packet0.json');hash_object(dp,'packet_sha256');assert dp['packet_sha256']==source['decoder_packet_sha256']
result=j(R/'anonymous-decoder/result0.json');assert result['reconstructed_text_sha256']==source['reconstructed_text_sha256']
assert sha(result['reconstructed_theorem_text'].encode())==source['reconstructed_text_sha256']
assert decode['basis']['reconstruction']['reconstructed_theorem_text']==result['reconstructed_theorem_text']
pin(decode['input_bindings'][0],R/'anonymous-decoder/packet0.json')
for row in decode['output_bindings']:
 p=R/'anonymous-decoder'/Path(row['path']).name
 if p.exists():pin(row,p)
topology_path=Path('runs/20261007-companion-priority/rademacher-law-source-graph-review/source-topology-review.repaired.json')
topology=j(topology_path);hash_object(topology,'review_run_sha256');assert topology['status']=='accepted-scoped' and topology['independent_from_graph_author'] and not topology['implementation35_exposure'] and not topology['blocking']
for key in ['review_target','source_inventory','repair']:pin(topology[key])
for row in topology['input_artifacts']:pin(row,row['reviewer_raw_snapshot'])
assert topology['coverage']['graph_nodes']==54 and topology['coverage']['graph_edges']==107 and topology['coverage']['source_regions']==79
assert advance.current_discoveries()['ASTIS-DISC-20261007-BernoulliGaussianEntropyEnergyMirror']['status']=='validated'
assert not astis.forbidden_pattern_hits()
files=astis.lean_source_files();closure=[Path('AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/TwoPointEntropy.lean'),Path('AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/BernoulliLogSobolev.lean'),Path('Tests/BernoulliLogSobolev.lean'),Path('AutoSamplingTheory/TechnicalLemmas/Probability/BalancedRademacherCLT.lean'),Path('Tests/BalancedRademacherCLT.lean')]
for p in closure:assert not astis.FORBIDDEN_REGEX.search(astis.strip_lean_comments_and_strings(p.read_text(encoding='utf-8')))
selected=set(subprocess.check_output(['git','ls-tree','-r','--name-only',C,'--',R.as_posix()],text=True).splitlines())
selected|={x['path'] for x in prior['exact_currentGit_inputs']};selected|={r['path'] for r in sourceunion if not r['path'].startswith('.lake/')}
selected|={topology_path.as_posix(),topology['review_target']['path'],topology['source_inventory']['path']}
selected=sorted(selected)
proc=subprocess.Popen(['git','cat-file','--batch'],stdin=subprocess.PIPE,stdout=subprocess.PIPE);out,_=proc.communicate(('\n'.join(C+':'+p for p in selected)+'\n').encode());assert proc.returncode==0
offset=0;gitrows=[]
for p in selected:
 end=out.index(b'\n',offset);header=out[offset:end].split();assert header[-1]!=b'missing',(p,header)
 n=int(header[-1]);offset=end+1;blob=out[offset:offset+n];offset+=n+1;live=Path(p).read_bytes();raw=p.startswith('runs/')
 assert (blob==live if raw else blob.replace(b'\r\n',b'\n')==live.replace(b'\r\n',b'\n')),p
 gitrows.append({**desc(p),'git_blob_sha256':sha(blob),'mode':'raw-exact' if raw else 'LF-exact'})
assert subprocess.check_output(['git','diff','--name-only',C34,C,'--','AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/TwoPointEntropy.lean','AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/BernoulliLogSobolev.lean','Tests/BernoulliLogSobolev.lean'],text=True).strip()==''
report={'schema_version':1,'status':'passed-scoped-exact-admission-ready','checked_working_head':C,'proof_commits':{'34':C34,'35':C},'verifier_id':V,'fresh_gates':gates,'new35_direct_standard_axioms':dict(axioms),'named_axioms':['propext','Classical.choice','Quot.sound'],'prior34_ready':desc(R34/'reviewer.exact.overlay2.ready.json'),'prior34_unchanged_exactGit_inputs':len(prior['exact_currentGit_inputs']),'35_math_review':desc(R/'whole-proof-review/math.review.json'),'35_math_run_sha256':mr['deterministic_run_sha256'],'35_math_inputs35':mathrows,'35_freeze14_unchanged':True,'35_parent_API_regions_checked':len(parents['regions']),'current3_source_bindings':sourcechecks,'35_source_input_union':sourceunion,'35_exact_admin_reconciliation':drifts,'35_evidence_representation_overlay':desc(R/'source-evidence-representation-overlay1/overlay.review.json'),'35_sourceblind_decoder_run_sha256':decode['decoder_run_sha256'],'35_independent_topology':desc(topology_path),'35_topology_scope':topology['coverage'],'exact_currentGit_inputs':gitrows,'exact_currentGit_input_count':len(gitrows),'fake_closure_scan':{'full_canonical_files':len(files),'reachable_selected_files':[desc(p) for p in closure],'hits':[],'full_scan_and_current_ASTIS_gate_passed':True},'remaining_boundary':['34 actual signed two-point/Bernoulli finite function LSI only, coefficient1/2, alln including0.','35 actual all-N normalized Boolean count law, N0Dirac0 and successor weakGaussian0 variance1 only. No entropy or unbounded-observable limit follows from weak convergence.','Gaussian entropy/derivative limit and full flip-energy4, Gaussian functionLSI, finite-Hilbert/domain extension, T2/FIRST4.6/bias/fullLemma/main/querywork/composition open.','Current shared imports/Registry remain prior33 leaf476; new34/35 repository integration/ProofSeal/Exposition/purification/remoteCI are separate.'],'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
dest=R/'reviewer.exact.bindings.json';assert not dest.exists();dest.write_bytes((json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps({'status':report['status'],'receipt':desc(dest),'source_union':len(sourceunion),'Git_input_count':len(gitrows),'full_fake_files':len(files)}))
