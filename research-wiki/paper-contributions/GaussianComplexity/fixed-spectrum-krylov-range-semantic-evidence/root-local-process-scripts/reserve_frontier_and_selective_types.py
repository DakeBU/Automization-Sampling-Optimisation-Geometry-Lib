from pathlib import Path
import hashlib, json, subprocess, sys
sys.dont_write_bytecode = True
sys.path.insert(0, 'tools')
import astis_advance as adv
W = Path(__file__).resolve().parent.relative_to(Path.cwd())
E = Path('research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-krylov-range-semantic-evidence')
C = Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-krylov-range.json')
S = E.parent/'fixed-spectrum-krylov-range-statement-seal.json'
ADV = 'ASTIS-SA-20261110-GaussianComplexityFixedSpectrumKrylovRange'
OWNER = 'huanjian_gc_20261110_fixed_spectrum_krylov_range'
sha = lambda b: hashlib.sha256(b).hexdigest()
dump = lambda x: (json.dumps(x, ensure_ascii=False, indent=2)+'\n').encode()
def put(p, b):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('xb') as f:
        f.write(b)
assert not C.exists()
seal_raw = S.read_bytes()
assert sha(seal_raw) == 'f47e23a601d1a8e0ff4760224676313e0f1999877a97156841a65c01847e5d82'
assert seal_raw == (W/'statement-seal-v1.json').read_bytes()
s = json.loads(seal_raw)
base_raw = (W/'preproof-baseline.private.json').read_bytes()
base = json.loads(base_raw)
assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip() == base['head']
def guard():
    for p, h in base['all_tracked_regular_file_hashes'].items():
        assert sha(Path(p).read_bytes()) == h, p
    for p, h in base['all_existing_frontier_hashes'].items():
        assert sha(Path(p).read_bytes()) == h, p
    ledger = Path('runs/substantive_advances.jsonl').read_bytes()
    assert sha(ledger) == base['ledger_sha256'] and len(ledger) == base['ledger_bytes']
    states = adv._replay_advances([json.loads(z) for z in ledger.splitlines()])
    assert states == base['all_foreign_states'] and ADV not in states
guard()
memory = Path('research-wiki/process-memory.json')
pm = json.loads(memory.read_bytes())
assert len(pm['entries']) == 3
process = {'path': str(memory), 'sha256': sha(memory.read_bytes()), 'entries_checked': [x['id'] for x in pm['entries']],
           'applicable_process_memory_ids': [], 'reason': 'The three existing entries address tilted-law Fisher base measures and gradient-flow/descent domains. They impose no new mathematical assumption on this pointwise finite-dimensional algebra packet. Process memory is never proof authority.'}
put(E/'process-memory-applicability.json', dump(process))
name = s['producer']['name']
anchor = 'arXiv2610.20492v1 S4.SS1.p1; S4.SS2.SSS0.Px1.p2; A3.Thmtheorem5/A3.SS2.2 range component; A3.SS2.p19 exact Euclidean energy equalities'
boundary = ('Reserved planning fragment only: exact literal statements formed, not target proofs or normal SAU intake. '
            'Source d/q natural with2q+1<d includingq0, kappa>=2; arbitrary pointwise feature arrays. '
            'Actual unscaled g, d^-1/2 B and ordinary diagonal-matrix Krylov powers. '
            'Producer must prove actual image=span; private consumer must materially derive coefficient representation '
            'and actual Euclidean norm/weighted-inner identities. No supplied rank, invertibility, span, moment or Gram certificate. '
            'C6/concentration/absoluteC/full Lemma4.4, Haar/joint/adaptive/Borel coefficient selection, actual '
            'oracle/exact-matvec/precision/TV/dimension-condition-number/deterministic query-cap/explicit expected-cost '
            'adapters, both mains, sourceV/global/site/browser/publication/purification/ExpositionSeal/Goal remain separate. '
            'All12 prior original sourceV values, frontiers, queues and other ASTIS chat remain intact; original global lease not transferred.')
