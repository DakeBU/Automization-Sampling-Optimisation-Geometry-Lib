exec(open('runs/20261007-companion-priority/gaussian-noncompact-lsi/reviewer.exact.gate.py',encoding='utf-8').read().split('assert subprocess.check_output')[0])
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
freeze=j(R/'math-freeze.json');W=R/'whole-proof-review42';math=j(W/'reviewer.math.review.json');mb=j(W/'inputs.json');mr=j(W/'run.json')
assert len(freeze['inputs'])==46 and len(mb['bindings'])==86
assert math['status']=='accepted-scoped' and not math['blockers'] and not math['canonical_or_production_edits']
assert pub.digest(mr['artifacts'])==mr['run_sha256'] and mr['all_leases_CLOSED']
for row in mr['artifacts']:pin(row,W/row['path'])
for row in freeze['inputs']:pin(row)
for row in mb['bindings']:
 pin(row);pin(row,W/row['raw_snapshot']);assert (W/row['lf_snapshot']).read_bytes()==(W/row['raw_snapshot']).read_bytes().replace(b'\r\n',b'\n')
sig=Path('runs/20261007-companion-priority/gaussian-noncompact-lsi-preproof42/signature.prospective.txt').read_bytes()
assert len(sig)==691 and sha(sig)==j(W/'reachability.analysis.json')['public691_LF_sha256']
assert sig.rstrip()+b' := by' in Path(freeze['inputs'][0]['path']).read_bytes().replace(b'\r\n',b'\n')
api=j(W/'api-evidence.json');api_new=j(W/'api-evidence.span-corrected.json');assert diff(api,api_new)==['/14/lines'] and api[14]['lines']==[44,112] and api_new[14]['lines']==[44,95]
repair=j(W/'api-span-correction.json');pin(repair['original_api_evidence'],W/repair['original_api_evidence']['path']);pin(repair['corrected_api_evidence'],W/repair['corrected_api_evidence']['path']);assert d(W/'reviewer.math.review.json')['raw_sha256']==repair['unchanged_original_review_sha256']
assert j(R/'root.api-span-correction.accepted.json')['status']=='independently-accepted-exact-one-field-metadata-correction'
assert len(Path(repair['actual_source']['path']).read_text().splitlines())==95
plan=j(R/'publication-plan.json');local=j(R/'proved-local.json');decls=plan['mathematical_declarations']
assert decls==local['lean_declarations']==local['publication_declarations'] and local['result_kind']=='theorem-edge'
data=pub.inputs();item=next(z for z in pub.load() if z['id']==plan['slugs'][0]);binding=next(z for z in item['bindings'] if z['declaration']==decls[0]);audit=data['audits'][plan['audit_ids'][0]]
s=j(R/'source.0.review.json');p=j(R/'source.0.reviewer-packet.json');dec=j(R/'anonymous-decoder/run.json');result=j(R/'anonymous-decoder/result0.json');dp=j(R/'anonymous-decoder/packet0.json');dr=j(R/'anonymous-decoder/binding-receipt.json')
assert pub.digest({k:v for k,v in s.items() if k!='review_run_sha256'})==s['review_run_sha256']
assert pub.digest({k:v for k,v in p.items() if k!='packet_sha256'})==p['packet_sha256']
assert s['verdict']=='equivalent-after-elaboration' and not s['blocking'] and s['deltas']==s['repairs']==s['source_EXCESS']==[]
assert s['independent_from_decoder'] and s['independent_from_formalizer'] and s['reviewer']!=V
assert s['whole_module_file_sha256']==pin(freeze['inputs'][0])['raw_sha256'] and s['whole_module_lf_sha256']==pin(freeze['inputs'][0])['lf_sha256']
assert len(s['whole_module_coverage']['private_helpers'])==5 and s['whole_module_coverage']['Tests_read']==3
assert sha(p['source']['original_text'].encode())==s['source_text_sha256']==p['source']['text_sha256']
assert sha(p['lean']['statement'].encode())==s['statement_sha256']==p['lean']['statement_sha256']
assert pub.binding_digest(item,binding,data)==s['publication_binding_sha256']==p['publication_binding_sha256']==audit['publication_binding_sha256']
assert pub.review_context(item,binding,data)==p['candidate_publication_context']==audit['publication_context']
assert audit['state']=='accepted' and audit['source_review']['review_run_sha256']==s['review_run_sha256'] and audit['source_review']['reviewer_packet_sha256']==p['packet_sha256']
assert set(s['semantic_slots'])=={'objects','domains','quantifiers','assumptions','conclusion','scopes','constant_dependencies'}
assert all(not x for x in p['anti_anchoring'].values()) and not s['exposure'].get('whole_math_verdict_read',False)
assert d(R/'anonymous-decoder/run.json')['raw_sha256']==s['decoder_run_sha256']==dr['decoder_run_sha256']
assert not result['source_text_visible'] and not dec['source_text_visible'] and not dec['compiler_started']
assert sha(result['reconstructed_theorem_text'].encode())==s['reconstruction_sha256']==result['reconstructed_text_sha256']
assert pub.digest({k:v for k,v in dp.items() if k!='packet_sha256'})==dp['packet_sha256']==s['decoder_packet_sha256']
assert audit['reconstruction']['text']==result['reconstructed_theorem_text'] and audit['reconstruction']['decoder_run_sha256']==s['decoder_run_sha256']
assert result['decoder_id'] not in [V,s['reviewer']]
for row in dr['output_artifacts']:pin(row)
pin(dr['opening_lease']);pin(dec['input_artifacts'][0],R/'anonymous-decoder/packet0.json');pin(dec['input_artifacts'][1],R/'anonymous-decoder/initial-lease.raw.snapshot.json')
pin(s['primary_before_body']);pin(s['checks_artifact'])
primary=j(s['primary_before_body']['path']);primarypins=[pin(z) for z in primary['input_artifacts']]
assert j(R/'source.review.lease.json')['all_leases']=='CLOSED'
pub.check_advance(decls,reviewed=True)
checks=j(R/'source.review.checks.json');snapshots={z['input']['path']:z['snapshot']['path'] for z in checks['immutable_snapshot_mapping']}
assert len(s['input_artifacts'])==177
expected_audit={'/deltas','/semantic_slots','/source_review/evidence','/source_review/independent_from_decoder','/source_review/independent_from_formalizer','/source_review/review_run_sha256','/source_review/reviewer','/source_review/reviewer_packet_sha256','/source_review/run_artifact','/source_review/state','/state','/verdict'}
expected_cell={'/evidence/execution_boundary','/evidence/proof_review','/evidence/source_review','/status'}
admin=[]
for row in s['input_artifacts']:
 raw=Path(snapshots[row['path']]);pin(row,raw)
 if d(row['path'])['raw_sha256']!=row['raw_sha256']:
  paths=diff(j(raw),j(row['path']));expected=expected_audit if '/audits/' in row['path'] else expected_cell
  assert set(paths)==expected,(row['path'],paths);admin.append(dict(path=row['path'],before=pin(row,raw),current=d(row['path']),admin_paths=paths))
 else:pin(row)
