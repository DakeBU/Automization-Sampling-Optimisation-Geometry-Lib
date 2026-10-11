from pathlib import Path
import gzip,hashlib,json,re,subprocess,copy
R=Path('E:/Samplinglib');O=Path(__file__).parent;B=O.parent;PRE=R/'runs/20261007-companion-priority/pbps-prescribed-path-density-preread94'
C='ad3b80a339bf1cf0dd88685f202632a92eeb0797';BASE='87975b5682bec621644b12e701aa5e45fefc3c2d'
M='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPrescribedPathDensity.lean';L='website/content/declaration_lessons/pbps-actual-prescribed-path-density.json';P='website/content/publications/pbps-actual-prescribed-path-density.json';A='research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualPrescribedPathDensity.json';CELL='ASTIS-SW-PBPS-actual-prescribed-path-density'
def path(p):
 p=Path(p);return p if p.is_absolute() else R/p
def rel(p):return path(p).relative_to(R).as_posix()
def sha(b):return hashlib.sha256(b).hexdigest()
def info(p):
 p=path(p);b=p.read_bytes();return dict(path=rel(p),raw_sha256=sha(b),bytes=len(b))
def load(p):return json.loads(path(p).read_bytes())
def save(n,v):
 with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
def git(*a):return subprocess.check_output(['git',*a],cwd=R,stderr=subprocess.PIPE)
def canon(v):return json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()
assert git('rev-parse','HEAD').decode().strip()==C
assert git('merge-base',BASE,C).decode().strip()==BASE
tree={x.split('\t',1)[1]:x.split()[2] for x in git('ls-tree','-r','--full-tree',C).decode().splitlines()};cache={}
def blob(r):
 if r not in cache:cache[r]=git('cat-file','blob',tree[r])
 return cache[r]
stage=load(B/'science-staging94.json');assert blob(rel(B/'science-staging94.json'))==(B/'science-staging94.json').read_bytes()
prior=load(R/'runs/20261007-companion-priority/pbps-actual-finite-count-path93/exact-commit-verification93/closed-RAW-manifest93.json')
collab=prior['preserved_collaborator_inputs'];assert len(collab)==21
for x in collab:assert info(x['path'])['raw_sha256']==x['raw_sha256']
assert stage['preserved_collaborator_inputs']==collab
baseline_paths={rel(x['path']) for x in collab}
archives={rel(x['raw_path']):x for x in stage['raw_archives']};archive_by_hash={};archive_audit=[];snapshots={}
for r in stage['files']:
 assert r in tree,'staged but not committed '+r
 if not r.endswith('.gz'):snapshots.setdefault(sha(blob(r)),[]).append(r)
for r,x in archives.items():
 ab=blob(rel(x['archive']));assert sha(ab)==x['archive_sha256'];rb=gzip.decompress(ab)
 assert sha(rb)==x['raw_sha256'] and rb==path(r).read_bytes(),r
 if x['public_text_sha256'] is not None:assert sha(blob(r))==x['public_text_sha256'],r
 archive_by_hash.setdefault(sha(rb),[]).append(x)
 archive_audit.append(dict(raw_path=r,archive=rel(x['archive']),raw_sha256=sha(rb),archive_sha256=sha(ab)))
print('ARCHIVES PASS',len(archive_audit),flush=True)
matched={};local={};historical=[]
primary='runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
def exact(p):
 r=rel(p);p=path(p)
 if r in matched or r in local:return
 if r==primary or r.startswith('runs/20261007-companion-priority/pbps-actual-finite-count-path93/next-primary94/') or r.startswith(('.astis/toolchain/','.lake/')) or r in baseline_paths:
  local[r]=dict(**info(p),reason='Pinned local primary/source-only preread, runtime/library, or preserved collaborator input; no public theorem evidence waived.');return
 if r in archives:
  x=archives[r];assert gzip.decompress(blob(rel(x['archive'])))==p.read_bytes()
  matched[r]=dict(**info(p),binding='lossless-committed-gzip',archive=x['archive'],archive_raw_sha256=x['archive_sha256']);return
 assert r in tree,'MISSING COMMITTED EVIDENCE '+r
 assert blob(r)==p.read_bytes(),'BLOB MISMATCH '+r
 matched[r]=dict(**info(p),binding='exact-git-blob',git_object=tree[r])
