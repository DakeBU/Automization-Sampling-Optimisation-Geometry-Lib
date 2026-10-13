# -*- coding: utf-8 -*-
from pathlib import Path
import json,hashlib,datetime,sys
sys.stdout.reconfigure(encoding='utf-8')
R=Path('E:/Samplinglib');O=R/'runs/20261007-companion-priority/pbps-conditional-gradient-sourcegraph48'
def sha(b):return hashlib.sha256(b).hexdigest()
def lf(b):return b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def write(n,x):(O/n).write_bytes(enc(x))
lease=json.loads((O/'lease.json').read_text(encoding='utf-8-sig'));assert lease['state']=='OPEN'
binding=json.loads((O/'input-bindings.json').read_text(encoding='utf-8'));checks=[]
for i in binding['inputs']:
 raw=(R/i['path']).read_bytes();assert sha(raw)==i['whole_raw_sha256'] and sha(lf(raw))==i['whole_lf_sha256'],i['id'];rows=raw.splitlines(keepends=True);ranges=i['selected_physical_ranges']
 if i.get('end_column_exclusive'):
  a,b=ranges[0];part=b''.join(rows[a-1:b-1])+rows[b-1][:i['end_column_exclusive']-1]
 else:part=b''.join(b''.join(rows[a-1:b]) for a,b in ranges)
 assert sha(part)==i['fragment_raw_sha256'] and sha(lf(part))==i['fragment_lf_sha256'],i['id']
 assert (O/(i['id']+'.raw.snapshot.txt')).read_bytes()==part and (O/(i['id']+'.lf.snapshot.txt')).read_bytes()==lf(part),i['id'];checks.append(dict(id=i['id'],raw_exact=True,lf_exact=True,original_unchanged=True))
