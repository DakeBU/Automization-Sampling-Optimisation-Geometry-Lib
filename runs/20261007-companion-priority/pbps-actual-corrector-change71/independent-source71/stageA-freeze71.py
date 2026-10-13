import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,hashlib,os,datetime,collections
O=pathlib.Path(__file__).resolve().parent
B=pathlib.Path('E:/Samplinglib')
P=B/'runs/20261007-companion-priority/pbps-corrector-change-preproof71'
H=P/'independent-header-source71'; S=P/'independent-source-first71'
def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def write(n,x):
    with (O/n).open('xb') as f:f.write((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
def pin(p):
    p=pathlib.Path(p);b=p.read_bytes();lf=b.replace(b'\r\n',b'\n')
    return {'path':p.relative_to(B).as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_bytes':len(lf),'LF_sha256':sha(lf),'mtime_ns_observed':p.stat().st_mtime_ns}
inventory=json.loads((O/'stageA.primary255.reparsed-inventory.json').read_bytes())['items']
byid={x['math_id']:x for x in inventory};assert len(byid)==255
old_expect=json.loads((H/'stageA.source-expectations71.before-header.frozen.json').read_bytes())
assert sha((H/'stageA.source-expectations71.before-header.frozen.json').read_bytes())=='858e56e10208c57130ae4a15efdf90206b62f50810419292bcbce6d20e85e761'
oldgraphpath=B/'runs/20261007-companion-priority/pbps-actual-projected-rotation70/independent-source70/stageA.source-proof-graph70.frozen.json'
oldgraph=json.loads(oldgraphpath.read_bytes());oldnodes={x['id']:x for x in oldgraph['nodes']}
closure_pins=[]
for d,mname,lhash in [(H,'owned-manifest.json','279b90f74b7b0e2d07ae681245f7da143b517305b6fe58e62c732cc6ed45df9f'),(S,'outputs.manifest.json','6feb5f619afc7d32cd196f2748165eaed9862da3a682bf782916e456fe423082')]:
    assert sha((d/'lease.final.json').read_bytes())==lhash
    m=json.loads((d/mname).read_bytes());entries=m['files']
    for q in entries:
        p=d/(q.get('relative_path') or q['path']);b=p.read_bytes();lf=b.replace(b'\r\n',b'\n')
        assert len(b)==q.get('RAW_bytes',q.get('raw_bytes')) and sha(b)==q.get('RAW_sha256',q.get('raw_sha256'))
        assert len(lf)==q.get('LF_bytes',q.get('lf_bytes')) and sha(lf)==q.get('LF_sha256',q.get('lf_sha256'))
    closure_pins.append({'scope':d.relative_to(B).as_posix(),'manifest':pin(d/mname),'lease':pin(d/'lease.final.json'),'opaque_regular_files_verified':len(entries),'mathematical_verdicts_or_old_candidate_bytes_decoded':False,'old_writes':False})
write('stageA.prior-closures-opaque-integrity.frozen.json',{'schema':'source71-stageA-opaque-closure-integrity-v1','actual_pid':os.getpid(),'closures':closure_pins,'interpretation':'Read-only RAW/LF integrity. No previous acceptance substitutes current71 review.'})

# These descriptions and edge reasons are rebuilt from primary B3/B4/D1.
# P0-P11 source provenance outside the four selected regions is carried source-only background.
specs=[
('P0','source-hypotheses','Original Gibbs law, C2 potential, 0<alpha<=beta, two Hessian bounds and 0<eta<=1/beta.','Finite real Hilbert/Borel/volume typing; rank may be zero.','carried-source-background',['S1.p1.m1','S1.p1.m2','S1.p1.m3','S1.p1.m4','S1.E1.m1']),
('P1','actual-joint-law','Same pi_eta from X~mu and independent Gaussian noise Y=X+sqrt(eta)Z.','Real L2(pi_eta) modulo AE equality.','carried-source-background',[]),
('P2','actual-reflection','Same F(x,y)=(x,2x-y); U is its L2 pullback, measure preserving involution fixing constants.','AE reflection identity; U is not an arbitrary unitary witness.','carried-source-background',[]),
('P3','actual-projection','P is conditional expectation given Y; Hperp=ker P; Pperp=I-P.','HP=ran P; HP0=HP intersect L2_0.','carried-source-background',['A4.SS1.p1.m2','A4.SS1.p1.m3','A4.SS1.p1.m4','A4.SS1.p1.m5','A4.SS1.p1.m6']),
('P4','reflection-block-identities','A=P U inclusion, B=R U inclusion; D=R U inclusion on all Hperp; B*D=-A B*.','Every micro vector in ker P, not only ran V.','carried-source-background',['A2.SS3.p5.m11']),
('P5','same-positive-root','Gamma=(I-A^2)^(1/2) is the nonnegative root; A Gamma=Gamma A; A^2+Gamma^2=I.','Same real bounded selfadjoint operators.','carried-source-background',['A2.SS3.p5.m12','A2.SS3.p5.m13','A2.SS3.p5.m20','A4.SS1.p2.m7','A4.SS1.p2.m8','A4.SS1.p2.m9']),
('P6','centered-positive-gap','Gamma restricted to HP0 has positive lower bound gamma_gap from the original assumptions.','No positive dimension or alpha eta<1 premise.','carried-source-background',['A2.SS3.p4.m4']),
('P7','centered-inverse-and-reducing-domain','A0 and Gamma0 preserve HP0; Inv is SAME Gamma0 two-sided bounded inverse; A0 Inv=Inv A0.','Only HP0; no global inverse on constants.','carried-source-background',['A2.SS3.p4.m2','A2.SS3.p4.m3','A2.SS3.p4.m4','A2.SS3.p5.m17','A2.SS3.p5.m18']),
('P8','same-polar-isometry','V0=B0 Inv, B0=V0 Gamma0, V0*V0=I; V0 maps HP0 into Hperp isometrically.','V0 need not be onto; V0 V0* is range projection.','carried-source-background',['A2.SS3.p3.m5','A2.SS3.p3.m7','A2.SS3.p3.m8','A2.SS3.p3.m10']),
('P9','adjoint-inclusion-adapter','Ambient B*h is centered inclusion(Gamma0 V0*h); internal B0*=Gamma0 V0*.','All h in Hperp, with centered/ambient types explicit.','carried-source-background',['A2.SS3.p3.m3','A2.SS3.p5.m10']),
('P10','centered-cancellation-domain','V0*D h and A0 V0*h lie in HP0, where Gamma0 can be cancelled using Inv.','No ambient cancellation across constants.','carried-source-background',['A2.SS3.p5.m14','A2.SS3.p5.m15','A2.SS3.p5.m16']),
('P11','retained-all-micro-intertwining','V0*D=-A0 V0* for all micro vectors, with SAME U, root, inverse and polar map.','Retained69 input composition, not a new public certificate caller.','retained-parent-source',['A2.Ex14.m1','A2.SS3.p5.m19']),
('P12','actual-centered-decomposition','For every globally centered f: fP=Pf, fperp=Rf, fV=V0*Rf; fP,fV in HP0 and norm(fV)<=norm(fperp).','No assumption fperp in ran V0.','retained-parent-source',['A2.SS3.p1.m2','A2.Ex6.m1','A2.Ex8.m1','A2.SS3.p3.m11','A2.SS3.p3.m15']),
('P13','actual-ideal-update','g=U(Pf-(f-Pf)); actual gP=Pg, gperp=Rg, gV=V0*Rg. Mean(g)=0 is internally obtained.','Same U and actual conditional expectation; never RHS-defined coefficient vectors.','retained-parent-source',['A2.Ex10.m1','A2.SS3.p5.m7','A2.Ex11.m1']),
('P14','actual-rotation-and-pair-energy','gP=A0 fP-Gamma0 fV; gV=Gamma0 fP+A0 fV; pair squared norm is preserved.','HP0 direct sum; actual projections first, rotation second.','retained-parent-source',['A2.Ex12.m1','A2.Ex13.m1','A2.Ex13.m2','A2.Ex15.m1','A2.Ex15.m2','A2.SS3.p5.m20','A2.SS3.p5.m21']),
('P15','B20-exact-corrector','C(u,v)=(norm(u)^2-norm(v)^2)/2-inner(A0(Inv u),v).','HP0 x HP0; SAME A0 and SAME centered Inv.','new71-definition',['A2.E20.m1','A4.E1.m1','A4.E2.m1']),
('P16','B21-coefficient-algebra-ingredient','For u,v in HP0 and u1=A0u-Gamma0v,v1=Gamma0u+A0v: C(u1,v1)-C(u,v)=-norm(u)^2+norm(v)^2.','Uses internal selfadjointness, commutation, both inverse identities and A0^2+Gamma0^2=I.','new71-proof-ingredient',['A2.Ex17.m1','A2.E21.m1','A2.SS3.p7.m1','A2.SS3.p7.m2','A2.SS3.p7.m3','A2.SS3.p7.m4','A2.Ex19.m1','A2.SS3.p7.m5']),
('P17','B21-actual-corrector-change','C(gP,gV)-C(fP,fV)=-norm(fP)^2+norm(fV)^2.','All globally centered actual f, common witnesses selected before f.','new71-actual-target',['A2.Ex16.m1','A2.Ex17.m1','A2.E21.m1']),
('P18','leading-term-consumer','B21 with norm(fV)<=norm(fperp) gives macro/micro leading decay when 0<omega<rho.','Consumer context only; rho/omega are not71 caller binders.','open-real-consumer',['A2.SS3.p5.m22','A2.SS3.p5.m23','A2.Ex18.m1']),
('P19','B4-shared-error-components','r_rho=V0*[I+(1-rho)H]fperp; (Kf)P=gP+Gamma0 r_rho; (Kf)V=gV-A0 r_rho.','Same g comparator and centered error vector; actual K is not Kid.','open-real-consumer',['A2.SS3.p8.m4','A2.SS3.p8.m5','A2.SS3.p8.m6','A2.SS3.p8.m9','A2.SS3.p8.m10','A2.Ex27.m1','A2.E27.m1']),
('P20','B4-B28-direct-consumer','C((Kf)P,(Kf)V)-C(fP,fV)=-norm(fP)^2+norm(fV)^2+inner(gP,Inv r_rho)+norm(r_rho)^2/2.','B27 perturbation expansion plus explicit B21 addition; not proved by71 alone.','open-real-consumer',['A2.Ex28.m1','A2.Ex31.m1','A2.Ex33.m1','A2.Ex34.m1','A2.Ex35.m1','A2.Ex36.m1','A2.E28.m1']),
('P21','B4-errors-and-modified-decay-boundary','B17 error control, B29/B30/B31, B18 norm loss and sibling B22 norm equivalence are needed for B26 decay.','B4 small-step beta eta<=c0, c0<=1/16 and gamma<=1/2 are separate consumer assumptions.','open-real-consumer',['A2.E25.m1','A2.Thmtheorem4.p1.m1','A2.Thmtheorem4.p1.m2','A2.E26.m1','A2.E29.m1','A2.E29.m2','A2.E30.m1','A2.E30.m2','A2.E31X.m2'])]
nodes=[]
for ident,kind,statement,domain,role,ids in specs:
    anchors=[byid[x] for x in ids]
    carried=[]
    if int(ident[1:])<=11:
        for a in oldnodes[ident]['primary_math']:
            if a['id'] not in byid:carried.append(a)
    nodes.append({'id':ident,'kind':kind,'statement':statement,'domain_and_scope':domain,'role':role,'current_four_region_RAW_anchors':anchors,'carried70_primary_source_anchors_not_reread_in_four_regions':carried,'formal_status':'source-expectation-only-current71-BODY-unread'})
edge_specs=[
('P0','P1','Original analytic data construct the same joint law.'),('P1','P2','Same joint law yields reflection preservation.'),('P1','P3','Same joint law defines conditional projection.'),
('P2','P4','Selfadjoint reflection involution supplies block equations.'),('P3','P4','Exact projection inclusions supply block domains.'),('P4','P5','I-A^2 is the squared micro block norm.'),('P0','P6','Original assumptions yield gap; no stronger endpoint restriction.'),('P5','P6','Gap applies to SAME positive root.'),
('P2','P7','Reflection fixes constants and preserves mean.'),('P3','P7','Projection fixes constants and preserves mean.'),('P5','P7','Functional calculus supplies commutation on reducing centered space.'),('P6','P7','Positive centered gap supplies bounded inverse.'),('P4','P8','Polar map uses SAME actual B restriction.'),('P7','P8','Polar map is B0 composed with SAME Inv.'),
('P8','P9','Adjoint of polar identity supplies Gamma0 V0*.'),('P2','P9','Fixing constants makes B* output centered.'),('P3','P9','Centered inclusion and ambient adjoint must agree.'),('P7','P10','A0 preserves centered space.'),('P8','P10','V0* has centered codomain.'),('P4','P11','Start with exact B*D=-A B* on all Hperp.'),('P9','P11','Transport B* into centered Gamma0 V0*.'),('P10','P11','Both sides have cancellable centered range.'),('P7','P11','Commute and cancel SAME Gamma0 using SAME inverse.'),
('P3','P12','Conditional expectation supplies actual centered decomposition.'),('P8','P12','Polar adjoint supplies actual fV and contraction.'),('P2','P13','U preserves the mean of the reflected input.'),('P3','P13','Pf-(f-Pf) is internally centered when f is.'),('P13','P14','Compute actual projected components of g.'),('P12','P14','Use actual fP,fperp,fV decomposition.'),('P9','P14','Macro formula uses transported polar adjoint.'),('P11','P14','Micro formula uses all-micro intertwining.'),('P8','P14','V0*B0=Gamma0 gives positive rotation sign.'),
('P7','P15','B20 is defined only with centered inverse.'),('P5','P16','Selfadjoint commuting A0,Gamma0 and square sum give cancellations.'),('P7','P16','Two inverse identities and inverse commutation justify transport.'),('P15','P16','Use precisely B20 half coefficient and cross term.'),('P14','P17','Actual components realize the algebraic rotation.'),('P16','P17','Substitute actual centered fP,fV into coefficient identity.'),('P17','P18','B21 supplies signed leading contribution.'),('P12','P18','Contraction bounds polar component by whole micro norm.'),
('P11','P19','B4 explicitly reuses all-micro intertwining.'),('P9','P19','B4 reuses SAME polar adjoint for macro error.'),('P13','P19','B4 compares actual K to SAME Kid update.'),('P19','P20','B27 error pair yields perturbation expansion.'),('P15','P20','Expand SAME B20 corrector.'),('P17','P20','Primary B21 href adds exact signed term in B28.'),('P14','P21','Pair energy bounds gP in later Young estimate.'),('P20','P21','B28 requires independent residual-error control for decay.'),('P18','P21','Leading decay is only one part of modified contraction.')]
assert len(nodes)==22 and len(edge_specs)==49
graph={'schema':'source71-stageA-independently-rebuilt-primary-graph-v1','source':'arXiv:2609.06905v1 fixed RAW primary','node_count':22,'edge_count':49,'nodes':nodes,'edges':[{'parent':a,'child':b,'kind':'source-proof-dependency-or-open-consumer-not-certified-Lean-edge','reason':c} for a,b,c in edge_specs],'current71_BODY_read':False,'no_source_hypothesis_invented_from_proof_ingredients':True,'rebuild_method':'B3/B4/D1 RAW reread and independently reparsed anchors. Stable P0-P11 source-only provenance carried from prior primary graph; current target/consumer descriptions and edge reasons written before current71 BODY.'}
write('stageA.source-proof-graph71.before-current-BODY.frozen.json',graph)

# Exhaustive finite classification is broader than the prospective header delta.
def classify(x):
    i=x['math_id'];r=x['region']
    if r=='global-assumptions':
        if i in ['S1.p1.m1','S1.p1.m2','S1.p1.m3','S1.p1.m4','S1.E1.m1']:return 'NODE',['P0'],'retained-source-hypothesis','Exact original analytic assumptions; no new caller.'
        return 'EXCLUDED',[],'main-and-cost-boundary','Warm start, TV, complexity, comparisons or introduction prose; bounded71 does not prove these.'
    if r=='real-L2-spectral-conventions-D1':
        if i.startswith('A4.Thmtheorem1.') or i in ['A4.E1.m1','A4.E2.m1']:return 'NODE',['P12','P15'],'definition-convention','Real AE L2, centered mean and norm/inner conventions for actual components and C.'
        if i.startswith('A4.SS1.p1.'):return 'NODE',['P3'],'definition-convention','Closed orthogonal projection and complementary-space convention, not onto V.'
        if i.startswith('A4.SS1.p2.') or i=='A4.E3.m1':return 'NODE',['P5','P7','P16'],'proof-material-convention','Adjoint/selfadjointness/order/spectral calculus conventions; supply internal ingredients rather than caller certificates.'
        return 'EXCLUDED',[],'markov-density-and-chi-square-boundary','General kernel/density/chi-square convergence context is outside actual ideal corrector-change edge.'
    if r=='corrector-sharp-energy-and-consumers-B3':
        if i in ['A2.SS3.m1','A2.SS3.p1.m1'] or i.startswith('A2.SS3.p1.') or i=='A2.Ex6.m1':return 'NODE',['P12'],'retained-actual-semantics','Every global mean-zero actual f and its conditional macro/micro decomposition.'
        if i.startswith('A2.SS3.p2.') or i.startswith('A2.Ex7.') or i=='A2.E18.m1':return 'EXCLUDED',[],'actual-K-norm-loss-boundary','B18 refreshment/H contraction and motivational failure of ordinary norm decay are not71 theorem conclusions or new assumptions.'
        if i.startswith('A2.SS3.p3.') or i=='A2.Ex8.m1':return 'NODE',['P8','P9','P12'],'retained-actual-polar-semantics','Actual polar adjoint on all ker P; range projection is not identity on all micro vectors.'
        if i=='A2.E20.m1':return 'NODE',['P15'],'new71-definition','Exact B20 half norm difference and negative SAME A0 Inv cross term.'
        if i in ['A2.SS3.p4.m2','A2.SS3.p4.m3','A2.SS3.p4.m4']:return 'NODE',['P7','P15'],'centered-inverse-domain','B20 inverse only on HP0; gap justifies inverse internally.'
        if i in ['A2.SS3.p4.m1','A2.E19.m1']:return 'EXCLUDED',[],'weighted-energy-boundary','Definition of L_omega and omega positivity are downstream context; C-change has no omega premise.'
        if i in ['A2.Ex9.m1'] or i.startswith('A2.SS3.p5.m') and 1<=int(i.rsplit('m',1)[1])<=6:return 'EXCLUDED',[],'ideal-versus-actual-K-context','rho=0 and replacing H by -I explain idealization; they are not identities for actual K and not71 caller assumptions.'
        if i in ['A2.Ex10.m1','A2.Ex11.m1','A2.SS3.p5.m7','A2.SS3.p5.m8']:return 'NODE',['P13'],'retained-actual-update','Same U(P-Pperp), g actual first, then Pg and V*Rg.'
        if i.startswith('A2.Ex12.') or i.startswith('A2.Ex13.') or i.startswith('A2.Ex15.') or i in ['A2.SS3.p5.m9','A2.SS3.p5.m20','A2.SS3.p5.m21']:return 'NODE',['P14'],'retained-actual-rotation','Exact minus/plus signs and orthogonal pair-energy argument on HP0 direct sum.'
        if i=='A2.Ex14.m1' or i.startswith('A2.SS3.p5.m') and 10<=int(i.rsplit('m',1)[1])<=19:return 'NODE',['P7','P9','P10','P11'],'retained-domain-intertwining','Same-root commutation, centered cancellation and all-micro intertwining supply actual rotation.'
        if i in ['A2.Ex16.m1','A2.Ex17.m1','A2.E21.m1']:return 'NODE',['P16','P17'],'new71-actual-target','Primary actual pair is substituted into exact B20 coefficient algebra; signed result is -norm fP squared +norm fV squared.'
        if i in ['A2.SS3.p5.m22','A2.SS3.p5.m23','A2.Ex18.m1']:return 'NODE',['P18'],'open-real-consumer','Downstream leading-term consumer only; omega/rho restrictions not inherited by71.'
        if i in ['A2.SS3.p7.m1','A2.SS3.p7.m2','A2.SS3.p7.m3','A2.SS3.p7.m4','A2.Ex19.m1','A2.SS3.p7.m5']:return 'NODE',['P16'],'source-internal-algebra-material','Primary explicitly states commuting selfadjoint A,Gamma and A Inv, plus square identity; use as internal proof-material expectations, not sibling68 dependency.'
        if i in ['A2.Thmtheorem4.p1.m1','A2.Thmtheorem4.p1.m2','A2.Thmtheorem4.p1.m3','A2.E25.m1','A2.E26.m1']:return 'NODE',['P21'],'open-real-consumer','B4 statement and smaller-step/constants are separate open consumer boundary; no71 decay or small-step claim.'
        return 'EXCLUDED',[],'sibling-sharp-energy-and-norm-equivalence','Lemma B3/B22-B24 sharp corrector bound, block-square/norm estimate or intervening exposition is a separate result; not a68 parent or71 proof premise.'
    if r=='corrector-change-B4-consumer-proof':
        if i in ['A2.SS3.p8.m1','A2.SS3.p8.m2','A2.SS3.p8.m3']:return 'NODE',['P21'],'open-consumer-assumptions','B4-only c0/gap/log constants; retain alpha eta=1 in71, never introduce gamma<=1/2 caller.'
        if i in ['A2.E29.m1','A2.E29.m2','A2.E30.m1','A2.E30.m2','A2.E31X.m2']:return 'NODE',['P21'],'open-error-consumer','B29/B30/B31 residual-error estimates need B17 and refreshment; not supplied by71.'
        if x['RAW_full_start']<byid['A2.Ex28.m1']['RAW_full_start']:return 'NODE',['P19'],'open-real-consumer','Actual K-Kid comparison, same g, centered residual and B27 components; distinct from ideal update equality.'
        if x['RAW_full_start']<=byid['A2.E28.m1']['RAW_full_start']:return 'NODE',['P20'],'open-direct-B21-consumer','Exact B20 perturbation expansion and B21 addition give B28; bound as consumer relationship only.'
        return 'EXCLUDED',[],'B4-error-decay-main-boundary','Further B17 error estimates, Young bounds, constants, Lyapunov decay and B22 conversion remain independent open obligations outside71.'
    raise AssertionError(r)
entries=[]
for x in inventory:
    cl,ns,role,reason=classify(x);entries.append({**x,'classification':cl,'source_nodes':ns,'role':role,'reason':reason,'is_current71_implementation_verdict':False})
counts=dict(collections.Counter(x['classification'] for x in entries));assert sum(counts.values())==255
write('stageA.primary255-NODE-EXCLUDED71.before-current-BODY.frozen.json',{'schema':'source71-stageA-exhaustive-finite-primary-coverage-v1','count':255,'RAW_regions':4,'counts':counts,'unclassified':0,'entries':entries,'NODE_means':'Source graph attribution including carried definitions, proof ingredients and OPEN consumers; never implementation/proof acceptance.','EXCLUDED_means':'Outside bounded71 implementation target with explicit remaining source boundary.','prior_header_scope':{'count':255,'NODE':11,'EXCLUDED':244,'reason':'Prospective header review only selected new target and direct formula anchors. Current whole-review expectation additionally attributes unchanged definitions/rotation and open consumers; this is scope refinement, no mathematical repair.'}})
target=json.loads((H/'source-first71.source.formulas.exact.json').read_bytes())
for f in target['formulas']:
    x=byid[f['id']];assert f['RAW_sha256']==x['math_RAW_sha256'] and f['start_byte']==x['RAW_full_start'] and f['end_byte_exclusive']==x['RAW_full_end_exclusive'] and f['alttext']==x['formula_latex']
write('stageA.target18-exact-RAW-formulas71.frozen.json',{'schema':'source71-stageA-target18-RAW-revalidated-v1','count':18,'source_B21_href_RAW_offset':926328,'formulas':[{**f,'current_coverage':next({'classification':e['classification'],'source_nodes':e['source_nodes'],'role':e['role']} for e in entries if e['math_id']==f['id'])} for f in target['formulas']],'authority':'Exact RAW math spans and byte offsets; alttext decoded as display aid only.'})

more=[
('W14','Expand C on arbitrary centered u,v using the same A0/Inv, then explicitly substitute actual fP/fV and gP/gV; algebra alone is insufficient.'),
('W15','Produce selfadjoint A0,Gamma0 and A0 Inv or equivalent explicit real inner transport from existing hypotheses; never add caller binders.'),
('W16','Produce A0 Inv=Inv A0, Inv Gamma0=I and Gamma0 Inv=I on HP0, preserving type/inclusion and SAME inverse.'),
('W17','Check norm expansion, inner symmetry and all mixed-term signs; norm-part difference is -norm(Gamma0 u)^2+norm(Gamma0 v)^2-2 inner(A0 Gamma0 u,v).'),
('W18','Check cross-term difference cancels the mixed part: its negative change is -norm(A0u)^2+norm(A0v)^2+2 inner(A0 Gamma0u,v); square sum gives exact B21.'),
('W19','Use A0^2+Gamma0^2=I on every HP0 vector; do not replace actual micro space by ran V0 or require V0 onto.'),
('W20','Account for every complete528 module line and all new algebra/helpers in StageB, with exact BODY ranges and formulas; no current BODY exposure at StageA.'),
('W21','Compare eight semantic concerns including the new exact B20-definition/actual-B21 slot, blind reconstruction and official publication-bound packet only after authorization.'),
('W22','Reader must distinguish private literal Prop record from proof provider and expose complete conditions/parent clauses adjacent to exact initially folded statement/BODY.'),
('W23','Classify B4/B28 explicit real consumer, B17/B18/B22 residual dynamics, main sampling errors/caps/cost/composition as remaining, not theorem completion.')]
obligations=[{'id':x['id'],'expectation':x['expectation'],'stage':'retained-pre-header-source-expectation','status':'frozen-pending-current71-StageB'} for x in old_expect['obligations']]+[{'id':i,'expectation':e,'stage':'whole-module-source-first-review-obligation','status':'frozen-pending-current71-StageB'} for i,e in more]
write('stageA.source-expectations71.before-current-BODY.frozen.json',{'schema':'source71-stageA-independent-primary-first-expectations-v1','freeze_actual_pid':os.getpid(),'freeze_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'fixed_primary_RAW_bytes':1482128,'fixed_primary_RAW_sha256':'d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760','source_target':['P15','P16','P17'],'source_real_consumers':['P18','P19','P20','P21'],'public_analytic_callers':['0<alpha','alpha<=beta','V is C2','global lower and upper Hessian bounds','0<eta','beta*eta<=1'],'same_common_witnesses_before_f':['S','e','U','T','Gamma','q','GammaP0','Inv','A0','B0','V0','R'],'actual_input_scope':'All globally centered f in SAME real L2(actual pi_eta), with actual conditional fP,gP and actual polar fV,gV; preserve entire parent70 literal result.','new_definition':'C(u,v)=(norm(u)^2-norm(v)^2)/2-inner(A0(Inv u),v) on HP0 x HP0.','new_conclusion':'C(gP,gV)-C(fP,fV)=-norm(fP)^2+norm(fV)^2.','mean_g_completion':{'source_status':'Implicit in source use of centered gP/gV; ASTIS must supply internal adapter.','internal_route':'condExp integral preservation gives integral(Pf)=integral(f)=0; integral(f-Pf)=0; their difference is centered; actual reflection measure preservation gives integral(U h)=integral(h); hence mean(g)=0.','forbidden':'No mean_g caller, extra smoothness, alternate U, or RHS-defined actual components.'},'proof_ingredients_are_edges_not_caller_binders':True,'endpoint_contract':'Rank0 and alpha*eta=1 retained; no onto V0, no global inverse on constants; no68 sharp-energy parent.','obligation_count':len(obligations),'obligations':obligations,'current71_BODY_read':False,'final_source_fidelity_or_VERIFIED_credit':False,'full_paper_B4_main_errors_costs_composition_Purified_Exposition_live_credit':False})
write('stageA.anti-anchoring-exposure71.frozen.json',{'schema':'source71-stageA-honest-exposure-v1','source_blind_claim':False,'earlier_exposure':{'same147_line_prospective_header':True,'prospective_header_RAW_sha256':'2bef0d5cf364270b6f580288e966d9bb78310f646a7fe13b6f8855807e70f42c','parent70_complete_BODY':True,'same_header_semantics_unchanged_reported_by_parent':True,'current71_implementation_ever_read':False},'current_stage_allowed_reads':'Fixed primary RAW four regions, independently reparsed255 items; own pre-header StageA evidence; carried70 primary source-only graph; opaque old closure bytes for integrity.','not_read':['current71 BODY','rootmath verdict','anonymous decoder','new publication','root source summary','sourcefirst71 mathematical verdict or interface'],'technical_observer_failures_retained':['UTF-8 stdout fix after gbk read-only print failure','PID46568 EXIT1 wrapper invocation passed Python executable twice','PID4764 EXIT2 wrapper invocation used repeated relative script path'],'successful_read_actual_PIDs':[27308,42668],'no_prior_acceptance_substituted_for_current71_review':True})
write('stageA.bounded-synthesis71.frozen.json',{'schema':'source71-stageA-synthesis-v1','status':'STAGE_A_FROZEN_STAGE_B_OPEN','source_graph_nodes':22,'source_graph_edges':49,'RAW_regions':4,'source_math_items':255,'source_counts':counts,'exact_target_formulas':18,'source_obligations':24,'conclusion':'Freeze exact same-C B20/B21 actual-input expectations and real B28 consumer relationship before current71 implementation read. No final theorem/source verdict.','source_boundary':'New coefficient identity must be internally derived and applied to actual parent70 rotation. Keep six callers, twelve common witnesses, every old clause, rank0 and alpha eta1. B4 residual errors/dynamics/main/cost/composition remain open.','next_authorization':'Await official publication-bound StageB reviewer packet and blind reconstruction; do not inspect current71 BODY meanwhile.','canonical_Git_ledger_Goal_or_old_closed_writes':False})
outputs=[p for p in O.glob('stageA.*.frozen.json')]
freeze_pins=[pin(p) for p in sorted(outputs)]
bundle={'schema':'source71-stageA-small-complete-named-expectation-payload-v1','no_recursive_history_or_primary_fullfile_base64':True,'LF_recipe':'Replace ONLY CRLF byte pairs with LF. RAW authoritative.','primary_input_manifest':pin(O/'stageA.primary-input-pins.json'),'permitted_read_only_anchor_manifest':pin(O/'stageA.read-only-anchor-pins.json'),'frozen_named_records':{p.name:json.loads(p.read_bytes()) for p in sorted(outputs)},'frozen_RAW_pins':freeze_pins,'closure_policy':'StageA freeze is immutable within OPEN whole review; final CLOSED_LAST lease only after StageB. No current71 candidate BODY is included.'}
write('stageA.complete-named-expectations-input-payload71.json',bundle)
print(json.dumps({'actual_pid':os.getpid(),'status':'PASS_STAGE_A_SOURCE_ONLY','counts':counts,'nodes':22,'edges':49,'obligations':24,'target_formulas':18,'frozen_files':freeze_pins,'payload':pin(O/'stageA.complete-named-expectations-input-payload71.json')},ensure_ascii=False,indent=2))
