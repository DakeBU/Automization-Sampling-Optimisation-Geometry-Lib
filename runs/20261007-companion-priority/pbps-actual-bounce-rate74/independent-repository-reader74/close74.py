import datetime,json,os,sys
from pathlib import Path
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).parent))
from review74 import O,R,DIS,SCI,ACTOR,load,pin,check,save,sha,can
assert not (O/'lease.final.json').exists()
inputs=load(O/'inputs.manifest.json');assert inputs['inputs']==load(DIS)['inputs']
for z in inputs['inputs']:check(z)
checked=load(O/'checks.json');assert checked['result']['status']=='PASS_SCOPED_CURRENT_READER_FINITE_CHECKS'
image_comments={
 'render-unit0-statement.png':'Viewed attribution, complete ten-clause statement, all assumptions and reflection/rate/weighted-SUM energy/cap formulas. Plain complete-statement notation remains dense.',
 'render-unit0-proof-1.png':'Viewed internal r=0 gradient-Lipschitz producer, formula and initially closed corresponding Lean; subsequent numbered steps visible.',
 'render-unit0-proof-2.png':'Viewed zero-safe orthogonal-complement reflection, involution/norm/pairing formula and closed Lean; zero branch explicit.',
 'render-unit0-proof-3.png':'Viewed Borel S versus continuous rate distinction, correct sqrt(eta) formula and closed Lean; no S-continuity claim.',
 'render-unit0-proof-4.png':'Viewed actual bounce/energy/flipped-rate/difference identities and closed Lean; positive-part sign cases explained.',
 'render-unit0-proof-5.png':'Viewed nonnegative weighted energy and zero-energy-safe collection of laws, with closed Lean and same-layer setup.',
 'render-unit0-proof-6.png':'Viewed both squared bounds and square-root radii, no division by energy, closed Lean and the following cap formula.',
 'render-unit0-proof-7.png':'Viewed exact cap scalar factors, closed Lean statement/proof and assumption/source boundary table; stochastic claims withheld.',
 'render-branch-actual-consumer.png':'Viewed exact ActualBounceRate declaration focus, module prerequisite/direct relations and truth legend. Graph labels remain dense.',
 'copy-unit0-copy-and-download.png':'Independently viewed copy/download capture, complete statement and displayed formulas. Same RAW image as statement capture does not remove this distinct view call.'
}
images=[dict(input=z,independently_viewed_with='tools.view_image',observation=image_comments[Path(z['path']).name]) for z in inputs['inputs'] if z['path'].endswith('.png')]
assert len(images)==10 and set(image_comments)=={Path(z['input']['path']).name for z in images}
debts=['Dense graph labels remain a scoped reader debt; no whole-graph usability or certified theorem-implication claim.','Complete-statement plain notation remains dense; full Chapter1.3 Exposition Seal and broader reader delivery are open.','Three isolated page clipboard callbacks do not test the physical OS clipboard.','Full72 Python/browser regressions are reused with same paths and mtime continuity; historical executable RAW hashes were not recorded, so historical byte identity is not claimed.','Postmerge purification, main integration and live deployment remain open.','Random clocks/path recursion/nonexplosion/invariance/terminal kernels/convergence/cost/actual-input composition/full-paper/Goal claims remain withheld.']
decision=dict(status='ACCEPTED_SCOPED_AGGREGATE_CURRENT_READER74_WITH_EXPOSITION_DEBT',accepted_scoped_aggregate=True,blockers=[],independent_of_formalizer_stabilizer=True,actor=ACTOR,checked_science_commit=SCI,new_VERIFIED_transition=False,new_independent_mathematics_certification=False,new_independent_source_certification=False,formula_BODY_steps=7,independently_viewed_PNGs=10,independently_viewed_PNG_records=images,Registry=523,publication_units=244,copy_callbacks=3,RAW_downloads=3,download_UTF8_RAW_bytes=10565,download_record_character_count=9729,initially_closed_details=13,original_six_callers_retained=True,unused_standing_callers_disclosed=['hα','hαβ','hβη'],all_dispatch_inputs_checked=181,current_target_browser_fresh=True,full_regressions_fresh_for74=False,reader_debts=debts,Goal_complete=False,PURIFIED=False,full_Exposition_Seal=False,main=False,live=False,whole_paper=False,source_math_blind_exact_native_closures_reused_unchanged=True,source_binding_context_matches_current=True,whole_RAW_whitespace_green_claim=False,checker_negative_preserved=dict(PID=45872,EXIT=1,diagnosis=pin(O/'checker-diagnosis.json')),corrected_finite_check=dict(PID=36172,EXIT=0),canonical_shared_Git_ledger_writes=False)
save('decision.json',decision)
review=(O/'named.scoped-aggregate-current-reader74.md').read_text(encoding='utf8')
payload=dict(name='Complete named independent scoped aggregate/current reader74 RAW payload',actor=ACTOR,checked_science_commit=SCI,decision=decision,inputs=inputs,full_named_review_UTF8=review,finite_check_results_and_actual_terminal_receipts=checked,ten_independently_viewed_PNGs=images,new_VERIFIED_transition=False,new_independent_mathematics_certification=False)
save('complete.named.RAW.payload74.json',payload)
run=dict(name='Independent scoped aggregate/current reader74',actor=ACTOR,checked_science_commit=SCI,status=decision['status'],decision=pin(O/'decision.json'),inputs_manifest=pin(O/'inputs.manifest.json'),complete_named_RAW_payload=pin(O/'complete.named.RAW.payload74.json'),named_review=pin(O/'named.scoped-aggregate-current-reader74.md'),finite_checks=pin(O/'checks.json'),actual_writer_PID=os.getpid(),new_VERIFIED_transition=False,new_independent_mathematics_certification=False,wholelogical_recipe='sha256 sorted compact JSON ensure_ascii=False allow_nan=False UTF8; remove ONLY top-level run_sha256')
run['run_sha256']=sha(can(run));save('run.json',run)
files=[pin(p) for p in sorted(O.rglob('*')) if p.is_file() and p.name!='lease.final.json']
lease=dict(status='CLOSED_LAST',actor=ACTOR,postclose_owned_writes_forbidden=True,final_owned_write=True,files=files,file_count_including_lease=len(files)+1,closure_logical_sha256=sha(can(files)),run_sha256=run['run_sha256'],writer_PID=os.getpid(),writer_terminal_EXIT_expected=0,closed_UTC=datetime.datetime.now(datetime.timezone.utc).isoformat())
save('lease.final.json',lease)
print(json.dumps(dict(status='CLOSED_LAST',actual_writer_PID=os.getpid(),writer_terminal_EXIT_expected=0,owned_files=len(files)+1,inputs=181,viewed_PNGs=10,run_sha256=run['run_sha256'],lease=pin(O/'lease.final.json'),complete_named_RAW_payload=run['complete_named_RAW_payload'],closure_logical_sha256=lease['closure_logical_sha256']),ensure_ascii=False),flush=True)
