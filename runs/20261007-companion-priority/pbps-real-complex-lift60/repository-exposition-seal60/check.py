import pathlib,json,hashlib,subprocess,os,sys,re,gzip,struct
ROOT=pathlib.Path('E:/Samplinglib'); R=ROOT/'runs/20261007-companion-priority/pbps-real-complex-lift60'; D=R/'repository-exposition-seal60'
SCI='0a77416f5ec38702c46ec1358966b9dd4846c8d3'; INT='63c74351566095343985d36dfcb13dca32a666b7'
os.chdir(ROOT);sys.dont_write_bytecode=True;sys.path[:0]=[str(ROOT/'tools'),str(ROOT/'website/scripts'),str(ROOT)]
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(q):return json.dumps(q,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def path(s):
 p=pathlib.Path(str(s).replace('\\','/'));return p if p.is_absolute() else ROOT/p
def load(p):return json.loads(path(p).read_bytes())
def write(p,q):path(p).write_bytes((json.dumps(q,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode())
def pin(p):
 p=path(p);b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=p.as_posix(),bytes=len(b),lf_bytes=len(l),raw_sha256=sha(b),lf_sha256=sha(l))
def rows(q):
 if isinstance(q,dict):
  if {'path','raw_sha256','lf_sha256'}<=q.keys():yield q
  for v in q.values():yield from rows(v)
 elif isinstance(q,list):
  for v in q:yield from rows(v)
def key(q):return path(q['path']).as_posix(),q['raw_sha256'],q['lf_sha256']
def match(a,b):
 return a['raw_sha256']==b['raw_sha256'] and a['lf_sha256']==b['lf_sha256'] and all(a.get(k) is None or b.get(k) is None or a[k]==b[k] for k in ['bytes','lf_bytes'])
def git(rel,commit=SCI):return subprocess.check_output(['git','show',commit+':'+rel],cwd=ROOT)
assert subprocess.check_output(['git','rev-parse','HEAD']).decode().strip()==INT
assert subprocess.check_output(['git','rev-parse','HEAD^']).decode().strip()==SCI
maps=[];seen={};used={};selfchecks=[]
for x in load(R/'exact-science-verification/historical-mappings.json')['mappings']:
 maps.append(dict(original=x['original'],snapshot=x['snapshot'],reason=x['reason']))
for x in load(R/'exact-science-verification/before-admin-mappings.json')['mappings']:
 maps.append(dict(original=x['original'],snapshot=x['exact_snapshot'],reason=x['reason']))
notes=load(R/'integration.notes.json')
for x in notes['cell_administration_updates']:
 maps.append(dict(original=x['before'],snapshot=x['before'],reason='Exact independently verified post-science before-aggregate cell snapshot'))
 # The original path is the canonical after path, with precisely the before bytes.
 maps[-1]['original']=dict(x['before'],path=x['after']['path'])
def checkpin(row):
 k=key(row)
 if k in seen:return
 p=path(row['path']);actual=pin(p) if p.exists() else None;route='CURRENT_EXACT'
 if actual is None or not match(row,actual):
  choices=[x for x in maps if key(x['original'])==k and match(x['original'],row)]
  assert choices,('UNMAPPED_QUALIFIED_PIN',row)
  for x in choices:assert match(pin(x['snapshot']['path']),row),('WRONG_HISTORICAL_SNAPSHOT',x)
  x=choices[0];actual=pin(x['snapshot']['path']);route='EXACT_HISTORICAL_SNAPSHOT';used[k]=x
 assert match(actual,row)
 seen[k]=dict(original=row,resolved=actual,route=route)
for row in load(D/'inputs.open.json')['artifacts']:checkpin(row)
freeze=load(R/'math-freeze.json');assert len(freeze['inputs'])==31
for row in freeze['inputs']:checkpin(row)
groups={
 'independent-math60':['run.json','receipt.json','lease.json','input.manifest.json','outputs.final.json','readback.json','compiler.status.json','signature-check.json','axiom-check.json','fake-closure-scan.json'],
 'source-review60':['run.json','lease.json','native.receipt.json','input.manifest.json','named-source-review.payload.json','source.0.review.json','source.1.review.json'],
 'anonymous-decoder':['run.json','input-lease.json','input-manifest.json','decoder-payload.json','final-readback.json','decoded0.json','decoded1.json'],
 'exact-science-verification':['run.json','receipt.json','lease.json','input.manifest.json','outputs.final.json','readback.json','gates.json','fake-closure-axioms.json','historical-mappings.json','before-admin-mappings.json']}
for folder,names in groups.items():
 for name in names:
  p=R/folder/name;q=load(p);checkpin(pin(p))
  for row in rows(q):checkpin(row)
  # Bounded source-owned JSON output rows, never recurse into earlier cycles.
  if name in ['run.json','outputs.final.json']:
   for row in rows(q):
    pp=path(row['path'])
    if '/source-review60/' in pp.as_posix() and pp.suffix=='.json':
     for extra in rows(load(pp)):checkpin(extra)
 forun=load(R/folder/'run.json');assert sha(canon({k:v for k,v in forun.items() if k!='run_sha256'}))==forun['run_sha256'];selfchecks.append(dict(path=pin(R/folder/'run.json'),whole_run_sha256=forun['run_sha256'],recipe='complete sorted compact UTF8 object excluding ONLY run_sha256'))
math=load(R/'independent-math60/run.json');source=load(R/'source-review60/run.json');dec=load(R/'anonymous-decoder/run.json');exact=load(R/'exact-science-verification/run.json')
assert sha(canon(math['named_mathematics_payload']))==math['named_mathematics_payload_sha256']
assert sha((R/'source-review60/named-source-review.payload.json').read_bytes())==source['named_source_payload_sha256']
assert sha(canon(load(R/'anonymous-decoder/decoder-payload.json')['payload']))==dec['payload_sha256']
assert sha(canon(exact['named_exact_verification_payload']))==exact['named_exact_verification_payload_sha256']
assert load(R/'independent-math60/lease.json')['status']=='CLOSEDLAST'
assert load(R/'source-review60/lease.json')['status']=='CLOSED' and load(R/'source-review60/lease.json')['closed_last']
assert load(R/'anonymous-decoder/input-lease.json')['status']=='CLOSED'
for folder in ['independent-math60','exact-science-verification']:
 for fn,field in [('lease.json','lease_sha256'),('outputs.final.json','outputs_sha256')]:
  q=load(R/folder/fn);assert sha(canon({k:v for k,v in q.items() if k!=field}))==q[field];selfchecks.append(dict(path=pin(R/folder/fn),self_digest=q[field],excluded_only=field))
exlease=load(R/'exact-science-verification/lease.json');assert exlease['status']=='CLOSEDLAST'
assert sha(canon({k:v for k,v in exlease.items() if k!='lease_sha256'}))==exlease['lease_sha256']
assert exact['checked_commit']==SCI and not dec['source_text_visible'] and not dec['source_identity_visible'] and not dec['compiler_started']
for i in range(2):
 q=load(R/('source-review60/source.'+str(i)+'.review.json'));assert q['verdict']=='equivalent-after-elaboration' and q['repairs']==[] and len(q['semantic_slots'])==7 and q['excess_count']==0 and all(not x['blocking'] for x in q['deltas'])
for n in ['root.math60.adoption.json','root.decoder60.adoption.json','root.source60.adoption.json','root.exact-verification60.adoption.json','commit-observer-split.json','publication-plan.json']:
 checkpin(pin(R/n))
 for row in rows(load(R/n)):checkpin(row)
# Exact integration entry blobs: qualified index snapshots; source-only61 is opaque.
names=[x.decode() for x in subprocess.check_output(['git','diff-tree','--no-commit-id','--name-only','-r','-z',INT]).split(b'\0') if x]
batch=subprocess.run(['git','cat-file','--batch'],input=('\n'.join(INT+':'+x for x in names)+'\n').encode(),stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True);b=batch.stdout;off=0;entries=[]
(D/'git-inputs').mkdir(exist_ok=True)
for i,rel in enumerate(names):
 end=b.index(b'\n',off);meta=b[off:end].decode().split();size=int(meta[2]);body=b[end+1:end+1+size];off=end+size+2
 cur=pin(ROOT/rel);assert cur['lf_sha256']==sha(body.replace(b'\r\n',b'\n')),('INTEGRATION_GIT_CURRENT_MISMATCH',rel)
 snap=D/'git-inputs'/(str(i).zfill(4)+'-'+sha(rel.encode())+'.raw.snapshot');snap.write_bytes(body)
 entries.append(dict(original_path=rel,git_oid=meta[0],git_bytes=size,git_raw_sha256=sha(body),git_lf_sha256=sha(body.replace(b'\r\n',b'\n')),exact_git_snapshot=pin(snap),current=cur,semantic_scope='OPAQUE_SOURCE_ONLY61_NO_PROOF_CREDIT' if 'source61/' in rel else 'INTEGRATION60_SCOPED'))
 checkpin(cur)
write(D/'integration.git-pins.json',dict(checked_commit=INT,parent=SCI,count=len(entries),all_current_LF_equal=True,entries=entries))
observer=load(R/'commit-observer-split.json');checkpin(observer['exact_science_snapshot']);checkpin(observer['final_closed_observer']);checkpin(observer['current_checkout'])
# Frozen math and source/publication/lesson bytes remain exactly SCI blobs.
plan=load(R/'publication-plan.json');unchanged=[]
for row in freeze['inputs'][:3]:
 p=path(row['path']);rel=p.relative_to(ROOT).as_posix();assert git(rel).replace(b'\r\n',b'\n')==p.read_bytes().replace(b'\r\n',b'\n');unchanged.append(pin(p))
for folder in ['publications','declaration_lessons']:
 for slug in plan['slugs']:
  p=ROOT/'website/content'/folder/(slug+'.json');checkpin(pin(p));assert git(p.relative_to(ROOT).as_posix()).replace(b'\r\n',b'\n')==p.read_bytes().replace(b'\r\n',b'\n');unchanged.append(pin(p))
for aid in plan['audit_ids']:
 p=ROOT/'research-wiki/semantic-roundtrip/audits'/(aid+'.json');checkpin(pin(p));assert git(p.relative_to(ROOT).as_posix()).replace(b'\r\n',b'\n')==p.read_bytes().replace(b'\r\n',b'\n');unchanged.append(pin(p))
shared=['AutoSamplingTheory/ExampleCases.lean','AutoSamplingTheory/TechnicalLemmas.lean','AutoSamplingTheory/TechnicalLemmas/Registry.lean','Tests.lean','Tests/Basic.lean']
diff=subprocess.check_output(['git','diff',SCI,INT,'--']+shared).decode();(D/'shared.Lean.diff.raw.txt').write_bytes(diff.encode())
assert 'DefectComplexLift' in (ROOT/shared[0]).read_text() and 'L2RealComplexOperator' in (ROOT/shared[1]).read_text() and 'Tests.ProximalBPSDefectComplexLift' in (ROOT/'Tests.lean').read_text()
for rel in shared[:2]:assert not re.search(r'^(?:theorem|lemma|def|axiom)\b',(ROOT/rel).read_text(),re.M)
assert '503' in (ROOT/'Tests/Basic.lean').read_text()
import astis,astis_publication as pub,astis_advance as advance
scans=[]
for row in freeze['inputs'][:4]:
 p=path(row['path']);text=astis.strip_lean_comments_and_strings(p.read_text());hits=re.findall(r'\b(?:axiom|sorry|admit|sorryAx)\b|\bProp\s*:=\s*True\b|:=\s*(?:by\s*)?trivial\b',text);assert not hits
 assert not re.search(r'^import Tests(?:\.|$)',text,re.M);scans.append(dict(source=pin(p),fake_hits=hits,production_Test_import=False))
pub.check_advance(freeze['mathematical_declarations'],reviewed=True)
state=advance.current_advances();assert state[freeze['advance_id']]['state']=='VERIFIED';assert [k for k,v in state.items() if v.get('state')=='STABILIZING']==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
admin=[]
def differences(a,b,p=''):
 if isinstance(a,dict) and isinstance(b,dict):
  out=[]
  for k in sorted(set(a)|set(b)):
   out+=differences(a.get(k,'__ABSENT__'),b.get(k,'__ABSENT__'),p+'/'+k)
  return out
 return [] if a==b else [dict(pointer=p,before=a,after=b)]
for x in notes['cell_administration_updates']:
 before=load(x['before']['path']);after=load(x['after']['path']);checkpin(x['before']);checkpin(x['after']);assert after['status']=='independently_verified'
 admin.append(dict(before=x['before'],after=x['after'],exact_deltas=differences(before,after)))
gate_records=[]
for x in notes['checks']+notes['final_administrative_gate_receipts']:
 if isinstance(x,str):x=dict(receipt=pin(x),label=path(x).parent.name)
 rr=x['receipt'] if 'receipt' in x else x
 if isinstance(rr,str):rr=pin(rr)
 checkpin(rr);q=load(rr['path']);assert q['exit_code']==0 and q['terminal_closed'] and q['actual_foreground_pid']>0
 for row in [q['stdout'],q['stderr']]:checkpin(row)
 gate_records.append(dict(label=x.get('label',path(rr['path']).parent.name),receipt=rr,actual_PID=q['actual_foreground_pid'],exit_code=q['exit_code'],terminal_closed=q['terminal_closed'],stdout=q['stdout'],stderr=q['stderr']))
assert notes['root_jobs']==9165 and notes['test_jobs']==9457 and notes['registry_count']==503
log=path(next(x['stdout']['path'] for x in gate_records if x['label']=='mandatory-astis-check')).read_text()
assert '9165 jobs' in log and '9457 jobs' in log and 'ASTIS check passed' in log and 'sorryAx' not in log
closures=[]
for name in freeze['mathematical_declarations']:
 m=re.search("'"+re.escape(name)+r"' depends on axioms: \[([^\]]+)\]",log);assert m;ax=[x.strip() for x in m.group(1).split(',')];assert set(ax)=={'propext','Classical.choice','Quot.sound'};closures.append(dict(declaration=name,actual_axioms=ax))
# Current 511 actual module inventory, 80 exact restored files, 63 retained metadata.
inventory=load(ROOT/'research-wiki/retrieval-index/astis-lean-arsenal-module-graph.json');actual=astis.lean_module_records();assert len(actual)==511
indexed={x['module']:x for x in inventory['modules']}
for x in actual:
 q=indexed[x['module']]
 for k in ['path','imports','local_imports','declarations','exports']:assert q[k]==x[k],(x['module'],k)
pres=load(R/'integration60/generated-context-preservation/manifest.json');restored=[]
for x in pres['emitted_snapshots']:
 checkpin(pin(x['emitted_snapshot']));assert sha(gzip.decompress(path(x['emitted_snapshot']).read_bytes()))==x['emitted_raw_sha256']
 if x['action']=='restored root-generated unrelated changes to exact HEAD bytes':
  assert sha(git(x['path']))==x['baseline_raw_sha256'];assert (ROOT/x['path']).read_bytes()==git(x['path']);restored.append(x['path']);checkpin(pin(ROOT/x['path']))
assert len(restored)==80 and len(pres['preserved_canonical_metadata'])==63
for x in pres['preserved_canonical_metadata']:
 assert sha(git(x['canonical_card']))==x['card_raw_sha256'];assert (ROOT/x['canonical_card']).read_bytes()==git(x['canonical_card'])
 for k,v in x['metadata'].items():assert indexed[x['module']][k]==v,(x['module'],k)
cache=load(R/'integration60/generated-card-cache.json');checkpin(pin(R/'integration60/generated-card-cache.json'))
# Native full graph digest, not a target projection substituted for full recipe.
import publication_reader,astis_site
gp=ROOT/'_site/data/underlying-lean-graph.json';checkpin(pin(gp));graph=load(gp);digest=publication_reader.graph_input_digest();assert graph['publication_inputs_sha256']==digest
helpers=[pin(ROOT/'website/scripts/publication_reader.py'),pin(ROOT/'tools/astis_publication.py'),pin(ROOT/'tools/astis_site.py')]
selection=b''.join((ROOT/'website/scripts/publication_reader.py').read_bytes().splitlines(keepends=True)[182:187]);(D/'graph-input-digest.selected.exactbytes.txt').write_bytes(selection)
branches=[]
for name in freeze['mathematical_declarations']:
 ident='decl:'+name;n=next(x for x in graph['nodes'] if x['id']==ident);edges=[x for x in graph['edges'] if x['source']==ident or x['target']==ident];assert n['status']=='compiled';branches.append(dict(node=n,incident_edges=edges,count=len(edges)))
# Actual viewed root images + DOM, no new browser or implied physical-device test.
visual=load(R/'visual.inspection.json');cap=load(R/'integration60/visual60/capture.json');assert visual['viewed_by_root'] and len(cap['records'])==8 and cap['ownedBrowserExit']=={'code':0,'signal':None}
images=[]
for stem in ['producer','producer-proof','producer-proof-late','consumer','consumer-proof','consumer-proof-late','branch-producer','branch-consumer']:
 p=R/'integration60/visual60'/(stem+'.png');bp=p.read_bytes();assert bp[:8]==b'\x89PNG\r\n\x1a\n';w,h=struct.unpack('>II',bp[16:24]);assert (w,h)==(1440,1800);checkpin(pin(p));images.append(dict(input=pin(p),width=w,height=h,independently_viewed=True))
staged=load(R/'integration60/staging-whitespace/diagnosis.json');tracked=load(R/'integration60/tracked-whitespace-preserved/diagnosis.json');assert staged['full_staged_exit']==2 and not staged['full_staged_called_PASS'] and staged['authored_complement_exit']==0 and staged['no_folder_exclusion']
negative=R/'integration60/staging-whitespace/full-staged-immutable-negative.raw.gz';assert sha(gzip.decompress(negative.read_bytes()))==staged['negative_raw_sha256'];assert struct.unpack('<I',negative.read_bytes()[4:8])[0]==0
assert tracked['full_tracked_exit']==0 and tracked['full_tracked_called_PASS']
write(D/'historical-mappings.json',dict(rule='Exact qualified original path + raw/LF/lengths only; no basename or folder exceptions',available=maps,used=list(used.values()),used_count=len(used)))
write(D/'input.manifest.json',dict(opening_count=60,opening_pins=load(D/'inputs.open.json')['artifacts'],qualified_count=len(seen),artifacts=list(seen.values()),freeze31_verified_before_and_after=True))
write(D/'checks.json',dict(status='PASS',actual_PID=os.getpid(),science=SCI,integration=INT,git_entries=len(entries),native_pin_count=len(seen),native_whole_run_checks=selfchecks,distinct_payload_recipes={'math':'canonical named_mathematics_payload','source':'RAW whole named-source-review.payload.json','decoder':'canonical nested payload','exact':'canonical named_exact_verification_payload'},source='unchanged accepted 2 seven-slot reviews; no repairs/blockers',decoder='source text and identity blind, separate native',math_frozen=31,private_providers=26,unchanged_science=unchanged,shared_diff=pin(D/'shared.Lean.diff.raw.txt'),cell_admin_deltas=admin,gates=gate_records,actual_gate_count=len(gate_records),root_jobs=9165,test_jobs=9457,registry=503,fake_scans=scans,closures=closures,inventory={'actual_modules':511,'restored_unrelated':len(restored),'preserved_canonical_metadata':63,'cache':cache},graph={'full_native_digest':digest,'helpers':helpers,'selected_helper_bytes':pin(D/'graph-input-digest.selected.exactbytes.txt'),'branches':branches,'edge_scope':'module/import ownership and incomplete scanned/source-reference relations; not certified theorem implications'},visual={'images':images,'capture':pin(R/'integration60/visual60/capture.json'),'capture_PID':cap['pid'],'ownedBrowserExit':cap['ownedBrowserExit'],'independent_observations':'8 actual images viewed; 5 generic +3 actual formula steps, exact folded Lean; explicit no Gamma/root-descent claims','debts':'Dense duplicate statement/assumption blocks, long labels and tall graph; scoped readability accepted, no whole-reader/purification'},whitespace={'staged_findings':len(staged['findings']) if isinstance(staged['findings'],list) else staged['findings'],'immutable_paths':len(staged['exact_immutable_raw_paths']),'full_staged_PASS':False,'authored_complement_PASS':True,'full_tracked_PASS':True,'negative_gzip':pin(negative)},compiler='NOT_STARTED_THIS_REVIEW_REUSE_ACTUAL_CLOSED_FOCUSED_AND_MANDATORY',remote='pending integrationCI separate from local seal'))
for row in freeze['inputs']:assert match(row,pin(row['path']))
for row in load(D/'inputs.open.json')['artifacts']:assert match(row,pin(row['path']))
print(json.dumps(dict(status='SCOPED_REPOSITORY_EXPOSITION_CHECKS_PASS',actual_PID=os.getpid(),science=SCI,integration=INT,native_pins=len(seen),git_entries=len(entries),historical_resolutions=len(used),terminal_records=len(gate_records),graph_digest=digest)),flush=True)
