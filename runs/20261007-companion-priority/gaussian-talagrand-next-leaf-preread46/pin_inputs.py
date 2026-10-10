# -*- coding: utf-8 -*-
"""Source-only extraction. Never calls Lean and never reads paper result bodies."""
from pathlib import Path
import json, hashlib, re, subprocess, sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path('E:/Samplinglib')
OUT = ROOT / 'runs/20261007-companion-priority/gaussian-talagrand-next-leaf-preread46'
def sha(b): return hashlib.sha256(b).hexdigest()
def lf(b): return b.replace(b'\r\n', b'\n').replace(b'\r', b'\n')
def write(name, b): (OUT/name).write_bytes(b)
assert json.loads((OUT/'lease.json').read_text(encoding='utf-8'))['state'] == 'OPEN'
write('lease.open.raw.snapshot.json', (OUT/'lease.json').read_bytes())
inputs, apis = [], []
def pin_slice(sid, path, ranges):
    raw = (ROOT/path).read_bytes(); rows = raw.splitlines(keepends=True)
    selected = b''.join(b''.join(rows[a-1:b]) for a,b in ranges)
    write(sid+'.raw.snapshot.txt',selected); write(sid+'.lf.snapshot.txt',lf(selected))
    inputs.append(dict(id=sid,path=path,whole_file_raw_sha256=sha(raw),whole_file_lf_sha256=sha(lf(raw)),selected_physical_ranges=ranges,raw_sha256=sha(selected),lf_sha256=sha(lf(selected)),raw_bytes=len(selected),lf_bytes=len(lf(selected))))
def pin_file(sid,path):
    raw=(ROOT/path).read_bytes();write(sid+'.raw.snapshot.txt',raw);write(sid+'.lf.snapshot.txt',lf(raw))
    inputs.append(dict(id=sid,path=path,raw_sha256=sha(raw),lf_sha256=sha(lf(raw)),raw_bytes=len(raw),lf_bytes=len(lf(raw)),scope='frozen prior source/API synthesis; no proof'))
prior='runs/20261007-companion-priority/gaussian-talagrand-preread44/'
for name in ['capsule.md','source-detail.json','sourcecontract.json','input-bindings.json']:
    pin_file('prior44-'+name.replace('.','-'),prior+name)
for p in [45,46,60,61]:
    pin_file('prior44-chewi-page%03d'%p,prior+'chewi-page%03d.lf.snapshot.txt'%p)
