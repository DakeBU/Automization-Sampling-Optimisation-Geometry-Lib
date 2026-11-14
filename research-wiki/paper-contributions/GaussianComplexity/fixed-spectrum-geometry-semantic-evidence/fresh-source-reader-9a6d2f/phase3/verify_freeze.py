from pathlib import Path
import hashlib,json,subprocess,os
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[3]
def h(b):return hashlib.sha256(b).hexdigest()
m=json.loads((OUT/'phase3_manifest.json').read_text());assert h((OUT/'phase3_manifest.json').read_bytes())==(OUT/'phase3_manifest.sha256').read_text().split()[0]
for f in m['files']:
 p=(OUT/f['path']).resolve();assert p.is_relative_to(OUT);b=p.read_bytes();assert len(b)==f['bytes'] and h(b)==f['sha256'],f['path']
assert {str(p.relative_to(OUT)) for p in OUT.rglob('*') if p.is_file()}=={f['path'] for f in m['files']}|{'phase3_manifest.json','phase3_manifest.sha256'}
for phase,digest,count in [('phase1','aa9b3ffb40981e0d6d80d9c1ac8458a610c41bb7137e185a89baf6d9c25f81f1',28),('phase2','951200393b1492ea53419605942a792d3506822f3f6937ab5ec46ca374addc17',25)]:
 p=OUT.parent/phase;b=(p/(phase+'_manifest.json')).read_bytes();assert h(b)==digest;pm=json.loads(b);assert len(pm['files'])==count
 for f in pm['files']:assert h((p/f['path']).read_bytes())==f['sha256']
pins=json.loads((OUT/'inputs/evidence__full-review-input-pins.json').read_text())
for rel,digest in pins['exact_inputs'].items():assert h((ROOT/rel).read_bytes())==digest,rel
for row in json.loads((OUT/'input-preservation.json').read_text())['inputs']:
 assert h((OUT/row['snapshot']).read_bytes())==row['sha256'];assert h((ROOT/row['path']).read_bytes())==row['sha256']
env=dict(os.environ);env['GIT_OPTIONAL_LOCKS']='0';assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,env=env,text=True).strip()==pins['checked_candidate_commit']
assert subprocess.run(['git','diff','--quiet'],cwd=ROOT,env=env).returncode==0 and subprocess.run(['git','diff','--cached','--quiet'],cwd=ROOT,env=env).returncode==0
r=json.loads((OUT/'review-result.json').read_text());a=json.loads((OUT/'accepted-audit-successor.json').read_text());assert r['review_run_sha256']==h((OUT/'reviewer-run.json').read_bytes())==a['source_review']['review_run_sha256']
assert r['verdict']==a['verdict']=='equivalent-after-elaboration' and a['state']=='accepted'
assert len(r['semantic_slots'])==7 and all(not d['blocking'] for d in r['deltas'])
assert json.loads((OUT/'private-successor-schema-check.json').read_text())['errors']==[]
fresh=json.loads((OUT/'lean-evidence/fresh-compilation.json').read_text());assert len(fresh['runs'])==5 and all(x['returncode']==0 for x in fresh['runs'])
assert json.loads((OUT/'lean-evidence/kernel-probe-run.json').read_text())['returncode']==0
c=json.loads((OUT/'source-coverage-completeness.json').read_text());assert c['source_units']==32 and c['formula_link_atoms']==120 and not(c['missing_units'] or c['extra_units'] or c['missing_atoms'] or c['extra_atoms'])
print(json.dumps({'phase3_static_preservation_check':'pass','manifest_sha256':h((OUT/'phase3_manifest.json').read_bytes()),'payloads':len(m['files']),'checked_candidate':pins['checked_candidate_commit'],'verdict_proposal':r['verdict'],'private_successor_sha256':h((OUT/'accepted-audit-successor.json').read_bytes()),'canonical_audit_unchanged':True,'both_ledgers_unchanged':True,'sourceV_transition':'not executed','reader':'static-only; runtime/canonical-root/site/remote acceptance remains separate'}))
