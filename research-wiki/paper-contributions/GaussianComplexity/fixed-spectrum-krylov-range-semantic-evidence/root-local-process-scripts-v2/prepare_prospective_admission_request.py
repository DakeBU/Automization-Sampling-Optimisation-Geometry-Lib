from pathlib import Path
import hashlib, json
W = Path(__file__).parent
sha = lambda b: hashlib.sha256(b).hexdigest()
dump = lambda x: (json.dumps(x, ensure_ascii=False, indent=2)+'\n').encode()
post = {'state': 'DISCLOSED_ABSTRACT_POSTSEAL_PLANNING_NOT_A_LEAN_PROOF',
        'root_sole_mathematical_worker': True,
        'abstract_thoughts': 'After sealing, root considered the source polynomial triangular-basis argument and possible generic polynomial-basis or cosine-recurrence span routes, together with algebraic transport of Euclidean norm/weighted quadratic forms. No target-specific theorem proof/API was retrieved and no Lean proof term, helper implementation or target proof module was written.',
        'generic_prior_exposure_not_pristine': 'Earlier C7/Gram work and the preseal adjacent standard-definition/proof/header exposures are retained in preseal-exposure-qualified-complete.json. No retroactive clean-history claim.',
        'new_target_proof_and_normal_API_calls': 0}
