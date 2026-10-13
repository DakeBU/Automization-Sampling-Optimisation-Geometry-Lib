# -*- coding: utf-8 -*-
from pathlib import Path
import json,hashlib,datetime,sys
sys.stdout.reconfigure(encoding='utf-8')
R=Path('E:/Samplinglib');O=R/'runs/20261007-companion-priority/next-ready-preread47'
def sha(b):return hashlib.sha256(b).hexdigest()
def lf(b):return b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def write(name,obj):(O/name).write_bytes(enc(obj))
lease_raw=(O/'lease.json').read_bytes();lease=json.loads(lease_raw.decode('utf-8-sig'));assert lease['state']=='OPEN';(O/'lease.open.raw.snapshot.json').write_bytes(lease_raw)
public=json.loads((O/'public-input-bindings.json').read_text(encoding='utf-8'))
primitives=json.loads((O/'primitive-input-bindings.json').read_text(encoding='utf-8'))
checks=[]
for i in public:
 raw=(R/i['path']).read_bytes();assert sha(raw)==i['whole_raw_sha256'],i['id']
 saved=(O/(i['id']+'.public.raw.txt')).read_bytes();assert saved in raw and sha(saved)==i['raw_sha256'];assert (O/(i['id']+'.public.lf.txt')).read_bytes()==lf(saved)
 assert sha(lf(saved))==i['lf_sha256'];assert b':= by' not in saved
 checks.append(dict(id=i['id'],status='EXACT_COMPLETE_PUBLIC_HEADER_RAW_LF',physical_span=i['physical_span']))
for i in primitives:
 raw=(R/i['path']).read_bytes();ranges=i.get('physical_ranges')
 if 'whole_raw_sha256' in i:assert sha(raw)==i['whole_raw_sha256'],i['id']
 saved=(O/(i['id']+'.raw.txt')).read_bytes() if ranges else (O/(i['id']+'.metadata.raw.json')).read_bytes()
 if ranges and not i.get('stop_before_proof'):
  rows=raw.splitlines(keepends=True);assert saved==b''.join(b''.join(rows[a-1:z]) for a,z in ranges),i['id']
 else:assert saved in raw,i['id']
 assert sha(saved)==i['raw_sha256'] and sha(lf(saved))==i['lf_sha256'],i['id']
 checks.append(dict(id=i['id'],status='EXACT_RAW_LF_SOURCE_BYTES',kind=i['kind']))
primary=(O/'primary-pbps.raw.snapshot.html').read_bytes();assert sha(primary)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
selected=[]
for name,ranges in [('primary-selected-0',[(4566,4653)]),('primary-selected-1',[(4654,4665)]),('primary-selected-2',[(695,754)])]:
 saved=(O/(name+'.raw.html')).read_bytes();rows=primary.splitlines(keepends=True);assert saved==b''.join(b''.join(rows[a-1:b]) for a,b in ranges)
 selected.append(dict(id=name,path=str(O/'primary-pbps.raw.snapshot.html').replace('\\','/'),physical_ranges=ranges,raw_sha256=sha(saved),lf_sha256=sha(lf(saved))))
for a,b in [(1255,1288),(1315,1371)]:
 p=R/'runs/20261007-companion-priority/gaussian-canonical-kl-fisher-preread43/primary.raw.snapshot.html';raw=p.read_bytes();saved=(O/('primary-sphmc-%d-%d.raw.html'%(a,b))).read_bytes();assert saved==b''.join(raw.splitlines(keepends=True)[a-1:b])
 selected.append(dict(id='sphmc-rejected-duplicate-context-%d-%d'%(a,b),path=str(p).replace('\\','/'),whole_raw_sha256=sha(raw),physical_ranges=[[a,b]],raw_sha256=sha(saved),lf_sha256=sha(lf(saved))))
