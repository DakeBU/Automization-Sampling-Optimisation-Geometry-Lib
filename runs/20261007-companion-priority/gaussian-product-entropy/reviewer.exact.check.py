exec(open('runs/20261007-companion-priority/gaussian-product-entropy/reviewer.exact.gate.py',encoding='utf-8').read().split('assert subprocess.check_output')[0])
import sys,re
sys.path.insert(0,'tools')
import astis,astis_publication as pub,astis_advance as advance
def pin(row,p=None):
 x=d(p or row['path']);assert x['raw_sha256']==row['raw_sha256'],(x,row)
 if 'lf_sha256' in row:assert x['lf_sha256']==row['lf_sha256'],(x,row)
 return x
def diff(a,b,k=''):
 if type(a)!=type(b):return [k]
 if isinstance(a,dict):return [z for key in sorted(a.keys()|b.keys()) for z in ([k+'/'+key] if key not in a or key not in b else diff(a[key],b[key],k+'/'+key))]
 if isinstance(a,list):return [k] if len(a)!=len(b) else [z for i,(x,y) in enumerate(zip(a,b)) for z in diff(x,y,k+'/'+str(i))]
 return [] if a==b else [k]
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==C
assert subprocess.check_output(['git','-C','.lake/packages/mathlib','rev-parse','HEAD'],text=True).strip()=='db584cd6d46c92f209a44c0f1c829460d327499d'
assert Path('lean-toolchain').read_text().strip()=='leanprover/lean4:v4.33.0'
freeze=j(R/'math-freeze.json');math=j(R/'whole-proof-review/math.review.json')
assert len(freeze['inputs'])==26 and math['verification_status']=='passed-scoped' and not math['blockers'] and math['all_private_providers_reviewed']==15
assert d(R/'whole-proof-review/math.review.json')['raw_sha256']=='1ddb34bcb6771d3f9c19af40fd0414962e5f0081d6cbdf62796ae7ac7ea4b638'
pin(math['input_bindings']);mb=j(math['input_bindings']['path']);assert len(mb['inputs'])==31
for row in freeze['inputs']+mb['inputs']:pin(row)
for row in mb['inputs']:
 pin(row,row['raw_snapshot']);assert Path(row['lf_snapshot']).read_bytes()==Path(row['path']).read_bytes().replace(b'\r\n',b'\n')
