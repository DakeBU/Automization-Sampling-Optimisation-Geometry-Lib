exec(open('runs/20261007-companion-priority/gaussian-flip-energy/reviewer.exact.check.py',encoding='utf-8').read().split('assert subprocess.check_output')[0])
R=Path('runs/20261007-companion-priority/gaussian-compact-lsi');C='d8cbf270a3627d99971023d783c785d0585be18a'
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==C
assert subprocess.check_output(['git','-C','.lake/packages/mathlib','rev-parse','HEAD'],text=True).strip()=='db584cd6d46c92f209a44c0f1c829460d327499d'
assert Path('lean-toolchain').read_text().strip()=='leanprover/lean4:v4.33.0'
freeze=j(R/'math-freeze.json');math=j(R/'whole-proof-review/math.review.json');assert len(freeze['inputs'])==22 and math['verification_status']=='passed-scoped' and math['all_private_providers_reviewed']==0 and not math['blockers']
assert d(R/'whole-proof-review/math.review.json')['raw_sha256']=='d3689ebc99a535aa3c1f875a4b8815da84ac3a7b50c5116b2298f357cbe513ac'
pin(math['input_bindings']);mb=j(math['input_bindings']['path']);assert len(mb['inputs'])==34
for row in freeze['inputs']+mb['inputs']:pin(row)
for row in mb['inputs']:
 if 'raw_snapshot' in row:
  pin(row,row['raw_snapshot']);assert Path(row['lf_snapshot']).read_bytes()==Path(row['path']).read_bytes().replace(b'\r\n',b'\n')
sig=(R/'preproof/signature.prospective.txt').read_bytes();assert len(sig)==308 and sha(sig)=='cf52aef70523e2e4f95eb9ccefc2ea661ddb6ed1e0400bc8f02473c282ee0e63' and sig.rstrip()+b' := by' in Path(freeze['inputs'][0]['path']).read_bytes()
plan=j(R/'publication-plan.json');local=j(R/'proved-local.json');decls=plan['mathematical_declarations'];assert decls==local['lean_declarations']==local['publication_declarations']
data=pub.inputs();item=next(z for z in pub.load() if z['id']==plan['slugs'][0]);b=next(z for z in item['bindings'] if z['declaration']==decls[0]);audit=data['audits'][plan['audit_ids'][0]]
s=j(R/'source.0.review.json');p=j(R/'source.0.reviewer-packet.json');dec=j(R/'anonymous-decoder/run.json');result=j(R/'anonymous-decoder/result0.json');dp=j(R/'anonymous-decoder/packet0.json')
assert pub.digest({k:v for k,v in s.items() if k!='review_run_sha256'})==s['review_run_sha256'] and pub.digest({k:v for k,v in p.items() if k!='packet_sha256'})==p['packet_sha256']
assert s['verdict']=='equivalent-after-elaboration' and not s['blocking'] and s['deltas']==s['repairs']==s['source_excess']==[] and s['independent_from_decoder'] and s['independent_from_formalizer'] and s['reviewer']!=V
assert s['whole_module_covered'] and s['whole_module_file_sha256']==d(freeze['inputs'][0]['path'])['raw_sha256'] and s['whole_module_file_lf_sha256']==d(freeze['inputs'][0]['path'])['lf_sha256']
assert sha(p['source']['original_text'].encode())==s['source_text_sha256']==p['source']['text_sha256'] and sha(p['lean']['statement'].encode())==s['lean_statement_sha256']==p['lean']['statement_sha256']
assert pub.binding_digest(item,b,data)==s['publication_binding_sha256']==p['publication_binding_sha256']==audit['publication_binding_sha256'] and pub.review_context(item,b,data)==p['candidate_publication_context']==audit['publication_context']
assert audit['state']=='accepted' and audit['source_review']['review_run_sha256']==s['review_run_sha256'] and audit['source_review']['reviewer_packet_sha256']==p['packet_sha256']
assert set(s['semantic_slots'])=={'objects','domains','quantifiers','assumptions','conclusion','scopes','constant_dependencies'}
assert dec['status']=='CLOSED' and not dec['source_text_visible'] and not dec['compiler_started'] and pub.digest(dec['canonical_basis'])==dec['decoder_run_sha256']==s['decoder_run_sha256']
assert {k:v for k,v in result.items() if k!='decoder_run_sha256'}==dec['canonical_basis']['reconstruction'] and sha(result['reconstructed_theorem_text'].encode())==s['reconstructed_text_sha256']==result['reconstructed_text_sha256']
assert pub.digest({k:v for k,v in dp.items() if k!='packet_sha256'})==dp['packet_sha256']==s['decoder_packet_sha256']
assert audit['reconstruction']['text']==result['reconstructed_theorem_text'] and audit['reconstruction']['decoder_run_sha256']==dec['decoder_run_sha256']
pub.check_advance(decls,reviewed=True)
expected={0:{'/deltas','/semantic_slots','/source_review/evidence','/source_review/independent_from_decoder','/source_review/independent_from_formalizer','/source_review/review_run_sha256','/source_review/reviewer','/source_review/reviewer_packet_sha256','/source_review/run_artifact','/source_review/state','/state','/verdict'},31:{'/evidence/execution_boundary','/evidence/proof_review','/evidence/source_review','/status'}};admin=[]
assert len(s['input_artifacts'])==67
for i,row in enumerate(s['input_artifacts']):
 snap=R/f'source.review.input.{i:02d}.raw.snapshot';pin(row,snap)
 if d(row['path'])['raw_sha256']!=row['raw_sha256']:
  assert i in expected;paths=dif(j(snap),j(row['path']));assert set(paths)==expected[i];admin.append(dict(path=row['path'],before=pin(row,snap),current=d(row['path']),admin_paths=paths))
 else:pin(row)
