from pathlib import Path
import copy,datetime,hashlib,json,os,subprocess,sys
R=Path('E:/Samplinglib');O=Path(__file__).parent;B=O.parent
sys.path[:0]=[str(R),str(R/'tools')]
from tools.astis_advance import transition_advance,current_advances
C='SUCCESSOR_COMMIT_REQUIRED';ME='/root/exact_verify77'
ID='ASTIS-SA-20261011-PBPSActualFiniteHistoryExtension';CELL=R/'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-conditional-next-wait-density.json'
M=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteHistoryExtension.lean';A=R/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualFiniteHistoryExtension.json'
D='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteHistoryExtension.actual_finite_history_extension'
def path(p):
 p=Path(p);return p if p.is_absolute() else R/p
def load(p):return json.loads(path(p).read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def info(p):
 p=path(p);b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),raw_sha256=sha(b),bytes=len(b))
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def save(n,d):
 with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
def git(*args):return subprocess.check_output(['git',*args],cwd=R,stderr=subprocess.PIPE)
assert git('rev-parse','HEAD').decode().strip()==C and load(O/'checks-complete90.json')['status']=='PASS'
assert info(M)['raw_sha256']=='6cdc14328be5ec3ece3f028e6e1dd0185ee4031a8e651956ee0f55d4beebf029' and M.read_bytes()==git('show',C+':'+M.relative_to(R).as_posix())
freeze=load(O/'input-freeze90.json')
for group in ['exact_commit_matches','nested_mathlib_matches','local_fixed_primary_and_excluded_extracts','preexisting_collaborator_inputs']:
 for e in freeze[group]:assert info(e['path'])['raw_sha256']==e['raw_sha256']
preserved=load(O/'collaborator-preservation90.json')['RAWs'];assert len(preserved)==21
for e in preserved:assert info(e['path'])==e
before=current_advances();assert before[ID]['state']=='PROVED_LOCAL' and before[ID]['owner_id']=='companion_root_20261005'
lane={k:v for k,v in before.items() if v['state']=='STABILIZING'};assert set(lane)=={'ASTIS-SA-20261005-SPHMCImplementedPhaseKernel'}
cell=load(CELL);assert cell['status']=='proved_locally' and cell['graph_contribution']['lean_view']=='new-node'
save('cell.before-independent-admission90.json',cell)
ledger=R/'runs/substantive_advances.jsonl';ledger_before=ledger.read_bytes();save('ledger.before-admission90.json',info(ledger))
other_cells={p.relative_to(R).as_posix():sha(p.read_bytes()) for p in CELL.parent.glob('*.json') if p!=CELL};save('other-cells.before-admission90.json',other_cells)
receipts=[]
for n in ['packet','focused-module','current-kernel','contributor','publication','publication-reviewed','semantic','frontier']:
 p=O/(n+'.receipt.json');d=load(p);assert d['exit_code']==0 and d['terminal_closed'] and d['checked_commit']==C
 for k in ['stdout','stderr']:assert info(d[k]['path'])==d[k]
 receipts.append(info(p))
