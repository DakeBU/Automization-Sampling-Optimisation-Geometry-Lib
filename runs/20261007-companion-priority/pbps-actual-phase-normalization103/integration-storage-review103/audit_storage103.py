import pathlib,json,hashlib,gzip,subprocess,datetime,re
from html.parser import HTMLParser
R=pathlib.Path('E:/Samplinglib');S='030f4f70feb3641cafca981ee81c48a2687db1ee';I='82d544e79ddc48726f9aea16b1b144f68ba4f049';B='runs/20261007-companion-priority/pbps-actual-phase-normalization103';O=R/(B+'/integration-storage-review103')
def h(b):return hashlib.sha256(b).hexdigest()
def normpath(p):return p.replace('\\','/').replace('E:/Samplinglib/','')
reads={};cache={};batch=subprocess.Popen(['git','cat-file','--batch'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,cwd=str(R))
def blob(c,p):
 p=normpath(p);k=(c,p)
 if k not in cache:
  batch.stdin.write((c+':'+p+'\n').encode());batch.stdin.flush();head=batch.stdout.readline().decode().strip()
  if head.endswith(' missing'):cache[k]=None
  else:
   size=int(head.rsplit(' ',1)[1]);cache[k]=batch.stdout.read(size);assert batch.stdout.read(1)==b'\n'
 if cache[k] is not None:reads[c+':'+p]={'commit':c,'path':p,'raw_sha256':h(cache[k]),'bytes':len(cache[k])}
 return cache[k]
def J(p,c=I):return json.loads(blob(c,p).decode('utf-8-sig'))
def local(p):
 p=normpath(p);b=(R/p).read_bytes();reads['working:'+p]={'path':p,'storage':'working tree','raw_sha256':h(b),'bytes':len(b)};return b
def put(n,d):
 p=O/n;assert not p.exists();p.write_bytes((json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode());return {'path':p.relative_to(R).as_posix(),'raw_sha256':h(p.read_bytes()),'bytes':p.stat().st_size}
def public_normalize(b):return b'\n'.join(x.rstrip(b' \t') for x in b.replace(b'\r\n',b'\n').split(b'\n')).rstrip(b'\n')+b'\n'
notes=J(B+'/integration.notes.json');fr=J(B+'/exact-commit-verification103/input-freeze103.json');ar=J(B+'/exact-commit-verification103/archive-audit103.json');cl=J(B+'/exact-commit-verification103/closed-RAW-manifest103.json');im=J(B+'/integration103/immutable-integration-RAW-archives103.json');stage=J(B+'/science-staging103.json');scope=J(B+'/integration103/staged-scope103.json')
index={}
for a in ar['archives']+im['files']:index.setdefault((normpath(a['raw_path']),a['raw_sha256']),[]).append(a)
details={};errors=[]
def check(n,ok,e=None):
 details[n]={'PASS':bool(ok),'evidence':e}
 if not ok:errors.append(n)
def resolve(r,commits=(I,S)):
 rr=r.get('reference',r);p=normpath(rr.get('path',rr.get('raw_path','')));want=rr.get('raw_sha256');cand=[]
 for key in ['snapshot','archive']:
  if r.get(key):cand.append((normpath(r[key]),key))
 for a in index.get((p,want),[]):cand.append((a['archive'],'indexed archive'))
 for q,m in list(cand):
  for a in index.get((q,want),[]):cand.append((a['archive'],'snapshot indexed archive'))
 cand.append((p,'direct'))
 for c in commits:
  for q,m in cand:
   z=blob(c,q)
   if z is None:continue
   try:d=gzip.decompress(z) if q.endswith('.gz') else z
   except Exception:continue
   if h(d)==want:return {'path':p,'raw_sha256':want,'storage':q,'commit':c,'method':m,'PASS':True}
 return {'path':p,'raw_sha256':want,'PASS':False,'candidates':cand}
def archcheck(a,c):
 z=blob(c,a['archive']);want=a.get('archive_raw_sha256',a.get('archive_sha256'));out={'archive':a['archive'],'commit':c,'PASS':False}
 if z is None:return out
 d=gzip.decompress(z);ok=h(z)==want and h(d)==a['raw_sha256'];out.update(archive_RAW_matches=h(z)==want,decompressed_RAW_matches=h(d)==a['raw_sha256'])
 pub=a.get('public_text_raw_sha256',a.get('public_text_sha256'))
 if pub:
  b=blob(c,a['raw_path'])
  pok=b is not None and h(b)==pub and b in [d,d.replace(b'\r\n',b'\n'),public_normalize(d)]
  out['public_presentation_matches_declared_policy']=pok;ok=ok and pok
 out['PASS']=ok;return out
for name,records,commits in [('science_archives',ar['archives'],[S,I]),('integration_archives',im['files'],[I])]:
 result=[archcheck(a,c) for a in records for c in commits];details[name]=result;check('all_'+name,all(v['PASS'] for v in result),{'archive_count':len(records),'commits':commits})
check('science_staging_archive_inventory_matches_verifier',stage['raw_archives']==ar['archives'])
for name,records in [('science_inputs',fr['exact_commit_matches']),('historical_references',fr['historical_reference_resolutions']),('exact_verifier_outputs',cl['owned_artifacts'])]:
 out=[resolve(r) for r in records];details[name]=out;check('all_'+name+'_recoverable',all(v['PASS'] for v in out),len(out))
collab=[dict(r,PASS=h(local(r['path']))==r['raw_sha256']) for r in fr['preserved_collaborator_inputs']];details['collaborators']=collab;check('all21_protected_collaborator_RAWs',len(collab)==21 and all(v['PASS'] for v in collab) and stage['preserved_collaborator_inputs']==fr['preserved_collaborator_inputs'])
excl=[dict(r,PASS=h(local(r['path']))==r['raw_sha256']) for r in fr['local_pinned_or_excluded_inputs']];details['local_pinned']=excl;check('all_pinned_excluded_inputs',all(v['PASS'] for v in excl))
gates=[]
for g in notes['checks']:
 refs=[resolve(g[k]) for k in ['receipt','stdout','stderr']];rc=J(g['receipt']['path']);gates.append({'label':g['label'],'receipt':rc,'bindings':refs,'PASS':all(v['PASS'] for v in refs) and rc.get('exit_code')==0 and rc.get('terminal_closed') is True})
details['gates']=gates;check('all15_terminal_gates_PASS',len(gates)==15 and all(g['PASS'] for g in gates))
reg=next(g for g in notes['checks'] if g['label']=='integration-site-regressions');rz=resolve(reg['stderr']);rb=blob(rz['commit'],rz['storage']);rb=gzip.decompress(rb) if rz['storage'].endswith('.gz') else rb;check('226_regression_tests_PASS',b'Ran 226 tests' in rb and rb.rstrip().endswith(b'OK'))
module='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhaseNormalization.lean';lesson='website/content/declaration_lessons/pbps-actual-phase-normalization.json';pub='website/content/publications/pbps-actual-phase-normalization.json';audit='research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261012-PBPSActualPhaseNormalization.json';want='c7806ada54ca78514a75ea1d13ed4bf08e5af4e92546d9ba0165683d77b36af4'
check('reviewed_production_RAW_preserved',h(local(module))==want and resolve({'path':module,'raw_sha256':want},(S,))['PASS'] and resolve({'path':module,'raw_sha256':want},(I,))['PASS'] and blob(S,module)==blob(I,module)==public_normalize(local(module)))
for p in [lesson,pub,audit]:check('unchanged_science_publication:'+p,blob(S,p)==blob(I,p) and blob(I,p) in [local(p),public_normalize(local(p))])
ver=J(B+'/exact-commit-verification103/verified.json');ad=J(B+'/exact-commit-verification103/admission103.json');au=J(audit)
check('exact_verified_science_and_current_review_bindings',ver['verified_commit']==S and ver['status']=='PASS_INDEPENDENT_EXACT_COMMIT_VERIFICATION' and ver['verifier_id']=='/root/exact_verifier96' and au['publication_binding_sha256']==ver['publication_binding_sha256']=='349f71636e82ddb57d97fb9e228a792f1d77f13dd232decdccff39c399cce8b7' and au['source_review']['reviewer_packet_sha256']=='c11373d3e8a67a275fe8bcaa6913d30dba5b55aa102ff34e8f63706b6b8d98b4')
check('five_actual_parents_and_seven_regions_unchanged',len(ver['source_audit']['exact_five_actual_producer_parents'])==5 and ver['source_audit']['seven_exposition_regions_accepted'])
for k in ['native_verdict','native_run','closed_manifest','lesson','topology_independent_acceptance']:
 check('reused_source_binding:'+k,resolve(ver['source_audit'][k])['PASS'])
check('whole_math_binding_recoverable',resolve(ver['whole_math'])['PASS'])
cell=J(ad['cell']['path']);check('current_admission_cell',h(blob(I,ad['cell']['path']))==ad['cell']['raw_sha256'] and cell['status']=='independently_verified')
ledger=blob(I,'runs/substantive_advances.jsonl');lr=resolve(ad['ledger']);lraw=blob(lr['commit'],lr['storage']);lraw=gzip.decompress(lraw) if lr['storage'].endswith('.gz') else lraw
scienceledger=next(a for a in ar['archives'] if a['raw_path']=='runs/substantive_advances.jsonl');oldledger=gzip.decompress(blob(S,scienceledger['archive']))
events=[json.loads(x) for x in ledger.decode('utf-8-sig').splitlines() if x.strip()];eid='ASTIS-SA-20261012-PBPSActualPhaseNormalization';ev=[e for e in events if e.get('advance_id')==eid and e.get('to_state')=='VERIFIED'];latest={}
for e in events:
 if e.get('advance_id') and e.get('to_state'):latest[e['advance_id']]=e['to_state']
lanes=[k for k,v in latest.items() if v=='STABILIZING'];check('one_independent_VERIFIED_event_and_append_only_RAW_ledger',len(ev)==1 and ev[0]['worker_id']=='/root/exact_verifier96' and lr['PASS'] and lraw.startswith(oldledger),{'event_count':len(ev),'science_ledger_prefix_bytes':len(oldledger)})
check('sole94lane',lanes==['ASTIS-SA-20261011-PBPSActualPrescribedPathDensity'] and notes['sole_lane']==lanes[0],lanes)
def gitargs(*args):return subprocess.check_output(['git',*args],cwd=str(R)).decode('utf-8').strip()
check('exact_commit_chain',gitargs('show','-s','--format=%P',I)==S)
baseline=gitargs('show','-s','--format=%P',S).split()[0];changed=gitargs('diff','--name-only',baseline,I).splitlines();tree=gitargs('ls-tree','-r','--name-only',I).splitlines();bad=[p for p in changed if 'next-primary104' in p or 'preread104' in p or 'Header104' in p or 'primary-pbps.exactraw.snapshot.html' in p];future=[p for p in tree if 'next-primary104' in p or 'preread104' in p or 'Header104' in p]
def treeids(c):return {s.split('\t',1)[1]:s.split('\t',1)[0].split()[2] for s in gitargs('ls-tree','-r',c).splitlines()}
oldtree=treeids(baseline);newtree=treeids(I);hist=[p for p in tree if 'primary-pbps.exactraw.snapshot.html' in p];priorarchives=[p for p in oldtree if p.endswith('.gz')]
check('no_NEW_primary_or104_delivery',not bad and not future and all(oldtree.get(p)==newtree[p] for p in hist),{'baseline':baseline,'changed_count':len(changed),'bad':bad,'future':future,'historical_primary_paths':hist})
check('all_inherited_gzip_archives_unchanged',all(oldtree[p]==newtree.get(p) for p in priorarchives),len(priorarchives))
check('scope_manifest_files_committed',all(p in newtree for p in scope['paths']),len(scope['paths']))
before=[resolve(r) for r in J(B+'/integration103/owned-before.json')];check('explicit_before_snapshot_keys_recover',all(v['PASS'] for v in before),before)
# Independently parse generated reader section; only display bytes and folding are checked.
off=J(B+'/integration103/offline-reader103.json');page=local(off['page']);download=local(off['Lean_download']);check('generated_page_download_bound',h(page)==off['page_raw_sha256'] and h(download)==off['Lean_download_raw_sha256']==want)
class Reader(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.active=False;self.depth=0;self.codes=[];self.code=None;self.details=[];self.links=[]
 def handle_starttag(self,t,a):
  a=dict(a)
  if t=='section':
   if a.get('id')=='pbps-actual-phase-normalization':self.active=True;self.depth=1
   elif self.active:self.depth+=1
  if not self.active:return
  if t=='details':self.details.append(a)
  if t=='code':self.code=''
  if t=='a':self.links.append(a.get('href',''))
 def handle_endtag(self,t):
  if not self.active:return
  if t=='code' and self.code is not None:self.codes.append(self.code);self.code=None
  if t=='section':
   self.depth-=1
   if self.depth==0:self.active=False
 def handle_data(self,s):
  if self.active and self.code is not None:self.code+=s
reader=Reader();reader.feed(page.decode('utf-8'));u=J(lesson)['units'][0];lines=download.splitlines(keepends=True);regout=[]
for step in u['steps']:
 r=step['lean_source_region'];span=b''.join(lines[r['start_line']-1:r['end_line']]);lf=span.replace(b'\r\n',b'\n');display=step['lean'].encode();ok=lf==display and h(display)==r['exact_code_raw_sha256'] and any(c.strip()==step['lean'].strip() for c in reader.codes);regout.append({'title':step['title'],'source_CRLF_RAW':h(span),'display_LF_RAW':h(display),'PASS':ok,'region':r})
check('seven_exact_regions_LF_source_and_display',len(regout)==7 and all(v['PASS'] for v in regout),regout)
check('thirteen_details_initially_folded',len(reader.details)==13 and all('open' not in d for d in reader.details),reader.details)
source_lf=download.decode('utf-8').replace('\r\n','\n').splitlines(keepends=True)
sig=''.join(source_lf[60:69]).split(' := by',1)[0].strip()
fullproof=''.join(source_lf[60:]).strip()
check('full_signature_and_full_proof_generated',any(code.strip()==sig for code in reader.codes) and any(code.strip()==fullproof for code in reader.codes),{'signature_lines':[61,69],'signature_excludes_trailing_proof_introducer':True,'full_proof_and_module_closing_lines':[61,len(source_lf)],'signature_LF_sha256':h(sig.encode()),'fullproof_LF_sha256':h(fullproof.encode()),'lesson_lean_statement_and_lean_proof_are_prose_not_code':True})
fullprop=''.join(download.decode('utf-8').splitlines(keepends=True)[23:55]).replace('\r\n','\n');check('full_literal_proposition_generated',any(fullprop.strip()==c.strip() for c in reader.codes))
check('complete_download_link',any('ActualPhaseNormalization.lean' in x for x in reader.links))
branch=J(B+'/integration103/static-svg/branch-viewed103.json');bs=J(branch['slice']['path']);graph=local(bs['source_graph']);diag=J(B+'/integration103/scanner-boundary103.json');wm=J(ver['whole_math']['path'])
actual=set(ver['source_audit']['exact_five_actual_producer_parents']);edgeparents={x['source'][5:] for x in bs['edges']};scanned={x['source'][5:] for x in diag['scanner_edges']}
check('actual_six_node_five_parent_static_branch',all(resolve(branch[k])['PASS'] for k in ['svg','png','slice','scanner_diagnostic']) and h(graph)==bs['source_graph_RAW_sha256'] and len(bs['nodes'])==6 and len(bs['edges'])==5 and edgeparents==actual and branch['viewed_by_root'] is True and not branch['actual_browser_page_viewed'] and not branch['interactive_branch_viewed'],{'nodes':[v['id'] for v in bs['nodes']],'edges':bs['edges'],'scope':branch['scope']})
check('honest_scanner_boundary',len(scanned & actual)==2 and len(scanned-actual)==2 and set(diag['actual_public_parents'])==actual and bs['scanner_is_not_kernel_dependency_certificate'] is True and not diag['full_kernel_dependency_graph_claim'] and not diag['production_changed'] and all(e['relation']=='independently reviewed exact public producer call' for e in bs['edges']),{'scanner_hits':sorted(scanned & actual),'name_collisions':sorted(scanned-actual),'resolution':diag['resolution'],'whole_math_direct_producers':wm.get('direct_consumed_public_producers')})
check('static_public_SVG_and_PNG_exact',all(h(blob(I,branch[k]['path']))==branch[k]['raw_sha256']==h(local(branch[k]['path'])) for k in ['svg','png']))
svg=J(B+'/integration103/static-svg/viewed103.json');sr=resolve({'path':normpath(svg['output']),'raw_sha256':svg['output_raw_sha256']});check('overview_archive_only_recoverable',sr['PASS'] and blob(I,normpath(svg['output'])) is None and resolve({'path':normpath(svg['input']),'raw_sha256':svg['input_raw_sha256']})['PASS'] and svg['viewed_by_root'] is True and svg['actual_page_or_fine_branch'] is False,{'storage':sr,'scope':svg['scope']})
check('visual_and_completion_flags_honest',all(notes['state_distinctions'][k] is False for k in ['stabilized','merged','purified','live_verified','full_Exposition_Seal','main_theorem_complete']) and notes['Goal_complete'] is False and not off['actual_browser_page_viewed'] and not off['interactive_branch_viewed'] and not branch['full_Exposition_Seal'])
paths=[pathlib.Path('AutoSamplingTheory.lean'),*sorted(pathlib.Path('AutoSamplingTheory').rglob('*.lean')),pathlib.Path('Tests.lean'),*sorted(pathlib.Path('Tests').rglob('*.lean')),pathlib.Path('lakefile.lean'),pathlib.Path('lean-toolchain'),pathlib.Path('lake-manifest.json')];dg=hashlib.sha256();count=0
for p in paths:
 if p.exists():dg.update(p.as_posix().encode());dg.update(b'\0');dg.update(p.read_bytes());dg.update(b'\0');count+=1
check('current_RAW_source_digest',dg.hexdigest()==notes['source_digest'],{'actual':dg.hexdigest(),'expected':notes['source_digest'],'file_count':count,'recipe':'path NUL exact RAW NUL in tools/astis_site.py order'})
check('HEAD_still_requested_commit',gitargs('rev-parse','HEAD')==I)
report=put('storage-checks103.native.json',{'kind':'independent-immutable-storage-generated-reader103','reviewer':'/root/source_final96','science':S,'checked_integration':I,'details':details,'errors':errors,'no_mathematical_or_source_reproof':True,'remote_delivery_claim':False})
inp=put('storage-inputs103.native.json',{'kind':'exact-commit-and-working-storage-inputs103','inputs':list(reads.values())})
batch.stdin.close();batch.wait()
print(json.dumps({'checks':report,'inputs':inp,'errors':errors,'counts':{'science_inputs':len(fr['exact_commit_matches']),'science_archives':len(ar['archives']),'integration_archives':len(im['files']),'verifier_outputs':len(cl['owned_artifacts']),'collaborators':len(collab)}},indent=2))