pin_slice('primary-caffarelli','runs/20261007-companion-priority/gaussian-canonical-kl-fisher-preread43/primary.raw.snapshot.html',[(1372,1385),(7403,7410)])
A='AutoSamplingTheory/TechnicalLemmas/Analysis/'
M='AutoSamplingTheory/TechnicalLemmas/Measure/'
C='.lake/packages/mathlib/Mathlib/Analysis/Calculus/'
V='.lake/packages/mathlib/Mathlib/Analysis/Convex/'
specs=[
('ConvexOpen',A+'ConvexOpenAEDifferentiable.lean',[(24,35)],['ae_differentiableAt_of_convexOn_isOpen']),
('ConvexAC',A+'ConvexDomainACAEDifferentiable.lean',[(16,29)],['ae_differentiableAt_of_convexOn_of_absolutelyContinuous']),
('CouplingAE',M+'CouplingConvexDomainAE.lean',[(19,35)],['ae_fst_mem_interior_and_differentiableAt']),
('RockafellarSupportGradient',A+'PairingRockafellarSupportGradient.lean',[(18,32)],['eq_gradient_of_properSupportsAt_of_mem_interior','snd_eq_gradient_of_mem_of_mem_interior']),
('RockafellarRealDomain',A+'PairingRockafellarRealDomain.lean',[(22,36)],['convexOn_finitePart_effectiveDomain']),
('MeasurableGradient',A+'MeasurableGradient.lean',[(16,27)],['measurable_gradient']),
('Brenier',M+'QuadraticOptimalBrenierMap.lean',[(33,58)],['ae_snd_eq_gradient_of_quadraticOptimal_of_base','exists_base_map_gradient_eq_of_quadraticOptimal','exists_base_map_gradient_eq_of_quadraticOptimal_p2ac']),
('PSD',M+'DisplacementConvexGradientPositive.lean',[(25,34),(57,60)],['isPositive_fderiv_of_convex_gradient_field','toMatrix_fderiv_posSemidef_of_convex_gradient_field']),
('MonotoneDerivative',M+'DisplacementMonotoneDerivative.lean',[(29,37)],['inner_fderiv_nonneg_of_monotone','isPositive_fderiv_of_monotone_of_isSymmetric']),
('DerivativeSymmetry',M+'DisplacementGradientDerivativeSymmetry.lean',[(26,33)],['isSymmetric_fderiv_of_gradient_field']),
('MapInjectivity',M+'DisplacementMapInjectivity.lean',[(25,37)],['injective_affineDisplacementMap_of_monotone']),
('ChangeOfVariables',M+'DisplacementChangeOfVariables.lean',[(24,40)],['integral_image_affineDisplacementMap_eq_integral_det_smul']),
('Rademacher',C+'Rademacher.lean',[(49,58),(73,73),(333,335)],['ae_differentiableAt_of_real','ae_differentiableWithinAt_of_mem','ae_differentiableWithinAt','LipschitzWith.ae_differentiableAt']),
('Monotone',C+'Monotone.lean',[(27,31)],['Monotone.ae_hasDerivAt','Monotone.ae_differentiableAt','MonotoneOn.ae_differentiableWithinAt_of_mem','MonotoneOn.ae_differentiableWithinAt']),
('Gradient',C+'Gradient/Basic.lean',[(49,53),(82,83)],['gradient_eq_zero_of_not_differentiableAt','Filter.EventuallyEq.gradient_eq','HasGradientWithinAt.congr']),
('ConvexContinuous',V+'Continuous.lean',[(19,23)],['ConvexOn.lipschitzOnWith_of_abs_le','ConvexOn.exists_lipschitzOnWith_of_isBounded']),
('ConvexDeriv',V+'Deriv.lean',[(418,420)],['monotoneOn_derivWithin','monotoneOn_deriv']),
]
for sid,path,contexts,names in specs:
    raw=(ROOT/path).read_bytes(); rows=raw.splitlines(keepends=True); text=raw.decode('utf-8'); offsets=[];acc=0
    for row in rows: offsets.append(acc);acc+=len(row.decode('utf-8'))
    for name in names:
        pattern=r'^(?:protected |noncomputable |private )?(?:theorem|lemma) '+re.escape(name)+r'(?=[\s{(:])'
        matches=list(re.finditer(pattern,text,re.M));assert len(matches)==1,(sid,name,len(matches))
        start=matches[0].start(); end=text.index(':=',start)
        bodyfree=text[start:end].rstrip()+'\n'
        line1=text[:start].count('\n')+1;line2=text[:end].count('\n')+1
        # Retain original byte line endings in raw header; stop before proof delimiter.
        raw_start=sum(len(x) for x in rows[:line1-1]);raw_end=sum(len(x) for x in rows[:line2-1])
        raw_end += rows[line2-1].index(b':=')
        header=raw[raw_start:raw_end]
        hid=sid+'--'+name.replace('.','_')
        write(hid+'.raw.snapshot.txt',header);write(hid+'.lf.snapshot.txt',lf(header))
        inputs.append(dict(id=hid,path=path,whole_file_raw_sha256=sha(raw),whole_file_lf_sha256=sha(lf(raw)),selected_physical_ranges=[[line1,line2]],end_column_exclusive=rows[line2-1].index(b':=')+1,raw_sha256=sha(header),lf_sha256=sha(lf(header)),raw_bytes=len(header),lf_bytes=len(lf(header)),proof_body_read=False))
        apis.append(dict(id=hid,name_as_printed=name,file=path,physical_span=[line1,line2],header_lf_sha256=sha(lf(header)),context_id=sid+'-context' if contexts else None))
        print(hid+' ['+str(line1)+'-'+str(line2)+']\n'+bodyfree)
    if contexts: pin_slice(sid+'-context',path,contexts)
# Exact definitional content, not theorem proofs.
pin_slice('finitePart-definition',A+'PairingRockafellarRealDomain.lean',[(35,36)])
pin_slice('gradient-definition',C+'Gradient/Basic.lean',[(82,83)])
pin_slice('IsMonotoneMap-definition',M+'DisplacementMapInjectivity.lean',[(36,37)])
cmd=['rg','-n',r'Alexandrov|Alexandroff|Caffarelli|ae_differentiableAt.*monotone|Monotone.*ae_differentiableAt',A,M,V,C,'-g','*.lean']
p=subprocess.run(cmd,cwd=str(ROOT),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
write('bounded-search.stdout.txt',p.stdout);write('bounded-search.stderr.txt',p.stderr)
write('bounded-search.json',json.dumps(dict(argv=cmd,exit_code=p.returncode,scope='Only four named Analysis/Measure convex/calculus provider directories; no universal absence claim',stdout_sha256=sha(p.stdout),stderr_sha256=sha(p.stderr)),indent=2).encode()+b'\n')
write('input-bindings.json',json.dumps(dict(schema_version=1,inputs=inputs),ensure_ascii=False,indent=2).encode('utf-8')+b'\n')
write('api-inventory.json',json.dumps(dict(schema_version=1,apis=apis,kind='Source header inventory, not compiled declaration validation'),ensure_ascii=False,indent=2).encode('utf-8')+b'\n')
print('PINNED',len(inputs),'inputs;',len(apis),'public headers; compiler NOT USED')
