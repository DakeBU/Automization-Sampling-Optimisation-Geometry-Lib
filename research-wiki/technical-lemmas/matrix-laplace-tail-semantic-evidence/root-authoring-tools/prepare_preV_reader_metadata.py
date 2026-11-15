from pathlib import Path
import json,hashlib,subprocess
r=Path.cwd();w=r/'.astis/huanjian-gc-matrix-laplace-20261114'
e=r/'research-wiki/technical-lemmas/matrix-laplace-tail-semantic-evidence'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p):
    p=Path(p);return {'file':str(p.relative_to(r)),'bytes':p.stat().st_size,'sha256':sha(p)}
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def copy_exact(src,dst):
    assert src.is_file();dst.parent.mkdir(parents=True,exist_ok=True)
    if dst.exists():assert dst.read_bytes()==src.read_bytes()
    else:dst.write_bytes(src.read_bytes())
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()=='3fdf32b93a1fcfc9740cec4f1e3460fd201e538c'
pl=e/'PROVED_LOCAL-evidence.full.json';assert sha(pl)=='da479ae33a80a68835bbb517390a8532760df06054872873c767a5cb65cb198a'
runtime=e/'reader-originals/laplace_native_61e4/v3'
sup=e/'reader-originals/laplace_native_61e4/parent-supplement-v2'
review=e/'reader-review/laplace_fresh_source_8d2a'
assert sha(runtime/'selected-presentation-originals.actual-v3.356.v1.tar.gz')=='6ca0ea14775341f2e9146d3175a9f1ac6c9ff3491e62014f6251115fe28f5082'
assert sha(sup/'selected-native-parent-supplement-originals36.v1.tar.gz')=='a0f2086928a81a4a9a6533b68f425588317ba4cf488619a28b7fc27b49392b06'
finalreview=review/'supplement-v2/reader-visual-supplement.review.json'
assert sha(finalreview)=='ab8bcaf035826329ebcc3cf92cf11e301f95f0a18bdbb72e5f90fa0a0b356e9f'
native=json.loads((sup/'native-supplemental-outcome.v1.json').read_text())
assert native['actual_exit_code']==1 and native['actual_false_check_count']==2
assert native['all_v2_contract_checks_passed'] is False
main=w/'latest-main-before-independent-V.20261115.json'
copy_exact(main,e/'latest-main-original-owners.before-independent-V.20261115.json')
clarification=r/'.astis/semantic-neutral-20261114/laplace_native_61e4/native-public-exposure-clarification.v1.json'
assert sha(clarification)=='88126a2704441d3f09892588823eb56f8c15b4100c40583056fa5e38665622d2'
copy_exact(clarification,e/'native-originals/laplace_native_61e4/native-public-exposure-clarification.v1.json')
observed=[]
for base,name,note in [
 (r/'.astis/semantic-neutral-20261114/laplace_native_61e4/reader-runtime-v3/browser-output-v1/candidate','mobile-proof-initial.png','Rendered main formula; initially closed statement/proof and six proof steps; long formula uses local horizontal scrolling.'),
 (r/'.astis/semantic-neutral-20261114/laplace_native_61e4/reader-runtime-v3/browser-output-v1/candidate','desktop-step-5.png','Readable radius/sum mathematical step and adjacent exact Tests source77–164 with copy/download.'),
 (r/'.astis/semantic-neutral-20261114/laplace_native_61e4/reader-runtime-v3/browser-output-v1/candidate','mobile-source-T-anchor.png','Private literal model theorem line44 and complete horizontally scrollable source.'),
 (r/'.astis/semantic-neutral-20261114/laplace_native_61e4/reader-runtime-v3/browser-output-v1/candidate','mobile-graph-detail-reader-and-edges.png','Complete public P identifier wraps in detail; source55 and reader/parent navigation visible.'),
 (r/'.astis/semantic-neutral-20261114/laplace_native_61e4/reader-runtime-v3/browser-output-v1/candidate','desktop-parent-1-actual-UI-zoom-pan.png','Actually viewed original empty SVG region; confirms independent clipping finding, not successful parent visibility.'),
 (r/'.astis/semantic-neutral-20261114/laplace_native_61e4/reader-parent-supplement-v2/output','desktop-Radius-node-after-real-wheel-pointer.png','Complete viewport shows selected Radius node and core label within SVG, with full identifier/source101 in detail.'),
 (r/'.astis/semantic-neutral-20261114/laplace_native_61e4/reader-parent-supplement-v2/output','mobile-Structure-node-after-real-wheel-pointer.png','Complete viewport shows selected Structure node and core label inside SVG; full identifier wraps in detail.')]:
    p=base/name;observed.append({**ref(p),'actually_viewed_by_ROOT':True,'observation':note})
