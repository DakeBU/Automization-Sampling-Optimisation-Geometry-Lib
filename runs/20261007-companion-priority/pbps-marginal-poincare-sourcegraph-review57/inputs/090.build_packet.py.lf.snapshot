from pathlib import Path
import hashlib, json, re, sys
from datetime import datetime, timezone
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
SRC = ROOT / 'runs/20261007-companion-priority/phase-pbps-gamma-preread57'
SELF = 'content_self_sha256'
def digest(b): return hashlib.sha256(b).hexdigest()
def canonical(x): return json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')
def pin(p):
    b=p.read_bytes()
    return dict(path=p.relative_to(ROOT).as_posix(), bytes=len(b), raw_sha256=digest(b), lf_sha256=digest(b.replace(b'\r\n',b'\n')))
def native(p):
    x=json.loads(p.read_bytes()); expected=x[SELF]
    assert digest(canonical({k:v for k,v in x.items() if k != SELF})) == expected, p
    return x
def write(name,x):
    assert SELF not in x
    x[SELF]=digest(canonical(x))
    p=OUT/name; p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
    assert native(p)==x
    return pin(p)
def now(): return datetime.now(timezone.utc).isoformat()

class Tree(HTMLParser):
    def __init__(self,s):
        super().__init__(convert_charrefs=True); self.s=s; self.roots=[]; self.stack=[]; self.all=[]
        self.starts=[0]
        for m in re.finditer('\n',s): self.starts.append(m.end())
        self.feed(s); assert not self.stack
    def pos(self):
        l,c=self.getpos(); return self.starts[l-1]+c
    def handle_starttag(self,t,a):
        n={'tag':t,'attrs':dict(a),'start':self.pos(),'children':[], 'parent':self.stack[-1] if self.stack else None}
        (self.stack[-1]['children'] if self.stack else self.roots).append(n); self.all.append(n)
        if t in {'br','hr','img','meta','link','input','wbr','col'}: n['end']=self.pos()+len(self.get_starttag_text())
        else: self.stack.append(n)
    def handle_startendtag(self,t,a):
        self.handle_starttag(t,a)
        if self.stack and self.stack[-1]['tag']==t: self.stack.pop()['end']=self.pos()+len(self.get_starttag_text())
    def handle_endtag(self,t):
        assert self.stack and self.stack[-1]['tag']==t, (t,self.getpos())
        self.stack.pop()['end']=self.pos()+len('</'+t+'>')
    def handle_data(self,d):
        if self.stack: self.stack[-1]['children'].append(d)
def text(n):
    if isinstance(n,str): return n
    if n['tag']=='math': return n['attrs'].get('alttext','')
    return ' '.join(text(c) for c in n['children'])
def norm(n): return re.sub(r'\s+',' ',text(n)).strip()
def ancestor(n,cls):
    p=n['parent']
    while p:
        if cls in p['attrs'].get('class','').split(): return True
        p=p['parent']
    return False

