from pathlib import Path
import json, hashlib, re, sys, os, time, datetime
from html.parser import HTMLParser

BASE=Path('E:/Samplinglib')
OUT=BASE/'runs/20261007-companion-priority/pbps-macro-range-sourcegraph58'
PRIMARY=BASE/'runs/20261007-companion-priority/phase-pbps-gamma-preread57'
NEXT=BASE/'runs/20261007-companion-priority/phase-pbps-next-primary58'
start=time.time(); reads=[]; writes=[]
def digest(b): return hashlib.sha256(b).hexdigest()
def pin(p,b):
    q=b.replace(b'\r\n',b'\n')
    return dict(path=str(p).replace('\\','/'),bytes=len(b),raw_sha256=digest(b),lf_bytes=len(q),lf_sha256=digest(q))
def read(p):
    p=Path(p); b=p.read_bytes(); reads.append(pin(p,b)); return b
def load(p): return json.loads(read(p).decode('utf-8-sig'))
def write(name,obj):
    p=OUT/name
    if isinstance(obj,dict):
        obj=dict(obj); obj['content_self_sha256']=digest(json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
        b=(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode()
    elif isinstance(obj,str): b=obj.encode()
    else: b=obj
    p.write_bytes(b); writes.append(pin(p,b)); return pin(p,b)

if sys.argv[-1]=='--ids':
    for n in ['A2.SS1.raw.html','A3.SS1.raw.html','A4.SS1.raw.html']:
        print(n, re.findall(r'id="([^"]+)"',read(PRIMARY/n).decode()))
    sys.exit(0)

source=load(NEXT/'source.contract.json'); blueprint=load(NEXT/'next-edge.blueprint.json'); adoption=load(NEXT/'root.source-only58.adoption.json')
contracts=[load(PRIMARY/'primary.contract.json'),load(PRIMARY/'source.precision-addendum.json')]
manifest=load(NEXT/'input.manifest.json'); supplemental=load(NEXT/'supplemental.input.manifest.json')
historical={str(BASE/'docs/companion-papers-handoff.md').replace('\\','/'),str(BASE/'website/content/samplewiki_companion_frontiers.json').replace('\\','/'),str(BASE/'research-wiki/frontier-cells/ASTIS-SHARED-gaussian-marginal-poincare.json').replace('\\','/')}
checks=[]
for record in manifest['inputs']+supplemental['inputs']:
    for role in ['actual_input','exactraw_snapshot','crlf_to_lf_snapshot']:
        expected=record[role]
        if role=='actual_input' and expected['path'] in historical:
            checks.append(dict(role=role,status='historical-control-not-live-rechecked',expected=expected,immutable_mapping=record['exactraw_snapshot'])); continue
        actual=pin(Path(expected['path']),read(expected['path']))
        assert actual==expected,(role,expected,actual)
        checks.append(dict(role=role,status='strict-pin-pass',expected=expected,actual=actual))
for old,new in adoption['explicit_temporal_maps']:
    actual=pin(Path(new['path']),read(new['path'])); assert actual==new
    assert {k:v for k,v in old.items() if k!='path'}=={k:v for k,v in new.items() if k!='path'}
    checks.append(dict(role='full-row-temporal-map',status='pass',historical=old,immutable_snapshot=new))

nodes=[]
def node(i,anchor,kind,statement,status='SOURCE_NODE',ingredients=None):
    nodes.append(dict(id=i,anchor=anchor,kind=kind,statement=statement,status=status,proof_ingredients=ingredients or []))
node('S:model','S1.p1/p2;S2.SS2;2.6','standing/source-model','V is C2 on printed R^d, 0<alpha<=beta, alpha I<=Hess V<=beta I, eta>0, beta eta<=1; mu is normalized exp(-V) volume law; J=law(X,X+sqrt(eta)Z) with independent Gaussian Z; nu=J.snd.')
node('S:real-L2','D.1/D.2','definition/quotient','H=L2(J) is the complete REAL Hilbert space of AE classes, not finite dimensional. H0=ker(mean_J).')
node('S:P','B.1/D.1','definition/orthogonal-projection','Pf=E[f|Y], on the sigma algebra comap snd; P^2=P=P*, ran(P)=lpMeas(comap snd).')
node('S:M','B.2/D.1','definition/pullback','Canonical M:L2(nu)->L2(J), Mu=[u composed snd]; ||Mu||=||u||, real-linear, with AE J action.')
node('S:M-fixed','B.1/B.2','derived-pullback-inclusion','PM=M: a snd-pullback class is fixed by conditional expectation; ran(M) subset ran(P).')
node('BG:comap-representative','B.2 omitted quotient bookkeeping','mathlib-available','A class in lpMeas(comap snd) has an AE J equal representative g strongly measurable for comap snd. No arbitrary every-y representative equality.')
node('BG:Doob-Dynkin','B.2 omitted factorization','mathlib-available','For REAL target (nonempty, completely metrizable), strongly measurable g for comap snd factors as h composed snd for strongly measurable h. Fixed FactorsThrough exists_eq_measurable_comp; no additional StandardBorel assumption.')
node('BG:pushforward-Lp','B.2 omitted Lp transfer','mathlib-available','Since nu=map snd J, AE measurability and MemLp of h composed snd imply h in MemLp(2,nu), via memLp_map_measure_iff. Measurability is discharged from h and snd.')
node('S:M-onto','B.2','source-identification','ran(M)=ran(P); M is a real linear isometric equivalence L2(nu) to H_P=ran(P). Reverse inclusion constructs h in L2(nu), not a supplied caller certificate.')
node('S:mean-pullback','D.2/B.2','background integral transport','mean_J(Mu)=mean_nu(u), by actual probability pushforward and L2 integrability; alternatively pair with class 1.')
node('S:centered-onto','D.2/B.2/C.3','derived-subspace-identification','M maps the closed centered L2_0(nu) ONTO H_P,0=ran(P) intersect L2_0(J); onto identification and closedness are conclusions.')
node('S:U','B.4/2.14','actual-reflection','Uf=[f(x,2x-y)]; reflection preserves actual J and is an involution, hence real selfadjoint unitary.')
node('S:blocks','B.3/B.4','actual-compression','A=PUP restricted H_P; B=(I-P)UP:H_P->ker(P). The full joint PUP identity is P-A_full^2, not I-A_full^2.')
node('S:block-defect','B.5','source-identity','On H_P, B*B=I-A^2 and ||Bf||^2=||f||^2-||Af||^2 by orthogonal decomposition/unitarity.')
node('S:T-same','B.8/B.2/C.1','actual-scalar-intertwining','One uniform bounded scalar T on actual L2(nu), literal reflected conditional mean; same canonical M satisfies MT=AM. Operator choices identified from AE action, never a caller equality premise.')
node('S:centered-A','C.3/B.4/D.2','discharged-centering','A is selfadjoint and A1=1, so <1,Af>=<A1,f>=<1,f>=0. Equivalent actual stationarity/mean preservation is an alternative sufficient route, not another mandatory AND input.')
node('S:sharp-C2','C.1/C.2/density sentence','source-proof-predecessor','eta||G(Tu)||^2 <= (1-alpha eta)^2/[4(1+alpha eta)] (||u||^2-||Tu||^2), all rough L2 via accepted closed compact-gradient graph; full source weak H1 equality remains OPEN.')
node('S:marginal-PI','C.3;2.13;D.6/D.10','source-proof-predecessor','On centered closed-gradient domain under actual nu: ||v||^2 <= (1/alpha+eta)||Gv||^2. Actual curvature implies marginal PI; no public PI certificate.')
node('S:scalar-C4','C.3/C.4','source-contraction','For every u in centered L2(nu), ||Tu|| <= rho||u||, rho=(1-alpha eta)/(1+alpha eta), with SAME T/G/laws. Sharp C2 and PI yield rho by rearrangement.')
node('S:macro-C4','C.4','integration-target','For every f in H_P,0, choose unique centered u with Mu=f; ||Af||=||MTu||=||Tu||<=rho||u||=rho||f||.')
node('S:squared-gap','final C.1 paragraph proving B.15','integration-target','For every f in H_P,0, ||Bf||^2=||f||^2-||Af||^2 >= 4alpha eta/(1+alpha eta)^2 ||f||^2. No Gamma construction is needed for this squared predecessor.')
node('BG:positive-root','B.10/D.1/D.3','source-contract-gap','Construct unique bounded nonnegative selfadjoint Gamma=(I-A^2)^(1/2) on true potentially infinite real H_P; source invokes spectral theorem. No eta prefactor, no gradient/Laplacian resolvent.',status='OPEN_SOURCE_GAP')
node('S:Gamma-norm','B.11','later-consumer','After actual positive root construction, ||Gamma f||^2=||Bf||^2 for all H_P.',status='OPEN_CONSUMER')
node('S:Gamma-gap','B.15','later-consumer','Positive root monotonicity/spectral calculus gives Gamma >= 2sqrt(alpha eta)/(1+alpha eta) I on H_P,0.',status='OPEN_CONSUMER')
node('S:inverse-polar','B.16','later-consumer','Gamma inverse only on H_P,0 after positive gap; B Gamma^-1 is isometry INTO microscopic space, not onto.',status='OPEN_CONSUMER')
edges=[]
def edge(parents,target,use,route='AND',discharge=None): edges.append(dict(parents=parents,consumer=target,consumer_use_site=use,logic=route,discharged_conditions=discharge or []))
edge(['S:model'],'S:real-L2','D.1: actual probability J')
edge(['S:real-L2','S:model'],'S:P','B.1: conditional expectation on actual comap snd')
edge(['S:model','S:real-L2'],'S:M','B.2: nu actual marginal and AE pullback')
edge(['S:P','S:M'],'S:M-fixed','B.2 forward inclusion')
edge(['S:P'],'BG:comap-representative','B.2 reverse inclusion: lpMeas representative')
edge(['BG:comap-representative'],'BG:Doob-Dynkin','B.2 reverse inclusion: factor real measurable representative',discharge=['REAL nonempty/completely metrizable'])
edge(['BG:Doob-Dynkin','S:model'],'BG:pushforward-Lp','B.2 reverse inclusion: construct actual factor L2nu',discharge=['h strongly measurable','snd measurable','nu=map snd J'])
edge(['S:M-fixed','BG:pushforward-Lp','S:M'],'S:M-onto','B.2: equality of ranges, not inference from embedding')
edge(['S:M','S:model'],'S:mean-pullback','D.2 centered pullback: actual pushforward integral',discharge=['L2 under probability implies L1'])
edge(['S:M-onto','S:mean-pullback','S:real-L2'],'S:centered-onto','C.3: exact centered macro domain')
edge(['S:model','S:real-L2'],'S:U','B.4 actual reflection invariant law/involution')
edge(['S:P','S:U'],'S:blocks','B.3/B.4 actual same A/B restrictions')
edge(['S:blocks','S:U'],'S:block-defect','B.5 block-square/Pythagoras on H_P')
edge(['S:M','S:P','S:U'],'S:T-same','B.8 actual reflected conditional mean to MT=AM')
edge(['S:blocks','S:U'],'S:centered-A','C.3: selfadjoint and constant preserving',route='OR_ROUTE:selfadjoint-plus-constant')
edge(['S:T-same','S:mean-pullback','S:U'],'S:centered-A','C.3: actual stationarity transports mean preservation',route='OR_ROUTE:stationarity')
edge(['S:model','S:T-same'],'S:sharp-C2','C.1 score covariance, conditional PI, CS, density/closed graph; inherited source predecessors required')
edge(['S:model'],'S:marginal-PI','C.3: Hessian marginal bound2.13 via D.10 + D.6; inherited actual PI provider')
edge(['S:sharp-C2','S:marginal-PI','S:centered-A','S:T-same'],'S:scalar-C4','C.3/C.4: PI(Tu), same G domain from actual closure, rearrangement')
edge(['S:centered-onto','S:T-same','S:scalar-C4'],'S:macro-C4','C.4: choose centered preimage under actual M, transport norm')
edge(['S:macro-C4','S:block-defect','S:model'],'S:squared-gap','final C.1 B.15 proof: 1-rho^2=4alpha eta/(1+alpha eta)^2',discharge=['0<alpha eta<=1','1+alpha eta>0'])
edge(['S:block-defect','S:blocks'],'BG:positive-root','B.10/D.1: positive defect on full H_P; actual root construction OPEN')
edge(['BG:positive-root','S:block-defect'],'S:Gamma-norm','B.11 actual root square and norm identity')
edge(['S:squared-gap','BG:positive-root'],'S:Gamma-gap','B.15 monotonic positive root/spectral gap OPEN')
edge(['S:Gamma-gap','S:Gamma-norm'],'S:inverse-polar','B.16 centered inverse then polar isometry OPEN')

graph=dict(schema_version=1,actor='/root/source_graph58',source_id='arXiv:2609.06905v1',status='SOURCE_FIRST_SEALED_PENDING_INDEPENDENT_TOPOLOGY_REVIEW',candidate58_implementation_exposure=False,source_contract_pin=pin(NEXT/'source.contract.json',read(NEXT/'source.contract.json')),nodes=nodes,edges=edges,alternative_routes=[dict(target='S:centered-A',logic='OR',routes=['selfadjoint-plus-constant','stationarity'])],truth_boundary='Bounded source DAG only. No Lean/compiler/source-review admission. Full source weak H1 equality, actual Gamma positivity/root/inverse, C5-C7 lower bound, halfturn, dynamics, main, costs and actual-input composition remain OPEN.',endpoint_audit=dict(alpha_eta='(0,1] derived',rho='[0,1)',squared_gap='>0 and <=1',alpha_eta_one='rho=0; squared_gap=1; no division by 1-alpha eta',rank_zero='explicit finite real Hilbert extension; centered spaces may be {0}; no nonzero vector/finite-dimensional L2 assumption'),creator_validation=False)
write('source-proof-graph.json',graph)
write('pin-validation.json',dict(actual_checks=len(checks),checks=checks,parent_670_checks='Historical root adoption retained; this script reports only its own explicit checks.',historical_controls_not_frozen_live=True))
write('source-first-seal.json',dict(status='SEALED_BEFORE_PUBLIC_HEADERS',source_graph=pin(OUT/'source-proof-graph.json',read(OUT/'source-proof-graph.json')),source_anchors=[pin(PRIMARY/n,read(PRIMARY/n)) for n in ['A2.SS1.raw.html','A3.SS1.raw.html','A4.SS1.raw.html','A2.E10.raw.html','A2.E11.raw.html','A2.E15.raw.html','A2.E16.raw.html']],candidate58_exists=False,implementation_read=False,compiler='NOT_STARTED_CLOSED',standing='Exact mathematical source hypotheses remain binders; proof ingredients are edges.'))
write('source-first-run.json',dict(actor='/root/source_graph58',status='SOURCE_FIRST_STAGE_CLOSED',python_pid=os.getpid(),python_executable=sys.executable,foreground=True,started_utc=datetime.datetime.utcfromtimestamp(start).isoformat()+'Z',finished_utc=datetime.datetime.utcnow().isoformat()+'Z',wall_seconds=time.time()-start,reads=reads,writes=writes,compiler='NOT_STARTED_CLOSED',exit_code_intended=0,validation_authority='bookkeeping-only; independent topology review required'))
print(json.dumps(dict(status='SOURCE_FIRST_SEALED',nodes=len(nodes),edges=len(edges),pin_checks=len(checks),run=str(OUT/'source-first-run.json'))))
