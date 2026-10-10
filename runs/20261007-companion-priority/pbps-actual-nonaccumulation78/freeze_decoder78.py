from pathlib import Path
import hashlib,json,sys
r=Path('runs/20261007-companion-priority/pbps-actual-nonaccumulation78')
f=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualNonaccumulation.lean'); b=f.read_bytes(); s=b.decode()
seal=json.loads((r/'root.statement-seal78.json').read_bytes())
h=Path(seal['header']['path']).read_text(encoding='utf8')
literal=h.split('private def actual_fixed_reference_event_time_nonaccumulation_statement',1)[1].split('\nend\n',1)[0].rstrip()
actual=s.split('private def actual_fixed_reference_event_time_nonaccumulation_statement',1)[1].split('\n\nset_option',1)[0].rstrip()
assert literal==actual
q=json.loads((r/'focused78-attempt2/receipt.json').read_bytes()); assert q['exit_code']==0 and q['source_RAW_sha256']==hashlib.sha256(b).hexdigest()
statement=literal.replace(' : Prop :=\n',' :\n',1)
context=[
 'All displayed functions and objects are literal definitions. The potential is real-valued on a finite-dimensional real inner-product space with its Borel measurable structure; dimension zero is allowed. The six analytic hypotheses are the only supplied mathematical premises. fderiv is the Frechet derivative, gradient is the real inner-product gradient, and ContDiff real 2 means twice continuously differentiable.',
 'expMeasure 1 is the rate-one exponential measure on the real line. infinitePi is the canonical countable product on all real sequences. toNNReal is max(x,0) viewed as a nonnegative real, including exceptional nonpositive coordinates.',
 'hittingAfter f s 0 a denotes the infimum of nonnegative times at which f(t)(a) belongs to s, with infinity for an empty hit set. WithTop NNReal includes a greatest element top. untopD 0 returns the finite value when finite, and zero at top; the guard branches before evaluating a finite-state update.',
 'Sum.inl stores a finite accumulated time and state pair. Sum.inr Unit is the absorbing stopped record, represented by eventTime top and carrying no state at infinity. Nat.rec initializes at (0,z0) and uses coordinate k in update k to k+1.',
 'For each fixed displayed deterministic parameter triple, the conclusion holds almost everywhere under the literal product P. Eventually n in atTop means all sufficiently large natural indices. Every tested horizon t is finite. Set.Finite refers to finitely many natural indices, including initialization index0. The conclusion does not assert that every sequence eventually stops or that finite times become equal to infinity.'
]
lean=dict(statement=statement,statement_sha256=hashlib.sha256(statement.encode()).hexdigest(),compiled=True,decoder_context=context)
sys.path.insert(0,str(Path.cwd()/'tools')); import astis_semantic_roundtrip as rt
packet=rt.decoder_packet(dict(lean=lean))
def new(p,x):
 p=Path(p); assert not p.exists(); p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
d=Path('.astis/decoder-78');d.mkdir(exist_ok=False)
new(d/'packet.json',packet);new(r/'anonymous.decoder78.json',packet);new(r/'anonymous.lean-context78.json',lean)
new(r/'mathematics-freeze78.json',dict(status='FOCUSED_COMPILED_EXACT_SEALED_STATEMENT_REVIEW_PENDING',module=f.as_posix(),module_RAW_sha256=hashlib.sha256(b).hexdigest(),compiler_receipt=(r/'focused78-attempt2/receipt.json').as_posix(),header_RAW_sha256=seal['header']['RAW_sha256'],anonymous_packet_sha256=packet['packet_sha256'],Goal_complete=False))
print('anonymous packet generated, exact private literal matches seal')
