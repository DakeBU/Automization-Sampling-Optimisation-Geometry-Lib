from common_v2 import *
pre=json.loads((OUT/'pre-invariants.json').read_bytes());post=json.loads((OUT/'post-invariants.json').read_bytes());a=json.loads((OUT/'acceptance-checks.json').read_bytes());outcome=json.loads((OUT/'normal-api-outcome.json').read_bytes())
assert post['result']=='pass' and post['own_state']=='VERIFIED' and post['own_cell']['status']=='independently_verified'
assert outcome['normal_API_calls']==1 and outcome['api_returned_successfully'] and outcome['error'] is None and outcome['actual_target_VERIFIED_events']==1
assert git('rev-parse','HEAD').decode().strip()==HEAD
assert git('rev-parse','refs/heads/main').decode().strip()==LOCAL_MAIN and git('rev-parse','refs/remotes/origin/main').decode().strip()==ORIGIN_MAIN
assert info(ROOT/LEDGER)['sha256']==post['ledger']['sha256'] and info(ROOT/CELL)['sha256']==post['own_cell']['raw_sha256']
labels=['pre-frontier','pre-preservation','pre-preservation-v2','acceptance-v1','acceptance-v2','prepare-decision','normal-api','post-frontier','post-preservation']
check_exits={}
for label in labels:
 r=json.loads((OUT/'receipts'/f'{label}.json').read_bytes());check_exits[label]=r['exit_code']
 for kind in ['stdout','stderr']:
  p=ROOT/r[kind]['path'];b=p.read_bytes();assert len(b)==r[kind]['bytes'] and sha(b)==r[kind]['sha256']
assert {k:v for k,v in check_exits.items() if v!=0}=={'pre-preservation':1,'acceptance-v1':1}
sources={}
def exact_copy(source,destination):
 b=source.read_bytes();destination.parent.mkdir(parents=True,exist_ok=True)
 if destination.exists():assert destination.read_bytes()==b
 else:destination.write_bytes(b)
 sources[rel(destination)]=rel(source)
for name in ['actual-PROVED_LOCAL-evidence.full.json','actual-PROVED_LOCAL-append.exact.jsonl','actual-PROVED_LOCAL-run.log','actual-PROVED_LOCAL-run.receipt.json']:
 exact_copy(E/name,OUT/'inputs/PROVED_LOCAL'/name)
N=E/'native-review/ri_native_74b8'
for name in ['report.json','portable-manifest.json','portable-evidence.tar.gz','relevant-input-binding.json','metadata-carrier-byte-comparison.json']:
 exact_copy(N/name,OUT/'inputs/native-originals'/name)
S=E/'source-review/ri_src_5ab9'
for source,dest in [(S/'phase4_review/review-report.md','review-report.md'),(S/'phase4_review/canonical-overlay.json','canonical-overlay.json'),(S/'portable-manifest.json','portable-manifest.json')]:
 exact_copy(source,OUT/'inputs/source-review-originals'/dest)
exact_copy(ROOT/'research-wiki/semantic-roundtrip/audits/huanjian-gaussian-source-row-independence.json',OUT/'inputs/source-review-originals/canonical-audit.original.json')
exact_copy(ROOT/'research-wiki/paper-contributions/GaussianComplexity/source-row-independence-statement-seal.json',OUT/'inputs/source-row-independence-statement-seal.original.json')
exact_copy(ROOT/'.agents/skills/astis-substantive-advance/SKILL.md',OUT/'inputs/protocol/astis-substantive-advance.SKILL.md')
for x in a['four_final_gates']:
 for field in ['receipt','log']:
  p=ROOT/x[field]['path'];exact_copy(p,OUT/'inputs/final-gates'/p.name)
sources[rel(OUT/'decision.original.json')]=rel(E/'actual-VERIFIED-independent-decision.json')
assert (OUT/'decision.original.json').read_bytes()==(E/'actual-VERIFIED-independent-decision.json').read_bytes()
refs=[E.parent/'source-row-law-semantic-evidence/normal-verification/rl_src_3dd4'/name for name in ['perform_normal_transition.py','state_checks_v2.py','prepare_decision.py','run.py']]
write(OUT/'inputs-exposure.json',{
 'verifier_id':WORKER,'task':'Separately authorized independent normal VERIFIED after genuine PL, native/source review and final gates; no root transition.',
 'mathematical_and_native_candidate_only':CANDIDATE,'held_metadata_HEAD':HEAD,'local_main':LOCAL_MAIN,'origin_main':ORIGIN_MAIN,
 'exact_input_copies':[{'source':source,'destination':dest,**{k:v for k,v in info(ROOT/dest).items() if k!='path'}} for dest,source in sources.items()],
 'process_only_reference_reads':[info(p) for p in refs]+[info(ROOT/'tools/astis_advance.py'),info(ROOT/'.agents/skills/astis-substantive-advance/SKILL.md')],
 'full_state_read_policy':'Ledger/discovery replay and tracked/frontier file inventories were evaluated in memory and exported only as counts/aggregate full-state and full-byte/mode SHA256. No broad foreign/control snapshot or ledger prefix exported.',
 'native_review_policy':'Actual bounded native originals now read only after prior own raw/type/code/fresh-source freezes. All460 listed files and461 archive members rehashed,106 receipt/212 streams, three local .oleans and excluded local full body dump independently rehashed. Frozen archive was never modified or supplemented.',
 'retained_failures':[{'class':'IMPLEMENTATION_FAILED','diagnosis':'precheck-v1-diagnosis.json','rejected_scripts':['common_v1.py','state_checks_v1.py'],'receipt':'receipts/pre-preservation.json'},{'class':'IMPLEMENTATION_FAILED','diagnosis':'acceptance-v1-diagnosis.json','rejected_scripts':['acceptance_v1.py'],'receipt':'receipts/acceptance-v1.json'}],
 'native_original_failure_preserved':'receipts/reader-static-driver.json exit1 ENV_BLOCKED; corrected reader-static-v2-driver and all decisive native receipts exit0. No mathematical refutation inferred.',
 'actual_API_calls':1,'successful_API_replays':0,
 'authorized_tracked_changes_only':[LEDGER,CELL],
 'cell_changed_fields_only':['status','evidence.independent_verification'],
 'no_Git_commit_push_shared_import_site_or_ownership_release':True,
 'all_prior_source_freezes_and_59_entry_portable_package_preserved':True,
 'no_ATLAS_or_broad_foreign_snapshot_export':True})