write('input-bindings.json',dict(schema_version=1,primary=dict(url='https://arxiv.org/html/2609.06905v1',raw_bytes=len(primary),raw_sha256=sha(primary),lf_sha256=sha(lf(primary)),physical_target_span=[4646,4653]),selected_primary=selected,public_parents=public,primitives_and_status_metadata=primitives,control_capsule_status='read-only process metadata;45 review/status/path metadata exposure retained; no underlying45artifact read'))
write('input-validation.json',dict(status='PASS_EXACT_RAW_LF_INPUTS_NO_COMPILER',checked=checks,selected_primary_checked=True,proof_verification=False))
details=dict(schema_version=1,status='ONE_DEPENDENCY_READY_SOURCE_API_RECOMMENDATION_NOT_ADMISSION',candidate_count=1,recommended_candidate=dict(rank=1,proposed_name='AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalGradientVariance.reflected_conditional_gradient_variance',proposed_file='AutoSamplingTheory/ExampleCases/ProximalBPS/ConditionalGradientVariance.lean',source='arxiv:2609.06905v1 AppendixC.1 A3.Ex7',physical_span=[4646,4653],assumptions=['finite realHilbert/Borel E, including rank0','V C2, 0<alpha<=beta, exact global Hessian lower/upper','eta>0, beta*eta<=1','C-infinity compact f as printed initial proof scope'],actual_outputs=['true Gaussian augmentation J and genuine Markov conditional/reflected R/S','literal normalized S_y density','actual T_f=integral f S_y and pointwise true covariance derivative','norm(gradient T_f y)^2 <= (1/eta-alpha)^2/(4*(alpha+1/eta))*actual centered-square variance(S_y,f)'],parents=[dict(name='ConditionalScore.reflected_conditional_covariance',status='independently_verified_current_DAG',integration_commit='b76a6a14282479d9bd48116549ccb1513789f8b9',header_span=[36,57]),dict(name='ConditionalScoreVariance.conditional_centered_domain_and_score_variance',status='independently_verified_current_DAG',verified_commit='292878b81db3f6d6ff46bdf59ba98539f05ce87f',header_span=[11,43])],internal_coherence='Only explicit S_y density equality; norm-sub symmetry; do not assume R/D witness equality',hidden_contracts=['probability output before scalar centering','compact-continuous f genuinely bounded/L2','directional score continuous/measurable and genuine centered-square L1 output','dual score and f-score L1 supplied by actual derivative parent','actual L2 quotient/product integrability, zero-aware covariance CS','dual operator norm and isometric Riesz gradient'],remaining_uncertainty='Small exact law/centered L2/evaluation/operator norm API join; no missing analytic producer located for this pointwise scope',actual_consumer='Printed A3.Ex7, next integrated C.2/B.13 via actual MacroscopicRepresentative and ReflectionL2 interfaces',extensions=['finiteHilbert/rank0 authored extension, no Nontrivial premise','measurable kernels retained; no arbitrary joint gradient selector'],excluded_claims=['C.2/B.13 outer integration','rough weighted-domain extension','marginal Poincare','halfturn/sampler/invariance/nonexplosion/hypocoercivity','W2/T2/FIRST/main/querycost']),rejected_routes=[dict(target='SPHMC4.4/4.5',reason='Already independently verified ProximalEstimatorLipschitz producer; duplicate'),dict(target='GaussianT2 static derivative leaf',reason='Immutable46 typed vector regularity/representative/Jacobian gap; substantial genuine missing producer')],strategy_steps=6,source_detail_sha256=sha((O/'source-detail.md').read_bytes()),source_api_only=True,compiler_used=False,self_admission=False)
write('source-detail.json',details)
contract=dict(schema_version=1,actor='gaussian_noncompact_preread_42',stage='47 source-first next-ready recommendation',scope='Own47 only. Root sole writer. No theorem proof/compiler/claim/Goal/sourcegraph/canonical mutation.',source_first_chronology=['Actual read/write/Python lease opened before first scheduling/source read','Current execution/handoff/cell metadata consulted as process state','Immutable primary PBPS AppendixC.1 read before full public score/variance contracts','Exact complete public headers extracted before mathematical candidate capsule','Mathlib primitives/source definitions pinned; no compiler'],source_primary_raw_sha256=sha(primary),input_bindings_sha256=sha((O/'input-bindings.json').read_bytes()),input_validation_sha256=sha((O/'input-validation.json').read_bytes()),source_detail_sha256=sha((O/'source-detail.json').read_bytes()),exposures=['Historical41 reviewer/source metadata and decoder-binding original_text exposure, earlier shared32body236-249 and44Registry32/41/42 metadata remain recorded in immutable earlier packets; not fresh-blind.','47 current control capsule included45 nested verification/status/path metadata; underlying45proof/Test/blind/review files not opened.','47 overbroad primary filename lookup returned large truncated metadata list including reviewer/decoder names; no listed artifact opened. Primary formula-index lookup also returned more source lines than needed; later exact physical source slices govern candidate.','Read-only capsule initially failed GBK stdout; UTF8 rerun completed; no compiler or state mutation.','Four first extracts were truncated at let-mu :=; original truncated header snapshots preserved, corrected complete headers stop at final := by, no proof body read.'],prohibited_file_reads=dict(proof45=False,Tests45=False,blind45=False,review45=False),actual_leases=dict(opened_at_utc=lease['opened_at_utc'],read='actual OPEN aggregate role, closed in final write',write='actual OPEN aggregate role, closed in final write',python='actual OPEN aggregate role, closed in final write',compiler='CLOSED_NO_COMPILER_USE'),independent_statement_and_topology_admission='Not performed by this agent; root and distinct reviewer decide next stage')
write('sourcecontract.json',contract)
closed_at=datetime.datetime.now(datetime.timezone.utc).isoformat();closed=dict(lease,state='CLOSED',closed_at_utc=closed_at,actual_roles=dict(read='CLOSED',write='CLOSED',python='CLOSED',compiler='CLOSED_NO_COMPILER_USE'),closure='Final filesystem operation closes actual read/write/Python leases; no filesystem operations follow.',result='source-only dependency-ready recommendation, not theorem admission')
closed_bytes=enc(closed);outputs=[]
for p in sorted(O.iterdir()):
 if p.is_file() and p.name not in ['lease.json','run.json']:
  b=p.read_bytes();outputs.append(dict(path=p.name,raw_bytes=len(b),raw_sha256=sha(b),lf_sha256=sha(lf(b))))
run=dict(schema_version=1,actor='gaussian_noncompact_preread_42',stage='47 next-ready source/API prerequisite',status='SOURCE_ONLY_PACKET_CLOSED',opened_at_utc=lease['opened_at_utc'],closed_at_utc=closed_at,candidates=1,compiler_invocations=0,canonical_writes=0,claims=0,sourcegraphs=0,forbidden_parent_file_reads=0,accidental_metadata_exposure=True,output_bindings=outputs,actual_closed_lease_sha256=sha(closed_bytes))
run_bytes=enc(run);(O/'run.json').write_bytes(run_bytes)
report=dict(packet=str(O).replace('\\','/'),source_detail_sha256=sha((O/'source-detail.json').read_bytes()),contract_sha256=sha((O/'sourcecontract.json').read_bytes()),run_sha256=sha(run_bytes),closed_lease_sha256=sha(closed_bytes),candidate_count=1,public_parent_count=len(public),primitive_input_count=len(primitives),status='SOURCE_ONLY_CLOSED_NO_ADMISSION')
# This must be the final filesystem operation.
(O/'lease.json').write_bytes(closed_bytes)
print(json.dumps(report,ensure_ascii=False))
