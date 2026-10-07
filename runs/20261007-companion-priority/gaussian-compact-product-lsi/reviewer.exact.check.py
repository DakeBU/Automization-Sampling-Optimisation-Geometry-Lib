exec(open('runs/20261007-companion-priority/gaussian-compact-product-lsi/reviewer.exact.gate.py',encoding='utf-8').read().split('assert subprocess.check_output')[0])
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
freeze=j(R/'math-freeze.json');math=j(R/'whole-proof-review/math.review.json');assert len(freeze['inputs'])==44
assert math['verification_status']=='passed-scoped' and not math['blockers'] and math['all_private_providers_reviewed']==8
assert d(R/'whole-proof-review/math.review.json')['raw_sha256']=='8bd0b155317e44d6cbcb5edb78d231fb683b904191d3bef1cba40bcf77323dc0'
pin(math['input_bindings']);mb=j(math['input_bindings']['path']);assert len(mb['inputs'])==51
for row in freeze['inputs']:pin(row)
for row in mb['inputs']:
 pin(row['original']);pin(row['snapshot']);assert Path(row['original']['path']).read_bytes()==Path(row['snapshot']['path']).read_bytes()
for key in ['actual_parent_API_review','reachability_fake_closure']:pin(math[key])
for row in math['fresh_compiler_evidence']:pin(row['log']);pin(row['status'])
pin(math['meaningful_stress']['source'])
sig=Path(freeze['inputs'][12]['path']).read_bytes();assert len(sig)==678 and sha(sig)=='fc859f057a9242675d2a769fa3b2dbbd7b66764fdbe429f608decf0018511d50'
assert sig.rstrip()+b' := by' in Path(freeze['inputs'][0]['path']).read_bytes().replace(b'\r\n',b'\n')
plan=j(R/'publication-plan.json');local=j(R/'proved-local.json');decls=plan['mathematical_declarations'];assert decls==local['lean_declarations']==local['publication_declarations'] and local['result_kind']=='theorem-edge'
data=pub.inputs();item=next(z for z in pub.load() if z['id']==plan['slugs'][0]);binding=next(z for z in item['bindings'] if z['declaration']==decls[0]);audit=data['audits'][plan['audit_ids'][0]]
s=j(R/'source.0.review.json');p=j(R/'source.0.reviewer-packet.json');dec=j(R/'anonymous-decoder/contract-adapter-run.json');orig=j(R/'anonymous-decoder/run.json');result=j(R/'anonymous-decoder/result0.contract.json');raw_result=j(R/'anonymous-decoder/result0.json');dp=j(R/'anonymous-decoder/packet0.json')
assert pub.digest({k:v for k,v in s.items() if k!='review_run_sha256'})==s['review_run_sha256']
assert pub.digest({k:v for k,v in p.items() if k!='packet_sha256'})==p['packet_sha256']
assert s['verdict']=='equivalent-after-elaboration' and not s['blocking'] and s['deltas']==s['repairs']==s['source_excess']==[]
assert s['independent_from_decoder'] and s['independent_from_formalizer'] and s['reviewer']!=V
assert s['whole_module_raw_sha256']==d(freeze['inputs'][0]['path'])['raw_sha256'] and s['whole_module_LF_sha256']==d(freeze['inputs'][0]['path'])['lf_sha256']==s['whole_module_file_sha256']
assert 'eight reachable private providers' in s['whole_module_scope']
assert sha(p['source']['original_text'].encode())==s['source_text_sha256']==p['source']['text_sha256']
assert sha(p['lean']['statement'].encode())==s['lean_statement_sha256']==p['lean']['statement_sha256']
assert pub.binding_digest(item,binding,data)==s['publication_binding_sha256']==p['publication_binding_sha256']==audit['publication_binding_sha256']
assert pub.review_context(item,binding,data)==p['candidate_publication_context']==audit['publication_context']==s['review_context']
assert audit['state']=='accepted' and audit['source_review']['review_run_sha256']==s['review_run_sha256'] and audit['source_review']['reviewer_packet_sha256']==p['packet_sha256']
assert set(s['semantic_slots'])=={'objects','domains','quantifiers','assumptions','conclusion','scopes','constant_dependencies'}
assert all(not x for x in p['anti_anchoring'].values()) and s['exposure']['current_math_review_verdict_read']==False
assert dec['status']=='CLOSED' and not dec['source_text_visible'] and not dec['compiler_started']
assert pub.digest(dec['canonical_basis'])==dec['decoder_run_sha256']==s['decoder_run_sha256']
assert dec['canonical_basis']['independent_reconstruction']==dec['independent_reconstruction']=={k:result[k] for k in dec['independent_reconstruction']}
assert all(raw_result[k]==result[k] for k in ['reconstructed_theorem_text','objects','assumptions','ambient_space','measures','operators','conclusion','scope_boundary'])
assert sha(result['reconstructed_theorem_text'].encode())==s['reconstructed_text_sha256']==result['reconstructed_text_sha256']==orig['reconstructed_text_sha256']
assert pub.digest({k:v for k,v in dp.items() if k!='packet_sha256'})==dp['packet_sha256']==s['decoder_packet_sha256']
assert audit['reconstruction']['text']==result['reconstructed_theorem_text'] and audit['reconstruction']['decoder_run_sha256']==dec['decoder_run_sha256']
assert dec['decoder'] not in [V,s['reviewer']] and all(dec[k]=='CLOSED' for k in ['read_lease','write_lease','python_lease','compiler_lease'])
pin(dec['original_input_bindings']['packet'],R/'anonymous-decoder/packet0.json');pin(dec['original_input_bindings']['opening_lease'],R/'anonymous-decoder/initial-lease.raw.snapshot.json')
pin(s['primary_first_contract']);pin(s['checks']);pin(s['source_graph_reuse']|{'path':s['source_graph_reuse']['prior_independent_topology_receipt'],'raw_sha256':s['source_graph_reuse']['receipt_raw_sha256']})
assert all(x=='CLOSED' for k,x in s['closure'].items() if k.endswith('lease'))
pub.check_advance(decls,reviewed=True)
expected_audit={'/deltas','/semantic_slots','/source_review/evidence','/source_review/independent_from_decoder','/source_review/independent_from_formalizer','/source_review/review_run_sha256','/source_review/reviewer','/source_review/reviewer_packet_sha256','/source_review/run_artifact','/source_review/state','/state','/verdict'}
expected_cell={'/evidence/execution_boundary','/evidence/proof_review','/evidence/source_review','/status'}
admin=[];assert len(s['input_artifacts'])==108
for row in s['input_artifacts']:
 raw=R/row['raw_snapshot'];lf=R/row['lf_snapshot'];pin(row,raw);assert lf.read_bytes()==raw.read_bytes().replace(b'\r\n',b'\n')
 if d(row['path'])['raw_sha256']!=row['raw_sha256']:
  paths=diff(j(raw),j(row['path']));expected=expected_audit if '/audits/' in row['path'] else expected_cell
  assert set(paths)==expected,(row['path'],paths);admin.append(dict(path=row['path'],before=pin(row,raw),current=d(row['path']),admin_paths=paths))
 else:pin(row)
