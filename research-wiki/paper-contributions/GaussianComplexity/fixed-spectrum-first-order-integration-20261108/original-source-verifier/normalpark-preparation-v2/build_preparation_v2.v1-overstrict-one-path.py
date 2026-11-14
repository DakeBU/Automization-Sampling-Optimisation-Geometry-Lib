from pathlib import Path
from datetime import datetime,timezone
import ast,json,sys
sys.dont_write_bytecode=True
from park_common import *

OLD=BASE/'normalpark-preparation'
old_manifest_raw=(OLD/'preparation-manifest.json').read_bytes()
assert sha(old_manifest_raw)=='081ad017e02b73787de19bf895406b9326787bc950734d366ce071b4902df6d3'
old_manifest=json.loads(old_manifest_raw)
assert len(old_manifest['artifacts'])==17
for row in old_manifest['artifacts']:
 data=(OLD/row['path']).read_bytes()
 assert len(data)==row['bytes'] and sha(data)==row['sha256'],row['path']
old=readjson(OLD/'preservation-baseline.json')
assert git('rev-parse','HEAD').decode().strip()==CORE
assert not git('diff','--name-only',CORE).strip()
assert git('diff','--name-only',HELD_CORE,CORE).decode().splitlines()==['website/static/underlying-lean-graph.js']
repair=ui_repair()
assert sha((ROOT/repair['source_path']).read_bytes())==repair['after_sha256']
assert sha(git('show',HELD_CORE+':'+repair['source_path']))==repair['before_sha256']
assert sha(ref_bytes(repair['independent_static_review']))=='5b488c34d9eee3bb26215b61e106d2ab8a95b6f58b2fa6ce3d4b3adc4b658a97'
for parent,child in [(CHECKED,SOURCEV_COMMIT),(SOURCEV_COMMIT,HELD_CORE),(HELD_CORE,CORE)]:
 assert subprocess.run(['git','merge-base','--is-ancestor',parent,child],cwd=ROOT).returncode==0
ledger=LEDGER.read_bytes()
v=(OLD/'original-V306.exact.jsonl').read_bytes()
stab=(OLD/'original-STAB621.exact.jsonl').read_bytes()
assert sha(v)==V_SHA and sha(stab)==STAB_SHA
assert ledger.count(v)==ledger.count(stab)==1 and ledger.index(v)<ledger.index(stab)
assert sha(AUDIT.read_bytes())==AUDIT_SHA
s=states();assert len(s)==285 and s[ADV]==old['own_STAB_state']
assert s[ADV]['latest_evidence']['integration_owner']==INTEGRATOR
assert [k for k,v in s.items() if v['state']=='STABILIZING']==[ADV]
assert foreign_state_digest(s)==old['foreign_284_SAU_state_sha256']
f=frontiers();assert f==old['frontier_raw_hashes'] and len(f)==444
critical=dict(old['critical_raw_pins'])
frozen=dict(old['frozen_originals'])
# Held87 canonical gate/site-metadata are mutable build outputs; never bind
# their old hashes as the new9b gate. Future context pins actual new outputs.
for rel in ['.astis/site-lean-gate.json','_site/data/build-metadata.json']:
 assert rel in critical;critical.pop(rel)
# Keep the actual held v3 code as immutable history rather than current code.
for name in ['check_final_reader_v3.py','first_order_browser_common_v3.py']:
 rel=(R/'independent-reader'/name).relative_to(ROOT).as_posix()
 frozen[rel]=critical.pop(rel)
for name,h in [('check_final_reader_v4.py',CHECKER_SHA),('first_order_browser_common_v4.py',BROWSER_COMMON_SHA)]:
 rel=(R/'independent-reader'/name).relative_to(ROOT).as_posix()
 assert sha((ROOT/rel).read_bytes())==h;critical[rel]=h
critical[repair['source_path']]=repair['after_sha256']
critical[repair['independent_static_review']['path']]=repair['independent_static_review']['sha256']
assert len(critical)==40,len(critical)
for rel,h in critical.items():assert sha((ROOT/rel).read_bytes())==h,rel
for p in OLD.rglob('*'):
 if p.is_file():frozen[p.relative_to(ROOT).as_posix()]=sha(p.read_bytes())
for ref in [repair['proposal'],repair['independent_static_review']]:
 frozen[ref['path']]=sha(ref_bytes(ref))
# Preserve completed held87 browser originals by raw hashes only; never treat
# script PASS as pixel acceptance, and never view/modify any image here.
held_browser_reports=[]
for report in (R/'independent-reader/browser').glob('*/report.json'):
 try:obj=json.loads(report.read_bytes())
 except (ValueError,OSError):continue
 if obj.get('head')!=HELD_CORE:continue
 frozen[report.relative_to(ROOT).as_posix()]=sha(report.read_bytes())
 for image in obj.get('screenshots',[]):
  p=report.parent/image['file'];data=p.read_bytes()
  assert sha(data)==image['sha256'];frozen[p.relative_to(ROOT).as_posix()]=sha(data)
 held_browser_reports.append({'path':report.relative_to(ROOT).as_posix(),'status':obj.get('status'),
  'scope':'Held87 script outcome only; actual pixel HOLD is preserved, not contradicted or accepted by this preparation.'})
