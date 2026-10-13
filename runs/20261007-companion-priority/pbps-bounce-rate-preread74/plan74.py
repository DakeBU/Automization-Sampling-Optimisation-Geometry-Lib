"""Source-first prerequisite plan only; no Lean search, implementation or canonical writes."""
from __future__ import annotations
import ctypes, hashlib, html, json, os, re, subprocess, sys
from pathlib import Path

ROOT=Path('E:/Samplinglib')
OWN=Path(__file__).resolve().parent
PRIMARY=ROOT/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
EXPECTED='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
PRE73=ROOT/'runs/20261007-companion-priority/pbps-half-turn-construction-preread73'
MODULE=ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHarmonicFlow.lean'
LF_RECIPE='Replace CRLF byte pairs with LF only; preserve bare CR and every other byte.'
RUN_RECIPE='Delete ONLY top-level run_sha256. json.dumps ensure_ascii=False, sort_keys=True, separators=(comma,colon), allow_nan=False; UTF-8 without BOM/newline; SHA256. Retain every nested hash and all other fields.'
def sha(b): return hashlib.sha256(b).hexdigest()
def cj(v): return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode('utf-8')
def logical(v): return sha(cj({k:x for k,x in v.items() if k!='run_sha256'}))
def read(p): return json.loads(Path(p).read_bytes())
def pin(p):
    p=Path(p); b=p.read_bytes(); lf=b.replace(b'\r\n',b'\n')
    return {'path':p.as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_bytes':len(lf),'LF_sha256':sha(lf),'LF_recipe':LF_RECIPE}
def save(n,v):
    assert not (OWN/'lease.final.json').exists()
    p=OWN/n; assert OWN in p.resolve().parents; p.parent.mkdir(parents=True,exist_ok=True)
    p.write_bytes((json.dumps(v,ensure_ascii=False,sort_keys=True,indent=2,allow_nan=False)+'\n').encode('utf-8'))
def textfile(n,t):
    assert not (OWN/'lease.final.json').exists()
    p=OWN/n; assert OWN in p.resolve().parents; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(t.encode('utf-8'))
def guard(pins):
    for p in pins: assert pin(p['path'])==p,('input drift',p['path'])
def readview(raw):
    s=raw.decode('utf-8')
    s=re.sub(r'<math\b[^>]*alttext="([^"]*)"[^>]*>[\s\S]*?</math>',lambda m:html.unescape(m.group(1)),s)
    return ' '.join(html.unescape(re.sub(r'<[^>]*>',' ',s)).split())

STATEMENT='''Proposed single actual-consumer theorem (not sealed, implemented or compiled): actual_bounce_rate_energy_laws.

Ambient E is a finite-dimensional real inner-product space with its compatible norm, MeasurableSpace and BorelSpace, including rank zero. Retain exactly the six original analytic callers: hα:0<(α:ℝ), hαβ:α≤β, hV:ContDiff ℝ 2 V, hH:the two global genuine iterated-Frechet-Hessian quadratic bounds with α,β:ℝ≥0, hη:0<η, hβη:(β:ℝ)η≤1. y,xRef,x,p range over all E independently. No supplied gradient-Lipschitz, flow, reflection, energy, kernel, clock, positive-dimension, nonzero-normal or higher-regularity certificate is a caller.

Define c(y,xRef)=y−η∇V(xRef); h(xRef,x)=∇V(x)−∇V(xRef); R(h,p)=p−2⟨p,h⟩h/‖h‖² when h≠0 and R(0,p)=p; S(xRef,(x,p))=(x,R(h(xRef,x),p)); λ(xRef,(x,p))=√η max(0,⟨p,h(xRef,x)⟩); H(y,xRef,(x,p))=(η⁻¹‖x−c(y,xRef)‖²+‖p‖²)/2. H uses the weighted SUM of two vector squared norms.

Required bounded conclusions:
1. The actual map (y,xRef,x,p)↦S(xRef,(x,p)) is jointly Borel measurable, including the zero-normal locus. The unused y argument is harmless; the leanest literal may quantify only (xRef,x,p).
2. S fixes x and is involutive on every phase point, including h=0.
3. ‖R(h(xRef,x),p)‖=‖p‖; hence H(y,xRef,S(xRef,z))=H(y,xRef,z) for all y,xRef,z.
4. ⟨R(h,p),h⟩=−⟨p,h⟩, for the actual h and also h=0.
5. λ is jointly continuous in (xRef,x,p), hence Borel, and λ≥0. If h(xRef,x)=0 then S(xRef,(x,p))=(x,p) and λ(xRef,(x,p))=0.
6. Writing a=⟨p,h(xRef,x)⟩, λ(xRef,S(xRef,(x,p)))=√η max(0,−a) and λ(xRef,(x,p))−λ(xRef,S(xRef,(x,p)))=√η a.
7. Derive, internally from hV,hH, LipschitzWith β (gradient V); no extra public premise. It may remain an internal witness rather than a separate conjunct if only the envelope consumes it.
8. For every z0 and every z=(x,p) with H(y,xRef,z)=H(y,xRef,z0), put ℰ=H(y,xRef,z0). Internally ℰ≥0; then ‖p‖≤√(2ℰ) and ‖x−c‖≤√(2ηℰ).
9. For the SAME y,xRef,z0,z, λ(xRef,z)≤Λ_ℰ(y,xRef), where Λ_ℰ(y,xRef)=√η β √(2ℰ){√(2ηℰ)+‖c(y,xRef)−xRef‖}. This is the exact printed source majorant on one energy layer. It assumes no ℰ>0 and divides by no Λ.

Scope excludes flow reconstruction, hazard integrals or stopping times, clocks/random variables, path recursion, nonexplosion/uniqueness/Markov/stationarity, invariant or terminal kernels, rates of convergence and expected costs. The same-level condition is a universally quantified conclusion antecedent expressing the source energy layer, not a new analytic caller. Optional later sublevel generalization H≤ℰ is unnecessary for this source-faithful packet and is not selected.
'''

REVIEW='''# Source-first PBPS bounce/rate prerequisite plan74

Select one actual-consumer theorem, proposed name actual_bounce_rate_energy_laws in proposed AutoSamplingTheory/ExampleCases/ProximalBPS/ActualBounceRate.lean. No Lean file or header is created. The selected delta includes the actual Borel bounce, its involution/norm/weighted-SUM-energy laws, continuous nonnegative actual rate, flipped pairing/rate identity, and the printed uniform energy-layer envelope. These are one connected deterministic prerequisite for Proposition3.1, not a new generic reflection library or a full PDMP construction. The sole root writer may seal or adjust this prospective statement after review.

The primary input is the exact PBPS v1 HTML RAW d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760. Selected source intervals are checked directly against those bytes. Earlier pre73 source.regions is only an interval locator: every chosen interval/hash and formula is re-read from the primary. This standalone source graph follows printed definitions and proof assertions rather than a Lean proof. The fixed published formula anchors are S2.E4.m1 for R_h and R_0, S3.E4.m1 for c/h, Algorithm1 steps6–7 and S3.E9.m1 for λ and bounce, A1.SS1.p1 for S and involution/zero-rate discontinuity, and A1.SS1.p3 plus A1.Ex4–6 for energy, coordinate radii and Λ. Proposition3.1 is S3.Thmtheorem1. The printed Davis[12,§2] link is #bib.bib16, not #bib.bib12; its 1984 PDMP paper is an external cited future construction dependency, not read/admitted here.

The public assumptions must remain the original finite-real-Hilbert/Borel setting and six callers hα,hαβ,hV,hH,hη,hβη. Current compiled73 has exactly this header and the same c,H. Its science admission is still pending; planning74 does not upgrade it. Bounce/rate algebra does not require the73 flow theorem as a formal parent. Actual harmonic flow73 and the proposed74 laws are sibling deterministic ingredients consumed together only in the later hazard/recursion/nonexplosion proof. Nothing in72 corrector perturbation or the L2 reflection blocks is a dependency of74.

Mathlib already has the generic geometric reflection. Let K=span{h}. Its reflection is 2 projection_K−id; reflection in K-perp is its negative. Submodule.reflection_singleton_apply and reflection_orthogonal_apply therefore identify source R_h with reflection in K-perp. At h=0, K=bottom and K-perp=top, so source R_0=id. This identification internally yields involution and norm preservation; no generic ASTIS wrapper theorem or user-supplied isometry is needed. At a nonzero h, the elementary pairing calculation is ⟨p−2⟨p,h⟩h/‖h‖²,h⟩=−⟨p,h⟩. At h=0 both sides are zero. Position is unchanged, so preserving the second individual norm preserves the exact weighted SUM energy.

For joint Borel measurability use the actual explicit coordinate formula with total real division: p−(2⟨p,h⟩/‖h‖²)h. Real total inverse/division are Borel at zero even though inverse is not continuous there; at h=0 its correction is exactly zero, agreeing with R_0=id. Native ContinuousInv₀.measurableInv and Measurable.div/smul/prodMk supply this route after actual gradient continuity. Do not infer continuous bounce from fixed-h linear continuity: in E=R, V(x)=x²/2, xRef=0, p=1, R_{h(x)}p=−1 for x≠0 but R_0p=1. This counterexample obeys α=β=η=1 and the source callers, including the step endpoint. λ instead is continuous because gradient, inner product and max are continuous. Thus h=0 gives λ=0 and no rate ambiguity.

Actual β-Lipschitzness is already available internally: QuadraticRegularization.strongConvexOn_and_lipschitzWith_gradient_add_quadratic with U=V,m=α,L=β,r=0,u=0 produces LipschitzWith β (gradient V) after zero-quadratic simplification. Finite dimension supplies completeness. The existing GibbsGradientMean proof already uses this exact r=0 specialization. It also gives gradient continuity, so the separate Gradient.continuous_gradient_of_contDiff_one API is an audited fallback, not a required duplicate parent. The lower Hessian bound is retained as in the original source; no supplied Hessian operator, Lipschitz condition or stronger regularity is introduced.

The source envelope is pointwise and finite. If H(z)=ℰ≥0, the nonnegative SUM gives ‖p‖²≤2ℰ and ‖x−c‖²≤2ηℰ. Cauchy–Schwarz, actual β-Lipschitzness and the triangle inequality give λ≤√η‖p‖‖h‖≤√η β‖p‖‖x−xRef‖≤√η β√(2ℰ){√(2ηℰ)+‖c−xRef‖}. This is the printed A1.Ex6 constant, with no dimension factor and no unrecorded strictness. Pairing flip gives λ(Sz)=√η max(0,−a), so λ(z)−λ(Sz)=√η a. This supports a future stationarity balance calculation; it is not stationarity by itself.

Rank zero has only zero vectors: h=0, S=id, H=λ=Λ=0 and every formula remains legal. αη=1 is allowed; there is no denominator1−αη. For zero energy z=(c,0), bounce fixes z and λ=Λ=0 even if h(c)≠0. A future hazard proof must branch on Λ=0 before any waiting-time division. At h=0 with p≠0, momentum is fixed and rate is zero; neither nonzero h nor positive energy may become a caller.

The real consumer is the deterministic bound used inside AppendixA.1's Proposition3.1 construction: combine harmonic73 energy preservation with74 jump energy preservation and Λ to keep every finite recursively produced state in the same layer, then bound each integrated hazard. Crossing-time Borel measurability, canonical independent Exp(1) clocks, finite/infinite stopping conventions, actual recursion, SLLN/nonaccumulation, memorylessness/Markov property and stationary law require separate packets and cited background. The source graph records these as out-of-scope nodes, not completed edges. Actual terminal H_y, actual K/r_rho/B27/B28, full paper results, errors/caps, costs/composition, PURIFIED and Goal completion remain open.

Minimal route in seven steps: (1) internally specialize the existing quadratic producer at r=0; (2) identify total-coordinate R with the existing orthogonal-complement reflection including h=0; (3) derive involution/norm and weighted energy; (4) prove actual joint Borel by measurable total division and rate continuity/nonnegativity; (5) derive pairing/rate flip with a zero/nonzero case split only inside the proof; (6) extract coordinate radii from the SUM energy; (7) combine Cauchy–Schwarz, β-Lipschitzness and triangle inequality for the exact Λ. This is an analytic plan, not Lean proof search or implementation. The public header still needs root's Statement Seal and independent prospective review before proof search.

Retrieval negatives are preserved separately: bs4 is absent, an exploratory one-line shell quoting attempt failed, two guessed module cards and two guessed Mathlib paths were absent. These are tooling/path evidence only; corrected native files and the standard-library reader supplied the actual contracts. No API or mathematical nonexistence is inferred from these diagnostics. No Lean compiler, harness/publication/site aggregate, Goal, ledger, Git mutation or VERIFIED transition ran. Native final manifest and CLOSED_LAST cover only this new owned directory; an external process verifies it read-only.
'''

def build():
    assert not (OWN/'plan74.json').exists()
    b=PRIMARY.read_bytes(); assert sha(b)==EXPECTED
    regions=read(PRE73/'source.regions.json')
    ids=['S1.p1','S2.E4.m1','S3.E4.m1','alg1','S3.Thmtheorem1','A1.SS1.p1','A1.SS1.p3']
    slices=[]
    for ident in ids:
        x=next(x for x in regions['regions'] if x['source_id']==ident)
        lo,hi=x['raw_byte_start_inclusive'],x['raw_byte_end_exclusive']; raw=b[lo:hi]
        assert len(raw)==x['bytes'] and sha(raw)==x['literal_span_raw_sha256']
        target=OWN/'source-slices'/f'{ident}.exactraw.html'; target.parent.mkdir(parents=True,exist_ok=True); target.write_bytes(raw)
        slices.append({'source_id':ident,'source':pin(PRIMARY),'RAW_start_inclusive':lo,'RAW_end_exclusive':hi,'literal_slice':pin(target),'readview':readview(raw)})
    match=re.search(rb'<li id="bib\.bib16"[\s\S]*?</li>',b); assert match and b'Davis' in match.group()
    target=OWN/'source-slices/bib.bib16.exactraw.html'; target.write_bytes(match.group())
    slices.append({'source_id':'bib.bib16','source':pin(PRIMARY),'RAW_start_inclusive':match.start(),'RAW_end_exclusive':match.end(),'literal_slice':pin(target),'readview':readview(match.group())})
    formulas=[]
    fids=['S1.E1.m1','S2.E4.m1','S3.E4.m1','S3.E9.m1','A1.Ex1.m1','A1.Ex4.m1','A1.Ex5.m1','A1.Ex6.m1']
    for ident in fids:
        x=next(x for x in regions['formulas'] if x['source_id']==ident); raw=b[x['raw_byte_start_inclusive']:x['raw_byte_end_exclusive']]
        assert sha(raw)==x['literal_span_raw_sha256']
        alt=re.search(rb'alttext="([^"]*)"',raw); assert alt
        formula=html.unescape(alt.group(1).decode()); assert formula==x['formula_alttext']
        formulas.append({'source_id':ident,'literal_span_RAW_sha256':sha(raw),'RAW_start_inclusive':x['raw_byte_start_inclusive'],'RAW_end_exclusive':x['raw_byte_end_exclusive'],'formula_alttext':formula})
    save('source.regions74.json',{'primary':pin(PRIMARY),'source_URL':'https://arxiv.org/html/2609.06905v1','offset_rule':'0-based RAW byte start inclusive/end exclusive; source-native ids; HTML math alttext retained','regions':slices,'formulas':formulas,'source_review_or_formal_credit':False})
    api_specs=[
      ('AutoSamplingTheory/TechnicalLemmas/Analysis/QuadraticRegularization.lean','strongConvexOn_and_lipschitzWith_gradient_add_quadratic',29,43,'Existing ASTIS actual Hessian-to-gradient producer; use r=0 internally, not a caller.'),
      ('AutoSamplingTheory/TechnicalLemmas/Analysis/GibbsGradientMean.lean','existing r=0 specialization',44,52,'Actual local reuse example, not a new theorem dependency.'),
      ('AutoSamplingTheory/TechnicalLemmas/Analysis/Calculus/Gradient.lean','continuous_gradient_of_contDiff_one',None,None,'Audited fallback; selected route obtains continuity from β-Lipschitzness.'),
      ('.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Projection/Reflection.lean','Submodule.reflection + reflection_involutive + reflection_orthogonal_apply + reflection_singleton_apply',26,109,'Real complete/subspace-projection context; R is reflection in orthogonal complement, not span reflection itself.'),
      ('.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Continuous.lean','continuous_inner and Continuous.inner',63,92,'Joint continuous pairing.'),
      ('.lake/packages/mathlib/Mathlib/MeasureTheory/Constructions/BorelSpace/Basic.lean','ContinuousInv₀.measurableInv',601,604,'Borel total inverse at zero; no continuity of inverse at zero.'),
      ('.lake/packages/mathlib/Mathlib/MeasureTheory/Group/Arithmetic.lean','Measurable.div',269,272,'MeasurableDiv₂ including real total division.'),
      ('.lake/packages/mathlib/Mathlib/MeasureTheory/Group/Arithmetic.lean','Measurable.smul',536,539,'Joint measurable scalar/vector multiplication.'),
      ('.lake/packages/mathlib/Mathlib/MeasureTheory/MeasurableSpace/Constructions.lean','Measurable.prodMk',410,414,'Joint phase output.'),
      ('.lake/packages/mathlib/Mathlib/Topology/Order/OrderClosed.lean','Continuous.max',696,700,'Positive part as max0.'),
      ('.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Basic.lean','norm_sub_sq_real',435,437,'Optional direct algebra fallback, no new generic leaf.'),
      ('.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Basic.lean','abs_real_inner_le_norm',465,467,'Cauchy–Schwarz in exact real orientation.'),
      ('.lake/packages/mathlib/Mathlib/Analysis/Real/Sqrt.lean','Real.le_sqrt and le_sqrt_of_sq_le',240,260,'Non-strict radius bounds including zero energy.'),
      ('.lake/packages/mathlib/Mathlib/Topology/MetricSpace/Lipschitz.lean','LipschitzWith.dist_le_mul',45,50,'Distance bound; translate with dist_eq_norm.'),
      ('.lake/packages/mathlib/Mathlib/Analysis/Normed/Operator/LinearIsometry.lean','SemilinearIsometryClass.norm_map',69,78,'Reflection is already a LinearIsometryEquiv, so generic norm preservation exists.')]
    apis=[]
    for rel,name,lo,hi,role in api_specs:
        p=ROOT/rel; lines=p.read_bytes().splitlines(keepends=True)
        if lo is None:
            lo=next(i+1 for i,x in enumerate(lines) if x.startswith(b'theorem continuous_gradient_of_contDiff_one')); hi=lo+6
        raw=b''.join(lines[lo-1:hi]); assert raw
        apis.append({'source_file':pin(p),'API':name,'start_line':lo,'end_line':hi,'literal_RAW_sha256':sha(raw),'literal_UTF8':raw.decode('utf-8'),'role':role,'status':'RETRIEVED_FIXED_SOURCE_ONLY_NOT_NEW74_CERTIFICATE'})
    save('minimal.actual-API-audit74.json',{'APIs':apis,'minimal_direct_import_candidates':['AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularization','Mathlib.Analysis.InnerProductSpace.Projection.Reflection','Mathlib.MeasureTheory.Constructions.BorelSpace.Basic'],'imports_compiled':False,'local_reflections_not_the_bounce':{'GaussianReflection.reflection_preserves_augmentation':'Auxiliary affine y↦2x−y on generative Gaussian augmentation; different state/normal/map.','ReflectionL2.actual_reflection_block_identities':'L2 conditional-projection/auxiliary-reflection algebra; not momentum Householder bounce.'},'Probability_SDE_inventory':'Base Probability/SDE contracts do not provide the actual event-driven PBPS construction; no new generic probability/SDE wrapper is proposed.'})
    nodes=[
      ('SRC-assumptions','source-conditions','S1.p1','C2, original two global Hessian bounds, positive moduli, positive capped η'),
      ('SRC-R','source-definition','S2.E4.m1','R_h=I−2hhᵀ/‖h‖², R_0=I'),
      ('SRC-center-normal','source-definition','S3.E4.m1','c=y−η∇V(xRef), h=∇V(x)−∇V(xRef)'),
      ('SRC-rate','source-definition','S3.E9.m1','λ=√η[pᵀh]_+'),
      ('SRC-bounce','source-definition','A1.SS1.p1','S(x,p)=(x,R_hp), possible h=0 discontinuity with zero event rate'),
      ('SRC-involution','source-assertion','A1.SS1.p1','Bounce map is an involution'),
      ('SRC-energy','source-definition','A1.Ex4.m1','H=(η⁻¹‖x−c‖²+‖p‖²)/2'),
      ('SRC-energy-preservation','source-assertion','A1.SS1.p3','Each bounce preserves harmonic energy'),
      ('SRC-radii','source-assertion','A1.Ex5.m1','‖p‖≤√2ℰ and ‖x−c‖≤√(2ηℰ)'),
      ('SRC-Lambda','source-assertion','A1.Ex6.m1','Uniform finite rate majorant on same energy layer'),
      ('BG-regularity','background-gap','S1.p1; A1.SS1.p3','C2/Hessian assumptions imply continuous actual gradient and β-Lipschitzness; background not an extra binder'),
      ('BG-reflection','background-gap','S2.E4.m1; A1.SS1.p1','Zero-safe reflection identification, norm preservation and sign flip'),
      ('BG-Borel','background-gap','A1.SS1.p1; Algorithm1 step7','Joint measurability through the possibly discontinuous zero-normal locus'),
      ('BG-positive-part','background-gap','S3.E9.m1','Continuous nonnegative positive-part rate; flipped pairing gives rate difference'),
      ('BG-envelope','background-gap','A1.SS1.p3','Nonnegative SUM radii, Cauchy–Schwarz, Lipschitz, triangle inequality'),
      ('OUT-hazard-recursion','out-of-scope-source-consumer','A1.SS1.p2; A1.SS1.p3','Integrated hazard crossing, exponential clocks, actual measurable recursion'),
      ('OUT-Prop3.1','out-of-scope-source-consumer','S3.Thmtheorem1','Nonexplosion/uniqueness/Markov/stationarity and actual terminal position'),
      ('EXT-Davis','external-cited-open','A1.SS1.p3 -> bib.bib16','Davis1984 integrated hazard construction §2, source printed [12]; external paper not reviewed here')]
    edges=[('SRC-assumptions','BG-regularity'),('SRC-R','BG-reflection'),('SRC-center-normal','SRC-bounce'),('SRC-R','SRC-bounce'),('BG-reflection','SRC-involution'),('BG-reflection','SRC-energy-preservation'),('SRC-energy','SRC-energy-preservation'),('SRC-center-normal','BG-Borel'),('BG-regularity','BG-Borel'),('SRC-bounce','BG-Borel'),('SRC-rate','BG-positive-part'),('BG-regularity','BG-positive-part'),('BG-reflection','BG-positive-part'),('SRC-energy','BG-envelope'),('BG-regularity','BG-envelope'),('BG-envelope','SRC-radii'),('SRC-rate','SRC-Lambda'),('SRC-radii','SRC-Lambda'),('BG-envelope','SRC-Lambda'),('SRC-bounce','OUT-hazard-recursion'),('BG-Borel','OUT-hazard-recursion'),('BG-positive-part','OUT-hazard-recursion'),('SRC-energy-preservation','OUT-hazard-recursion'),('SRC-Lambda','OUT-hazard-recursion'),('OUT-hazard-recursion','OUT-Prop3.1'),('EXT-Davis','OUT-Prop3.1')]
    save('standalone.source-proof-graph74.json',{'schema':'astis-prospective-source-first-graph74/v1','primary':pin(PRIMARY),'graph_truth':'source definitions/assertions and independently reconstructed background prerequisites only; not compiled Lean edges or acceptance','nodes':[{'id':a,'kind':k,'source_anchor':anchor,'statement':s,'admission':'PLANNING_ONLY_OPEN74'} for a,k,anchor,s in nodes],'edges':[{'from':a,'to':z,'semantics':'source-proof-ingredient-not-new-formal-edge'} for a,z in edges],'coverage_boundary':'Only actual bounce/rate/energy-majorant source slice. Full Proposition3.1 and full paper source coverage are not claimed.'})
    module_bytes=MODULE.read_bytes(); assert sha(module_bytes)=='506c1d57b3c9133db1cfc0515dccbd8759aaec3e1dbf4a128f6a73d3aeb73c8c'
    header=module_bytes[:module_bytes.index(b':= by\n')+6]
    textfile('actual73.compiled-header.exactraw.txt',header.decode('utf-8'))
    textfile('prospective.actual-contract74.utf8.md',STATEMENT)
    negatives=[{'type':'retrieval-tooling','diagnostic':'ModuleNotFoundError: No module named bs4','resolution':'Use standard-library regex/math-alttext reader on exact bounded intervals.','actual_PID':'not captured by preliminary tool call; no PID invented'}, {'type':'shell-quoting','diagnostic':'SyntaxError: unterminated string literal in one exploratory inline command','resolution':'Use owned Python file with native Path reads.','actual_PID':'not captured by preliminary tool call; no PID invented'}, {'type':'path-lookup','diagnostic':'Two guessed cards QuadraticRegularization/GaussianReflection and guessed Reflection/Prod Mathlib paths absent; PowerShell rg wildcard syntax error','resolution':'Use rg --files and actual Projection/Reflection, MeasurableSpace/Constructions plus existing Gradient module card. Absence of a guessed path is not absence of mathematics.','actual_PID':'not captured by preliminary tool call; no PID invented'}]
    save('retrieval-negative-evidence74.json',{'failures':negatives,'mathematical_negative_evidence':False,'all_retained_no_failed_proof_search':True})
    paths=[PRIMARY,PRE73/'source.regions.json',PRE73/'selected-contract.json',MODULE,ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/GaussianReflection.lean',ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ReflectionL2.lean',ROOT/'AutoSamplingTheory/Probability.lean',ROOT/'AutoSamplingTheory/SDE.lean',ROOT/'AutoSamplingTheory/TechnicalLemmas/Probability.lean',ROOT/'research-wiki/sampling-sde-library/cards/AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient.md',ROOT/'website/content/samplewiki_companion_frontiers.json',ROOT/'docs/companion-papers-handoff.md',ROOT/'.agents/skills/astis-source-dependency-audit/SKILL.md',ROOT/'docs/theorem-publication-protocol.md',ROOT/'docs/proof-digestion-protocol.md',ROOT/'lean-toolchain',ROOT/'lake-manifest.json']+[Path(x['source_file']['path']) for x in apis]
    pins=[pin(x) for x in dict.fromkeys(paths)]; guard(pins)
    plan={'schema':'astis-source-first-prerequisite-plan74/v1','status':'READY_FOR_ROOT_STATEMENT_SEAL_ONLY','author':'/root/header_math72','actual_plan_reader_PID':os.getpid(),'checked_parent':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'source_primary':pin(PRIMARY),'selected_delta':'Actual zero-safe Borel bounce, involution/norm/weighted energy, continuous nonnegative rate, flipped pairing/rate difference and exact uniform energy-layer envelope','proposed_home':'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualBounceRate.lean (not created)','proposed_declaration':'actual_bounce_rate_energy_laws (not sealed)','complete_natural_statement':STATEMENT,'original_six_callers':read(PRE73/'selected-contract.json')['caller_contract'],'real_consumer':'Proposition3.1 AppendixA.1 fixed-reference hazard recursion/nonexplosion deterministic prerequisites','actual73_status':'Current exact compiled header inspected; science admission pending. No74 prerequisite completion follows.73 and74 are siblings for later consumer, not an invented formal edge.','background_gap_classes':{'BG-regularity':'local-lemma already available; derive internally at r=0','BG-reflection':'mathlib-available; source orientation/zero adapter remains74 work','BG-Borel':'internal-paper-step/source-implicit; measurable total quotient available','BG-positive-part':'internal-paper-step/source-implicit; max/inner continuity and sign adapter','BG-envelope':'internal-paper-step; all constituent norm/Lipschitz/sqrt APIs available','EXT-Davis':'external-cited-result future consumer, unreviewed'},'proof_route_steps':7,'new_public_regularities':[],'duplicate_generic_wrapper':False,'new_Lean_files':False,'proof_search':False,'compiler_ran':False,'source_admission':False,'VERIFIED':False,'Goal_created_or_completed':False,'canonical_Git_ledger_writes':False,'fullpaper_cost_composition_credit':False,'input_count':len(pins),'inputs':pins,'retrieval_negatives':negatives}
    save('finite.inputs74.json',{'inputs':pins,'LF_recipe':LF_RECIPE})
    save('plan74.json',plan); textfile('named.source-first-prerequisite-review74.utf8.md',REVIEW)
    print(json.dumps({'actual_reader_writer_PID':os.getpid(),'status':plan['status'],'finite_inputs':len(pins),'source_regions':len(slices),'source_formulas':len(formulas),'source_nodes':len(nodes),'source_edges':len(edges),'actual_APIs':len(apis),'Lean_run':False,'EXIT':0},ensure_ascii=False))

def launch():
    assert not (OWN/'reader.terminal.json').exists()
    command=[sys.executable,'-B','-X','utf8',str(Path(__file__).resolve()),'build']
    with (OWN/'reader.stdout.txt').open('wb') as out,(OWN/'reader.stderr.txt').open('wb') as err:
        p=subprocess.Popen(command,cwd=ROOT,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONUTF8='1'),stdout=out,stderr=err); code=p.wait()
    save('reader.terminal.json',{'command':command,'actual_foreground_PID':p.pid,'terminal_EXIT':code,'observer_PID':os.getpid(),'stdout':pin(OWN/'reader.stdout.txt'),'stderr':pin(OWN/'reader.stderr.txt')})
    print(json.dumps(read(OWN/'reader.terminal.json'),ensure_ascii=False)); return code

