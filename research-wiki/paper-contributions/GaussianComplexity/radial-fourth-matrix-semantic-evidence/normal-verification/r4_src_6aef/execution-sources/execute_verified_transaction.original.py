from pathlib import Path
import datetime, hashlib, json, os, stat, subprocess, sys, time

ROOT=Path.cwd();sys.path.insert(0,str(ROOT))
from tools.astis_advance import _replay_advances, _replay_discoveries
BASE=ROOT/'.astis/semantic-neutral-20261111/r4_src_6aef/normal-verification'
LOCAL=BASE/'local-only'
E=ROOT/'research-wiki/paper-contributions/GaussianComplexity/radial-fourth-matrix-semantic-evidence'
OUT=E/'normal-verification/r4_src_6aef'
HEAD='3ba24f46ea74e4537e57824982dfee9f51aeac27';MATH='69a3336dde302c4a34dbd88708ff6226b2bd0e87'
ADV='ASTIS-SA-20261111-GaussianComplexityRadialFourthMatrix';ACTOR='/root/radial_fourth_fresh_source_6aef'
DECL='AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumRadialFourthMoment.actual_radial_fourth_moment_matrix'
PY='/opt/anaconda3/bin/python'
def sha(b):return hashlib.sha256(b).hexdigest()
def enc(v):return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode()
def canon(v):return json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()
def git(*args):return subprocess.run(['git',*args],cwd=ROOT,check=True,capture_output=True).stdout
def binding(p):
    p=Path(p);b=p.read_bytes();return {'path':str(p.relative_to(ROOT) if p.is_absolute() else p),'bytes':len(b),'sha256':sha(b)}
baseline=json.loads((LOCAL/'baseline.full.local-only.json').read_bytes())
preflight=json.loads((OUT/'preflight-assessment.json').read_bytes())
assert git('rev-parse','HEAD').decode().strip()==HEAD
prefix=(LOCAL/'advances.prefix.original.local-only.jsonl').read_bytes()
assert (ROOT/'runs/substantive_advances.jsonl').read_bytes()==prefix
assert (ROOT/'runs/substantive_discoveries.jsonl').read_bytes()==(LOCAL/'discoveries.original.local-only.jsonl').read_bytes()
C=ROOT/baseline['C'];originalC=(LOCAL/'C.before.original.local-only.json').read_bytes();assert C.read_bytes()==originalC
assert not (OUT/'transition-attempted.once.json').exists()
decision_path=E/'actual-VERIFIED-independent-decision.json';assert not decision_path.exists()
pl_raw=(E/'actual-PROVED_LOCAL-evidence.full.json').read_bytes();pl=json.loads(pl_raw)
append_raw=(E/'actual-PROVED_LOCAL-append.exact.jsonl').read_bytes()
assert sha(pl_raw)=='f4bc0bedf3a46a4232f369a55a28ce88cc33122bd9b2a50419912cc381030773'
assert sha(append_raw)=='a46e0b650bf2aa227cc9b4d2ee322ec06204d947199019ab4575dd76481a6262'

truth=('Verified scope is the canonical standard Gaussian radial fourth matrix moment and the actual individual uncentered squared-summand PSD consequence, with integrability internal and q=0 included. '
 'Original-family law/integral transport, aggregation, centered variance, matrix concentration, full Lemma 4.4, both main lower bounds and oracle/TV/cost adapters remain open. '
 'Serialized/shared integration, root aggregate acceptance, actual desktop/mobile/public delivery, full source-index/graph/copy/download integration and purification remain pending.')
