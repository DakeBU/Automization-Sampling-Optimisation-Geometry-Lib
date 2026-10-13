from pathlib import Path
import ast,hashlib,json,os,re
old=Path('.astis/pbps-bounce74');new=Path('.astis/pbps-clock75');rows=[]
def adapt(s):
 for a,b in [('pbps-actual-bounce-rate74','pbps-actual-hazard-clock75'),('pbps-bounce74','pbps-clock75'),('ActualBounceRate.actual_bounce_rate_energy_laws','ActualHazardClock.actual_integrated_hazard_clock_laws'),('ActualBounceRate','ActualHazardClock'),('actual-bounce-rate','actual-hazard-clock')]:s=s.replace(a,b)
 return re.sub(r'74(?![0-9a-f])','75',s)
for name in ['inspect-cdp74.mjs','inspect-copy74.mjs','final-gates74.py','reuse-regression74.py']:
 p=old/name;s=adapt(p.read_text(encoding='utf8'));dest=new/name.replace('74.','75.');assert not dest.exists(),dest
 if dest.suffix=='.py':ast.parse(s)
 dest.write_text(s,encoding='utf8',newline='\n');rows.append(dict(source=p.as_posix(),source_RAW_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),adapted=dest.as_posix(),adapted_RAW_sha256=hashlib.sha256(dest.read_bytes()).hexdigest()))
out=Path(os.environ['ASTIS_FOREGROUND_OBSERVER_DIR'])
(out/'integration-helper-adaptations75.json').write_text(json.dumps(dict(status='EXACT_CURRENT_TARGET_ADAPTATION_ONLY',actual_root_PID=os.getpid(),files=rows,canonical_tool_sources_changed=False,graph_refresh_scope='Five affected existing graph outputs/card via existing pure generators; no global refresh or unrelated cards.',math_source_unchanged=True,prior_full_regression_reuse_qualified=True),indent=2)+'\n',encoding='utf8',newline='\n')
print('PASS75 scoped browser/gate/reuse helpers prepared; no canonical mutation or gate credit.')