(W/'postseal-abstract-planning-disclosure.json').write_bytes(dump(post))
prepared = json.loads((W/'prepared-intake-safe-summary.json').read_bytes())
assert sha((W/'admit_normal_intake_prepared.py').read_bytes()) == prepared['prepared_intake_script_sha256']
assert sha((W/'intake-baseline.private.json').read_bytes()) == prepared['private_baseline_sha256']
assert sha((W/'preproof-baseline.private.json').read_bytes()) == prepared['private_preproof_baseline_sha256']
request = {
 'kind': 'PROSPECTIVE_PROCESS_REVIEW_REQUEST_NOT_A_GRANT',
 'mathematical_review_must_be_frozen_first': 'Use your own raw-first/type/source-graph challenge freezes; do not alter their mathematical judgments to accommodate this process request.',
 'root_sole_mathematical_worker': True,
 'advance_id': 'ASTIS-SA-20261110-GaussianComplexityFixedSpectrumKrylovRange',
 'owner': 'huanjian_gc_20261110_fixed_spectrum_krylov_range',
 'seal_sha256': 'f47e23a601d1a8e0ff4760224676313e0f1999877a97156841a65c01847e5d82',
 'prepared_intake_script': prepared['prepared_intake_script'],
 'prepared_intake_script_sha256': prepared['prepared_intake_script_sha256'],
 'private_baseline_sha256': prepared['private_baseline_sha256'],
 'private_preproof_baseline_sha256': prepared['private_preproof_baseline_sha256'],
 'own_frontier': 'research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-krylov-range.json',
 'own_frontier_sha256': '130d9889589b4153a93857868206281367c933d2790e332b34c3425b4e242786',
 'normal_SAU_API_calls_so_far': 0,
 'target_producer_Test_and_temporary_Lean_probe_absent': True,
 'preserved_baseline': {'foreign_states': 299, 'foreign_frontier_files': 459, 'tracked_regular_files': 128851, 'foreign_controls': 927, 'all_counts_are_integrity_not_math_credit': True},
 'actual_history_to_review': [
  'preseal-exposure-qualified-complete.json', 'postseal-abstract-planning-disclosure.json',
  'actual-environment-before-statement-formation.json', 'statement-formation-reserved-identifier-diagnostic.json',
  'StatementFormation.lean.attempt1.raw.txt', 'StatementFormation.lean.coordinate-energy-v2.raw.txt', 'StatementFormation.raw.lean.txt',
  'producer-signature.draft.txt.attempt1.raw.txt', 'consumer-signature.draft.txt.attempt1.raw.txt',
  'consumer-signature.draft.txt.coordinate-energy-v2.raw.txt', 'unsealed-actual-Euclidean-consumer-elaboration.json',
  'definition-locator-overlay-diagnostic.json', 'minimal-definition-context.json', 'minimal-definition-context-exact-LF.json',
  'seal_exact_statements.py', 'reserve_frontier_and_selective_types.py', 'prepare_normal_intake.py', 'admit_normal_intake_prepared.py',
  'frontier-reservation-safe-summary.json', 'prepared-intake-safe-summary.json'],
 'real_R_receipt_stems': [
  '20261110T181225816765Z-krylov-range-real-environment-and-two-literal-statement-drafts',
  '20261110T181238322111Z-krylov-range-two-closed-literal-Prop-type-formation-only',
  '20261110T181443053420Z-krylov-range-two-literal-Prop-formation-v2-unreserved-local-name',
  '20261110T181711845884Z-krylov-range-literal-Prop-v3-actual-Euclidean-norm-and-inner',
  '20261110T182213064132Z-krylov-range-exact-statement-binder-definition-seal-before-proof',
  '20261110T182440236577Z-krylov-range-exact-definition-LF-locator-metadata-overlay',
  '20261110T183126243816Z-krylov-range-reserve-new-only-frontier-and-selective-types-no-intake',
  '20261110T184625830431Z-krylov-range-preproof-frontier-reservation-format-only',
  '20261110T185434118035Z-krylov-range-prepare-exact-intake-script-and-private-control-baseline-no-API'],
 'failed_attempt_fairness': 'First literal Prop probe failed on reserved lambda token. Its printed Prop names are not accepted formation evidence. Original source bytes/errors remain. Later source-identical alpha rename passed; actual metric consumer was explicitly elaborated before the exact seal and passed. No target proof or normal API was attempted. Definition locator metadata overlay is explicit and core seal unchanged.',
 'process_memory': 'Three existing process-memory entries checked; none supplies mathematical authority or an applicable new condition. Record process-only scope.',
 'requested_future_gate_if_warranted': 'After independent mathematical freezes and process audit, issue an exact qualified prospective grant bound to the actual source/typed/topology inputs, this prepared script hash and private baseline hashes. No grant may retroactively make root API-pristine. Prepared script checks all exact grant input hashes, PYTHONOPTIMIZE=0, one O_EXCL intake marker, full original ledger prefix, all tracked/frontier/control/foreign-state preservation before and after exactly3 normal proposal/CLAIMED/EXPLORING API calls. Only after actual success and root readback may target Lean proof/API retrieval begin.',
 'grant_fields_required_by_prepared_script': ['prospective_target_Lean_proof_API_allowed_after_this_grant', 'root_sole_mathematical_worker', 'prepared_intake_script_sha256', 'private_baseline_sha256', 'independent_inputs'],
 'private_data_policy': 'Private baseline files are PROCESS ONLY: you may verify raw hash and inspect schema/counts/hash-only selected metadata, but never export or reproduce full foreign state/evidence/path-hash inventories. Never traverse/hash/read restricted ATLAS content/index/projections/derivatives or giant ignored kernel dumps. Latest old sourceV portable paths are enumerated by its exact manifest; private sibling excluded.',
 'global_truth_boundary': 'Original remote SlcLsiWeightedRadialMGF lease remains active. Twelve original sourceVs/readerHOLDs, other ASTIS chat and PBPS/SPHMC/nonempty queues remain exact; no takeover/shared-import/rootTests/Registry/global graph/site/push/purification/Goal completion. Conditional integration proposals are separate DISABLED read-only work, not a lease transfer.'
}
(W/'prospective-admission-request.json').write_bytes(dump(request))
print(json.dumps({'request': str(W/'prospective-admission-request.json'), 'request_sha256': sha(dump(request)), 'normal_API_calls': 0, 'target_proof_API_authority': False}))
