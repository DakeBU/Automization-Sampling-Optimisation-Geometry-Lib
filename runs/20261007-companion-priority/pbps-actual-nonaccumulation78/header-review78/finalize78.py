"""Bounded independent prospective header and source-topology decisions only."""
import datetime, difflib, hashlib, json, re, subprocess
from pathlib import Path
ROOT=Path('E:/Samplinglib')
BASE=ROOT/'runs/20261007-companion-priority/pbps-actual-nonaccumulation78'
OUT=BASE/'header-review78'
def sha(b):return hashlib.sha256(b).hexdigest()
def info(p):
    b=Path(p).read_bytes();return {'path':str(p),'RAW_bytes':len(b),'RAW_sha256':sha(b)}
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def save(n,v):(OUT/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
original=BASE/'header78.proposed.lean';passing=OUT/'header78.syntax-rename-only.lean'
assert info(original)['RAW_sha256']=='36196edf4d668c21b8e56d66622ad3e0ee1d9eea2c6e853647335d059c674e17'
assert info(passing)['RAW_sha256']=='2cf3c2926353f1ec421c01236254bc15ba59675941ab0a835cb121bbbc4738a0'
expected=original.read_text(encoding='utf-8').replace('ω','sample').replace('\n#check actual_','\nend\n\n#check actual_')
assert passing.read_text(encoding='utf-8')==expected
receipt=load(OUT/'syntax-rename-typecheck.receipt.json')
assert receipt['exit_code']==0 and receipt['terminal_closed']
assert receipt['input']==info(passing)
diff=''.join(difflib.unified_diff(original.read_text(encoding='utf-8').splitlines(True),passing.read_text(encoding='utf-8').splitlines(True),fromfile='original-prospective-header',tofile='alpha-rename-and-section-end-only'))
(OUT/'passing-syntax-overlay.diff').write_text(diff,encoding='utf-8')
freeze=load(BASE/'source-preread78/source-freeze78.json')
regions=[]
for item in freeze['regions']:
    p=OUT/(item['anchor'].replace('.','_')+'.independent.raw.html')
    assert info(p)['RAW_sha256']==item['raw_sha256']
    regions.append({'anchor':item['anchor'],'independent_exact_subtree':info(p),'matches_extractor_raw':True})
head=subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,check=True,capture_output=True).stdout.decode().strip()
mathlib=subprocess.run(['git','-C',str(ROOT/'.lake/packages/mathlib'),'rev-parse','HEAD'],cwd=ROOT,check=True,capture_output=True).stdout.decode().strip()
assert mathlib=='db584cd6d46c92f209a44c0f1c829460d327499d'
checks=[
 {'slot':'six analytic hypotheses','decision':'accepted','evidence':'Full binder block exactly equals finite parent: hα/hαβ/hV/hH/hη/hβη. Source S1.p1.1/S1.E1/S2.SS2.p1.1. C2 only, full Hessian quadratic-form bounds and beta*eta<=1; no positivity of dimension, energy or cap.'},
 {'slot':'literal definitions','decision':'accepted','evidence':'c/Phi/S/rate/Lambda/tau/next/record/eventTime byte-equal to existing parent private Prop. Canonical P and epsilon are two additional literal definitions, for 11 total. H and C remain internal proof ingredients, not public certificates.'},
 {'slot':'sample/index','decision':'accepted','evidence':'P=infinitePi Exp(1) on real sequences. epsilon(sample)(k)=toNNReal(sample k) equals verified product epsilon(k)(sample) by beta reduction. k=0 feeds E1; record0=(0,z0); range n matches E1..En.'},
 {'slot':'quantifier order','decision':'accepted','evidence':'For every deterministic y/xRef/z0, AE canonical sample, then forall finite t. No uncountable AE intersection over parameters or horizons is assumed. A proof must derive all-horizon escape samplewise on the product full-measure input event.'},
 {'slot':'finite-horizon escape','decision':'accepted','evidence':'Eventually (t:WithTop NNReal)<eventTime_n for each finite t admits both eventual top after stopping and arbitrarily large finite event times on never-stopped paths. It does not demand eventual top, as a target WithTop atTop filter would.'},
 {'slot':'finite index count','decision':'accepted','evidence':'Given escape at t, exists N with every n>=N having T_n>t, so the displayed set is contained in {n|n<N}, hence finite. Index0 is included: this is finite event-index set, not equality with physical bounce-count N_b or an expectation bound.'},
 {'slot':'zero/stopped branches','decision':'accepted','evidence':'C>=0 is internal. If C=0, a positive first threshold forces stop and absorption makes all n>=1 top. Positive cap may also stop; top times exceed every finite horizon. Rank0/zero energy are not excluded. The null zero-threshold samples are not promised divergence.'},
 {'slot':'continuing branch','decision':'accepted','evidence':'For C>0 and never-stopped paths, actual one-step increments imply T_n >= sum(epsilon_k)/C. Verified product supplies divergent real partial sums. Neither C>0 nor nontermination nor a crossing/SLLN witness is a public assumption.'},
 {'slot':'truth boundary','decision':'accepted','evidence':'Only actual source recurrence event-time nonaccumulation and finite bounded-horizon indices. No global physical-time state, path uniqueness/measurability, Markov/invariance/kernel/hypocoercivity/main accuracy/query cost or composition is asserted.'}
]
header_review={'schema_version':1,'reviewer':'/root/exact_verify77','role':'independent prospective header/math reviewer',
 'status':'ACCEPTED_MATHEMATICAL_TARGET_WITH_EXACT_SYNTAX_OVERLAY_ONLY',
 'original_candidate':info(original),'original_typecheck':info(OUT/'typecheck.receipt.json'),
 'original_as_written_elaborates':False,'passing_immutable_candidate':info(passing),'passing_typecheck':info(OUT/'syntax-rename-typecheck.receipt.json'),
 'exact_diff':info(OUT/'passing-syntax-overlay.diff'),
 'syntax_repairs':[{'change':'Bound sample variable omega -> sample throughout','reason':'ContDiff scoped notation omega is the analytic smoothness exponent; Mathlib Analysis/Calculus/ContDiff/FTaylorSeries.lean:118. Pure bound-variable alpha renaming.'},
  {'change':'Standalone end before #check','reason':'Close unnamed noncomputable section before the later named namespace end. Scope syntax only.'}],
 'parent_binder_definition_readback':info(OUT/'header-definition-binder-readback.json'),
 'slot_checks':checks,'required_mathematical_target_repairs':[],
 'warning_policy':'The six preserved standing hypothesis arguments are unused in the literal Prop body and trigger unused-variable warnings. Do not remove source binders to silence these warnings.',
 'checked_head_at_review':head,'fixed_mathlib_revision':mathlib,
 'source_preservation_overlay_review':'Separate independent source-preservation reviewer must bind the exact passing candidate bytes; wrong failed parentheses-only copy is not accepted.',
 'proof_BODY_created':False,'proof_credit':False,'statement_seal_created':False,'VERIFIED':False,'Goal_complete':False}
