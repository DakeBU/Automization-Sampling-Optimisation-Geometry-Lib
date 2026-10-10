import hashlib, json, os, pathlib, re, sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT = pathlib.Path('E:/Samplinglib')
BASE = ROOT/'runs/20261007-companion-priority/pbps-real-complex-lift-preproof60'
OUT = BASE/'independent-preproof60'
OUT.mkdir(exist_ok=True)
def sha(b): return hashlib.sha256(b).hexdigest()
def rel(p): return p.relative_to(ROOT).as_posix()
def pin(p):
    b=p.read_bytes(); l=b.replace(b'\r\n',b'\n')
    return dict(path=rel(p),bytes=len(b),lf_bytes=len(l),raw_sha256=sha(b),lf_sha256=sha(l))
def write(n,x):
    p=OUT/n; p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n'); return pin(p)
inputs=[]
def capture(p):
    p=ROOT/p; b=p.read_bytes(); i=len(inputs); d=OUT/'inputs'; d.mkdir(exist_ok=True)
    a=d/f'{i:02d}-{p.name}.raw.snapshot'; a.write_bytes(b)
    z=d/f'{i:02d}-{p.name}.LF.snapshot'; z.write_bytes(b.replace(b'\r\n',b'\n'))
    inputs.append(dict(original=pin(p),raw_snapshot=pin(a),lf_snapshot=pin(z)))
    return b
scout='runs/20261007-companion-priority/pbps-centered-defect59/next-root-source-scout60/'
primary_objects=json.loads(capture(scout+'primary.required-objects.json'))
capture(scout+'next-edge.source-contract.json'); capture(scout+'run.json'); capture(scout+'lease.json')
supppath='runs/20261007-companion-priority/pbps-centered-defect-preproof59/independent-source-topology59/primary.supplemental-context.json'
supp=json.loads(capture(supppath))
primary=ROOT/primary_objects['primary']['path']; raw=primary.read_bytes()
assert pin(primary)==primary_objects['primary']
regions=list(primary_objects['regions'])
select=['S1.p1','S2.E6','S2.E7','A2.SS1.p1','A2.SS1.p2','A2.SS1.p3','A2.E8','A3.SS1.p2']
regions += [x for x in supp['exact_regions'] if x['id'] in select]
assert len(regions)==22 and len({x['id'] for x in regions})==22
qualified=[]
for x in regions:
    b=raw[x['start_utf8_byte']:x['end_utf8_byte_exclusive']]
    assert len(b)==x['slice_bytes'] and sha(b)==x['slice_sha256']
    p=OUT/'inputs'/f"primary-{x['id']}.raw.html"; p.write_bytes(b)
    qualified.append(dict(**x,original_primary=pin(primary),snapshot=pin(p)))