for x in ['actual_parent_API_review','reachability_fake_closure']:pin(math[x])
for row in math['fresh_compiler_evidence']:pin(row['log']);pin(row['status'])
pin(math['meaningful_zero_mass_stress']['evidence']['log']);pin(math['meaningful_zero_mass_stress']['evidence']['stdin_source']);pin(math['meaningful_zero_mass_stress']['diagnosis'])
sig=Path(freeze['inputs'][8]['path']).read_bytes();assert len(sig)==1029 and sha(sig)=='4c3634612a055d16e4aec0516823192db42307ac1330ae4bddb88b959a436b0d' and sig.rstrip()+b' := by' in Path(freeze['inputs'][0]['path']).read_bytes()
plan=j(R/'publication-plan.json');local=j(R/'proved-local.json');decls=plan['mathematical_declarations'];assert decls==local['lean_declarations']==local['publication_declarations']
data=pub.inputs();item=next(z for z in pub.load() if z['id']==plan['slugs'][0]);binding=next(z for z in item['bindings'] if z['declaration']==decls[0]);audit=data['audits'][plan['audit_ids'][0]]
s=j(R/'source.0.review.json');p=j(R/'source.0.reviewer-packet.json');dec=j(R/'anonymous-decoder/run.json');result=j(R/'anonymous-decoder/result0.json');dp=j(R/'anonymous-decoder/packet0.json')
assert pub.digest({k:v for k,v in s.items() if k!='review_run_sha256'})==s['review_run_sha256']
assert pub.digest({k:v for k,v in p.items() if k!='packet_sha256'})==p['packet_sha256']
assert s['verdict']=='equivalent-after-elaboration' and not s['blocking'] and s['deltas']==s['repairs']==s['source_excess']==[]
assert s['independent_from_decoder'] and s['independent_from_formalizer'] and s['reviewer']!=V
assert s['whole_module_covered'] and s['whole_module_proof_and_private_helpers_covered'] and s['whole_module_file_sha256']==d(freeze['inputs'][0]['path'])['raw_sha256'] and s['whole_module_lf_sha256']==d(freeze['inputs'][0]['path'])['lf_sha256']
assert sha(p['source']['original_text'].encode())==s['source_text_sha256']==p['source']['text_sha256']
assert sha(p['lean']['statement'].encode())==s['lean_statement_sha256']==p['lean']['statement_sha256']
assert pub.binding_digest(item,binding,data)==s['publication_binding_sha256']==p['publication_binding_sha256']==audit['publication_binding_sha256']
assert pub.review_context(item,binding,data)==p['candidate_publication_context']==audit['publication_context']
assert audit['state']=='accepted' and audit['source_review']['review_run_sha256']==s['review_run_sha256'] and audit['source_review']['reviewer_packet_sha256']==p['packet_sha256']
assert set(s['semantic_slots'])=={'objects','domains','quantifiers','assumptions','conclusion','scopes','constant_dependencies'}
assert dec['status']=='CLOSED' and not dec['source_text_visible'] and not dec['compiler_started'] and pub.digest(dec['canonical_basis'])==dec['decoder_run_sha256']==s['decoder_run_sha256']
assert {k:v for k,v in result.items() if k!='decoder_run_sha256'}==dec['canonical_basis']['reconstruction']
assert sha(result['reconstructed_theorem_text'].encode())==s['reconstructed_text_sha256']==result['reconstructed_text_sha256']
assert pub.digest({k:v for k,v in dp.items() if k!='packet_sha256'})==dp['packet_sha256']==s['decoder_packet_sha256']
assert j(R/'anonymous.0.decoder.json')==dp
assert audit['reconstruction']['text']==result['reconstructed_theorem_text'] and audit['reconstruction']['decoder_run_sha256']==dec['decoder_run_sha256']
pub.check_advance(decls,reviewed=True)
expected_audit={'/deltas','/semantic_slots','/source_review/evidence','/source_review/independent_from_decoder','/source_review/independent_from_formalizer','/source_review/review_run_sha256','/source_review/reviewer','/source_review/reviewer_packet_sha256','/source_review/run_artifact','/source_review/state','/state','/verdict'}
expected_cell={'/evidence/execution_boundary','/evidence/proof_review','/evidence/source_review','/status'}
admin=[];assert len(s['input_artifacts'])==95
for row in s['input_artifacts']:
 pin(row,row['raw_snapshot'])
 if d(row['path'])['raw_sha256']!=row['raw_sha256']:
  paths=diff(j(row['raw_snapshot']),j(row['path']));expected=expected_audit if '/audits/' in row['path'] else expected_cell
  assert set(paths)==expected,(row['path'],paths)
  admin.append(dict(path=row['path'],before=pin(row,row['raw_snapshot']),current=d(row['path']),admin_paths=paths))
 else:pin(row)