searches = ['Samplinglib: bounded Gaussian module/declaration/frontier name inventory found no existing Krylov-range target or planned exact names; current selected C5 component is not supplied by a known compiled range node.',
            'Mathlib: literal Set.range/Submodule.span/Matrix.diagonal/mulVec/dotProduct/WithLp/PiLp/EuclideanSpace definitions and one metric characterization header audited. General new-target proof-API retrieval waits for independent admission; root generic prior/adjacent-API exposure is disclosed.']
c = {'schema_version': 3, 'cell_id': C.stem, 'route': 'samplewiki-route', 'mode': 'faithfulPaper',
     'title': 'Actual cosine-feature Krylov range with genuine Euclidean energy coordinates',
     'source_anchor': anchor, 'target_statement': s['producer']['signature'],
     'status': 'claimed', 'owner_id': OWNER, 'advance_id': ADV,
     'parents': ['source:arXiv2610.20492v1 selected C5 range and C2 pointwise energy component; actual compiled parent set is not yet known'],
     'consumers': ['GaussianComplexity actual Krylov quadratic-coordinate consumer', 'GaussianComplexity Lemma4.4 uniform-space argument'],
     'shared_floor_audit': {'searched': searches, 'classification': 'missing', 'decision': 'new_route_local', 'canonical_declaration': '', 'canonical_shared_cell': ''},
     'reuse_plan': {'searched_existing': searches, 'reused_declarations': ['Matrix.mulVec', 'Matrix.diagonal', 'Submodule.span', 'Set.range', 'WithLp.ofLp', 'WithLp.toLp', 'EuclideanSpace'],
                    'new_shared_declarations': [], 'known_consumers': [], 'planned_consumers': [s['actual_private_consumer']['name']],
                    'no_duplicate_wrapper': True, 'decision_reason': 'Prove the literal hard-family range equality, then genuinely transport actual Euclidean norm and signed energy for each source Krylov vector. A supplied span equality or a restatement wrapper is not progress.'},
     'reader_contract': {'reference_standard': 'textbook/chapter-01/section-1-3.html',
                         'source_ordered': False, 'source_statement_adjacent': False, 'natural_language_formula_proof': False,
                         'hidden_assumptions_visible': False, 'lean_collapsed': False, 'external_dependencies_visible': False,
                         'status': 'Prospective requirements only; no lesson or reader acceptance yet.'},
     'graph_contribution': {'lean_view': 'new-node', 'overview_view': 'no-change-with-reason', 'functor_view': 'pending-audit',
                            'edge_semantics': 'formal-solid; overlays-dashed', 'color_semantics': 'evidence-status; library-scope',
                            'focus_targets': [name], 'visual_review': 'Planned target only, no compiled edge or new global graph/source-index/site update. Source DAG is not the compiler DAG.'},
     'learning_contract': {'control_plane_math_authority': False, 'process_memory_checked': True, 'process_memory_ids': [],
                           'failure_class': 'IMPLEMENTATION_FAILED',
                           'salvage': {'required': True, 'status': 'completed',
                                       'reason': 'The unsealed reserved lambda identifier was alpha-renamed; actual parser failure retained, final literal Prop formation exit0. Coordinate-energy draft was explicitly elaborated to actual Euclidean norm/inner before sealing. Original metadata span/LF mismatch is preserved with a separately auditable exact-locator overlay; no target theorem/proof or source repair is claimed.', 'promoted_fragments': [], 'discarded_fragments': []},
                           'parallelism': {'decision': 'serial', 'direction_fingerprints': [], 'expected_information_gain': 'Root alone proves mathematics. Independent raw source graph and distinct topology roles address separate epistemic checks, not competing Lean proofs.', 'shared_verified_context_digest': ''},
                           'cross_route_blind_spot_audit': {'required': False, 'status': 'not-applicable', 'evidence': '', 'canonical_route': '', 'selection_reason': 'No parallel mathematical implementation routes.'},
                           'reader_backpressure': {'purification_status': 'pending', 'exposition_seal_status': 'pending', 'exposition_evidence': '', 'source_expansion_nodes': [], 'lean_expansion_nodes': [], 'assumptions_preserved': False, 'boundary_preserved': False}},
     'source_detail_audit': {'primary_edition': 'arXiv2610.20492v1 fixed raw6bc5ddc1...', 'primary_anchor': anchor,
                            'detail_status': 'sufficient', 'gap': 'No source gap or mathematical repair accepted. Source states a polynomial triangular-basis route; all background/normalization/power/metric steps still require independent expansion and actual proof.',
                            'fidelity_boundary': boundary},
     'statement_seal': {'status': 'EXACT_LITERAL_PROP_FORMED_UNPROVED;INDEPENDENT_SOURCE_TOPOLOGY_PENDING', 'file': str(S), 'sha256': sha(seal_raw), 'signature_sha256': s['producer']['signature_sha256']},
     'evidence': {'focused_checks': [s['actual_statement_formation']['receipt']], 'independent_verification': '',
                  'source_review': 'Distinct independent source/topology raw-first reviews are in progress; no target proof or sourceV.',
                  'execution_boundary': boundary, 'definition_locator_overlay': str(E/'minimal-definition-context-exact-LF.json'),
                  'prior_results_preserved': 'All299 previous states,459 existing frontier files and128851 tracked regular files were guarded before and after this new-only fragment reservation; full private baseline is never exported.'},
     'blocked': {'reason': '', 'children': []},
     'owned_files': [s['producer']['planned_file'], s['actual_private_consumer']['planned_file'], str(C), str(S), str(E), 'website/content/declaration_lessons/huanjian-fixed-spectrum-krylov-range.json', 'website/content/publications/huanjian-fixed-spectrum-krylov-range.json', 'research-wiki/semantic-roundtrip/audits/huanjian-fixed-spectrum-krylov-range.json'],
     'forbidden_shared_files': ['AutoSamplingTheory.lean', 'Tests.lean', 'Registry.lean', 'research-wiki/semantic-roundtrip/registry.json', 'website/content/source_correspondence.json', 'website/content/graph_memory_index.json', 'website/content/functor_hypergraph.json'],
     'truth_boundary': boundary, 'conceptual_mirror_audit': None}
