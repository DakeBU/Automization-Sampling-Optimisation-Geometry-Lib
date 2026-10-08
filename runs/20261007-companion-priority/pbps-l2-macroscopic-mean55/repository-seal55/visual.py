from common import *
v=load(B/'visual.inspection.json');assert v['viewed_images']==['cdp.pbps.png','cdp.branch.png','proof.proof.png','proof.proof-late.png'];artifacts=[]
for e in v['artifacts']:
 a=pin(e['portable_path']);assert a['raw_sha256']==e['raw_sha256'] and a['bytes']==e['bytes'];artifacts.append(a)
images=[]
for name in v['viewed_images']:
 p=B/'visual-inspection55'/name;b=path(p).read_bytes();assert b[:8]==b'\x89PNG\r\n\x1a\n';width,height=struct.unpack('>II',b[16:24]);assert (width,height)==(1440,1800);images.append(dict(actual_image=pin(p),width=width,height=height,independently_viewed=True))
records=[]
for f in ['cdp.capture.json','proof.capture.json']:
 d=load(B/'visual-inspection55'/f);assert d['ownedBrowserExit']['code']==0 and d['ownedBrowserExit']['signal'] is None
 for row in d['records']:
  assert row['bodyVisibility']=='visible' and row['bodyDisplay']=='block';records.append(row)
assert len(records)==4 and records[0]['closedLeanDetails']==11 and records[0]['mathContainers']==8 and records[2]['closedLeanDetails']==records[3]['closedLeanDetails']==1
node=[]
for name in ['companion','proof']:
 d=load(B/('desktop55.'+name+'.status.json'));assert d['exit_code']==0 and pin(B/('desktop55.'+name+'.log'))['raw_sha256']==d['log_raw_sha256'];node.append(dict(actual_status=pin(B/('desktop55.'+name+'.status.json')),native=d,log=pin(B/('desktop55.'+name+'.log'))))
lease=load(B/'root.desktop-capture55.lease.json');assert lease['status']=='CLOSED' and lease['exit_code']==0
observations=[
 'Actual complete attributed statement retains C2/two Hessian/cap/finite Hilbert/rank0 and actual mu/J/nu/source S. Every-y law is explicitly separated from AE rough input mean/fiber integrability; no rough gradient B13/main result is claimed.',
 'Canonical snd isometry, dense closed range, uniform bounded inverse-range T, actual posterior uniqueness/stationarity/AE fibers, genuine Fubini/variance norm defect are displayed in six steps with initially folded Lean adjacent. Formulas visible in proof capture render legibly, no visible doubled-TeX command error.',
 'Actual step6 explicitly treats the difference as an Lp class and same T, and noncentered rank0 fixed1/variance0. Main and step6 formula containers visibly have horizontal scrollbars with rightmost end outside initial viewport. No claim that all formulas overflow.',
 'Graph shows exact target compiled; displayed disclaimer distinguishes solid import/module ownership from dashed incomplete name scans. Incidental LogConcaveOn.prod name scan is not admitted as a theorem parent; actual five parents remain evidenced by body/compiled full math.',
 'Presentation debts retained: repeated title/statement, dense inline/source notation, graph label clutter and awkward qualified-name wraps; main/step6 formula scrolling. This is scoped desktop evidence, not full-reader/mobile/interaction/live/PURIFIED or an independent ExpositionSeal.'
]
dump('visual.review.json',dict(status='ACCEPT_SCOPED_DESKTOP_CAPTURE_EVIDENCE_WITH_PRESENTATION_DEBTS',reviewer=ACTOR,checked_integration=HEAD,root_inspection=pin(B/'visual.inspection.json'),actual_portable_artifacts=artifacts,independently_viewed_four_PNG=images,actual_DOM_capture_records=records,actual_node_statuses=node,actual_capture_CLOSED_lease=pin(B/'root.desktop-capture55.lease.json'),observations=observations,physical_device_live_or_full_Exposition_acceptance=False))
print(json.dumps(dict(status='PASS_SCOPED',actual_viewed_PNG=4,DOM_records=4,actual_Node_exit0=len(node),capture_lease='CLOSED')))