assert len(admin)==2
for row in s['additional_input_artifacts']:pin(row)
for lp in [R/'anonymous-decoder/lease.json',R/'source.review.lease.json',R/'whole-proof-review/lease.json']:assert j(lp)['status']=='CLOSED'
assert not astis.forbidden_pattern_hits();files=astis.lean_source_files();closure=[row['path'] for row in freeze['inputs'][:2]+freeze['inputs'][16:19]]
for q in closure:assert not astis.FORBIDDEN_REGEX.search(astis.strip_lean_comments_and_strings(Path(q).read_text(encoding='utf-8')))
assert 'import Tests' not in Path(closure[0]).read_text()
selected=set(subprocess.check_output(['git','ls-tree','-r','--name-only',C,'--',R.as_posix()],text=True).splitlines())|{row['path'] for row in mb['inputs']+s['input_artifacts'] if not row['path'].startswith('.lake/')}
gitrows=[]
q=subprocess.Popen(['git','cat-file','--batch'],stdin=subprocess.PIPE,stdout=subprocess.PIPE);out,_=q.communicate(('\n'.join(C+':'+v for v in sorted(selected))+'\n').encode());assert q.returncode==0;offset=0
for v in sorted(selected):
 e=out.index(b'\n',offset);h=out[offset:e].split();assert h[-1]!=b'missing',v;n=int(h[-1]);offset=e+1;blob=out[offset:offset+n];offset+=n+1;live=Path(v).read_bytes();assert (blob==live if v.startswith('runs/') else blob.replace(b'\r\n',b'\n')==live.replace(b'\r\n',b'\n')),v;gitrows.append(dict(d(v),git_blob_sha256=sha(blob),git_lf_sha256=sha(blob.replace(b'\r\n',b'\n')),raw_exact=blob==live))
g=j(R/'reviewer.exact.gates.json');assert g['checked_commit']==C and len(g['results'])==8
for row in g['results']:assert row['returncode']==0;pin(row)
assert 'ASTIS check passed' in (R/'reviewer.exact.aggregate.log').read_text();ax=re.findall(r"'([^']+)' depends on axioms: \[([^\]]+)\]",(R/'reviewer.exact.direct-axioms.log').read_text(),re.S)
assert len(ax)==3 and all(set(z.strip() for z in a.split(','))=={'propext','Classical.choice','Quot.sound'} for n,a in ax)
assert advance.current_advances()[freeze['advance_id']]['state']=='PROVED_LOCAL'
receipt=dict(status='passed-scoped-exact-admission-ready',checked_commit=C,verifier_id=V,math_freeze_count=22,whole_math_inputs=34,whole_math_review=d(R/'whole-proof-review/math.review.json'),source_inputs=67,source_review=d(R/'source.0.review.json'),source_packet=d(R/'source.0.reviewer-packet.json'),source_review_run_sha256=s['review_run_sha256'],publication_binding_sha256=s['publication_binding_sha256'],decoder_run_sha256=dec['decoder_run_sha256'],source_admin_reconciliation=admin,exact_Git_inputs=gitrows,exact_Git_input_count=len(gitrows),gates=g,aggregate_jobs=re.findall(r'Build completed successfully \((\d+) jobs\)',(R/'reviewer.exact.aggregate.log').read_text()),named_standard_axioms=[dict(declaration=n,axioms=[z.strip() for z in a.split(',')]) for n,a in ax],fake_closure_scan=dict(status='PASS',canonical_files=len(files),hits=0,reachable_files=closure,production_Test_imports=False),historical37_general_file='research-wiki/cited-results/SLT_reuse_audit.md now includes append-only38 checkpoint; not claimed equal to historical37 source footprint. Old37 production/source/decoder/raw receipts unchanged by38 and reused only in bounded mathematical scope.',remaining_boundary=['Full Hilbert/noncompact GaussianLSI, actual SPHMC square-root extension, T2/FIRST4.6 and both papers main results/query costs/composition remain open.','Shared38 imports/Registry/site/repository ProofSeal/Exposition/PURIFIED/remote CI/live are separate pending boundaries.'])
(R/'reviewer.exact.bindings.json').write_bytes((json.dumps(receipt,ensure_ascii=False,indent=2)+'\n').encode());print(json.dumps(dict(status=receipt['status'],git_inputs=len(gitrows),jobs=receipt['aggregate_jobs'],source_inputs=67,admin=admin),ensure_ascii=False))