acceptance={'schema':'separate-post-PL-current-reader-acceptance-v1',
 'status':'ACCEPTED_BOUNDED_ISOLATED_READER_WITH_PRESERVED_PARENT_CLIP_CORRECTION',
 'record_role':'ROOT adoption/custody summary of independently frozen source/reader findings; not an original native process receipt and not proof VERIFIED.',
 'independent_reader':'/root/laplace_fresh_source_8d2a',
 'publication_binding_sha256':'159708e68a0601d85a6081464aa654ea80b7b58cbf0fa41ac697a03fcd8e4346',
 'mathematical_commit':'1d1103af694b9663a72b0d610004ed85c7c6b527',
 'new_v4_browser_run':False,'v4_transfer':'Only the207 exact served-byte identities transfer page observations. No new v4 run or source/metadata approval is inferred.',
 'native_original_run':{'archive':ref(runtime/'selected-presentation-originals.actual-v3.356.v1.tar.gz'),
   'original_actor_manifest':ref(runtime/'presentation-selected-originals.manifest.v1.json'),
   'actual_exit_code':0,'raw_script_checks':398,'raw_script_false_checks':0,'actual_PNGs':103,'actual_downloads':20,
   'original_raw_check_limitation':'Font-size-only parent zoom assertion missed two desktop nodes above the SVG clip; the original raw PASS remains unchanged, not adopted as evidence of those node states.'},
 'initial_independent_reader_review':{'freeze':ref(review/'v1/READER_VISUAL_V1_FROZEN.json'),
   'run':ref(review/'v1/reader-visual.review-run.json'),'result':ref(review/'v1/reader-visual.review.json'),
   'archive':ref(review/'v1/selected-reader-visual-originals19.v1.tar.gz'),'actually_viewed_PNGs':62,'verdict':'PARTIAL; sole parent clipping finding open then.'},
 'actual_targeted_supplement':{'archive':ref(sup/'selected-native-parent-supplement-originals36.v1.tar.gz'),
   'actor_manifest':ref(sup/'public-safe-selected-originals.manifest.v1.json'),'native_outcome':ref(sup/'native-supplemental-outcome.v1.json'),
   'actual_exit_code':1,'raw_checks':167,'raw_false_checks':2,'actual_PNGs':24,'original_contract_all_PASS':False,
   'usable_observations':'Four complete desktop/mobile parent viewport PNGs and independently recomputed actual SVG/node/core-label geometry. All four visible fractions1; effective fonts14.367px/13.262px.',
   'preserved_failure':'Crop helper added scroll offsets to viewport clip coordinates: two desktop crops show detail rather than SVG and are excluded as SVG evidence; two mobile crop calls failed, and their subsequent repeated detail/source steps did not execute.',
   'no_unexecuted_actions_claimed':True},
 'independent_corrective_review':{'freeze':ref(review/'supplement-v2/READER_VISUAL_SUPPLEMENT_V2_FROZEN.json'),
   'run':ref(review/'supplement-v2/reader-visual-supplement.review-run.json'),'result':ref(finalreview),
   'archive':ref(review/'supplement-v2/selected-reader-visual-supplement-originals15.v1.tar.gz'),
   'actually_viewed_new_PNGs':10,'finding':'R15-VIS-GRAPH-PARENT-SVG-CLIP',
   'disposition':'CLOSED_BY_ACTUAL_VIEWPORT_EVIDENCE_BOUNDED',
   'composition':'The independent reviewer matched unchanged v1 same-fixture complete mobile source/detail/exact-link/navigation/copy/download observations with the four new complete viewport states. This closes the required isolated reader scope without converting the failed supplemental contract to PASS.',
   'necessary_reader_residual':0},
 'parent_clip_correction_independently_accepted':True,
 'optional_v3':{'execution':False,'reason':'Independent required-scope residual0; Root cancelled the pending optional correct-crop repeat. Prepared files are reference-only; no fabricated process receipt.',
   'original_actor_cancellation_note':ref(sup/'unexecuted-v3-cancellation.reference-only.json')},
 'accepted_features':['desktop1440×1000 and mobile390×844 responsive views','rendered formulas/local horizontal reach','initially closed statement/proof/six-step exact Lean disclosures','six readable mathematical proof steps and adjacent correct P/P/P/T/T/T source folds','all four complete source modules/anchors/final Unicode glyph/horizontal-vertical scroll','actual clipboard and complete-module downloads','source-index/parent-context/bounded graph/detail navigation and exact identifiers'],
 'graph_boundary':'One public P canonical node; private T source module has no public declaration credit. P has no ASTIS theorem parent; actual private T parents are P/Radius/Structure. Formal module structure and reference/curated relationships remain distinguished.',
 'limits':['Default-fit graph labels remain small; long zoomed SVG labels can be ellipsized or leave the mobile viewport. Full identifiers use readable detail.','Responsive viewports are not physical touch devices.','Frozen isolated scaffold TODO/Lean-gate badges are not production or post-VERIFIED status pixels.','No full production site/main/Registry/global graph integration, purification or whole-Goal completion.'],
 'ROOT_limited_visual_observations':observed,
 'historical_PL_evidence':{'unchanged_original24':ref(pl),'historical_reader_pending_snapshot_preserved':True},
 'proof_VERIFIED_by_this_record':False,'ROOT_normal_V_calls':0}