write('primary.exact-regions.json',dict(primary=pin(primary),regions=qualified,scope='22 bounded regions; exact literal primary bytes independently rechecked; full primary not copied'))
# Source-first reconstruction used the previously closed scout and its frozen literal source
# texts before header reads; this new extraction is an exact-byte readback, not a new source verdict.
spec={
'S1.p1':[('NODE','model','Normalized Gibbs target, global C2 and both Hessian bounds, 0<alpha<=beta; actual original binders'),('EXCLUDED','main','Main-result and complexity claims are not this prerequisite')],
'S2.E6':[('NODE','joint','Normalized joint density exp(-V(x)-||x-y||²/(2 eta)); proportionality resolved internally')],
'S2.E7':[('NODE','joint','Independent X~mu,Z standard Gaussian; Y=X+sqrt(eta) Z, actual J and nu')],
'A2.E1':[('NODE','P','Conditional-expectation projection on joint real L2, equalities of AE classes')],
'A2.E2':[('NODE','macro','ran(P) consists of y-only classes; exact scalar marginal adapter M'),('NODE','P','ker(P)=ran(I-P) is the conditional-mean-zero microscopic subspace')],
'A2.E3':[('NODE','blocks','Four blocks PTP,PTPperp,PperpTP,PperpTPperp; target/source subscript orientation')],
'A2.E4':[('NODE','U','Actual pullback reflection (x,y)->(x,2x-y)')],
'A2.E5':[('NODE','D','Printed UperpP*UperpP=I-UPP² derived from U²=I; retained source edge, not the selected scalar proof'),('EXCLUDED','crossblock','Second printed identity UperpP*Uperpperp=-UPP UperpP* is not claimed by the lift')],
'A2.E9':[('NODE','T','Scalar macro T is E[f(Yminus)|Yplus=y] on real marginal L2'),('EXCLUDED','micronorm','Squared microscopic conditional-variance formula is upstream context; no new microscopic operator identity here')],
'A4.SS1':[('NODE','realL2','D1: real AE equivalence classes, integral fg inner product, norm, probability convention'),('EXCLUDED','center','D2: mean-zero L2 subspace not a new conclusion or premise here'),('NODE','P','Closed subspace, orthogonal complement and bounded orthogonal projection conventions'),('NODE','T','Bounded operators, adjoints, selfadjointness and contraction conventions'),('NODE','U','Onto norm-preserving unitary; selfadjoint involution is unitary, parent source route'),('NODE','D','D3: nonnegative quadratic-form convention for selfadjoint operators; positivity background'),('EXCLUDED','CFC','Spectral theorem, bounded Borel calculus and spectral projections are not constructed'),('EXCLUDED','root','Unique nonnegative real square root remains the next boundary'),('NODE','S','D4: preserving Markov kernel acts by integration and gives L2 contraction'),('NODE','T','Constants fixed under a preserving Markov operator; inherited actual parent, not separately re-exported'),('EXCLUDED','density','Adjoint density evolution and chi²=D5 are unclaimed'),('EXCLUDED','mixing','Centered adjoint norm/chi² contraction is unclaimed')],
'A2.E10':[('NODE','root-demand','B10 motivates the all-macro positive real root of I-UPP²; no eta prefactor'),('EXCLUDED','root','Actual Gamma construction/equality on the full macro space is not this lift theorem')],
'A2.E11':[('EXCLUDED','root','Gamma²=UperpP*UperpP is future root/adapter integration'),('EXCLUDED','micronorm','||UperpP f||=||Gamma f|| for all macro f is future consumer')],
'A3.E4':[('EXCLUDED','sharp','C4 sharp centered rho contraction already provided by58; unused in generic/all-macro complexification')],
'A2.E12':[('EXCLUDED','constants','rho=(1-alpha eta)/(1+alpha eta), gamma=2sqrt(alpha eta)/(1+alpha eta); no centered root-gap conclusion')],
'A2.E15':[('EXCLUDED','center-root','B15 Loewner Gamma>=gamma I on centered macro space remains open')],
'A2.E16':[('EXCLUDED','polar','B16 bounded centered Gamma inverse, polar isometry and V*V=I remain open')],
'A2.SS2.p5':[('EXCLUDED','polar','Centered inverse/polar, microscopic magnitude/direction and following half-turn claim are unclaimed')],
'A2.SS1.p1':[('NODE','joint','Target real joint Hilbert space and B1/B2 projection/decomposition conventions'),('EXCLUDED','dynamics','Full ideal PBPS chain, conditional half-turn branch and induced full K are not this source consumer')],
'A2.SS1.p2':[('NODE','blocks','Block orientation and domains HrHmacro/Hmicro; same printed B3 convention')],
'A2.SS1.p3':[('NODE','U','Selfadjoint unitary reflection and selfadjoint contractive macro compression'),('NODE','D','Printed B5 derivation uses U²=I and joint projection block multiplication; retained, not asserted completed by scalar positivity'),('EXCLUDED','crossblock','Other crossblock identity is unclaimed')],
'A2.E8':[('NODE','joint','Yplus=X+sqrt(eta)Z and Yminus=X-sqrt(eta)Z; actual Lambda is their law')],
'A3.SS1.p2':[('NODE','S','Normalized every-y reflected conditional density exp(-V((y+u)/2)-||y-u||²/(8 eta))'),('EXCLUDED','weakH1','Score definition, differentiating normalized density and gradient covariance C1 are not new claims')]
}
coverage=[]
for x in regions:
    assert x['id'] in spec
    for j,(status,node,description) in enumerate(spec[x['id']]):
        coverage.append(dict(id=f"{x['id']}:{j+1}",region_id=x['id'],classification=status,target=node,description=description,primary_slice_sha256=x['slice_sha256']))
