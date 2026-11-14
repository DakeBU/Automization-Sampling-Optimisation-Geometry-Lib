from pathlib import Path
import hashlib,json,subprocess,sys
sys.dont_write_bytecode=True
ROOT=Path('/Users/zhouhuanjian/ASTIS-GC')
BASE=ROOT/'.astis/semantic-neutral-20261108/src_4e8f6a'
PREP=BASE/'normalpark-preparation-v2'
R=ROOT/'.astis/huanjian-gc-fixed-spectrum-first-order-integration-20261108'
CORE='9b1e90d25711668203c6e252cfe5a748f95c8ad4'
HELD_CORE='87ecd4d421de0146a062435f63e9dcb1f815c807'
CHECKED='9d306d837fbddf1518b0035494baaf5c21c24488'
SOURCEV_COMMIT='f45ba48f7dc74db28f648c38c5a486615723a513'
ACTOR='/root/source_reader_4e8f6a'
OWNER='huanjian_gc_20261108_fixed_spectrum_first_order'
INTEGRATOR='huanjian_gc_20261108_fixed_spectrum_first_order_integration'
ADV='ASTIS-SA-20261108-GaussianComplexityFixedSpectrumFirstOrder'
DECL='AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumFirstOrder.actual_first_order_query'
OWN_CELL='research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-first-order.json'
V_SHA='306b3ebcc5e659b5f2877a9ebe8ff010c09183a47c4b65be767b4ed489e9a99f'
STAB_SHA='621a4498cd7825f10315e0948ff0cc9e82ca8dc85378fbf3453588b288b91486'
AUDIT_SHA='a14867ad5fd8723933500d4c264c91c05d6b11ef510090c3b6da216fcb402b57'
CHECKER_SHA='de762a4107ce9bf844fa6ecf7f7d388928f0f15b391b9e63209ddeee22a9614f'
BROWSER_COMMON_SHA='523eefc6eba165093e51cdcb9fd67377ba6a66b95b1721e34d62b337d9a10e26'
SOURCE_DIGEST='18bcbfebf85cdf214e00cff1fa6d72c4bbf344a6c09bc76340efc783a3803c39'
LEDGER=ROOT/'runs/substantive_advances.jsonl'
AUDIT=ROOT/'research-wiki/semantic-roundtrip/audits/huanjian-fixed-spectrum-first-order.json'
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tools'))
from tools import astis_advance as advance

def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def readjson(p):return json.loads(Path(p).read_text())
def dump(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
def states():
 return advance._replay_advances([json.loads(s) for s in LEDGER.read_bytes().splitlines() if s.strip()])
def frontiers():
 return {p.relative_to(ROOT).as_posix():sha(p.read_bytes()) for p in sorted((ROOT/'research-wiki/frontier-cells').rglob('*.json'))}
def foreign_state_digest(s):return sha(canonical({k:v for k,v in s.items() if k!=ADV}))
def ref_bytes(ref):
 assert isinstance(ref,dict) and set(ref)>={'path','sha256'}
 assert isinstance(ref['path'],str) and isinstance(ref['sha256'],str) and len(ref['sha256'])==64
 p=(ROOT/ref['path']).resolve()
 assert p.is_relative_to(ROOT) and '..' not in Path(ref['path']).parts
 data=p.read_bytes();assert sha(data)==ref['sha256'],ref['path']
 return data

def ui_repair():
 # Read a literal descriptor from the exact frozen common file; never import
 # the browser checker or call its old125k-path baseline/execution machinery.
 import ast
 p=R/'independent-reader/first_order_browser_common_v4.py'
 raw=p.read_bytes();assert sha(raw)==BROWSER_COMMON_SHA
 for node in ast.parse(raw.decode()).body:
  if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='UI_REPAIR' for t in node.targets):
   repair=ast.literal_eval(node.value)
   assert repair['held_core']==HELD_CORE
   assert repair['source_path']=='website/static/underlying-lean-graph.js'
   assert repair['after_sha256']=='016c11a60392c449ebb28e8bedc7d3ab69134fff8dde4b438fd06c9f6c951a3a'
   return repair
 raise AssertionError('Exact v4 UI_REPAIR descriptor absent')