def check(x):
 p=path(x['path']);h=x.get('raw_sha256',x.get('sha256'))
 if not isinstance(h,str) or len(h)!=64:return
 if not p.exists() or sha(p.read_bytes())!=h:
  if h in snapshots:
   r=snapshots[h][0];b=blob(r)
   if 'bytes' in x:assert len(b)==x['bytes']
   historical.append(dict(reference=x,resolved_committed_snapshot=r));return
  aa=archive_by_hash.get(h,[]);assert aa,'UNRESOLVED HISTORICAL RAW '+str(p)+' '+h
  b=gzip.decompress(blob(rel(aa[0]['archive'])))
  if 'bytes' in x:assert len(b)==x['bytes']
  historical.append(dict(reference=x,resolved_committed_archive=aa[0]['archive']));return
 if 'bytes' in x:assert len(p.read_bytes())==x['bytes']
 exact(p)
def records(v):
 if isinstance(v,dict):
  if isinstance(v.get('path'),str) and ('raw_sha256' in v or 'sha256' in v):check(v)
  for a in v.values():records(a)
 elif isinstance(v,list):
  for a in v:records(a)
def manifest(p):exact(p);v=load(p);records(v);return v
core=[M,L,P,A,'lean-toolchain','lake-manifest.json','runs/substantive_advances.jsonl','research-wiki/frontier-cells/'+CELL+'.json']
for p in core:exact(p)
assert info(M)['raw_sha256']=='60792981d3d2bac30d78a2373f7eed0002def8600e92553e9b5b0c87761599ec'
assert info('lean-toolchain')['raw_sha256']=='b2b5068d5a4835675e651ce83b29c0ddb308d28b80076e7c007aef4630af0477'
assert info('lake-manifest.json')['raw_sha256']=='b1f16b43aaf4a886cfe0382d5e3ae63d6904281c00afd8f35af20f0270a747e2'
assert git('-C','.lake/packages/mathlib','rev-parse','HEAD').decode().strip()=='db584cd6d46c92f209a44c0f1c829460d327499d'
seal=manifest(PRE/'root.statement-seal94.json');header=(PRE/'Header94.lean').read_text(encoding='utf8')
params=header.split('noncomputable def candidate_statement\n',1)[1].split(' : Prop := by',1)[0];body=header.split('  exact\n',1)[1].split('\n#check',1)[0].rstrip()
assert path(M).read_text(encoding='utf8').split('theorem actual_prescribed_path_density_rewrite\n',1)[1].split(' := by\n',1)[0]==params+' :\n'+body
for p in [PRE/'independent-header-math94/closed-RAW-manifest94.native.json',PRE/'independent-header-source94/closed-RAW-header-audit94.native.json',B/'independent-fragment-math94/closed-RAW-fragment94.native.json',B/'independent-whole-math94/closed-RAW-whole94.native.json',B/'independent-whole-math94/exposition94/closed-RAW-exposition94.native.json',B/'independent-whole-math94/lf-transfer94/closed-RAW-LF-transfer94.native.json',B/'primary-source94/closed-RAW-review94.native.json',B/'primary-source94/closed-RAW-source-prep94.native.json',B/'decoder-freeze94.json']:manifest(p)
math=load(B/'independent-whole-math94/lf-transfer94/LF-transfer-decision94.native.json');assert math['decision']=='ACCEPT_LF_TRANSFER_OF_PRIOR_WHOLE_MATH_AND_EXPOSITION' and not math['necessary_repairs'] and math['production_after_raw']==info(M)['raw_sha256']
S=B/'primary-source94';native=load(S/'source-review-decision94.native.json');run=load(S/'review-run94.native.json');audit=load(A)
assert native['independent_from_formalizer'] and native['independent_from_decoder'] and native['reviewer']=='/root/primary_source93'
assert native['source_review']['state']=='accepted' and native['verdict']=='equivalent-after-elaboration' and not native['repairs'] and not native['blocking_findings']
assert native['whole_module_reviewed'] and native['all_seven_authored_steps_reviewed'] and not native['other_math_reviewer_verdicts_read']
assert audit['state']=='accepted' and audit['semantic_slots']==native['semantic_slots'] and len(audit['semantic_slots'])==7
RUN='36e22753d0345a8369f2e7f76bc4b798b1d491e57db148665585879247b9ed82';BIND='22a19fb883390aa4f0516852f6d215a1f7b27d904b0847757ef588cce47ed183';PACK='5413ba30c36fb4e0db7b9a172694a8d7611540b038d7f380a228209395d61dee'
assert audit['source_review']['review_run_sha256']==native['review_run_sha256']==run['review_run_sha256']==RUN
assert sha(canon({k:v for k,v in run.items() if k!='review_run_sha256'}))==RUN
payload=copy.deepcopy(native);payload.pop('review_run_sha256');payload.pop('review_run_artifact');payload['source_review'].pop('review_run_sha256')
assert sha(canon(payload))==run['decision_payload_sha256']
assert audit['publication_binding_sha256']==native['publication_binding_sha256']==BIND
assert audit['source_review']['reviewer_packet_sha256']==native['reviewer_packet_sha256']==PACK
packet=load(B/'reviewer-packet94.lf.json');assert packet.pop('packet_sha256')==sha(canon(packet))==PACK
for key in ['module','publication','lesson','primary','source_graph','source_only_reconstruction','input_checks']:check(native[key])
oldpub=load(B/'independent-whole-math94/exposition94/publication.accepted.exactraw.json');newpub=load(P)
oldpc=oldpub['items'][0].pop('source_proof_coverage');newpc=newpub['items'][0].pop('source_proof_coverage');assert oldpub==newpub,'unexpected publication metadata change'
assert newpc['coverage_report']==rel(S/'compiled-source-coverage-exposition94.native.json')
save('publication-metadata-transfer94.json',dict(status='PASS',only_change='source_proof_coverage metadata',before=oldpc,after=newpc,current=info(P),binding_unchanged=BIND,mathematical_statement_and_lesson_unchanged=True))
dec=R/'runs/semantic-roundtrip/anonymous94/decoder';dm=manifest(dec/'raw-manifest.json');dr=load(dec/'decoder-report.json');dp=load(dec.parent/'input.json')
for p in [dec/'decoder-report.json',dec/'reconstructed-theorem.txt',dec.parent/'input.json']:exact(p)
assert dp.pop('packet_sha256')==sha(canon(dp))==dm['packet_sha256']==audit['reconstruction']['decoder_packet_sha256']
assert sha(canon({k:v for k,v in dr.items() if k!='decoder_run_sha256'}))==dr['decoder_run_sha256']==dm['decoder_run_sha256']==audit['reconstruction']['decoder_run_sha256']
assert not dm['source_text_visible'] and not dr['source_text_visible'] and not audit['reconstruction']['source_text_visible']
assert dr['decoder']=='/root/blind_decoder93' and not dr['access_boundary']['source_files_read'] and not dr['access_boundary']['implementation_files_read'] and not dr['access_boundary']['previous_reviews_read']
assert dr['exact_lean_statement']==dp['lean']['statement']
assert sha(dp['lean']['statement'].encode())==audit['reconstruction']['lean_statement_sha256']
assert audit['reconstruction']['text']==dr['reconstructed_theorem_text']==(dec/'reconstructed-theorem.txt').read_text(encoding='utf8')
assert sha(dr['reconstructed_theorem_text'].encode())==dm['reconstructed_text_sha256']
assert dr['semantic_slots']==audit['reconstruction']['native_semantic_slots']
save('source-decoder-bindings94.json',dict(status='PASS',source_decision=info(S/'source-review-decision94.native.json'),source_run=info(S/'review-run94.native.json'),source_manifest=info(S/'closed-RAW-review94.native.json'),source_packet_sha256=PACK,source_run_canonical_sha256=RUN,publication_binding_sha256=BIND,decoder_manifest=info(dec/'raw-manifest.json'),decoder_packet_sha256=dm['packet_sha256'],decoder_run_sha256=dr['decoder_run_sha256'],seven_source_semantic_slots_exact=True,native_decoder_reconstruction_exact=True,canonical_hash_recipes_checked=True))
for p in ['astis.py','astis_advance.py','astis_publication.py','astis_contributor_contract.py','astis_frontier_cells.py','astis_semantic_roundtrip.py']:exact(R/'tools'/p)
for row in collab:assert info(row['path'])['raw_sha256']==row['raw_sha256']
save('archive-audit94.json',dict(status='PASS',verified_commit=C,count=len(archive_audit),archives=archive_audit,historical_reference_resolutions=historical))
save('input-freeze94.json',dict(status='PASS',verified_commit=C,base=BASE,exact_commit_matches=list(matched.values()),local_pinned_or_excluded_inputs=list(local.values()),preserved_collaborator_inputs=collab,publication_binding_sha256=BIND,reviewer_packet_sha256=PACK,source_review_run_sha256=RUN,archive_count=len(archive_audit),historical_reference_resolutions=historical))
print('SCIENCE94 EXACT INPUTS PASS',len(matched),len(local),len(historical),flush=True)