assert len(admin)==2
draft=j(R/'decoder-binding-before.0.raw.snapshot.audit.json');pre=j(R/'source-admission-before.0.raw.snapshot.audit.json');decoderpaths=diff(draft,pre)
assert set(decoderpaths)<= {'/state','/reconstruction','/publication_context','/publication_binding_sha256','/source_review/run_artifact','/source_review/evidence'},decoderpaths
assert Path(R/'source-admission-before.0.raw.snapshot.audit.json').read_bytes()==(R/s['input_artifacts'][0]['raw_snapshot']).read_bytes()
assert not astis.forbidden_pattern_hits();files=astis.lean_source_files();reach=j(math['reachability_fake_closure']['path'])
for row in reach['reachable_canonical_modules']:pin(row)
assert reach['all_eight_reachable'] and reach['private_count']==8 and not reach['production_imports_Tests']
for lp in [R/'anonymous-decoder/lease.json',R/'anonymous-decoder/adapter.lease.json',R/'source.review.lease.json',R/'whole-proof-review/lease.json']:assert j(lp)['status']=='CLOSED'
scope_dirs=[R.as_posix(),'runs/20261007-companion-priority/gaussian-compact-product-preproof','runs/20261007-companion-priority/gaussian-compact-product-preproof-review','runs/20261007-companion-priority/gaussian-compact-product-source-graph','runs/20261007-companion-priority/gaussian-compact-product-source-topology-review']
selected=set(subprocess.check_output(['git','ls-tree','-r','--name-only',C,'--',*scope_dirs],text=True).splitlines())|{x['original']['path'] for x in mb['inputs'] if not x['original']['path'].startswith('.lake/')}|{x['path'] for x in s['input_artifacts'] if not x['path'].startswith('.lake/')}|{x['path'] for x in reach['reachable_canonical_modules']}
pr=subprocess.Popen(['git','cat-file','--batch'],stdin=subprocess.PIPE,stdout=subprocess.PIPE);out,_=pr.communicate(('\n'.join(C+':'+v for v in sorted(selected))+'\n').encode());assert pr.returncode==0;offset=0;gitrows=[]
for v in sorted(selected):
 e=out.index(b'\n',offset);header=out[offset:e].split();assert header[-1]!=b'missing',v;n=int(header[-1]);offset=e+1;blob=out[offset:offset+n];offset+=n+1;live=Path(v).read_bytes()
 assert (blob==live if v.startswith('runs/') else blob.replace(b'\r\n',b'\n')==live.replace(b'\r\n',b'\n')),v
 gitrows.append(dict(d(v),git_blob_sha256=sha(blob),git_lf_sha256=sha(blob.replace(b'\r\n',b'\n')),raw_exact=blob==live))
