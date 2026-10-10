from pathlib import Path
from html.parser import HTMLParser
import json, hashlib, datetime, html, re

root=Path('E:/Samplinglib'); p=Path(__file__).parent
sha=lambda b:hashlib.sha256(b).hexdigest()
canon=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode('utf-8')
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def fp(path,b=None):
    path=Path(path);b=path.read_bytes() if b is None else b
    return dict(path=str(path).replace('\\','/'),raw_sha256=sha(b),lf_sha256=sha(b.replace(b'\r\n',b'\n')),bytes=len(b))
def write(path,x):
    assert not path.exists(),str(path)
    b=(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8');path.write_bytes(b);return fp(path,b)
def logical(x,field):x[field]=sha(canon(x));return x
leasepath=p/'reviewer.primary.lease.json';opening=leasepath.read_bytes();lease=json.loads(opening)
assert lease['status']=='OPEN'
src=root/'runs/20261007-companion-priority/next-ready-preread47/primary-pbps.raw.snapshot.html'
raw=src.read_bytes();assert sha(raw)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
assert (p/'primary.raw.snapshot.html').read_bytes()==raw
s=raw.decode('utf-8');lines=s.splitlines(keepends=True);offsets=[0]
for line in lines:offsets.append(offsets[-1]+len(line))
class Spans(HTMLParser):
    void={'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
    def __init__(self):super().__init__(convert_charrefs=False);self.stack=[];self.items={}
    def pos(self):a,b=self.getpos();return offsets[a-1]+b
    def handle_starttag(self,tag,attrs):
        start=self.pos();d=dict(attrs)
        if tag in self.void:
            if d.get('id'):self.items[d['id']]=(start,start+len(self.get_starttag_text()))
        else:self.stack.append((tag,d.get('id'),start))
    def handle_startendtag(self,tag,attrs):
        d=dict(attrs)
        if d.get('id'):self.items[d['id']]=(self.pos(),self.pos()+len(self.get_starttag_text()))
    def handle_endtag(self,tag):
        if not self.stack:return
        assert self.stack[-1][0]==tag,(tag,self.stack[-1])
        _,ident,start=self.stack.pop();end=s.index('>',self.pos())+1
        if ident:self.items[ident]=(start,end)
q=Spans();q.feed(s);assert not q.stack
ids=['S1.p1.1','S1.E1','S2.SS2.p1.1','S2.E6','S2.E7','S2.E8','S2.E14',
 'A2.E1','A2.E2','A2.E4','A2.SS1.p3.3','A2.SS2.p1.1','A2.E8','A2.SS2.p2.2','A2.E9','A2.E10','A2.E11',
 'A2.Thmtheorem1.p1.1','A2.E12','A2.Thmtheorem1.p2.1','A2.E13',
 'A3.SS1.p1.1','A3.SS1.p2.1','A3.Ex1','A3.SS1.p2.2','A3.Ex2','A3.SS1.p2.3','A3.E1',
 'A3.SS1.p3.1','A3.Ex3','A3.SS1.p3.2','A3.EGx24','A3.SS1.p3.3','A3.Ex5','A3.SS1.p3.4','A3.Ex6','A3.SS1.p3.5','A3.Ex7','A3.SS1.p3.6','A3.EGx25','A3.SS1.p3.7']
missing=[x for x in ids if x not in q.items];assert not missing,missing
fragdir=p/'primary.fragments';assert not fragdir.exists();fragdir.mkdir()
anchors=[]
for i,ident in enumerate(ids):
    a,b=q.items[ident];text=s[a:b];data=text.encode('utf-8')
    f=fragdir/f'{i:02d}.{ident}.raw.html';f.write_bytes(data)
    formulas=[html.unescape(x) for x in re.findall(r'alttext="([^"]*)"',text)]
    anchors.append(dict(source_item_id=ident,physical_start=s.count('\n',0,a)+1,physical_end=s.count('\n',0,b)+1,raw_fragment=fp(f,data),balanced_full_outer_span=True,formula_alttexts=formulas,interpretation='Literal primary evidence; neither Lean/API nor candidate topology'))
inventory=logical(dict(schema_version=1,reviewer='phase_source_reviewer_20261005',source=fp(src,raw),source_edition='arXiv2609.06905v1',anchors=anchors,anchor_count=len(anchors),coverage='Bounded standing/joint/operator/B13/C1 passage selection; not exhaustive whole-paper coverage',fragment_hash_rule='SHA256 literal balanced full-outer HTML UTF8 bytes; separate wholefile identity',sourcegraph_authored=False),'inventory_run_sha256')
invpin=write(p/'primary.anchor-inventory.json',inventory)
provenance=[fp(root/'.agents/skills/astis-semantic-roundtrip/SKILL.md'),fp(root/'runs/20261007-companion-priority/phase-pbps-primary-preread53/primary.contract.json')]
contract=dict(schema_version=1,reviewer='phase_source_reviewer_20261005',stage='OWN_PRIMARY_ONLY55_BEFORE_TARGET_API_BODY',status='CLOSED_SOURCE_ONLY_NO_STATEMENT_OR_PROOF_ADMISSION',source_edition='PBPS arXiv2609.06905v1',source_url='https://arxiv.org/html/2609.06905v1#A3.SS1',source_input=fp(src,raw),source_snapshot=fp(p/'primary.raw.snapshot.html'),anchor_inventory=invpin,source_read_opened_utc=lease['opened_utc'],source_read_completed_utc=now(),
 semantic_slots={
  'objects':'Same Gibbs mu=e^-V/ZV, J=law(X,X+sqrt(eta)Z), outer nu=J.snd, posterior R_y, reflected S_y=(2x-y)#R_y, literal compact mean T_f and its macroscopic L2(nu) class A=U_PP; B=U_perpP, Gamma_P=(I-A^2)^(1/2). A/B are convenient analytic names, not substituted source notation.',
  'domains':'Printed R^d; V C2 globally; signed smooth compact f for the estimate, then arbitrary f in L2(nu) for the B13 Sobolev class. Gradients/energies are outer-nu weighted, not volume-only or conditional-fiber norms.',
  'quantifiers':'Fix one actual source V/alpha/beta/eta and J/nu/R/S first; every compact smooth observer for the uniform estimate; then every L2(nu) observer via density/closedness. Source does not demand centering. Rough mean representatives are identified nu-AE, not guaranteed pointwise C1 everywhere.',
  'assumptions':'V C2, 0<alpha<=beta, alpha I<=HessV<=beta I, 0<eta<=1/beta. Probability/partitions/conditional laws/integrability/density/closed-gradient/approximation bounds are analytic ingredients, not new source caller certificates.',
  'conclusion':'Source B13: A f in H1(nu), 4eta*||gradient A f||_L2(nu)^2 <= ||f||^2-||A f||^2 = ||Gamma_P f||^2 = ||B f||^2. Current55 stage only reconstructs this endpoint and its missing passage; it proves/adopts no candidate interface.',
  'scopes':'Source C1 normalized covariance formula and C2 integrated estimate are compact-core starting points. Density/closedness passage, same-law L2 representative convergence and exact source H1 identification are separate obligations. No paper/main/error/work/Gamma implementation or future55 statement admission.',
  'constant_dependencies':'W_y=V((y+u)/2)+||y-u||^2/(8eta); posterior2eta vs reflected8eta; HessW=(HessV+eta^-1I)/4; conditional c_y=(eta^-1-alpha)^2/[4(alpha+eta^-1)]; integrated c=(1-alpha*eta)^2/[4(1+alpha*eta)] in eta||gradient Af||^2<=c||Bf||^2; 0<=c<=1/4 under source cap.'},
 binder_classification=[
  dict(binder='V:R^d->R C2; 0<alpha<=beta; global two-sided Hessian bounds',classification='SOURCE_STANDING',anchors=['S1.p1.1','S1.E1']),
  dict(binder='0<eta and beta*eta<=1',classification='SOURCE_STEP',anchors=['S2.SS2.p1.1','A2.Thmtheorem1.p1.1','A3.SS1.p3.3']),
  dict(binder='signed f in C_c^infty for smooth estimate; arbitrary f in L2(nu) for rough B13',classification='SOURCE_OBSERVER_CLASSES',anchors=['A3.SS1.p1.1','A2.Thmtheorem1.p2.1']),
  dict(binder='finite Hilbert/Borel/rank0 or C1 compact observer',classification='DISCLOSED_AUTHORED_EXTENSION_IF_LATER_SELECTED_NOT_PRINTED_STANDING'),
  dict(binder='supplied partitions/probability/law/gradient-domain/coherence/density/convergence/energy certificates',classification='NOT_SOURCE_BINDERS_MUST_BE_PRODUCED')],
 source_objects={
  'nu':'Outer marginal pi_eta^Y of actual J; both Y_plus and Y_minus have this law by exchangeability.',
  'R':'Every-y specified normalized density exp(-V(x)-||x-y||^2/(2eta))/ZR(y); arbitrary disintegrations alone are only nu-AE versions.',
  'S':'Every-y literal exp(-W_y(u))/ZS(y), affine same-R reflection; ZS=2^d ZR and inverse Jacobian2^-d.',
  'compact_mean':'T_f(y)=integral f(u)dS_y = E[f(Y_minus)|Y_plus=y], representing A f in L2(nu). C1/derivative facts for compact observers do not transport pointwise along arbitrary AE representatives.',
  'rough_mean':'For genuine L2 representative f, conditional integrability and mean definition hold nu-AE via same pair law/Fubini; a quotient class is not a pointwise function to differentiate. Everywhere finite or C1 for arbitrary rough f would be a separate stronger result.',
  'gradient_domain':'Source says H1(nu) and closedness of gradient, without defining a particular local Lean graph/domain. A graph-closure result must explicitly match the intended weighted Sobolev convention, not silently identify different domains.'},
 source_vs_reconstructed_passage={
  'literal_source':'A3.SS1.p1.1 physical4573-4576 states compact smooth suffices by density and closedness of gradient. It supplies no approximation/closed-graph proof detail.',
  'uniform_compact_estimate':'For each smooth compact f, eta||G_f||^2<=c||B f||^2; B9 identifies the RHS with expected conditional variance and norm defect. G_f is the actual derivative of the literal compact mean, internally in L2(nu).',
  'difference_estimate':'Necessary inferred application to compact f_n-f_m on SAME law: eta||G_n-G_m||^2<=c(||f_n-f_m||^2-||T_n-T_m||^2)<=c||f_n-f_m||^2. This is linearity plus printed estimate, not a separately printed theorem; no constants/centering added.',
  'function_convergence':'Conditional expectation under exchangeable pair gives ||T_n-T_f||_L2(nu)<=||f_n-f||_L2(nu). Identify limit with actual same-law mean class, not a new opaque existential output.',
  'gradient_convergence':'Difference bound gives gradient Cauchy and actual vector-L2 limit. Closedness then requires graph-domain membership of EACH T_n; T_n generally lacks compact support even if f_n is compact.',
  'smooth_mean_domain_admission':'Before closedness, prove genuine weighted C1 mean and both weighted L2 function/gradient admit the SAME original compact-smooth gradient closure, via a valid approximation/cutoff route or a justified distributional Sobolev characterization. Mere closability on compact functions is insufficient.',
  'limit_energy':'Use strong L2 convergence of f_n/T_n/G_n and actual norm-defect identities to pass the sharp scalar estimate. Obtain B13 using c<=1/4; Gamma equality requires its own already specified positive-operator identity, not manufactured from an energy estimate.',
  'H1_alignment':'Explicitly connect actual chosen closure gradient to source H1(nu) with representatives, weak derivative/domain convention and AE invariance. Source omits this background; do not use supplied final H1 certificate as a public premise.'},
 source_dependency_order=[
  '1. Fix original standing and actual normalized Gibbs/joint/outer laws; derive genuine positive partitions and probability.',
  '2. Fix same literal posterior/reflection law and compact mean; actual normalization/domination yields derivative and its continuity.',
  '3. Conditional Poincare, parameter-score variance and covariance CS give compact pointwise estimate; integrate under SAME nu using B9.',
  '4. Supply actual C_c^infty L2(nu) density and true graph-domain admission for noncompact T_n; preserve source H1 convention.',
  '5. Apply compact estimate to differences and conditional-mean contraction; produce strong L2 limits for function and gradient.',
  '6. Use SAME closed graph to identify rough mean class and gradient; pass strong norm limits and exact defect/Gamma identities.',
  '7. Keep rough source H1 alignment, operator/Gamma/half-turn/main/cost and any stronger pointwise rough regularity separately typed until genuinely produced.'],
 hidden_obligations=['Measurability and L1/L2 products before totalized integrals/covariance.', 'Compact smooth density on actual nu; no approximation sequence certificate added to source binders.', 'Every-y compact mean regularity differs from nu-AE rough integrability and quotient representatives.', 'Noncompact compact-observer means require actual original gradient-domain membership before applying closedness.', 'Gradient limit and energy must use the same nu and same domain fixed before observers.', 'No inferred equality between arbitrary alternative gradient closures or conditional kernel versions.', 'Rank0 extension must handle absence of unit vectors directly: gradients and energies vanish; no Nontrivial premise or observer-centering required.'],
 remaining_boundaries=['Future55 exact statement/binder/topology/proof and source fidelity', 'Actual all-L2 same-law mean/closed-gradient extension and exact source H1 adapter', 'Literal Gamma/CFC/operator/half-turn and paper main/errors/work/composition', 'Full-reader/PURIFIED/live delivery'],
 exposure={'prior52_and53_source_body_Test_roles_known':True,'historical_blindness_claimed':False,'fresh_primary55_passages_read':True,'preliminary_protocol_and_historical_primary53_contract_before_owned_lease_disclosed':True,'future55_candidate_API_body_decoder_verdict_read':False,'future54_packet_read':False,'sourcegraph_or_other_agent_preread55_read':False,'compiler_started':False,'math_verdict_as_source_used':False},
 execution_diagnosis=['First text-print helper omitted encoding and stopped at Windows GBK decoding; no source output or mathematical conclusion from that failed read. Repeated once with explicit UTF8 successfully.', 'Balanced-fragment inventory preflight rejected guessed A2.SS2.p1.2 before fragment/contract output. Actual primary line3725 is A2.SS2.p2.2; corrected the locator from literal source, no mathematical change.'],
 input_artifacts=[fp(src,raw)]+provenance,
 hash_recipe='review_run_sha256=SHA256 UTF8 sorted compact ensure_ascii=False entire contract minus review_run_sha256,allow_nan=False,no trailing newline.')
logical(contract,'review_run_sha256');contractpin=write(p/'primary.contract.json',contract)
assert src.read_bytes()==raw
run=logical(dict(schema_version=1,reviewer=contract['reviewer'],stage=contract['stage'],opened_utc=lease['opened_utc'],completed_utc=now(),input_artifacts=contract['input_artifacts'],opening_lease_snapshot=fp(p/'opening.lease.raw.snapshot.json'),outputs=[contractpin,invpin,fp(p/'primary.raw.snapshot.html'),fp(__file__)]+[x['raw_fragment'] for x in anchors],compiler_started=False,source_inputs_pre_post_identical=True,no_candidate_or_API_exposure=True,hash_recipe='run_sha256=SHA256 UTF8 sorted compact ensure_ascii=False entire object minus run_sha256,allow_nan=False,no trailing newline.'),'run_sha256')
runpin=write(p/'source.preread.run.json',run)
lease.update(status='CLOSED',read='CLOSED',write='CLOSED',Python='CLOSED',compiler='NOT_STARTED_CLOSED',closed_utc=now(),input_artifacts=contract['input_artifacts'],outputs=[contractpin,invpin,runpin],review_run_sha256=contract['review_run_sha256'],run_sha256=run['run_sha256'],compiler_started=False,hash_recipe='lease_run_sha256=SHA256 sorted compact ensure_ascii=False UTF8 entire lease minus lease_run_sha256,no newline,allow_nan=False.')
logical(lease,'lease_run_sha256');b=(json.dumps(lease,ensure_ascii=False,indent=2)+'\n').encode('utf-8');lp=fp(leasepath,b)
# Actual primary lease closure is the final filesystem operation.
leasepath.write_bytes(b)
print(json.dumps(dict(contract=contractpin,contract_logical=contract['review_run_sha256'],inventory=invpin,run=runpin,run_logical=run['run_sha256'],lease=lp,lease_logical=lease['lease_run_sha256'],all_roles_CLOSED=True,compiler='NOT_STARTED_CLOSED'),ensure_ascii=False))