native=E/'native-review/r4_native_7f24'
decision={'schema_version':1,'kind':'original independent normal VERIFIED admission decision',
 'reviewer':ACTOR,'independent_from_proof_owner':True,'proof_owner':'huanjian_gc_20261111_radial_fourth_matrix',
 'advance_id':ADV,'decision':'ACCEPT_ONE_NORMAL_PROVED_LOCAL_TO_VERIFIED_TRANSACTION',
 'checked_metadata_HEAD':HEAD,'native_mathematical_candidate':MATH,
 'compilation_boundary':'Controlled-native compilation and literal kernel checks are for immutable69a3336. Current3ba metadata/code/source/audit/report hashes were independently checked exact; no new3ba native recompilation is claimed.',
 'source_audit':{'original_report':binding(E/'source-review/r4_src_6aef/original-mathematical-report.md'),
  'overlay':binding(E/'source-review/r4_src_6aef/audit-overlay.json'),
  'whole_module_original':binding(ROOT/'.astis/semantic-neutral-20261111/r4_src_6aef/code-only-source-report.md'),
  'source_sha256':'6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915',
  'publication_binding_sha256':pl['publication_binding_sha256'],'verdict':'equivalent-after-elaboration','all_7_slots_checked':True,'all_5_code_folds_exact':True,'all_49_source_code_background_spans_exact':True},
 'normal_reviewed_publication_gate':preflight['normal_reviewed_publication_gate'],
 'native_original_report':preflight['native_original_report'],'native_original_manifest':preflight['native_manifest'],
 'native_exact_receipt_supplement':preflight['native_supplement'],
 'independent_native_assessment':{'six_original_successful_receipts_and_streams_hash_checked':True,'isolated_ASTIS_source_closure_compiled':True,
  'literal_producer_and_actual_private_consumer_kernel_applications_passed':True,
  'all_owned_generated_declarations':8,'axioms_only':['propext','Classical.choice','Quot.sound'],
  'all_owned_generated_reachable':True,'actual_direct_parent_edges_match_code':True,
  'bounded_static_render_accepted':True,'browser_and_public_integration_not_claimed':True},
 'final_actual_strict_gates_assessed':preflight['final_strict_gates'],
 'formalizer_API_pristine':False,'pristine_chronology_certified':False,
 'proved_local_original_payload':binding(E/'actual-PROVED_LOCAL-evidence.full.json'),
 'proved_local_original_append':binding(E/'actual-PROVED_LOCAL-append.exact.jsonl'),
 'preflight_assessment':binding(OUT/'preflight-assessment.json'),
 'truth_boundary':truth,'authorized_canonical_changes':'One existing normal advance transition API call and only C.status plus C.evidence.independent_verification.',
 'foreign_preservation_required':preflight['preservation_preconditions'],
 'outcome_is_recorded_separately':'normal-verification/r4_src_6aef/actual-outcome.json'}
decision_path.write_bytes(enc(decision))
evidence={'verifier_id':ACTOR,'verified_commit':HEAD,'native_mathematical_candidate':MATH,
 'gate':{'normal_reviewed_publication_admission':preflight['normal_reviewed_publication_gate'],
         'final_actual_strict_gates':preflight['final_strict_gates'],
         'six_original_native_kernel_static_receipts':preflight['native_successful_receipts'],
         'scope':'Bounded canonical row moment plus individual PSD consequence; no aggregate repository/root/public integration gate claimed.'},
 'source_audit':decision['source_audit'],
 'semantic_roundtrip_audit':{'path':'research-wiki/semantic-roundtrip/audits/huanjian-gaussian-radial-fourth-matrix.json',
    'sha256':preflight['current_audit']['sha256'],'state':'accepted','verdict':'equivalent-after-elaboration',
    'publication_binding_sha256':pl['publication_binding_sha256']},
 'fake_closure_scan':{'native_report':preflight['native_original_report'],
    'native_declaration_audit':binding(native/'portable/native-declaration-audit.json'),
    'result':'All8 owned/generated source-closure declarations have bodies, are reachable, are not unsafe/partial/axiom and use only propext/Classical.choice/Quot.sound or no axioms. Production forbidden-pattern scan has no hits.'},
 'publication_declarations':pl['publication_declarations'],
 'independent_decision':binding(decision_path),'truth_boundary':truth,
 'formalizer_API_pristine':False,'pristine_chronology_certified':False,
 'proved_local_evidence':pl,
 'proved_local_evidence_binding':binding(E/'actual-PROVED_LOCAL-evidence.full.json'),
 'proved_local_exact_append_binding':binding(E/'actual-PROVED_LOCAL-append.exact.jsonl'),
 'proved_local_append_carried_exact':binding(OUT/'PROVED_LOCAL-append.original.exact.jsonl'),
 'native_original_report':preflight['native_original_report'],
 'native_portable_manifest':preflight['native_manifest'],'native_reproducibility_supplement':preflight['native_supplement']}