def stage1():
    assert not (OUT/'source-only-freeze.json').exists(), 'Do not overwrite frozen source-first topology'
    OUT.mkdir(parents=True,exist_ok=True)
    write('lease.open.json',dict(schema_version=1,actor='/root/sourcegraph57',state='OPEN',opened_at=now(),compiler_started=False,proof_started=False,allowed_output_prefix=OUT.relative_to(ROOT).as_posix()))
    primary=native(SRC/'primary.contract.json'); addendum=native(SRC/'source.precision-addendum.json'); lease=native(SRC/'lease.json')
    assert lease['state']=='CLOSED' if 'state' in lease else lease.get('status')=='CLOSED'
    manifest=native(SRC/'source-anchor-manifest.json')
    anchors=manifest['anchors']; assert len(anchors)==21
    raw=(SRC/'primary-pbps.exactraw.snapshot.html').read_bytes()
    assert digest(raw)==manifest['raw_copy']['raw_sha256']
    source_pins=[pin(SRC/f) for f in ['primary.contract.json','source.precision-addendum.json','lease.json','source-anchor-manifest.json','primary-pbps.exactraw.snapshot.html','primary-pbps.crlf-to-lf.snapshot.html']]
    nodes=[]; coverage=[]; seen={}
    active={'S1.p1','S2.SS2','A4.SS2','A3.SS1'}
    exclusions={
      'S1.p2':'Pointer to main theorem parameter choices; no marginal-Poincare prerequisite.',
      'A2.SS1':'Operator/half-turn framework downstream of scalar marginal PI; definitions retained as separate context roots, not hypotheses of marginal PI.',
      'A2.SS3':'Modified L2 hypocoercivity and main theorem proof downstream of C.4; excluded from this bounded marginal PI delta.',
      'A3.SS2':'Conditional affine half-turn estimates; independent downstream analytic lane, excluded from marginal PI construction.',
      'A3.SS3':'Interpolation/half-turn and spectral-localization downstream lane; excluded from marginal PI construction.',
      'A4.SS1':'Hilbert/Markov/spectral conventions; separate context for Gamma, not marginal PI proof.',
    }
    for a in anchors:
        ident=a['id']; p=ROOT/a['exactraw']['path']; b=p.read_bytes(); assert pin(p)==a['exactraw']
        assert b==raw[a['source_start_utf8_byte']:a['source_end_utf8_byte_exclusive']]
        for key in ['exactraw','crlf_to_lf','math_alttext_text']:
            q=ROOT/a[key]['path']; assert pin(q)==a[key]; source_pins.append(pin(q))
        tree=Tree(b.decode('utf-8'))
        for n in tree.all:
            cl=n['attrs'].get('class','').split()
            kind=('external-citation' if n['tag']=='a' and 'ltx_cite' in cl else
                  'source-statement' if 'ltx_theorem' in cl else
                  'proof-container' if 'ltx_proof' in cl else
                  'display-equation' if 'ltx_equation' in cl else
                  'substantive-paragraph' if n['tag']=='p' and 'ltx_p' in cl else
                  'unnumbered-display' if n['tag']=='math' and n['attrs'].get('display')=='block' and not ancestor(n,'ltx_equation') else None)
            if kind is None: continue
            start=a['source_start_utf8_byte']+len(tree.s[:n['start']].encode('utf-8'))
            end=a['source_start_utf8_byte']+len(tree.s[:n['end']].encode('utf-8'))
            rid=n['attrs'].get('id') or f'byte-{start}-{end}'
            if rid in seen:
                assert seen[rid]==(start,end); continue
            seen[rid]=(start,end)
            s=norm(n); disposition='NODE'; reason='Source region within marginal-Poincare prerequisite/consumer slice.'
            if ident not in active:
                disposition='EXCLUDED'; reason=exclusions.get(ident,'Gamma/block/gap/half-turn source equation belongs to a separate source root or downstream theorem; no marginal PI prerequisite.')
            if ident=='S2.SS2':
                if any(v in s for v in ['prox}_{','proximal map convention','minimizer is unique','Definition 2.2','fresh randomness','Gibbs sampling alternates','scale \\eta controls','The convergence and query','Moreau']):
                    disposition='EXCLUDED'; reason='Proximal/RGO algorithm convention or complexity motivation; not required for Eq2.13/D.6 marginal PI.'
                if rid=='S2.E14': disposition='EXCLUDED'; reason='Reflection symmetry is separate operator root, not curvature/marginal PI prerequisite.'
                if rid=='S2.E15': disposition='EXCLUDED'; reason='Exact prox minimizer is analysis-only algorithm object, not marginal PI prerequisite.'
            if ident=='A4.SS2' and (rid=='A4.E7' or rid=='A4.SS2.p1.2'):
                disposition='EXCLUDED'; reason='D.7 Gaussian concentration/LSI consequences are not consumed by bounded marginal PI delta.'
            if ident=='A3.SS1':
                local=tree.s[:n['start']]
                c5=tree.s.find('id="A3.E5"')
                # The paragraph introducing C.5 starts the independent uniform negative-spectrum lane.
                marker=tree.s.find('It remains only')
                cutoff=marker if marker>=0 else c5
                if n['start']>=cutoff:
                    disposition='EXCLUDED'; reason='C.5-C.7 uniform negative-spectrum/Gamma-gap or C.8-C.9 derivative/weak-H1 extension lane; independent of marginal PI C.3 and norm C.4.'
                if kind=='proof-container':
                    disposition='EXCLUDED'; reason='Container spans included C.1-C.4 and excluded later lanes; every substantive child paragraph/display is classified individually.'
            record=dict(region_id=rid,anchor_container=ident,kind=kind,disposition=disposition,reason=reason,
                        primary_start_utf8_byte=start,primary_end_utf8_byte_exclusive=end,raw_sha256=digest(raw[start:end]),
                        lf_sha256=digest(raw[start:end].replace(b'\r\n',b'\n')),source_text=s)
            if disposition=='NODE': record['node_id']='pbps57:region:'+rid
            coverage.append(record)
    def node(i,kind,anchor,statement,boundary='Source-only assertion; no Lean admission'):
        nodes.append(dict(id='pbps57:'+i,kind=kind,source_anchor=anchor,statement=statement,boundary=boundary))
    node('standing','source-assumptions','S1.p1/Eq1.1; S2.SS2','R^d, V in C2, 0<alpha<=beta, global alpha I<=Hess V<=beta I; 0<eta<=1/beta.')
    node('actual-law','source-definition','S2.E6/E7/E8','X~normalized exp(-V), Z~N(0,I) independent, Y=X+sqrt(eta)Z; nu=pi_eta^Y=mu*N(0,eta I).')
    node('conditional-potential','source-definition-estimate','S2.E9/E10','V_y(x)=V(x)+||x-y||²/(2eta); alpha+eta^-1<=Hess V_y<=beta+eta^-1.')
    node('BE','external-citation','A4.SS2.p1.3/D.6; bibliography3 Chapters4/5','Bakry-Emery curvature criterion: m-strong logconcavity implies Var(f)<=m^-1 E||grad f||² for smooth f; source citation not locally proved.')
    node('BL','external-citation','D.3 proof bibliography3 Chapter4','Brascamp-Lieb on linear functions gives covariance upper bound from lower Hessian curvature.')
    node('CR','external-result','D.3 proof','Cramer-Rao location-family inequality gives covariance lower bound from upper Hessian curvature; smooth density/tail/IBP conditions implicit in source.')
    node('covariance','source-lemma','A4.Thmtheorem3/D.8/D.9; S2.E12','For m I<=Hess W<=L I, L^-1 I<=Cov(Z)<=m^-1 I; conditional Cov between eta/(1+beta eta) I and eta/(1+alpha eta) I.')
    node('differentiate-logdensity','source-proof-step','A4.SS2.SSS0.Px1.p1.1','Differentiate actual Gaussian-convolved marginal log-density; differentiation under integral, normalization, finite conditional moments and representative conventions remain analytic obligations.')
    node('D10','reused-equation','A4.E10','grad U_eta=eta^-1(y-E[X|Y=y]); Hess U_eta=eta^-1(I-Sigma_y), Sigma_y=eta^-1 Cov(X|Y=y).')
    node('marginal-curvature','source-proposition','S2.E13; A4.SS2.SSS0.Px1.p1.2','alpha/(1+alpha eta) I<=Hess U_eta<=beta/(1+beta eta) I; actual nu, not supplied measure.')
    node('smooth-marginal-PI','source-consequence','D.6 applied at Eq2.13; C.3 use site','Var_nu(g)<=((1/alpha)+eta) E_nu||grad g||² for smooth g; alpha_nu=alpha/(1+alpha eta)>0.')
    node('weak-H1-adapter','SOURCE_GAP','C.1 opening density/closedness; C.3 rough Af use','Extend smooth PI to source weighted H1(nu); source does not prove smooth density and gradient closedness. Authored compact-gradient closure gives a scoped extension only, without asserting equivalence with weighted H1.')
    node('centered-Af','source-proof-step','A3.SS1 C.3 preceding paragraph; B.1/B.2/B.9','f in macro mean-zero implies Af centered because A preserves constants and actual marginal law; var_nu(Af)=||Af||².')
    node('C3','actual-consumer','A3.E3','For f in H_P,0: ||Af||²<=((1/alpha)+eta)||grad Af||². Domain requirement Af in source H1 is discharged using B.13 in printed argument, not an added public PI certificate.')
    node('C2','independent-source-input','A3.E2','eta||grad Af||²<=(1-alpha eta)²/[4(1+alpha eta)] (||f||²-||Af||²); separate gradient proof. Current closure result is a scoped adapter, not source H1 equivalence.')
    node('C4','actual-downstream-consumer','A3.E4','Combine C.2 with C.3 and rearrange: ||Af||<=(1-alpha eta)/(1+alpha eta)||f|| on mean-zero macro subspace; no claim candidate57 alone proves C.4.')
    node('Gamma-root','separate-source-root','B.5/B.10/B.11; D.1','Gamma=(I-A²)^(1/2) positive operator square root on macro L2; B*B=I-A² and norm defect; no weighted-Laplacian/resolvent identification, no eta prefactor.')
    edges=[]
    def edge(i,parents,target,use,discharge):
        edges.append(dict(id='pbps57:edge:'+i,parents=['pbps57:'+p for p in parents],consumer='pbps57:'+target,consumer_use_site=use,semantics='AND within this single printed route',conditional_discharge=discharge,formal_dependency_admitted=False))
    edge('conditional-curvature',['standing','actual-law'],'conditional-potential','Eq2.9-2.10','C2 Hessian of quadratic term eta^-1 I; eta positive; actual conditional law normalized.')
    edge('covariance-upper',['BL','conditional-potential'],'covariance','D.3 proof; Proposition2.1(i)','Lower curvature m=alpha+eta^-1>0; linear functions and moments require analytic discharge.')
    edge('covariance-lower',['CR','conditional-potential'],'covariance','D.3 proof; Proposition2.1(i)','Upper curvature L=beta+eta^-1>0; location-family Fisher information identity requires regularity/tails.')
    edge('actual-density',['actual-law','standing'],'differentiate-logdensity','D.10 preceding paragraph','Gaussian smoothing actual probability density and differentiations remain explicit analytical edge obligations.')
    edge('D10',['differentiate-logdensity'],'D10','D.10','Sigma normalization eta^-1, conditional moments not silently assumed.')
    edge('Eq213',['D10','covariance'],'marginal-curvature','D.10 final paragraph gives Eq2.13','Both conditional covariance sides yield corresponding opposite Hessian sides; eta^-1(1-1/(1+alpha eta))=alpha/(1+alpha eta).')
    edge('marginalPI',['BE','marginal-curvature','actual-law'],'smooth-marginal-PI','C.3 marginal Poincare invocation','nu actual normalized Gaussian convolution; U_eta at least required smoothness and positive m=alpha/(1+alpha eta).')
    edge('rough-extension',['smooth-marginal-PI'],'weak-H1-adapter','C.1 density/closedness; C.3 use for Af','Source H1 extension requires independent adapter; compact-gradient closure extension does not discharge equivalence.')
    edge('C3',['weak-H1-adapter','centered-Af'],'C3','A3.E3','Af domain and centering supplied as theorem results inside the consuming proof; not marginal PI public premises.')
    edge('C4',['C3','C2'],'C4','A3.E4 and paragraph combining C.3/C.2','0<alpha<=beta and beta eta<=1 imply 0<alpha eta<=1; centered f, common actual A and gradient representative; scalar rearrangement supplies rho_mac.')
    freeze=dict(schema_version=1,actor='/root/sourcegraph57',status='SOURCE_ONLY_TOPOLOGY_FROZEN_BEFORE_CANDIDATE_READ',created_at=now(),source_id='arXiv:2609.06905v1',source_pins=source_pins,nodes=nodes,edges=edges,coverage=coverage,
      chronology=dict(prospective_statement_read=False,root_proposal_read=False,parent_public_contract_read=False,parent_proof_body_read=False,candidate_proof_or_implementation_read=False,compiler_started=False),
      truth_boundary='Source topology extraction only. Independent reviewer required; no self-validation, Lean theorem, paper completion, or VERIFIED transition.',
      coverage_contract='All substantive p/source theorem/proof container/numbered and unnumbered display/citation regions in all21 balanced anchors are NODE or EXCLUDED; overlapping exact anchors deduplicated by region identity and exact primary byte span. Inline math belongs to its exact enclosing region.',
      gap_scope=['Gaussian differentiation, normalization and conditional moments','Bakry-Emery/Brascamp-Lieb/Cramer-Rao source external inputs','source weakH1 versus compact-gradient closure adapter','actual mean-zero A compatibility for C3 and C4','Gamma separate spectral root'],review_status='PENDING_DISTINCT_SOURCE_REVIEW')
    result=write('source-only-freeze.json',freeze)
    print(json.dumps(dict(stage=1,exit=0,anchors=len(anchors),coverage_regions=len(coverage),included=sum(r['disposition']=='NODE' for r in coverage),freeze=result)))

