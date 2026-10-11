from pathlib import Path
import datetime, hashlib, json, subprocess
root=Path.cwd().resolve()
r=Path(__file__).resolve().parent
out=r/'integration96'
load=lambda p:json.loads(Path(p).read_bytes())
def ref(p):
    p=Path(p);b=p.read_bytes()
    return dict(path=p.resolve().relative_to(root).as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
labels=['integration-tests','integration-astis','integration-canonical','integration-publication','integration-contributor','integration-semantic','integration-frontier','integration-process-memory','integration-python-compile','integration-site-build','integration-site-check','integration-graph-after-site','integration-site-regressions','integration-harness','integration-diff-check']
checks=[]
for label in labels:
    p=r/'checks96'/label;d=load(p/'receipt.json')
    assert d['exit_code']==0 and d['terminal_closed'],label
    checks.append(dict(label=label,receipt=ref(p/'receipt.json'),stdout=ref(p/'stdout.log'),stderr=ref(p/'stderr.log')))
gate=load('.astis/site-lean-gate.json')
head=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip()
assert gate['passed'] and gate['commit']==head==load(out/'integration-scope.json')['science_commit']
saved=load(r/'exact-commit-verification96/closed-RAW-manifest96.json')['preserved_collaborator_inputs']
for d in saved:
    assert hashlib.sha256(Path(d['path']).read_bytes()).hexdigest()==d['raw_sha256'],d['path']
note=dict(status='LOCAL_AGGREGATE_AND_GENERATED_READER_PASS_VISUAL_PENDING',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),science_commit=head,integration_base_commit=head,registry_count=546,verification=ref(r/'exact-commit-verification96/verified.json'),checks=checks,source_digest=gate['source_digest'],offline_reader=ref(out/'offline-reader96.json'),static_svg=ref(out/'static-svg/viewed96.json'),graph_delta='One actual phase-volume and reversal node; two verified actual ASTIS parents (harmonic flow and bounce rate). Eight private mathematical helpers are internally consumed. Product-volume shear/reflection mechanics are formal dependencies; source/curated/scanned overlays retain separate meanings. No new conceptual mirror',independent_dependency_certificate=ref(r/'exact-commit-verification96/verified.json'),preserved_collaborator_modified_files=len(saved),sole_lane='ASTIS-SA-20261011-PBPSActualPrescribedPathDensity',state_distinctions=dict(proved_locally=True,independently_verified=True,local_aggregate_and_generated_site_gates=True,stabilized=False,merged=False,purified=False,live_verified=False,full_Exposition_Seal=False,main_theorem_complete=False),remaining=['Actual finite prescribed endpoint/time reversal is the next source dependency; next-primary97 is only a source preread, no proof claim.','Stationary Gibbs averaging/invariance, restart/Markovness, hypocoercivity, implementation errors, actual expected costs, main results, actual-input composition and all four full papers remain open.','Actual paper-page/fine-graph visual acceptance, main merge and postmerge purification remain separate. Browser returned no accessible tabs.'],resolved_gate_failure='Exact mathematical theorem unchanged across reviews; a mistaken escaping diagnosis was corrected, with original and corrected evidence retained. Final formula string runs and source review accepted.',Goal_complete=False)
p=r/'integration.notes.json'
assert not p.exists()
p.write_text(json.dumps(note,indent=2)+'\n',encoding='utf8',newline='\n')
print('Aggregate96 evidence recorded; visual/main/purification/full-paper credit remains pending.')
