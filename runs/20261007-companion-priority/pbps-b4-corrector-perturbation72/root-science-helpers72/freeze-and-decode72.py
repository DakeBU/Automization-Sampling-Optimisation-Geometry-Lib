from pathlib import Path
import hashlib,json,os,re,sys
root=Path.cwd();r=Path('runs/20261007-companion-priority/pbps-b4-corrector-perturbation72');pre=Path('runs/20261007-companion-priority/pbps-b4-perturbation-preproof72')
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def new(p,x):
 p=Path(p);assert not p.exists(),p;p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.resolve().as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
claim=load(r/'claim.json');seal=load(pre/'root.statement-seal72.json')
paths=[Path(p) for p in claim['proposed_files']];names=claim['target_declarations']
labels=['focused-generic-typed-inner','focused-actual-first'];compiled=[]
for i,(p,decl,label) in enumerate(zip(paths,names,labels)):
 raw=p.read_bytes();q=load(r/label/'receipt.json');assert q['terminal_closed'] and q['exit_code']==0
 assert any(Path(z['path']).resolve()==p.resolve() and z['RAW_sha256']==sha(raw) for z in q['inputs'])
 log=(r/label/'stdout.log').read_text(encoding='utf8')
 match=re.search(re.escape("'"+decl+"' depends on axioms: ")+r'\[([^\]]+)\]',log)
 assert match,decl
 axioms={x.strip() for x in match.group(1).split(',')};assert axioms=={'propext','Classical.choice','Quot.sound'},axioms
 jobs=int(re.search(r'Build completed successfully \((\d+) jobs\)',log).group(1))
 (r/f'canonical72.{i}.frozen.exactraw.lean').write_bytes(raw)
 compiled.append(dict(declaration=decl,module=pin(p),focused_receipt=pin(r/label/'receipt.json'),focused_PID=q['actual_foreground_PID'],focused_EXIT=0,jobs=jobs,axioms=sorted(axioms),lines=len(raw.decode().splitlines())))
actual=paths[1].read_bytes();header=(pre/'header72.actual.named-literal.proposed.lean').read_bytes();assert actual.startswith(header)
generic=paths[0].read_text(encoding='utf8');generic_header=generic.split(' := by\n',1)[0].replace('import Mathlib.Tactic.Linarith\n','')
assert generic_header==(pre/'header72.generic.proposed.lean').read_text(encoding='utf8')
s=actual.decode();literal=s[s.index('private def actual_corrector_perturbation_statement'):s.index('\ntheorem actual_corrector_perturbation')].rstrip()
expanded=literal.replace('private def actual_corrector_perturbation_statement','theorem actual_corrector_perturbation',1).replace(' : Prop :=\n',' :\n',1)+'\n'
(r/'expanded72.actual.frozen.header.lean').write_text(expanded,encoding='utf8',newline='\n')
generic_stmt=generic_header.split('theorem quadratic_corrector_perturbation',1)[1].rstrip('\n')
actual_stmt=expanded.split('theorem actual_corrector_perturbation',1)[1].rstrip('\n')
contexts=[['H is one complete real Hilbert space; bounded real-linear endomorphism multiplication is composition and 1 is its identity operator.','IsSelfAdjoint means selfadjoint for the real Hilbert adjoint; Commute A Inv means their two composition orders are equal.','Every displayed operator condition is an explicit hypothesis. The functional C is exactly the displayed let definition, not an independently assumed object. u,v,r range over all H, including the zero space.'],load('runs/20261007-companion-priority/pbps-actual-corrector-change71/anonymous.lean-context71.json')['decoder_context']]
sys.path.insert(0,str(root/'tools'));import astis_semantic_roundtrip as rt
neutral=Path('.astis/decoder-72');neutral.mkdir(exist_ok=False)
packets=[]
for i,(statement,context) in enumerate(zip([generic_stmt,actual_stmt],contexts)):
 lean=dict(statement=statement,statement_sha256=sha(statement.encode()),compiled=True,decoder_context=context)
 packet=rt.decoder_packet(dict(lean=lean))
 new(neutral/f'packet{i}.json',packet);new(r/f'anonymous.{i}.decoder.json',packet);new(r/f'anonymous.{i}.lean-context72.json',lean)
 packets.append(pin(neutral/f'packet{i}.json'))
new(neutral/'lease.open.json',dict(status='OPEN',allowed_inputs=['packet0.json','packet1.json'],source_text_visible=False,source_identity_visible=False,proof_BODY_visible=False,search_or_compiler_allowed=False))
inputs=[Path('lean-toolchain'),Path('lake-manifest.json'),Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualCorrectorChange.lean'),*paths,pre/'root.statement-seal72.json',pre/'root.header-math72.adoption.json',pre/'root.header-source72.adoption.json',pre/'library-retrieval72/retrieval.json',r/'expanded72.actual.frozen.header.lean']
new(r/'mathematics-freeze72.json',dict(status='FOCUSED_COMPILED_FROZEN_NOT_INDEPENDENTLY_REVIEWED',actual_root_PID=os.getpid(),inputs=[pin(p) for p in inputs],compiled=compiled,exact_sealed_signatures=True,new_public_analytic_premises=[],actual_parent71_reused=True,failed_first_compile_retained=(r/'typed-inner-repair/diagnosis.json').as_posix(),anonymous_packets=packets,independent_math_decoder_source_pending=True,Goal_complete=False))
graphpaths=['Libraries/conceptual-mirror-protocol.json','website/content/graph_memory_index.json','website/content/functor_hypergraph.json','Libraries/frontloaded-shared-spine.json']
assert any(x['id']=='family:discrete-hypocoercivity' for x in load(graphpaths[1])['families'])
new(r/'conceptual-mirror-audit72.json',dict(status='none-found',discovery_ids=[],checked=[pin(p) for p in graphpaths],existing_family='family:discrete-hypocoercivity',reason='Exact quadratic corrector perturbation remains within the existing discrete hypocoercivity mechanism. No new source-backed cross-domain hypothesis/conclusion map or formal transport is inferred.'))
print(json.dumps(dict(status='PASS_FOCUSED72_FROZEN',compiled=compiled,anonymous_packets=packets),ensure_ascii=False))