write('source.coverage.json',dict(status='independent bounded extraction for preproof statement review; no postproof source acceptance',regions=22,items=coverage,node_items=sum(x['classification']=='NODE' for x in coverage),excluded_items=sum(x['classification']=='EXCLUDED' for x in coverage)))
nodes=[('model','printed original model'),('joint','printed Gaussian augmentation and actual reflected pair'),('realL2','printed real Hilbert conventions'),('P','printed orthogonal conditional projection'),('macro','printed all-macro marginal identification'),('blocks','printed block convention'),('U','printed reflection involution'),('T','printed scalar macro conditional action'),('D','printed nonnegative squared defect'),('S','printed reflected conditional density'),('root-demand','printed B10/B11 future demand'),('parent59','ASTIS compiled genuine scalar T and positive D; reused parent, no new proof credit'),('lift','ASTIS attributed real-to-complex completion, presently unproved candidate'),('actual-lift','ASTIS actual consumer, presently unproved candidate')]
edges=[('model','joint','source definition'),('joint','P','source definition'),('P','macro','source definition'),('realL2','P','source convention'),('P','blocks','source block convention'),('joint','U','source reflection'),('U','D','printed U²=I block proof'),('P','D','printed joint projection block proof'),('blocks','D','printed B5 block proof'),('macro','T','printed marginal identification'),('joint','S','printed conditional law'),('S','T','source conditional action'),('D','root-demand','printed positive-root demand'),('T','parent59','ASTIS scalar adapter, separate from printed block proof'),('S','parent59','ASTIS actual representative/normalization adapter'),('parent59','actual-lift','planned producer consumption, not yet Lean proof'),('lift','actual-lift','planned generic interface use, not yet Lean proof')]
write('source.graph.json',dict(status='preproof independently reconstructed topology; not formal Lean edges or postproof proof coverage',source_read_order='closed scout exact primary texts read first, then candidate/header; raw primary slice recheck now; candidate metadata incidentally exposed before this file was written',nodes=[dict(id=a,kind=b) for a,b in nodes],edges=[dict(parent=a,child=b,kind=c) for a,b,c in edges],route_separation='Printed B5 U/P/block proof retained. Planned ASTIS route is verified59 actual scalar positivity -> generic canonical complex lift -> actual consumer. Complexification is not printed in PBPS. No CFC/root proof is inserted into source graph.'))
candidate=json.loads(capture(rel(BASE/'statement-candidate.json')))
headers=[]; probes=[]
for i in range(2):
    hb=capture(rel(BASE/f'header{i}.lean')); pb=capture(rel(BASE/f'elab{i}.lean'))
    headers.append(pin(BASE/f'header{i}.lean')); probes.append(pin(BASE/f'elab{i}.lean'))
    assert headers[-1]['raw_sha256']==candidate['headers'][i]['raw_sha256']
    assert probes[-1]['raw_sha256']==candidate['type_probes'][i]['raw_sha256']
    ht=hb.decode().replace('\r\n','\n').rstrip(); pt=pb.decode().replace('\r\n','\n').rstrip()
    decl=re.sub(r'^theorem \w+\n','#check (fun\n',ht,count=1).replace(' :\n    let',' =>\n    let',1)+' : _)'
    assert pt[pt.index('#check (fun'):]==decl, f'probe {i} exact full proposition reconstruction mismatch'
