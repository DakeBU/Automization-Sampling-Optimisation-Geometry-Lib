from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, subprocess, sys
sys.dont_write_bytecode = True
sys.path.insert(0, 'tools')
import astis_advance as adv
W = Path(__file__).resolve().parent.relative_to(Path.cwd())
E = Path('research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-krylov-range-semantic-evidence')
S = E.parent/'fixed-spectrum-krylov-range-statement-seal.json'
ADV = 'ASTIS-SA-20261110-GaussianComplexityFixedSpectrumKrylovRange'
sha = lambda b: hashlib.sha256(b).hexdigest()
dump = lambda x: (json.dumps(x, ensure_ascii=False, indent=2)+'\n').encode()
def put(p, b):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('xb') as f:
        f.write(b)
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
assert head == '6a7a3a454b3ded093e335f57032227d3de02663f'
assert not S.exists() and not E.exists()
for p in ['AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumKrylovRange.lean', 'Tests/GaussianComplexityFixedSpectrumKrylovRange.lean']:
    assert not Path(p).exists()
rp = Path('.astis/huanjian-resume-20261103/20261110T181711845884Z-krylov-range-literal-Prop-v3-actual-Euclidean-norm-and-inner.receipt.json')
rr = json.loads(rp.read_bytes())
assert rr['exit_code'] == 0 and rr['head_before'] == rr['head_after'] == head
assert sha(Path(rr['log']).read_bytes()) == rr['log_sha256']
P = (W/'producer-signature.draft.txt').read_bytes()
T = (W/'consumer-signature.draft.txt').read_bytes()
assert sha(P) == '4d5056d57aa0536b95af7aa9f7c3b6860ab7c9652b0bb306b6bad42434235ab6'
assert sha(T) == '082eda7b36ecff3e87a62358e4f234b6d6c129b491405de3761fa83f79412969'
probe = (W/'StatementFormation.lean').read_bytes()
assert b':= by' not in probe and b'sorry' not in probe and b'axiom' not in probe
assert 'inner ℝ' in probe.decode() and 'EuclideanSpace ℝ (Fin d)' in T.decode()
ledger = Path('runs/substantive_advances.jsonl').read_bytes()
states = adv._replay_advances([json.loads(z) for z in ledger.splitlines()])
assert ADV not in states
assert states['ASTIS-SA-20261110-GaussianComplexityFixedSpectrumCosineGram']['state'] == 'VERIFIED'
tracked = [p.decode() for p in subprocess.check_output(['git', 'ls-files', '-z']).split(b'\0') if p]
hashes, metadata = {}, []
for n in tracked:
    p = Path(n)
    if p.is_file():
        hashes[n] = sha(p.read_bytes())
    else:
        metadata.append({'path': n, 'scope': 'Non-regular tracked entry, metadata only, not traversed.'})
frontiers = {str(p): sha(p.read_bytes()) for p in Path('research-wiki/frontier-cells').rglob('*') if p.is_file()}
baseline = {'state': 'PRIVATE_FULL_FOREIGN_BASELINE_NEVER_EXPORT', 'head': head,
            'ledger_bytes': len(ledger), 'ledger_sha256': sha(ledger), 'all_foreign_states': states,
            'all_tracked_regular_file_hashes': hashes, 'all_existing_frontier_hashes': frontiers,
            'nonregular_tracked_metadata_only': metadata,
            'scope': 'Preservation hashing only. No ignored private kernel dump or restricted nested repository content/index/derivative is traversed or used as mathematics.'}
put(W/'preproof-baseline.private.json', dump(baseline))
defs = []
def literal(file, start, context):
    p = Path(file)
    raw = p.read_bytes()
    text = raw.decode('utf-8')
    a = text.index(start)
    b = text.index('\n\n', a)
    block = text[a:b]+'\n'
    defs.append({'file': str(p), 'wholefile_raw_sha256': sha(raw),
                 'kind': 'literal-canonical-definition', 'context': context,
                 'start_character_inclusive': a, 'end_character_exclusive': b,
                 'start_line_1based': text[:a].count('\n')+1,
                 'literal': block, 'literal_sha256': sha(block.encode())})
