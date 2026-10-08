import pathlib,json,hashlib,subprocess,os,sys,re,shutil,gzip
ROOT=pathlib.Path('E:/Samplinglib');R=ROOT/'runs/20261007-companion-priority/pbps-real-complex-lift60';D=R/'exact-science-verification';M=R/'independent-math60';SCI='0a77416f5ec38702c46ec1358966b9dd4846c8d3';BASE='10d9fef15afc4c21208b6b75d8a71f51c664cfce'
os.chdir(ROOT);sys.path[:0]=[str(ROOT),str(ROOT/'tools')]
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(q):return json.dumps(q,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def load(p):return json.loads(path(p).read_bytes())
def write(p,q):path(p).write_bytes((json.dumps(q,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode())
def path(s):
 p=pathlib.Path(str(s).replace('\\','/'));return p if p.is_absolute() else ROOT/p
def pin(p):
 p=path(p);b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=p.as_posix(),bytes=len(b),lf_bytes=len(l),raw_sha256=sha(b),lf_sha256=sha(l))
def pins(q):
 if isinstance(q,dict):
  if {'path','raw_sha256','lf_sha256'}<=q.keys():yield q
  for v in q.values():yield from pins(v)
 elif isinstance(q,list):
  for v in q:yield from pins(v)
def key(row):return path(row['path']).as_posix(),row['raw_sha256'],row['lf_sha256']
def size(x):return x.get('bytes',x.get('raw_bytes',x.get('raw_byte_count')))
def match(a,b):return a['raw_sha256']==b['raw_sha256'] and a['lf_sha256']==b['lf_sha256'] and (size(a) is None or size(b) is None or size(a)==size(b)) and (a.get('lf_bytes') is None or b.get('lf_bytes') is None or a['lf_bytes']==b['lf_bytes'])
assert subprocess.check_output(['git','rev-parse','HEAD']).decode().strip()==SCI
assert subprocess.check_output(['git','rev-parse','HEAD^']).decode().strip()==BASE
maps=[];plan=load(R/'publication-plan.json')
for i,aid in enumerate(plan['audit_ids']):
 original=ROOT/'research-wiki/semantic-roundtrip/audits'/(aid+'.json')
 for stage in ['before-decoder','before-source-admission']:
  snapshot=pin(R/('audit.'+str(i)+'.'+stage+'.raw.snapshot.json'));maps.append(dict(original=dict(snapshot,path=original.as_posix()),snapshot=snapshot,reason='Exact root historical audit stage, matched only full qualified identity'))
for pair in load(R/'source-review60/input.manifest.json')['raw_LF_pairs']:
 maps.append(dict(original=pair['original'],snapshot=pair['raw_snapshot'],reason='Native reviewer exact qualified raw snapshot'))
decoder_adopt=load(R/'root.decoder60.adoption.json')
for x in decoder_adopt['historical_lease_resolution']+decoder_adopt['raw_snapshot_mappings']:
 maps.append(dict(original=x['original'],snapshot=x['exact_raw_snapshot'],reason='Native decoder neutral lease/output qualified historical map'))
seen={};used={}
def checkpin(row):
 k=key(row)
 if k in seen:return
 p=path(row['path']);a=pin(p) if p.exists() else None;route='CURRENT_EXACT'
 if a is None or not match(a,row):
  alternatives=[x for x in maps if key(x['original'])==k and match(x['original'],row)];assert alternatives,('UNMAPPED_NATIVE_INPUT',row)
  # Distinct qualified copies of identical historical bytes are corroboration,
  # not an ambiguous original. Check every full row before selecting native copy.
  for candidate in alternatives:assert match(pin(candidate['snapshot']['path']),row)
  m=next((x for x in alternatives if x['reason']=='Native reviewer exact qualified raw snapshot'),alternatives[0]);a=pin(m['snapshot']['path']);assert match(a,row);route='EXACT_QUALIFIED_RAW_SNAPSHOT';used[k]=dict(m,corroborating_exact_snapshot_paths=[path(x['snapshot']['path']).as_posix() for x in alternatives])
 assert match(a,row);seen[k]=dict(original=row,resolved=a,route=route)
freeze=load(R/'math-freeze.json');assert len(freeze['inputs'])==31
for row in freeze['inputs']:checkpin(row)
objects=[]
for folder,names in [(M,['run.json','receipt.json','lease.json','input.manifest.json','outputs.final.json','readback.json','compiler.status.json','signature-check.json','axiom-check.json','fake-closure-scan.json']), (R/'source-review60',['run.json','lease.json','native.receipt.json','input.manifest.json','named-source-review.payload.json','source.0.review.json','source.1.review.json']), (R/'anonymous-decoder',['run.json','input-lease.json','input-manifest.json','decoder-payload.json','final-readback.json','decoded0.json','decoded1.json'])]:
 for name in names:
  p=folder/name;q=load(p);objects.append(pin(p));checkpin(pin(p))
  for row in pins(q):checkpin(row)
  if name in ['outputs.final.json','run.json']:
   for row in pins(q):
    pp=path(row['path'])
    # Only actual native-owned JSON outputs, no recursive old evidence trees.
    if '/source-review60/' in pp.as_posix() and pp.suffix=='.json':
     for extra in pins(load(pp)):checkpin(extra)
for p,pfield,expected in [(M/'run.json','named_mathematics_payload_sha256','3be958e33d66b76d95b031891cf071974b3f46f0052866cd8e5030db5d419662'),(R/'source-review60/run.json','named_source_payload_sha256','4af52bdda765565a9896fe9e89b61edb1152b625a52158a433b05cb29977355a'),(R/'anonymous-decoder/run.json','payload_sha256','d3a6e3dd1faa57f0c8242e1305e36c86a1fca54024025af1a88304ab82eed4d9')]:
 q=load(p);assert sha(canon({k:v for k,v in q.items() if k!='run_sha256'}))==q['run_sha256'];assert q[pfield]==expected
assert sha(canon(load(M/'run.json')['named_mathematics_payload']))==load(M/'run.json')['named_mathematics_payload_sha256']
assert sha((R/'source-review60/named-source-review.payload.json').read_bytes())==load(R/'source-review60/run.json')['named_source_payload_sha256']
assert sha(canon(load(R/'anonymous-decoder/decoder-payload.json')['payload']))==load(R/'anonymous-decoder/run.json')['payload_sha256']
assert load(M/'lease.json')['status']=='CLOSEDLAST' and load(R/'source-review60/lease.json')['status']=='CLOSED' and load(R/'source-review60/lease.json')['closed_last']
assert load(R/'anonymous-decoder/input-lease.json')['status']=='CLOSED'
decoder=load(R/'anonymous-decoder/run.json');assert not decoder['source_text_visible'] and not decoder['source_identity_visible'] and not decoder['compiler_started']
for row in decoder['outputs']:
 p=R/'anonymous-decoder'/row['filename'];assert sha(p.read_bytes())==row['raw_sha256'];checkpin(pin(p))
source=load(R/'source-review60/run.json')
source_details=[]
for i,aid in enumerate(plan['audit_ids']):
 q=load(R/('source-review60/source.'+str(i)+'.review.json'));assert q['verdict']=='equivalent-after-elaboration' and q['repairs']==[] and q['excess_count']==0 and len(q['semantic_slots'])==7 and all(not x['blocking'] for x in q['deltas']) and q['review_run_sha256']==source['run_sha256']
 a=load(ROOT/'research-wiki/semantic-roundtrip/audits'/(aid+'.json'));source_details.append(dict(audit=pin(ROOT/'research-wiki/semantic-roundtrip/audits'/(aid+'.json')),review=pin(R/('source-review60/source.'+str(i)+'.review.json')),native_verdict=q['verdict'],native_binding=q['publication_binding_sha256'],canonical_audit=a))
for p in [R/'root.math60.adoption.json',R/'root.source60.adoption.json',R/'root.decoder60.adoption.json',R/'proved-local.json',R/'publication-plan.json']:
 checkpin(pin(p));objects.append(pin(p))
# Exact science entry bytes from one foreground cat-file batch, never shell path interpolation.
names=subprocess.check_output(['git','diff-tree','--no-commit-id','--name-only','-r','-z',SCI]).split(b'\0');names=[x.decode() for x in names if x]
oids=[SCI+':'+x for x in names];batch=subprocess.run(['git','cat-file','--batch'],input=('\n'.join(oids)+'\n').encode(),stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True);b=batch.stdout;offset=0;entries=[]
for rel in names:
 end=b.index(b'\n',offset);meta=b[offset:end].decode().split();size=int(meta[2]);body=b[end+1:end+1+size];offset=end+1+size+1
 current=pin(ROOT/rel);assert current['lf_sha256']==sha(body.replace(b'\r\n',b'\n')),('GIT_LF_MISMATCH',rel)
 entries.append(dict(path=rel,git_oid=meta[0],git_bytes=size,git_raw_sha256=sha(body),git_lf_sha256=sha(body.replace(b'\r\n',b'\n')),working=current));checkpin(current)
write(D/'science.git-pins.json',dict(checked_commit=SCI,parent=BASE,count=len(entries),entries=entries))
write(D/'historical-mappings.json',dict(mappings=maps,used_mappings=list(used.values()),used_count=len(used),rule='Full qualified original path plus original raw/LF and actual lengths; exact snapshot only, never basename fallback'))
write(D/'native-checks.json',dict(actual_reader_PID=os.getpid(),status='ALL_SCOPED_NATIVE_AND_GIT_INPUT_CHECKS_PASS',freeze_count=31,native_qualified_pin_count=len(seen),readbacks=list(seen.values()),native_object_inputs=objects,native_complete_run_self_checks=3,distinct_payload_recipes=dict(mathematics='canonical JSON named_mathematics_payload only',source='RAW complete named-source-review.payload.json bytes',decoder='canonical JSON nested payload object inside decoder-payload.json only'),current_source_audits=source_details,source_review_CLOSED=True,decoder_CLOSED=True,decoder_source_TEXT_blind=True,decoder_source_identity_blind=True,complete_unchanged_math_review=pin(M/'receipt.json'),science_entries=len(entries)))
from tools import astis_publication as pub,astis_advance as advance
pub.check_advance(freeze['mathematical_declarations'],reviewed=True)
state=advance.current_advances();assert state[freeze['advance_id']]['state']=='PROVED_LOCAL';assert [k for k,v in state.items() if v.get('state')=='STABILIZING']==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
write(D/'source-publication-gate.json',dict(status='PASS',actual_reader_PID=os.getpid(),reviewed=True,actual_API='tools.astis_publication.check_advance',declarations=freeze['mathematical_declarations'],checked_commit=SCI,current_source_audits=[x['audit'] for x in source_details],current_state='PROVED_LOCAL',sole_STABILIZING='ASTIS-SA-20261005-SPHMCImplementedPhaseKernel',helpers=[pin(ROOT/'tools/astis_publication.py'),pin(ROOT/'tools/astis_advance.py')]))
env=dict(os.environ);env.pop('ELAN_TOOLCHAIN',None);env.update(LEAN_NUM_THREADS='2',PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1');assert (ROOT/'lean-toolchain').read_text().strip()=='leanprover/lean4:v4.33.0';lake=shutil.which('lake');assert lake
before=[pin(path(x['path'])) for x in freeze['inputs']];write(D/'inputs.before-compiler.json',dict(frozen=before,count=31,freeze=pin(R/'math-freeze.json'),checked_commit=SCI,toolchain=pin(ROOT/'lean-toolchain'),lake_manifest=pin(ROOT/'lake-manifest.json'),lake=pin(path(lake)),environment=dict(ELAN_TOOLCHAIN='UNSET',LEAN_NUM_THREADS='2',PYTHONUTF8='1'),pin_timing='Actual input bytes before independent focused compiler'))
gates=[]
def run(label,command):
 with (D/(label+'.stdout.log')).open('wb') as out,(D/(label+'.stderr.log')).open('wb') as err:
  p=subprocess.Popen(command,cwd=ROOT,env=env,stdout=out,stderr=err);pid=p.pid;code=p.wait()
 q=dict(label=label,command=command,actual_PID=pid,exit_code=code,terminal_closed=True,stdout=pin(D/(label+'.stdout.log')),stderr=pin(D/(label+'.stderr.log')));write(D/(label+'.status.json'),q);gates.append(q);assert code==0,q
run('toolchain',[lake,'env','lean','--version']);assert '4.33.0' in (D/'toolchain.stdout.log').read_text()
run('focused',[lake,'build','Tests.ProximalBPSDefectComplexLift']);assert before==[pin(path(x['path'])) for x in freeze['inputs']]
log=(D/'focused.stdout.log').read_text(encoding='utf8');assert 'Build completed successfully (3915 jobs).' in log and 'sorryAx' not in log
closures=[]
for name in freeze['mathematical_declarations']+['AutoSamplingTheory.ExampleCases.ProximalBPS.CenteredDefectOperator.actual_centered_selfadjoint_defect']:
 m=re.search("'"+re.escape(name)+r"' depends on axioms: \[([^\]]+)\]",log);assert m;aa=[x.strip() for x in m.group(1).split(',')];assert set(aa)=={'propext','Classical.choice','Quot.sound'};closures.append(dict(declaration=name,actual_axioms=aa))
import astis;scans=[]
for p in [path(x['path']) for x in freeze['inputs'][:4]]:
 text=astis.strip_lean_comments_and_strings(p.read_text());hits=re.findall(r'\b(?:axiom|sorry|admit|sorryAx)\b|\bProp\s*:=\s*True\b|:=\s*(?:by\s*)?trivial\b',text);assert not hits;scans.append(dict(source=pin(p),authored_hits=hits,comments_strings_removed=True))
write(D/'fake-closure-axioms.json',dict(scans=scans,count=4,authored_fake_closures=0,actual_named_standard3_closures=closures,anonymous_Test='Complete compiled anonymous consumer; no fabricated named axiom print',focused_jobs=3915,invocation_count=1,forced_rebuild=False,post_compiler_frozen=before))
run('publication',[sys.executable,'-B','-X','utf8','tools/astis_publication.py','check','--base',BASE])
run('semantic',[sys.executable,'-B','-X','utf8','tools/astis_semantic_roundtrip.py','check'])
run('frontier',[sys.executable,'-B','-X','utf8','tools/astis_frontier_cells.py','check'])
run('contributor',[sys.executable,'-B','-X','utf8','tools/astis_contributor_contract.py','check','--base',BASE])
write(D/'gates.json',dict(actual=gates,count=len(gates),shared_aggregate='NOT_RUN_DEFERRED_TO_ROOT_SERIALIZED_INTEGRATION'))
print(json.dumps(dict(status='EXACT_SCIENCE_GATES_PASS_BEFORE_TRANSITION',actual_PID=os.getpid(),checked_commit=SCI,science_entries=len(entries),native_pin_count=len(seen),historical_maps_used=len(used),compiler_PID=next(x['actual_PID'] for x in gates if x['label']=='focused'))),flush=True)
