from pathlib import Path
import json,hashlib,subprocess,sys,re,datetime
sys.path.insert(0,'tools')
import astis_publication as pub,astis_advance as advance,astis
R=Path('runs/20261007-companion-priority/gaussian-compact-entropy')
C='421496a5de7355830c0b4904ea10f33722ed3602';V='picard_commit_verifier_20261005'
def j(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
def d(p):
 b=Path(p).read_bytes();return {'path':Path(p).as_posix(),'raw_sha256':sha(b),'lf_sha256':sha(b.replace(b'\r\n',b'\n')),'bytes':len(b)}
def pin(row,p=None):
 x=d(p or row['path']);assert x['raw_sha256']==row['raw_sha256'],(x,row)
 if 'lf_sha256' in row:assert x['lf_sha256']==row['lf_sha256'],(x,row)
 if 'bytes' in row:assert x['bytes']==row['bytes'],(x,row)
 return x
def dif(a,b,p=''):
 if type(a)!=type(b):return [p]
 if isinstance(a,dict):return [q for k in sorted(a.keys()|b.keys()) for q in ([p+'/'+k] if k not in a or k not in b else dif(a[k],b[k],p+'/'+k))]
 if isinstance(a,list):return [p] if len(a)!=len(b) else [q for i,(x,y) in enumerate(zip(a,b)) for q in dif(x,y,p+'/'+str(i))]
 return [] if a==b else [p]
def ho(x,k):assert pub.digest({a:b for a,b in x.items() if a!=k})==x[k],k
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==C
assert subprocess.check_output(['git','-C','.lake/packages/mathlib','rev-parse','HEAD'],text=True).strip()=='db584cd6d46c92f209a44c0f1c829460d327499d'
assert Path('lean-toolchain').read_text().strip()=='leanprover/lean4:v4.33.0'
math=j(R/'whole-proof-review/math.review.json');assert d(R/'whole-proof-review/math.review.json')['raw_sha256']=='8f394ccd9ef7dde5353b851800fae9198cf3c649b5ded154303cdfb8c7939268'
assert math['verification_status']=='passed-scoped' and not math['blockers'] and math['all_private_providers_reviewed']==3
pin(math['input_bindings']);bindings=j(math['input_bindings']['path']);assert len(bindings['inputs'])==36 and bindings['original_frozen22_unchanged']
for row in bindings['inputs']:
 pin(row)
 if 'raw_snapshot' in row:
  pin(row,row['raw_snapshot']);assert Path(row['lf_snapshot']).read_bytes()==Path(row['path']).read_bytes().replace(b'\r\n',b'\n')
freeze=j(R/'math-freeze.json');assert len(freeze['inputs'])==22
for row in freeze['inputs']:pin(row)
mr=j(R/'whole-proof-review/run.json');assert pub.digest({k:v for k,v in mr.items() if k not in {'deterministic_run_sha256','status','hash_recipe'}})==mr['deterministic_run_sha256']
assert mr['status']=='CLOSED'
api=j(math['actual_parent_API_review']['path']);pin(math['actual_parent_API_review'])
for row in api['regions']:
 pin(row['source_file']);pin(row['snapshot']);lo,hi=row['lines'];assert b''.join(Path(row['path']).read_bytes().splitlines(keepends=True)[lo-1:hi])==Path(row['snapshot']['path']).read_bytes()
signature=(R/'preproof/signature.prospective.txt').read_bytes();assert len(signature)==1581 and sha(signature)=='d0adc2bfa9a83b8389706c10b31d10c64b5f7b6dba8c7454cd370a738ac7100e'
module=Path(freeze['inputs'][0]['path']).read_bytes().replace(b'\r\n',b'\n');assert signature.rstrip()+b' := by' in module
plan=j(R/'publication-plan.json');decls=plan['mathematical_declarations'];local=j(R/'proved-local.json');assert decls==local['lean_declarations']==local['publication_declarations'] and len(decls)==1
data=pub.inputs();item=next(x for x in pub.load() if x['id']==plan['slugs'][0]);b=next(x for x in item['bindings'] if x['declaration']==decls[0]);audit=data['audits'][plan['audit_ids'][0]]
source=j(R/'source.0.review.json');packet=j(R/'source.0.reviewer-packet.json');ho(source,'review_run_sha256');ho(packet,'packet_sha256')
assert d(R/'source.0.review.json')['raw_sha256']=='291bb8d8f9558f7ecc0dd9575f0fa231e974b6e202e4acd805260eeca684fec7'
assert source['reviewer']!=V and source['independent_from_formalizer'] and source['independent_from_decoder'] and source['verdict']=='equivalent-after-elaboration' and not source['blocking'] and source['deltas']==source['repairs']==[]
assert set(source['semantic_slots'])=={'objects','domains','quantifiers','assumptions','conclusion','scopes','constant_dependencies'}
assert pub.binding_digest(item,b,data)==source['publication_binding_sha256']==packet['publication_binding_sha256']==audit['publication_binding_sha256']
assert pub.review_context(item,b,data)==packet['candidate_publication_context']
assert audit['state']=='accepted' and audit['source_review']['review_run_sha256']==source['review_run_sha256'] and audit['source_review']['reviewer_packet_sha256']==packet['packet_sha256']
assert source['whole_module_reviewed'] and source['whole_module_raw_sha256']==d(freeze['inputs'][0]['path'])['raw_sha256'] and source['whole_module_lf_sha256']==d(freeze['inputs'][0]['path'])['lf_sha256']
pub.check_advance(decls,reviewed=True)
drifts=[];assert len(source['input_artifacts'])==88
for row in source['input_artifacts']:
 pin(row,row['raw_snapshot']);assert Path(row['lf_snapshot']).read_bytes()==Path(row['raw_snapshot']).read_bytes().replace(b'\r\n',b'\n')
 if d(row['path'])['raw_sha256']!=row['raw_sha256']:
  changes=dif(j(row['raw_snapshot']),j(row['path']))
  assert '/audits/' in row['path'] or '/frontier-cells/' in row['path'],(row['path'],changes)
  allowed={'/state','/source_review/state','/source_review/reviewer','/source_review/independent_from_formalizer','/source_review/independent_from_decoder','/source_review/evidence','/source_review/run_artifact','/source_review/review_run_sha256','/source_review/reviewer_packet_sha256','/semantic_slots','/deltas','/verdict'}
  if '/frontier-cells/' in row['path']:
   allowed={'/status','/evidence/proof_review','/evidence/source_review','/evidence/execution_boundary'}
   assert j(row['raw_snapshot'])['status']=='claimed' and j(row['path'])['status']=='proved_locally'
  assert set(changes)<=allowed,changes
  drifts.append({'path':row['path'],'before':pin(row,row['raw_snapshot']),'current':d(row['path']),'exact_admin_pointers':changes})
 else:pin(row)
assert len(drifts)==2
before=j(R/'source-admission-before.0.raw.snapshot.audit.json');assert before==j(source['input_artifacts'][0]['raw_snapshot'])
dec=j(R/'anonymous-decoder/run.json');assert pub.digest(dec['canonical_basis'])==dec['decoder_run_sha256']==source['decoder_run_sha256']
assert dec['status']=='CLOSED' and not dec['source_text_visible'] and not dec['compiler_started']
dp=j(R/'anonymous-decoder/packet0.json');ho(dp,'packet_sha256');assert dp['packet_sha256']==source['decoder_packet_sha256']
result=j(R/'anonymous-decoder/result0.json');assert sha(result['reconstructed_theorem_text'].encode())==result['reconstructed_text_sha256']==source['reconstruction_text_sha256']
assert set(result)-set(dec['canonical_basis']['reconstruction'])=={'decoder_run_sha256'}
assert dec['canonical_basis']['reconstruction']=={k:v for k,v in result.items() if k!='decoder_run_sha256'}
assert result['decoder_run_sha256']==dec['decoder_run_sha256']
assert audit['reconstruction']['text']==result['reconstructed_theorem_text'] and audit['reconstruction']['decoder_run_sha256']==dec['decoder_run_sha256']
assert j(R/'anonymous-decoder/initial-lease.raw.snapshot.json')==dec['canonical_basis']['initial_lease']
for name in ['lease.json']:
 dl=j(R/'anonymous-decoder'/name);assert dl['status']=='CLOSED'
sl=j(R/'source.review.lease.json');assert sl['read_lease']==sl['write_lease']==sl['compiler_lease']=='CLOSED'
closed=j(R/'source.review.run.closed.json');pin(closed['result']);pin(closed['checks']);pin(closed['lease'])
assert not astis.forbidden_pattern_hits()
files=astis.lean_source_files();closure=[freeze['inputs'][0]['path'],freeze['inputs'][1]['path'],'AutoSamplingTheory/TechnicalLemmas/Probability/BalancedRademacherCLT.lean']
for p in closure:assert not astis.FORBIDDEN_REGEX.search(astis.strip_lean_comments_and_strings(Path(p).read_text(encoding='utf-8')))
assert 'import Tests' not in Path(closure[0]).read_text()
selected=set(subprocess.check_output(['git','ls-tree','-r','--name-only',C,'--',R.as_posix()],text=True).splitlines())
selected|={row['path'] for row in bindings['inputs'] if not row['path'].startswith('.lake/')}
selected|={row['path'] for row in source['input_artifacts'] if not row['path'].startswith('.lake/')}
selected|={row['raw_snapshot'] for row in source['input_artifacts']}|{row['lf_snapshot'] for row in source['input_artifacts']}
selected=sorted(selected)
q=subprocess.Popen(['git','cat-file','--batch'],stdin=subprocess.PIPE,stdout=subprocess.PIPE);out,_=q.communicate(('\n'.join(C+':'+p for p in selected)+'\n').encode());assert q.returncode==0
offset=0;gitrows=[]
for p in selected:
 e=out.index(b'\n',offset);h=out[offset:e].split();assert h[-1]!=b'missing',(p,h)
 n=int(h[-1]);offset=e+1;blob=out[offset:offset+n];offset+=n+1;live=Path(p).read_bytes()
 assert (blob==live if p.startswith('runs/') else blob.replace(b'\r\n',b'\n')==live.replace(b'\r\n',b'\n')),p
 gitrows.append(dict(d(p),git_blob_sha256=sha(blob),git_lf_sha256=sha(blob.replace(b'\r\n',b'\n')),raw_exact=blob==live))
gates=j(R/'reviewer.exact.gates.json');assert len(gates['results'])==8 and gates['checked_commit']==C
for row in gates['results']:assert row['returncode']==0;pin(row)
assert 'ASTIS check passed' in (R/'reviewer.exact.aggregate.log').read_text(encoding='utf-8')
ax=re.findall(r"'([^']+)' depends on axioms: \[([^\]]+)\]",(R/'reviewer.exact.direct-axioms.log').read_text(encoding='utf-8'),re.S)
assert len(ax)==3 and all(set(t.strip() for t in a.split(','))=={'propext','Classical.choice','Quot.sound'} for _,a in ax)
jobs=re.findall(r'Build completed successfully \((\d+) jobs\)',(R/'reviewer.exact.aggregate.log').read_text(encoding='utf-8'))
A=j(R/'claim.json')['advance_id'];state=advance.current_advances()[A];assert state['state']=='PROVED_LOCAL' and state['owner_id']!=V
receipt={'status':'passed-scoped-exact-admission-ready','checked_commit':C,'verifier_id':V,'whole_math_review':d(R/'whole-proof-review/math.review.json'),'whole_math_run_sha256':mr['deterministic_run_sha256'],'math_binding_count':36,'original_frozen_inputs':22,'parent_API_regions':len(api['regions']),'source_review':d(R/'source.0.review.json'),'source_packet':d(R/'source.0.reviewer-packet.json'),'source_review_run_sha256':source['review_run_sha256'],'source_input_count':88,'source_admin_reconciliation':drifts,'source_binding_sha256':source['publication_binding_sha256'],'decoder_run_sha256':dec['decoder_run_sha256'],'decoder_packet_sha256':dp['packet_sha256'],'current_publication_reviewed_true':True,'exact_currentGit_inputs':gitrows,'exact_currentGit_input_count':len(gitrows),'fresh_gates':gates,'aggregate_jobs':jobs,'named_standard_axioms':[{'declaration':n,'axioms':[x.strip() for x in a.split(',')]} for n,a in ax],'fake_closure_scan':{'status':'PASS','canonical_files':len(files),'hits':0,'reachable_files':closure,'production_Tests_imports':False},'source_scope':'Authored compact real C2 entropy/derivative observer limits; actual35 only ASTIS proof parent. No Bernoulli direct-parent claim.','remaining_boundary':['Full flip-energy factor4 is open.','Gaussian LSI, noncompact domain extension, Hilbert LSI/T2/FIRST4.6, both papers main results/composition/query cost remain open.','Shared imports/Registry/site/current repository ProofSeal/Exposition/PURIFIED/remoteCI/main merge/live remain pending.'],'leases':{'compiler':'CLOSED','read':'OPEN until independent transition','write':'OPEN task receipts/VERIFIED only'}}
Path(R/'reviewer.exact.bindings.json').write_bytes((json.dumps(receipt,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps({'status':receipt['status'],'git_inputs':len(gitrows),'source_inputs':88,'admin':drifts,'jobs':jobs},ensure_ascii=False))
