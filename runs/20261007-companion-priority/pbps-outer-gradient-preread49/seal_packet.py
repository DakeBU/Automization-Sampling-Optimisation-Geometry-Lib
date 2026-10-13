# -*- coding: utf-8 -*-
import pathlib,json,hashlib,datetime,sys
sys.stdout.reconfigure(encoding='utf-8');r=pathlib.Path('E:/Samplinglib');d=r/'runs/20261007-companion-priority/pbps-outer-gradient-preread49';H=lambda b:hashlib.sha256(b).hexdigest();J=lambda o:(json.dumps(o,indent=2,ensure_ascii=False)+'\n').encode('utf-8')
opened=(d/'lease.json').read_bytes();(d/'lease.open.raw.snapshot.json').write_bytes(opened)
contract=dict(schema_version=1,status='SOURCE_API_PREREAD_ONLY_DEPENDENCY_READY_CANDIDATE_PENDING48_ADMISSION',owner='gaussian_noncompact_preread_42',canonical_writer='companion_root_20261005',primary='arxiv2609.06905v1',primary_first=True,actual_chronology=['OPEN actual read/write/Python; compiler CLOSED','read frozen47 primary outerC2 and B13 region','extract exact primary standing/laws/definitions/B9/B13/C2; only then public parent headers','narrow actual Mathlib/ASTIS API contracts','synthesize internal direct J.swap integration route and finite domain obligations','revalidate selected exactinputs and close all leases as final filesystem operation'],known48production_exposure=True,blind_role=False,nonexistent49implementation_exposure=False,proof_claim=False,source_graph_created=False,compiler_used=False,shared_edits=False,goal_changes=False,recommendation='Smooth compact actual outer energy/variance-defect C.2, all real law/finite-domain facts internally produced',shorter_alternative='Actual smooth compact outer conditional variance equals marginal second-moment deficit',minimal_binders=['finite real Hilbert E/Borel; author extension including rank0','V C2, true Hessian lower alpha and upper beta','0<alpha, alpha<=beta, eta>0, beta*eta<=1','f C-infinity compact'],forbidden_extra_binders=['IsProbabilityMeasure arbitrary chosen law','caller conditional law/density match','MemLp gradient/Tf certificate','variance-defect identity','desired outer bound','rough H1 witness'],source_extension_boundary='Source R^d -> finite real Hilbert incl rank0; smoothcompact ingredient only, no allL2 -> H1 completion',opaque_parent_status='Existing verified parent status inherited47/history, actual current public headers pinned;48 focusedcompiled/wholeproofreviewed but final source admission still active',route_residuals=['Implement and independently seal/review49 actual integration/domain edge only after48admission','Literal U/P/A/B/Γ adapter requires real representative/law coherence; not automatic from parent existence','All L2 to closed H1 rough extension remains separate'],administrative_execution_metadata_is_mathematical_source=False)
(d/'sourcecontract.json').write_bytes(J(contract))
# Bind all selected input families; whole provider byte checks differ from selected-fragment scope.
allinputs=[]
for name in ['primary-bindings.json','primary-additional-bindings.json','input-bindings.json','additional-input-bindings.json']:
 allinputs += json.loads((d/name).read_text(encoding='utf-8'))
for v in allinputs:
 b=pathlib.Path(v['path']).read_bytes();assert H(b)==v['whole_raw_sha256'];assert H(b.replace(b'\r\n',b'\n'))==v['whole_lf_sha256']
# Initial broader semantic previews are exposure-only source pins, excluded from recommended mathematical scope.
p=r/'runs/20261007-companion-priority/next-ready-preread47/primary-pbps.raw.snapshot.html';b=p.read_bytes();raw= b.splitlines(keepends=True);ev=[]
for name,a,z in [('outer-C2',4644,4679),('B13-search-region',3750,3890)]:
 part=b''.join(raw[a-1:z]);assert (d/(name+'.raw.html')).read_bytes()==part;ev.append(dict(path=str(p),span=[a,z],selected_mathematical_scope=False,exposure_snapshot=name+'.raw.html',fragment_raw_sha256=H(part),fragment_lf_sha256=H(part.replace(b'\r\n',b'\n'))))
(d/'exposure-input-bindings.json').write_bytes(J(ev));(d/'input-validation.json').write_bytes(J(dict(status='PASS_RAW_LF_INPUT_REVALIDATION_ONLY',selected_bindings=len(allinputs),scope='Source/API exact byte validation; not theorem or topology admission',compiler=False)))
closed=json.loads(opened.decode('utf-8-sig'));closed.update(status='CLOSED',read='CLOSED',write='CLOSED',python='CLOSED',compiler='CLOSED',compiler_used=False,closed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),last_filesystem_operation='write this actual CLOSED lease; no read/write follows');cb=J(closed)
outputs={}
for p in sorted(d.rglob('*')):
 if p.is_file() and p.name not in ['run.json','lease.json']:
  b=p.read_bytes();outputs[str(p.relative_to(d))]=dict(raw_sha256=H(b),lf_sha256=H(b.replace(b'\r\n',b'\n')),bytes=len(b))
run=dict(schema_version=1,status='CLOSED_SOURCE_ONLY_PREREAD49',outputs=outputs,closed_lease_sha256=H(cb),run_hash_recipe='SHA256 exact run.json UTF8 bytes; excludes itself and binds predicted exact final CLOSED lease bytes, no cyclic hash',compiler_used=False,claim=False,topology_admission=False)
rb=J(run);(d/'run.json').write_bytes(rb)
msg=dict(status=run['status'],capsule_sha256=H((d/'capsule.md').read_bytes()),source_detail_sha256=H((d/'source-detail.md').read_bytes()),contract_sha256=H((d/'sourcecontract.json').read_bytes()),run_sha256=H(rb),closed_lease_sha256=H(cb),selected_bindings=len(allinputs))
(d/'lease.json').write_bytes(cb) # FINAL FILESYSTEM OPERATION
print(json.dumps(msg))