assert len(admin)==2
for row in s['supplemental_input_artifacts']:pin(row);pin(row,row['raw_snapshot'])
assert Path(R/'source-admission-before.0.raw.snapshot.audit.json').read_bytes()==Path(s['input_artifacts'][0]['raw_snapshot']).read_bytes()
draft=j(R/'decoder-binding-before.0.raw.snapshot.audit.json');preaccepted=j(R/'source-admission-before.0.raw.snapshot.audit.json')
decoderpaths=diff(draft,preaccepted)
assert set(decoderpaths)<= {'/state','/reconstruction','/publication_context','/publication_binding_sha256','/source_review/run_artifact','/source_review/evidence'},decoderpaths
for lp in [R/'anonymous-decoder/lease.json',R/'source.review.lease.json',R/'whole-proof-review/lease.json']:assert j(lp)['status']=='CLOSED'
assert all(s[k]=='CLOSED' for k in ['read_lease','write_lease','compiler_lease','Python_lease'])
sync=j(R/'upstream-sync.json');merge=sync['merge_commit'];up=sync['upstream_commit']
assert subprocess.check_output(['git','rev-list','--parents','-n','1',merge],text=True).strip().split()==[merge]+sync['parents']
upfiles=subprocess.check_output(['git','diff','--name-only',sync['parents'][0],merge],text=True).splitlines();assert sorted(upfiles)==sorted(x['path'] for x in sync['upstream_files'])
for row in sync['upstream_files']:pin(row)
assert subprocess.check_output(['git','merge-base','--is-ancestor',merge,C]).decode()==''
assert subprocess.check_output(['git','rev-parse','origin/main'],text=True).strip()==up
assert not astis.forbidden_pattern_hits();files=astis.lean_source_files()
closure=[freeze['inputs'][0]['path'],freeze['inputs'][1]['path'],'AutoSamplingTheory/TechnicalLemmas/Analysis/Calculculus/Cutoff.lean']
closure[2]='AutoSamplingTheory/TechnicalLemmas/Analysis/Calculus/Cutoff.lean'
for path in closure:assert not astis.FORBIDDEN_REGEX.search(astis.strip_lean_comments_and_strings(Path(path).read_text(encoding='utf-8')))
assert 'import Tests' not in Path(closure[0]).read_text()
scope_dirs=[R.as_posix(),R.as_posix()+'-preproof',R.as_posix()+'-preproof-review',R.as_posix()+'-preread',R.as_posix()+'-source-graph',R.as_posix()+'-source-graph-review']
selected=set(subprocess.check_output(['git','ls-tree','-r','--name-only',C,'--',*scope_dirs],text=True).splitlines())|{x['path'] for x in mb['inputs']+s['input_artifacts']+s['supplemental_input_artifacts']+sync['upstream_files'] if not x['path'].startswith('.lake/')}
gitrows=[];pr=subprocess.Popen(['git','cat-file','--batch'],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
out,_=pr.communicate(('\n'.join(C+':'+v for v in sorted(selected))+'\n').encode());assert pr.returncode==0;offset=0
for v in sorted(selected):
 e=out.index(b'\n',offset);header=out[offset:e].split();assert header[-1]!=b'missing',v;n=int(header[-1]);offset=e+1;blob=out[offset:offset+n];offset+=n+1;live=Path(v).read_bytes()
 assert (blob==live if v.startswith('runs/') else blob.replace(b'\r\n',b'\n')==live.replace(b'\r\n',b'\n')),v
 gitrows.append(dict(d(v),git_blob_sha256=sha(blob),git_lf_sha256=sha(blob.replace(b'\r\n',b'\n')),raw_exact=blob==live))
g=j(R/'reviewer.exact.gates.json');assert g['checked_commit']==C and g['all_pass'] and len(g['results'])==8
for row in g['results']:assert row['returncode']==0;pin(row)
assert 'ASTIS check passed' in (R/'reviewer.exact.mandatory.log').read_text()
ax=re.findall(r"'([^']+)' depends on axioms: \[([^\]]+)\]",(R/'reviewer.exact.direct-axioms.log').read_text(),re.S)
assert len(ax)==3 and all(set(z.strip() for z in a.split(','))=={'propext','Classical.choice','Quot.sound'} for _,a in ax)
private_coverage=[]
for line in (R/'reviewer.exact.publication.log').read_text(encoding='utf-8').splitlines():
 if line.startswith('Private implementation coverage: '):
  row=json.loads(line[len('Private implementation coverage: '):])
  if row['file']==closure[0]:private_coverage.append(row);assert row['owner']==decls[0]
assert len(private_coverage)==15
assert advance.current_advances()[freeze['advance_id']]['state']=='PROVED_LOCAL'
reconciliation=put(R/'reviewer.exact.admission-reconciliation.json',dict(verifier_id=V,checked_commit=C,source_administrative_changes=admin,decoder_binding_paths=decoderpaths,source_and_decoder_raw_snapshots_preserved=True,math26_and_whole31_unchanged=True,upstream_merge=sync,source_scope='Bounded heterogeneous binary background, independent authored sufficient route; no full unbounded finite tensorization/LSI claim.'))
x=dict(status='passed-scoped-exact-admission-ready',checked_commit=C,verifier_id=V,math_freeze_count=26,whole_math_inputs=31,whole_math_review=d(R/'whole-proof-review/math.review.json'),source_inputs=95,source_supplemental_inputs=6,source_review=d(R/'source.0.review.json'),source_packet=d(R/'source.0.reviewer-packet.json'),source_review_run_sha256=s['review_run_sha256'],publication_binding_sha256=s['publication_binding_sha256'],decoder_run_sha256=dec['decoder_run_sha256'],source_admin_reconciliation=reconciliation,exact_Git_inputs=gitrows,exact_Git_input_count=len(gitrows),gates=g,aggregate_jobs=re.findall(r'Build completed successfully \((\d+) jobs\)',(R/'reviewer.exact.mandatory.log').read_text()),named_standard_axioms=[dict(declaration=n,axioms=[z.strip() for z in a.split(',')]) for n,a in ax],fake_closure_scan=dict(status='PASS',canonical_files=len(files),hits=0,reachable_files=closure,production_Test_imports=False,private_providers=15,private_owner_coverage=private_coverage),remaining_boundary=['Bounded binary product entropy only; unbounded/finite-coordinate tensorization, finite/Hilbert/noncompact GaussianLSI, T2/FIRST4.6, paper mains/cost/composition remain open.','Shared39 imports/Registry/site, repository ProofSeal/static-reader delivery/PURIFIED/remote CI/live are separate pending boundaries.'])
saved=put(R/'reviewer.exact.bindings.json',x)
print(json.dumps(dict(status=x['status'],bindings=saved,git_inputs=len(gitrows),aggregate_jobs=x['aggregate_jobs'],source_inputs=95,admin_changes=len(admin),canonical_fake_files=len(files),fake_hits=0),indent=2))
