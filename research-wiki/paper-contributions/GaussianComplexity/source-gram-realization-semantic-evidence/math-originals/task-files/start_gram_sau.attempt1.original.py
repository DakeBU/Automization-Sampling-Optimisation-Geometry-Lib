"""One source-admitted Gram packet; run only after the prior actual normal V is carried."""
from pathlib import Path
import copy,hashlib,json,os,stat,subprocess,sys,tarfile
sys.dont_write_bytecode=True
sys.path.insert(0,'tools')
import astis_advance as advance
import astis_frontier_cells as frontiers
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
E=Path('research-wiki/paper-contributions/GaussianComplexity/source-gram-realization-semantic-evidence')
C=Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-gram-realization.json')
SP=Path('research-wiki/paper-contributions/GaussianComplexity/source-gram-realization-statement-seal.json')
L=Path('runs/substantive_advances.jsonl')
ADV='ASTIS-SA-20261113-GaussianComplexitySourceGramRealization'
OWNER='huanjian_gc_20261113_source_gram_realization'
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
head=git('rev-parse','HEAD').decode().strip()
assert head==json.loads((W/'intake-config.json').read_bytes())['expected_HEAD']
assert not git('diff','HEAD','--name-only') and not git('diff','--cached','--name-only')
assert not C.exists() and not SP.exists() and not E.exists()
assert not (W/'normal-intake-attempted.once.json').exists()
sealraw=(W/'statement-seal-v1.unclaimed.json').read_bytes()
assert sha(sealraw)=='7b2f71cf9e89a41da4f66b2b3908222c875cd2fec2f8b2ca6533fe61b3bb3ce9'
seal=json.loads(sealraw);P,T=[seal[k]['planned_file'] for k in ['producer','actual_private_consumer']]
assert not Path(P).exists() and not Path(T).exists()
SG=Path('.astis/semantic-neutral-20261113/structure_sg_a94e/next_gram_graph_v1')
TC=Path('.astis/semantic-neutral-20261113/structure_tc_b7c6/next_gram_raw_tc')
critical={SG/'SOURCE-GRAPH.v3.json':'e8b7971a3ca918bc680902cef27b6c2ab36f023f7fca52665696afd5c18b63f1',SG/'SOURCE-COVERAGE.v3.json':'39e0000f89ad56c841828e533968d384ae2c4a41a73d7872096a8211019b3b46',SG/'INTERNAL-PORTS.v2.json':'ccbf7e2a118982d7be2d58035eec5c9adc1101ca44262feb3e2dc4ca7ba507d5',SG/'BINDER-DEFINITION-AUDIT.v1.json':'d7c153920d953440bf4bf37b2db1c4ac661804aa66792a81fd58ca73f2738452',SG/'FINAL-MANIFEST.v1.json':'b2a0713f16f707b0dcca62fadb7b865d1c59175704927bedb73d8844f8d1eaf7',TC/'TC-FINAL-MANIFEST.v1.json':'2315ffb93729f7c6269a08eb390e8034eca42f1f47b6fdcc351dabfa8d3dbdb6',TC/'seal_audit/literal-seal-audit.v1.json':'9f38e94a95687c6d933ff4b44e056a4434559bce896725d8b59f84e452fda582'}
for p,h in critical.items():assert sha(p.read_bytes())==h
for n,h in json.loads((SG/'FINAL-MANIFEST.v1.json').read_bytes())['files'].items():assert sha((SG/n).read_bytes())==h
for x in json.loads((TC/'TC-FINAL-MANIFEST.v1.json').read_bytes())['files']:
 b=(TC/x['path']).read_bytes();assert sha(b)==x['sha256'] and len(b)==x['bytes']
