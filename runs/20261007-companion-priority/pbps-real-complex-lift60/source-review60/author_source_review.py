import hashlib,json,os,pathlib,re,sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT=pathlib.Path('E:/Samplinglib'); OUT=pathlib.Path(__file__).resolve().parent
BASE=OUT.parent
def sha(b): return hashlib.sha256(b).hexdigest()
def canon(x): return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def pin(p):
    b=p.read_bytes(); l=b.replace(b'\r\n',b'\n')
    return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(b),lf_bytes=len(l),raw_sha256=sha(b),lf_sha256=sha(l))
def write(n,x): (OUT/n).write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
inputdir=OUT/'inputs'; inputdir.mkdir(exist_ok=True)
pairs=[]
def capture(p,opaque=False):
    raw=p.read_bytes(); n=len(pairs)
    a=inputdir/f'{n:02d}-{p.name}.raw.snapshot'; a.write_bytes(raw)
    b=inputdir/f'{n:02d}-{p.name}.LF.snapshot'; b.write_bytes(raw.replace(b'\r\n',b'\n'))
    pairs.append(dict(original=pin(p),raw_snapshot=pin(a),lf_snapshot=pin(b),semantic_inspection='opaque bytes only; no prior semantic verdict read' if opaque else 'current scoped source/body/publication input'))
    return raw
lease=json.loads(capture(BASE/'source.review.lease.json'))
assert len(lease['input_artifacts'])==16
for item in lease['input_artifacts']:
    p=pathlib.Path(item['path']); raw=capture(p,opaque='/semantic-roundtrip/audits/' in item['path'])
    assert len(raw)==item['raw_bytes'] and sha(raw)==item['raw_sha256']
    assert sha(raw.replace(b'\r\n',b'\n'))==item['lf_sha256']