assert len(admin)==2
draft=j(R/'decoder-binding-before.0.raw.snapshot.audit.json');pre=j(R/'source-admission-before.0.raw.snapshot.audit.json');decoderpaths=diff(draft,pre)
assert set(decoderpaths)<= {'/state','/reconstruction','/publication_context','/publication_binding_sha256','/source_review/run_artifact','/source_review/evidence'},decoderpaths
assert Path(R/'source-admission-before.0.raw.snapshot.audit.json').read_bytes()==Path(snapshots[s['input_artifacts'][0]['path']]).read_bytes()
for lp in [R/'anonymous-decoder/lease.json',R/'source.review.lease.json',R/'whole-proof-review42/lease.json']:assert j(lp)['status']=='CLOSED'
reach=j(R/'whole-proof-review42/reachability.analysis.json');assert not reach['fake_closure_hits'] and not reach['unmapped_constants']
assert not astis.forbidden_pattern_hits();files=astis.lean_source_files()
prod=Path(freeze['inputs'][0]['path']).read_text();assert len(re.findall(r'^private theorem ',prod,re.M))==5 and 'import Tests.' not in prod
selected=set(subprocess.check_output(['git','ls-tree','-r','--name-only',C,'--',R.as_posix()],text=True).splitlines())|{z['path'] for z in mb['bindings']+s['input_artifacts']+primary['input_artifacts'] if not z['path'].startswith('.lake/')}
for z in reach['reached_modules'].values():selected.add(z['path'])
pr=subprocess.Popen(['git','cat-file','--batch'],stdin=subprocess.PIPE,stdout=subprocess.PIPE);out,_=pr.communicate(('\n'.join(C+':'+v for v in sorted(selected))+'\n').encode());assert pr.returncode==0;offset=0;gitrows=[]
for v in sorted(selected):
 e=out.index(b'\n',offset);header=out[offset:e].split();assert header[-1]!=b'missing',v;n=int(header[-1]);offset=e+1;blob=out[offset:offset+n];offset+=n+1;live=Path(v).read_bytes()
 assert (blob==live if v.startswith('runs/') else blob.replace(b'\r\n',b'\n')==live.replace(b'\r\n',b'\n')),v
 gitrows.append(dict(d(v),git_blob_sha256=sha(blob),git_lf_sha256=sha(blob.replace(b'\r\n',b'\n')),raw_exact=blob==live))
