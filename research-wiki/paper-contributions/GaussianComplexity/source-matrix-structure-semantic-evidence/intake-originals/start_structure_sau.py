"""Admit one exact source-reviewed structure packet after completing the prior SAU."""
from pathlib import Path
import copy,hashlib,json,os,stat,subprocess,sys,tarfile
sys.dont_write_bytecode=True
sys.path.insert(0,'tools')
import astis_advance as advance
import astis_frontier_cells as frontiers
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
E=Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-structure-semantic-evidence')
C=Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-matrix-structure.json')
SP=Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-structure-statement-seal.json')
L=Path('runs/substantive_advances.jsonl')
ADV='ASTIS-SA-20261113-GaussianComplexitySourceMatrixStructure'
OWNER='huanjian_gc_20261113_source_matrix_structure'
sha=lambda b:hashlib.sha256(b).hexdigest()
dump=lambda o:(json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode()
git=lambda *a:subprocess.check_output(['git',*a])
def create(p,b):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(b)
def fingerprint(p):
    st=p.lstat()
    if stat.S_ISLNK(st.st_mode):return {'mode':stat.S_IMODE(st.st_mode),'kind':'symlink','target':os.readlink(p)}
    assert stat.S_ISREG(st.st_mode)
    return {'mode':stat.S_IMODE(st.st_mode),'kind':'regular','bytes':st.st_size,'sha256':sha(p.read_bytes())}
head=git('rev-parse','HEAD').decode().strip();assert head=='96fc5f68fa7e0390e43279fd3228aa60f9ad3a90'
assert not git('diff','HEAD','--name-only') and not git('diff','--cached','--name-only')
assert not C.exists() and not SP.exists() and not E.exists()
sealraw=(W/'statement-seal-v2.json').read_bytes();assert sha(sealraw)=='0164b6bcb7f1362c27e459eccf6a68a72a7cea81272f15377e7c193af18e3c60'
seal=json.loads(sealraw);P,T=[seal[k]['planned_file'] for k in ['producer','actual_private_consumer']]
assert not Path(P).exists() and not Path(T).exists()
SG=Path('.astis/semantic-neutral-20261113/structure_sg_a94e');TC=Path('.astis/semantic-neutral-20261113/structure_tc_b7c6')
critical={SG/'source-graph.source-only.v3.json':'9242c7792704cb38a213905baee8cd074b286d5ead153b27defa3d65676cf182',SG/'source-coverage.source-only.v3.json':'91ebd82a04303bbdc0551bf646accb6d92cd1d986d841741fc1a7d364fa07eb7',SG/'internal-obligation-ports.v3.json':'e006fead44edfb7cccaebd0870789d2eb0a2252b0c25508609378db909b33618',SG/'binder-definition-audit.v2.json':'7a415e820d6689383ea7e9cd5e5ce687945606866133c56058e5aeb33e71fa91',TC/'phase3/distinct-final-review.v2.json':'5bb669aeea59a3b8320e57ee2339ea4007275ea0affdaadf8fe0147412719e7d',TC/'MANIFEST.v2.json':'0cc1f259cba62bea2806aa20f9b10cecc8b1d2143b0b248c01954b870bd6922d'}
for p,h in critical.items():assert sha(p.read_bytes())==h
decision=json.loads((TC/'phase3/distinct-final-review.v2.json').read_bytes())
assert decision['decision']=='ACCEPTED_SOURCE_ONLY_TOPOLOGY_AND_COVERAGE_FOR_NEXT_PACKET_PREPARATION'
assert not decision['additional_mathematical_or_type_findings']
assert all(x['resolution']=='RESOLVED' for x in decision['original_findings'])
for x in json.loads((TC/'MANIFEST.v2.json').read_bytes())['files']:
    b=(TC/x['path']).read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256']
formation=json.loads((W/'v2-actual-formation.json').read_bytes());assert formation['exit_code']==0 and formation['theorem_proofs']==0
envraw=(W/'actual-environment-before-intake.json').read_bytes();assert json.loads(envraw)['HEAD']==head
before=L.read_bytes();states=advance._replay_advances([json.loads(x) for x in before.splitlines()]);assert ADV not in states
assert states['ASTIS-SA-20261113-GaussianComplexitySourceMatrixRadius']['state']=='VERIFIED'
discover=Path('runs/substantive_discoveries.jsonl').read_bytes();ds=advance._replay_discoveries([json.loads(x) for x in discover.splitlines()])
index=git('ls-files','--stage','-z');cache={}
def cached(p):
    k=str(p)
    if k not in cache:cache[k]=fingerprint(p)
    return cache[k]
tracked={}
for entry in index.split(b'\0'):
    if entry:
        _,n=entry.split(b'\t',1);p=Path(os.fsdecode(n));tracked[str(p)]=cached(p)
controls={}
for root in [Path('runs'),*[Path('.astis')/n for n in ['control','queues','runtime','harness','state','locks']]]:
    if root.is_dir() and not root.is_symlink():
        for p in root.rglob('*'):
            if p.is_file() or p.is_symlink():controls[str(p)]=cached(p)
for p in Path('.astis').iterdir():
    if p.is_file() and any(s in p.name.lower() for s in ['queue','control','goal','steer','execution']):controls[str(p)]=cached(p)
frontier_before={str(p):sha(p.read_bytes()) for p in C.parent.rglob('*') if p.is_file() and not p.is_symlink()}
create(W/'preproof-baseline.private.json',dump({'head':head,'ledger_sha256':sha(before),'ledger_bytes':len(before),'all_foreign_states':states,'all_existing_frontier_hashes':frontier_before,'tracked_git_index':index.decode(),'all_existing_tracked_fingerprints':tracked,'actual_control_fingerprints':controls,'scope':'Private complete preservation only; never export full foreign states/index/control snapshots.'}))
create(W/'preproof-discoveries.private.json',dump({'ledger_sha256':sha(discover),'full_states':ds,'scope':'Private only'}))
originals={}
for root in [SG,TC]:
    for p in sorted(root.rglob('*')):
        if p.is_file() and '__pycache__' not in p.parts:
            assert not p.is_symlink() and not any(x.startswith('.PRIVATE') for x in p.parts)
            originals[str(p)]={'sha256':sha(p.read_bytes()),'bytes':p.stat().st_size}
E.mkdir(parents=True);archive=E/'independent-preproof-originals.tar.gz'
with tarfile.open(archive,'x:gz') as tf:
    for n in originals:tf.add(n,arcname=n,recursive=False)
with tarfile.open(archive,'r:gz') as tf:
    for n,x in originals.items():
        b=tf.extractfile(n).read();assert len(b)==x['bytes'] and sha(b)==x['sha256']
create(E/'independent-preproof-originals.manifest.json',dump({'files':originals,'archive_sha256':sha(archive.read_bytes()),'private_guard_exported':False}))
admission={'exact_seal_sha256':sha(sealraw),'critical_current_inputs':{str(p):h for p,h in critical.items()},'distinct_reviewer_decision':decision['decision'],'current_topology_blocks':[],'binder_policy':'Only natural dimensions/q and source hq; explicit fixed Borel letI is TYPING, never caller certificate.','independent_coverage_boundary':'Whole source variance blocks excluded here; each centered family independent separately; actualsame-mu mean/integrability/Hermitian remain internal obligations.','original_tc2_qualification':'Oldcoveragealreadyhad contextual-exclusionnote; v3clarifies whole-block disposition. No false mathematical source claim inferred.','source_only':True,'target_proofs':0,'all_source_originals_preserved':len(originals)}
create(E/'preproof-source-admission.json',dump(admission));create(SP,sealraw);create(E/'actual-environment-before-intake.original.json',envraw)
names=['AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceRowIndependence.actual_source_rows_independent','AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceRowLaw.actual_source_row_marginal_law','AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixMean.actual_source_truncated_matrix_means']
searches=['Samplinglib/ASTIS canonical actual_source_rows_independent supplies the literal original physical row family; no duplicate joint-law theorem.','Samplinglib/ASTIS actual_source_row_marginal_law supplies each literal row measurability; actual_source_truncated_matrix_means supplies genuine Y integrability and actual integral formula, not a supplied mean.','Samplinglib/Mathlib standard finite Matrix product topology/Borel and L2Operator norm topology compatibility audited independently; existing measurable maps, independent composition, Bochner subtraction and fixed-scalar rules are the shared floor.','Samplinglib target-name search found no existing public centered/weighted structure declarations. Existing private uncentered-Y independence consumer and private variance/radius consumers are retained; no public duplicate or added certificate premise.']
prior=json.loads(Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-matrix-radius.json').read_bytes())
reader=copy.deepcopy(prior['reader_contract']);reader['status']='Exact proof-free standardBorel signatures and independent source/type/topology preparation accepted; actual P/T proofs and reader delivery pending.'
graph=copy.deepcopy(prior['graph_contribution']);graph.update({'focus_targets':[seal['producer']['name']],'visual_review':'Source-only accepted v3 structure graph, not a compiled or runtime graph. Global integration and later matrix concentration outside this packet.'})
boundary='Only actual original-experiment centered and deterministic cosine-weighted sequences: measurability, each-family joint independence, integrability, actual zero mean and pointwise real Hermitian symmetry. q0 and source hq retained; no combined2d-family independence, new radius/variance/concentration bound, full C6/Lemma4.4/main lower bound, oracle/TV/precision/cap/cost, publicT API or integration/purification credit.'
cell={'schema_version':3,'cell_id':C.stem,'route':'samplewiki-route','mode':'faithfulPaper','title':'Actual centered Gaussian matrix structure with weighted consumer','source_anchor':'arXiv2610.20492v1 AppendixC.2 p15 first structure assertion; p1/p10/Ex107,p12 actualmean,p13Zi/cosineweights; S4Lemma4.4 q regime. Bernstein probability tail excluded.','target_statement':seal['producer']['signature']+'\nPrivate actual weighted consumer\n'+seal['actual_private_consumer']['signature'],'status':'claimed','owner_id':OWNER,'advance_id':ADV,'parents':['ASTIS-SW-GAUSSIAN-COMPLEXITY-source-row-independence','ASTIS-SW-GAUSSIAN-COMPLEXITY-source-row-law','ASTIS-SW-GAUSSIAN-COMPLEXITY-source-matrix-mean'],'consumers':[seal['actual_private_consumer']['name']],'shared_floor_audit':{'searched':searches,'classification':'adapt','decision':'reuse_existing','canonical_declaration':seal['producer']['name'],'canonical_shared_cell':''},'reuse_plan':{'searched_existing':searches,'reused_declarations':[],'planned_existing_parents':names,'new_shared_declarations':[],'known_consumers':[],'planned_consumers':[seal['actual_private_consumer']['name']],'no_duplicate_wrapper':True,'decision_reason':'New actual centered-family structural outputs are materially consumed by the literal cosine-weighted source family. Existing row/law/actualmean and canonical Mathlib maps/integrals discharge all premises internally.'},'reader_contract':reader,'graph_contribution':graph,'learning_contract':{'control_plane_math_authority':False,'process_memory_checked':True,'process_memory_ids':[],'failure_class':'API_BLOCKED','salvage':{'required':True,'status':'completed','reason':'Initial proof-free matrix measurable-space synthesis failure corrected by an explicitly audited fixed standard Borel definition; original failure and all source topology/custody corrections preserved. No mathematical route retired and no target proof supplied.','promoted_fragments':[],'discarded_fragments':[]},'parallelism':{'decision':'serial','direction_fingerprints':[],'expected_information_gain':'One ROOT prover, distinct independent source extraction and topology challenge.','shared_verified_context_digest':sha(sealraw)},'cross_route_blind_spot_audit':{'required':False,'status':'not-applicable','evidence':'','canonical_route':'','selection_reason':'No parallel serious proof routes.'},'reader_backpressure':{'purification_status':'pending','exposition_seal_status':'pending','exposition_evidence':'','source_expansion_nodes':[],'lean_expansion_nodes':[],'assumptions_preserved':False,'boundary_preserved':True}},'source_detail_audit':{'primary_edition':'arXiv2610.20492v1 rawSHA '+seal['source']['sha256'],'primary_anchor':'C.2 p15 structural assertion and exact original experiment/actualmean definitions','detail_status':'omitted','gap':'Source asserts independent, centered, self-adjoint sequences without the row-transformation, Bochner applicability and explicit Borel details; all remain internal source-gap ports, not caller assumptions.','consulted':[{'source':'Pinned rawsource plus independent SG/TC roles','anchor':'Exact v3 sourcegraph/coverage and seven internal ports','hypothesis_adapter':'Solehq, q0, standardBorel, sameoriginalmu/actualmean, inclusivecutoff and each-family scope preserved.'}],'fidelity_boundary':boundary},'statement_seal':{'status':'EXACT_TYPES_FORMED;SOURCE_TYPE_TOPOLOGY_PREPARATION_ACCEPTED;UNPROVED','file':str(SP),'sha256':sha(sealraw),'signature_sha256':seal['producer']['signature_sha256'],'private_consumer_signature_sha256':seal['actual_private_consumer']['signature_sha256']},'evidence':{'preproof_source_admission':{'file':str(E/'preproof-source-admission.json'),'sha256':sha(dump(admission))},'actual_literal_formation':formation,'actual_environment':{'file':str(E/'actual-environment-before-intake.original.json'),'sha256':sha(envraw)},'normal_API_calls':0,'target_proof_calls':0,'formalizer_API_pristine':False},'blocked':{},'owned_files':[P,T,str(C),str(SP),str(E)+'/', 'website/content/declaration_lessons/huanjian-gaussian-source-matrix-structure.json','website/content/publications/huanjian-gaussian-source-matrix-structure.json','research-wiki/semantic-roundtrip/audits/huanjian-gaussian-source-matrix-structure.json'],'forbidden_shared_files':prior['forbidden_shared_files'],'truth_boundary':boundary,'conceptual_mirror_audit':{'status':'pending','discovery_ids':[]},'reservation_only':'Source-admitted exact type reservation, no target proof.'}
create(C,dump(cell));errors=frontiers.validate_cells(frontiers.load_cells());assert not errors,errors
proposal=advance.AdvanceProposal(advance_id=ADV,task_id='ASTIS-SW-GAUSSIAN-COMPLEXITY-2026',goal='Prove actual centered Gaussian matrix measurability/joint independence/integrability/zero mean/Hermitian structure, then materially consume all in actual deterministic cosine-weighted family, sole source hq and same original experiment.',source_anchor=cell['source_anchor'],theorem_delta=seal['producer']['signature'],truth_boundary=boundary,created_by=OWNER,dag_inputs=(cell['source_anchor'],'Actual row/law/mean and standard Borel/Bochner applicability, never extra source certificates.'),proposed_files=tuple(p for p in cell['owned_files'] if not p.endswith('/')),focused_checks=('lake env lean '+P,'lake build Tests.GaussianComplexityFixedSpectrumSourceMatrixStructure'),modes=('source-reading','proof-design','compiler-diagnosis'),priority=50,frontier_cell=C.stem,target_declarations=(seal['producer']['name'],))
proposal.validate();create(W/'normal-intake-attempted.once.json',dump({'advance_id':ADV,'before_ledger_sha256':sha(before),'source_admission_sha256':sha(dump(admission)),'no_replay':True}))
ev={'statement_seal_sha256':sha(sealraw),'independent_topology':admission['distinct_reviewer_decision'],'truth_boundary':boundary,'formalizer_API_pristine':False}
advance.propose_advance(proposal);advance.transition_advance(ADV,'CLAIMED',worker_id=OWNER,evidence=ev);advance.transition_advance(ADV,'EXPLORING',worker_id=OWNER,evidence=ev)
after=L.read_bytes();assert after.startswith(before);append=after[len(before):];events=[json.loads(x) for x in append.splitlines()]
assert len(events)==3 and all(x['advance_id']==ADV for x in events)
now=advance._replay_advances([json.loads(x) for x in after.splitlines()]);assert now.pop(ADV)['state']=='EXPLORING' and now==states
assert git('ls-files','--stage','-z')==index
checked={}
for p,fp in {**tracked,**controls}.items():
    if p!=str(L):assert fingerprint(Path(p))==fp,'existing bytes/mode changed'
for p,h in frontier_before.items():assert sha(Path(p).read_bytes())==h
assert Path('runs/substantive_discoveries.jsonl').read_bytes()==discover
cell['evidence']['normal_API_calls']=3;cell['reservation_only']='Normalledger EXPLORING, no target proof yet.';C.write_bytes(dump(cell))
assert not frontiers.validate_cells(frontiers.load_cells())
create(E/'normal-EXPLORING-append.exact.jsonl',append)
summary={'state':'EXPLORING','actual_API_calls':3,'append_sha256':sha(append),'foreign_full_advances_preserved':len(states),'foreign_full_discoveries_preserved':len(ds),'foreign_regular_frontier_files_preserved':len(frontier_before),'existing_tracked_fingerprints_preserved':len(tracked),'historical_control_fingerprints_preserved':len(controls),'control_count_qualification':'Historical runs and named actual control roots, not a literal queue count.','source_original_files':len(originals),'private_guards_exported':False,'target_proof_calls':0,'ROOT_V_calls':0}
create(E/'normal-intake-preservation.json',dump(summary))
for n in ['statement-seal-v1.json','formation-v1-typing-diagnosis.json','v2-actual-formation.json','start_structure_sau.py','seal_explicit_borel_successor.py']:create(E/'intake-originals'/n,(W/n).read_bytes())
paths=[C,SP,L,*[p for p in sorted(E.rglob('*')) if p.is_file()]]
spec=W/'normal-intake-paths.private.nul';create(spec,b'\0'.join(str(p).encode() for p in paths)+b'\0')
subprocess.run(['git','add','-f','--pathspec-from-file='+str(spec),'--pathspec-file-nul'],check=True)
assert set(git('diff','--cached','--name-only').decode().splitlines())==set(map(str,paths))
subprocess.run(['git','diff','--cached','--check','--',str(C),str(SP),str(L)],check=True)
subprocess.run(['git','commit','--quiet','-m','Admit source-faithful actual centered matrix structure packet'],check=True)
commit=git('rev-parse','HEAD').decode().strip()
result={'intake_commit':commit,**summary};create(W/'actual-normal-intake-commit.json',dump(result));print(json.dumps(result))