save('header-math-review78.json',header_review)

inventory=[
 {'anchors':['S1.p1.1','S1.E1','S2.SS2.p1.1'],'disposition':'NODE','reason':'C2, Hessian sandwich and source eta standing assumptions.'},
 {'anchors':['S2.E4','S3.E4','S3.E8','S3.E9','A1.SS1.p1.1','A1.Ex1','A1.SS1.p1.2','A1.Ex2','A1.Ex3','A1.SS1.p1.3'],'disposition':'NODE','reason':'Source c/residual/reflection including R0, explicit harmonic flow and event rate; discontinuity is harmless because rate0.'},
 {'anchors':['A1.SS1.p2.1','A1.E1','A1.E2','A1.SS1.p2.2'],'disposition':'NODE','reason':'Independent Exp1 E_(n+1), initial T0/zeta0, actual integrated-hazard waiting time, exact finite state/time update, stop-empty branch; between-jump formula only for finite prefix.'},
 {'anchors':['A1.SS1.p3.1','A1.Ex4','A1.SS1.p3.2','A1.Ex5'],'disposition':'NODE','reason':'Initial harmonic energy, flow/bounce preservation and momentum/displacement bounds.'},
 {'anchors':['A1.SS1.p3.3','A1.Ex6','A1.SS1.p3.4','A1.Ex7'],'disposition':'NODE','reason':'Beta-Lipschitz residual gives one initial-energy uniform finite rate cap and integrated cap.'},
 {'anchors':['A1.SS1.p3.5','A1.Ex8','A1.SS1.p3.6','A1.Ex9'],'disposition':'NODE','reason':'Separate zero-cap no-jump branch and positive-cap actual finite-wait/prefix-sum comparison; never-terminated source branch is explicit.'},
 {'anchors':['A1.SS1.p3.7 first SLLN and nonaccumulation clauses'],'disposition':'NODE','reason':'Author direct Exp1 finite-mean SLLN implies continuing times diverge; terminated branch has finite generated prefix.'},
 {'anchors':['A1.SS1.p3.7 later unique-process/Markov/Davis clauses'],'disposition':'EXCLUDED','reason':'Global path construction/uniqueness and memoryless Markov construction are downstream obligations, not this header.'},
 {'anchors':['A1.SS1.p4','A1.Ex10-Ex23','A1.Thmtheorem1','A1.E3-E8','A1.I1'],'disposition':'EXCLUDED','reason':'Momentum reversal/stationarity/L2/complete-path density and averaging statements and their substantive proofs are outside the selected edge.'},
 {'anchors':['S2.SS1 except reflection','S2.SS2 except eta','S3.SS2 vanilla/harmonic motivation','S3.E6-E7','Algorithm1 halfturn horizon/return','S3.Thmtheorem2-3','S3.E10'],'disposition':'EXCLUDED','reason':'Vanilla BPS thinning/refresh, conditional geometry/RGO, halfturn selection, position kernel/reversibility and stationary cost do not enter fixed-reference every-initial-state nonaccumulation.'}
]
topology={'schema_version':1,'reviewer':'/root/exact_verify77','distinct_from_extractor':'/root/source_review77',
 'status':'ACCEPTED_SCOPED_SOURCE_INVENTORY_AND_CASE_TOPOLOGY_WITH_EXPLICIT_REVIEWER_ADAPTER_OVERLAY',
 'extractor_freeze':info(BASE/'source-preread78/source-freeze78.json'),
 'bounded_synthesis':info(BASE/'source-preread78/bounded-synthesis78.json'),
 'independent_primary_region_readback':info(OUT/'independent-source-regions.json'),'six_complete_subtrees':regions,
 'reviewed_inventory':inventory,'missing_substantive_in_scope_source_regions_found':[],
 'source_errors_or_extra_binders_required':[],
 'source_route_assessment':'Source Ex9 requires actual clock-prefix summation AND positive finite cap AND divergent source Exp sums on the continuing branch. Terminated and zero-cap branches are alternatives. Direct author mean-one/SLLN and ASTIS bounded-indicator divergence remain alternative sufficient numerator proofs, never one false AND.',
 'open_source_background_gaps':['Global gradient Lipschitz from C2 Hessian upper bound','Finite integrated-hazard infimum attainment','Actual finite-prefix induction','Direct Exp integrability/mean-one SLLN background route','Zero-cap stopping from positive thresholds','Finite bounded-horizon index-set adapter'],
 'gap_status_note':'SOURCE_GAP means an omitted background or bridge requiring evidence, not a paper error or permission for a new public premise. Existing compiled parents may discharge relevant gaps but do not rewrite how the author argued.',
 'reviewer_edge_clarifications':[
  {'kind':'source-hypothesis edge refinement','parents':['standing-eta'],'consumer':'energy-invariance','use_site':'A1.SS1.p3.2','reason':'The harmonic sqrt/inverse energy identities use eta>0; retain the explicit edge rather than relying only on implicit global source context.'},
  {'kind':'prospective target adapter, not new attributed source theorem','parents':['nonaccumulation source conclusion plus stopped-as-top representation'],'consumer':'finite-horizon-escape','use_site':'prospective header first conclusion','reason':'Each finite physical horizon is eventually exceeded on either stopped or continuing sample paths.'},
  {'kind':'prospective target adapter, not author proof credit','parents':['finite-horizon-escape'],'consumer':'bounded-horizon-finite-count','use_site':'prospective header second conclusion','reason':'An eventual strict bound gives containment of the sublevel index set in Finset.range N, including initialization index0. This SOURCE_GAP node is listed but unconnected in the extractor graph; attach this reviewed adapter when binding the header.'}],
 'optional_graph_compression_note':'Exp-moment-support bundles positivity with integrability/mean-one. Zero-cap stopping uses positivity only; split support from direct-moment background when refining dependencies, so a future graph does not suggest direct moments are necessary on zero-cap or indicator routes.',
 'required_source_or_mathematical_header_repairs':[],
 'chronology_and_limits':[
  'The original candidate and extractor bounded synthesis were read before successful independent raw-primary extraction. Initial bs4 extraction failed because bs4 is unavailable; the standard-library parser then independently selected complete primary regions and verified all six exact raw digests.',
  'An initial broad read of the existing finite-parent file included the beginning of its proof BODY, consisting of repeated literal definitions. Definition equality checks use only the private Prop. Existing BODY was not used to infer the source author topology; no edge78 BODY exists.',
  'This is a distinct reviewer mathematical/raw-source coverage audit, not a source-blind decoder, extractor self-approval, future final compiled-source audit, or theorem proof.',
  'Bind this review and its explicit adapter overlay with the unchanged source freeze. Do not present the unconnected finite-count gap as already compiled.'
 ],'proof_credit':False,'VERIFIED':False,'Goal_complete':False}
save('independent-source-topology-review78.json',topology)
save('prospective-review-manifest78.json',{'reviewer':'/root/exact_verify77','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'original_candidate':info(original),'passing_syntax_overlay':info(passing),'overlay_diff':info(OUT/'passing-syntax-overlay.diff'),
 'header_math_review':info(OUT/'header-math-review78.json'),'independent_source_topology_review':info(OUT/'independent-source-topology-review78.json'),
 'typecheck_receipt':info(OUT/'syntax-rename-typecheck.receipt.json'),
 'failed_diagnostic_receipts':[info(OUT/'typecheck.receipt.json'),info(OUT/'syntax-repair-typecheck.receipt.json')],
 'canonical_candidate_modified':False,'shared_metadata_or_ledger_modified':False,'new_theorem_BODY':False,'proof_credit':False})
print('PROSPECTIVE HEADER/MATH AND DISTINCT SOURCE-TOPOLOGY REVIEWS WRITTEN')
print('passing candidate',info(passing))
print('review manifest',info(OUT/'prospective-review-manifest78.json'))
