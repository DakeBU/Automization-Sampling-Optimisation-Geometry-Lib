"""One source-admitted radius SAU intake; complete existing states stay private and unchanged."""
from pathlib import Path
import copy
import hashlib
import json
import os
import stat
import subprocess
import sys
import tarfile
sys.dont_write_bytecode=True
sys.path.insert(0,'tools')
import astis_advance as advance
import astis_frontier_cells as frontiers
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
E=Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-radius-semantic-evidence')
SP=Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-radius-statement-seal.json')
C=Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-matrix-radius.json')
L=Path('runs/substantive_advances.jsonl')
ADV='ASTIS-SA-20261113-GaussianComplexitySourceMatrixRadius'
OWNER='huanjian_gc_20261113_source_matrix_radius'
sha=lambda raw:hashlib.sha256(raw).hexdigest()
dump=lambda obj:(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode()
git=lambda *args:subprocess.check_output(['git',*args])
def create(p,raw):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(raw)
def fingerprint(p):
    info=p.lstat()
    if stat.S_ISLNK(info.st_mode):
        target=os.readlink(p)
        return {'mode':stat.S_IMODE(info.st_mode),'kind':'symlink','target':target}
    assert stat.S_ISREG(info.st_mode),str(p)
    return {'mode':stat.S_IMODE(info.st_mode),'kind':'regular','bytes':info.st_size,'sha256':sha(p.read_bytes())}
head=git('rev-parse','HEAD').decode().strip()
assert head=='505879e768e94f446bddd790d9330bf43ca2ea76'
assert not git('diff','HEAD','--name-only') and not git('diff','--cached','--name-only')
assert not C.exists() and not SP.exists() and not E.exists()
sealraw=(W/'statement-seal-v1.json').read_bytes()
assert sha(sealraw)=='49d5fa00c9ae90d65878d955fab59d6a4bc03e942501677719881f3d26bf1a72'
seal=json.loads(sealraw)
reviewraw=(W/'reviewed-preproof-inputs.json').read_bytes()
assert sha(reviewraw)=='1401d188fb352a3d2a768d11a2d79f484261195d658fff2d9f17b1fff2f9b514'
review=json.loads(reviewraw)
assert review['current_topology_blocks']==[] and review['source_type_verdict']['binders']=='NO_EXCESS_DETECTED'
assert review['independent_topology_verdict']['TC_F1']==review['independent_topology_verdict']['TC_F2']=='CLOSED_AT_SOURCE_TOPOLOGY_LEVEL'
assert review['target_formal_proof_or_implementation_attempts']==0
for name,item in review['all_original_files'].items():
    p=Path(name);raw=p.read_bytes();assert len(raw)==item['bytes'] and sha(raw)==item['sha256'],name
P,T=[seal[k]['planned_file'] for k in ['producer','actual_private_consumer']]
assert not Path(P).exists() and not Path(T).exists()
before=L.read_bytes();states=advance._replay_advances([json.loads(x) for x in before.splitlines()])
assert len(states)==310 and ADV not in states
assert states['ASTIS-SA-20261112-GaussianComplexitySourceMatrixVariance']['state']=='VERIFIED'
assert states['ASTIS-SA-20261112-RealMatrixPositiveIntegral']['state']=='VERIFIED'
frontier_before={str(p):sha(p.read_bytes()) for p in C.parent.rglob('*') if p.is_file() and not p.is_symlink()}
assert len(frontier_before)==470
discovery=Path('runs/substantive_discoveries.jsonl').read_bytes()
ds=advance._replay_discoveries([json.loads(x) for x in discovery.splitlines()]);assert len(ds)==43
index=git('ls-files','--stage','-z')
tracked={}
for entry in index.split(b'\0'):
    if not entry:continue
    _,name=entry.split(b'\t',1);p=Path(os.fsdecode(name));tracked[str(p)]=fingerprint(p)
controls={}
for root in [Path('runs'),*[Path('.astis')/name for name in ['control','queues','runtime','harness','state','locks']]]:
    if root.is_dir() and not root.is_symlink():
        for p in root.rglob('*'):
            if p.is_file() or p.is_symlink():controls[str(p)]=fingerprint(p)
for p in Path('.astis').iterdir():
    if p.is_file() and any(s in p.name.lower() for s in ['queue','control','goal','steer','execution']):
        controls[str(p)]=fingerprint(p)
baseline={'head':head,'ledger_bytes':len(before),'ledger_sha256':sha(before),
    'all_foreign_states':states,'all_existing_frontier_hashes':frontier_before,
    'tracked_git_index':index.decode(),'all_existing_tracked_fingerprints':tracked,
    'actual_control_fingerprints':controls,'scope':'Fullprivatepreservation; neverexport foreign states/index/control bodies.'}
create(W/'preproof-baseline.private.json',dump(baseline))
create(W/'preproof-discoveries.private.json',dump({'ledger_sha256':sha(discovery),'full_states':ds,'scope':'Private only'}))

create(SP,sealraw)
E.mkdir(parents=True)
archive=E/'independent-preproof-source.original-files.tar.gz'
originals=sorted(review['all_original_files'])
with tarfile.open(archive,'x:gz') as out:
    for name in originals:out.add(name,arcname=name,recursive=False)
with tarfile.open(archive,'r:gz') as inp:
    for name in originals:assert inp.extractfile(name).read()==Path(name).read_bytes()
create(E/'independent-preproof-source.original-manifest.json',dump({'files':review['all_original_files'],'archive_sha256':sha(archive.read_bytes()),'private_foreign_data_exported':False}))
create(E/'preproof-source-admission.json',reviewraw)
envraw=(W/'actual-environment-before-intake.json').read_bytes()
env=json.loads(envraw)
assert env['HEAD']==head and env['manifest_sha256']=='b83ca83b9cf7caa85fa8b023c2ff9a3fb7a7cce7e1c332e810c348535ec49c37'
create(E/'actual-environment-before-intake.original.json',envraw)
slug='huanjian-gaussian-source-matrix-radius'
names=[
    'AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixMean.actual_source_truncated_matrix_means',
    'AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCosineGram.actual_cosine_frame_gram',
    'AutoSamplingTheory.TechnicalLemmas.Probability.StdGaussianMoment.integrable_norm_sq_and_integral_stdGaussian']
searches=[
    'Actual ASTIS SourceMatrixMean signature inspected/typed: genuine literalYi integrability and exact radial mean identity on originalmu. It does NOT itself return0<=a<=1; derive requiredscalar range internally using canonicalStdGaussianMoment and indicatorintegral order, never a new caller binder.',
    'Canonical actual_cosine_frame_gram supplies uniform literalfeature squarednorm<=2r, q0included, with exact halfgrid shift reconciled internally. Reuse it instead of another publicfeature lemma.',
    'Mathlib realfinite matrix L2Operator norm maps to EuclideanCLM; existing InnerProductSpace.norm_rankOne and symm_toEuclideanLin_rankOne, ContinuousLinearMap.opNorm_le_bound, EuclideanSpace.norm_sq_eq are realcompatible canonical APIs. Concrete scopednorm verified by realLean typeprint. No norm-kronecker provider claimed from a text search.',
    'Complex CStarAlgebra norm-order API is not assumed applicable to realmatrices. Source/implementation route may use existingreal rankone/block norm providers; any genuinelymissingmulti-consumer generic lemma must first be given one sharedcell, never a certificateinput.']
cell=copy.deepcopy(json.loads(Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-matrix-variance.json').read_bytes()))
for k in ['source_proof_coverage','proof_digestion','purification']:cell.pop(k,None)
cell.update({'cell_id':C.stem,'title':'Actual truncated Gaussian summand and mean norms with centered radius consumer',
    'source_anchor':'arXiv2610.20492v1 AppendixC.2/A3.SS2.p13,Ex111/112; originalp1/p10/Ex107 experiment,p12 radial actualmean andFactC5 feature bound. p14variance andp15Bernstein excluded.',
    'target_statement':seal['producer']['signature']+'\nPrivate actual consumer\n'+seal['actual_private_consumer']['signature'],
    'status':'claimed','owner_id':OWNER,'advance_id':ADV,
    'reservation_only':'Source-admitted exacttype reservation before one normalintake; no targetproof.',
    'parents':['ASTIS-SW-GAUSSIAN-COMPLEXITY-source-matrix-mean','ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-cosine-gram','ASTIS-SHARED-std-gaussian-second-moment'],
    'consumers':[seal['actual_private_consumer']['name']],
    'shared_floor_audit':{'searched':searches,'classification':'adapt','decision':'reuse_existing','canonical_declaration':seal['producer']['name'],'canonical_shared_cell':''},
    'reuse_plan':{'searched_existing':searches,'reused_declarations':[],'planned_existing_parents':names,
        'new_shared_declarations':[],'known_consumers':[],'planned_consumers':[seal['actual_private_consumer']['name']],
        'no_duplicate_wrapper':True,'decision_reason':'Actualsource norm outputs and material literalZ/cosine radius consumer. Reuse canonical mean/frame/Gaussianmoment andrealMathliboperatornorm APIs; estimates andregularity are internallyproved edges, not theorem premises.'},
    'source_detail_audit':{'primary_edition':'arXiv2610.20492v1 rawSHA '+seal['source']['sha256'],
        'primary_anchor':'C.2p13/Ex111/112 with literalp1/p10/p12 experiment andmean, FactC5; no p14/p15 claim',
        'detail_status':'omitted','gap':'Source omits rankone/tensor norm, radial mean transport, triangle/scalar norm derivations. Five explicitSOURCE_GAP proof obligations andnineinternalports remainunproved; no false source or newhypothesis established.',
        'consulted':[{'source':'Pinned rawprimary plus distinctsource-only graph/type/topologyroles',
            'anchor':'Exact87source units andv2internalnumeric/cutoff/mean-object graph refinement',
            'hypothesis_adapter':'Solehq andliteraloriginalproduct experiment, actualBochnermean, realL2operatornorm, closedcutoff andq0 unchanged. d/r/log/L/branch sideconditions internallydischarged.'}],
        'fidelity_boundary':seal['scope_boundary']},
    'statement_seal':{'status':'EXACT_TYPES_AND_DEFINITIONS;INDEPENDENT_SOURCE_TOPOLOGY_ACCEPTED;UNPROVED',
        'file':str(SP),'sha256':sha(sealraw),'signature_sha256':seal['producer']['signature_sha256'],
        'private_consumer_signature_sha256':seal['actual_private_consumer']['signature_sha256']},
    'evidence':{'actual_literal_formation':seal['actual_statement_formation'],
        'actual_definition_meaning':{'file':str(E/'independent-preproof-source.original-manifest.json'),'source_audit_sha256':'dd1484596b083d59f3a9908235b9ee0de95d014b6ef9d98449cc5713e8b4d939'},
        'preproof_source_admission':{'file':str(E/'preproof-source-admission.json'),'sha256':sha(reviewraw)},
        'actual_environment':{'file':str(E/'actual-environment-before-intake.original.json'),'sha256':sha(envraw)},
        'normal_API_calls':0,'target_proof_calls':0,'formalizer_API_pristine':False},
    'blocked':{},'owned_files':[P,T,str(SP),str(C),str(E)+'/',
        'website/content/declaration_lessons/'+slug+'.json','website/content/publications/'+slug+'.json',
        'research-wiki/semantic-roundtrip/audits/'+slug+'.json'],
    'truth_boundary':seal['scope_boundary'],'conceptual_mirror_audit':{'status':'pending','discovery_ids':[]}})
cell['reader_contract']['status']='Exactunproved norm/radius statements andsource/type/topology admitted. Authored formula proof andinitiallyfolded exactLean require actualproof; productiondelivery andglobalintegration remainopen.'
cell['graph_contribution'].update({'lean_view':'new-node','overview_view':'no-change-with-reason','functor_view':'none-found',
    'focus_targets':[seal['producer']['name']],
    'visual_review':'Source-onlyv2topology accepted; no compilednewnode orruntimegraph/reader claim. Conceptualaudit remains pending beforePL; no newcandidate asserted atintake.'})
cell['learning_contract']={
    'control_plane_math_authority':False,'process_memory_checked':True,'process_memory_ids':[],
    'failure_class':'IMPLEMENTATION_FAILED',
    'salvage':{'required':True,'status':'completed','reason':'Only preproof parser/unnecessarytypequeries andROOTAPI-locator guesses failed. All originals retained; no mathematical route/statement retired andno targetproof yet.','promoted_fragments':[],'discarded_fragments':[]},
    'parallelism':{'decision':'serial','direction_fingerprints':[],'expected_information_gain':'One ROOTprover; independent source extraction anddistincttopologychallenge own separateuncertainty.','shared_verified_context_digest':''},
    'cross_route_blind_spot_audit':{'required':False,'status':'not-applicable','evidence':'','canonical_route':'','selection_reason':'No seriousparallelproof routes attempted.'},
    'reader_backpressure':{'purification_status':'pending','exposition_seal_status':'pending','exposition_evidence':'','source_expansion_nodes':[],'lean_expansion_nodes':[],'assumptions_preserved':False,'boundary_preserved':True}}
create(C,dump(cell))
assert not frontiers.validate_cells(frontiers.load_cells())
proposal=advance.AdvanceProposal(advance_id=ADV,task_id='ASTIS-SW-GAUSSIAN-COMPLEXITY-2026',
    goal='Prove actualpointwise truncatedYi norm<=2rL/d andactualmean norm<=2r/d; materiallyconsume both in literalcentered andcosineweighted radius<=2r(L+1)/d on the originalexperiment withonlyhq.',
    source_anchor=cell['source_anchor'],theorem_delta=seal['producer']['signature'],truth_boundary=seal['scope_boundary'],created_by=OWNER,
    dag_inputs=(cell['source_anchor'],'Actualpublicmean/frame/standardGaussiansecondmoment andrealMathliboperatornorm applicability; allnorm/mean/regularity/sign/cutoff/triangle/scalar estimates remaininternal, never sourcecertificatebinders.'),
    proposed_files=tuple(p for p in cell['owned_files'] if not p.endswith('/')),
    focused_checks=('lake env lean '+P,'lake build Tests.GaussianComplexityFixedSpectrumSourceMatrixRadius'),
    modes=('source-reading','proof-design','compiler-diagnosis'),priority=50,frontier_cell=C.stem,target_declarations=(seal['producer']['name'],))
proposal.validate()
create(W/'normal-intake-attempted.once.json',dump({'advance_id':ADV,'before_ledger_sha256':sha(before),'source_admission_sha256':sha(reviewraw),'no_replay':True}))
ev={'independent_topology':cell['evidence']['preproof_source_admission'],'statement_seal_sha256':sha(sealraw),'truth_boundary':seal['scope_boundary'],'formalizer_API_pristine':False}
advance.propose_advance(proposal)
advance.transition_advance(ADV,'CLAIMED',worker_id=OWNER,evidence=ev)
advance.transition_advance(ADV,'EXPLORING',worker_id=OWNER,evidence=ev)
after=L.read_bytes();assert after.startswith(before)
append=after[len(before):];events=[json.loads(x) for x in append.splitlines()]
assert len(events)==3 and all(x['advance_id']==ADV for x in events)
assert [x.get('state',x.get('to_state')) for x in events]==['PROPOSED','CLAIMED','EXPLORING']
now=advance._replay_advances([json.loads(x) for x in after.splitlines()])
assert now.pop(ADV)['state']=='EXPLORING' and now==states
assert git('ls-files','--stage','-z')==index
for name,fp in tracked.items():
    if name!=str(L):assert fingerprint(Path(name))==fp,name
for name,fp in controls.items():
    if name!=str(L):assert fingerprint(Path(name))==fp,name
for name,h in frontier_before.items():assert sha(Path(name).read_bytes())==h,name
assert Path('runs/substantive_discoveries.jsonl').read_bytes()==discovery
cell['reservation_only']='Normalledger EXPLORING under namedowner; no targetproof yet.'
cell['evidence']['normal_API_calls']=3
C.write_bytes(dump(cell))
assert not frontiers.validate_cells(frontiers.load_cells())
create(E/'normal-EXPLORING-append.exact.jsonl',append)
summary={'state':'EXPLORING','actual_normal_API_calls':3,'append_sha256':sha(append),'baseline_commit':head,
    'foreign_full_advances_preserved':len(states),'foreign_discoveries_preserved':len(ds),
    'all_existing_regular_frontier_files_preserved':len(frontier_before),'all_existing_tracked_bytes_modes_index_preserved_except_exact_ledger_append':len(tracked),
    'actual_control_files_preserved':len(controls),'target_formal_proof_calls':0,'root_VERIFIED_calls':0,
    'preproof_archive_sha256':sha(archive.read_bytes()),'statement_seal_sha256':sha(sealraw)}
create(E/'normal-intake-preservation.json',dump(summary))
assert set(git('diff','HEAD','--name-only').decode().splitlines())=={str(L)}
print(json.dumps(summary))
