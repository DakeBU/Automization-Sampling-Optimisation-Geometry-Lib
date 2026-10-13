from pathlib import Path
import json,hashlib
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent;N=R/'runs/20261007-companion-priority/pbps-actual-phase-reversal-volume96/next-primary97'
sha=lambda b:hashlib.sha256(b).hexdigest();load=lambda p:json.loads(p.read_bytes())
def info(p):return dict(path=p.relative_to(R).as_posix(),raw_sha256=sha(p.read_bytes()),bytes=p.stat().st_size)
def write(n,v):
 p=O/n;assert not p.exists();p.write_bytes((json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode())
cov=load(N/'source-coverage97.native.json');primary=R/cov['primary']['path'];raw=primary.read_bytes();assert sha(raw)==cov['primary']['raw_sha256']
checks=[]
for x in cov['regions']:
 b=raw[x['byte_start']:x['byte_end_exclusive']];assert sha(b)==x['raw_sha256'] and len(b)==x['bytes']
 checks.append(dict(region=x['id'],html_id=x['html_id'],line_start=x['line_start'],line_end=x['line_end'],raw_sha256=sha(b),disposition=x['disposition'],exact_byte_slice=True))
assert len(checks)==15
for key in ['inherited_inventory']:
 ref=cov[key];assert sha((R/ref['path']).read_bytes())==ref['raw_sha256']
ref=cov['inherited_inventory']['inherited_coverage_reference'];assert sha((R/ref['path']).read_bytes())==ref['raw_sha256']
snap=O/'inputs';snap.mkdir(exist_ok=False);paths=[N/'source-coverage97.native.json',N/'source-proof-graph97.native.json',N/'source-proof-graph97.preimplementation.native.json',N/'source-first-reconstruction97.native.json',N/'jump-convention-audit97.native.json',N/'next-edge-recommendation97.native.json'];inputs=[]
for i,p in enumerate(paths):
 q=snap/(str(i)+'.'+p.name+'.exactraw');q.write_bytes(p.read_bytes());inputs.append(dict(**info(p),snapshot=q.relative_to(R).as_posix()))
write('initial-topology-findings97.native.json',dict(kind='independent-source-topology-validation',reviewer='/root/exact_verifier96',mode='independent validation after reading proposed topology; NOT blind reconstruction',primary=info(primary),inputs=inputs,selected_region_checks=checks,scope='Bounded source slice for proposed unweighted endpoint/time transform97; inherited inventory preserved by exact reference; no whole-paper closure claim.',findings=[dict(id='D97-to-END_VOL97',severity='required graph-only correction',reason='Source endpoint-Borel-volume paragraph explicitly builds endpoint from finite composition. Existing factor preservation M96 is insufficient without the actual finite word D97.',edge=dict(source='D97',target='END_VOL97',consumer_use_site='actual zAt/final-flow finite composition')),dict(id='REV_TIME97-to-END_INV97',severity='required graph-only correction',reason='Source inverse-and-time-volume paragraph obtains inverse using reversed ordered times. Endpoint inverse consumes rho defining coordinate equation and reversed arc-gap order; time-measure preservation itself is NOT required.',edge=dict(source='REV_TIME97',target='END_INV97',consumer_use_site='projection: rho coordinate equation and reversal of arc gaps only; no dependency on time-volume conclusion'))],header_mathematics_unchanged=True,all_15_selected_raw_slices_verified=True,conditional_admission='Accept corrected graph only after both omitted direct use-site edges are made explicit and all other nodes, edges and exclusions preserved.',theorem_credit=False,Lean_dependency_credit=False))
print('Saved independent topology diagnostics and exact original graph snapshots')
