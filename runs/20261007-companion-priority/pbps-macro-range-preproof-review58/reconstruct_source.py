import json, hashlib, os, re, html, datetime
from pathlib import Path

B = Path('E:/Samplinglib/runs/20261007-companion-priority/pbps-macro-range-preproof-review58')
P = Path('E:/Samplinglib/runs/20261007-companion-priority/phase-pbps-next-primary58')
B.mkdir(parents=True, exist_ok=True)
def stamp(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def digest(b): return hashlib.sha256(b).hexdigest()
def receipt(p):
    b=Path(p).read_bytes(); l=b.replace(b'\r\n',b'\n')
    return dict(path=str(p).replace('\\','/'), bytes=len(b), raw_sha256=digest(b), lf_bytes=len(l), lf_sha256=digest(l))
def write(name,o):
    (B/name).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
write('lease.open.json',dict(actor='/root/statement_topology58',pid=os.getpid(),opened=stamp(),status='OPEN',sole_write_scope=str(B),compiler='NOT_STARTED',statement_and_topology_only=True))
pins=[]
contract=json.loads((P/'source.contract.json').read_text(encoding='utf-8'))
def check_records(x):
    if isinstance(x,dict):
        if all(k in x for k in ['path','raw_sha256','lf_sha256','bytes','lf_bytes']):
            got=receipt(x['path']); assert all(got[k]==x[k] for k in ['bytes','raw_sha256','lf_bytes','lf_sha256']),x['path'];pins.append(got)
        else:
            for v in x.values():check_records(v)
    elif isinstance(x,list):
        for v in x:check_records(v)
check_records(contract)
for n in ['input.manifest.json','supplemental.input.manifest.json']:
    obj=json.loads((P/n).read_text(encoding='utf-8'))
    for e in obj['inputs']:
        for key in ['exactraw_snapshot','crlf_to_lf_snapshot']:
            if key in e:check_records(e[key])
raw=Path(contract['source']['fixed_raw_primary']['path']).read_bytes()
(B/'primary.exactraw.snapshot.html').write_bytes(raw)
(B/'primary.crlf-to-lf.snapshot.html').write_bytes(raw.replace(b'\r\n',b'\n'))
s=raw.decode('utf-8')
def section(anchor):
    start=re.search(r'<section\b[^>]*\bid="'+re.escape(anchor)+r'"[^>]*>',s)
    assert start,anchor
    depth=0
    for t in re.finditer(r'</?section\b[^>]*>',s[start.start():]):
        depth+= -1 if t.group().startswith('</') else 1
        if not depth:return s[start.start():start.start()+t.end()]
    raise AssertionError(anchor)
def textof(r):
    r=re.sub(r'<math\b[^>]*\balttext="([^"]*)"[^>]*>.*?</math>',lambda m:html.unescape(m.group(1)),r,flags=re.S)
    r=re.sub(r'<[^>]+>',' ',r)
    return re.sub(r'\s+',' ',html.unescape(r)).strip()
anchors=['S1','S2.SS2','A2.SS1','A2.SS2','A3.SS1','A4.SS1']
anchor_records=[]
for a in anchors:
    r=section(a);(B/(a+'.raw.html')).write_text(r,encoding='utf-8');(B/(a+'.text.txt')).write_text(textof(r)+'\n',encoding='utf-8')
    anchor_records.append(dict(anchor=a,raw=receipt(B/(a+'.raw.html')),text=receipt(B/(a+'.text.txt'))))
own=dict(schema_version=1,actor='/root/statement_topology58',source_first=True,read_time=stamp(),pid=os.getpid(),creator_graph_or_signatures_read=False,primary=receipt(B/'primary.exactraw.snapshot.html'),pinchecks=pins,anchor_records=anchor_records,
    mathematical_reconstruction=[
      dict(id='R1',anchor='2.6;B.1;B.2;D.1-D.2',claim='Actual J is joint Gibbs plus independent Gaussian augmentation; nu=J.snd. P is conditional-Y orthogonal projection. ran P consists exactly of AE classes g composed with snd for g in real L2(nu). Forward inclusion is insufficient.'),
      dict(id='R2',anchor='B.2;D.1-D.2',claim='For M the measure-preserving snd pullback, integral_J M u=integral_nu u. Hence M identifies centered L2(nu) with ran P intersect centered L2(J). Quotient representatives only require AE equality; no every-fiber equality for arbitrary rough u.'),
      dict(id='R3',anchor='B.4;B.5;B.8-B.9',claim='Reflection U is self-adjoint unitary. A=PUP and B=(I-P)UP. On ran P, ||Bf||^2=||f||^2-||Af||^2. On whole joint space the operator identity has P rather than I.'),
      dict(id='R4',anchor='C.1-C.4;B.13-B.14',claim='Marginal PI applied to actual centered Af and sharp conditional score-gradient energy produce rho=(1-alpha eta)/(1+alpha eta) contraction. The source constants-preservation sentence needs preceding self-adjointness; constants preservation alone does not establish centering. Stationarity plus integrability is an alternative sufficient route and must be identified separately.'),
      dict(id='R5',anchor='C.1 final paragraph;B.15',claim='For centered macro f, squared-defect gap is 4 alpha eta/(1+alpha eta)^2 ||f||^2 <= ||B f||^2. This precursor requires neither construction nor invertibility of Gamma. Printed Gamma=sqrt(I-A^2) remains an additional real potentially infinite-dimensional spectral obligation.'),
      dict(id='R6',anchor='S1 standing assumptions;S2.SS2;D.1',claim='V C2, global alpha/beta Hessian sandwich, 0<alpha<=beta, eta>0, beta eta<=1. Ambient finite real Hilbert Borel formulation extends Euclidean notation including rank zero; L2 itself is potentially infinite dimensional. alpha eta=1 yields rho=0 and squared gap=1; no division by 1-alpha eta, no nonzero centered-space requirement.')],
    omitted_background=[dict(id='R7',anchor='B.2',claim='Reverse range requires Doob-Dynkin factorization of a comap strongly measurable representative and MemLp transfer, not an assumed range or measurable factorization certificate.')],
    exclusions=['No Gamma square root/inverse/polar map construction','No full weak-H1 identification','No full B.14 lower spectral bound','No paper/Goal completion','No proof compilation/admission'])
write('independent-source-reconstruction.json',own)
print(json.dumps(dict(pid=os.getpid(),pinchecks=len(pins),anchors=anchors,source_first_output=receipt(B/'independent-source-reconstruction.json'),exit_intended=0)))