def close():
    plan=read(OWN/'plan74.json'); terminal=read(OWN/'reader.terminal.json'); assert terminal['terminal_EXIT']==0 and terminal['actual_foreground_PID']==plan['actual_plan_reader_PID']; guard(plan['inputs'])
    assert (OWN/'reader.stderr.txt').read_bytes()==b''
    assert (ROOT/'lean-toolchain').read_text(encoding='utf-8').strip()=='leanprover/lean4:v4.33.0'
    mathlib=next(p for p in read(ROOT/'lake-manifest.json')['packages'] if p['name']=='mathlib')
    assert mathlib['rev']=='db584cd6d46c92f209a44c0f1c829460d327499d'
    capsule={'schema':'astis-bounded-source-first-capsule74/v1','status':'READY_FOR_ROOT_STATEMENT_SEAL_ONLY','attribution':'Fan Chen, Sinho Chewi, Jianfeng Lu and Matthew S. Zhang; PBPS arXiv2609.06905v1','selected_delta':plan['selected_delta'],'proposed_declaration':plan['proposed_declaration'],'same_six_callers':['hα','hαβ','hV','hH','hη','hβη'],'exact_primary_RAW_sha256':EXPECTED,'source_anchors':['S2.E4.m1','S3.E4.m1','alg1 steps6-7; S3.E9.m1','A1.SS1.p1','A1.Ex4.m1','A1.Ex5.m1','A1.Ex6.m1','S3.Thmtheorem1'],'minimal_existing_parents':['QuadraticRegularization.strongConvexOn_and_lipschitzWith_gradient_add_quadratic, r=0 internally','Mathlib Submodule orthogonal-complement reflection; total real Borel division'],'actual73_relationship':'Sibling deterministic prerequisite for later Proposition3.1 consumer; exact compiled header unchanged, science admission pending. No invented formal parent.','zero_and_endpoint':'R0=id; h0 rate0; rank0 legal; alphaeta1 legal; E0 gives Lambda0 with no division.','real_consumer':plan['real_consumer'],'next_unproved_boundary':'Combine73 flow energy with74 bounce/majorant in a separately measurable integrated-hazard/clock recursion. Nonexplosion, Markov/stationarity and terminal kernels remain open.','explicit_background_gaps':['actual Hessian to beta-Lipschitz producer specialization','zero-safe Householder orientation/norm/flip adapter','joint Borel at discontinuous zero normal','continuous positive-part rate and difference identity','SUM-energy radii/Cauchy/triangle majorant'],'no_duplicate_generic_wrapper':True,'no_proof_search_implementation_compiler_run':True,'native_finite_inputs':len(plan['inputs']),'reader_PID':terminal['actual_foreground_PID'],'reader_terminal_EXIT':terminal['terminal_EXIT'],'named_plan':pin(OWN/'plan74.json'),'source_graph':pin(OWN/'standalone.source-proof-graph74.json'),'actual_API_audit':pin(OWN/'minimal.actual-API-audit74.json'),'toolchain':'Lean4.33.0','Mathlib_revision':mathlib['rev'],'no_new_truth_or_Goal_credit':True}
    save('capsule74.json',capsule)
    complete={'schema':'astis-complete-named-source-first-plan74/v1','bounded_capsule':capsule,'named_review':REVIEW,'named_decision_and_input_payload':plan,'source_regions_and_exact_formulas':read(OWN/'source.regions74.json'),'standalone_source_graph':read(OWN/'standalone.source-proof-graph74.json'),'minimal_actual_API_audit':read(OWN/'minimal.actual-API-audit74.json'),'terminal_receipt':terminal,'writer_PID':os.getpid(),'wholelogicalrun_recipe':RUN_RECIPE}
    save('complete-named-review-decision-input-payload.json',complete)
    run={'schema':'astis-source-first-plan74-run/v1','author':plan['author'],'inputs':plan['inputs'],'named_plan':pin(OWN/'plan74.json'),'complete_named_payload':pin(OWN/'complete-named-review-decision-input-payload.json'),'review':pin(OWN/'named.source-first-prerequisite-review74.utf8.md'),'reader_terminal':terminal,'actual_final_writer_PID':os.getpid(),'wholelogicalrun_recipe':RUN_RECIPE,'proof_search_implementation_compilation':False,'canonical_Git_ledger_Goal_VERIFIED_writes':False,'retrieval_negative_evidence':pin(OWN/'retrieval-negative-evidence74.json')}
    run['run_sha256']=logical(run); save('run.json',run)
    owned=[pin(p) for p in sorted(OWN.rglob('*')) if p.is_file() and p.name not in ['native.manifest.json','lease.final.json']]
    save('native.manifest.json',{'owned_root':OWN.as_posix(),'owned_files':owned,'LF_recipe':LF_RECIPE,'exclusions':['native.manifest.json self-reference','lease.final.json final write'],'run_sha256':run['run_sha256'],'wholelogicalrun_recipe':RUN_RECIPE})
    lease={'status':'CLOSED_LAST','actual_last_writer_PID':os.getpid(),'owned_files':len(owned)+2,'run_sha256':run['run_sha256'],'manifest':pin(OWN/'native.manifest.json'),'complete_named':pin(OWN/'complete-named-review-decision-input-payload.json'),'decision':pin(OWN/'plan74.json'),'last_write_contract':'THIS lease.final.json is the final owned write. No write after CLOSED_LAST; subsequent validation read-only.','writer_terminal_EXIT_contract':'EXIT0 immediately; external tool observes actual terminal exit','scope':'Prospective source-first plan only; no formal/source/PURIFIED/Exposition/VERIFIED/Goal credit.'}
    save('lease.final.json',lease)
    print(json.dumps({'actual_writer_PID':os.getpid(),'owned_files':lease['owned_files'],'run_sha256':run['run_sha256'],'lease':pin(OWN/'lease.final.json'),'EXIT':0},ensure_ascii=False))