def validated_future_context(ref):
 # The actual v4 context/path/raw hash are intentionally unknown at preparation.
 # Only a later supplied immutable ref can satisfy these current-core guards.
 context=json.loads(ref_bytes(ref))
 assert context['authorized_by']=='/root'
 assert context['authorization_kind']=='fixed-spectrum-first-order-final-browser-v4-ui-repair'
 assert context['execute_browser_authorized'] is True
 assert context['new_source_verdict'] is False and context['parking_authorized'] is False
 assert context['accepted_immutable_core']==CORE and context['candidate_commit']==CHECKED
 assert context['source_digest']==SOURCE_DIGEST
 assert context['source_verifier_to_preserve']==ACTOR and context['integration_owner']==INTEGRATOR
 assert context['source_V_first_carrying_commit']==SOURCEV_COMMIT
 assert context['source_V_append']['sha256']==V_SHA and context['STAB_append']['sha256']==STAB_SHA
 assert context['accepted_source_audit']['sha256']==AUDIT_SHA
 assert context['browser_checker_sha256']==CHECKER_SHA
 assert context['browser_common_sha256']==BROWSER_COMMON_SHA
 assert context['reviewed_UI_repair']==ui_repair()
 repair=context['reviewed_UI_repair']
 assert sha((ROOT/repair['source_path']).read_bytes())==repair['after_sha256']
 assert sha((ROOT/repair['generated_asset_path']).read_bytes())==repair['after_sha256']
 assert git('show',CORE+':'+repair['source_path'])==(ROOT/repair['source_path']).read_bytes()
 checker=R/'independent-reader/check_final_reader_v4.py'
 assert sha(checker.read_bytes())==CHECKER_SHA
 gate=json.loads(ref_bytes(context['actual_gate']))
 meta=json.loads(ref_bytes(context['site_metadata']))
 assert gate['passed'] and meta['gate']['passed'] and meta['gate']['current']
 assert gate['commit']==meta['git']['commit']==CORE
 assert gate['source_digest']==meta['source_digest']==SOURCE_DIGEST
 assert set(context['actual_checks_before_browser'])=={
  'canonical_lean','publication','contributor','semantic','frontier','site_build','site_check','graph_check'}
 needles={'publication':'astis_publication.py','contributor':'astis_contributor_contract.py',
  'semantic':'astis_semantic_roundtrip.py','frontier':'astis_frontier_cells.py',
  'site_build':'build_site.py','site_check':'check_site.py','graph_check':'graph-check'}
 for role,receipt_ref in context['actual_checks_before_browser'].items():
  receipt=json.loads(ref_bytes(receipt_ref))
  assert receipt['exit_code']==0 and receipt['head_before']==receipt['head_after']==CORE
  log=Path(receipt['log']).resolve();assert log.is_relative_to(ROOT)
  lograw=log.read_bytes();assert sha(lograw)==receipt['log_sha256']
  if role=='canonical_lean':
   assert lograw.decode().splitlines().count('ASTIS check passed')==1
   assert receipt['command'][1:] in [['tools/astis.py','check'],['website/scripts/lean_gate.py']]
  else:assert needles[role] in str(receipt['command'])
 return context

def validate_native_geometry(report):
 routes={'native-Lean-parent','native-Lean-module','emitted-Functor-preset-with-query','native-Functor-to-Lean-module'}
 rows=report['native_selection_geometry']
 assert len(rows)==8
 assert {(r['width'],r['route']) for r in rows}=={(w,r) for w in [1440,390] for r in routes}
 keys={'unique_selected','source_kind','source_full_name','expected_view','nonempty_query',
  'readable_card','readable_label','full_card_inside_svg','full_card_inside_canvas',
  'full_card_inside_viewport','full_label_inside_svg','full_label_inside_canvas',
  'full_label_inside_viewport','full_label_inside_card'}
 images={s['file'] for s in report['screenshots']}
 def inside(a,b):
  return a['left']>=b['left']-1 and a['right']<=b['right']+1 and a['top']>=b['top']-1 and a['bottom']<=b['bottom']+1
 for row in rows:
  g=row['geometry'];assert g['ok'] is True and set(g['checks'])==keys
  assert all(v is True for v in g['checks'].values())
  assert g['camera_actions_by_harness']==[] and g['query']
  assert g['viewport']['right']==row['width']
  card,label=g['selected_main_rect'],g['rendered_label']
  assert card['width']>=160 and card['height']>=40
  assert label['width']>=80 and label['height']>=10 and g['rendered_label_font_px']>=10
  for outer in ['svg','canvas','viewport']:
   assert inside(card,g[outer]) and inside(label,g[outer])
  assert inside(label,card)
  assert row['extra_screenshot'] is False
  if row['route'] in ['emitted-Functor-preset-with-query','native-Functor-to-Lean-module']:
   assert row['pixel_review_claim'] is False and 'main_original' not in row
  else:
   assert row['main_original'] in images
 return {'actual_native_geometry_rows':8,'extra_DOM_only_rows':4,'extra_PNGs':0,
  'all_card_and_label_bounds_checked':True,'harness_camera_actions':[]}