receipts=[]
for folder in ['elab-generic','elab-actual']:
    rec=json.loads(capture(rel(BASE/folder/'receipt.json')))
    for stream in ['stdout','stderr']:
        capture(rec[stream]['path']); assert pin(ROOT/rec[stream]['path'])['raw_sha256']==rec[stream]['raw_sha256']
    assert rec['exit_code']==0 and rec['terminal_closed'] and rec['actual_foreground_pid']>0
    receipts.append(dict(folder=folder,actual_pid=rec['actual_foreground_pid'],exit_code=rec['exit_code'],scope='Exact Prop-valued full expression TYPE elaboration only; no theorem body, proof or mathematical closure',unused_warnings='hD or all original source hypotheses remain forall binders in printed Pi type; do not remove'))
capture('AutoSamplingTheory/ExampleCases/ProximalBPS/CenteredDefectOperator.lean')
capture('lake-manifest.json'); capture('lean-toolchain')
# Bounded support spans, not whole-library scans.
api=[]
for name,a,b in [('.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Positive.lean',261,321),('.lake/packages/mathlib/Mathlib/MeasureTheory/Function/LpSpace/Basic.lean',785,831),('AutoSamplingTheory/ExampleCases/ProximalBPS/CenteredDefectOperator.lean',12,72),('docs/companion-papers-handoff.md',1,55)]:
    p=ROOT/name; full=p.read_bytes(); lines=full.replace(b'\r\n',b'\n').splitlines(keepends=True); fragment=b''.join(lines[a-1:b]); snap=OUT/'inputs'/f'api-{len(api):02d}-{p.name}.L{a}-{b}.LF.snapshot'; snap.write_bytes(fragment)
    api.append(dict(original=pin(p),start_line=a,end_line=b,snapshot=pin(snap)))
