from pathlib import Path
import hashlib,json,os,re,sys
r=Path('runs/20261007-companion-priority/pbps-actual-bounce-rate74');pre=r.parent/'pbps-bounce-rate-preproof74'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.resolve().as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
def new(p,x):
 p=Path(p);assert not p.exists(),p;p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
claim=load(r/'claim.json');decl=claim['target_declarations'][0];p=Path(claim['proposed_files'][0]);raw=p.read_bytes();s=raw.decode();header=(pre/'header74.proposed.lean').read_bytes();assert raw.startswith(header)
assert not re.search(r'\b(?:sorry|admit|axiom)\b',s)
label=sys.argv[1];q=load(r/label/'receipt.json');assert q['terminal_closed'] and q['exit_code']==0
assert any(Path(z['path']).resolve()==p.resolve() and z['RAW_sha256']==sha(raw) for z in q['inputs'])
log=(r/label/'stdout.log').read_text(encoding='utf8');m=re.search(r'Build completed successfully \((\d+) jobs\)',log);assert m
ax=load(r/'axioms/receipt.json');assert ax['terminal_closed'] and ax['exit_code']==0
al=(r/'axioms/stdout.log').read_text(encoding='utf8');am=re.search(re.escape("'"+decl+"' depends on axioms: ")+r'\[([^\]]+)\]',al);assert am
axioms={x.strip() for x in am[1].split(',')};assert axioms=={'propext','Classical.choice','Quot.sound'}
frozen=r/'canonical74.frozen.exactraw.lean';assert not frozen.exists();frozen.write_bytes(raw)
literal=s[s.index('private def actual_bounce_rate_energy_statement'):s.index('\ntheorem actual_bounce_rate_energy_laws')].rstrip()
expanded=literal.replace('private def actual_bounce_rate_energy_statement','theorem actual_bounce_rate_energy_laws',1).replace(' : Prop :=\n',' :\n',1)+'\n'
ep=r/'expanded74.frozen.header.lean';assert not ep.exists();ep.write_text(expanded,encoding='utf8',newline='\n')
statement=expanded.split('theorem actual_bounce_rate_energy_laws',1)[1].rstrip('\n')
context=['The ambient space is finite-dimensional over the reals with its compatible norm and real inner product; its given measurable structure is Borel. Product spaces use product topology and measurable structure. Rank zero is allowed.','gradient is the Hilbert gradient represented by the Frechet derivative. The displayed iterated Frechet derivative applied twice to v is the Hessian quadratic form. ContDiff order 2 means twice continuously Frechet differentiable.','Every c,h,R,S,rate,H is exactly the displayed let definition. Real division is total, including division by zero; max is the ordinary real maximum. The two norms in H are separate vector norms and form a weighted sum. No stochastic interpretation is supplied.']
lean=dict(statement=statement,statement_sha256=sha(statement.encode()),compiled=True,decoder_context=context)
sys.path.insert(0,str(Path.cwd()/'tools'));import astis_semantic_roundtrip as rt
neutral=Path('.astis/decoder-74');neutral.mkdir(exist_ok=False);packet=rt.decoder_packet(dict(lean=lean))
new(neutral/'packet.json',packet);new(r/'anonymous.decoder.json',packet);new(r/'anonymous.lean-context74.json',lean)
new(neutral/'lease.open.json',dict(status='OPEN',allowed_inputs=['packet.json'],source_text_visible=False,source_identity_visible=False,proof_BODY_visible=False,search_or_compiler_allowed=False))
compiled=dict(declaration=decl,module=pin(p),focused_receipt=pin(r/label/'receipt.json'),focused_PID=q['actual_foreground_PID'],focused_EXIT=0,jobs=int(m[1]),axioms_receipt=pin(r/'axioms/receipt.json'),axioms_PID=ax['actual_foreground_PID'],axioms=sorted(axioms),lines=len(s.splitlines()))
inputs=[Path('lean-toolchain'),Path('lake-manifest.json'),p,Path('AutoSamplingTheory/TechnicalLemmas/Analysis/QuadraticRegularization.lean'),pre/'root.statement-seal74.json',pre/'root.header-reviews74.adoption.json',ep]
new(r/'mathematics-freeze74.json',dict(status='FOCUSED_COMPILED_FROZEN_NOT_INDEPENDENTLY_REVIEWED',actual_root_PID=os.getpid(),inputs=[pin(x) for x in inputs],compiled=[compiled],exact_sealed_signatures=True,new_public_analytic_premises=[],anonymous_packet=pin(neutral/'packet.json'),independent_math_decoder_source_pending=True,Goal_complete=False))
graphs=['Libraries/conceptual-mirror-protocol.json','website/content/graph_memory_index.json','website/content/functor_hypergraph.json','Libraries/frontloaded-shared-spine.json']
new(r/'conceptual-mirror-audit74.json',dict(status='none-found',discovery_ids=[],checked=[pin(x) for x in graphs],reason='The actual state-dependent zero-safe reflection, positive-part rate and one-energy-layer majorant are prerequisites of one existing PBPS construction. Generic orthogonal reflection is reused directly; no new cross-domain hypothesis/conclusion correspondence is claimed. Energy conservation does not imply path-law invariance or nonexplosion.'))
print(json.dumps(dict(status='PASS_FOCUSED74_FROZEN',compiled=compiled,anonymous_packet=pin(neutral/'packet.json'))))
