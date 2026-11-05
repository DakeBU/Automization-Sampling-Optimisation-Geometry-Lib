"""Append current local proof evidence, never an independent verdict."""
import hashlib
import json
from pathlib import Path
from tools.astis_advance import AdvanceProposal, current_advances, propose_advance, transition_advance

cell_id='ASTIS-SHARED-compact-gradient-sqrt-test-data'
advance='ASTIS-SA-20261105-CompactGradientSqrtTest'
actor='agent-task:/root'
cell=json.loads(Path('research-wiki/frontier-cells',cell_id+'.json').read_text(encoding='utf-8'))
declaration=cell['shared_floor_audit']['canonical_declaration']
files=['AutoSamplingTheory/TechnicalLemmas/Analysis/Calculus/CompactGradientSqrtPerturbation.lean',
       'Tests/Shared/CompactGradientSqrtPerturbation.lean']
ledger=Path('runs/substantive_advances.jsonl');before=ledger.read_bytes()
assert advance not in current_advances(),'Never replay an already recorded transition'
propose_advance(AdvanceProposal(
    advance_id=advance,task_id='ASTIS-CHEWI-EXERCISE-1-7',goal=cell['target_statement'],
    source_anchor=cell['source_anchor'],theorem_delta='Produce original energy and genuine smooth square-root L2/entropy/energy inputs from bounded compact-derivative source tests.',
    truth_boundary=cell['statement_seal']['boundary'],created_by=actor,
    dag_inputs=tuple(cell['parents']),proposed_files=tuple(files),
    focused_checks=('lake build owning-module and Tests.Shared.CompactGradientSqrtPerturbation',),
    modes=('source-class-input-production','focused-proof','reader-publication'),
    frontier_cell=cell_id,target_declarations=(declaration,)))
transition_advance(advance,'CLAIMED',worker_id=actor,evidence={
    'checkpoint':'One writer. These are present-time publication transitions after the sealed prototype/focused compile, not fabricated earlier process timestamps.'})
transition_advance(advance,'EXPLORING',worker_id=actor,evidence={
    'statement_seal':'runs/20261105-compact-gradient-sqrt-test/statement-seal.json',
    'failure_diagnosis':'First elaboration timeout was underconstrained comp_left type inference. Explicitly type its function; same default heartbeats, signature and mathematical route. Focused Hilbert composition required Function.comp_def; no source hypothesis changed.'})
transition_advance(advance,'PROVED_LOCAL',worker_id=actor,evidence={
    'result_kind':'integration-node',
    'theorem_delta':'Original energy is derived by continuous compact support; eventual global positivity gives C-infinity, L2 and integrable entropy, and the existing energy theorem gives actual perturbed energy integrability.',
    'lean_files':files,'lean_declarations':[declaration],'publication_declarations':[declaration],
    'focused_checks':['Owning module/focused Lake build PASS2679; standard3 axioms.',
        'Updated direct Hilbert test exits0: compact gradient support is mapped through actual Riesz duality, and the old energy limit is consumed without an input energy premise.',
        'Target check_advance reviewed=False, semantic registry and Frontier Cell protocols pass. Draft review is not independent source acceptance.'],
    'truth_boundary':'Analytic source-class producer only. No compact-test LSI extension/application, canonical probability KL/Fisher, PI/core closure, full exercise, Bench QA or model score. Old source bindings, Registry/root imports and cycle/paper frontiers unchanged.',
    'conceptual_mirror_audit':{'status':'none-found','discovery_ids':[]},
    'source_audit':'ASTIS-RT-20261105-CompactGradientSqrtTest; draft. Anonymous decoder requested; source review not yet started.'})
after=ledger.read_bytes();assert after.startswith(before),'Existing ledger bytes changed'
print(json.dumps({'advance':advance,'state':current_advances()[advance]['state'],
    'preserved_prefix_bytes':len(before),'preserved_prefix_sha256':hashlib.sha256(before).hexdigest()}))