sealpath='runs/20261007-companion-priority/pbps-conditional-gradient-preproof48/statement-seals.accepted.json';sealraw=(R/sealpath).read_bytes();seal=json.loads(sealraw.decode('utf-8-sig'));sig=seal['signatures'][0];assert sig['LF_bytes']==1356 and sig['signature_lf_sha256']=='770bb0bac75b2f2c94fc72e68c1a5a19a1d4642cd2fcf15ea71b9aa608a65e61'
(O/'statement-seals.accepted.raw.snapshot.json').write_bytes(sealraw);(O/'statement-seals.accepted.lf.snapshot.json').write_bytes(lf(sealraw))
binding['statement_seal']=dict(path=sealpath,raw_sha256=sha(sealraw),lf_sha256=sha(lf(sealraw)),kind='independent statement-only admission; not48 graph/proof admission');write('input-bindings.json',binding)
graph=json.loads((O/'source-proof-graph.json').read_text(encoding='utf-8'));coverage=json.loads((O/'source-coverage.json').read_text(encoding='utf-8'));inventory=json.loads((O/'caller-inventory.json').read_text(encoding='utf-8'));tokens=json.loads((O/'selected-token-inventory.json').read_text(encoding='utf-8'))
write('input-validation.json',dict(status='PASS_RAW_LF_SELECTED_BYTES_AND_SCHEMA_ONLY',checks=checks,coverage_rows=coverage['total_rows'],physical_partition_unique=True,statement_seal_same_exact1356=True,topology_admission=False,theorem_verification=False,compiler_used=False))
hypotheses=[
 dict(binder='E and structural instances',source='R^d Euclidean in1.1; C.1 unit projection/norm',class_='AUTHORED_CARRIER_EXTENSION',detail='finite realHilbert/Borel including rank0; completeness internally derived; no positive dimension/Nontrivial'),
 dict(binder='V alpha beta eta',source='1.1 and2.7 setup',class_='SOURCE_DATA',detail='NNReal alpha beta represent source positive real curvature; eta real'),
 dict(binder='h_alpha',source='1.1',class_='SOURCE_HYPOTHESIS',formula='0<alpha'),
 dict(binder='h_alpha_beta',source='1.1',class_='SOURCE_HYPOTHESIS',formula='alpha<=beta'),
 dict(binder='hV',source='1.1',class_='SOURCE_HYPOTHESIS',formula='V C2 globally'),
 dict(binder='hH',source='1.1',class_='SOURCE_HYPOTHESIS',formula='alpha norm(a)^2 <= D2V(x)[a,a] <= beta norm(a)^2'),
 dict(binder='h_eta',source='eta in(0,1/beta] before2.6',class_='SOURCE_HYPOTHESIS',formula='eta>0'),
 dict(binder='h_beta_eta',source='eta in(0,1/beta] and explicit C.1 before Ex5',class_='SOURCE_HYPOTHESIS',formula='beta eta<=1'),
 dict(binder='f, C-infinity and compact',source='C.1 initial reduction4574-4576',class_='PRINTED_SCOPED_OBSERVER',detail='universally quantified after common R/S, no rough-domain completion'),
 dict(binder='y',source='pointwise C.1',class_='SOURCE_UNIVERSAL_PARAMETER',detail='actual positive normalized conditional version at every y'),
]
write('hypothesis-contract.json',dict(schema_version=1,hypotheses=hypotheses,outputs_not_public_hypotheses=['literal mu/J definitions','actual Markov R/S and conditional/reflection/density equations','actual T_f derivatives','S_y probability and score/f analytic domains','same S witness equality','scalar covariance CS and norm estimate','desired gradient variance bound'],true_constant='(1/eta-alpha)^2/(4*(alpha+1/eta))',source_definition_map=dict(mu='normalized Gibbs',J='actual2.7 independent Gaussian map',R='actual2.8 backward conditional',S='actual law Y-minus given Y-plus via2X-Y-plus',T_f='B.9 first identity U_PP f(y)=E[f(Y-minus)|Y-plus=y]',score='C.1 parameter-y score, vector/dual Riesz correspondence',variance='actual centered-square probability integral',gradient='actual Riesz inverse of true fderiv, not default0 outside domain'),family='same measurable R/S before all f/y; no joint gradient-selector claim',rank0='authored internally handled extension; no unit-existence premise'))
contract=dict(schema_version=1,stage='48 independent bounded source graph',actor='gaussian_noncompact_preread_42',status='CREATED_AWAITING_DISTINCT_TOPOLOGY_REVIEW',source_before_target_contract_sha256=sha((O/'source-before-target.contract.json').read_bytes()),statement_seal_raw_sha256=sha(sealraw),target_lf_sha256=sig['signature_lf_sha256'],graph_sha256=sha((O/'source-proof-graph.json').read_bytes()),coverage_sha256=sha((O/'source-coverage.json').read_bytes()),caller_inventory_sha256=sha((O/'caller-inventory.json').read_bytes()),token_inventory_sha256=sha((O/'selected-token-inventory.json').read_bytes()),inputs_sha256=sha((O/'input-bindings.json').read_bytes()),expansion_boundary='Selected primary through pointwise Ex7 with necessary source references, two opaque actual public parents and narrow definitions/API contracts; not whole PBPS or parent implementation',exposures=['Historical41 metadata/decoder-binding original_text, earlier shared32 snippet,44metadata,46provider snippets and47control45status/path metadata are retained in immutable originals; not fresh blind.','48 read only independent StatementSeal metadata/signature, not its reviewer/typecheck artifacts.','48 viewing frozen47 Riesz-type snapshot accidentally exposed the first background toDual definition proof lines137-139 (intro/set Y); selected48 Riesz contract now ends before := on135. No parent production proof/48implementation/Test/review/decoder read.','A guessed LinearIsometryEquiv.lean file did not exist; exact norm_map was found in LinearIsometry.lean. One Y-minus regex failed due braces and was replaced by literal search; no mathematical inference from failures.','Initial primary plaintext preview stripped a less-than-containing TeX fragment while removing HTML; all exact raw/LF fragments remain authoritative, and the raw source1.1/math assertions are retained.'],self_topology_admission=False,compiler_invocations=0,claims=0,canonical_edits=0,proof_files_read=False,actual_lease=dict(opened_at_utc=lease['opened_at_utc'],roles='real read/write/Python OPEN before reads and closed by final filesystem write',compiler='CLOSED_NO_COMPILER_USE'))
write('sourcecontract.json',contract)
closed_at=datetime.datetime.now(datetime.timezone.utc).isoformat();closed=dict(lease,state='CLOSED',closed_at_utc=closed_at,actual_roles=dict(read='CLOSED',write='CLOSED',python='CLOSED',compiler='CLOSED_NO_COMPILER_USE'),result='source graph authored; distinct topology admission required; no theorem/proof approval',closure='Final filesystem operation; no reads or writes follow.')
closed_bytes=enc(closed);outputs=[]
for p in sorted(O.iterdir()):
 if p.is_file() and p.name not in ['lease.json','run.json']:
  b=p.read_bytes();outputs.append(dict(path=p.name,raw_bytes=len(b),raw_sha256=sha(b),lf_sha256=sha(lf(b))))
run=dict(schema_version=1,stage='48 independent source graph',actor='gaussian_noncompact_preread_42',status='CREATED_CLOSED_AWAITING_DISTINCT_TOPOLOGY_REVIEW',opened_at_utc=lease['opened_at_utc'],closed_at_utc=closed_at,node_count=len(graph['nodes']),edge_count=len(graph['edges']),coverage_rows=coverage['total_rows'],NODE=coverage['NODE'],EXCLUDED=coverage['EXCLUDED'],caller_count=len(inventory['records']),selected_name_occurrence_count=len(tokens['records']),input_count=len(binding['inputs']),compiler_invocations=0,implementation_used=False,source_topology_self_admitted=False,output_bindings=outputs,actual_closed_lease_sha256=sha(closed_bytes))
run_bytes=enc(run);(O/'run.json').write_bytes(run_bytes)
report=dict(folder=str(O).replace('\\','/'),graph_sha256=sha((O/'source-proof-graph.json').read_bytes()),contract_sha256=sha((O/'sourcecontract.json').read_bytes()),run_sha256=sha(run_bytes),closed_lease_sha256=sha(closed_bytes),nodes=len(graph['nodes']),edges=len(graph['edges']),coverage_rows=coverage['total_rows'],NODE=coverage['NODE'],EXCLUDED=coverage['EXCLUDED'],callers=len(inventory['records']),tokens=len(tokens['records']),status='CREATED_CLOSED_AWAITING_DISTINCT_TOPOLOGY_REVIEW')
# Last filesystem operation closes all actual source-only leases.
(O/'lease.json').write_bytes(closed_bytes)
print(json.dumps(report,ensure_ascii=False))
