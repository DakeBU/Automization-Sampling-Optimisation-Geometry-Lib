from pathlib import Path
import ast, builtins, gzip, hashlib, json, os, re, subprocess, sys, time
from datetime import datetime, timezone

ROOT=Path('E:/Samplinglib')
R=ROOT/'runs/20261007-companion-priority/pbps-actual-corrector-change71'
OWN=R/'exact-science-verification71'
PY='C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
SCI='4e7ce5d2996ffe1d1b0ab570778e02425c6be34e'
BASE='d8342abe2747438af6738b03a06224c85bad08b3'
ACTOR='/root/exact_science63'
SAU='ASTIS-SA-20261010-PBPSActualCorrectorChange'
DECL='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualCorrectorChange.actual_corrector_change'
CODE='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualCorrectorChange.lean'
PARENT='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualProjectedRotation.lean'
CELL='research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-corrector-change.json'
AUDIT='research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSActualCorrectorChange.json'
PUB='website/content/publications/pbps-actual-corrector-change.json'
LESSON='website/content/declaration_lessons/pbps-actual-corrector-change.json'
CODE_SHA='f321d13c612a3702e3d42043a49fff8feb3b76bb302638a60f9dad4cb166ad1a'
PACKET='2c513c4f2660ad96817f683e072f1e7d56ddd0aa400da9bc82c51488ee0e59a8'
BIND='c1b90bd0a303ab6da562aac5f51e8c2d56b6a1f2cf89165b87cd79024dfada24'
def now():return datetime.now(timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(d):return json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def load(p):return json.loads(Path(p).read_bytes())
def rel(p):
 p=Path(p);return p.relative_to(ROOT).as_posix() if p.is_absolute() else p.as_posix()
def absolute(p):
 p=Path(str(p).replace('\\','/'));return p if p.is_absolute() else ROOT/p
def pin(p):
 p=absolute(p);b=p.read_bytes();lf=b.replace(b'\r\n',b'\n')
 return dict(path=rel(p),RAW_bytes=len(b),RAW_sha256=sha(b),LF_bytes=len(lf),LF_sha256=sha(lf))
def save(n,d):
 assert not (OWN/'lease.final.json').exists(),'CLOSED_LAST'
 p=OWN/n;p.parent.mkdir(parents=True,exist_ok=True)
 p.write_bytes(d if isinstance(d,bytes) else json.dumps(d,ensure_ascii=False,sort_keys=True,indent=2).encode()+b'\n')
 return pin(p)
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
def oid(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def tree(paths):
 out=b''.join(git('ls-tree','-r','-z',SCI,'--',*paths[i:i+30]) for i in range(0,len(paths),30));d={}
 for l in out.split(b'\0'):
  if not l:continue
  h,p=l.split(b'\t',1);d[p.decode()]=h.split()[2].decode()
 return d
def gitpin(p, t=None):
 p=absolute(p);k=rel(p);b=p.read_bytes();o=(t or tree([k]))[k]
 exact=oid(b)==o
 gb=b if exact else git('cat-file','blob',o)
 assert gb.replace(b'\r\n',b'\n')==b.replace(b'\r\n',b'\n'),('Git content differs beyond CRLF-only recipe',k)
 return {**pin(p),'git_commit':SCI,'git_blob_oid':o,'Git_RAW_equals_current':exact,'Git_RAW_bytes':len(gb),'Git_RAW_sha256':sha(gb),'Git_LF_sha256':sha(gb.replace(b'\r\n',b'\n')),'qualification':'exact RAW equality' if exact else 'Git RAW differs from workspace RAW ONLY by CRLF-vs-LF; exact distinct RAW hashes retained, CRLF-only LF equality verified'}
def diff(a,b,path=''):
 if type(a)!=type(b):return [path]
 if isinstance(a,dict):
  out=[]
  for k in sorted(set(a)|set(b)):
   q=path+'/'+str(k)
   out+= [q] if k not in a or k not in b else diff(a[k],b[k],q)
  return out
 if isinstance(a,list):
  if len(a)!=len(b):return [path]
  return sum((diff(x,y,path+'/'+str(i)) for i,(x,y) in enumerate(zip(a,b))),[])
 return [] if a==b else [path]
def terminal(label,cmd):
 assert not (OWN/f'{label}.receipt.json').exists()
 start=now();out=OWN/f'{label}.stdout.log';err=OWN/f'{label}.stderr.log'
 with out.open('wb') as fo,err.open('wb') as fe:
  p=subprocess.Popen(cmd,cwd=ROOT,stdout=fo,stderr=fe)
  print(json.dumps({'started':label,'actual_foreground_PID':p.pid,'command':cmd}),flush=True)
  ec=p.wait()
 d=dict(label=label,actual_foreground_PID=p.pid,actual_parent_PID=os.getpid(),command=cmd,started_utc=start,finished_utc=now(),exit_code=ec,terminal_closed=True,stdout=pin(out),stderr=pin(err))
 save(f'{label}.receipt.json',d)
 print(json.dumps({'finished':label,'PID':p.pid,'exit_code':ec}),flush=True)
 return d

def freeze():
 assert git('rev-parse','HEAD').decode().strip()==SCI
 assert git('show','-s','--format=%P',SCI).decode().strip()==BASE
 if not (OWN/'lease.open.json').exists():save('lease.open.json',dict(status='OPEN',actor=ACTOR,owned_scope=rel(OWN),exact_checked_commit=SCI,parent_commit=BASE,utc=now(),RAW_LF_recipe='LF replaces ONLY byte CRLF with LF; preserves all other bytes',allowed_shared_writes=['one authorized nonowner VERIFIED ledger append',rel(R/'verified.json')]))
 core=[CODE,PARENT,'lean-toolchain','lake-manifest.json',CELL,AUDIT,PUB,LESSON,
  rel(R/'publication-plan.json'),rel(R/'proved-local.json'),rel(R/'root.math71.adoption.json'),rel(R/'root.source71.adoption.json'),rel(R/'root.decoder71.adoption.json'),rel(R/'root.reader-status-overlay71.adoption.json'),
  'runs/20261007-companion-priority/pbps-corrector-change-preproof71/header71.named-literal.proposed.lean','runs/20261007-companion-priority/pbps-corrector-change-preproof71/root.statement-seal71.json',
  rel(R/'mathematics-freeze71.json'),rel(R/'expanded71.frozen.header.lean'),rel(R/'publication-freeze71.json'),rel(R/'source-review.packet.1.json'),rel(R/'source-review.freeze71.json'),
  rel(R/'reader-status-overlay71/proposal.json'),rel(R/'reader-status-overlay71/packet-mapping.json'),rel(R/'audit.before-decoder71.exactraw.snapshot.json'),rel(R/'audit.before-source-admission71.exactraw.json'),rel(R/'cell.before-source-admission71.exactraw.json'),rel(R/'publication.before-source-admission71.exactraw.json'),
  rel(R/'whitespace-diagnosis71/diagnosis.json'),rel(R/'whitespace-diagnosis71/staged.raw-negative.log.gz'),
  'tools/astis.py','tools/astis_advance.py','tools/astis_publication.py','tools/astis_semantic_roundtrip.py','tools/astis_contributor_contract.py','tools/astis_frontier_cells.py']
 for sub,files in [('independent-math71',['lease.final.json','run.json','named-review.payload.json','inputs.manifest.json','auxiliary.inputs.manifest.json','mathematical-verdict.json','compiler.result.json','fresh-lean.receipt.json','fresh-lean.stdout.log','statement-and-parent-retention.json']),('independent-source71',['lease.final.json','owned-manifest.json','source.0.run.json','source.0.decision.json','source.0.admission-fields.json','source.0.complete-finite-input-manifest.json','complete-named-review-decision-input-payload.json','stageB.reader-status-overlay71.decision.json','stageB.eight-formula-BODY-bindings71.json','stageB.final-packet-and-overlay-binding71.json']),('anonymous-decoder',['lease.closed.json','decoder-run.json','manifest.json','decoded0.json'])]:
  core += [rel(R/sub/f) for f in files]
 t=tree(core);rows=[gitpin(p,t) for p in core]
 for i,p in enumerate([CODE,PARENT,'lean-toolchain','lake-manifest.json',CELL,AUDIT,PUB,LESSON]):
  save(f'inputs/{i:02d}.exactraw.snapshot',absolute(p).read_bytes())
 assert pin(ROOT/CODE)['RAW_sha256']==CODE_SHA
 save('inputs.manifest.json',dict(input_count=len(rows),entries=rows,exact_commit=SCI,parent_commit=BASE,RAW_LF_recipe='ONLY byte CRLF -> LF; RAW Git blobs checked with native blob framing; no normalization, no recursive history copies',snapshot_count=8))
 sys.path.insert(0,str(ROOT));from tools import astis_advance as adv
 a=adv.current_advances();found=[(k,v) for k,v in a.items() if DECL in v.get('target_declarations',[])]
 assert len(found)==1
 k,item=found[0];global SAU;SAU=k
 assert item['state']=='PROVED_LOCAL' and item['owner_id']=='companion_root_20261005'
 ledger=(ROOT/'runs/substantive_advances.jsonl').read_bytes()
 save('ledger.before.compact.json',dict(SAU=k,current_item=item,ledger_RAW_bytes=len(ledger),ledger_RAW_sha256=sha(ledger),Git_ledger_blob_oid=tree(['runs/substantive_advances.jsonl'])['runs/substantive_advances.jsonl'],whole_ledger_copied=False))
 save('git.baseline.json',dict(HEAD=SCI,parent=BASE,changed_paths=git('diff','--name-only',BASE,SCI).decode().splitlines(),current_core_unchanged=True))
 print(json.dumps(dict(status='FROZEN',input_count=len(rows),snapshot_count=8,SAU=k)),flush=True)

def native():
 rows=[];summaries=[]
 specs=[('independent-math71','lease.final.json','run.json','named-review.payload.json','90b3b83f5de254f49b90dccb4f046c3dd048ad0ecc2aa1130f30646894f819a5','e7f8c6dcac107780a8752fd146a09e77bd643ea34ee4dd6bbf21b8dff6dfa63b'),('independent-source71','lease.final.json','source.0.run.json','complete-named-review-decision-input-payload.json','c58386e42e0944ee590fe84ddcbf4d6462297532adf758fdf5671c7c008070fb','92ada58587378e938bf02e1b9d91f575d36e062df90e9b248bb1aec8e541a524'),('anonymous-decoder','lease.closed.json','decoder-run.json','decoded0.json','c846e44be094734fda524a511d088f70358100518df56260ccaae31dc76add97','0a23d882205f2cecc030f12ba5a32525d9bbbaa8c2538154a65b8d7806cd961d')]
 for sub,ln,rn,nn,whole,named in specs:
  folder=R/sub;l=load(folder/ln);assert l['status']=='CLOSED_LAST'
  d=load(folder/rn);assert d['run_sha256']==whole and sha(canonical({k:v for k,v in d.items() if k!='run_sha256'}))==whole
  assert pin(folder/nn)['RAW_sha256']==named
  bindings=l.get('all_owned_outputs_except_only_self',l.get('bindings',l.get('covered_files')))
  paths=[]
  for e in bindings:
   p=Path(e.get('path',e.get('name','')))
   if not p.is_absolute():p=folder/p
   b=p.read_bytes();assert sha(b)==e.get('RAW_sha256',e.get('raw_sha256'))
   assert len(b)==e.get('RAW_bytes',e.get('raw_bytes',e.get('byte_count')))
   lf=e.get('LF_sha256',e.get('lf_sha256'))
   if lf:assert sha(b.replace(b'\r\n',b'\n'))==lf
   paths.append(rel(p))
  paths.append(rel(folder/ln));t=tree(paths);rr=[gitpin(p,t) for p in paths];rows+=rr
  count=l.get('owned_file_count_including_self',l.get('owned_count',l.get('owned_file_count_including_lease')))
  assert len(rr)==count
  extras=sorted(set(rel(p) for p in folder.rglob('*') if p.is_file())-set(paths))
  if sub!='anonymous-decoder':assert extras==[]
  else:assert extras==[rel(folder/x) for x in ['decoded0.root-adapter.json','parent-lease.open.json','parent-packet0.json']]
  summaries.append(dict(package=sub,owned_count=count,lease=pin(folder/ln),whole_logical_run_sha256=whole,complete_named_RAW=pin(folder/nn),every_native_RAW_LF_binding_PASS=True,Git_exact_RAW_count=sum(x['Git_RAW_equals_current'] for x in rr),Git_CRLF_only_qualified_count=sum(not x['Git_RAW_equals_current'] for x in rr),root_transport_extras_outside_native_closed_scope=extras))
 save('native-authorities.integrity.json',dict(status='PASS',native_file_count=len(rows),packages=summaries,bindings=rows,recipe='Whole logical run removes ONLY top-level run_sha256; complete named RAW hashes are distinct; native files not copied or rewritten.'))
 return summaries

def maps():
 source=R/'independent-source71';adopt=load(R/'root.source71.adoption.json')
 overlay=load(source/'stageB.reader-status-overlay71.decision.json')
 assert overlay['decision']=='accept_exact_reader_status_overlay_only'
 chain=[];allowed={}
 for row in adopt['finite_current_input_maps']:
  before=absolute(row['approved_overlay_before']['path']);after=absolute(row['approved_overlay_after']['path'])
  assert pin(before)['RAW_sha256']==row['historical_RAW_sha256']
  assert pin(after)['RAW_sha256']==row['current_RAW_sha256']
  paths=diff(load(before),load(after))
  expected={PUB:['/items/0/bindings/0/boundary','/items/0/purification/scope'],LESSON:['/units/0/boundary'],CELL:['/purification/scope'],AUDIT:['/publication_binding_sha256']}[row['path']]
  assert paths==expected,(row['path'],paths)
  allowed[(row['path'],row['historical_RAW_sha256'])]=before
  chain.append(dict(stage='independently-approved-reader-status-overlay',path=row['path'],before=pin(before),after=pin(after),exact_changed_JSON_pointers=paths))
 # The subsequent root source admission is checked field-for-field against the native admission payload.
 fields=load(source/'source.0.admission-fields.json');audit=load(ROOT/AUDIT)
 for k,v in fields['audit_fields'].items():assert audit[k]==v,('native source admission field',k)
 assert audit['publication_binding_sha256']==BIND
 assert audit['source_review']['reviewer_packet_sha256']==PACKET
 assert len(audit['semantic_slots'])==7 and len(audit['deltas'])==16
 assert all(x['severity']=='informational' for x in audit['deltas']) and audit['repairs']==[]
 for p,fn in [(AUDIT,'audit.before-source-admission71.exactraw.json'),(PUB,'publication.before-source-admission71.exactraw.json'),(CELL,'cell.before-source-admission71.exactraw.json')]:
  before=R/fn;after=ROOT/p;dd=diff(load(before),load(after));allowed[(p,pin(before)['RAW_sha256'])]=before
  if p==AUDIT:
   assert set(x.split('/')[1] for x in dd)<=set(fields['audit_fields'])
   for k in ['source','lean','reconstruction','publication_binding_sha256','publication_context']:assert load(before)[k]==load(after)[k]
  elif p==PUB:
   a,b=load(before),load(after)
   expected=fields['publication_source_proof_coverage'];assert b['items'][0]['source_proof_coverage']==expected
   a['items'][0]['source_proof_coverage']=expected;assert a==b
  else:
   a,b=load(before),load(after);proved=load(R/'proved-local.json');boundary=proved['truth_boundary']
   assert a['status']=='claimed' and b['status']=='proved_locally'
   a['source_proof_coverage']=fields['cell_source_proof_coverage']
   a['source_detail_audit'].update(gap='Actual B21 is locally compiled and independently source-reviewed. Next exact B4 perturbation algebra and actual residual-dynamics producer remain open.',fidelity_boundary=boundary)
   a['evidence']['truth_boundary']=boundary
   a['status']='proved_locally';a['conceptual_mirror_audit']=proved['conceptual_mirror_audit']
   a['evidence'].update(proof_review=rel(R/'independent-math71/mathematical-verdict.json'),source_review=rel(source/'source.0.decision.json'),execution_boundary=boundary)
   assert a==b,('cell admission is not the exact native-coverage/PROVED_LOCAL process update',diff(a,b))
  chain.append(dict(stage='exact-native-source-admission-and-PROVED_LOCAL',path=p,before=pin(before),after=pin(after),exact_changed_JSON_pointers=dd))
 manifest=load(source/'source.0.complete-finite-input-manifest.json');rr=[]
 for e in manifest['entries']:
  p=ROOT/e['path'];cur=pin(p)
  if cur['RAW_sha256']==e['RAW_sha256']:rr.append(dict(path=e['path'],historical_RAW_sha256=e['RAW_sha256'],resolution='exact-current-Git-RAW',current=gitpin(p)));continue
  key=(e['path'],e['RAW_sha256']);assert key in allowed,('UNMAPPED source input',key)
  q=allowed[key];assert pin(q)['RAW_sha256']==e['RAW_sha256']
  assert any(sha((source/z).read_bytes())==e['RAW_sha256'] for z in e['owned_RAW_snapshot_refs'])
  assert pin(q)['LF_sha256']==e['LF_sha256']
  rr.append(dict(path=e['path'],historical_RAW_sha256=e['RAW_sha256'],resolution='explicit-finite-native-map',exact_snapshot=gitpin(q),current=gitpin(p)))
 assert len(rr)==77
 save('finite-current-input-resolutions.json',dict(source_versioned_rows=len(rr),current_rows=sum(x['resolution']=='exact-current-Git-RAW' for x in rr),historical_rows=sum(x['resolution']!='exact-current-Git-RAW' for x in rr),chain=chain,rows=rr,exact_root_admission_helper=gitpin(R/'root-science-helpers71/adopt-source71.py'),no_blanket_exclusions=True))
 return audit

def audit():
 if not (OWN/'native-authorities.integrity.json').exists():native()
 if not (OWN/'finite-current-input-resolutions.json').exists():a=maps()
 else:a=load(ROOT/AUDIT)
 # Reuse unchanged closed mathematical proof review through exact SCI code and source seals.
 m=load(R/'independent-math71/mathematical-verdict.json')
 assert pin(ROOT/CODE)['RAW_sha256']==CODE_SHA
 seal=ROOT/'runs/20261007-companion-priority/pbps-corrector-change-preproof71/header71.named-literal.proposed.lean'
 assert (ROOT/CODE).read_bytes().startswith(seal.read_bytes())
 lines=(ROOT/CODE).read_bytes().splitlines(keepends=True)
 assert len(lines)==528
 body=load(R/'independent-source71/stageB.eight-formula-BODY-bindings71.json');checks=[]
 lesson=load(ROOT/LESSON);steps=lesson['units'][0]['steps']
 for row,step in zip(body['steps'],steps):
  r=row['exact_source_region'];b=b''.join(lines[r['start_line']-1:r['end_line']])
  assert r['start_line']>=147 and sha(b)==r['exact_code_raw_sha256']==row['RAW_sha256']
  assert step['formula']==row['formula']
  assert step['lean']==b.decode().rstrip('\n') or step['lean']==b.decode()
  checks.append(dict(step=row['step'],start_line=r['start_line'],end_line=r['end_line'],RAW_sha256=sha(b),exact_literal_BODY=True,formula_unchanged=True))
 assert len(checks)==8
 treeast=ast.parse((ROOT/'tools/astis.py').read_text(encoding='utf-8-sig'));nodes=[]
 for n in treeast.body:
  if isinstance(n,(ast.Assign,ast.AnnAssign)) and any(isinstance(t,ast.Name) and t.id=='FORBIDDEN_REGEX' for t in (n.targets if isinstance(n,ast.Assign) else [n.target])):nodes.append(n)
  if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name=='strip_lean_comments_and_strings':nodes.append(n)
 env={'re':re};exec(builtins.compile(ast.Module(body=nodes,type_ignores=[]),'pinned-astis-scan','exec'),env)
 text=(ROOT/CODE).read_text(encoding='utf-8-sig');stripped=env['strip_lean_comments_and_strings'](text)
 hits=[]
 hits=[dict(kind='pinned FORBIDDEN_REGEX',match=x.group(),line=stripped[:x.start()].count('\n')+1) for x in env['FORBIDDEN_REGEX'].finditer(stripped)]
 assert hits==[]
 assert len(re.findall(r'^private def ',text,re.M))==1
 assert len(re.findall(r'^theorem ',text,re.M))==1
 assert re.findall(r'^import (.+)$',text,re.M)==['AutoSamplingTheory.ExampleCases.ProximalBPS.ActualProjectedRotation']
 save('fake-closure-and-statement-scan.json',dict(status='PASS',hits=hits,pinned_scanner=gitpin('tools/astis.py'),whole_module=gitpin(CODE),private_full_literal_Prop=1,private_proof_providers=0,public_theorems=1,original_callers=6,same_common_witnesses=12,rank_zero_and_alphaeta_one_legal=True,actual_parent_only=PARENT,sharp_energy68_dependency=False,sealed147prefix=gitpin(seal)))
 save('literal-BODY-bindings.json',dict(steps=checks,count=8,covered_BODY_lines=377))
 diag=load(R/'whitespace-diagnosis71/diagnosis.json');gb=gzip.decompress((R/'whitespace-diagnosis71/staged.raw-negative.log.gz').read_bytes())
 assert sha(gb)==diag['negative_RAW_sha256'];assert len(diag['findings'])==1089 and diag['authored_complement_exit']==0
 save('whitespace-preservation.json',dict(immutable_findings=1089,full_staged_exit=diag['full_staged_exit'],full_staged_PASS=False,authored_complement_PASS=True,native_negative_RAW_bytes=len(gb),native_negative_RAW_sha256=sha(gb),lossless_gzip=gitpin(R/'whitespace-diagnosis71/staged.raw-negative.log.gz'),native_diagnosis=gitpin(R/'whitespace-diagnosis71/diagnosis.json'),normalized=False))
 fresh=load(R/'independent-math71/fresh-lean.receipt.json');assert fresh['exit_code']==0 and fresh['actual_foreground_PID']==3064
 ax=(R/'independent-math71/fresh-lean.stdout.log').read_text(encoding='utf-8-sig')
 axrows=re.findall(r"'"+re.escape(DECL)+r"' depends on axioms:\s*\[([^\]]*)\]",ax)
 assert len(axrows)==1 and [x.strip() for x in axrows[0].split(',')]==['propext','Classical.choice','Quot.sound']
 assert 'leanprover/lean4:v4.33.0' in (ROOT/'lean-toolchain').read_text()
 manifest=load(ROOT/'lake-manifest.json');mathlib=[x for x in manifest['packages'] if x['name']=='mathlib'][0]
 assert git('-C',str(ROOT/'.lake/packages/mathlib'),'rev-parse','HEAD').decode().strip()==mathlib['rev']
 save('mathematics-reuse.json',dict(status='EXACT_SCI_RAW_EQUALS_INDEPENDENTLY_REVIEWED_SOURCE',checked_commit=SCI,code=gitpin(CODE),parent=gitpin(PARENT),native_math_verdict=gitpin(R/'independent-math71/mathematical-verdict.json'),fresh_source_elaboration_reused=fresh,axioms=['propext','Classical.choice','Quot.sound'],independent_written_proof=gitpin(R/'independent-math71/mathematical-review.utf8.txt'),seal_retained=True,Lean_version='4.33.0',Mathlib_rev=mathlib['rev'],new_fresh_proof_compile=False))
 save('source-acceptance.json',dict(status='ACCEPTED_BOUND_SOURCE_REVIEW',audit=gitpin(AUDIT),source_lease=gitpin(R/'independent-source71/lease.final.json'),source_run_sha256=a['source_review']['review_run_sha256'],official_packet_sha256=PACKET,publication_binding_sha256=BIND,semantic_slots=a['semantic_slots'],deltas=a['deltas'],verdict=a['verdict'],repairs=a['repairs'],source_coverage=load(R/'root.source71.adoption.json')['coverage'],schema_adapter_required=False,source_graph_distinct_from_Lean_dependencies=True))
 print(json.dumps(dict(status='AUDIT_PASS',native_files=382,source_slots=7,informational=16,BODY_steps=8,fake_closure_hits=0)),flush=True)

def gates():
 cmds=[('frontier',[PY,'-B','-X','utf8','tools/astis_frontier_cells.py','check']),('publication',[PY,'-B','-X','utf8','tools/astis_publication.py','check','--base',BASE,'--ci']),('contributor',[PY,'-B','-X','utf8','tools/astis_contributor_contract.py','check','--base',BASE,'--ci']),('semantic',[PY,'-B','-X','utf8','tools/astis_semantic_roundtrip.py','check']),('reviewed',[PY,'-B','-X','utf8','-c',"from tools import astis_publication as p; import json; print(json.dumps(p.check_advance(['"+DECL+"'],reviewed=True),ensure_ascii=False))"])]
 receipts=[terminal(n,c) for n,c in cmds];save('gates.json',dict(exact_checked_commit=SCI,base=BASE,receipts=receipts,all_actual_exit_zero=all(x['exit_code']==0 for x in receipts)))
 assert all(x['exit_code']==0 for x in receipts),'REQUIRED_GATE_FAILURE'

def crosslinks():
 source=R/'independent-source71';math=R/'independent-math71';blind=R/'anonymous-decoder'
 payload=load(source/'complete-named-review-decision-input-payload.json')
 assert payload['native_run_complete']==load(source/'source.0.run.json')
 assert payload['decision_complete']==load(source/'source.0.decision.json')
 assert payload['canonical_admission_fields_complete']==load(source/'source.0.admission-fields.json')
 assert payload['full_RAW_review_utf8'].encode()==(source/'source.0.review.RAW.md').read_bytes()
 assert payload['complete_finite_versioned_input_manifest_complete']==load(source/'source.0.complete-finite-input-manifest.json')
 for n,v in payload['named_finite_input_records'].items():assert v==load(source/n)
 owned=load(source/'owned-manifest.json');lease=load(source/'lease.final.json')
 assert sha(canonical(owned['files']))==owned['entries_canonical_sha256']==lease['entries_canonical_sha256']
 assert pin(source/'owned-manifest.json')['RAW_sha256']==lease['native_manifest_RAW_sha256']
 m=load(math/'named-review.payload.json')
 assert m['complete_mathematical_verdict']==load(math/'mathematical-verdict.json')
 assert m['complete_exact_input_manifest']==load(math/'inputs.manifest.json')
 assert m['complete_written_independent_mathematics'].encode()==(math/'mathematical-review.utf8.txt').read_bytes()
 mathrows=[]
 for row in load(math/'inputs.manifest.json')['inputs']:
  e=row['original'];p=absolute(e['path']);assert pin(p)['RAW_sha256']==e['raw_sha256']
  for name in ['RAW_snapshot','LF_snapshot']:
   q=row[name];assert pin(q['path'])['RAW_sha256']==q['raw_sha256']
  mathrows.append(dict(original_current=gitpin(p),native_RAW_snapshot=gitpin(row['RAW_snapshot']['path']),native_LF_snapshot=gitpin(row['LF_snapshot']['path'])))
 assert len(mathrows)==14
 br=load(blind/'decoder-run.json');assert br['source_text_visible']==br['source_identity_visible']==br['external_source_used']==br['proof_BODY_visible']==False
 assert br['caller_condition_count']==6 and br['common_existential_witness_count']==12 and br['unresolved_count']==0 and br['slot_count']==51
 sys.path.insert(0,str(ROOT));from tools import astis_semantic_roundtrip as rt;from tools import astis_publication as p
 a=load(ROOT/AUDIT);packet=rt.semantic_reviewer_packet(a)
 assert packet==load(R/'source-review.packet.1.json') and packet['packet_sha256']==PACKET
 item=next(x for x in p.load() if x['id']=='pbps-actual-corrector-change')
 assert p.binding_digest(item,item['bindings'][0],p.inputs())==BIND==a['publication_binding_sha256']
 assert p.review_context(item,item['bindings'][0],p.inputs())==a['publication_context']
 old=load(R/'focused-first/receipt.json');good=load(R/'focused-typed-substitution/receipt.json')
 assert old['exit_code']==1 and old['actual_foreground_PID']==29980
 assert good['exit_code']==0 and good['actual_foreground_PID']==49980
 rr=load(OWN/'finite-current-input-resolutions.json')['rows']
 negative_observers=[]
 for f in sorted(OWN.glob('*.receipt.json')):
  d=load(f)
  if d['exit_code']!=0:negative_observers.append(dict(receipt=pin(f),stdout=d['stdout'],stderr=d['stderr'],scope='observer failure, no mathematical/source/canonical mutation; corrected observer success separately retained'))
 save('authority-crosslinks-and-retained-negatives.json',dict(status='PASS',math_frozen_input_rows_all14_current=mathrows,source_complete_named_payload_is_complete_native_run_decision_review_input_union=True,source_owned_manifest_logical_checked=True,strict_blind_source_invisible_and_6callers12witnesses51rows_zero_unresolved=True,canonical_source_slots=7,official_packet_current_exact=gitpin(R/'source-review.packet.1.json'),publication_binding=BIND,publication_context_exact=True,source_input_current_RAW_rows=70,source_input_historical_explicit_rows=7,source_current_rows_Git_exact_RAW=sum(x['current']['Git_RAW_equals_current'] for x in rr if x['resolution']=='exact-current-Git-RAW'),source_current_rows_Git_CRLF_only_qualified=sum(not x['current']['Git_RAW_equals_current'] for x in rr if x['resolution']=='exact-current-Git-RAW'),resolution_label_qualification='exact-current-Git-RAW identifies equality of historical RAW with current workspace RAW. Each Git_RAW_equals_current boolean and distinct Git_RAW/LF fields separately states Git RAW equality or CRLF-only qualification; no false toolchain RAW identity.',root_first_negative=[gitpin(R/'focused-first'/n) for n in ['receipt.json','stdout.log','stderr.log']],failed_first_print_no_axioms_is_not_certificate=True,root_successful_compile=gitpin(R/'focused-typed-substitution/receipt.json'),own_observer_failures=negative_observers,own_observer_failure_count=len(negative_observers),no_failures_discarded=True))
 print(json.dumps(dict(status='CROSSLINK_PASS',math_frozen_current_rows=14,source_current_rows=70,historical_rows=7,own_observer_failures=len(negative_observers))),flush=True)

def decision():
 assert load(OWN/'gates.json')['all_actual_exit_zero']
 rows=load(OWN/'inputs.manifest.json')['entries']
 for e in rows:assert pin(e['path'])['RAW_sha256']==e['RAW_sha256']
 assert git('rev-parse','HEAD').decode().strip()==SCI
 d=dict(status='ACCEPTED_EXACT_SCI71_NONOWNER_VERIFICATION',actor=ACTOR,checked_commit=SCI,parent_commit=BASE,production_declarations=[DECL],mathematics_reused_by_exact_Git_RAW=True,source_slots=7,informational_deltas=16,blocking_deltas=0,mathematical_repairs=0,source_packet_sha256=PACKET,publication_binding_sha256=BIND,fake_closure_hits=0,axioms=['propext','Classical.choice','Quot.sound'],fresh_admission_gates=pin(OWN/'gates.json'),full_repository_gate_run=False,remaining_boundary='Actual same-witness B20/B21 corrector-change only. B4/B27/B28 perturbation/dynamics, H1/nonexplosion, full paper/main/errors/caps/query costs/composition, aggregate/reader/remoteCI/main/live/full Exposition/PURIFIED/Goal are not granted.',approved_transition_pending=True)
 save('verdict.json',d)
 save('independent-review.utf8.txt',('Exact SCI71 '+SCI+' independently accepted. Complete source equals the already independently checked 528-line mathematical implementation RAW '+CODE_SHA+'. Six original caller hypotheses, twelve common witnesses, actual conditional/polar components and all parent70 conclusions remain intact. K=A0 Inv is not a new inverse; SAME Gamma0 Inv cancellation and commutation yield the mixed identity; the diagonal norm terms and cross terms give exactly C(gP,gV)-C(fP,fV)=-||fP||²+||fV||² for C(u,v)=(||u||²-||v||²)/2-<A0 Inv u,v>. Rank0 and alpha eta=1 remain legal.\nIndependent source CLOSED277 and blind CLOSED10 are validated in full by every native RAW binding and exact SCI Git blobs, with 7 semantic slots, all16 informational deltas retained, zero blockers/repairs. Explicit reader-status and source-admission finite maps preserve historical inputs without current-only fallback. All eight formula steps match literal BODY. Fresh current frontier/publication/contributor/semantic/reviewed gates are required; independent fresh elaboration PID3064 is reused solely by exact source/toolchain/Mathlib RAW equality. The failed first compile is retained and not a proof certificate.\nOnly the exact theorem edge is accepted; no whole-repository build, integration, reader acceptance, main/live/PURIFIED/full-paper/Goal claim.\n').encode())
 print(json.dumps(d),flush=True)

def transition():
 sys.path.insert(0,str(ROOT));from tools import astis_advance as adv
 before=load(OWN/'ledger.before.compact.json');sau=before['SAU'];item=adv.current_advances()[sau]
 assert item['state']=='PROVED_LOCAL' and item['owner_id']=='companion_root_20261005' and item['owner_id']!=ACTOR
 assert item['publication_declarations']==item['latest_evidence']['lean_declarations']==[DECL]
 ledger=ROOT/'runs/substantive_advances.jsonl';b=ledger.read_bytes()
 assert len(b)==before['ledger_RAW_bytes'] and sha(b)==before['ledger_RAW_sha256']
 assert git('rev-parse','HEAD').decode().strip()==SCI
 assert load(OWN/'verdict.json')['status']=='ACCEPTED_EXACT_SCI71_NONOWNER_VERIFICATION'
 evidence=dict(verifier_id=ACTOR,verified_commit=SCI,gate=dict(status='PASS',focused_math_compile='independent fresh Lean3064 EXIT0 reused by exact SCI RAW equality; root49980 EXIT0/3950/standard3',fresh_focused_gates=rel(OWN/'gates.json'),toolchain='Lean4.33.0/pinned Mathlib',scope='bounded exact theorem/source admission only'),source_audit=dict(id='ASTIS-RT-20261010-PBPSActualCorrectorChange',state='accepted',evidence=rel(OWN/'source-acceptance.json'),source_packet_sha256=PACKET,semantic_slots=7,informational_deltas=16,blocking_deltas=0,mathematical_repairs=0),fake_closure_scan=dict(status='PASS',hits=0,evidence=rel(OWN/'fake-closure-and-statement-scan.json')),publication_declarations=[DECL],native_independent_verdict_path=rel(OWN/'verdict.json'),parent_commit=BASE,remaining_boundary=load(OWN/'verdict.json')['remaining_boundary'])
 result=adv.transition_advance(sau,'VERIFIED',worker_id=ACTOR,modes=['independent-exact-science-verification'],evidence=evidence)
 after=ledger.read_bytes();assert after.startswith(b)
 addition=after[len(b):];assert len(addition.splitlines())==1
 event=json.loads(addition);assert event['to_state']=='VERIFIED'
 save('ledger.VERIFIED.append.exactraw.jsonl',addition)
 save('ledger.after.compact.json',dict(SAU=sau,before_RAW_bytes=len(b),before_RAW_sha256=sha(b),after_RAW_bytes=len(after),after_RAW_sha256=sha(after),prefix_unchanged=True,appended_event_count=1,actual_nonowner_PID=os.getpid(),verified_commit=SCI,event=event))
 v=dict(status='VERIFIED',advance_id=sau,verifier_id=ACTOR,owner_id=item['owner_id'],verified_commit=SCI,parent_commit=BASE,gate=evidence['gate'],source_audit=evidence['source_audit'],fake_closure_scan=evidence['fake_closure_scan'],publication_declarations=[DECL],native_scope=rel(OWN),ledger_append=pin(OWN/'ledger.VERIFIED.append.exactraw.jsonl'),remaining_boundary=evidence['remaining_boundary'],aggregate=False,reader_admission=False,full_Exposition=False,PURIFIED=False,main_live=False,full_paper=False,Goal_complete=False)
 assert not (R/'verified.json').exists();(R/'verified.json').write_bytes(json.dumps(v,ensure_ascii=False,sort_keys=True,indent=2).encode()+b'\n')
 save('verified.external-write.binding.json',dict(authorized_shared_write=pin(R/'verified.json'),ledger_after=pin(OWN/'ledger.after.compact.json'),only_one_VERIFIED_event=True))
 print(json.dumps(dict(status='VERIFIED',advance_id=sau,verified_commit=SCI,actual_nonowner_PID=os.getpid(),result=result),ensure_ascii=False,default=str),flush=True)

def transition_readback():
 # Readback/finish only. The one authorized append already succeeded in PID17972;
 # the old terminal EXIT1 was a post-append field-observer error. Never retry append.
 sys.path.insert(0,str(ROOT));from tools import astis_advance as adv
 before=load(OWN/'ledger.before.compact.json');sau=before['SAU'];item=adv.current_advances()[sau]
 assert item['state']=='VERIFIED' and item['owner_id']=='companion_root_20261005'
 after=(ROOT/'runs/substantive_advances.jsonl').read_bytes();n=before['ledger_RAW_bytes'];prefix=after[:n];addition=after[n:]
 assert sha(prefix)==before['ledger_RAW_sha256'] and len(addition.splitlines())==1
 event=json.loads(addition);assert event['to_state']=='VERIFIED' and event['from_state']=='PROVED_LOCAL' and event['worker_id']==ACTOR
 evidence=event['evidence'];assert evidence['verified_commit']==SCI and evidence['verifier_id']==ACTOR and event['advance_id']==sau
 assert item['latest_evidence']==evidence
 old=load(OWN/'transition.receipt.json');assert old['exit_code']==1 and old['actual_foreground_PID']==17972
 assert 'KeyError' in (OWN/'transition.stderr.log').read_text() and "'state'" in (OWN/'transition.stderr.log').read_text()
 save('ledger.VERIFIED.append.exactraw.jsonl',addition)
 save('ledger.after.compact.json',dict(SAU=sau,before_RAW_bytes=n,before_RAW_sha256=sha(prefix),after_RAW_bytes=len(after),after_RAW_sha256=sha(after),prefix_unchanged=True,appended_event_count=1,actual_nonowner_transition_call_PID=17972,transition_command_exit=1,post_append_observer_error="KeyError 'state'; actual event field is to_state",actual_completion_readback_PID=os.getpid(),readback_only_no_second_append=True,verified_commit=SCI,event=event))
 v=dict(status='VERIFIED',advance_id=sau,verifier_id=ACTOR,owner_id=item['owner_id'],verified_commit=SCI,parent_commit=BASE,gate=evidence['gate'],source_audit=evidence['source_audit'],fake_closure_scan=evidence['fake_closure_scan'],publication_declarations=[DECL],native_scope=rel(OWN),ledger_append=pin(OWN/'ledger.VERIFIED.append.exactraw.jsonl'),actual_transition_call_PID=17972,transition_terminal_EXIT1_after_successful_append_retained=True,completion_readback_PID=os.getpid(),readback_no_second_transition=True,remaining_boundary=evidence['remaining_boundary'],aggregate=False,reader_admission=False,full_Exposition=False,PURIFIED=False,main_live=False,full_paper=False,Goal_complete=False)
 assert not (R/'verified.json').exists();(R/'verified.json').write_bytes(json.dumps(v,ensure_ascii=False,sort_keys=True,indent=2).encode()+b'\n')
 save('verified.external-write.binding.json',dict(authorized_shared_write=pin(R/'verified.json'),ledger_after=pin(OWN/'ledger.after.compact.json'),only_one_VERIFIED_event=True,post_append_observer_failure=pin(OWN/'transition.receipt.json'),actual_readback_PID=os.getpid()))
 print(json.dumps(dict(status='VERIFIED_SINGLE_EVENT_READBACK_COMPLETE',advance_id=sau,verified_commit=SCI,actual_completion_PID=os.getpid(),no_transition_call=True)),flush=True)

def finalize():
 failures=[]
 for f in sorted(OWN.glob('*.receipt.json')):
  d=load(f)
  if d['exit_code']!=0:failures.append(dict(receipt=pin(f),stdout=d['stdout'],stderr=d['stderr'],actual_PID=d['actual_foreground_PID'],exit_code=d['exit_code']))
 save('complete-negative-terminal-catalog.json',dict(count=len(failures),failures=failures,post_append_observer_failure_completed_without_second_append=True,no_negative_or_executed_helper_discarded=True))
 # Explicit finite input union only: no walking historical directories or ledger copies.
 union={}
 def collect(v):
  if isinstance(v,dict):
   if {'path','RAW_sha256','RAW_bytes'}<=set(v):
    p=absolute(v['path'])
    if not p.is_relative_to(OWN):
     e=pin(p);assert e['RAW_sha256']==v['RAW_sha256'] and e['RAW_bytes']==v['RAW_bytes']
     union[(e['path'],e['RAW_sha256'])]=e
   for x in v.values():collect(x)
  elif isinstance(v,list):
   for x in v:collect(x)
 for name in ['inputs.manifest.json','native-authorities.integrity.json','finite-current-input-resolutions.json','authority-crosslinks-and-retained-negatives.json','mathematics-reuse.json','source-acceptance.json','fake-closure-and-statement-scan.json','whitespace-preservation.json']:
  collect(load(OWN/name))
 unionrows=[union[k] for k in sorted(union)]
 save('inputs.complete-finite-union.json',dict(input_count=len(unionrows),initial_core_pin_count=59,core_snapshot_count=8,reused_native_closed_file_count=382,entries=unionrows,entries_logical_sha256=sha(canonical(unionrows)),finite_explicit_pin_union_only=True,no_recursive_historical_directory_copy=True,ledger_only_compact_prefix_plus_one_event=True))
 files=['inputs.manifest.json','inputs.complete-finite-union.json','native-authorities.integrity.json','finite-current-input-resolutions.json','authority-crosslinks-and-retained-negatives.json','complete-negative-terminal-catalog.json','mathematics-reuse.json','source-acceptance.json','fake-closure-and-statement-scan.json','literal-BODY-bindings.json','whitespace-preservation.json','gates.json','verdict.json','independent-review.utf8.txt','ledger.after.compact.json','verified.external-write.binding.json']
 payload={f:load(OWN/f) if f.endswith('.json') else (OWN/f).read_text(encoding='utf-8') for f in files}
 named=save('complete-named-verification.payload.json',dict(schema='complete-named-independent-exact-SCI71-review-decision-input-payload-v1',checked_commit=SCI,complete_named_payload=payload))
 out=[pin(p) for p in sorted(OWN.rglob('*')) if p.is_file() and p.name not in ['finalize.stdout.log','finalize.stderr.log','finalize.receipt.json','outputs.manifest.json','run.json','lease.final.json']]
 manifest=dict(schema='finite-owned-baseline-manifest-v1',entries=out,entry_count=len(out),deferred_to_final_lease=['finalize.stdout.log','finalize.stderr.log','finalize.receipt.json','outputs.manifest.json','run.json','readback terminal layers','close terminal layers','lease.final.json'],entries_logical_sha256=sha(canonical(out)))
 save('outputs.manifest.json',manifest)
 run=dict(schema='independent-exact-SCI71-verification-native-run-v1',actor=ACTOR,status='VERIFIED',checked_commit=SCI,parent_commit=BASE,input_manifest=pin(OWN/'inputs.manifest.json'),complete_input_manifest=pin(OWN/'inputs.complete-finite-union.json'),native_integrity=pin(OWN/'native-authorities.integrity.json'),named_complete_RAW_payload=named,output_manifest=pin(OWN/'outputs.manifest.json'),whole_logical_recipe='canonical JSON sort_keys/ensure_ascii=False/separators comma colon; omit ONLY top-level run_sha256',gate_receipts=[pin(OWN/f'{n}.receipt.json') for n in ['frontier','publication','contributor','semantic','reviewed']],transition_receipt=pin(OWN/'transition.receipt.json'),transition_receipt_qualification='EXIT1 after the one successful append; retained wrong-field readback observer. No transition retry.',transition_completion_receipt=pin(OWN/'transition-readback.receipt.json'),shared_verified=pin(R/'verified.json'),verdict=pin(OWN/'verdict.json'),negative_terminal_catalog=pin(OWN/'complete-negative-terminal-catalog.json'),closed_math_source_blind_counts=[95,277,10],no_aggregate_reader_or_whole_Goal_credit=True)
 run['run_sha256']=sha(canonical(run));save('run.json',run)
 print(json.dumps(dict(status='FINALIZED',whole_logical_run_sha256=run['run_sha256'],complete_named_RAW=named,output_manifest=pin(OWN/'outputs.manifest.json'))),flush=True)

def validate(closed=False):
 run=load(OWN/'run.json');assert sha(canonical({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']
 for field in ['input_manifest','complete_input_manifest','native_integrity','named_complete_RAW_payload','output_manifest','shared_verified','verdict','transition_receipt','transition_completion_receipt']:
  e=run[field];assert pin(e['path'])['RAW_sha256']==e['RAW_sha256']
 for e in load(OWN/'outputs.manifest.json')['entries']:assert pin(e['path'])['RAW_sha256']==e['RAW_sha256']
 for e in load(OWN/'inputs.complete-finite-union.json')['entries']:assert pin(e['path'])==e
 after=load(OWN/'ledger.after.compact.json');ledger=(ROOT/'runs/substantive_advances.jsonl').read_bytes()
 assert len(ledger)==after['after_RAW_bytes'] and sha(ledger)==after['after_RAW_sha256']
 if closed:
  l=load(OWN/'lease.final.json');assert l['status']=='CLOSED_LAST'
  actual=set(rel(p) for p in OWN.rglob('*') if p.is_file());expected={e['path'] for e in l['all_owned_outputs_except_only_self']}|{rel(OWN/'lease.final.json')};assert actual==expected
  for e in l['all_owned_outputs_except_only_self']:assert pin(e['path'])==e
  assert len(actual)==l['owned_file_count_including_self']
  assert sha(canonical(l['all_owned_outputs_except_only_self']))==l['closure_manifest_logical_sha256']
  assert all(absolute(e['path']).stat().st_mtime_ns<=(OWN/'lease.final.json').stat().st_mtime_ns for e in l['all_owned_outputs_except_only_self'])
 print(json.dumps(dict(status='READ_ONLY_PASS',actual_foreground_PID=os.getpid(),exit_code=0,owned_writes=0,closed=closed,owned_count=len(list(p for p in OWN.rglob('*') if p.is_file())),whole_logical_run_sha256=run['run_sha256'],complete_named_RAW=run['named_complete_RAW_payload'],lease=pin(OWN/'lease.final.json') if closed else None)),flush=True)

def close():
 assert not (OWN/'lease.final.json').exists()
 receipt=terminal('close-readonly',[PY,'-B','-X','utf8',str(OWN/'verify71.py'),'validate'])
 assert receipt['exit_code']==0
 rows=[pin(p) for p in sorted(OWN.rglob('*')) if p.is_file()]
 run=load(OWN/'run.json');lease=dict(status='CLOSED_LAST',actor=ACTOR,owned_scope=rel(OWN),actual_last_writer_PID=os.getpid(),actual_close_exit_code=0,actual_foreground_close_probe=receipt,owned_file_count_including_self=len(rows)+1,all_owned_outputs_except_only_self=rows,closure_manifest_logical_sha256=sha(canonical(rows)),whole_logical_run_sha256=run['run_sha256'],named_complete_RAW_review=run['named_complete_RAW_payload'],last_owned_write=True,no_more_owned_writes=True,checked_commit=SCI,approved_nonowner_VERIFIED=True,canonical_writes_only=['one VERIFIED ledger append',rel(R/'verified.json')],postclose='read-only external validator; no owned writes')
 save('lease.final.json',lease)
 print(json.dumps(dict(status='CLOSED_LAST',actual_close_writer_PID=os.getpid(),owned_count=len(rows)+1,lease_RAW=pin(OWN/'lease.final.json'),closure_manifest_logical_sha256=lease['closure_manifest_logical_sha256'],whole_logical_run_sha256=run['run_sha256'],complete_named_RAW=run['named_complete_RAW_payload'])),flush=True)

if __name__=='__main__':
 os.chdir(ROOT);cmd=sys.argv[1]
 {'freeze':freeze,'audit':audit,'gates':gates,'crosslinks':crosslinks,'decision':decision,'transition':transition,'transition-readback':transition_readback,'finalize':finalize,'validate':validate,'postclose':lambda:validate(True),'close':close}[cmd]()
