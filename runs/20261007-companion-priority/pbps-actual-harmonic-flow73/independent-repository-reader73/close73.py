from pathlib import Path
import datetime, difflib, json, os, re, subprocess, sys
sys.path.insert(0, str(Path(__file__).parent))
import review73 as v

assert not (v.OWN/'lease.final.json').exists() and v.head()==v.COMMIT
manifest=v.load(v.OWN/'inputs.manifest.json'); inspection=v.load(v.OWN/'inspection.json')
v.check(manifest['dispatch'])
for z in manifest['inputs']: v.check(z)
assert inspection['actual_reader_PID']==32816
registry=(v.BASE/'AutoSamplingTheory/TechnicalLemmas/Registry.lean').read_text(encoding='utf8')
assert len(re.findall(r'status\s*:=\s*LemmaMemoryStatus\.formalizedLocal',registry))==522
assert 'formalizedTechnicalLemmaCount = 522' in (v.BASE/'Tests/Basic.lean').read_text(encoding='utf8')
science_identity=[]
core=['AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHarmonicFlow.lean','website/content/declaration_lessons/pbps-actual-harmonic-flow.json','website/content/publications/pbps-actual-harmonic-flow.json','research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSActualHarmonicFlow.json']
for n in core:
    raw=(v.BASE/n).read_bytes(); committed=subprocess.check_output(['git','show',v.COMMIT+':'+n],cwd=v.BASE)
    assert raw==committed,n
    science_identity.append(v.pin(v.BASE/n))