execution=json.loads((ROOT/'website/content/samplewiki_companion_frontiers.json').read_text(encoding='utf-8'))['execution']
write('execution.snapshot.json',execution)
write('input.manifest.json',dict(qualified_inputs=inputs,primary=pin(primary),primary_regions_manifest=pin(OUT/'primary.exact-regions.json'),api_LF_spans=api,bounded_scope='No compiler, no canonical mutation, no broad scans, no root math/source verdict reused as current verdict'))
review=dict(status='ACCEPTED_PREPROOF_STATEMENT_AND_BINDER_SCOPE_ONLY',header0_verdict='equivalent-after-elaboration',header1_verdict='equivalent-after-elaboration',exact_headers=headers,exact_type_probes=probes,elaboration=receipts,blocking_deltas=[],repairs=[],source_version='2609.06905v1',attribution='ASTIS background completion; not a printed PBPS theorem',
    seven_slots={
      'objects':'Generic D is a bounded REAL endomorphism of Lp real2mu; canonical iota/re/im/conj are fixed real continuous linear compLpL maps; Dc is a bounded COMPLEX endomorphism. Actual T is on real marginal nu and D is typed I-T*T.',
      'domains':'Generic arbitrary measurable Omega and arbitrary measure mu; no sigma-finite/finite/probability assumption. Actual E finite real Hilbert and Borel; L2 remains potentially infinite dimensional. AE quotient equality throughout; rank0/subsingleton allowed.',
      'quantifiers':'Generic forall mu,D,hD and all real u/complex g, exists Dc. Actual original forall E,V,alpha,beta,eta with source hypotheses; exists every-y normalized S then actual T then Dc. T action only nu-AE per u, not pointwise all y. Fixed conjugation range iff exists u is exact quotient-class equality.',
      'assumptions':'Generic IsPositive D explicitly includes symmetry and nonnegative real quadratic form, legitimate input of the reusable background lemma. Actual no caller S/T/D/selfadjoint/positivity/probability/CFC/root witness: all are conclusions of verified59. All original C2/two global Hessians/positive alpha ordered beta/positive capped eta binders retained.',
      'conclusion':'Norm-preserving real embedding, fixed-real range, positive canonical complex Dc formula, intertwining Dc iota=iota D, pointwise conjugation commutation. Actual also reproduces genuine kernel, invariant reflected pair marginals and scalar mean-preserving selfadjoint contraction. No root conclusion.',
      'scopes':'All-macro scalar marginal, no centered restriction claimed. Every-y S density is normalized tilted probability law from parent. Integral T representative nu-AE: conditional integrability follows from parent L2/L1 and disintegration, not a default-integral certificate. Parent U/M uniquely identify the same T through AE equality; parent witnesses need not be duplicate public outputs.',
      'constants':'Conditional reflection half midpoint and denominator 8 eta, Gaussian sqrt eta and reflection 2x-y exact. Defect I-T² has no eta prefactor. beta eta<=1 retains alpha eta=1. No gamma/rho/delta root claim and no division requiring strict alpha eta<1.'},
    mathematical_statement_check=['For g=iota a+I*iota b, real-linearity of D makes the specified formula complex-linear; boundedness follows from bounded canonical maps and D. This is design reasoning, not a Lean proof.', 'Positivity requires real symmetry to cancel imaginary cross terms; IsPositive includes it. Real quadratic form splits into <Da,a>+<Db,b> >=0. No missing symmetry assumption.', 'Real embedding is isometric for arbitrary measure by scalar abs(ofReal x)=abs x; fixed conjugation implies imaginary part zero AE and g=iota(Rg). No finite measure or probability needed.', 'Actual consumer may obtain S,T and positive I-T² directly from producer59, then apply the generic lemma. This is a planned proof graph, not completed60 evidence.'],
    actual_same_identity='The forall-y normalized S law fixes the kernel. Equality T u=AE integral_S u for all u fixes T as a continuous map by Lp extensionality; thus the parent59 choice and any stated witness are the SAME scalar operator, not an arbitrary replacement.',
    definition_adapters=['volume.tilted(-V) normalizes the density, finite positive partition derived from strong convexity under original assumptions; J is exact independent Gaussian augmentation.', 'Lp and compLpL transport scalar maps on AE classes; R,Q,C are real-linear, iota real-linear isometry; C is not asserted complex-linear.', 'IsPositive uses REAL PART of the complex quadratic form and symmetry, hence compatible with positive operator semantics; complete L2 gives selfadjointness without finite dimension.'],
    source_omitted_detail='D1 cites the spectral theorem in prose without an explicit bibliography item at that sentence. A real positive root is asserted as standard background but not constructed by this candidate; complexification supplies an ASTIS prerequisite rather than source-printed proof.',
    excluded=['real positive Gamma existence/uniqueness/descent','B10 exact full-macro Gamma and B11 microscopic norm integration','B15 centered root order and B16 inverse/polar','full weighted weakH1 and normalized-density gradient route','PBPS event dynamics/nonexplosion/invariance/full K','mixing, implementation errors, costs, actual-input PBPS/SPHMC composition','source-blind decoder acceptance, PROVED_LOCAL, VERIFIED, paper or Goal completion'],
    input_chronology='Frozen primary quoted regions and source-only scout were read before candidate headers. Current exact snapshot bytes are revalidated in this foreground native reader. Candidate metadata incidental exposure before new graph serialization is disclosed; no60 proof bodies exist/read. Parent59 header and incidental beginning of already-proved body only serve actual producer identification.',
    source_topology_status='Independent preproof extraction and source boundary review; root must separately admit the graph, and later actual proof coverage is not implied.',
    no_compiler_by_reviewer=True)
write('statement.review.json',review)
write('named-preproof-source.payload.json',dict(kind='independent60-preproof-source-statement',review=pin(OUT/'statement.review.json'),source_graph=pin(OUT/'source.graph.json'),coverage=pin(OUT/'source.coverage.json'),primary=pin(OUT/'primary.exact-regions.json'),headers=headers,remaining_boundary=review['excluded']))
print(json.dumps(dict(author_pid=os.getpid(),input_pairs=len(inputs),regions=len(regions),coverage_items=len(coverage),verdict=review['status'],receipts=receipts),ensure_ascii=True))
