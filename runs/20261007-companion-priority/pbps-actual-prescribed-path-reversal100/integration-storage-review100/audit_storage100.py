
import json,hashlib,gzip,subprocess,datetime,re,html
from pathlib import Path
S='d9850090b15210e29ecd9b932f02c358d2c9e786'
I='8354a8eb43bc8ec8a757efd60771f31e36c106ab'
B='runs/20261007-companion-priority/pbps-actual-prescribed-path-reversal100'
O=Path(B)/'integration-storage-review100'
def h(b):return hashlib.sha256(b).hexdigest()
def normpath(p):return p.replace('\\','/').removeprefix('E:/Samplinglib/') if hasattr(str,'removeprefix') else p.replace('\\','/').replace('E:/Samplinglib/','')
cache={}
reads={}
def blob(c,p):
 p=normpath(p);k=(c,p)
 if k not in cache:
  q=subprocess.run(['git','show',c+':'+p],stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
  cache[k]=q.stdout if q.returncode==0 else None
 if cache[k] is not None:reads[c+':'+p]={'commit':c,'path':p,'raw_sha256':h(cache[k]),'bytes':len(cache[k])}
 return cache[k]
def J(p,c=I):return json.loads(blob(c,p).decode('utf-8-sig'))
def local(p):
 b=Path(p).read_bytes();reads['working:'+p]={'path':p,'raw_sha256':h(b),'bytes':len(b),'storage':'working tree'};return b
def put(n,d):
 p=O/n
 assert not p.exists(),p
 p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 return {'path':p.as_posix(),'raw_sha256':h(p.read_bytes()),'bytes':p.stat().st_size}
notes=J(B+'/integration.notes.json')
fr=J(B+'/exact-commit-verification100/input-freeze100.json')
ar=J(B+'/exact-commit-verification100/archive-audit100.json')
cl=J(B+'/exact-commit-verification100/closed-RAW-manifest100.json')
im=J(B+'/integration100/immutable-integration-RAW-archives100.json')
archives=ar['archives']+im['files']
index={}
for a in archives:index.setdefault((a['raw_path'],a['raw_sha256']),[]).append(a)
details={};errors=[]
def check(name,condition,evidence=None):
 details[name]={'PASS':bool(condition),'evidence':evidence}
 if not condition:errors.append(name)
def resolve(r,commits=(I,S)):
 rr=r.get('reference',r);p=rr.get('path',rr.get('raw_path'));want=rr.get('raw_sha256')
 candidates=[]
 for key in ['snapshot','archive']:
  if r.get(key):candidates.append((normpath(r[key]),key))
 for a in index.get((p,want),[]):candidates.append((a['archive'],'indexed archive'))
 candidates.append((p,'direct'))
 for c in commits:
  for q,method in candidates:
   if not q:continue
   b=blob(c,q)
   if b is None:continue
   try:d=gzip.decompress(b) if q.endswith('.gz') else b
   except Exception:continue
   if h(d)==want:return {'path':p,'raw_sha256':want,'storage':q,'commit':c,'method':method,'PASS':True}
 return {'path':p,'raw_sha256':want,'PASS':False}
def archcheck(a,c):
 z=blob(c,a['archive']);zh=a.get('archive_raw_sha256',a.get('archive_sha256'))
 if z is None:return {'archive':a['archive'],'commit':c,'PASS':False,'reason':'archive absent'}
 d=gzip.decompress(z);passed=h(z)==zh and h(d)==a['raw_sha256']
 public=a.get('public_text_raw_sha256',a.get('public_text_sha256'))
 rec={'archive':a['archive'],'commit':c,'archive_hash_matches':h(z)==zh,'decompressed_RAW_matches':h(d)==a['raw_sha256'],'PASS':passed}
 if public:
  b=blob(c,a['raw_path'])
  crlf=d.replace(b'\r\n',b'\n')
  trim=b'\n'.join(x.rstrip(b' \t') for x in crlf.split(b'\n')).rstrip(b'\n')+b'\n'
  ok=b is not None and h(b)==public and b in [d,crlf,trim]
  rec.update(public_hash_matches=b is not None and h(b)==public,public_only_CRLF_line_trailing_space_and_terminal_blank_normalization=ok)
  rec['PASS']=rec['PASS'] and ok
 return rec
details['integration_archives']=[archcheck(a,I)for a in im['files']]
details['science_archives']=[archcheck(a,c)for a in ar['archives']for c in [S,I]]
check('all_integration_archives_lossless',all(x['PASS']for x in details['integration_archives']),len(im['files']))
check('all_science_archives_preserved_in_both_commits',all(x['PASS']for x in details['science_archives']),len(ar['archives']))
details['frozen_science_inputs']=[resolve(r)for r in fr['exact_commit_matches']]
details['historical_snapshots']=[resolve(r)for r in fr['historical_reference_resolutions']]
details['exact_verifier_artifacts']=[resolve(r)for r in cl['owned_artifacts']]
for key in ['frozen_science_inputs','historical_snapshots','exact_verifier_artifacts']:
 check('all_'+key,all(r['PASS']for r in details[key]),len(details[key]))
details['collaborator_RAWs']=[dict(r,PASS=h(local(r['path']))==r['raw_sha256'])for r in fr['preserved_collaborator_inputs']]
details['excluded_pinned_inputs']=[dict(r,PASS=h(local(r['path']))==r['raw_sha256'])for r in fr['local_pinned_or_excluded_inputs']]
check('all21_collaborator_RAWs_preserved',len(details['collaborator_RAWs'])==21 and all(r['PASS']for r in details['collaborator_RAWs']))
check('local_pinned_inputs_match',all(r['PASS']for r in details['excluded_pinned_inputs']))
gates=[]
for gate in notes['checks']:
 refs=[resolve(gate[k])for k in ['receipt','stdout','stderr']]
 rc=J(gate['receipt']['path'])
 gates.append({'label':gate['label'],'receipt':rc,'references':refs,'PASS':all(r['PASS']for r in refs) and rc.get('exit_code')==0 and rc.get('terminal_closed') is True})
details['gates']=gates
check('all15_linked_gates_closed_pass',len(gates)==15 and all(g['PASS']for g in gates))
module='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPrescribedPathReversal.lean'
lesson='website/content/declaration_lessons/pbps-actual-prescribed-path-reversal.json'
pub='website/content/publications/pbps-actual-prescribed-path-reversal.json'
audit='research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261012-PBPSActualPrescribedPathReversal.json'
want='59d3131209605d2df34e74abb098f42d41338ae44f7e4f4bee4d75ac7bc0a3c8'
check('production_exact_RAW_unchanged',h(blob(S,module))==want and blob(S,module)==blob(I,module)==local(module))
for p in [lesson,pub,audit]:
 check('science_integration_unchanged:'+p,blob(S,p)==blob(I,p)==local(p))
ver=J(B+'/exact-commit-verification100/verified.json')
check('independent_exact_science',ver['verified_commit']==S and ver['status']=='PASS_INDEPENDENT_EXACT_COMMIT_VERIFICATION' and ver['verifier_id']=='/root/exact_verifier96')
check('five_parents_and_six_regions_unchanged',len(ver['source_audit']['exact_five_actual_producer_parents'])==5 and ver['source_audit']['six_exposition_regions_accepted'] is True and blob(S,lesson)==blob(I,lesson))
ad=J(B+'/exact-commit-verification100/admission100.json')
cell=J(ad['cell']['path'])
check('current_metadata_cell_binding',h(blob(I,ad['cell']['path']))==ad['cell']['raw_sha256'] and cell['status']=='independently_verified')
ledger=blob(I,'runs/substantive_advances.jsonl')
original=gzip.decompress(blob(I,'runs/substantive_advances.jsonl.science100.raw.gz'))
integrationledger=[a for a in im['files']if a['raw_path']=='runs/substantive_advances.jsonl']
ledgerraw=gzip.decompress(blob(I,integrationledger[0]['archive'])) if integrationledger else ledger
events=[json.loads(x)for x in ledger.decode('utf-8-sig').splitlines()if x.strip()]
eid='ASTIS-SA-20261012-PBPSActualPrescribedPathReversal'
ev=[e for e in events if e.get('advance_id')==eid and e.get('to_state')=='VERIFIED']
latest={}
for e in events:
 if e.get('advance_id') and e.get('to_state'):latest[e['advance_id']]=e['to_state']
lanes=[k for k,v in latest.items()if v=='STABILIZING']
check('one_VERIFIED_event_and_preserved_ledger_prefix',len(ev)==1 and ev[0]['worker_id']=='/root/exact_verifier96' and ledgerraw.startswith(original) and h(ledgerraw)==ad['ledger']['raw_sha256'],{'event_count':len(ev),'lanes':lanes})
check('sole94lane',lanes==['ASTIS-SA-20261011-PBPSActualPrescribedPathDensity'],lanes)
parent=subprocess.check_output(['git','show','-s','--format=%P',I]).decode().strip()
check('integration_direct_child_of_science',parent==S)
baseline=subprocess.check_output(['git','show','-s','--format=%P',S]).decode().split()[0]
changed=subprocess.check_output(['git','diff','--name-only',baseline,I]).decode().splitlines()
tree=subprocess.check_output(['git','ls-tree','-r','--name-only',I]).decode().splitlines()
bad=[p for p in changed if 'next-primary101' in p or 'primary-pbps.exactraw.snapshot.html' in p]
wholehistorical=[p for p in tree if 'primary-pbps.exactraw.snapshot.html' in p]
details['scope']={'baseline':baseline,'changed_paths_count':len(changed),'new_or_changed_future101_or_primary':bad,'historical_primary_paths':wholehistorical,'historical_unmodified':all(blob(baseline,p)==blob(I,p) for p in wholehistorical),'next_primary101_in_tree':[p for p in tree if 'next-primary101' in p]}
check('no_new_full_primary_or101_in100_span',not bad and details['scope']['historical_unmodified'] and not details['scope']['next_primary101_in_tree'])
before=J(B+'/integration100/owned-before.json')
details['before_snapshots']=[resolve(r)for r in before]
check('explicit_snapshot_keys_resolve',all(r['PASS']for r in details['before_snapshots']),len(before))
off=J(B+'/integration100/offline-reader100.json')
page=local(off['page']);download=local(off['Lean_download'])
check('generated_page_and_download_hashes',h(page)==off['page_raw_sha256'] and h(download)==off['Lean_download_raw_sha256']==want)
check('six_generated_regions_report_and_bound_lesson',off['exact_step_Lean_regions']==6 and off['details_initially_folded']==12 and off['actual_browser_page_viewed'] is False and off['interactive_branch_viewed'] is False)
svg=J(B+'/integration100/static-svg/viewed100.json')
png=blob(I,svg['output']) or local(svg['output'])
check('scoped_SVG_evidence_only',h(blob(I,svg['input']))==svg['input_raw_sha256'] and h(png)==svg['output_raw_sha256'] and svg['viewed_by_root'] is True and svg['actual_page_or_fine_branch'] is False,svg)
check('delivery_flags_separate',all(notes['state_distinctions'][k] is False for k in ['stabilized','merged','purified','live_verified','full_Exposition_Seal','main_theorem_complete']) and notes['Goal_complete'] is False)
details['remote_state']='Parent reports not pushed; no remote publication or main merge claimed by this audit.'
r=put('storage-checks100.native.json',{'kind':'bounded-independent-storage-checks100','science':S,'integration':I,'details':details,'errors':errors,'diagnostic_read_failures':[{'stage':'preaudit inspection','error':'Python default GBK read failed on Unicode lesson; corrected to explicit UTF-8 before audit. No data mutation or mathematical finding.'}]})
rr=put('storage-inputs100.native.json',{'kind':'exact-commit-and-working-storage-inputs100','inputs':list(reads.values())})
print(json.dumps({'checks':r,'inputs':rr,'errors':errors,'counts':{'science_inputs':len(fr['exact_commit_matches']),'verifier_outputs':len(cl['owned_artifacts']),'science_archives':len(ar['archives']),'integration_archives':len(im['files'])}}))