dp=TC/'graph_challenge/distinct-challenge-decision.v1.json';decision=json.loads(dp.read_bytes())
assert decision['decision']=='ACCEPTED_EXACT_SOURCE_ONLY_TOPOLOGY_COVERAGE_AND_PORTS_FOR_UNCLAIMED_PREPARATION'
assert decision['blocking_findings']==0 and not decision['findings']
assert decision['independent_checks']['byte_character_hash_and_line_errors']==0
critical[dp]=sha(dp.read_bytes())
formation=json.loads((W/'v1-actual-formation.json').read_bytes());assert formation['exit_code']==0 and formation['theorem_proofs']==0
envraw=(W/'actual-environment-before-intake.json').read_bytes();assert json.loads(envraw)['HEAD']==head
before=L.read_bytes();states=advance._replay_advances([json.loads(x) for x in before.splitlines()])
assert ADV not in states
assert states['ASTIS-SA-20261113-GaussianComplexitySourceMatrixStructure']['state']=='VERIFIED'
discover=Path('runs/substantive_discoveries.jsonl').read_bytes();ds=advance._replay_discoveries([json.loads(x) for x in discover.splitlines()])
index=git('ls-files','--stage','-z');cache={}
def cached(p):
 if str(p) not in cache:cache[str(p)]=fingerprint(p)
 return cache[str(p)]
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
foreign_frontiers={str(p):sha(p.read_bytes()) for p in C.parent.rglob('*') if p.is_file() and not p.is_symlink()}
create(W/'preproof-baseline.private.json',dump({'head':head,'ledger_sha256':sha(before),'ledger_bytes':len(before),'all_foreign_states':states,'all_existing_frontier_hashes':foreign_frontiers,'tracked_git_index':index.decode(),'all_existing_tracked_fingerprints':tracked,'actual_control_fingerprints':controls,'scope':'PRIVATE full preservation only; no export of full foreign/control/index snapshots.'}))
create(W/'preproof-discoveries.private.json',dump({'ledger_sha256':sha(discover),'full_states':ds,'scope':'PRIVATE only'}))
originals={}
for root in [SG,TC]:
 for p in sorted(root.rglob('*')):
  if p.is_file() and '__pycache__' not in p.parts:
   assert not p.is_symlink() and not any(x.startswith('.PRIVATE') for x in p.parts)
   originals[str(p)]={'sha256':sha(p.read_bytes()),'bytes':p.stat().st_size}
E.mkdir();archive=E/'independent-preproof-originals.tar.gz'
with tarfile.open(archive,'x:gz') as tf:
 for n in originals:tf.add(n,arcname=n,recursive=False)
with tarfile.open(archive,'r:gz') as tf:
 assert len(tf.getmembers())==len(originals)
 for n,x in originals.items():
  b=tf.extractfile(n).read();assert len(b)==x['bytes'] and sha(b)==x['sha256']