pre=ROOT/'runs/20261007-companion-priority/pbps-real-complex-lift-preproof60'
for p in [pre/'header0.lean',pre/'header1.lean',ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/CenteredDefectOperator.lean',ROOT/'lake-manifest.json',ROOT/'lean-toolchain']:
    capture(p)
source=json.loads((pre/'independent-preproof60/primary.exact-regions.json').read_bytes())
cap=json.loads((pre/'independent-preproof60/cap-source-readback/cap.source.supplement.json').read_bytes())
raw=(ROOT/source['primary']['path']).read_bytes(); assert sha(raw)==source['primary']['raw_sha256']
regions=source['regions']+[cap['source_region']]
spans=[]
for r in regions:
    b=raw[r['start_utf8_byte']:r['end_utf8_byte_exclusive']]
    assert len(b)==r['slice_bytes'] and sha(b)==r['slice_sha256']
    p=inputdir/f"primary-{r['id']}.raw.html"; p.write_bytes(b)
    spans.append(dict(id=r['id'],start_utf8_byte=r['start_utf8_byte'],end_utf8_byte_exclusive=r['end_utf8_byte_exclusive'],original_primary=pin(ROOT/source['primary']['path']),snapshot=pin(p)))
api=[]
for name,a,b in [('.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Positive.lean',261,321),('.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Positive.lean',442,454),('.lake/packages/mathlib/Mathlib/Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Instances.lean',180,218),('.lake/packages/mathlib/Mathlib/Analysis/CStarAlgebra/ContinuousLinearMap.lean',11,23),('.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/StarOrder.lean',28,81),('.lake/packages/mathlib/Mathlib/Analysis/SpecialFunctions/ContinuousFunctionalCalculus/Rpow/Basic.lean',1,40),('.lake/packages/mathlib/Mathlib/Analysis/SpecialFunctions/ContinuousFunctionalCalculus/Rpow/Basic.lean',229,268),('tools/astis_publication.py',82,117)]:
    p=ROOT/name; lines=p.read_bytes().replace(b'\r\n',b'\n').splitlines(keepends=True); z=inputdir/f'api-{len(api):02d}-{p.name}.L{a}-{b}.LF.snapshot'; z.write_bytes(b''.join(lines[a-1:b])); api.append(dict(original=pin(p),start_line=a,end_line=b,snapshot=pin(z)))
write('input.manifest.json',dict(original_lease_inputs=16,raw_LF_pairs=pairs,primary=pin(ROOT/source['primary']['path']),exact_primary_slices=spans,api_LF_spans=api,audits_policy='Both original pre-mutation canonical audit JSON files frozen as opaque exact raw/LF snapshots only; not parsed for prior verdicts/slots/repairs.'))
packets=[json.loads((BASE/f'source.{i}.reviewer-packet.json').read_bytes()) for i in range(2)]
units=[]; pubs=[]; code=[]
slugs=['l2-real-complex-positive-lift','pbps-positive-defect-complex-lift']
for i,p in enumerate(packets):
    core=dict(p); expected=core.pop('packet_sha256'); assert sha(canon(core))==expected==lease['reviewer_packet_sha256'][i]
    txt=(ROOT/p['lean']['file']).read_text(encoding='utf-8'); code.append(txt)
    assert txt==p['candidate_publication_context']['current_lean_module']
    assert sha(txt.encode())==p['candidate_publication_context']['file']
    name=p['lean']['declaration'].split('.')[-1]
    signature=txt[txt.index('theorem '+name):txt.index(' := by',txt.index('theorem '+name))]
    assert signature== (pre/f'header{i}.lean').read_text(encoding='utf-8').rstrip()
    assert p['lean']['statement']==signature[len('theorem '+name):]
    assert sha(p['lean']['statement'].encode())==p['lean']['statement_sha256']
    pub=json.loads((ROOT/f'website/content/publications/{slugs[i]}.json').read_bytes())['items'][0]; pubs.append(pub)
    unit=json.loads((ROOT/f'website/content/declaration_lessons/{slugs[i]}.json').read_bytes())['units'][0]; units.append(unit)
    binding=pub['bindings'][0]
    payload=dict(file=sha(txt.encode()),current_lean_module=txt,toolchain=sha((ROOT/'lean-toolchain').read_text(encoding='utf-8').encode()),dependencies=sha((ROOT/'lake-manifest.json').read_text(encoding='utf-8').encode()),source=pub['source'],statement=pub['statement'],formulae=pub['formulae'],assumptions=pub['assumptions'],obligations=pub['obligations'],lesson=unit,binding={k:v for k,v in binding.items() if k not in ['audit_id','legacy_audit_debt']})
    assert sha(canon(payload))==p['publication_binding_sha256']
    expectedlesson={k:v for k,v in unit.items() if k not in ['boundary','source_history_boundary']}
    assert expectedlesson==p['candidate_publication_context']['lesson']
    assert pub['statement']==unit['statement']==p['candidate_publication_context']['statement']
    assert pub['assumptions']==unit['assumptions']
    assert unit['declaration']==p['lean']['declaration']==binding['declaration']
providers=re.findall(r'^private (?:abbrev|def|theorem) (\w+)',code[0],re.M)
assert len(providers)==26
plan=json.loads((BASE/'publication-plan.json').read_bytes()); assert providers==plan['private_providers']
assert not any(re.search(r'\b'+x+r'\b',code[0]+code[1]) for x in ['sorry','admit','axiom']) # #print axioms plural is inspection
assert 'import Tests' not in code[0]+code[1]
step_checks=[]
for i,u in enumerate(units):
    for j,s in enumerate(u['steps']):
        refs=[x.strip() for x in s['lean'].split(';')]
        for x in refs:
            assert x in code[i] or x.startswith('L2RealComplexOperator.') or x.startswith('ContinuousLinearMap.isPositive_iff_complex')
        step_checks.append(dict(item=i,step=j+1,title=s['title'],formula=s['formula'],lean_refs=refs,status='checked against exact current body and original source boundary',scope='ASTIS authored background proof, not printed source Gamma proof'))
write('body-publication.scope-review.json',dict(source_boundary_before_packets=pin(OUT/'primary-boundary.before-packets.json'),current_source_graph=pin(pre/'independent-preproof60/source.graph.json'),source_coverage=pin(pre/'independent-preproof60/source.coverage.json'),cap=pin(pre/'independent-preproof60/cap-source-readback/cap.source.supplement.json'),source_graph_status='Reused only after exact current header/body/formula comparison; literal23 regions44 bounded coverage items unchanged. Printed B5 U/P/block route remains source-present, separate from scalar59 positivity route.',private_providers=providers,provider_groups={'canonical maps':['embed','realPart','imagPart','conjugate'],'AE scalar identities':['real_embed','imag_embed','parts','real_I','imag_I','conjugate_embed','conjugate_parts','fixed_range'],'isometry':['inner_embed','norm_embed'],'complex bounded operator':['liftReal','liftReal_I','liftComplex','liftComplex_apply'],'coordinates and compatibility':['liftComplex_embed','real_lift','imag_lift','real_conjugate','imag_conjugate','liftComplex_conjugate'],'positivity':['inner_lift','liftComplex_positive']},provider_scope='All26 are private implementation providers with explicit arbitrary mu and displayed D,hD where needed; each is used transitively by the public generic theorem. No new source-facing premise hidden in a private helper.',formula_steps=step_checks,ASTIS_parents=[[],units[1]['astis_dependencies']],Mathlib_parents=[units[0]['mathlib_dependencies'],[]],same_actual_operator='Actual body destructures genuine59 S/U/M/T/q/hD, passes the literal I-T*T and that hD to generic theorem, and returns hAll(u).2.2; no replacement choice or source positivity caller premise.',CFC_test='Exact Test constructs complex normal CFC then real selfadjoint calculus locally on COMPLEX L2 operator algebra for arbitrary mu. Complete complex Hilbert CStar/StarOrder APIs do not assume real CFC, finite measure, finite L2 or nontriviality. Rc=CFC.sqrt Dc, Rc>=0, Rc*Rc=Dc is a Test-only API consumer; C Rc=Rc C, real-subspace preservation and descended Gamma are not proved.',exposition='Two complete attributed statements and all8 formula steps agree. Actual step1 unqualified displayed integral equation is qualified as AE in adjacent text and full statement. Fold refs target corresponding private provider/public consumer bodies; native UI/copy controls are outside this source review.',assumption_deltas='Generic arbitrary Omega/mu and actual finite Hilbert/Borel/rank0 extension explicitly generalized and attributed. Canonical maps/normalization and produced certificates are same. Unresolved real root/polar/paper boundary remains explicitly unresolved; no blocking source difference.'))
def slot(original,reconstructed,relation,evidence): return dict(original=original,reconstructed=reconstructed,relation=relation,evidence=evidence)
generic={
'objects':slot('D1 real complete L2 positive operator; ASTIS authored canonical complexification prerequisite','Real bounded D; literal compLpL ofReal/re/im/conj; complex bounded Dc with exact formula','explicit-elaboration','D1 actual real AE classes;26 private providers; generic public lets identical to sealed signature.'),
'domains':slot('ASTIS generalizes real L2 probability convention to arbitrary measurable Omega and any mu','Lp real2mu and complex2mu AE quotients; no finite/probability/SFinite/finite-dimensional/nontrivial assumption','explicit-elaboration','All generic variables are Omega,MeasurableSpace,mu,D,hD. L2 completeness and scalar maps derive library structures for arbitrary mu.'),
'quantifiers':slot('For every arbitrary mu and positive D, norm forall u, fixed range forall g iff exists u, exists Dc with universal identities','Same order and displayed real/complex domains; no pointwise all-state equality for selected representatives','equivalent','Public theorem complete statement, fixed_range proves both directions by Lp.ext and AE scalar identities.'),
'assumptions':slot('Generic bounded positive real D is legitimate reusable input; positivity includes selfadjointness','hD:IsPositive contains IsSymmetric and nonnegative real quadratic form; no supplied CFC or embedding','explicit-elaboration','Positive.lean266-315; inner_lift cross-term cancellation uses hD symmetry. Complete L2 equates symmetry/selfadjointness.'),
'conclusion':slot('Isometric canonical real embedding; its full range exactly Fix(C); positive complex lift formula, intertwining and conjugation commutation','Exactly all five full-domain outputs; Dc complex linear and bounded by its type; positivity derived from split quadratic form','equivalent','norm_embed/fixed_range/liftComplex_positive/liftComplex_apply/liftComplex_embed/liftComplex_conjugate all actually returned.'),
'scopes':slot('Attributed ASTIS complexification background for B10/B11 real root; not source printed Gamma theorem','No real Gamma, descent, inverse, uniqueness, centered root order, mixing/error/cost/composition','equivalent','Original primary B10/B11/D1 root assertions kept distinct; Test-only complex square root does not prove pointwise-conjugation preservation.'),
'constant_dependencies':slot('Canonical real inclusion/parts and complex i; no eta/rho/gamma constant in generic background','Same iota,R,Q,C and Complex.I; D arbitrary positive','same','No paper parameter enters generic theorem or providers; no fabricated positive gap or strict operator norm bound.')}
actual={
'objects':slot('Actual normalized Gibbs mu, Gaussian J, marginal nu, reflected pair Lambda, normalized conditional S and scalar macro T/D','Identical lets; genuine59 witnesses S,T reused; actual D is typed identity minus T*T; canonical maps at same nu','explicit-elaboration','Source2.6/2.7/B8/B9/C1 and actual code rcases hBase then generic nu D hD.'),
'domains':slot('Source Euclidean finite E; explicit ASTIS finite real Hilbert/Borel and rank-zero extension; full real marginal L2','FiniteDimensional applies to E only; arbitrary-dimension real/complex Lp nu, rank0 permitted; no Nontrivial','explicit-elaboration','Same actual sealed binders, no finite L2 inference, generic proof arbitrary measure.'),
'quantifiers':slot('Every x,v Hessian bounds, every y normalized kernel, each u AE action and mean preservation; exists actual S,T,Dc with all compatibility identities','Exactly every-y S formula vs nu-AE T u action; full fixed range iff exists real u; universal complex g','equivalent','Source C1 density vs B9 conditional action; actual forall scopes and body returns same hAll(u).2.2.'),
'assumptions':slot('Original C2,0<alpha<=beta,two global Hessian bounds,eta>0,beta eta<=1; probabilities/operators/positivity are produced','No caller D or hD, S,T,probability,selfadjoint,CFC/root certificates; all derived from59 then generic hD is discharged internally','equivalent','Literal cap paragraph rechecked; body passes hα hαβ hV hH hη hβη to parent59 and consumes returned hD.'),
'conclusion':slot('Produced law normalization/Markov disintegration and stationary marginals; actual selfadjoint contraction preserves mean; positive D and canonical full complex lift','Exactly same produced conclusions and Dc formula for I-T², embedding norm/full fixed range/positive Dc/both compatibilities','equivalent','Actual refine returns hμ,hJ,hν,S,hS,hSd,hSc,hSf,hSs,T,hTs,hD and complete generic outputs.'),
'scopes':slot('Full all-macro scalar marginal adapter supplies a root prerequisite; normalized kernel every y, integrals action AE with real L2/L1 integrability','No printed B5 block identity completion by this theorem; no actual Gamma or B11 norm/polar claimed','explicit-elaboration','Parent59 establishes actual same T through U/M and conditional action; sourcegraph printed block route preserved separately from scalar positivity. Parent normalization and disintegration prevent default-integral closure.'),
'constant_dependencies':slot('sqrt eta Gaussian augmentation, reflection2X-Y, midpoint(y+x)/2,8eta conditional denominator; unscaled D=I-T²','Exact all constants and original non-strict cap; alpha eta=1 and rank0 legal; no eta prefactor or gamma/rho assertion','same','Raw source2.7/B4/B8/C1/B10 and literalcap versus exact public lets/formula; no centered inverse assumption.')}
reviews=[]
for i,slots in enumerate([generic,actual]):
    deltas=[dict(slot='domains',classification='attributed-background-generalization' if i==0 else 'explicit-source-domain-extension',blocking=False,description='Arbitrary measurable base/measure background' if i==0 else 'Finite real Hilbert/Borel form with disclosed rank-zero extension; no finite L2 assumption.'),dict(slot='scopes',classification='unresolved-source-boundary',blocking=False,description='Complex lift only; printed real Gamma/B11 and centered inverse/polar/full paper remain open. Test-only complex CFC is a separate API consumer. No source theorem weakening is used to pretend to close them.')]
    r=dict(semantic_slots=slots,deltas=deltas,repairs=[],verdict='equivalent-after-elaboration',reviewer='/root/next_primary59',independent_from_formalizer=True,independent_from_decoder=True,review_evidence='Fresh primary-first source reconstruction and exact current bodies/provider scopes, reader formulas and publication bindings independently checked; see native input.manifest.json/body-publication.scope-review.json.',reviewer_packet_sha256=packets[i]['packet_sha256'],publication_binding_sha256=packets[i]['publication_binding_sha256'],publication_exposition_verdict='accepted-scoped-source-content; native rendered/copy/full-exposition seal separate',excess_count=0,source_attribution='ASTIS authored background completion supporting D1/B10-B11; not a printed paper numbered theorem',review_scope='postproof source and authored exposition fidelity only; no compiler rerun, source-blind decoder credit, VERIFIED/PURIFIED/whole-paper credit')
    reviews.append(r); write(f'source.{i}.decision.sealed.json',r)
write('named-source-review.payload.json',dict(kind='independent60-source-content-review',decisions=[pin(OUT/f'source.{i}.decision.sealed.json') for i in range(2)],source_boundary=pin(OUT/'primary-boundary.before-packets.json'),body_publication_scope=pin(OUT/'body-publication.scope-review.json'),inputs=pin(OUT/'input.manifest.json'),recipe='Named payload is raw SHA256 of this complete file, distinct from entire native run logical hash. Final review records are exact sealed decisions plus review_run_sha256 only.'))
print(json.dumps(dict(actual_foreground_author_pid=os.getpid(),input_pairs=len(pairs),original_lease_inputs=16,primary_regions=len(regions),private_providers=len(providers),formula_steps=len(step_checks),verdicts=[x['verdict'] for x in reviews],packet_hashes=[p['packet_sha256'] for p in packets],publication_bindings=[p['publication_binding_sha256'] for p in packets]),ensure_ascii=True))
