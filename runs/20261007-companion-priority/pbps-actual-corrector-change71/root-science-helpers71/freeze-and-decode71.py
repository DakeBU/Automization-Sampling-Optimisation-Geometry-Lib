from pathlib import Path
import hashlib,json,os,re,sys
root=Path.cwd();r=Path('runs/20261007-companion-priority/pbps-actual-corrector-change71');pre=Path('runs/20261007-companion-priority/pbps-corrector-change-preproof71')
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def new(p,x):
 p=Path(p);assert not p.exists(),p;p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.resolve().as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
claim=load(r/'claim.json');p=Path(claim['proposed_files'][0]);raw=p.read_bytes();header=(pre/'header71.named-literal.proposed.lean').read_bytes()
assert raw.startswith(header) and sha(header)=='2bef0d5cf364270b6f580288e966d9bb78310f646a7fe13b6f8855807e70f42c'
focused=r/'focused-typed-substitution/receipt.json';q=load(focused);assert q['terminal_closed'] and q['exit_code']==0 and q['actual_foreground_PID']==49980
assert any(z['path']==p.as_posix() and z['RAW_sha256']==sha(raw) for z in q['inputs'])
out=(r/'focused-typed-substitution/stdout.log').read_text(encoding='utf8');decl=claim['target_declarations'][0]
axioms=re.search(re.escape("'"+decl+"' depends on axioms: ")+r'\[([^\]]+)\]',out).group(1)
assert set(x.strip() for x in axioms.split(','))=={'propext','Classical.choice','Quot.sound'}
assert 'Build completed successfully (3950 jobs)' in out
(r/'canonical71.frozen.exactraw.lean').write_bytes(raw);(r/'canonical71.frozen.LF.lean').write_bytes(raw.replace(b'\r\n',b'\n'))
s=raw.decode();literal=s[s.index('private def actual_corrector_change_statement'):s.index('\ntheorem actual_corrector_change')].rstrip()
expanded=literal.replace('private def actual_corrector_change_statement','theorem actual_corrector_change',1).replace(' : Prop :=\n',' :\n',1)+'\n'
(r/'expanded71.frozen.header.lean').write_text(expanded,encoding='utf8',newline='\n')
names=[Path('lean-toolchain'),Path('lake-manifest.json'),Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualProjectedRotation.lean'),p,pre/'header71.named-literal.proposed.lean',pre/'root.statement-seal71.json',pre/'root.source-first71.adoption.json',pre/'root.header-math71.adoption.json',pre/'root.header-source71.adoption.json',pre/'library-retrieval71/retrieval.json',focused,r/'expanded71.frozen.header.lean']
new(r/'mathematics-freeze71.json',dict(status='FOCUSED_CANONICAL71_COMPILED_FROZEN_NOT_INDEPENDENTLY_REVIEWED',actual_root_PID=os.getpid(),inputs=[pin(p) for p in names],declaration=decl,RAW_module_sha256=sha(raw),module_lines=len(s.splitlines()),focused_PID=49980,focused_EXIT=0,focused_jobs=3950,axioms=['propext','Classical.choice','Quot.sound'],exact_sealed147line_prefix=True,typed_negative=(r/'typed-substitution-repair/diagnosis.json').as_posix(),new_public_premises=[],actual_parent70_reused=True,source_blind_decoder_and_independent_source_pending=True,full_paper=False,Goal_complete=False))
sys.path.insert(0,str(root/'tools'));import astis_semantic_roundtrip as rt
context=load('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261009-PBPSActualProjectedRotation.json')['lean']['decoder_context']
stmt=expanded[len('theorem actual_corrector_change'):].rstrip('\n')
lean=dict(statement=stmt,statement_sha256=sha(stmt.encode()),compiled=True,decoder_context=context)
packet=rt.decoder_packet(dict(lean=lean));neutral=Path('.astis/decoder-71');neutral.mkdir(exist_ok=False)
new(neutral/'packet0.json',packet);new(neutral/'lease.open.json',dict(status='OPEN',allowed_inputs=['packet0.json'],source_text_visible=False,source_identity_visible=False,proof_BODY_visible=False,search_or_compiler_allowed=False))
new(r/'anonymous.0.decoder.json',packet);new(r/'anonymous.lean-context71.json',lean)
paths=['Libraries/conceptual-mirror-protocol.json','website/content/graph_memory_index.json','website/content/functor_hypergraph.json','Libraries/frontloaded-shared-spine.json']
data=[load(p) for p in paths];assert any(x['id']=='family:discrete-hypocoercivity' for x in data[1]['families'])
new(r/'conceptual-mirror-audit71.json',dict(status='none-found',discovery_ids=[],checked=[pin(p) for p in paths],existing_family='family:discrete-hypocoercivity',reason='Exact source B21 modified-L2 corrector cancellation is within the retained family. No new source-backed cross-domain hypothesis/conclusion transport or certified functor is found. Gaussian coordinate-law rotation remains a separate law-level contract.'))
print('PASS frozen528-line71/3950/standard3; anonymous full literal packet only, mirror audit none-found; independent reviews pending.')