literal('.lake/packages/mathlib/Mathlib/Data/Set/Operations.lean', 'def range (f : ι → α)', 'Set.range is the actual existential image; arbitrary real coefficient functions, not a supplied span/range certificate.')
literal('.lake/packages/mathlib/Mathlib/LinearAlgebra/Span/Defs.lean', 'def span (s : Set M)', 'Submodule namespace; fixed ℝ module of functions Fin d → ℝ. General context Semiring R, AddCommMonoid M, Module R M; no norm chosen by span.')
literal('.lake/packages/mathlib/Mathlib/Data/Matrix/Mul.lean', 'def dotProduct [Mul α]', 'The ambient index m is finite. Fixed real scalar multiplication/addition in the target.')
literal('.lake/packages/mathlib/Mathlib/Data/Matrix/Mul.lean', 'def mulVec [Fintype n]', 'Matrix namespace; NonUnitalNonAssocSemiring α. Both fixed finite matrix multiplication and vector products use ordinary sums.')
literal('.lake/packages/mathlib/Mathlib/Data/Matrix/Diagonal.lean', 'def diagonal [Zero α]', 'Matrix namespace; decidable equality on finite indices, fixed real zero. Matrix powers are ordinary Nat powers in the canonical finite real matrix semiring, not entrywise powers.')
literal('.lake/packages/mathlib/Mathlib/Analysis/Normed/Lp/WithLp.lean', 'structure WithLp (p : ℝ≥0∞)', 'The literal constructor named toLp and projection ofLp identify the underlying values; this is not a norm-preserving claim about the raw function supremum norm.')
literal('.lake/packages/mathlib/Mathlib/Analysis/Normed/Lp/PiLp.lean', 'abbrev PiLp (p : ℝ≥0∞)', 'PiLp 2 supplies the L2 product structure.')
literal('.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/PiL2.lean', 'abbrev EuclideanSpace (𝕜 : Type*)', 'Fixed real scalars and finite indices. Actual norm and inner product in the consumer are those of EuclideanSpace, with WithLp.toLp shown explicitly.')
old_context = json.loads(Path('.astis/huanjian-gc-fixed-spectrum-cosine-gram-20261110/minimal-requested-orthonormal-normalization-context.json').read_bytes())
for x in old_context['definitions']:
    if x['literal'].startswith('theorem inner_eq_star_dotProduct') or x['literal'].startswith('instance (p : ℝ≥0∞)'):
        assert sha(Path(x['file']).read_bytes()) == x['wholefile_sha256']
        defs.append(x)
context = {'scope': 'Only literal canonical definitions and one Euclidean inner-product characterization statement without proof. No new-target proof/API recipe or prior reviewer verdict.', 'definitions': defs,
           'line_convention': 'UTF8-decoded Unicode character spans start-inclusive/end-exclusive; raw wholefile SHA; LF line numbering1-based. Display literals include one final LF after the selected exact definition block.'}