failed=v.R/'integration73/record-final-import-diagnosis/failed-helper.exactraw.py'
repaired=v.BASE/'.astis/pbps-harmonic73/record-integration73.py'
a=failed.read_text(encoding='utf8'); b=repaired.read_text(encoding='utf8')
helper_diff=list(difflib.unified_diff(a.splitlines(),b.splitlines(),fromfile='frozen_failed_helper',tofile='current_task_local_repaired_helper',lineterm=''))
assert len(helper_diff)<30
supplement=dict(actual_foreground_PID=os.getpid(),checked_science_commit=v.COMMIT,Registry=522,Tests_baseline=522,core_exact_RAW_equal_git_show=science_identity,current_graph_publication_inputs_equal_final_notes=v.load(v.BASE/'_site/data/underlying-lean-graph.json')['publication_inputs_sha256']==v.load(v.R/'integration.notes.json')['publication_inputs_sha256'],recorder_helper_finite_extra_pin=v.pin(repaired),recorder_helper_diff=helper_diff,no_canonical_or_site_mutation_by_this_review=True)
assert supplement['current_graph_publication_inputs_equal_final_notes']
v.write(v.OWN/'supplemental-inspection.json',supplement)
visual_notes={
 'render-unit0-statement.png':'Complete attributed statement, original assumptions, exact actual-arc/group/ODE/weighted-sum/half-turn displays visible. Dense prose contains plain notation; no stochastic Proposition3.1 credit.',
 'render-unit0-proof-1.png':'All six sequential formula/prose steps visible with closed adjacent Lean steps; the continuity scale and group formulas are legible.',
 'render-unit0-proof-2.png':'Group, derivative, nonnegative energy, cancellation and endpoint steps visible; statement/proof disclosures closed.',
 'render-unit0-proof-3.png':'Both ODE signs/scales visible, followed by energy and endpoint steps; assumption comparison discloses retained standing callers.',
 'render-unit0-proof-4.png':'Zero-energy-inclusive nonnegativity and exact conserved-sum formula visible; full Lean statement/proof remain folded.',
 'render-unit0-proof-5.png':'Mixed-term cancellation, factor one half, endpoint, and unresolved stochastic/paper boundary visible.',
 'render-unit0-proof-6.png':'Half-turn step, initially folded verification panels, source-versus-formal assumptions, encoder-denoiser result and open boundary visible.',
 'render-branch-actual-consumer.png':'Actual declaration selected with COMPILED status. Caption separates imports/ownership, incomplete reference scans and conceptual overlays; dense wrapped labels remain debt.',
 'copy-unit0-copy-and-download.png':'Current source-attributed statement view reproduced during isolated copy/download probe; display remains readable with the same bounded notation debt.'
}
visual=dict(actor=v.ACTOR,independent_of_root_visual_review=True,view_method='All nine exact pinned PNGs independently viewed using tools.view_image; no new screenshot or browser regression run.',image_count=9,observations=[dict(pin=z,observation=visual_notes[Path(z['path']).name]) for z in inspection['capture_pins']])
v.write(v.OWN/'independent-visual-review.json',visual)
diagnosis=dict(failed_foreground_PID=34600,failed_EXIT=1,failure_class='REVIEWER_CHECKER_EXPECTED_SPAN_MISMATCH',failure='First checker expected the theorem BODY panel to stop before namespace closures. Actual exact panel includes end/end and #print axioms trailer.',repair='Compare the full source suffix beginning at the theorem, omitting only the final display newline, as the existing renderer does.',retry_foreground_PID=32816,retry_EXIT=0,canonical_math_source_or_site_edits=False,failed_script=v.pin(v.OWN/'review73.initial-failed.exactraw.py'),negative_receipt=v.pin(v.OWN/'inspect.receipt.json'),retry_receipt=v.pin(v.OWN/'inspect-retry.receipt.json'))
v.write(v.OWN/'reviewer-checker-diagnosis.json',diagnosis)
debts=[
 'Dense graph labels and plain notation in the complete-statement/assumption prose remain bounded reader debt; the separate display formulas are legible.',
 'Full Chapter1.3/whole-paper Exposition Seal and postmerge PURIFIED admission remain open. This scoped reader acceptance supplies neither.',
 'Three isolated page clipboard callbacks were observed, not the physical OS clipboard. Captures and downloads are local; no live-site or physical-device acceptance.',
 'Prior complete Python/browser regressions are reused72, not fresh73. Same executable paths and mtime continuity are recorded; historical executable RAW hashes were absent, so historical byte identity is unclaimed.',
 'The original generated-scope assertion failed before writes (32932/1). The offending path was not captured and its cause remains unestablished; diagnostic26180/0 restored100 previously clean generated paths and preserved443 unused new cards.',
 'Actual stochastic bounce/rate/clock recursion, PDMP construction/nonexplosion/invariance, actual H_y/terminal kernel, same-J lift, K/r_rho/B27/B28, PBPS/SPHMC main results, errors/caps, expected-query costs and actual-input composition remain open.',
 'No remote CI, merge-to-main, live deployment, whole-paper or Goal-completion admission is supplied.'
]
decision=dict(status='ACCEPTED_INDEPENDENT_SCOPED_AGGREGATE_READER73_WITH_EXPOSITION_DEBT',actor=v.ACTOR,accepted_scoped_aggregate=True,independent_of_formalizer_stabilizer=True,checked_science_commit=v.COMMIT,new_VERIFIED_transition=False,new_independent_mathematics_certification=False,blockers=[],reader_debts=debts,Registry=522,publication_units=243,root_jobs=9184,test_jobs=9484,formula_BODY_steps=6,independently_viewed_PNGs=9,copy_callbacks=3,RAW_downloads=3,Goal_complete=False,PURIFIED=False,full_Exposition_Seal=False,main=False,live=False,whole_paper=False,native_math_source_blind_exact_reviews_reused=True,current_scoped_browser_evidence_reused_from_root_but_PNGs_independently_viewed=True,original_callers_preserved=['hα','hαβ','hV','hH','hη','hβη'],unused_standing_conditions_disclosed=['hα','hαβ','hH','hβη'],current_cell_diff=inspection['current_cell_admin_diff'],no_canonical_ledger_or_Git_writes=True)
review='''Independent repository and reader review73 — scoped acceptance with exposition debt

I accept the frozen local aggregate/current reader delivery attached to exact science child d7e00a7c0e8b0f37fcc2dbe99f6b646d3a7b1de6. I am /root/header_math72, distinct from the formalizer/stabilizer. This review verifies current delivery and bounded aggregate evidence; it reuses admitted independent mathematics73, source73, blind73 and nonowner exact-commit verification. It creates no mathematical certification or VERIFIED transition.

All 134 dispatch entries match their exact RAW size/SHA256 and CRLF-byte-pairs-to-LF-only SHA256. The dispatch itself is separately pinned. The canonical178-line module, complete lesson, publication and semantic audit are RAW-identical to git show of the named science commit. Current repository aggregate metadata is reviewed as the frozen working tree, not misrepresented as already committed to that child. The final cell differs from its preserved pre-admin snapshot only at /blocked/reason, /evidence/serialized_shared_gate and /graph_contribution/visual_review. No theorem or assumption changed.

The mandatory astis.py check PID4160 terminated EXIT0, including successful root9184 and Tests9484 builds. The actual Registry has522 formalizedLocal entries and the Tests count baseline is522. Final publication validation records243 source items. Final graph, site, publication, frontier, contributor and semantic receipts are terminal EXIT0 and bound to this science commit. The build gate is reused rather than rerun. The prior full Python/browser tests are historical72 evidence under explicit runtime qualification; no historical executable RAW hashes were recorded, so no historical-byte identity is asserted. Current scoped browser render/copy/download evidence is fresh73.

The reader preserves all six callers hα,hαβ,hV,hH,hη,hβη. It correctly discloses that hα,hαβ,hH,hβη are retained standing conditions, whereas C² supplies gradient continuity and η>0 supplies the positive square-root scale. Rank zero, αη=1 and zero energy are explicitly legal. The full private literal defines actual c,Φ,H and all nine clauses beside the public theorem; it is a specification, never a proof provider. Both exact ODE signs/scales, SUM-weighted energy with factor1/2, group/both inverse and π endpoint match the admitted theorem. This is a preservation check, not a fresh mathematics/source verdict.

All six lesson BODY spans equal their exact contiguous canonical lines and declared hashes:98–110,111–127,128–145,146–148,149–165,166–173. Each has explanatory prose and its formula. The current article has12 initially closed details. Full statement, complete theorem proof (including its namespace/axiom-print source trailer), the private literal helper, and six BODY snippets are present exactly in the article. Three isolated page clipboard callbacks return exact statement/proof/helper text. All three HTTP200 download texts encode to the identical8519-byte RAW module. The browser record's field bytes=7910 is JavaScript string length, not UTF8 byte count; its exact text reconstruction, rather than that label, establishes RAW equality. Physical OS clipboard behavior was not tested.

I independently viewed all nine pinned PNGs: statement, six proof-step views, affected Lean branch and copy/download view. Formulas, prose, initially folded Lean disclosures and open stochastic boundary are visible. The branch selects the actual compiled declaration. Its four finite edges are module declares, gradient source reference(scanner), Lean target under audit, and source correspondence—not a Lean dependency. The visible caption separates import/ownership from incomplete reference scans and conceptual overlays. Dense labels and plain notation remain bounded reader debt, not a full Exposition Seal.

Negative evidence remains explicit. Narrow-generated-scope32932/EXIT1 failed at its prewrite assertion; no offending path was captured and the cause remains unestablished. Diagnostic26180/EXIT0 reports100 previously clean generated paths restored and443 unused new cards saved. Final-recorder28464/EXIT1 lacked the tools import path; task-local repair19736/EXIT0 added that import path, reusing passed gates. Its failed helper and diagnosis are retained. My own first checker34600/EXIT1 expected the proof panel to stop before namespace closures; exact comparison showed the existing panel includes the source trailer. Corrected checker32816/EXIT0 passed. This did not require page/source/canonical edits.

This acceptance leaves Exposition/PURIFIED, remoteCI/main/live, full-paper and Goal admissions open. Actual bounce/rate/clock recursion, stochastic PDMP/nonexplosion/invariance, actual H_y and terminal law, same-J lift, K/r_rho/B27/B28, main results, implementation errors/caps, expected costs and actual-input composition receive no credit here. No canonical, ledger, Git or shared-site file was written by this reviewer. Large immutable logs, graph JSON and PNGs stay at their finite pinned paths; no recursive history was copied.
'''
(v.OWN/'named-review.md').write_text(review,encoding='utf8',newline='\n')
v.write(v.OWN/'decision.json',decision)
named_RAW=[dict(pin=v.pin(v.BASE/n),UTF8_RAW=(v.BASE/n).read_text(encoding='utf8')) for n in core[:3]]
payload=dict(schema_version=1,review_name='Independent scoped aggregate and current reader review73',decision=decision,inputs=manifest,named_review_UTF8=review,inspection=inspection,supplemental_inspection=supplement,independent_visual_review=visual,reviewer_negative_evidence=diagnosis,complete_named_core_RAW_payload=named_RAW,large_finite_input_policy='All134 exact pins retained; large graph/log/binary inputs remain at pinned native paths without recursive copying.')
v.write(v.OWN/'complete-named-review-decision-input-payload.json',payload)
run=dict(schema_version=1,actor=v.ACTOR,status='CLOSED_SCOPED_AGGREGATE_CURRENT_READER73',checked_science_commit=v.COMMIT,decision=v.pin(v.OWN/'decision.json'),inputs_manifest=v.pin(v.OWN/'inputs.manifest.json'),complete_named_RAW_payload=v.pin(v.OWN/'complete-named-review-decision-input-payload.json'),named_review=v.pin(v.OWN/'named-review.md'),inspection=v.pin(v.OWN/'inspection.json'),supplemental_inspection=v.pin(v.OWN/'supplemental-inspection.json'),independent_visual_review=v.pin(v.OWN/'independent-visual-review.json'),terminal_receipts=[v.pin(v.OWN/'inspect.receipt.json'),v.pin(v.OWN/'inspect-retry.receipt.json')],actual_close_writer_PID=os.getpid(),whole_logical_recipe='Delete ONLY top-level run_sha256; JSON ensure_ascii=False,sort_keys=True,separators=(comma,colon),allow_nan=False; UTF8; SHA256.',LF_recipe='CRLF byte pairs -> LF only; preserve bare CR and all other bytes.',new_math_or_VERIFIED=False)
run['run_sha256']=v.sha(v.can(run)); v.write(v.OWN/'run.json',run)
rows=[v.pin(p) for p in sorted(v.OWN.rglob('*')) if p.is_file()]
assert not any(Path(z['path']).name=='lease.final.json' for z in rows)
lease=dict(schema_version=1,status='CLOSED_LAST',actor=v.ACTOR,writer_PID=os.getpid(),writer_terminal_EXIT_expected=0,writer_terminal_observation='Actual foreground EXIT is recorded by caller tool; independent postclose checks writer terminated.',files=rows,file_count_including_lease=len(rows)+1,closure_logical_sha256=v.sha(v.can(rows)),run_sha256=run['run_sha256'],postclose_owned_writes_forbidden=True,final_owned_write=True,closed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
v.write(v.OWN/'lease.final.json',lease)
print(json.dumps(dict(status='CLOSED_LAST',actual_writer_PID=os.getpid(),owned_files=len(rows)+1,run_sha256=run['run_sha256'],lease=v.pin(v.OWN/'lease.final.json'),complete_named_RAW_payload=run['complete_named_RAW_payload']),ensure_ascii=False))
