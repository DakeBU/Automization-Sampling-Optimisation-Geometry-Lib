from pathlib import Path
import hashlib, json, os, re, sys

r = Path('runs/20261007-companion-priority/pbps-actual-harmonic-flow73')
pre = Path('runs/20261007-companion-priority/pbps-harmonic-flow-preproof73')
load = lambda p: json.loads(Path(p).read_bytes())
sha = lambda b: hashlib.sha256(b).hexdigest()
def pin(p):
    p = Path(p); b = p.read_bytes()
    return dict(path=p.resolve().as_posix(), RAW_bytes=len(b), RAW_sha256=sha(b),
                LF_sha256=sha(b.replace(b'\r\n', b'\n')))
def new(p, x):
    p = Path(p); assert not p.exists(), p
    p.write_text(json.dumps(x, ensure_ascii=False, indent=2) + '\n', encoding='utf8', newline='\n')

claim = load(r / 'claim.json')
name = claim['target_declarations'][0]
p = Path(claim['proposed_files'][0]); raw = p.read_bytes(); s = raw.decode()
label = 'focused-derivative-congruence-repair'
receipt = load(r / label / 'receipt.json')
assert receipt['terminal_closed'] and receipt['exit_code'] == 0
assert any(z['RAW_sha256'] == sha(raw) and Path(z['path']).resolve() == p.resolve() for z in receipt['inputs'])
log = (r / label / 'stdout.log').read_text(encoding='utf8')
m = re.search(re.escape("'" + name + "' depends on axioms: ") + r'\[([^\]]+)\]', log)
assert m
axioms = {x.strip() for x in m[1].split(',')}
assert axioms == {'propext', 'Classical.choice', 'Quot.sound'}
jobs = int(re.search(r'Build completed successfully \((\d+) jobs\)', log)[1])
original = (pre / 'header73.proposed.lean').read_text(encoding='utf8')
extra = s[:s.index('import AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient')]
assert s.startswith(extra + original)
assert not re.search(r'\b(?:sorry|admit|axiom)\b', s)
(r / 'canonical73.frozen.exactraw.lean').write_bytes(raw)
literal = s[s.index('private def actual_harmonic_flow_statement'):s.index('\ntheorem actual_harmonic_flow_laws')].rstrip()
expanded = literal.replace('private def actual_harmonic_flow_statement', 'theorem actual_harmonic_flow_laws', 1).replace(' : Prop :=\n', ' :\n', 1) + '\n'
(r / 'expanded73.frozen.header.lean').write_text(expanded, encoding='utf8', newline='\n')
statement = expanded.split('theorem actual_harmonic_flow_laws', 1)[1].rstrip('\n')
context = [
    'The ambient space is finite dimensional over the reals with its norm and real inner product, and its given measurable structure is Borel. Products have the product topology and measurable structure.',
    'gradient is the real Hilbert-space gradient obtained from the Frechet derivative through the Riesz isometry. The iterated Frechet derivative evaluated on v twice is the displayed Hessian quadratic form. ContDiff with order2 means twice continuously Frechet differentiable.',
    'All local c, Phi and H are exactly the displayed let definitions. The product coordinates z.1 and z.2 are independent vector coordinates; the norm terms in H are separate vector norms. HasDerivAt specifies the derivative at each real time.'
]
lean = dict(statement=statement, statement_sha256=sha(statement.encode()), compiled=True, decoder_context=context)
sys.path.insert(0, str(Path.cwd() / 'tools'))
import astis_semantic_roundtrip as rt
neutral = Path('.astis/decoder-73'); neutral.mkdir(exist_ok=False)
packet = rt.decoder_packet(dict(lean=lean))
new(neutral / 'packet.json', packet)
new(r / 'anonymous.decoder.json', packet)
new(r / 'anonymous.lean-context73.json', lean)
new(neutral / 'lease.open.json', dict(status='OPEN', allowed_inputs=['packet.json'], source_text_visible=False,
    source_identity_visible=False, proof_BODY_visible=False, search_or_compiler_allowed=False))
compiled = dict(declaration=name, module=pin(p), focused_receipt=pin(r / label / 'receipt.json'),
    focused_PID=receipt['actual_foreground_PID'], focused_EXIT=0, jobs=jobs, axioms=sorted(axioms), lines=len(s.splitlines()))
new(r / 'compiler-diagnoses73.json', dict(status='TWO_DISTINCT_IMPLEMENTATION_DIAGNOSES_REPAIRED_WITHOUT_STATEMENT_CHANGE',
    failures=[dict(receipt=pin(r / 'focused-initial/receipt.json'),
        diagnosis='field_simp progress assertion on already denominator-free coefficient goals; wrong sq_neg API name; broad eta rewrite nested sqrt unnecessarily.'),
        dict(receipt=pin(r / 'focused-scalar-reciprocal-repair/receipt.json'),
        diagnosis='convert generated function equalities treated as module atoms. Use HasDerivAt.congr_deriv to ask only the actual vector derivative equality.')],
    failed_logs_are_not_proof_or_axiom_certificates=True, sealed_binder_changes=[],
    late_packet_process_debt='Bounded publication packet was generated after initial implementation, before any local admission; Statement Seal/source topology were fixed before all proof search. Do not describe packet timing as pre-implementation.'))
inputs = [Path('lean-toolchain'), Path('lake-manifest.json'),
    Path('AutoSamplingTheory/TechnicalLemmas/Analysis/Calculus/Gradient.lean'), p,
    pre / 'root.statement-seal73.json', pre / 'root.header-math73.adoption.json',
    pre / 'root.header-source73.adoption.json', r / 'expanded73.frozen.header.lean']
new(r / 'mathematics-freeze73.json', dict(status='FOCUSED_COMPILED_FROZEN_NOT_INDEPENDENTLY_REVIEWED',
    actual_root_PID=os.getpid(), inputs=[pin(x) for x in inputs], compiled=[compiled],
    exact_sealed_signatures=True, extra_imports_only=extra.splitlines(), new_public_analytic_premises=[],
    anonymous_packet=pin(neutral / 'packet.json'), independent_math_decoder_source_pending=True, Goal_complete=False))
graphs = ['Libraries/conceptual-mirror-protocol.json', 'website/content/graph_memory_index.json',
          'website/content/functor_hypergraph.json', 'Libraries/frontloaded-shared-spine.json']
new(r / 'conceptual-mirror-audit73.json', dict(status='none-found', discovery_ids=[], checked=[pin(x) for x in graphs],
    reason='Actual harmonic rotation and weighted-energy preservation are deterministic ingredients in one existing PBPS source. No new reviewed cross-domain hypothesis/conclusion map or formal transport is inferred, and no Gaussian/PDMP invariance follows from this identity.'))
print(json.dumps(dict(status='PASS_FOCUSED73_FROZEN', compiled=compiled, anonymous_packet=pin(neutral / 'packet.json'))))