put(W/'minimal-definition-context.json', dump(context))
env = json.loads((W/'actual-environment-before-statement-formation.json').read_bytes())
exposure = json.loads((W/'preseal-exposure-and-planning.json').read_bytes())
exposure['additional_minimal_lookup_exposure'] = 'Subsequent minimal symbol searches showed generic WithLp.ofLp/toLp inverse and linearity rfl/header lines and one Countable exact-line false-positive. These remain honest generic preseal API exposure, not target proof search or a pristine-root claim.'
put(W/'preseal-exposure-qualified-complete.json', dump(exposure))
seal = {
 'schema': 1, 'seal_id': 'GC-FIXED-SPECTRUM-KRYLOV-RANGE-EXACT-20261110-v1',
 'state': 'EXACT_LITERAL_PROP_FORMED_UNPROVED', 'created_utc': datetime.now(timezone.utc).isoformat(),
 'source': {'version': 'arXiv2610.20492v1', 'raw': '.astis/huanjian-resume-20261103/2610.20492v1.html', 'raw_sha256': env['source_raw_sha256'],
            'anchors': ['S4.SS1.p1', 'S4.SS2.SSS0.Px1.p2', 'S4.Thmtheorem4 standing range', 'A3.SS2.p1', 'A3.SS2.p2', 'A3.Thmtheorem5 range component', 'A3.SS2.2 range proof', 'A3.SS2.p19 exact energy equalities'],
            'scope': 'Pointwise actual range(B)=Krylov for the literal hard-family spectrum and feature matrix, with an actual Euclidean norm/inner-product coordinate consumer. No concentration, sampled law, C6/absoluteC, full uniform lemma or main theorem.'},
 'producer': {'name': 'AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylovRange.actual_cosine_feature_krylov_range', 'planned_file': 'AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumKrylovRange.lean', 'signature': P.decode(), 'signature_sha256': sha(P), 'definition_kind': 'Direct theorem, all local objects literal; no public Prop alias or supplied proof certificate.'},
 'actual_private_consumer': {'name': 'AutoSamplingTheory.Tests.GaussianComplexityFixedSpectrumKrylovRange.actual_krylov_quadratic_coordinates', 'planned_file': 'Tests/GaussianComplexityFixedSpectrumKrylovRange.lean', 'signature': T.decode(), 'signature_sha256': sha(T), 'definition_kind': 'Private direct theorem, exact actual Euclidean norm/inner; existential representation must be derived from producer.', 'is_source_anchor': False, 'consumer_obligation': 'For every actual Krylov vector, materially use the producer to obtain a coefficient representation and prove actual Euclidean norm and signed weighted-inner-product identities. Not an assumed Bc representation, Gram bound or wrapper restatement.'},
 'binder_audit': [
  {'binder': 'd,q : ℕ', 'class': 'genuine-source-domain', 'meaning': 'q includes0; r=q+1, finite zero-based row/feature/power indices.'},
  {'binder': 'κ : ℝ; hκ :2≤κ', 'class': 'genuine-source-standing-hypothesis', 'source': 'S4.SS1.p1', 'internal_not_binders': ['κ-1 nonzero', 'affine polynomial change of basis / nonzero leading coefficients']},
  {'binder': 'hq :2q+1<d', 'class': 'genuine-source-standing-range', 'source': 'S4.Thmtheorem4', 'internal_not_binders': ['d>=2', 'sqrt d nonzero', 'column normalization nonzero']},
  {'binder': 'x :EuclideanSpace ℝ(Fin d × Fin(q+1))', 'class': 'pointwise-source-data-elaboration', 'meaning': 'The range proof is algebraic for every actual feature array. g_a are UNscaled underlying coordinates, as source N(0,I_d) features; B alone has d^-1/2. No Gaussian law or independence premise is required for this pointwise component.'},
  {'binder': 'private v :Fin d→ℝ and v∈K', 'class': 'genuine-consumer-object-and-domain', 'source': 'A3.SS2.p19', 'meaning': 'Select an actual source Krylov vector; coefficient c and both energy identities are conclusions, never caller certificates.'}],
 'EXCESS_public_binders': [], 'project_owned_Prop_aliases_or_hidden_bundles': [],
 'definition_semantics_audit': [
  'K uses literal ordinary matrix powers of the actual diagonal Lambda applied to unscaled g_a; it is not defined as the image of B.',
  'The image of B is an actual Set.range over all real finite coefficient vectors, not an assumed range witness.',
  'Transpose/matrix multiplication are ordinary real finite operations; feature/power paired-column order is fixed.',
  'The private norm and inner product explicitly use EuclideanSpace ℝ(Fin d) via WithLp.toLp; never the raw-function supremum norm.',
  'No O/Haar/target covariance law, measurable choice of coefficients, random-coefficient expectation factorization, oracle/cap/precision/TV/cost conclusion is supplied.'],
 'minimal_definition_context': {'path': str(W/'minimal-definition-context.json'), 'sha256': sha((W/'minimal-definition-context.json').read_bytes())},
 'no_proof_ingredient_binder': ['Chebyshev/polynomial expansion', 'nonzero leading coefficient or invertible triangular change matrix', 'nonzero sqrt/column normalization', 'rank/full-rank/nondegeneracy', 'range/span equality', 'Gram or moment identity', 'Gaussian law/independence', 'C6/absoluteC/operator norm bound'],
 'actual_statement_formation': {'receipt': str(rp), 'receipt_sha256': sha(rp.read_bytes()), 'actual_log_sha256': rr['log_sha256'], 'actual_HEAD': head, 'raw_probe': str(E/'Prop-only-statement-formation.raw.lean.txt'), 'raw_probe_sha256': sha(probe), 'scope': 'Both closed literal Prop definitions elaborated, actual exit0. No target theorem proof. hκ/hq unused-name warnings refer to proof-variable names inside Prop syntax and are retained; source conditions are not removed.'},
 'actual_environment': env,
 'honest_preseal_exposure': {'path': str(W/'preseal-exposure-qualified-complete.json'), 'sha256': sha((W/'preseal-exposure-qualified-complete.json').read_bytes()), 'root_API_pristine': False},
 'independent_source_graph_distinct_topology_and_prospective_process_gate': 'Pending. No target mathematical proof/API search or normal SAU intake until the exact qualified independent admission and preservation postguards.',
 'owner_boundary': 'Same user-authorized Goal, preserve all12 original sourceV values/foreign frontiers/queues. Original remote global owner remains active; no shared stabilization/publication work.'}
raw = dump(seal)
put(W/'statement-seal-v1.json', raw)
put(S, raw)
S.chmod(0o444)
(W/'statement-seal-v1.json').chmod(0o444)
put(E/'Prop-only-statement-formation.raw.lean.txt', probe)
put(E/'producer-signature.txt', P)
put(E/'consumer-signature.txt', T)
put(E/'minimal-definition-context.json', (W/'minimal-definition-context.json').read_bytes())
put(E/'preseal-exposure-qualified.raw.json', (W/'preseal-exposure-qualified-complete.json').read_bytes())
put(E/'actual-environment-before-statement-formation.json', dump(env))
put(E/'actual-statement-formation.json', dump(seal['actual_statement_formation']))
put(W/'StatementFormation.raw.lean.txt', probe)
(W/'StatementFormation.lean').unlink()
print(json.dumps({'seal_sha256': sha(raw), 'producer_signature_sha256': sha(P), 'consumer_signature_sha256': sha(T),
                  'actual_Lean_version': env['native_version'], 'foreign_states_preserved_in_PRIVATE_baseline': len(states), 'foreign_frontier_files': len(frontiers), 'tracked_regular_files': len(hashes),
                  'private_full_baseline_not_exported': True, 'target_proofs_and_normal_API_calls': 0}))
