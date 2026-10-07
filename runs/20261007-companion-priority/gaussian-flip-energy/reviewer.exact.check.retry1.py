from pathlib import Path
import json,hashlib,subprocess,sys,re
sys.path.insert(0,'tools')
import astis_publication as pub,astis_advance as advance,astis
R=Path('runs/20261007-companion-priority/gaussian-flip-energy');C='c3bbf938a6d46de7d43036d9f066ba68a3e6be6f';V='picard_commit_verifier_20261005'
def j(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
def d(p):
 b=Path(p).read_bytes();return dict(path=Path(p).as_posix(),raw_sha256=sha(b),lf_sha256=sha(b.replace(b'\r\n',b'\n')),bytes=len(b))
def pin(row,p=None):
 x=d(p or row['path']);assert x['raw_sha256']==row['raw_sha256'],(x,row)
 if 'lf_sha256' in row:assert x['lf_sha256']==row['lf_sha256'],(x,row)
 return x
def dif(a,b,p=''):
 if type(a)!=type(b):return [p]
 if isinstance(a,dict):return [q for k in sorted(a.keys()|b.keys()) for q in ([p+'/'+k] if k not in a or k not in b else dif(a[k],b[k],p+'/'+k))]
 if isinstance(a,list):return [p] if len(a)!=len(b) else [q for i,(x,y) in enumerate(zip(a,b)) for q in dif(x,y,p+'/'+str(i))]
 return [] if a==b else [p]
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==C
assert subprocess.check_output(['git','-C','.lake/packages/mathlib','rev-parse','HEAD'],text=True).strip()=='db584cd6d46c92f209a44c0f1c829460d327499d'
assert Path('lean-toolchain').read_text().strip()=='leanprover/lean4:v4.33.0'
freeze=j(R/'math-freeze.json');assert len(freeze['inputs'])==27
math=j(R/'whole-proof-review/math.review.json');assert math['verification_status']=='passed-scoped' and not math['blockers'] and math['all_private_providers_reviewed']==10
assert d(R/'whole-proof-review/math.review.json')['raw_sha256']=='f35e9f86b3fb312017c12d9bd32819bbcda6bdda40c3516640a557f38d5516a1'
pin(math['input_bindings']);mb=j(math['input_bindings']['path']);assert len(mb['inputs'])==42
for row in freeze['inputs']+mb['inputs']:pin(row)
for row in mb['inputs']:
 if 'raw_snapshot' in row:
  pin(row,row['raw_snapshot']);assert Path(row['lf_snapshot']).read_bytes()==Path(row['path']).read_bytes().replace(b'\r\n',b'\n')
sig=(R/'preproof/signature.prospective.txt').read_bytes();assert len(sig)==877 and sha(sig)=='4e9395eb1ff6054d2cc09ad4d938668d577935fb1a6c574a2e2c69dbe1d838f1'
assert sig.rstrip()+b' := by' in Path(freeze['inputs'][0]['path']).read_bytes().replace(b'\r\n',b'\n')
plan=j(R/'publication-plan.json');local=j(R/'proved-local.json');decls=plan['mathematical_declarations'];assert decls==local['lean_declarations']==local['publication_declarations']
data=pub.inputs();item=next(x for x in pub.load() if x['id']==plan['slugs'][0]);b=next(x for x in item['bindings'] if x['declaration']==decls[0]);audit=data['audits'][plan['audit_ids'][0]]
s=j(R/'source.0.review.overlay1.json');p=j(R/'source.0.reviewer-packet.overlay1.json')
assert pub.digest({k:v for k,v in s.items() if k!='review_run_sha256'})==s['review_run_sha256']
assert pub.digest({k:v for k,v in p.items() if k!='packet_sha256'})==p['packet_sha256']
assert s['verdict']=='equivalent-after-elaboration' and not s['blocking'] and s['deltas']==s['repairs']==[]
assert s['reviewer']!=V and s['independent_from_formalizer'] and s['independent_from_decoder'] and s['whole_module_covered']
assert s['whole_module_raw_sha256']==d(freeze['inputs'][0]['path'])['raw_sha256'] and s['whole_module_lf_sha256']==d(freeze['inputs'][0]['path'])['lf_sha256']
assert pub.binding_digest(item,b,data)==s['publication_binding_sha256']==p['publication_binding_sha256']==audit['publication_binding_sha256']
assert pub.review_context(item,b,data)==p['candidate_publication_context']==audit['publication_context']
assert pub.digest(p['candidate_publication_context'])==s['review_context_sha256']
assert audit['state']=='accepted' and audit['source_review']['review_run_sha256']==s['review_run_sha256'] and audit['source_review']['reviewer_packet_sha256']==p['packet_sha256']
assert set(s['semantic_slots'])=={'objects','domains','quantifiers','assumptions','conclusion','scopes','constant_dependencies'}
pub.check_advance(decls,reviewed=True)
allowed={'/state','/source_review/metadata_only_overlay','/source_review/state','/source_review/reviewer','/source_review/independent_from_formalizer','/source_review/independent_from_decoder','/source_review/evidence','/source_review/run_artifact','/source_review/review_run_sha256','/source_review/reviewer_packet_sha256','/semantic_slots','/deltas','/verdict','/status','/evidence/proof_review','/evidence/development_boundary'}
drifts=[];assert len(s['input_artifacts'])==119
for i,row in enumerate(s['input_artifacts']):
 snap=R/f'source.overlay1.review.input.{i:03d}.raw.snapshot';pin(row,snap)
 assert (R/f'source.overlay1.review.input.{i:03d}.lf.snapshot').read_bytes()==snap.read_bytes().replace(b'\r\n',b'\n')
 if d(row['path'])['raw_sha256']!=row['raw_sha256']:
  change=dif(j(snap),j(row['path']));assert set(change)<=allowed,(row['path'],change)
  assert '/audits/' in row['path'] or '/frontier-cells/' in row['path']
  drifts.append(dict(path=row['path'],before=pin(row,snap),current=d(row['path']),admin_paths=change))
 else:pin(row)
old=j(R/'source.0.review.json');assert old['blocking'] and d(R/'source.0.review.json')['raw_sha256']=='4da60ac71132deed2da980e3beafb86a8293205f623053ced7d205b7d4fdeaba'
overlay=j(R/'dependency-metadata-overlay1/overlay1.review.json');assert overlay['status']=='ACCEPTED_SCOPED_METADATA_ONLY_REPAIR_OVERLAY' and pub.digest({k:v for k,v in overlay.items() if k!='review_run_sha256'})==overlay['review_run_sha256']
assert s['metadata_overlay_review_run_sha256']==overlay['review_run_sha256']
dec=j(R/'anonymous-decoder/run.json');result=j(R/'anonymous-decoder/result0.json');dp=j(R/'anonymous-decoder/packet0.json')
assert not dec['source_text_visible'] and not dec['compiler_started'] and pub.digest(dec['canonical_basis'])==dec['decoder_run_sha256']==s['decoder_run_sha256']
assert {k:v for k,v in result.items() if k!='decoder_run_sha256'}==dec['canonical_basis']['reconstruction']
assert sha(result['reconstructed_theorem_text'].encode())==result['reconstructed_text_sha256']==s['reconstruction_text_sha256']
assert pub.digest({k:v for k,v in dp.items() if k!='packet_sha256'})==dp['packet_sha256']==s['decoder_packet_sha256']
assert audit['reconstruction']['decoder_run_sha256']==dec['decoder_run_sha256'] and audit['reconstruction']['text']==result['reconstructed_theorem_text']
assert not astis.forbidden_pattern_hits();files=astis.lean_source_files()
closure=[freeze['inputs'][0]['path'],'AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/GaussianCompactEntropy.lean','AutoSamplingTheory/TechnicalLemmas/Probability/BalancedRademacherCLT.lean',freeze['inputs'][1]['path']]
for q in closure:assert not astis.FORBIDDEN_REGEX.search(astis.strip_lean_comments_and_strings(Path(q).read_text(encoding='utf-8')))
assert 'import Tests' not in Path(closure[0]).read_text()
selected=set(subprocess.check_output(['git','ls-tree','-r','--name-only',C,'--',R.as_posix()],text=True).splitlines())
selected|={row['path'] for row in mb['inputs']+s['input_artifacts'] if not row['path'].startswith('.lake/')}
gitrows=[]
for q in sorted(selected):
 blob=subprocess.check_output(['git','show',C+':'+q]);live=Path(q).read_bytes()
 assert (blob==live if q.startswith('runs/') else blob.replace(b'\r\n',b'\n')==live.replace(b'\r\n',b'\n')),q
 gitrows.append(dict(d(q),git_blob_sha256=sha(blob),git_LF_sha256=sha(blob.replace(b'\r\n',b'\n')),raw_exact=blob==live))
gates=j(R/'reviewer.exact.gates.json');assert gates['checked_commit']==C and len(gates['results'])==8
for row in gates['results']:assert row['returncode']==0;pin(row)
ax=re.findall(r"'([^']+)' depends on axioms: \[([^\]]+)\]",(R/'reviewer.exact.direct-axioms.log').read_text(),re.S)
assert len(ax)==3 and all(set(x.strip() for x in a.split(','))=={'propext','Classical.choice','Quot.sound'} for n,a in ax)
assert 'ASTIS check passed' in (R/'reviewer.exact.aggregate.log').read_text()
state=advance.current_advances()[freeze['advance_id']];assert state['state']=='PROVED_LOCAL' and state['owner_id']!=V
out=dict(status='passed-scoped-exact-admission-ready',checked_commit=C,verifier_id=V,math_freeze_count=27,whole_math_bindings=42,whole_math_review=d(R/'whole-proof-review/math.review.json'),source_inputs=119,source_review=d(R/'source.0.review.overlay1.json'),source_packet=d(R/'source.0.reviewer-packet.overlay1.json'),source_review_run_sha256=s['review_run_sha256'],decoder_run_sha256=dec['decoder_run_sha256'],publication_binding_sha256=s['publication_binding_sha256'],source_admin_reconciliation=drifts,git_input_count=len(gitrows),git_inputs=gitrows,gates=gates,aggregate_jobs=re.findall(r'Build completed successfully \((\d+) jobs\)',(R/'reviewer.exact.aggregate.log').read_text()),named_standard_axioms=[dict(declaration=n,axioms=[x.strip() for x in a.split(',')]) for n,a in ax],fake_closure_scan=dict(status='PASS',canonical_files=len(files),hits=0,reachable_files=closure,production_Tests_imports=False),remaining_boundary=['Compact GaussianLSI, Hilbert/noncompact extension, T2/FIRST4.6, both main results and query cost/composition remain open.','Shared imports/Registry/site/repository ProofSeal/Exposition/PURIFIED/current CI/live remain separate.'])
(R/'reviewer.exact.bindings.json').write_bytes((json.dumps(out,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps({k:out[k] for k in ['status','checked_commit','git_input_count','source_inputs','aggregate_jobs','source_admin_reconciliation']},ensure_ascii=False))