audit=load(A);source=B/'independent-source90';native=load(source/'source-review89.decision.v2.native.json');math=B/'independent-math90';kernel=load(math/'kernel-dependency90.json');dec=R/'runs/semantic-decoder-outputs/round90'
assert audit['state']=='accepted' and audit['source_review']['reviewer']=='/root/fresh_source87'
assert audit['publication_binding_sha256']=='b3a9241d785c8132839c366f260d5fbc3dcaa40aba8566560ec814e6c5716472'
assert not load(O/'fake-closure-scan90.json')['hits'] and not native['blocking_deltas'] and not native['repairs'] and len(audit['semantic_slots'])==7
v=dict(status='PASS_INDEPENDENT_EXACT_COMMIT_VERIFICATION',verifier_id=ME,verified_commit=C,created_utc=now(),actual_admission_helper_PID=os.getpid(),lean_module=info(M),gate=receipts,publication_declarations=[D],publication_binding_sha256=audit['publication_binding_sha256'],semantic_roundtrip_audit='ASTIS-RT-20261011-PBPSActualFiniteHistoryExtension',
 source_audit=dict(state='accepted',reviewer='/root/fresh_source87',review_result=info(source/'source-review90.decision.native.json'),review_run=info(source/'source-review90.run.native.json'),native_manifest=info(source/'closed-raw-manifest.source-review90.native.json'),reviewer_packet_sha256=audit['source_review']['reviewer_packet_sha256'],immutable_source_first_chronology_verified=True,canonical_seven_semantic_slots_exact_native=True,topology_creator_not_self_approving=True,distinct_topology_repair=info(R/'runs/20261007-companion-priority/pbps-next-history-extension-preread90/independent-topology-repair90/decision90.native.json'),coverage='All28literaldefinitions/sixanalytic/sevensemantic slots/six contiguous BODY formula regions accepted;22localdispositions/3AND. One next-history strict finite transport step only.',accepted_truth_boundary=native['accepted_truth_boundary']),
 blind_decoder=dict(identity='/root/blind_decoder90',manifest=info(dec/'manifest.json'),native_run=info(dec/'decoder-run.json'),native_result=info(dec/'reconstruction.json'),packet=info(B/'anonymous.decoder90.json'),source_text_visible=False,source_identity_visible=False,hash_recipe='Native90 raw packet equals frozen anonymous input; declared canonical hash excludes only top-level packet_sha256. UTF8 statement/reconstruction and native run hashes verified. All disclosure flags false; no extra mathematical inputs.',native_uncertainties=info(source/'decoder90.uncertainties.native.json'),interpretation='Infimum alone does not prove attainment; actual guarded implementation proves the needed identity. No infinite-path/nonexplosion/unconditional normalization claim inferred.'),
 fake_closure_scan=info(O/'fake-closure-scan90.json'),standard_axioms=['propext','Classical.choice','Quot.sound'],fresh_current_focused_build=info(O/'focused-module.receipt.json'),fresh_current_public_kernel=info(O/'current-kernel.receipt.json'),reused_complete_source_elaboration=info(math/'fresh-whole-source-kernel.receipt.json'),independent_mathematics=info(math/'decision90.json'),independent_mathematics_closed_manifest=info(math/'closed-RAW-manifest90.json'),independent_complete_exposition=info(math/'final-exposition89.audit.json'),kernel_generated_and_transitive_ASTIS_proof_closure=info(math/'kernel-dependency90.json'),actual_public_producer_dependencies=kernel['immediate_public_producers'],owned_proof_constant_count=11,immediate_public_ASTIS_dependency_count=4,immediate_private_generated_ASTIS_dependency_count=18,transitive_ASTIS_constant_count=95,transitive_ASTIS_edge_count=170,transitive_ASTIS_source_files=12,
 generic_reuse_boundary='Pinned Mathlib supplies finite tuples, measurable products/maps/restrictions and nonnegative product integration. Actual89 density, actual87 history-tail law, actualHarmonicFlow and actualBounceRate are genuinely consumed internally. No supplied provider, no survival88 AND.',
 evidence_reuse_reason='Named successor science module Git blob equals unchanged own full source RAW6cdc exactly. Complete type+value/generated closure and six exhaustive BODY/formula regions reuse accepted independent mathematics. Fresh current build/public kernel and scoped admission gates PASS.',lossless_native_archive_audit=info(O/'lossless-archives90.audit.json'),exact_science_freeze=info(O/'input-freeze90.json'),
 mathematical_cases=['All6original analytic assumptions and28literaldefinitions; deterministic depth, full finite tagged history, Borel d/F/A.','Guarded positive finite wait below cutoff yields actual next history by total append; zero/negative append totalization uses max(s,0), not a source premise.','Stopped/top/zero-cutoff/rank0/flat-hazard/zero-normal/endpoints and unrealizable histories retain exact semantics.','Joint and marginal next-history laws have mass<=1; all ENNReal tests including infinity and null old-history A covered without normalization.'],
 truth_boundary=load(B/'claim.json')['truth_boundary'],remaining_acceptance=['Existing sole-lane shared imports/Registry/rootTests/full aggregate/graph/site integration','Browser/reader visual/live delivery, main merge and postmerge ExpositionSeal/PURIFIED','Remaining S87-I5 ordered-time/path assembly, density multiplication/absolute-time change/final-survival/count partition; fullG86-11/A7/summability','Physical-time restart/random stopping/Markov/CK/reversal/invariance/Jensen/allL2','Implementation/error/cost/main/actual-input composition/fullpaper/four-paperGoal'],
 all21collaborator_RAWs_preserved=True,production_edits=False,stabilization=False,PURIFIED=False,Goal_complete=False,provenance='Independent exact named-science verifier distinct from proving owner, neutral blind decoder and final source reviewer. No canonical source graph mutation or self-source acceptance.')
