from pathlib import Path
import hashlib,json,sys
root=Path.cwd();sys.path.insert(0,str(root/'tools'))
import astis_semantic_roundtrip as rt
r=Path('runs/20261007-companion-priority/pbps-actual-projected-rotation70')
pre=Path('runs/20261007-companion-priority/pbps-actual-projected-rotation-preproof70')
sha=lambda b:hashlib.sha256(b).hexdigest()
def load(p):return json.loads(Path(p).read_bytes())
def new(p,x):
 p=Path(p);assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
freeze=load(r/'math-freeze.theorem-only70.json')
assert freeze['status']=='FOCUSED_CANONICAL70_COMPILED_FROZEN_NOT_INDEPENDENTLY_REVIEWED'
header=(pre/'header0-proposed-expanded.lean').read_text(encoding='utf-8')
prefix='theorem actual_projected_rotation';assert header.startswith(prefix)
stmt=header[len(prefix):].rstrip('\n')
context=list(load('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261009-PBPSActualReflectionIntertwining.json')['lean']['decoder_context'])
context.append('For each globally mean-zero input f, the output g is exactly U(P f-(f-P f)). Its macro vector is the conditional-expectation component identified by the displayed inclusion; its second vector is V0.adjoint(R g). These output components are not defined by the asserted right-hand sides. The zero output mean is a conclusion, not an input premise.')
lean=dict(statement=stmt,statement_sha256=sha(stmt.encode()),compiled=True,decoder_context=context)
packet=rt.decoder_packet(dict(lean=lean))
neutral=Path('.astis/decoder-70');neutral.mkdir(exist_ok=False)
new(neutral/'packet0.json',packet);new(r/'anonymous.0.decoder.json',packet)
new(neutral/'lease.json',dict(status='OPEN',allowed_inputs=['packet0.json'],source_text_visible=False,source_identity_visible=False,compiler_started=False))
(neutral/'initial-lease.raw.snapshot.json').write_bytes((neutral/'lease.json').read_bytes())
new(r/'anonymous.lean-context70.json',lean)
names=['Libraries/conceptual-mirror-protocol.json','website/content/graph_memory_index.json','website/content/functor_hypergraph.json','Libraries/frontloaded-shared-spine.json']
data=[load(p) for p in names]
families=[x for x in data[1]['families'] if x['id']=='family:discrete-hypocoercivity'];assert len(families)==1
new(r/'conceptual-mirror-audit70.json',dict(status='none-found',discovery_ids=[],
 checked=[dict(path=p,RAW_sha256=sha(Path(p).read_bytes())) for p in names],
 existing_family=families[0]['id'],
 reason='The actual macro/polar rotation and pair-energy cancellation instantiate the existing reflection/modified-L2 family. No new source-backed cross-domain hypothesis/conclusion transport or recurring mechanism beyond this retained family was found. Gaussian coordinate-law rotation is already separately retained and has a distinct law-level truth contract. No conceptual edge is promoted to a Lean dependency.'))
print('PASS anonymous70 packet frozen from exact fully expanded proposition and approved minimal definitions; no source identity/BODY/publication metadata supplied. Mirror audit none-found within existing retained family.')