g=j(R/'reviewer.exact.gates.json');assert g['checked_commit']==C and g['all_pass'] and len(g['results'])==8
for row in g['results']:assert row['returncode']==0;pin(row)
assert 'ASTIS check passed' in (R/'reviewer.exact.mandatory.log').read_text()
ax=re.findall(r"'([^']+)' depends on axioms: \[([^\]]+)\]",(R/'reviewer.exact.direct-axioms.log').read_text(),re.S)
assert len(ax)==4 and all(set(z.strip() for z in a.split(','))=={'propext','Classical.choice','Quot.sound'} for _,a in ax)
coverage=[]
for line in (R/'reviewer.exact.publication.log').read_text(encoding='utf-8').splitlines():
 if line.startswith('Private implementation coverage: '):
  row=json.loads(line[len('Private implementation coverage: '):])
  if row['file']==freeze['inputs'][0]['path']:coverage.append(row);assert row['owner']==decls[0]
assert len(coverage)==5
states=advance.current_advances();assert states[freeze['advance_id']]['state']=='PROVED_LOCAL' and states[freeze['advance_id']]['owner_id']!=V
assert [a for a,z in states.items() if z['state']=='STABILIZING']==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
rec=put(R/'reviewer.exact.admission-reconciliation.json',dict(verifier_id=V,checked_commit=C,math46_and_whole86_unchanged=True,source177_and_primary_raw_LF_snapshots_preserved=True,source_administrative_changes=admin,decoder_binding_paths=decoderpaths,decoder_hash_contract='Actual original flat run RAW digest; opening lease preserved separately.',source_scope='Actual noncompact signed C2 Gaussian function LSI2 with genuine fL2/gradientL2/PhiL1; actual32 uncut posterior Test, no coherent33 KL/Fisher/T2 claim.'))
x=dict(status='passed-scoped-exact-admission-ready',checked_commit=C,verifier_id=V,math_freeze_count=46,whole_math_inputs=86,whole_math_review=d(R/'whole-proof-review42/reviewer.math.review.json'),whole_math_run_sha256=mr['run_sha256'],source_inputs=177,primary_source_inputs=len(primarypins),source_review=d(R/'source.0.review.json'),source_packet=d(R/'source.0.reviewer-packet.json'),source_review_run_sha256=s['review_run_sha256'],publication_binding_sha256=s['publication_binding_sha256'],decoder_run_sha256=s['decoder_run_sha256'],source_admin_reconciliation=rec,exact_Git_inputs=gitrows,exact_Git_input_count=len(gitrows),gates=g,aggregate_jobs=re.findall(r'Build completed successfully \((\d+) jobs\)',(R/'reviewer.exact.mandatory.log').read_text()),named_standard_axioms=[dict(declaration=n,axioms=[z.strip() for z in a.split(',')]) for n,a in ax],fake_closure_scan=dict(status='PASS',canonical_files=len(files),hits=0,reachable_modules=len(reach['reached_modules']),private_providers=5,private_owner_coverage=coverage),lean_declarations=decls,remaining_boundary=['Only signed globally C2 finite-Hilbert stdGaussian LSI2 with genuine fL2/gradientL2/PhiL1 domains and internal cutoff limits. True32 uncut posterior Test; coherent33 KL/Fisher, full weakW12, T2/FIRST4.6/main/work/cost/composition remain open.','New42 shared imports/Registry/site and repository ProofSeal, full-reader/Exposition/PURIFIED/remoteCI/merge/live remain separate pending boundaries; mandatory currently aggregates prior41 only.'])
saved=put(R/'reviewer.exact.bindings.json',x)
print(json.dumps(dict(status=x['status'],bindings=saved,git_inputs=len(gitrows),aggregate_jobs=x['aggregate_jobs'],source_inputs=177,primary_inputs=len(primarypins),admin_changes=len(admin),canonical_fake_files=len(files),fake_hits=0),indent=2))
