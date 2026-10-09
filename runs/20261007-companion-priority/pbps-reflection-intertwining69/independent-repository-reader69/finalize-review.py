import base64,datetime,hashlib,json,os,pathlib,sys
sys.dont_write_bytecode=True
from evidence_bytes import pack
out=pathlib.Path(__file__).resolve().parent
load=lambda n:json.loads((out/n).read_text(encoding='utf-8'))
sha=lambda b:hashlib.sha256(b).hexdigest()
def save(n,d):
    (out/n).write_text(json.dumps(d,sort_keys=True,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
canonical=lambda d:json.dumps(d,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8')
neg=load('negative-observations.json')
neg['console_negative'].append(dict(kind='Windows-console-GBK-encoding',tool_chunk='c0cf01',actual_exit=1,
    actual_child_pid=None,actual_child_pid_note='Exploratory exec did not print its child PID; no invented PID.',
    effect='Printing the mandatory log tail raised UnicodeEncodeError on U+2139 after useful registry output.',
    resolution='Owned inspect-aggregate-context.py explicitly configures UTF8 and ran foreground actual PID50976 EXIT0; full successful stdout/stderr/receipt preserved.'))
save('negative-observations.json',neg)
save('negative-console-encoding.failure.json',dict(tool_chunk='c0cf01',actual_exit=1,actual_child_pid=None,
    traceback="Traceback (most recent call last):\n  File \"<string>\", line 1, in <module>\nUnicodeEncodeError: 'gbk' codec can't encode character '\\u2139' in position 190: illegal multibyte sequence\n",
    no_canonical_effect=True,no_negative_counted_as_PASS=True))
viewed=['current.103.render-unit0-statement.png','current.091.render-unit0-proof-1.png','current.093.render-unit0-proof-2.png',
    'current.095.render-unit0-proof-3.png','current.097.render-unit0-proof-4.png','current.099.render-unit0-proof-5.png',
    'current.101.render-unit0-proof-6.png','current.087.render-branch-actual-consumer.png']
visual=dict(schema='repository-reader69-independent-eight-capture-inspection-v1',
    actual_view_image_calls_completed=True,viewed_capture_count=8,
    images=[dict(name=n,RAW_bytes=(out/n).stat().st_size,RAW_sha256=sha((out/n).read_bytes()),binary_RAW_only=True) for n in viewed],
    statement='Complete attributed statement is visible and readable; dense plain Unicode and underscore notation remains disclosed reader debt.',
    six_steps='Six formula narratives and adjacent closed Corresponding Lean step folds are legible and consistently ordered. Exact complete code and formulas are independently checked in DOM, not inferred from folded screenshot pixels.',
    branch='The focused compiled69 node, source125 and immediate relationships are visible. Inherited broad graph and long labels are dense; page expressly labels scans incomplete and separates formal topology from conceptual/source truth.',
    private_helper='Complete private literal Prop is verified in the actual DOM and copy callback rather than claimed visible inside a closed screenshot fold.',
    no_claim_about_unviewed_contact_sheets=True,no_physical_device_or_live_claim=True)
save('independent-eight-capture-visual-review.json',visual)
dom=load('current-scoped-DOM-comparison.json');copy=load('actual-copy-download-review.json');aggregate=load('bounded-current-aggregate-review.json')
finalmanifest=load('final-input-manifest.json');assert finalmanifest['count']==132
final_cell_sha=aggregate['final_cell_RAW_sha256']
final_pins=[]
for n in ['current.058.receipt.json','current.061.receipt.json','current.064.receipt.json','current.067.receipt.json','current.070.receipt.json','current.073.receipt.json','current.076.receipt.json']:
    r=load(n);cp=[x for x in r['inputs'] if x['path'].endswith('/frontier-cells/ASTIS-SW-PBPS-actual-reflection-intertwining.json')]
    assert len(cp)==1 and cp[0]['raw_sha256']==final_cell_sha
    final_pins.append(dict(receipt=n,actual_pid=r['actual_foreground_pid'],actual_exit=0,final_cell_RAW_sha256=final_cell_sha))
save('final-admin-and-gate-binding-review.json',dict(schema='repository-reader69-final-admin-binding-v1',
    final_cell_RAW_sha256=final_cell_sha,seven_final_receipts_bind_current_cell=final_pins,
    final_admin_stage_pending_field='The final-admin.json is explicitly a pre-final-graph stage record. Its pending flag is resolved by later final graph45932/graph29128/site21684/publication49560/frontier26068/contributor5960/semantic46812 receipts and final integration.notes.json; no stale stage field is treated as final failure.',
    prior66_freshness_withheld_preserved=True))
reasons={
 'I1':'Exactly one69 registry entry and ExampleCases import; 517 formalizedLocal entries and Tests.Basic guard517.',
 'I2':'Current Lean21072B, lesson and publication equal source211 frozen bytes; accepted native closures verified without mathematical re-review.',
 'M1':'Mandatory actual PID38812 EXIT0,9179/9479 jobs and ASTIS check passed. Same SCI69 Lean; final admin-only cell update is covered by seven later exact-current-cell checks.',
 'R1':'One exact attributed natural statement and full assumption list; public statement/proof initially closed and full module contexts available.',
 'R2':'All six exact formulas and adjacent literal BODY ranges134-441 match frozen payload,308 contiguous lines; every code fold initially closed.',
 'R3':'Complete6554 UTF8-byte literal Prop helper resolves by full identity inside public proof fold; natural statement says representation, not provider. Generic supporting-proof label remains a disclosed nonblocking wording limitation.',
 'R4':'Three actual isolated page clipboard callbacks copied exactly the immediate parent panel code; parent proof copy does not select nested helper.',
 'R5':'Three actual HTTP200 source fetches independently UTF8-encode to exact21072-byte RAW7bbaae... module. Capture bytes19568 is JS string length; physical save dialog/download filesystem not tested.',
 'R6':'All eight pinned actual PNGs directly viewed; formula text and closed adjacent folds legible. Statement notation and graph density remain bounded disclosed debt.',
 'G1':'Final graph45932,graph-check29128 and site21684 EXIT0; affected exact branch, imports/ownership/scanner/source correspondence retain their typed meanings. No sharp-energy68 edge or completed future B21/B4 implication.',
 'A1':'HEAD and independent VERIFIED event bind SCI69 commit2d286c...; final cell/admin preserve source parents and open frontier; final graph/publication input binding matches integration notes.',
 'N1':'WrongCLI PID47776/46100 EXIT2 receipts/stdout/stderr copied and typed; corrected commands distinct. Own rg-path/GBK-console negatives recorded and never counted PASS.',
 'B1':'Only local repository/scoped-reader current-state acceptance. Full Exposition/PURIFIED/main/live/B21/B4/wholepaper/Goal are not obtained.'}
checks=[dict(id=x['id'],classification=x['class'],expected=x['expected'],decision='PASS_BOUNDED',reason=reasons[x['id']]) for x in load('scoped-checklist.before-final-packet.json')['checks']]
coverage=dict(schema='repository-reader69-finite-coverage-v1',check_count=13,checks=checks,
    final_root_inputs=108,complete_named_inputs=132,actual_viewed_captures=8,exact_code_panels=3,actual_copy_callbacks=3,
    actual_HTTP200_RAW_roundtrip_downloads=3,BODY_steps=6,BODY_lines=308,
    reused_source419_items_7_regions_22_nodes_49_edges=True,reused_module446_line_source_review=True,
    no_new_source_mathematics_review=True,blocking_findings=0,required_repairs=0)
save('finite-repository-reader-coverage.json',coverage)
boundary=aggregate['remaining_truth_boundary']+[
    'This independent decision does not certify an elaborated proof-dependency graph, physical OS clipboard, physical save dialog, remote CI, main merge or live deployment.',
    'No70 implementation/proof/admission is supplied by this69 reader decision.']
decision=dict(schema='astis-repository-scoped-reader-review-decision-v1',owner='/root/independent_primary69',
    verdict='ACCEPT_LOCAL_REPOSITORY_AND_SCOPED_READER69',ready_to_close=True,checked_science_commit=aggregate['head'],
    final_root_packet_RAW_sha256='8bd48315996481ca610699deecaf5add6ccee521fbd003923b466785e5aedd67',
    expectation_RAW_sha256='ce3ed2de808455a64bf5c995c579a937761f7d7d606da2409fa0d573ab68be24',
    final_cell_RAW_sha256=final_cell_sha,final_graph_RAW_sha256=aggregate['final_graph_RAW_sha256'],
    current_publication_inputs_sha256=aggregate['final_publication_inputs_sha256'],
    source_review_run_reused='f1e5024fe6afdaedae4ac5f9b2dfc48bc86e09da51b490212c392bbc9bf2ce90',
    independently_VERIFIED_science_reused=True,checks=checks,blocking_findings=[],required_repairs=[],
    nonblocking_observations=[copy['nonblocking_metadata_observation'],
        'Generic helper label says Supporting proof called by the result above. The full private Prop is a proposition representation; complete natural statement expressly says it supplies no provider/premise.',
        'Name-scanned graph signals are incomplete; one incidental LogConcaveOn.prod match is not certified as a proof dependency. ReflectionL2 parent remains explicit in the frontier cell and actual module.',
        'Dense statement notation and inherited graph labels remain disclosed scoped reader debt.'],
    remaining_truth_boundary=boundary,
    scope=dict(repository_aggregate=True,scoped_reader=True,current_affected_graph=True,new_mathematical_source_verdict=False,
        full_Exposition_Seal=False,PURIFIED=False,main=False,live=False,wholepaper=False,Goal_complete=False),
    canonical_Git_ledger_Goal_edits=False)
save('repository-reader69.decision.json',decision)
run=dict(schema='repository-reader69-complete-RAW-review-run-v1',owner='/root/independent_primary69',
    actual_finalizer_pid=os.getpid(),created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    expectation=load('reader-aggregate-expectations.before-final-packet.json'),
    exact_current_packet=load('final-reader-repository-packet69.RAW.json'),finite_input_manifest=finalmanifest,
    reused_native_closures=load('reused-native-closure-integrity.json'),DOM=dom,copy_download=copy,
    aggregate=aggregate,final_admin_binding=load('final-admin-and-gate-binding-review.json'),visual=visual,
    coverage=coverage,decision=decision,negative_evidence=neg,
    no_new_proof_search_or_math_source_re_review=True,canonical_Git_ledger_Goal_edits=False)
run['run_sha256']=sha(canonical(run));save('review-run.json',run)
entries=finalmanifest['prior_frozen_inputs']+finalmanifest['final_current_inputs']+finalmanifest['extra_named_negative_inputs']
assert len(entries)==132
payload=dict(schema='repository-reader69-complete-exact-RAW-LF-input-payload-v1',complete_named_input_count=len(entries),
    text_LF_recipe='only CRLF-to-LF; lone CR preserved',binary_policy='RAW only; no LF rewrite',
    inputs=[dict(attribution=e,payload=pack(out/e['name'],e['name'],binary=e.get('binary',False))) for e in entries])
save('RAW-input-payload.json',payload)
save('complete-named-review-decision-input-payload.json',dict(schema='repository-reader69-complete-named-review-decision-input-v1',
    whole_logical_run_sha256=run['run_sha256'],whole_logical_deletes_ONLY_top_level_run_sha256=True,
    named=[pack(out/n,n) for n in ['review-run.json','repository-reader69.decision.json','RAW-input-payload.json']]))
save('bounded-synthesis.repository-reader69.json',dict(verdict=decision['verdict'],checked_science_commit=aggregate['head'],
    final_packet_RAW_sha256=decision['final_root_packet_RAW_sha256'],whole_logical_run_sha256=run['run_sha256'],
    final_root_inputs=108,complete_named_inputs=132,finite_checks=13,blocking_findings=0,required_repairs=0,
    root_jobs=9179,test_jobs=9479,registry_count=517,publication_units=238,successful_gates=17,
    BODY_steps=6,BODY_lines=308,actual_visual_captures=8,copy_callbacks=3,RAW_roundtrip_downloads=3,
    remaining_truth_boundary=boundary,no_canonical_Git_ledger_Goal_edits=True))
print(json.dumps(dict(actual_finalizer_pid=os.getpid(),verdict=decision['verdict'],whole_logical_run_sha256=run['run_sha256'],
    complete_named_inputs=132,checks=13,blocking_findings=0),sort_keys=True))
