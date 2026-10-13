from pathlib import Path
import ast,hashlib,json,re
old=Path('.astis/pbps-harmonic73');new=Path('.astis/pbps-bounce74');rows=[]
def adapt(s):
 for a,b in [('pbps-actual-harmonic-flow73','pbps-actual-bounce-rate74'),('pbps-harmonic73','pbps-bounce74'),('ActualHarmonicFlow.actual_harmonic_flow_laws','ActualBounceRate.actual_bounce_rate_energy_laws'),('ActualHarmonicFlow','ActualBounceRate'),('actual-harmonic-flow','actual-bounce-rate')]:s=s.replace(a,b)
 return re.sub(r'73(?![0-9a-f])','74',s)
names=['inspect-cdp73.mjs','inspect-copy73.mjs','small-gates73.py','final-gates73.py','run-integration73.py','prepare-generated-scope73.py','narrow-generated-scope73.py','reuse-regression73.py']
for name in names:
 p=old/name;s=adapt(p.read_text(encoding='utf8'));dest=new/name.replace('73.','74.');assert not dest.exists(),dest
 if dest.suffix=='.py':ast.parse(s)
 dest.write_text(s,encoding='utf8',newline='\n');rows.append(dict(source=p.as_posix(),source_RAW_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),adapted=dest.as_posix(),adapted_RAW_sha256=hashlib.sha256(dest.read_bytes()).hexdigest()))
s=adapt((old/'record-integration73.py').read_text(encoding='utf8'))
for a,b in [('==8','==9'),('==9','==10')]:
 if a=='==8':s=s.replace("len(capture['records'])==8","len(capture['records'])==9")
 else:s=s.replace("len(viewed['images'])==9","len(viewed['images'])==10")
for a,b in [('==6','==7'),('formula_BODY_steps=6','formula_BODY_steps=7'),('registry_count=522','registry_count=523'),('Registry522','Registry523'),('publication_units=243','publication_units=244'),('243 publication units','244 publication units'),('six formula/BODY steps','seven formula/BODY steps'),('Deterministic harmonic flow accepted','Deterministic bounce/rate/energy-layer laws accepted'),('Bounce/rate/clock/PDMP invariance/nonexplosion remain open.','Actual clock/recursive PDMP/invariance/nonexplosion remain open.'),('One actual deterministic harmonic-flow theorem and its existing gradient-continuity dependency.','One actual deterministic bounce/rate/energy-layer theorem; internal canonical gradient-Lipschitz producer and pinned Mathlib reflection dependencies.'),('Actual bounce/rate/clocks/PDMP/nonexplosion/invariance','Actual clocks/recursive PDMP/nonexplosion/invariance')]:s=s.replace(a,b)
assert "len(capture['records'])==9" in s and "len(viewed['images'])==10" in s and "len(lesson['steps'])==7" in s
ast.parse(s);(new/'record-integration74.py').write_text(s,encoding='utf8',newline='\n')
(new/'integration-helper-adaptations74.json').write_text(json.dumps(dict(status='EXACT_TARGET_ADAPTATION_ONE_STATEMENT_SEVEN_BODY_STEPS_TEN_PNGS',files=rows,canonical_scripts_changed=False,math_source_unchanged=True,prior_full_regression_reuse_qualified=True),indent=2)+'\n',encoding='utf8',newline='\n')
print('PASS74 integration helper sources prepared; no canonical/shared mutation or gate credit.')