assert evidence['proved_local_evidence']==json.loads(pl_raw)
(OUT/'VERIFIED-evidence.full.json').write_bytes(enc(evidence))
marker={'advance_id':ADV,'actor':ACTOR,'from_state':'PROVED_LOCAL','to_state':'VERIFIED',
 'evidence_sha256':sha((OUT/'VERIFIED-evidence.full.json').read_bytes()),
 'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'api_attempt_number':1,
 'HEAD':HEAD,'advance_ledger_prefix_sha256':sha(prefix)}
(OUT/'transition-attempted.once.json').write_bytes(enc(marker))

command=[PY,'-B',str((BASE/'transition_once.py').relative_to(ROOT))]
start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
run=subprocess.run(command,cwd=ROOT,capture_output=True)
(OUT/'actual-VERIFIED-transaction.stdout').write_bytes(run.stdout);(OUT/'actual-VERIFIED-transaction.stderr').write_bytes(run.stderr)
receipt={'argv':command,'cwd':str(ROOT),'started_utc':start,'elapsed_seconds':time.monotonic()-t,
 'exit_code':run.returncode,'HEAD_before':HEAD,'HEAD_after':git('rev-parse','HEAD').decode().strip(),
 'stdout_sha256':sha(run.stdout),'stderr_sha256':sha(run.stderr),'normal_transition_API_attempts':1,
 'actor':ACTOR,'advance_id':ADV,'request_evidence_sha256':sha((OUT/'VERIFIED-evidence.full.json').read_bytes())}
(OUT/'actual-VERIFIED-transaction.receipt.json').write_bytes(enc(receipt))
if run.returncode!=0:
    (OUT/'actual-outcome.json').write_bytes(enc({'outcome':'NORMAL_API_FAILED_NO_RETRY','receipt':binding(OUT/'actual-VERIFIED-transaction.receipt.json'),'C_mutated':False}))
    print(run.stdout.decode());print(run.stderr.decode(),file=sys.stderr);raise SystemExit(run.returncode)

after_raw=(ROOT/'runs/substantive_advances.jsonl').read_bytes();assert after_raw.startswith(prefix)
added=after_raw[len(prefix):];rows=[json.loads(x) for x in added.splitlines() if x.strip()];assert len(rows)==1
event=rows[0];assert event['advance_id']==ADV and event['event']=='transition' and event['from_state']=='PROVED_LOCAL' and event['to_state']=='VERIFIED' and event['worker_id']==ACTOR
assert event['evidence']==evidence and event['evidence']['proved_local_evidence']==pl
(OUT/'actual-VERIFIED-append.exact.jsonl').write_bytes(added)
assert C.read_bytes()==originalC
newC=originalC.replace(b'"status": "proved_locally"',b'"status": "independently_verified"',1)
needle=b'"independent_verification": ""';assert originalC.count(needle)==1
newC=newC.replace(needle,b'"independent_verification": '+json.dumps(str(decision_path.relative_to(ROOT))).encode(),1)
oldobj=json.loads(originalC);newobj=json.loads(newC);expect=json.loads(originalC)
expect['status']='independently_verified';expect['evidence']['independent_verification']=str(decision_path.relative_to(ROOT));assert newobj==expect
temp=C.with_name(C.name+'.r4_src_6aef.tmp');temp.write_bytes(newC);os.chmod(temp,stat.S_IMODE(C.stat().st_mode));os.replace(temp,C)

