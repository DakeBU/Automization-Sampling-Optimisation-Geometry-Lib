from pathlib import Path
import json,hashlib,sys
sys.path.insert(0,str(Path.cwd()/'tools'));import astis_advance as adv
r=Path(__file__).parent;load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
claim=load(r/'claim.json');assert adv.current_advances()[claim['advance_id']]['state']=='VERIFIED'
lanes=[x for x in adv.current_advances().values() if x['state']=='STABILIZING'];assert len(lanes)==1 and lanes[0]['advance_id']=='ASTIS-SA-20261005-SPHMCImplementedPhaseKernel'
a=load(r/'root.reader-adjacency86.adoption.json');p=Path('website/scripts/declaration_lessons.py')
assert sha(p.read_bytes())==a['canonical_renderer_before']['RAW_sha256']
q=Path(a['renderer_proposal']['path']);assert sha(q.read_bytes())==a['renderer_proposal']['RAW_sha256']=='671dc0d177856b9c0f91f8acc6922f1e0e0cf57de5656b44cf8dbdea51cb9cdc'
p.write_bytes(q.read_bytes())
x=dict(status='EXACT_DISTINCTLY_REVIEWED_V4_APPLIED_IN_EXISTING_SOLE_LANE',review_adoption=a,canonical_renderer_RAW_sha256=sha(p.read_bytes()),Lean_statement_proof_lesson_unchanged=True,full_site_build='pending',actual_browser='pending',Goal_complete=False)
p=r/'integration86/renderer-application86.json';assert not p.exists();p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf8',newline='\n');print('Applied exact V4 reader relocation; full site/browser gates pending')
