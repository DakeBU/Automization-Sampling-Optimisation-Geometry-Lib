# -*- coding: utf-8 -*-
"""Seal source-only evidence; final write closes the real aggregate lease."""
from pathlib import Path
import hashlib,json,datetime,sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path('E:/Samplinglib');OUT=ROOT/'runs/20261007-companion-priority/gaussian-talagrand-next-leaf-preread46'
def sha(b):return hashlib.sha256(b).hexdigest()
def lf(b):return b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def write(name,obj): (OUT/name).write_bytes(enc(obj))
lease=json.loads((OUT/'lease.json').read_text(encoding='utf-8'));assert lease['state']=='OPEN'
bindings=json.loads((OUT/'input-bindings.json').read_text(encoding='utf-8'))
for sid,path,ranges in [('mathlib-manifest','lake-manifest.json',[(1,14)]),('toolchain','lean-toolchain',None)]:
    raw=(ROOT/path).read_bytes();rows=raw.splitlines(keepends=True)
    selected=raw if ranges is None else b''.join(b''.join(rows[a-1:b]) for a,b in ranges)
    (OUT/(sid+'.raw.snapshot.txt')).write_bytes(selected);(OUT/(sid+'.lf.snapshot.txt')).write_bytes(lf(selected))
    bindings['inputs'].append(dict(id=sid,path=path,whole_file_raw_sha256=sha(raw),whole_file_lf_sha256=sha(lf(raw)),selected_physical_ranges=ranges,raw_sha256=sha(selected),lf_sha256=sha(lf(selected)),raw_bytes=len(selected),lf_bytes=len(lf(selected))))
write('input-bindings.json',bindings)
checked=[]
for i in bindings['inputs']:
    raw=(ROOT/i['path']).read_bytes();ranges=i.get('selected_physical_ranges');rows=raw.splitlines(keepends=True)
    selected=raw if ranges is None else b''.join(b''.join(rows[a-1:b]) for a,b in ranges)
    if 'end_column_exclusive' in i:
        a,b=ranges[0];selected=b''.join(rows[a-1:b-1])+rows[b-1][:i['end_column_exclusive']-1]
    assert sha(selected)==i['raw_sha256'],i['id']
    assert sha(lf(selected))==i['lf_sha256'],i['id']
    assert (OUT/(i['id']+'.raw.snapshot.txt')).read_bytes()==selected,i['id']
    assert (OUT/(i['id']+'.lf.snapshot.txt')).read_bytes()==lf(selected),i['id']
    if 'whole_file_raw_sha256' in i:assert sha(raw)==i['whole_file_raw_sha256'],i['id']
    checked.append(dict(id=i['id'],raw_exact=True,lf_exact=True,source_unchanged=True))
write('input-validation.json',dict(status='PASS_SOURCE_BYTES_ONLY',checked=checked,compiler_used=False,proof_validation=False))
inventory=json.loads((OUT/'api-inventory.json').read_text(encoding='utf-8'))
prefix='AutoSamplingTheory.TechnicalLemmas.'
astis={'ConvexOpen':'Analysis.ConvexOpenAEDifferentiable','ConvexAC':'Analysis.ConvexDomainACAEDifferentiable','CouplingAE':'Measure.CouplingConvexDomainAE','RockafellarSupportGradient':'Analysis.PairingRockafellarSupportGradient','RockafellarRealDomain':'Analysis.PairingRockafellarRealDomain','MeasurableGradient':'Analysis.MeasurableGradient','Brenier':'Measure.QuadraticOptimalBrenierMap','PSD':'Measure.DisplacementConvexGradientPositive','MonotoneDerivative':'Measure.DisplacementMonotoneDerivative','DerivativeSymmetry':'Measure.DisplacementGradientDerivativeSymmetry','MapInjectivity':'Measure.DisplacementMapInjectivity','ChangeOfVariables':'Measure.DisplacementChangeOfVariables'}
for a in inventory['apis']:
    sid=a['id'].split('--')[0];name=a['name_as_printed']
    if sid in astis:q=prefix+astis[sid]+'.'+name
    elif sid=='Rademacher':q=name if '.' in name else ('LipschitzWith.' if name=='ae_differentiableAt_of_real' else 'LipschitzOnWith.')+name
    elif sid=='ConvexDeriv':q='ConvexOn.'+name
    else:q=name
    a['qualified_name']=q;a['resolution']='Exact namespace and ambient public source context; no compiler'