# Required actual whole-frontier check after the only permitted cell update.
command=[PY,'-B','tools/astis_frontier_cells.py','check'];start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
frontier=subprocess.run(command,cwd=ROOT,capture_output=True)
(OUT/'post-VERIFIED-whole-frontier.stdout').write_bytes(frontier.stdout);(OUT/'post-VERIFIED-whole-frontier.stderr').write_bytes(frontier.stderr)
fr={'argv':command,'cwd':str(ROOT),'started_utc':start,'elapsed_seconds':time.monotonic()-t,'exit_code':frontier.returncode,
 'HEAD_before':HEAD,'HEAD_after':git('rev-parse','HEAD').decode().strip(),'stdout_sha256':sha(frontier.stdout),'stderr_sha256':sha(frontier.stderr)}
(OUT/'post-VERIFIED-whole-frontier.receipt.json').write_bytes(enc(fr))

# Full state equality is computed privately; only hashes/counts leave local custody.
after_states=_replay_advances([json.loads(x) for x in after_raw.splitlines() if x.strip()])
foreign_after={k:v for k,v in after_states.items() if k!=ADV}
discovery_after=(ROOT/'runs/substantive_discoveries.jsonl').read_bytes()
discoveries_after=_replay_discoveries([json.loads(x) for x in discovery_after.splitlines() if x.strip()])
older_after={}
for p in (ROOT/'research-wiki/frontier-cells').rglob('*'):
    if stat.S_ISREG(p.lstat().st_mode) and p!=C:older_after[str(p.relative_to(ROOT))]=sha(p.read_bytes())
tracked_after={}
for name,entry in baseline['tracked_files'].items():
    p=ROOT/name
    if p.is_symlink():tracked_after[name]={'type':'symlink','sha256':sha(os.readlink(p).encode())}
    elif p.is_file():tracked_after[name]={'type':'file','sha256':sha(p.read_bytes())}
    elif p.is_dir():tracked_after[name]={'type':'directory'}
    else:tracked_after[name]={'type':'missing'}
tracked_changed=[k for k in tracked_after if tracked_after[k]!=baseline['tracked_files'][k]]
assert foreign_after==baseline['foreign_states'] and len(foreign_after)==303
assert discovery_after==(LOCAL/'discoveries.original.local-only.jsonl').read_bytes()
assert discoveries_after==baseline['discovery_states'] and len(discoveries_after)==43
assert older_after==baseline['older_frontier_files'] and len(older_after)==463
assert tracked_changed==[str(C.relative_to(ROOT))]
assert after_states[ADV]['state']=='VERIFIED' and after_states[ADV]['last_actor']==ACTOR
assert json.loads(C.read_bytes())==expect and git('rev-parse','HEAD').decode().strip()==HEAD
preservation={'schema_version':1,'kind':'hash-only preservation; full foreign/control states stay local',
 'HEAD_before':HEAD,'HEAD_after':HEAD,'HEAD_unchanged':True,
 'advance_ledger':{'prefix_bytes':len(prefix),'prefix_sha256':sha(prefix),'exact_prefix_unchanged':after_raw[:len(prefix)]==prefix,
  'after_bytes':len(after_raw),'after_sha256':sha(after_raw),'one_exact_new_record':True,'append_sha256':sha(added),
  'target_only':ADV,'from_state':'PROVED_LOCAL','to_state':'VERIFIED','actor':ACTOR},
 'foreign_FULL_replayed_advance_states':{'count':303,'complete_nested_objects_equal':True,'before_sha256':baseline['foreign_states_sha256'],'after_sha256':sha(canon(foreign_after))},
 'discovery_ledger':{'exact_bytes_unchanged':True,'before_sha256':baseline['discovery_ledger_sha256'],'after_sha256':sha(discovery_after)},
 'all_discovery_FULL_states':{'count':43,'complete_nested_objects_equal':True,'before_sha256':baseline['discovery_states_sha256'],'after_sha256':sha(canon(discoveries_after))},
 'older_frontier_regular_files':{'count':463,'README_included':True,'all_paths_and_hashes_equal':True,'before_inventory_sha256':baseline['older_frontier_files_sha256'],'after_inventory_sha256':sha(canon(older_after))},
 'C_only_allowed_fields_changed':{'path':str(C.relative_to(ROOT)),'before_sha256':sha(originalC),'after_sha256':sha(C.read_bytes()),
  'changed_fields':['status','evidence.independent_verification'],'no_other_field_changed':True},
 'tracked_tree':{'existing_tracked_paths_changed_only':[str(C.relative_to(ROOT))],'other_existing_tracked_contents_unchanged':True},
 'normal_transition_API_calls':1,'other_ledger_mutation_API_calls':0,'event_replay_append_used':False,
 'whole_frontier_after':binding(OUT/'post-VERIFIED-whole-frontier.receipt.json'),'whole_frontier_exit_code':frontier.returncode,
 'full_local_snapshots_exported':False}