def readonly():
    lease=read(OWN/'lease.final.json'); assert lease['status']=='CLOSED_LAST'
    for name,key in [('native.manifest.json','manifest'),('complete-named-review-decision-input-payload.json','complete_named'),('plan74.json','decision')]: assert pin(OWN/name)==lease[key]
    manifest=read(OWN/'native.manifest.json'); guard(manifest['owned_files'])
    actual={p.as_posix() for p in OWN.rglob('*') if p.is_file()}; expected={p['path'] for p in manifest['owned_files']}|{(OWN/'native.manifest.json').as_posix(),(OWN/'lease.final.json').as_posix()}
    assert actual==expected and len(actual)==lease['owned_files']
    latest=(OWN/'lease.final.json').stat().st_mtime_ns; assert all(Path(p).stat().st_mtime_ns<=latest for p in actual)
    run=read(OWN/'run.json'); assert logical(run)==run['run_sha256']==lease['run_sha256']==manifest['run_sha256']; guard(run['inputs'])
    source=read(OWN/'source.regions74.json'); b=PRIMARY.read_bytes(); assert sha(b)==EXPECTED
    for row in source['regions']: assert b[row['RAW_start_inclusive']:row['RAW_end_exclusive']]==Path(row['literal_slice']['path']).read_bytes()
    k=ctypes.windll.kernel32; handle=k.OpenProcess(0x1000,False,lease['actual_last_writer_PID']); gone=not bool(handle)
    if handle:
        code=ctypes.c_ulong(); assert k.GetExitCodeProcess(handle,ctypes.byref(code)); k.CloseHandle(handle); gone=code.value!=259
    assert gone
    print(json.dumps({'actual_external_readonly_PID':os.getpid(),'terminal_EXIT':0,'writer_PID':lease['actual_last_writer_PID'],'writer_exited':gone,'owned_files':len(actual),'finite_inputs':len(run['inputs']),'wholelogicalrun_sha256':run['run_sha256'],'lease':pin(OWN/'lease.final.json')},ensure_ascii=False))

if __name__=='__main__':
    mode=sys.argv[1]
    if mode=='build': build()
    elif mode=='launch': raise SystemExit(launch())
    elif mode=='close': close()
    elif mode=='readonly': readonly()
    else: raise ValueError(mode)
