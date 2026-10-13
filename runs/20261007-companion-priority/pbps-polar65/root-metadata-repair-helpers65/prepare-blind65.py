from pathlib import Path
import ast,hashlib,json,sys
root=Path.cwd();sys.path.insert(0,'tools');import astis_semantic_roundtrip as rt
pre=root/'runs/20261007-companion-priority/pbps-polar-preproof65';r=root/'runs/20261007-companion-priority/pbps-polar65';out=root/'.astis/decoder-65';out.mkdir(exist_ok=False)
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
receipt=load(r/'focused65-v2/receipt.json');assert receipt['exit_code']==1
log=(r/'focused65-v2/stdout.log').read_text(encoding='utf-8')
assert "'AutoSamplingTheory.ExampleCases.ProximalBPS.PolarIsometry.actual_centered_polar_isometry' depends on axioms: [propext," in log
assert not any('error:' in s and 'AutoSamplingTheory/ExampleCases/ProximalBPS/PolarIsometry.lean' in s for s in log.splitlines())
sig=(pre/'header0.lean').read_text(encoding='utf-8');name='actual_centered_polar_isometry';statement=sig[len('theorem '+name):].rstrip('\n')
tree=ast.parse((root/'.astis/pbps-polar65/freeze-reader65.py').read_text(encoding='utf-8'))
node=next(n for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='context' for t in n.targets));context=ast.literal_eval(node.value)
packet=rt.decoder_packet(dict(lean=dict(statement=statement,statement_sha256=sha(statement.encode()),compiled=True,decoder_context=context)))
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
write(out/'packet0.json',packet);write(r/'anonymous.0.decoder.json',packet)
write(out/'lease.json',dict(status='OPEN',allowed_inputs=['packet0.json'],source_text_visible=False,source_identity_visible=False,compiler_started=False));(out/'initial-lease.raw.snapshot.json').write_bytes((out/'lease.json').read_bytes())
write(r/'decoder-early-statement-only65.json',dict(scope='Blind reconstruction of exact independently sealed production statement only; production compiled in v2. Failed consumer is not credited and full focused/source/publication admission remains pending.',production_compiler_receipt=(r/'focused65-v2/receipt.json').relative_to(root).as_posix(),packet_RAW_sha256=sha((out/'packet0.json').read_bytes()),source_text_visible=False,source_identity_visible=False,Test_compiled=False,PROVED_LOCAL=False))
print('Neutral statement-only packet ready; production compiled, full focused consumer still pending.')