(OUT/'hash-only-preservation-report.json').write_bytes(enc(preservation))
outcome={'schema_version':1,'outcome':'VERIFIED' if frontier.returncode==0 else 'VERIFIED_WITH_POSTCHECK_FAILURE',
 'advance_id':ADV,'actor':ACTOR,'normal_API_calls':1,'metadata_HEAD':HEAD,'native_mathematical_candidate':MATH,
 'actual_append':binding(OUT/'actual-VERIFIED-append.exact.jsonl'),'actual_transaction_receipt':binding(OUT/'actual-VERIFIED-transaction.receipt.json'),
 'actual_independent_decision':binding(decision_path),'C_status':'independently_verified',
 'whole_frontier_after':binding(OUT/'post-VERIFIED-whole-frontier.receipt.json'),'whole_frontier_exit_code':frontier.returncode,
 'hash_only_preservation_report':binding(OUT/'hash-only-preservation-report.json'),'truth_boundary':truth,
 'formalizer_API_pristine':False,'pristine_chronology_certified':False,
 'no_further_canonical_mutation_by_this_reviewer':True}
(OUT/'actual-outcome.json').write_bytes(enc(outcome))
entries=[]
for p in [decision_path,*sorted(OUT.iterdir())]:
    if p.is_file() and p.name!='portable-custody-manifest.json':
        entry=binding(p);entry.update({'destination':entry['path'],'classification':'bounded-original-normal-verification-evidence'});entries.append(entry)
manifest={'schema_version':1,'advance_id':ADV,'actor':ACTOR,'outcome':outcome['outcome'],'metadata_HEAD':HEAD,'native_mathematical_candidate':MATH,
 'entries':entries,'total_payload_bytes':sum(e['bytes'] for e in entries),
 'excluded':'Full before/after foreign advance states, discovery states, complete ledgers and frontier/control snapshots remain only in reviewer local-only custody and are not exported. Existing native/source custody sets are referenced by exact hashes, not recopied.',
 'normal_API_calls':1,'no_further_canonical_mutation_by_this_reviewer':True}
(OUT/'portable-custody-manifest.json').write_bytes(enc(manifest))
print(json.dumps({'outcome':outcome['outcome'],'normal_API_calls':1,'append_sha256':sha(added),
 'decision_sha256':sha(decision_path.read_bytes()),'VERIFIED_evidence_sha256':sha((OUT/'VERIFIED-evidence.full.json').read_bytes()),
 'transaction_receipt_sha256':sha((OUT/'actual-VERIFIED-transaction.receipt.json').read_bytes()),
 'whole_frontier_exit':frontier.returncode,'preservation_report_sha256':sha((OUT/'hash-only-preservation-report.json').read_bytes()),
 'outcome_report_sha256':sha((OUT/'actual-outcome.json').read_bytes()),
 'portable_manifest_sha256':sha((OUT/'portable-custody-manifest.json').read_bytes()),
 'portable_manifest':str((OUT/'portable-custody-manifest.json').relative_to(ROOT)),
 'foreign_FULL_states_preserved':303,'discovery_states_and_ledger_bytes_preserved':43,'older_frontier_regular_files_preserved':463,
 'HEAD_unchanged':True,'tracked_changes_only_C_two_fields':True},indent=2))
if frontier.returncode!=0:raise SystemExit(frontier.returncode)