def stage2():
    freeze=native(OUT/'source-only-freeze.json'); assert not (OUT/'graph.packet.json').exists()
    assert freeze['chronology']['prospective_statement_read'] is False
    pre=ROOT/'runs/20261007-companion-priority/pbps-marginal-poincare-preproof57'
    statement=pre/'prospective-statement.txt'; b=statement.read_bytes(); lf=b.replace(b'\r\n',b'\n')
    assert len(lf)==1244 and digest(lf)=='e706b4e6c3c07f58a090ee86cb51dd91be2f11afe707db653737e4983c7181e9'
    proposal=pre/'root.statement-proposal.json'; obj=json.loads(proposal.read_bytes())
    assert obj['signature_lf_sha256']==digest(lf)
    (OUT/'prospective-statement.exactraw.snapshot.txt').write_bytes(b)
    (OUT/'prospective-statement.lf.snapshot.txt').write_bytes(lf)
    (OUT/'root.statement-proposal.exactraw.snapshot.json').write_bytes(proposal.read_bytes())
    (OUT/'root.statement-proposal.lf.snapshot.json').write_bytes(proposal.read_bytes().replace(b'\r\n',b'\n'))
    inputs=[pin(statement),pin(proposal)]
    contracts=[]
    for name in ['GaussianMarginalGradient','GaussianConvolutionRegularity','CenteredDomainPoincare','GibbsLinearCovarianceUpper']:
        p=SRC/(name+'.public-contracts.lf.snapshot.lean'); inputs.append(pin(p))
        dest=OUT/(name+'.public-contracts.lf.snapshot.lean'); dest.write_bytes(p.read_bytes()); contracts.append(pin(dest))
    p=ROOT/'AutoSamplingTheory/ExampleCases/SmoothedPicardHMC/SmoothedGibbsPotential.lean'
    # Read through a statement-only prefix; never inspect the proof suffix.
    prefix=[]
    with p.open('r',encoding='utf-8',newline='') as f:
        for line in f:
            if ':= by' in line:
                prefix.append(line.split(':= by',1)[0]); break
            prefix.append(line)
    header=''.join(prefix).encode('utf-8')
    dest=OUT/'SmoothedGibbsPotential.public-header.exactraw.snapshot.lean'; dest.write_bytes(header); contracts.append(pin(dest))
    dest=OUT/'SmoothedGibbsPotential.public-header.lf.snapshot.lean'; dest.write_bytes(header.replace(b'\r\n',b'\n')); contracts.append(pin(dest))
    inputs.append(dict(path=p.relative_to(ROOT).as_posix(),exposure='prefix through theorem signature only, proof suffix not read',header_raw_bytes=len(header),header_raw_sha256=digest(header),header_lf_sha256=digest(header.replace(b'\r\n',b'\n'))))
    # Coverage-only supplement: HTML citations are cite elements, not anchors.
    # It adds no mathematical topology and never edits the frozen source-first graph.
    manifest=native(SRC/'source-anchor-manifest.json'); raw=(SRC/'primary-pbps.exactraw.snapshot.html').read_bytes()
    citations=[]; seen=set()
    regions=freeze['coverage']
    for a in manifest['anchors']:
        t=Tree((ROOT/a['exactraw']['path']).read_text(encoding='utf-8'))
        for n in t.all:
            if n['tag']!='cite': continue
            start=a['source_start_utf8_byte']+len(t.s[:n['start']].encode('utf-8'))
            end=a['source_start_utf8_byte']+len(t.s[:n['end']].encode('utf-8'))
            if (start,end) in seen: continue
            seen.add((start,end)); enclosing=[r for r in regions if r['primary_start_utf8_byte']<=start and end<=r['primary_end_utf8_byte_exclusive']]
            parent=min(enclosing,key=lambda r:r['primary_end_utf8_byte_exclusive']-r['primary_start_utf8_byte']) if enclosing else None
            included=parent is not None and parent['disposition']=='NODE'
            citations.append(dict(region_id=f'citation-byte-{start}-{end}',kind='external-citation',source_text=norm(n),anchor_container=a['id'],primary_start_utf8_byte=start,primary_end_utf8_byte_exclusive=end,raw_sha256=digest(raw[start:end]),lf_sha256=digest(raw[start:end].replace(b'\r\n',b'\n')),disposition='NODE' if included else 'EXCLUDED',node_id=f'pbps57:citation:{start}' if included else None,reason='External citation supporting enclosing included source region; independently explicit citation coverage.' if included else 'Citation within excluded source region; '+(parent['reason'] if parent else 'No marginal PI consumer.')))
    write('coverage.citation-supplement.json',dict(schema_version=1,actor='/root/sourcegraph57',status='SOURCE_COVERAGE_SUPPLEMENT_NOT_TOPOLOGY_REVIEW',frozen_topology=pin(OUT/'source-only-freeze.json'),reason='Source-only parser classification correction: cite elements receive explicit standalone disposition. No node/edge mathematics changed after candidate read.',coverage=citations,independent_review_pending=True))
    binder=[]
    def slot(name,kind,source,meaning,boundary='Exact source standing premise represented by binder'):
        binder.append(dict(binder=name,classification=kind,source_anchor=source,expanded_meaning=meaning,boundary=boundary))
    slot('E; NormedAddCommGroup; InnerProductSpace real; FiniteDimensional real','TYPING','S1.p1 R^d','Finite real Hilbert coordinate carrier','Authored finite-Hilbert generalization; rank0 is explicitly scoped extension, not asserted printed equivalence')
    slot('MeasurableSpace E; BorelSpace E','TYPING','S1.p1 Euclidean Borel probability convention','Measurable structure exactly Borel generated by norm topology; not arbitrary incompatible sigma algebra')
    slot('V:E->real; alpha beta:NNReal; eta:real','TYPING','Eq1.1; S2.SS2','Source potential and scalar parameters; NNReal nonnegativity inherent in source 0<alpha<=beta')
    slot('hAlpha:0<(alpha:real)','SOURCE','Eq1.1','Strictly positive lower curvature; no zero-alpha endpoint')
    slot('hAlphaBeta:alpha<=beta','SOURCE','Eq1.1','Positive ordered curvature constants')
    slot('hV:ContDiff real 2 V','SOURCE','S1.p1','Original C2 only; no C3/Cinfty potential premise')
    slot('hH.lower:forall x v, alpha||v||²<=HessV(x)[v,v]','SOURCE','Eq1.1','Every x and v global lower Hessian quadratic form')
    slot('hH.upper:forall x v, HessV(x)[v,v]<=beta||v||²','SOURCE','Eq1.1','Same V/x/v global upper Hessian quadratic form; conjunction not alternative')
    slot('hEta:0<eta','SOURCE','S2.SS2 eta in(0,1/beta]','Positive Gaussian smoothing scale')
    slot('hBetaEta:beta eta<=1','SOURCE','S2.SS2','Capped eta includes eta=1/beta; do not strengthen to beta eta<1 or small universal cap')
    conclusions=[
      dict(item='mu,J,nu let-bound actual laws',classification='DEFINITION',semantics='mu normalized tilt of volume by -V; J actual independent Gaussian product pushforward; nu=J.snd; no caller-supplied law/normalizer/augmentation certificate'),
      dict(item='IsProbabilityMeasure nu',classification='DERIVED_OUTPUT',semantics='Must derive probability from source curvature/integrability and actual Gaussian pushforward, not additional premise'),
      dict(item='exists G before forall centered z',classification='DERIVED_OUTPUT',semantics='Uniform actual scalar-to-vector L2 partial linear operator on one fixed nu; no z-dependent choice'),
      dict(item='Dense domain, closable, closed closure, exact smooth compact graph',classification='DERIVED_OUTPUT_SCOPED_ADAPTER',semantics='Graph iff exact a.e. representatives phi and gradient phi; genuine core/closure domain derives from public GaussianMarginalGradient provider. No weak-H1 equivalence is claimed'),
      dict(item='forall z:G.closure.domain, mean z=0 -> alpha/(1+alpha eta)||z||²<=||G.closure z||²',classification='DERIVED_OUTPUT',semantics='Centered closure-domain PI, actual normalized nu mean, source coefficient reciprocal(1/alpha+eta), constant alpha/eta only; candidate scoped closure result rather than full printed H1 target')]
    reuse=[
      dict(provider='GaussianMarginalGradient.gaussian_marginal_gradient_closable',source_graph_use='weak-H1-adapter scoped authored closure only',required_edges=['mu probability','eta positive','actual J.snd identity'],no_source_H1_equivalence=True),
      dict(provider='GaussianConvolutionRegularity.gaussian_convolution_potential_c2 / gaussian_convolution_derivatives',source_graph_use='actual density and D10',required_edges=['mu probability','eta positive','positive Gaussian density normalizer'],result='C2 positive actual density, posterior probability/MemLp, score/Hess-covariance formula; no supplied conditional moment input'),
      dict(provider='GibbsLinearCovarianceUpper.gibbs_linear_covariance_upper',source_graph_use='D3 upper-covariance side sufficient for lower marginal curvature',required_edges=['posterior Gibbs identity','C2 conditional potential','conditional Hessian both bounds','conditional exp integrable/positive normalization','posterior MemLp id2'],limit='Does not give D3 covariance lower or exact Eq2.13 upper Hessian; those stronger source regions remain visible'),
      dict(provider='CenteredDomainPoincare.gibbs_centered_domain_poincare',source_graph_use='source D6-to-centered-closure adapter',required_edges=['actual nu as Gibbs tilted law','actual potential C2','exp integrability/positive normalization','positive lower curvature alpha/(1+alpha eta)','some derived global upper Hessian for provider','same exact core graph and closability'],limit='Provider arguments are derived implementation dependency edges, never extra candidate public binders. An upper bound1/eta would suffice for this provider but is a separately attributed adapter, not exact printed upper beta/(1+beta eta).'),
      dict(provider='SmoothedPicardHMC.SmoothedGibbsPotential.smoothed_gibbs_potential',source_graph_use='actual Gibbs normalization/potential law identity public reuse',required_edges=['source V C2','positive lower Hessian','eta positive'],limit='Public source-specific SPHMC normalization adapter reused only with exact law identity; normalized log-density differs by log ZV. No SPHMC/PBPS full result credit.')]
    write('binder-and-reuse-audit.json',dict(schema_version=1,actor='/root/sourcegraph57',status='PROSPECTIVE_SOURCE_SCOPE_AUDIT_PENDING_REVIEW',statement=pin(OUT/'prospective-statement.lf.snapshot.txt'),binder_ledger=binder,conclusion_semantics=conclusions,EXCESS=[],public_certificate_inputs=[],public_reuse=reuse,public_contract_pins=contracts,
      source_scope_deltas=['Finite real Hilbert and rank0 explicitly authored extension','Compact-gradient closure domain scoped analytic adapter; weightedH1 equivalence absent','Candidate derives marginal PI coefficient only; exact two-sided Eq2.13 and C3/C4 actual operator compatibility not certified'],compiler_started=False,parent_proof_bodies_read=False))
    graph_nodes=freeze['nodes']+[dict(id=r['node_id'],kind=r['kind'],source_region=r['region_id'],source_start_utf8_byte=r['primary_start_utf8_byte'],source_end_utf8_byte_exclusive=r['primary_end_utf8_byte_exclusive'],coverage_node_only=True) for r in regions if r['disposition']=='NODE']+[dict(id=r['node_id'],kind=r['kind'],source_region=r['region_id'],coverage_node_only=True) for r in citations if r['disposition']=='NODE']
    write('graph.packet.json',dict(schema_version=1,actor='/root/sourcegraph57',status='EXTRACTED_PENDING_INDEPENDENT_TOPOLOGY_REVIEW',source_id='arXiv:2609.06905v1',source_first_freeze=pin(OUT/'source-only-freeze.json'),candidate_statement=pin(OUT/'prospective-statement.lf.snapshot.txt'),native_primary_contract=pin(SRC/'primary.contract.json'),native_primary_precision=pin(SRC/'source.precision-addendum.json'),native_closed_primary_lease=pin(SRC/'lease.json'),nodes=graph_nodes,edges=freeze['edges'],coverage_source_files=[pin(OUT/'source-only-freeze.json'),pin(OUT/'coverage.citation-supplement.json')],binder_audit=pin(OUT/'binder-and-reuse-audit.json'),
      actual_consumers=[dict(anchor='C3',consumer='actual56 same-nu rough-image centered PI',required='identify exact same core graph/closure for genuine Tu/Ku image; centered macro input; source H1 adapter still distinct'),dict(anchor='C4',consumer='macro norm rho_mac bound',required='C3 plus separately established C2 sharp energy on same actual A and G; rearrangement and mean-zero compatibility')],
      independent_review=dict(status='PENDING',required_actor='/root/next_primary56',creator_cannot_validate=True,reviewer_inputs='Pinned raw primary/anchors + native frozen source graph + prospective interface/binder audit only; no parent/candidate proof bodies or private creator rationale.'),
      explicit_source_gaps=freeze['gap_scope'],claim_boundary='No compiler, proof, implementation, SAU claim, canonical publication, formal edge admission, weightedH1 equivalence, Gamma/resolvent identity, whole-paper or whole-Goal completion.',chronology=dict(source_topology_frozen_before_candidate=True,source_topology_freeze_digest=pin(OUT/'source-only-freeze.json')['raw_sha256'],candidate_read_after_freeze=True,parent_public_contracts_read_after_freeze=True,parent_proof_bodies_read=False,candidate_proof_bodies_read=False)))
    write('input-manifest.json',dict(schema_version=1,actor='/root/sourcegraph57',source_inputs=freeze['source_pins'],postfreeze_inputs=inputs,source_first_freeze=pin(OUT/'source-only-freeze.json'),proof_exposure='NONE',compiler_exposure='NONE'))
    (OUT/'README.md').write_bytes(('PBPS marginal Poincare candidate57: source graph extraction only\n\nSource-only topology was frozen before prospective signature/public reuse contract reads. 21 balanced primary anchors are pinned. Every selected substantive paragraph, numbered/unnumbered display and source statement/proof container is NODE or EXCLUDED. Citation supplement adds cite-element coverage without changing mathematical topology.\n\nSource route: original C2 and both global Hessian bounds + positive capped eta -> actual conditional curvature -> D3 covariance + D10 actual marginal differentiation -> Eq2.13 -> D6 marginal PI -> explicit source weighted-H1 extension gap -> C3; C3 + independent C2 sharp gradient energy -> C4. Gamma=(I-A^2)^(1/2) is a separate root.\n\nProspective candidate uses one genuine compact-gradient closure, selected before every centered z, for nu=law(X+sqrt(eta)Z); no supplied measure, Poincare/domain/normalization/curvature certificate. Rank0 finite-Hilbert extension and weak-H1 non-equivalence remain explicit. Public provider obligations remain edges.\n\nIndependent source review by a distinct reviewer is pending. This packet is neither blueprint nor mathematical proof and makes no VERIFIED/full-paper claim.\n\nRecipes (PowerShell, bundled Python):\n\n& "C:\\Users\\admin\\.cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\python\\python.exe" -X utf8 "runs/20261007-companion-priority/pbps-marginal-poincare-sourcegraph57/build_packet.py" source-first\n\nThe source-first command is one-shot and refuses to overwrite the source freeze. Its observed process result: EXIT0, chunk fe4245.\n\n& "C:\\Users\\admin\\.cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\python\\python.exe" -X utf8 "runs/20261007-companion-priority/pbps-marginal-poincare-sourcegraph57/build_packet.py" bind-candidate\n\n& "C:\\Users\\admin\\.cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\python\\python.exe" -X utf8 "runs/20261007-companion-priority/pbps-marginal-poincare-sourcegraph57/finalize_packet.py"\n\nRead-only check after closing:\n\n& "C:\\Users\\admin\\.cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\python\\python.exe" -X utf8 "runs/20261007-companion-priority/pbps-marginal-poincare-sourcegraph57/finalize_packet.py" --check\n\nNative self hashes: entire parsed object minus only declared content_self_sha256; UTF8 ensure_ascii=False, sorted keys, compact comma/colon separators, no newline. Actual raw/LF output pins are distinct from native object hashes. CLOSED lease is written last, then read back and enclosing tool must observe EXIT0.\n').encode('utf-8'))
    print(json.dumps(dict(stage=2,exit=0,graph=pin(OUT/'graph.packet.json'),source_regions=len(regions),citation_regions=len(citations),candidate_lf_sha256=digest(lf))))

if __name__=='__main__':
    if sys.argv[1:] == ['source-first']: stage1()
    elif sys.argv[1:] == ['bind-candidate']: stage2()
    else: raise SystemExit('Use source-first or bind-candidate')