create(E/'independent-preproof-originals.manifest.json',dump({'files':originals,'archive_sha256':sha(archive.read_bytes()),'private_guards_exported':False}))
admission={'exact_seal_sha256':sha(sealraw),'critical_inputs':{str(p):h for p,h in critical.items()},'distinct_topology_decision':decision['decision'],'topology_blocks':[],'binder_policy':'Public sole hq and literal original G conclusion antecedent. Private all-realDelta actual-event norm consequence explicitly a deterministic generalization. All mean/frame/Gram/sqrt/a<=1 facts internal; no source probability certificate.','source_only':True,'new_target_proofs':0,'source_original_files':len(originals)}
create(E/'preproof-source-admission.json',dump(admission));create(SP,sealraw);create(E/'actual-environment-before-intake.original.json',envraw)
parents=['AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixMean.actual_source_truncated_matrix_means','AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCosineGram.actual_cosine_frame_gram']
moment='AutoSamplingTheory.TechnicalLemmas.Probability.StdGaussianMoment.integrable_norm_sq_and_integral_stdGaussian'
searches=['Actual target-name and canonical-parent rg scan before intake found no existing public actual centered Gram realization; prior private aggregate-mean consumer retained and not promoted into public API.','Reuse exact actual source matrix-mean and cosine-frame Gram declarations; literal angle transport is internal, not a new hypothesis or duplicate frame theorem.','Private norm consumer reuses canonical standard Gaussian norm-square moment and actual retained-radius domination; no supplied bias/range certificate.','Source-first exact22node/15edge/9gap graph and distinct raw-first challenge cover123source locators plus72node/use-site locators; probabilities remain excluded.']
prior=json.loads(Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-matrix-structure.json').read_bytes())
reader=copy.deepcopy(prior['reader_contract']);reader['status']='Exact proof-free literal actual B/Gram types and independent source/binder/topology preparation accepted; P/T proof, source fidelity and reader delivery pending.'
graph=copy.deepcopy(prior['graph_contribution']);graph.update({'focus_targets':[seal['producer']['name']],'visual_review':'Independent source-only actual Gram graph accepted; no compiled graph or site-runtime claim.'})
boundary='Only original-experiment eventwise actual Gram realization on the inclusive all-row good event: sumZi=B^TB-aI and sumwiZi=B^Tdiag(w)B. Private actual Ex126 norm consequence conditions on the same-outcome actual centered-sum deviation event at arbitrary realDelta, discharging a<=1 internally. No probability of that event, Bernstein tail, full FactC6/Lemma4.4/Krylov/mainlowerbound, oracle/TV/precision/cap/cost, publicprivateconsumer API or integration/purification credit.'
cell={'schema_version':3,'cell_id':C.stem,'route':'samplewiki-route','mode':'faithfulPaper','title':'Actual centered source Gram realization with eventwise norm consumer','source_anchor':'arXiv2610.20492v1 C.2 p17 Ex125/126; original experiment, frame, inclusive cutoff and actual mean definitions. Source Bernstein/probabilities excluded.','target_statement':seal['producer']['signature']+'\nPrivate deterministic actual norm consumer\n'+seal['actual_private_consumer']['signature'],'status':'claimed','owner_id':OWNER,'advance_id':ADV,'parents':['ASTIS-SW-GAUSSIAN-COMPLEXITY-source-matrix-mean','ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-cosine-gram'],'consumers':[seal['actual_private_consumer']['name']],'shared_floor_audit':{'searched':searches,'classification':'adapt','decision':'reuse_existing','canonical_declaration':seal['producer']['name'],'canonical_shared_cell':''},'reuse_plan':{'searched_existing':searches,'reused_declarations':[],'planned_existing_P_parents':parents,'planned_private_T_parents':[seal['producer']['name'],moment],'new_shared_declarations':[],'known_consumers':[],'planned_consumers':[seal['actual_private_consumer']['name']],'no_duplicate_wrapper':True,'decision_reason':'New actual rectangular Gaussian-feature B/Gram identities materially feed the literal source Gram-deviation norm bounds. Reuse exact mean/frame/moment nodes; no arbitrary B/mean/frame or probability certificates.'},'reader_contract':reader,'graph_contribution':graph,'learning_contract':{'control_plane_math_authority':False,'process_memory_checked':True,'process_memory_ids':[],'failure_class':'NONE','salvage':{'required':True,'status':'completed','reason':'All proof-free source/formation/port/custody iterations retained. No mathematical route discarded or proof attempted.','promoted_fragments':[],'discarded_fragments':[]},'parallelism':{'decision':'serial','direction_fingerprints':[],'expected_information_gain':'One ROOT mathworker; distinct source extraction and independent topology challenge only.','shared_verified_context_digest':sha(sealraw)},'cross_route_blind_spot_audit':{'required':False,'status':'not-applicable','evidence':'','canonical_route':'','selection_reason':'No competing proof routes.'},'reader_backpressure':{'purification_status':'pending','exposition_seal_status':'pending','exposition_evidence':'','source_expansion_nodes':[],'lean_expansion_nodes':[],'assumptions_preserved':False,'boundary_preserved':True}},'source_detail_audit':{'primary_edition':'arXiv2610.20492v1 rawSHA '+seal['source']['sha256'],'primary_anchor':'C.2 p17 Ex125/126','detail_status':'omitted','gap':'Actual B tensor/Gram coordinate algebra, inverse-sqrt normalization, actual aggregate mean/frame transport and finite-matrix identity norm are internal obligations, not caller certificates. PrivateDelta generalization explicitly excludes stochastic probability claims.','consulted':[{'source':'Pinned raw source with independent raw-first SG and distinct TC','anchor':'Exactv3graph/v3coverage/v2ports and frozen challenge','hypothesis_adapter':'Solehq/q0, actualoriginalmu/rows/mean/a/B, inclusiveG and actualsame-outcome deviation antecedents preserved.'}],'fidelity_boundary':boundary},'statement_seal':{'status':'EXACT_LITERAL_TYPES_FORMED;SOURCE_TYPE_TOPOLOGY_PREPARATION_ACCEPTED;UNPROVED','file':str(SP),'sha256':sha(sealraw),'signature_sha256':seal['producer']['signature_sha256'],'private_consumer_signature_sha256':seal['actual_private_consumer']['signature_sha256']},'evidence':{'preproof_source_admission':{'file':str(E/'preproof-source-admission.json'),'sha256':sha(dump(admission))},'actual_literal_formation':formation,'actual_environment':{'file':str(E/'actual-environment-before-intake.original.json'),'sha256':sha(envraw)},'normal_API_calls':0,'target_proof_calls':0,'formalizer_API_pristine':False},'blocked':{},'owned_files':[P,T,str(C),str(SP),str(E)+'/', 'website/content/declaration_lessons/huanjian-gaussian-source-gram-realization.json','website/content/publications/huanjian-gaussian-source-gram-realization.json','research-wiki/semantic-roundtrip/audits/huanjian-gaussian-source-gram-realization.json'],'forbidden_shared_files':list(dict.fromkeys(prior['forbidden_shared_files']+['website/static/proof-readers.css','website/static/source-lineage.css'])),'truth_boundary':boundary,'conceptual_mirror_audit':{'status':'pending','discovery_ids':[]},'reservation_only':'Source-admitted exact type reservation, no target proof.'}
create(C,dump(cell));errors=frontiers.validate_cells(frontiers.load_cells());assert not errors,errors
proposal=advance.AdvanceProposal(advance_id=ADV,task_id='ASTIS-SW-GAUSSIAN-COMPLEXITY-2026',goal='Prove literal actual source centered and weighted Gram identities on original good event, and materially consume in deterministic actual Gram-deviation norm bounds, with all mean/frame/sqrt/bias facts internal and no stochastic probability certificate.',source_anchor=cell['source_anchor'],theorem_delta=seal['producer']['signature'],truth_boundary=boundary,created_by=OWNER,dag_inputs=(cell['source_anchor'],'Canonical actual matrix mean/cosine frame, plus canonical Gaussian moment in private consumer.'),proposed_files=tuple(p for p in cell['owned_files'] if not p.endswith('/')),focused_checks=('lake env lean '+P,'lake build Tests.GaussianComplexityFixedSpectrumSourceGramRealization'),modes=('source-reading','proof-design','compiler-diagnosis'),priority=50,frontier_cell=C.stem,target_declarations=(seal['producer']['name'],))
proposal.validate();create(W/'normal-intake-attempted.once.json',dump({'advance_id':ADV,'before_ledger_sha256':sha(before),'source_admission_sha256':sha(dump(admission)),'no_replay':True}))
ev={'statement_seal_sha256':sha(sealraw),'independent_topology':admission['distinct_topology_decision'],'truth_boundary':boundary,'formalizer_API_pristine':False}
advance.propose_advance(proposal);advance.transition_advance(ADV,'CLAIMED',worker_id=OWNER,evidence=ev);advance.transition_advance(ADV,'EXPLORING',worker_id=OWNER,evidence=ev)
after=L.read_bytes();assert after.startswith(before);append=after[len(before):];events=[json.loads(x) for x in append.splitlines()]
assert len(events)==3 and all(x['advance_id']==ADV for x in events)
now=advance._replay_advances([json.loads(x) for x in after.splitlines()]);assert now.pop(ADV)['state']=='EXPLORING' and now==states
assert git('ls-files','--stage','-z')==index
for p,fp in {**tracked,**controls}.items():
 if p!=str(L):assert fingerprint(Path(p))==fp
for p,h in foreign_frontiers.items():assert sha(Path(p).read_bytes())==h
assert Path('runs/substantive_discoveries.jsonl').read_bytes()==discover
cell['evidence']['normal_API_calls']=3;cell['reservation_only']='Normalledger EXPLORING; target proofs not attempted.';C.write_bytes(dump(cell));assert not frontiers.validate_cells(frontiers.load_cells())
create(E/'normal-EXPLORING-append.exact.jsonl',append)
summary={'state':'EXPLORING','actual_API_calls':3,'append_sha256':sha(append),'foreign_full_advances_preserved':len(states),'foreign_full_discoveries_preserved':len(ds),'foreign_regular_frontier_files_preserved':len(foreign_frontiers),'existing_tracked_fingerprints_preserved':len(tracked),'historical_control_fingerprints_preserved':len(controls),'control_count_qualification':'Historical runs and actual named controls, not a literal queue count.','source_original_files':len(originals),'private_guards_exported':False,'target_proof_calls':0,'ROOT_V_calls':0}
create(E/'normal-intake-preservation.json',dump(summary))
for n in ['statement-seal-v1.unclaimed.json','v1-actual-formation.json','GramFormation.v1.lean','start_gram_sau.py']:create(E/'intake-originals'/n,(W/n).read_bytes())
paths=[C,SP,L,*[p for p in sorted(E.rglob('*')) if p.is_file()]]
spec=W/'normal-intake-paths.private.nul';create(spec,b'\0'.join(str(p).encode() for p in paths)+b'\0')
subprocess.run(['git','add','-f','--pathspec-from-file='+str(spec),'--pathspec-file-nul'],check=True)
assert set(git('diff','--cached','--name-only').decode().splitlines())==set(map(str,paths))
subprocess.run(['git','diff','--cached','--check','--',str(C),str(SP),str(L)],check=True)
subprocess.run(['git','commit','--quiet','-m','Admit exact original-experiment Gaussian Gram realization packet'],check=True)
commit=git('rev-parse','HEAD').decode().strip();out={'intake_commit':commit,**summary};create(W/'actual-normal-intake-commit.json',dump(out));print(json.dumps(out))
