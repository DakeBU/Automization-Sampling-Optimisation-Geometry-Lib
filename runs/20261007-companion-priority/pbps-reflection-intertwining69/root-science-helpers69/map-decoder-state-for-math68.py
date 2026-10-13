from pathlib import Path
import hashlib,json,os
r=Path('runs/20261007-companion-priority/pbps-sharp-energy68');sha=lambda b:hashlib.sha256(b).hexdigest()
rows=[]
for i,aid in enumerate(['ASTIS-RT-20261009-HilbertSharpQuadraticCorrectorBound','ASTIS-RT-20261009-PBPSSharpCorrectorEnergy']):
 before=r/f'audit.{i}.before-decoder.exactraw.snapshot.json';p=Path('research-wiki/semantic-roundtrip/audits')/(aid+'.json');b=before.read_bytes();c=p.read_bytes();old=json.loads(b);current=json.loads(c)
 assert old['state']=='draft' and current['state']=='blind-reconstructed'
 assert {k:v for k,v in old.items() if k not in ['state','reconstruction']}=={k:v for k,v in current.items() if k not in ['state','reconstruction']}
 snap=r/f'audit.{i}.after-decoder.exactraw.snapshot.json';assert not snap.exists();snap.write_bytes(c)
 rows.append(dict(canonical_file=p.resolve().as_posix(),frozen_exact_before_snapshot=before.resolve().as_posix(),before_RAW_sha256=sha(b),current_exact_after_snapshot=snap.resolve().as_posix(),current_RAW_sha256=sha(c),allowed_changed_top_fields=['state','reconstruction'],all_other_fields_exactly_unchanged=True))
x=dict(kind='FINITE_DECODER_STATE_ONLY_MAP_FOR_FROZEN_MATH_INPUTS',actual_root_pid=os.getpid(),rows=rows,prose_overlay_applied=False,Lean_and_lesson_changes=False,source_verdict=False,math_verdict=False)
p=r/'decoder-state-map.for-math68.json';assert not p.exists();p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Finite2 audit draft→blind-state maps, no source/math verdict:',sha(p.read_bytes()))