write('api-inventory.json',inventory)
opened=lease['opened_at_utc']
exposures=[
 'Earlier historical broad lookup exposed 41 reviewer/source metadata and decoder-binding original_text; not erased and not used as mathematical source.',
 'Earlier 42 preread oversized shared32 excerpt exposed provider body236-249; role is not fresh blind.',
 'Earlier44 Registry patterns exposed32/41/42 integration metadata; no43 forbidden proof or review read.',
 '46 initial TotalCount source-provider reads displayed ConvexOpen44-55, PSD45-53, Rademacher67-70 and75-78 proof snippets after headers. Shared background exposure only; no theorem/compilation credit.',
 '46 bounded declaration/namespace listings were sometimes truncated; exact later selected header snapshots supersede them. Guessed Convex/Derivative.lean lookup failed; corrected actual Convex/Deriv.lean path.',
 'Root status messages reported45 local compilation and43/42 integration statuses; these are metadata, not locally reread proof evidence.'
]
contract=dict(schema_version=1,actor='gaussian_noncompact_preread_42',stage='46 independent source/API uncertainty reduction',status='SOURCE_ONLY_TYPED_OBSTRUCTION_NO_SELF_ADMISSION',ownership=str(OUT).replace('\\','/'),source_first=dict(prior44_source_detail_sha256='5d39104950e6f6af067f17a382aa0deb12a6badeb42e810477a8c98c9771cf8f',prior44_contract_sha256='f29ad90cb5c01a85a5eae0524a33da069b7a8e69cffab6b5824093619405e60b',reuse='closed44 synthesis first; no broad restart',new_primary='Only1372-1385 and7403-7410 Caffarelli invocation/bibliography'),mathlib=dict(revision='db584cd6d46c92f209a44c0f1c829460d327499d',input_tag='v4.33.0',compiler_used=False),scope=dict(reads='Frozen44 capsule/contracts/selected background pages and narrow actual public shared/API source headers; primary selected Caffarelli excerpt',writes='Owned46 only',prohibited=['45 body/Tests/decoder/reviews/lessons/Gauss verdict','42/43 proof/DCT graph/lessons/reviews/blind/Tests','Lean compiler or proof search','Goal/SAU/cell/theorem claim','source graph expansion','canonical/shared edits','conditional desired-inequality wrapper','self source/topology/theorem admission']),exposures=exposures,leases=dict(actual_aggregate_open_before_read_write_python=opened,evidence='lease.open.raw.snapshot.json',roles=['read','write','Python-source-extraction-and-byte-validation'],compiler='CLOSED_NO_COMPILER_USE',note='One actual aggregate source lease authorized all three roles before first operation; no detached or fictitious historical sublease files. Final lease.json closes all three roles in the final filesystem write.'),input_bindings_sha256=sha((OUT/'input-bindings.json').read_bytes()),input_validation_sha256=sha((OUT/'input-validation.json').read_bytes()),api_inventory_sha256=sha((OUT/'api-inventory.json').read_bytes()),source_detail_md_sha256=sha((OUT/'source-detail.md').read_bytes()),capsule_sha256=sha((OUT/'capsule.md').read_bytes()))
write('sourcecontract.json',contract)
detail=dict(schema_version=1,status='STRICTLY_REDUCED_TYPED_OBSTRUCTION',source_facts=dict(true_target='actual coupling-infimum W2(mu,stdGaussian E)^2 <= 2 * canonical KL(mu||stdGaussian E), covarianceI',retained_domains='probability and P2; finiteKL and W2 before toReal; finite realHilbert including rank0',available_producers=['actual optimal coupling/Brenier literal map','measurable literal gradient','scalar potential ae first derivative under AC/effective-domain hypotheses'],conditional_consumers=['vector Rademacher needs genuine Lipschitz map','PSD needs global true potential derivative representation plus existing T derivative','Jacobian needs pointwise good-set derivative/PSD plus global monotone map'],source_specific='SPHMC S4.E10 invokes Caffarelli in both directions for actual smooth standardized RGO; external theorem not locally produced'),typed_blocker=dict(classes=['missing-vector-second-order-convex-or-monotone-operator-producer','total-gradient-representative/global-monotonicity-contract-mismatch'],retired_route='scalar convex ae derivative + measurability -> vector Rademacher -> PSD -> current Jacobian by bare API composition',strict_reduction='Missing derivative existence separated from PSD conditional algebra; global representative mismatch isolated by concrete convex reproducer; localized Jacobian/regular representative join required internally',smallest_genuine_missing_edge='Internally generated full-measure good-set second-order/relative or approximate gradient derivative with PSD and compatible Jacobian representative contract, or genuine Caffarelli regular map producer for special SPHMC RGO',source_precision='Original Alexandrov/monotone-operator or CAF00 theorem must be pinned and statement-reviewed before assigning a new producer; no newly sealed candidate in46'),authored_inferences=dict(convex_potential_not_gradient_lipschitz='phi=abs(x)^(3/2)',literal_gradient_not_global_monotone='phi=x^2/2+2x+abs(x); T(-1/2)=1/2,T(0)=0, inner product=-1/4',ae_equality_not_local_differentiability='identity changed to0 on rationals; equals identity a.e. but discontinuous away0',status='elementary source/API diagnostics, not compiled counterexample theorem or theorem approval'),family_and_rank=dict(rank0='internal zero case; no Nontrivial/dimensionpositive premise',arbitrary_finite_rank='scalar R->R result cannot stand in for vector theorem',family='no jointly measurable derivative/transport family produced',eta='no new upper bound or scaling assumption'),route_policy=dict(prospective_strategy=None,reason='No genuine producer found for the requested missing vector leaf; no <=7-step conditional wrapper route assigned',static_vs_dynamic='dynamic remains actual flow/dissipation/speed/convergence gap; not expanded here',SPHMC_consumer='canonicalKL numeric ingredient45 separate; eventual GaussianT2 to actualFIRST; no W2/FIRST/main/query-cost claim'),api_count=len(inventory['apis']),input_count=len(bindings['inputs']),independent_review_required=True,sourcecontract_sha256=sha((OUT/'sourcecontract.json').read_bytes()))
write('source-detail.json',detail)
closed_at=datetime.datetime.now(datetime.timezone.utc).isoformat()
closed=dict(lease,state='CLOSED',closed_at_utc=closed_at,compiler_lease='CLOSED_NO_COMPILER_USE',actual_roles=dict(read='CLOSED',write='CLOSED',python='CLOSED',compiler='CLOSED_NO_COMPILER_USE'),result='SOURCE_ONLY_REDUCED_OBSTRUCTION_NO_PROOF_NO_SELF_ADMISSION',closure_rule='This lease.json write is the final filesystem operation of46.')
closed_bytes=enc(closed)
outputs=[]
for p in sorted(OUT.iterdir()):
    if p.is_file() and p.name not in ['lease.json','run.json']:
        b=p.read_bytes();outputs.append(dict(path=p.name,raw_bytes=len(b),raw_sha256=sha(b),lf_sha256=sha(lf(b))))