def protected(b,*,after=False):
 assert git('rev-parse','HEAD').decode().strip()==CORE
 assert sha(git('ls-files','-s','-z'))==b['git_index_entries_sha256']
 changed=sorted(git('diff','--name-only',CORE).decode().splitlines())
 assert changed==(['runs/substantive_advances.jsonl'] if after else []),changed
 assert sha(AUDIT.read_bytes())==AUDIT_SHA
 assert frontiers()==b['frontier_raw_hashes']
 assert sha((ROOT/'runs/substantive_discoveries.jsonl').read_bytes())==b['discovery_sha256']
 for rel,h in b['critical_raw_pins'].items():assert sha((ROOT/rel).read_bytes())==h,rel
 for rel,h in b['frozen_originals'].items():assert sha((ROOT/rel).read_bytes())==h,rel
 s=states();assert len(s)==285 and foreign_state_digest(s)==b['foreign_284_SAU_state_sha256']
 own=s[ADV];assert own['owner_id']==OWNER and own['created_by']==OWNER
 return s

def validated_acceptance(bundle):
 # This intentionally requires real future artifacts. A missing/template bundle
 # never authorizes an API call, creates screenshots or substitutes DOM claims
 # for independent review of all38 original pixels.
 assert bundle.get('state')=='READY_FOR_SEPARATE_ROOT_PARK_AUTHORIZATION','External acceptance inputs are not ready'
 assert bundle.get('accepted_immutable_core')==CORE
 context_ref=bundle['browser_context']
 original_context=validated_future_context(context_ref)
 required=['bound_context_review','browser_report','browser_command_receipt','pixel_review','local_acceptance','parking_eligibility']
 assert set(bundle['artifacts'])==set(required)
 raw={k:ref_bytes(bundle['artifacts'][k]) for k in required}
 a={k:json.loads(v) for k,v in raw.items()}
 refs=bundle['artifacts']
 ctx=a['bound_context_review']
 # Consume the actual native late-context review. Never manufacture an accepted
 # wrapper/adapter from a weaker status or from the held CORE87 review.
 assert ctx['status']=='accepted' and ctx['context_raw_sha256']==context_ref['sha256']
 assert ctx['accepted_immutable_core']==CORE and ctx['new_source_verdict'] is False
 assert ctx['reviewer'] not in [OWNER,INTEGRATOR,'/root'] and ctx['reviewer']
 assert ctx['browser_checker_sha256']==original_context['browser_checker_sha256']
 assert ctx['browser_common_sha256']==original_context['browser_common_sha256']
 report=a['browser_report'];receipt=a['browser_command_receipt']
 assert report['status']=='passed' and report['errors']==[]
 assert report['head']==report['site_commit']==report['actual_gate_commit']==CORE
 assert report['candidate_commit']==CHECKED
 assert report['publication_binding_sha256']=='51d5a5e9390a0d66c2d5b72d042a042eec8d3d60433043ea3909bf9320ccb31e'
 assert report['source_digest']==original_context['source_digest']
 assert report['candidate_source_digest']==original_context['candidate_source_digest']
 assert report['actual_gate_sha256']==original_context['actual_gate']['sha256']
 assert report['site_metadata_sha256']==original_context['site_metadata']['sha256']
 assert report['authorization']==context_ref
 assert report['UI_repair']==original_context['reviewed_UI_repair']
 assert report['authorization_readback']['unique_original_V_append_sha256']==V_SHA
 assert report['authorization_readback']['original_source_verifier']==ACTOR
 assert report['authorization_readback']['lifecycle_API_called'] is False
 assert report['authorization_readback']['all8_actual_receipts_exact_core_read'] is True
 readback=report['authorization_readback']
 # V4 truthfully reports one reviewed foreign JS exception. Never rewrite its
 # native false flag to true or manufacture an unqualified preservation claim.
 assert readback['foreign_tracked_raw_bytes_preserved'] is False
 assert readback['all_other_foreign_tracked_raw_bytes_preserved'] is True
 exception=readback['reviewed_one_path_UI_exception']
 assert all(exception[k]==v for k,v in ui_repair().items())
 assert exception['source_generated_and_immutable_core_bytes_exact'] is True
 assert report['external_GitHub_HTML_checked'] is False
 assert len(report['pages'])==2 and {p['width'] for p in report['pages']}=={1440,390}
 assert len(report['graphs'])==4 and len(report['old_long_Lean_layout_regressions'])==2
 native_geometry=validate_native_geometry(report)
 assert receipt['exit_code']==0 and receipt['head_before']==receipt['head_after']==CORE
 assert 'check_final_reader_v4.py' in str(receipt['command'])
 logpath=Path(receipt['log']).resolve();assert logpath.is_relative_to(ROOT)
 log=logpath.read_bytes();assert sha(log)==receipt['log_sha256']
 logged_reports=[]
 for line in log.decode().splitlines():
  try:row=json.loads(line)
  except ValueError:continue
  if isinstance(row,dict) and 'report' in row:logged_reports.append(row)
 actual_report_path=(ROOT/refs['browser_report']['path']).resolve()
 assert len(logged_reports)==1
 logged=logged_reports[0]
 assert Path(logged['report']).resolve()==actual_report_path
 assert logged['status']=='passed' and logged['screenshots']==38 and logged['pages']==2 and logged['graphs']==4
 screenshots=report['screenshots'];assert len(screenshots)==38
 names=[s['file'] for s in screenshots];assert len(set(names))==38
 report_parent=(ROOT/refs['browser_report']['path']).resolve().parent
 image_map={}
 for row in screenshots:
  assert Path(row['file']).name==row['file'] and row['file'].endswith('.png')
  path=report_parent/row['file'];data=path.read_bytes()
  assert data[:8]==bytes([137,80,78,71,13,10,26,10]) and sha(data)==row['sha256']
  width=int.from_bytes(data[16:20],'big');height=int.from_bytes(data[20:24],'big')
  assert (width,height) in [(1440,1000),(390,844)]
  image_map[row['file']]=row['sha256']
 pixel=a['pixel_review']
 assert pixel['status']=='accepted' and pixel['accepted_immutable_core']==CORE
 assert pixel['browser_report_sha256']==refs['browser_report']['sha256']
 assert pixel['reviewer'] not in [OWNER,INTEGRATOR,'/root',ACTOR] and pixel['reviewer']
 assert pixel['independent_from_browser_executor'] is True
 assert pixel['new_source_verdict'] is False
 assert len(pixel['reviewed_images'])==38
 reviewed={}
 for row in pixel['reviewed_images']:
  assert row['viewed_original'] is True and row['status']=='accepted'
  assert row['file'] not in reviewed;reviewed[row['file']]=row['sha256']
 assert reviewed==image_map
 local=a['local_acceptance']
 assert local['status']=='accepted' and local['authorized_by']=='/root'
 assert local['accepted_immutable_core']==CORE
 assert local['browser_report_sha256']==refs['browser_report']['sha256']
 assert local['pixel_review_sha256']==refs['pixel_review']['sha256']
 assert local['bound_context_review_sha256']==refs['bound_context_review']['sha256']
 assert local['all38_original_pixels_reviewed'] is True
 assert local['remote_acceptance'] is False and local['wholeGoal_or_full_mains_claim'] is False
 eligible=a['parking_eligibility']
 assert eligible['eligible_for_normal_park'] is True and eligible['accepted_immutable_core']==CORE
 assert eligible['from_state']=='STABILIZING' and eligible['to_state']=='VERIFIED'
 assert eligible['original_source_verifier']==ACTOR
 assert eligible['source_V_append_sha256']==V_SHA and eligible['STAB_append_sha256']==STAB_SHA
 assert eligible['accepted_source_audit_sha256']==AUDIT_SHA
 assert eligible['local_acceptance_sha256']==refs['local_acceptance']['sha256']
 assert eligible['pixel_review_sha256']==refs['pixel_review']['sha256']
 assert eligible['no_new_source_verdict'] is True and eligible['remote_acceptance'] is False
 return {'accepted_immutable_core':CORE,'source_digest':report['source_digest'],
  'source_V_first_carrying_commit':SOURCEV_COMMIT,'original_source_V_append_sha256':V_SHA,
  'sole_STAB_append_sha256':STAB_SHA,'integration_owner':INTEGRATOR,
  'accepted_source_audit_sha256':AUDIT_SHA,'bound_context':context_ref,
  'reviewed_UI_repair':original_context['reviewed_UI_repair'],'native_geometry_validation':native_geometry,
  'native_v4_preservation_qualification':{
   'foreign_tracked_raw_bytes_preserved':False,'all_other_foreign_tracked_raw_bytes_preserved':True,
   'reviewed_one_path_UI_exception':exception},
  'acceptance_artifacts':refs,'all38_original_pixel_hashes':image_map,
  'pixel_reviewer':pixel['reviewer'],'context_reviewer':ctx['reviewer'],
  'scope':'Mechanical return from completed sole STAB to existing VERIFIED. Original V evidence remains exact; actual local acceptance is a later additional layer. No new source verdict/remote/purification/wholeGoal credit.',
  'new_source_verdict':False,'remote_acceptance':False}