put(C, dump(c))
context_raw = (W/'minimal-definition-context-exact-LF.json').read_bytes()
ctx = json.loads(context_raw)
packet = {'schema': 1, 'scope': 'Selective exact planned types and necessary canonical definition context only. No candidate proof, source graph, root binder classification, prior reviewer verdict or root implementation plan.',
          'sealed_statement_raw_sha256': sha(seal_raw),
          'sealed_statement_file_for_hash_and_signature_fields_only': str(S),
          'lean': [{k: s[role][k] for k in ['name', 'planned_file', 'signature', 'signature_sha256']} | {'literal_Prop_formation_only': True, 'target_theorem_compiled': False} for role in ['producer', 'actual_private_consumer']],
          'minimal_definition_exact_locator_overlay_raw_sha256': sha(context_raw),
          'minimal_definitions': [{k: v for k, v in row.items() if k not in ['metadata_changes']} for row in ctx['definitions']]}
raw = dump(packet)
for p in [W/'selective-preproof-types-and-definitions.json', E/'selective-preproof-types-and-definitions.json']:
    put(p, raw)
guard()
record = {'state': 'RESERVED_FRAGMENT_NO_NORMAL_INTAKE', 'cell': str(C), 'owner': OWNER,
          'cell_sha256': sha(C.read_bytes()), 'seal_sha256': sha(seal_raw),
          'selective_type_packet_sha256': sha(raw), 'private_baseline_raw_sha256': sha(base_raw),
          'all_foreign_states': len(base['all_foreign_states']), 'all_foreign_frontier_files': len(base['all_existing_frontier_hashes']),
          'all_protected_tracked_regular_files': len(base['all_tracked_regular_file_hashes']),
          'all_old_bytes_and_ledger_unchanged': True, 'normal_SAU_API_calls': 0,
          'target_proof_API_not_yet_authorized': True}
put(E/'preproof-reservation-preservation.json', dump(record))
put(W/'frontier-reservation-safe-summary.json', dump(record))
print(json.dumps(record))