save('verified.json',v)
e={k:v[k] for k in ['verifier_id','verified_commit','source_audit','fake_closure_scan','publication_declarations','semantic_roundtrip_audit']};e['gate']=info(O/'verified.json')
transition_advance(ID,'VERIFIED',worker_id=ME,evidence=e)
new=copy.deepcopy(cell);new['status']='independently_verified';new['evidence']['independent_verification']=(O/'verified.json').relative_to(R).as_posix()
CELL.write_text(json.dumps(new,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
after=current_advances();assert after[ID]['state']=='VERIFIED';assert {k:v for k,v in after.items() if k!=ID}=={k:v for k,v in before.items() if k!=ID}
ledger_after=ledger.read_bytes();assert ledger_after.startswith(ledger_before) and len(ledger_after[len(ledger_before):].splitlines())==1
rest=copy.deepcopy(load(CELL));rest['status']=cell['status']
if 'independent_verification' in cell.get('evidence',{}):rest['evidence']['independent_verification']=cell['evidence']['independent_verification']
else:rest['evidence'].pop('independent_verification')
assert rest==cell and {p.relative_to(R).as_posix():sha(p.read_bytes()) for p in CELL.parent.glob('*.json') if p!=CELL}==other_cells
for x in preserved:assert info(x['path'])==x
save('admission90.json',dict(state='VERIFIED',cell_state='independently_verified',verified_commit=C,verifier_id=ME,verified=info(O/'verified.json'),cell=info(CELL),ledger=info(ledger),exactly_one_append_only_event=True,independent_verification_is_string=True,all_other_cell_metadata_semantically_preserved=True,all_other_cell_RAWs_preserved=True,all_other_advances_unchanged=True,existing_stabilizing_lane_unchanged=[dict(id=k,owner=v['owner_id']) for k,v in lane.items()],all21collaborator_RAWs_preserved=True,stabilization=False,Goal_complete=False))
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf8');args=[sys.executable,'-X','utf8','tools/astis_frontier_cells.py','check'];start=now()
with (O/'post-admission-frontier.stdout.log').open('xb') as out,(O/'post-admission-frontier.stderr.log').open('xb') as err:
 child=subprocess.Popen(args,cwd=R,env=env,stdout=out,stderr=err);print('post-admission-frontier foreground PID',child.pid,flush=True);code=child.wait()
save('post-admission-frontier.receipt.json',dict(command=args,actual_foreground_PID=child.pid,exit_code=code,terminal_closed=True,checked_science_commit=C,started_utc=start,finished_utc=now(),stdout=info(O/'post-admission-frontier.stdout.log'),stderr=info(O/'post-admission-frontier.stderr.log')));assert code==0
for x in preserved:assert info(x['path'])==x
save('run-manifest90.json',dict(status='CLOSED_INDEPENDENT_EXACT_SCIENCE_ADMISSION',verified_commit=C,verifier_id=ME,verified=info(O/'verified.json'),admission=info(O/'admission90.json'),gate_receipts=receipts+[info(O/'post-admission-frontier.receipt.json')],science_input_freeze=info(O/'input-freeze90.json'),archive_audit=info(O/'lossless-archives89.audit.json'),postscience_cell_and_ledger_only=True,production_or_shared_integration_edits=False,all21collaborator_RAWs_preserved=True,native_reasoning_trajectory_claimed=False))
owned=[info(p) for p in sorted(O.iterdir()) if p.is_file()]
save('closed-RAW-manifest90.json',dict(status='CLOSED_RAW_NONCIRCULAR',verified_commit=C,verifier_id=ME,checked_science_inputs=freeze['exact_commit_matches'],nested_pinned_mathlib=freeze['nested_mathlib_matches'],local_fixed_primary_runtime_cache_and_excluded_snapshots=freeze['local_fixed_primary_and_excluded_extracts'],preexisting_collaborator_inputs=freeze['preexisting_collaborator_inputs'],owned_artifacts=owned,self_hash_intentionally_omitted=True,admission_cell_and_ledger_are_explicit_postscience_changes=True,science_input_cell_ledger_hashes_bind_named_git_commit_not_postadmission_worktree=True,native_review_inputs_unchanged=True,all21collaborator_RAWs_preserved=True))
for i in owned:assert info(i['path'])==i
assert git('rev-parse','HEAD').decode().strip()==C
print(json.dumps(dict(status='VERIFIED_NATIVE_CLOSED',verified_commit=C,verified=info(O/'verified.json'),manifest=info(O/'closed-RAW-manifest90.json'),admission=info(O/'admission90.json'),post_admission_frontier=info(O/'post-admission-frontier.receipt.json')),indent=2),flush=True)
