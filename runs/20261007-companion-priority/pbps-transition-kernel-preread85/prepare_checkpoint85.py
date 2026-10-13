from pathlib import Path
r=Path(__file__).parent
s=(r.parent/'pbps-outer-bounded-l2-preread84/checkpoint_before_fetch84.py').read_text(encoding='utf8')
s=s.replace("r.parent/'pbps-bounded-test-preread83/post-fetch83.workspace-RAW.corrected.json'","r.parent/'pbps-outer-bounded-l2-preread84/pre-fetch84.workspace-RAW.json'")
s=s.replace('source_freeze84.raw-manifest.json','source-first-run-manifest85.json')
s=s.replace("prior83='independently VERIFIED, full local aggregate/gates, normalpushed integration5f29b2a3; actual browser/main/PURIFIED/live separate'","prior84='independently VERIFIED science dd3a2301, all local aggregate/gates, normalpushed integration5186f926; actual browser/main/PURIFIED/live separate'")
for a,b in [('pre-fetch84','pre-fetch85'),('before-fetch84','before-fetch85'),('post-fetch84','post-fetch85')]:s=s.replace(a,b)
# The baseline path is an immutable prior84 snapshot; do not rewrite its suffix.
s=s.replace("r.parent/'pbps-outer-bounded-l2-preread84/pre-fetch85.workspace-RAW.json'","r.parent/'pbps-outer-bounded-l2-preread84/pre-fetch84.workspace-RAW.json'")
p=r/'checkpoint_before_fetch85.py';assert not p.exists();p.write_text(s,encoding='utf8',newline='\n')