run=dict(schema_version=1,stage='46 source-only static next-leaf API reduction',actor='gaussian_noncompact_preread_42',status='SOURCE_ONLY_OBSTRUCTION_PACKET_CLOSED',opened_at_utc=opened,closed_at_utc=closed_at,compiler_invocations=0,theorem_or_implementation_files=0,forbidden_parent_reads=0,self_admission=False,input_count=len(bindings['inputs']),header_count=len(inventory['apis']),output_bindings=outputs,actual_final_lease_sha256=sha(closed_bytes),actual_final_lease_lf_sha256=sha(lf(closed_bytes)),byte_validation='PASS exact raw/LF selected inputs, not Lean or theorem validation')
run_bytes=enc(run);(OUT/'run.json').write_bytes(run_bytes)
report={'packet':str(OUT).replace('\\','/'),'source_detail_sha256':sha((OUT/'source-detail.json').read_bytes()),'contract_sha256':sha((OUT/'sourcecontract.json').read_bytes()),'run_sha256':sha(run_bytes),'closed_lease_sha256':sha(closed_bytes),'input_count':len(bindings['inputs']),'header_count':len(inventory['apis']),'compiler_used':False,'status':'source-only strictly reduced obstruction'}
# No filesystem reads or writes may follow this final actual close.
(OUT/'lease.json').write_bytes(closed_bytes)
print(json.dumps(report,ensure_ascii=False))
