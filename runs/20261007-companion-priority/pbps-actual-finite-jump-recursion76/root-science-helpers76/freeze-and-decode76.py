from pathlib import Path
import hashlib,json,os,re,sys
r=Path('runs/20261007-companion-priority/pbps-actual-finite-jump-recursion76');pre=r.parent/'pbps-recursive-preproof76'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.resolve().as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
def new(p,x):
 p=Path(p);assert not p.exists(),p;p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
claim=load(r/'claim.json');decl=claim['target_declarations'][0];p=Path(claim['proposed_files'][0]);raw=p.read_bytes();s=raw.decode()
header=(pre/'header76.v3.proposed.lean').read_text(encoding='utf8');marker='theorem actual_fixed_reference_finite_jump_recursion\n'
literal=header[header.index('private def actual_fixed_reference_finite_jump_recursion_statement'):header.index('\ntheorem actual_fixed_reference')].rstrip()
actual_literal=s[s.index('private def actual_fixed_reference_finite_jump_recursion_statement'):s.index('\nset_option maxHeartbeats')].rstrip()
assert actual_literal==literal
a=s.index(marker);end=s.index(':= by\n',a)+len(':= by\n');assert s[a:end]==marker+header.split(marker,1)[1]
assert not re.search(r'\b(?:sorry|admit|axiom)\b',s)
label=sys.argv[1];q=load(r/label/'receipt.json');assert q['terminal_closed'] and q['exit_code']==0
assert any(Path(z['path']).resolve()==p.resolve() and z['RAW_sha256']==sha(raw) for z in q['inputs'])
log=(r/label/'stdout.log').read_text(encoding='utf8');m=re.search(r'Build completed successfully \((\d+) jobs\)',log);assert m
ax=load(r/'axioms/receipt.json');assert ax['terminal_closed'] and ax['exit_code']==0
al=(r/'axioms/stdout.log').read_text(encoding='utf8');am=re.search(re.escape("'"+decl+"' depends on axioms: ")+r'\[([^\]]+)\]',al);assert am
axioms={x.strip() for x in am[1].split(',')};assert axioms=={'propext','Classical.choice','Quot.sound'}
frozen=r/'canonical76.frozen.exactraw.lean';assert not frozen.exists();frozen.write_bytes(raw)
expanded=literal.replace('private def actual_fixed_reference_finite_jump_recursion_statement','theorem actual_fixed_reference_finite_jump_recursion',1).replace(' : Prop :=\n',' :\n',1)+'\n'
ep=r/'expanded76.frozen.header.lean';assert not ep.exists();ep.write_text(expanded,encoding='utf8',newline='\n')
statement=expanded.split('theorem actual_fixed_reference_finite_jump_recursion',1)[1].rstrip('\n')
context=[
 'The ambient real inner-product space is finite-dimensional, with its compatible norm and Borel measurable structure. Rank zero is allowed. Products use product topology and measurable structure; the sequence space uses the product measurable structure.',
 'gradient is the Hilbert gradient represented by the Frechet derivative. The displayed iterated Frechet derivative evaluated twice on v is the Hessian quadratic form. ContDiff of order two means twice continuously Frechet differentiable.',
 'All eleven displayed let definitions are literal. Real division is total, including division by zero. The square root is the nonnegative real square root. H uses the sum of two separate squared vector norms and the displayed cap C uses that same phase energy.',
 'NNReal is the set of nonnegative reals. WithTop NNReal adjoins a largest element infinity. untopD d takes the finite value, with default d at infinity; its use in the active successor is guarded by non-infinity. Real.toNNReal is the nonnegative part.',
 'Sum is the disjoint union. Sum.inl (T,z) represents a finite nonnegative time and a phase; Sum.inr () has no phase coordinate. Sum.elim applies its left or right function according to that tag. Unit has one element. The stopped branch has extended event time infinity.',
 'The displayed interval integral is the real Lebesgue integral on the oriented interval. hittingAfter is the infimum of times at or after the start whose process value belongs to the target set, returning infinity if the set is empty.',
 'Nat.rec starts with the displayed initial value and applies the successor rule once for each index. The threshold sequence e has arbitrary nonnegative entries; all zero entries are allowed. Its n-th entry is used between records n and n+1.',
 'Monotone means order preserving. Measurable means Borel measurable for the displayed finite-dimensional and extended-time spaces, with product and disjoint-union structures. All implications and finite/stopped/positive guards are part of the conclusion.'
]
lean=dict(statement=statement,statement_sha256=sha(statement.encode()),compiled=True,decoder_context=context)
sys.path.insert(0,str(Path.cwd()/'tools'));import astis_semantic_roundtrip as rt
neutral=Path('.astis/decoder-76');neutral.mkdir(exist_ok=False);packet=rt.decoder_packet(dict(lean=lean))
new(neutral/'packet.json',packet);new(r/'anonymous.decoder.json',packet);new(r/'anonymous.lean-context76.json',lean)
new(neutral/'lease.open.json',dict(status='OPEN',allowed_inputs=['packet.json'],source_text_visible=False,source_identity_visible=False,proof_BODY_visible=False,search_or_compiler_allowed=False))
compiled=dict(declaration=decl,module=pin(p),focused_receipt=pin(r/label/'receipt.json'),focused_PID=q['actual_foreground_PID'],focused_EXIT=0,jobs=int(m[1]),axioms_receipt=pin(r/'axioms/receipt.json'),axioms_PID=ax['actual_foreground_PID'],axioms=sorted(axioms),lines=len(s.splitlines()))
inputs=[Path('lean-toolchain'),Path('lake-manifest.json'),p,*[Path('AutoSamplingTheory/ExampleCases/ProximalBPS')/(n+'.lean') for n in ['ActualHarmonicFlow','ActualBounceRate','ActualHazardClock']],pre/'root.statement-seal76.json',pre/'root.header-reviews76.adoption.json',ep]
new(r/'mathematics-freeze76.json',dict(status='FOCUSED_COMPILED_FROZEN_NOT_INDEPENDENTLY_REVIEWED',actual_root_PID=os.getpid(),inputs=[pin(x) for x in inputs],compiled=[compiled],exact_sealed_signatures=True,new_public_analytic_premises=[],anonymous_packet=pin(neutral/'packet.json'),independent_math_decoder_source_pending=True,Goal_complete=False))
graphs=['Libraries/conceptual-mirror-protocol.json','website/content/graph_memory_index.json','website/content/functor_hypergraph.json','Libraries/frontloaded-shared-spine.json']
new(r/'conceptual-mirror-audit76.json',dict(status='none-found',discovery_ids=[],checked=[pin(x) for x in graphs],reason='Actual finite stopped iteration of the already compiled deterministic flow, bounce and first clock with inherited original-energy rate bound. No new cross-domain correspondence or stochastic process transport is certified. iid/SLLN/nonaccumulation, global phase, invariance and unbounded expected costs remain separate.'))
print(json.dumps(dict(status='PASS_FOCUSED76_FROZEN',compiled=compiled,anonymous_packet=pin(neutral/'packet.json'))))