write(OUT/'completion.original.json',{
 'advance_id':TARGET,'verifier_id':WORKER,'actual_state':'VERIFIED','actual_cell_status':'independently_verified','normal_API_calls':1,'successful_API_replays':0,
 'decision':info(E/'actual-VERIFIED-independent-decision.json'),'full_V_payload':info(OUT/'actual-VERIFIED-evidence.full.json'),'actual_V_append':info(OUT/'actual-VERIFIED-append.original.jsonl'),
 'original_PL_payload':info(E/'actual-PROVED_LOCAL-evidence.full.json'),'original_PL_append':info(E/'actual-PROVED_LOCAL-append.exact.jsonl'),'all20_PL_fields_inline_preserved':True,
 'receipt_exits':check_exits,'four_original_final_gate_exits':{x['gate']:x['exit_code'] for x in a['four_final_gates']},
 'preservation':{'foreign_full_states':post['foreign_full_states'],'discoveries_full_states':post['discovery_full_states'],'discovery_bytes':post['discovery_ledger'],'prior_regular_frontier_files_including_README':post['prior_other_regular_frontier_files_including_README'],'all_other_tracked_files':post['all_other_tracked_files'],'source_package59_unchanged':True,'HEAD_and_both_main_refs_preserved':True,'ledger_prefix_preserved':True,'sole_normal_append':True,'only_preseeded_two_C_fields_changed':True},
 'HOLD':json.loads((OUT/'decision.original.json').read_bytes())['HOLD'],
 'failure_interpretation':'Both verifier precheck failures are preserved implementation mistakes; corrected versions passed before the sole normal API. No mathematical failure or native archive mutation occurred.'})
entries=[]
for p in sorted(OUT.rglob('*')):
 if not p.is_file() or p.name in {'portable-manifest.json','portable-seal.json'} and p.parent==OUT:continue
 i=info(p);entries.append({'source':sources.get(rel(p),rel(p)),'destination':rel(p),'bytes':i['bytes'],'sha256':i['sha256']})
assert len({x['destination'] for x in entries})==len(entries)
manifest={'schema_version':1,'verifier_id':WORKER,'advance_id':TARGET,'exact_candidate':CANDIDATE,'held_metadata_HEAD':HEAD,'listed_original_files':len(entries),'total_files_including_manifest_and_seal':len(entries)+2,'manifest_destination':rel(OUT/'portable-manifest.json'),'seal_destination':rel(OUT/'portable-seal.json'),'self_exclusion':'Manifest and final seal are excluded from entries to prevent circular self-hashing; seal binds exact manifest bytes, and seal raw hash is returned externally.','entries':entries}
write(OUT/'portable-manifest.json',manifest)
for x in entries:
 b=(ROOT/x['destination']).read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256']
seal={'schema_version':1,'verifier_id':WORKER,'advance_id':TARGET,'actual_state':'VERIFIED','actual_cell_status':'independently_verified','normal_API_calls':1,'normal_API_receipt':info(OUT/'receipts/normal-api.json'),'manifest':info(OUT/'portable-manifest.json'),'listed_original_files':len(entries),'total_files_including_manifest_and_seal':len(entries)+2,'decision':info(E/'actual-VERIFIED-independent-decision.json'),'full_V_payload':info(OUT/'actual-VERIFIED-evidence.full.json'),'actual_V_append':info(OUT/'actual-VERIFIED-append.original.jsonl'),'pre_frontier_receipt':info(OUT/'receipts/pre-frontier.json'),'post_frontier_receipt':info(OUT/'receipts/post-frontier.json'),'pre_preservation_receipt':info(OUT/'receipts/pre-preservation-v2.json'),'post_preservation_receipt':info(OUT/'receipts/post-preservation.json'),'native_credit_only':CANDIDATE,'all_four_original_final_gates_exit0':True,'all_corrected_own_acceptance_and_pre_post_checks_exit0':True,'two_failed_prechecks_retained':True,'all_foreign_full_states_discovery_bytes_frontier_files_other_tracked_files_and_prior_source_package_unchanged':True,'no_ownership_release_or_integration_or_delivery_or_purification_credit':True}
write(OUT/'portable-seal.json',seal)
assert len([p for p in OUT.rglob('*') if p.is_file()])==len(entries)+2
for p in [OUT/'portable-manifest.json',OUT/'portable-seal.json',E/'actual-VERIFIED-independent-decision.json',OUT/'actual-VERIFIED-evidence.full.json',OUT/'actual-VERIFIED-append.original.jsonl']:
 print(json.dumps(info(p)))
print(json.dumps({'listed_original_files':len(entries),'total_files_including_manifest_and_seal':len(entries)+2,'actual_state':'VERIFIED','actual_cell_status':'independently_verified','normal_API_calls':1,'check_exits':check_exits}))