for rel,h in frozen.items():assert sha((ROOT/rel).read_bytes())==h,rel
(PREP/'original-V306.exact.jsonl').write_bytes(v)
(PREP/'original-STAB621.exact.jsonl').write_bytes(stab)
(PREP/'ledger-before-park.exact.jsonl').write_bytes(ledger)
dump(PREP/'original-V-evidence.exact-values.json',json.loads(v)['evidence'])
baseline={**old,'created_utc':datetime.now(timezone.utc).isoformat(),
 'accepted_immutable_core':CORE,'held_immutable_core':HELD_CORE,
 'parent_v1_manifest_sha256':sha(old_manifest_raw),
 'own_STAB_state':s[ADV],'foreign_284_SAU_state_sha256':foreign_state_digest(s),
 'frontier_raw_hashes':f,'git_index_entries_sha256':sha(git('ls-files','-s','-z')),
 'ledger_before_sha256':sha(ledger),'ledger_before_bytes':len(ledger),
 'critical_raw_pins':critical,'frozen_originals':frozen,
 'future_v4_context':{'path':None,'sha256':None,'status':'NOT_YET_SUPPLIED_NO_GUESSED_HASH'},
 'future_new9b_gates':'Actual new context must pin all8 successful same9b-head receipts/logs, current gate and site metadata. Held87 gate hashes are not reused.',
 'reviewed_UI_exception':repair,'held87_browser_originals':held_browser_reports,
 'new_source_verdict':False,'normal_API_called':False}
dump(PREP/'preservation-baseline.json',baseline)
protected(baseline)
dump(PREP/'acceptance-inputs.template.json',{
 'state':'MISSING_EXTERNAL_ACCEPTANCE_INPUTS','accepted_immutable_core':CORE,
 'browser_context':{'path':None,'sha256':None},
 'artifacts':{k:{'path':None,'sha256':None} for k in [
  'bound_context_review','browser_report','browser_command_receipt','pixel_review','local_acceptance','parking_eligibility']},
 'note':'No future context/hash is guessed. Require actual native accepted late-context consistency, actual v4 report/receipt/current9b gates,38 original PNGs+independent38 pixel review, native8 geometry rows (fourextra DOM-only/no extraPNG), actual local acceptance/eligibility and separate root park authorization. No manufactured accepted adapter.'})
for p in PREP.glob('*.py'):ast.parse(p.read_text())
assert not (BASE/'normalpark-execution-v2').exists()
assert not (PREP/'root-authorization.json').exists()
dump(PREP/'v1-v2-mechanical-delta.json',{
 'parent_v1_manifest_sha256':sha(old_manifest_raw),'parent_v1_all17_payloads_unchanged':True,
 'parent_negative_preflight_preserved':True,'source_V306_evidence_fields_values_unchanged':True,
 'source_audit148_unchanged':True,'normal_API_called':False,'new_source_verdict':False,
 'only_versioned_preparation_changes':[
  'CORE target held87 -> UI-only successor9b, with held87 ancestry and exactone JS commit path checked.',
  'v4 checker/common exact frozen hashes replace current v3 code; v3 originals remain raw-pinned history.',
  'Future native context ref stays null, never reuses/guesses held87 context or gate/site metadata hashes.',
  'Consume v4 native8 geometry rows, complete card/label bounds and fourextra DOM-only/no extraPNG; retain38 independent original pixel reviews.',
  'Consume native v4 false foreign_tracked flag plus explicit reviewed one-JS qualification, never change it into unqualified true.',
  'Future actual all8 new9b receipts/current gate/site metadata are validated from the actual future bound context.',
  'Separate v2 authorization literal and execution directory; original V evidence still gets only post_integration_normalpark.'
 ],
 'critical_raw_pins':40,'frozen_originals':len(frozen),'SAUs':285,'foreign_SAUs':284,
 'frontier_JSON':444,'foreign_frontiers':443,
 'independence':'Mechanical preparation by original source verifier only; no new source/JS/pixel verdict, no normal API/browser/OS/commit, no accepted external artifacts or adapter.'})
print(json.dumps({'helper_sha256':sha((PREP/'normalpark_once.py').read_bytes()),
 'common_sha256':sha((PREP/'park_common.py').read_bytes()),
 'baseline_sha256':sha((PREP/'preservation-baseline.json').read_bytes()),
 'critical_raw_pins':40,'frozen_originals':len(frozen),'future_context':'unknown/unbound',
 'normal_API_called':False,'canonical_mutation':False},indent=2))