out=e/'post-PL-current-reader-acceptance.v1.json';assert not out.exists();write(out,acceptance)
draft=w/'metadata-drafts/reader-runtime-public-selection/frontier-cell.preV-current-stage.candidate.v1.json'
assert sha(draft)=='febf5e5f519b29290f259aac320ad0a6f23de509c6675b2d9e5e2c83237a94f0'
cell=json.loads(draft.read_text());assert cell['status']=='proved_locally'
cell['evidence']['reader_review']=str(out.relative_to(r))
cell['evidence']['current_reader_acceptance']=ref(out)
cell['evidence']['latest_main_original_owner_observation']=ref(e/'latest-main-original-owners.before-independent-V.20261115.json')
cell['evidence']['current_normal_stage'].update({'advance_state':'PROVED_LOCAL','cell_status':'proved_locally','theorem_PROVED_LOCAL':True,'theorem_VERIFIED':False})
cell['consumer_scope']['first_realistic_consumer']['state']='ACTUAL_PRIVATE_COMPILED; immutable native/current v4 source and bounded isolated reader accepted; one normal PROVED_LOCAL; independent proof V/stabilization pending'
cell['reuse_plan']['new_shared_declarations_status']='ACTUAL_COMPILED_IMMUTABLE1d110; native/source/bounded isolated reader accepted; normalPL1; independent proofV/stabilization pending'
cell['statement_seal']['status']='EXACT_UNCHANGED_P_T; COMPILED_IMMUTABLE1d110; NATIVE_CURRENT_V4_SOURCE_AND_BOUNDED_READER_ACCEPTED; NORMAL_PL1; INDEPENDENT_PROOF_V_PENDING'
cell['source_detail_audit']['fidelity_boundary']=cell['source_detail_audit']['fidelity_boundary'].replace('proof VERIFIED and current reader/browser/visual acceptance remain pending.','proof VERIFIED remains pending; bounded current isolated reader acceptance is separately preserved with the original failed crop observations and independent correction review.')
cell['source_detail_audit']['current_reader_qualification']='Independent v1+targeted-v2 full-viewport evidence closes the bounded isolated reader scope; v2 remains native FAIL and optional v3 was not executed. See post-PL-current-reader-acceptance.v1.json. No physical touch, full graph fit, production/post-status pixel or integration acceptance.'
cell['graph_contribution']['visual_review']=str(out.relative_to(r))+'; independent four viewport correction closes the parent clip gap while preserving raw FAIL and graph/detail limits; no global graph stabilization.'
cell['integration_notes']['current_main_observation_scope']='Actual bounded root observation at origin/main9448; two original stabilizers held. Local private replay0 is not release. Exact observation is preserved separately.'
cell['integration_notes']['reader_graph_delta']='Isolated bounded graph/detail/source navigation accepted on identical served bytes; one public P and private T module with actual P/Radius/Structure parents. Targeted complete-viewport correction plus prior source/navigation observations; raw crop failure preserved. Shared generated graph/production-site integration remains held.'
write(r/'research-wiki/frontier-cells/ASTIS-SHARED-REAL-MATRIX-LAPLACE-TAIL.json',cell)
memory=json.loads((e/'local-cycle-memory.json').read_text())
memory.update({'normal_state':'PROVED_LOCAL','public_progress_commit':'3be3742810b87db7d9d8fac485427e97209c5f41',
 'public_scope':'Actual safe public full local proof/source/native admission; no independent proofV published yet.',
 'current_reader':str(out.relative_to(r)),'next':['Freeze the exact preV carrier and successful bounded gates','Independent non-prover exactly one normal VERIFIED then independent target-cell projection in a separate guarded window','Safe owned public export, independent privacy review and actual push/readback'],
 'normal_PL_calls':1,'ROOT_V_calls':0,'independent_V_calls':0,
 'remaining_reader_scope':'Necessary bounded isolated-reader residual0; native supplementary process stillFAIL, no production acceptance.',
 'latest_main_observed':'9448a8b6692ec17408e99f5aadafcd321d0daedf'})
write(e/'local-cycle-memory.json',memory)
print(json.dumps({'current_reader_acceptance':ref(out),'cell_status':'proved_locally','normal_PL_calls':1,'normal_V_calls':0,'source_and_original24_unchanged':True}))