g=j(R/'reviewer.exact.gates.json');assert g['checked_commit']==C and g['all_pass'] and len(g['results'])==8
for row in g['results']:assert row['returncode']==0;pin(row)
assert 'ASTIS check passed' in (R/'reviewer.exact.mandatory.log').read_text()
ax=re.findall(r"'([^']+)' depends on axioms: \[([^\]]+)\]",(R/'reviewer.exact.direct-axioms.log').read_text(),re.S)
assert len(ax)==5 and all(set(z.strip() for z in a.split(','))=={'propext','Classical.choice','Quot.sound'} for _,a in ax)
coverage=[]
for line in (R/'reviewer.exact.publication.log').read_text(encoding='utf-8').splitlines():
 if line.startswith('Private implementation coverage: '):
  row=json.loads(line[len('Private implementation coverage: '):])
  if row['file']==freeze['inputs'][0]['path']:coverage.append(row);assert row['owner']==decls[0]
assert len(coverage)==8
states=advance.current_advances();assert states[freeze['advance_id']]['state']=='PROVED_LOCAL' and states[freeze['advance_id']]['owner_id']!=V
assert [a for a,z in states.items() if z['state']=='STABILIZING']==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
rec=put(R/'reviewer.exact.admission-reconciliation.json',dict(verifier_id=V,checked_commit=C,math44_and_whole51_unchanged=True,source108_before_raw_LF_snapshots_preserved=True,source_administrative_changes=admin,decoder_binding_paths=decoderpaths,raw_to_contract_eight_strings_preserved=True,source_scope='Independent scoped authored compact C2 finite-Pi sufficient OR route; full external W12/Hilbert/noncompact/T2/FIRST/main not discharged.'))
x=dict(status='passed-scoped-exact-admission-ready',checked_commit=C,verifier_id=V,math_freeze_count=44,whole_math_inputs=51,whole_math_review=d(R/'whole-proof-review/math.review.json'),source_inputs=108,source_review=d(R/'source.0.review.json'),source_packet=d(R/'source.0.reviewer-packet.json'),source_review_run_sha256=s['review_run_sha256'],publication_binding_sha256=s['publication_binding_sha256'],decoder_run_sha256=dec['decoder_run_sha256'],source_admin_reconciliation=rec,exact_Git_inputs=gitrows,exact_Git_input_count=len(gitrows),gates=g,aggregate_jobs=re.findall(r'Build completed successfully \((\d+) jobs\)',(R/'reviewer.exact.mandatory.log').read_text()),named_standard_axioms=[dict(declaration=n,axioms=[z.strip() for z in a.split(',')]) for n,a in ax],fake_closure_scan=dict(status='PASS',canonical_files=len(files),hits=0,reachable_modules=reach['reachable_canonical_module_count'],private_providers=8,private_owner_coverage=coverage),remaining_boundary=['Compact C2 finite Pi variance1 function LSI with literal coordinate-square energy only; finite Hilbert law/Parseval, noncompact extensions, T2/FIRST4.6, paper mains/work/cost/composition remain open.','Shared40 imports/Registry/site, repository ProofSeal/full-reader/PURIFIED/remoteCI/live remain separate pending boundaries.'])
saved=put(R/'reviewer.exact.bindings.json',x)
print(json.dumps(dict(status=x['status'],bindings=saved,git_inputs=len(gitrows),aggregate_jobs=x['aggregate_jobs'],source_inputs=108,admin_changes=len(admin),canonical_fake_files=len(files),fake_hits=0),indent=2))
