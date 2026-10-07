from pathlib import Path
import json,hashlib,subprocess,sys,re,datetime
sys.path.insert(0,'tools')
import astis_publication as pub,astis,astis_advance as advance
R=Path('runs/20261007-companion-priority/standardized-rgo-relative-entropy')
C='3f01c4be14739067fc458033a74fa3937367fa61';V='picard_commit_verifier_20261005'
A='ASTIS-SA-20261007-StandardizedRGORelativeEntropy'
def j(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
def desc(p):
 b=Path(p).read_bytes();return {'path':Path(p).as_posix(),'raw_sha256':sha(b),'lf_sha256':sha(b.replace(b'\r\n',b'\n')),'bytes':len(b)}
def canon(d,key):return pub.digest({k:v for k,v in d.items() if k!=key})
def diffs(a,b,p=''):
 if type(a)!=type(b):return [p]
 if isinstance(a,dict):return [q for k in sorted(set(a)|set(b)) for q in ([p+'/'+k] if k not in a or k not in b else diffs(a[k],b[k],p+'/'+k))]
 if isinstance(a,list):
  if len(a)!=len(b):return [p]
  return [q for n,(x,y) in enumerate(zip(a,b)) for q in diffs(x,y,p+'/'+str(n))]
 return [] if a==b else [p]
paths=set();checks=[]
def bind(rec,path=None):
 p=Path(path or rec['path']);actual=desc(p)
 assert actual['raw_sha256']==rec['raw_sha256'],(p,'raw mismatch')
 assert actual['lf_sha256']==rec['lf_sha256'],(p,'LF mismatch')
 if 'bytes' in rec:assert actual['bytes']==rec['bytes'],(p,'bytes mismatch')
 paths.add(p.as_posix());return actual
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==C
plan=j(R/'publication-plan.json');proved=j(R/'proved-local.json')
assert proved['lean_declarations']==proved['publication_declarations']==plan['mathematical_declarations']
math=j(R/'reviewer.math.review.json');assert math['verdict']=='ACCEPTED_SCOPED_WHOLE_MATHEMATICAL_PROOF' and not math['blockers'] and math['full_body_and_tests_reviewed']
freeze=j(R/'math-freeze.json')
for row in freeze['inputs']:bind(row)
mathinputs=j(R/'reviewer.math.inputs.json')['inputs'];assert len(mathinputs)==68
for row in mathinputs:
 bind(row);bind(row,row['raw_snapshot'])
 p=Path(row['lf_snapshot']);assert sha(p.read_bytes())==row['lf_sha256'];paths.add(p.as_posix())
mathrun=j(R/'reviewer.math.run.json');assert pub.digest(mathrun['evidence_artifacts'])==mathrun['review_run_sha256']==math['review_run_sha256']
for row in mathrun['evidence_artifacts']:bind(row)
bind(mathrun['review'])
for seal in j(R/'preproof/statement-seals.accepted.json')['signatures']:
 text=Path(seal['file']).read_text(encoding='utf-8');start=text.index('theorem '+seal['full_declaration'].split('.')[-1]+'\n');stop=text.index(' := by',start)
 actual=text[start:stop]+'\n';assert actual==seal['signature_text'] and sha(actual.encode())==seal['signature_lf_sha256']
checks.append({'name':'whole_math_freeze_and_exact_signature','math_review':desc(R/'reviewer.math.review.json'),'math_run_sha256':mathrun['review_run_sha256'],'freeze_inputs':len(freeze['inputs']),'whole_math_inputs':len(mathinputs),'math_evidence_artifacts':len(mathrun['evidence_artifacts']),'body_review':'Entire actual155-line production including uniqueness/integrability/canonical KL/AE logratio and both actual119-line Test proofs with all3 private Test declarations read independently; distinct whole mathematical reviewer evidence reused only after exact raw/LF checks.'})
data=pub.inputs();items={x['id']:x for x in pub.load()};aid=plan['audit_ids'][0];a=data['audits'][aid]
review=j(R/'source.0.review.json');packet=j(R/'source.0.reviewer-packet.json');item=items[plan['slugs'][0]];b=next(x for x in item['bindings'] if x['declaration']==plan['mathematical_declarations'][0])
assert a['state']=='accepted' and a['source_review']['state']=='accepted'
assert canon(review,'review_run_sha256')==review['review_run_sha256']==a['source_review']['review_run_sha256']
assert canon(packet,'packet_sha256')==packet['packet_sha256']==review['reviewer_packet_sha256']
assert sha((R/'source.0.reviewer-packet.json').read_bytes())==review['packet_raw_sha256']
assert review['verdict']=='equivalent-after-elaboration' and not review['blocking'] and not review['blockers'] and not review['deltas'] and not review['repairs'] and not review['EXCESS']
assert review['independent_from_formalizer'] and review['independent_from_decoder']
assert set(review['semantic_slots'])=={'objects','domains','quantifiers','assumptions','conclusion','scopes','constant_dependencies'}
current=pub.binding_digest(item,b,data);assert current==a['publication_binding_sha256']==review['publication_binding_sha256']==packet['publication_binding_sha256']
assert pub.review_context(item,b,data)==review['current_review_context']
assert sha(packet['source']['original_text'].encode())==packet['source']['text_sha256']==review['source_text_sha256']
assert sha(packet['lean']['statement'].encode())==packet['lean']['statement_sha256']==review['lean_statement_sha256']
module=desc(packet['lean']['file']);assert module['raw_sha256']==review['whole_module_raw_sha256'] and module['lf_sha256']==review['whole_module_lf_sha256']==review['whole_module_file_sha256']
assert review['whole_module_covered'] and review['private_implementation_covered'] and review['test_whole_module_covered'] and review['test_private_helpers_covered']
assert review['production_private_helper_count']==0
adapter=j(R/'anonymous-decoder/contract-adapter-run.json');contract=j(R/'anonymous-decoder/result0.contract.json');original=j(R/'anonymous-decoder/result0.json');run=j(R/'anonymous-decoder/run.json');blind=j(R/'anonymous-decoder/packet0.json')
assert canon(adapter,'run_sha256')==adapter['run_sha256']==contract['decoder_run_sha256']==review['decoder_run_sha256']==a['reconstruction']['decoder_run_sha256']
assert canon(contract,'decoder_run_sha256')==adapter['contract_result_projection_sha256']
assert canon(run,'run_sha256')==run['run_sha256']==adapter['original_run_canonical_digest']
assert contract['reconstructed_theorem_text']==original['mathematical_reconstruction']
assert sha(contract['reconstructed_theorem_text'].encode())==contract['reconstructed_text_sha256']==review['reconstruction_text_sha256']==a['reconstruction']['text_sha256']
assert contract['reconstructed_theorem_text']==a['reconstruction']['text']
assert adapter['mathematical_text_changed'] is False and adapter['semantic_strings_changed'] is False and adapter['source_text_visible'] is False
for old,new in adapter['semantic_mapping'].items():assert original['semantic_slots'][old]==contract[new]
for p,rawsha in adapter['input_raw_sha256'].items():assert sha((R/'anonymous-decoder'/p).read_bytes())==rawsha
assert adapter['packet_sha256']==blind['packet_sha256']==review['decoder_packet_sha256']
assert not run['source_text_visible'] and not run['compiler_started'] and not adapter['compiler_started']
drifts=[]
for row in review['input_artifacts']:
 bind(row,row['snapshot']);h=desc(row['path']);paths.add(row['path'])
 if h['raw_sha256']!=row['raw_sha256']:
  delta=diffs(j(row['snapshot']),j(row['path']))
  if row['path']=='research-wiki/semantic-roundtrip/audits/'+aid+'.json':
   allowed=['/state','/semantic_slots','/deltas','/verdict','/source_review']
  elif row['path']=='research-wiki/frontier-cells/'+plan['active_cells'][0]+'.json':
   allowed=['/status','/evidence/execution_boundary','/evidence/proof_review','/evidence/source_review']
  else:raise AssertionError(('unexpected source drift',row['path'],delta))
  assert all(any(x==q or x.startswith(q+'/') for q in allowed) for x in delta),delta
  drifts.append({'path':row['path'],'source_snapshot':row['snapshot'],'reviewed_raw_sha256':row['raw_sha256'],'current':h,'administrative_only_fields':delta})
cell=data['cells'][plan['active_cells'][0]];parents=cell['reuse_plan']['reused_declarations']
assert parents==data['lessons'][plan['mathematical_declarations'][0]]['astis_dependencies']==plan['actual_ASTIS_parents'][0]
assert len(parents)==5 and cell['status']=='proved_locally'
pub.check_advance(plan['mathematical_declarations'],reviewed=True)
checks.append({'name':'current_encoder_denoiser_source_admission','review':desc(R/'source.0.review.json'),'source_review_run_sha256':review['review_run_sha256'],'packet_sha256':packet['packet_sha256'],'binding_sha256':current,'all7slots':list(review['semantic_slots']),'input_artifact_count':len(review['input_artifacts']),'neutral_sourceblind_adapter':desc(R/'anonymous-decoder/contract-adapter-run.json'),'adapter_run_sha256':adapter['run_sha256'],'original_decoder_run':desc(R/'anonymous-decoder/run.json'),'original_decoder_run_sha256':run['run_sha256'],'source_admission_and_PL_admin_only':drifts,'exact_parent_ids':parents})
closure=set()
def visit(path):
 if path in closure:return
 closure.add(path);paths.add(path)
 for name in re.findall(r'^import\s+((?:AutoSamplingTheory|Tests)\.[\w.]+)',Path(path).read_text(encoding='utf-8'),re.M):
  p=name.replace('.','/')+'.lean'
  if Path(p).exists():visit(p)
for p in proved['lean_files']:visit(p)
fake=[]
for p in sorted(closure):
 clean=astis.strip_lean_comments_and_strings(Path(p).read_text(encoding='utf-8'))
 for i,line in enumerate(clean.splitlines(),1):
  if astis.FORBIDDEN_REGEX.search(line):fake.append({'path':p,'line':i,'text':line.strip()})
assert not fake and not astis.forbidden_pattern_hits()
checks.append({'name':'fresh_reachable_and_canonical_fake_scan','reachable_modules':len(closure),'reachable_hits':fake,'canonical_files':len(astis.lean_source_files()),'canonical_hits':[],'reachable_inputs':[desc(p) for p in sorted(closure)]})
paths.update(p for p in subprocess.check_output(['git','ls-tree','-r','--name-only',C,'--',R.as_posix()],text=True).splitlines())
tracked=set(subprocess.check_output(['git','ls-tree','-r','--name-only',C],text=True).splitlines());selected=sorted(paths & tracked)
proc=subprocess.Popen(['git','cat-file','--batch'],stdin=subprocess.PIPE,stdout=subprocess.PIPE);out,_=proc.communicate(('\n'.join(C+':'+p for p in selected)+'\n').encode());assert proc.returncode==0
offset=0;gitrows=[]
for p in selected:
 stop=out.index(b'\n',offset);size=int(out[offset:stop].split()[-1]);offset=stop+1;blob=out[offset:offset+size];offset+=size+1;live=Path(p).read_bytes()
 immutable=p.startswith(R.as_posix()+'/') or '.snapshot.' in p or '.raw.snapshot' in p
 if immutable:assert blob==live,(p,'raw Git')
 else:assert blob.replace(b'\r\n',b'\n')==live.replace(b'\r\n',b'\n'),(p,'LF Git')
 gitrows.append({**desc(p),'git_blob_sha256':sha(blob),'mode':'raw-exact' if immutable else 'LF-exact'})
checks.append({'name':'exact_Git_raw_LF_inputs','checked_commit':C,'count':len(gitrows),'inputs':gitrows})
assert Path('lean-toolchain').read_text().strip()=='leanprover/lean4:v4.33.0'
assert next(x for x in j('lake-manifest.json')['packages'] if x['name']=='mathlib')['rev']=='db584cd6d46c92f209a44c0f1c829460d327499d'
gates=j(R/'reviewer.exact.gate-driver-reconciled.json');assert gates['checked_commit']==C and len(gates['results'])==7 and all(x['returncode']==0 for x in gates['results'])
for row in gates['results']:assert desc(row['path'])['raw_sha256']==row['raw_sha256']
log=(R/'reviewer.exact.focused.log').read_text(encoding='utf-8');axioms=[]
for name,vals in re.findall(r"'([^']+)' depends on axioms: \[([^\]]+)\]",log,re.S):
 values={x.strip() for x in vals.split(',')};assert values=={'propext','Classical.choice','Quot.sound'};axioms.append({'declaration':name,'axioms':sorted(values)})
assert len(axioms)==3 and '3759 jobs' in log
aggregate=(R/'reviewer.exact.aggregate.log').read_text(encoding='utf-8');assert '9137 jobs' in aggregate and '9404 jobs' in aggregate and 'ASTIS check passed' in aggregate
assert 'import Tests.StandardizedRGORelativeEntropy' not in Path('Tests.lean').read_text()
assert advance.current_advances()[A]['state']=='PROVED_LOCAL'
report={'schema_version':1,'artifact_kind':'independent-exact-commit-checks','verification_status':'passed-scoped','verified_commit':C,'verifier_id':V,'advance_id':A,'checks':checks,'gates':gates,'axioms':axioms,'focused_jobs':3759,'existing_aggregate_jobs':[9137,9404],'new33_shared_imports_present':False,'boundary':'Only genuine same-p standardized true RGO canonical finite KL, AE llr=logq, actual llr/rho L1 and both entropy identities plus derived unique stationary prox, for all positive eta and E0. No LSI/T2/Sobolev/FisherRN/W2/bias/fullLemma/main/work/composition. Focused current production/Test compiled, existing32 root imports aggregate preserved; no33sharedintegration credit.','compiler':'CLOSED','read_write':'OPEN pending permitted authoritative VERIFIED','completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
dest=R/'reviewer.exact.checks.json';dest.write_bytes((json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps({'status':'passed-scoped','verified_commit':C,'receipt':desc(dest),'Git_inputs':len(gitrows),'source_inputs':len(review['input_artifacts']),'closure_modules':len(closure),'canonical_fake_files':len(astis.lean_source_files()),'standard_axiom_targets':len(axioms)}))
