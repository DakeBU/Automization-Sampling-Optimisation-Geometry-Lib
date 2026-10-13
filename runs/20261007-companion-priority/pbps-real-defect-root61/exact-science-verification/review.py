from common import *
import re
from tools import astis,astis_publication,astis_advance
assert head()==SCI
verified={}; resolutions=[]; maps={}
def key(row): return (path(row['path']).as_posix().lower(),row['raw_sha256'],row.get('lf_sha256'))
def addmap(original,snapshot,origin):
 matches(original,snapshot['path']); matches(snapshot)
 maps[key(original)]=dict(original=original,exact_raw_snapshot=snapshot,authority=origin)
source_inputs=J(R/'source-review61/input.manifest.json')
for row in source_inputs['qualified_raw_LF_pairs']: addmap(row['original'],row['raw_snapshot'],'source native qualified original/raw snapshot pair')
decoder_adopt=J(R/'root.decoder61.adoption.json')
for row in decoder_adopt['raw_snapshot_mappings']: addmap(row['original'],row['exact_raw_snapshot'],'root decoder adoption exact one-path raw snapshot')
for row in decoder_adopt['historical_lease_resolution']:
 target=next(x['exact_raw_snapshot'] for x in decoder_adopt['raw_snapshot_mappings'] if x['original']['path'].replace('\\','/').endswith('/initial-lease.raw.snapshot.json'))
 addmap(row['original'],target,'Original neutral OPEN lease exact snapshot retained in tracked anonymous-decoder')
def check(row):
 try: actual=matches(row)
 except (AssertionError,FileNotFoundError):
  assert key(row) in maps,('UNMAPPED_QUALIFIED_PIN',row)
  m=maps[key(row)]; actual=matches(row,m['exact_raw_snapshot']['path']); resolutions.append(m)
 verified[(actual['path'],actual['raw_sha256'])]=actual
 return actual
def walk(obj):
 if isinstance(obj,dict):
  if isinstance(obj.get('path'),str) and obj.get('raw_sha256'): check(obj)
  else:
   for v in obj.values(): walk(v)
 elif isinstance(obj,list):
  for v in obj: walk(v)
objects=['math-freeze.json','independent-math61/run.json','independent-math61/lease.json','independent-math61/receipt.json','independent-math61/input.manifest.json','independent-math61/outputs.final.json','source-review61/run.json','source-review61/lease.json','source-review61/input.manifest.json','source-review61/output.manifest.json','source-review61/native.receipt.json','anonymous-decoder/decoder-native-run.json','anonymous-decoder/decoder-native-run.payload.json','anonymous-decoder/inputmanifest.json','anonymous-decoder/CLOSED_LAST.json','anonymous-decoder/closed-lease.json','anonymous-decoder/foreground-readback.json','root.math61.adoption.json','root.source61.adoption.json','root.decoder61.adoption.json']
for n in objects: check(pin(R/n)); walk(J(R/n))
math=J(R/'independent-math61/run.json'); assert math['run_sha256']==H(C({k:v for k,v in math.items() if k!='run_sha256'}))
mp=J(R/'independent-math61/payload.json'); assert mp['named_mathematics_payload_sha256']==math['named_mathematics_payload_sha256']==H(C(mp['named_mathematics_payload']))
ml=J(R/'independent-math61/lease.json'); assert ml['status']=='CLOSEDLAST' and ml['lease_sha256']==H(C({k:v for k,v in ml.items() if k!='lease_sha256'}))
mo=J(R/'independent-math61/outputs.final.json'); assert mo['outputs_sha256']==H(C({k:v for k,v in mo.items() if k!='outputs_sha256'}))
source=J(R/'source-review61/run.json'); assert source['run_sha256']==H(C({k:v for k,v in source.items() if k!='run_sha256'}))
assert source['named_source_payload_sha256']==H((R/'source-review61/named-source-review.payload.json').read_bytes())
sl=J(R/'source-review61/lease.json'); assert sl['status']=='CLOSED' and sl['closed_last'] and sl['terminal_closed'] and sl['final_foreground_exit_code']==0
for i in range(2):
 q=J(R/f'source-review61/source.{i}.review.json'); expected=dict(source['complete_decisions'][i],review_run_sha256=source['run_sha256']); assert q==expected
 assert q['verdict']=='equivalent-after-elaboration' and q['excess_count']==q['blocking_deltas']==0 and q['repairs']==[]
plan=J(R/'publication-plan.json'); pubs=[]
for i,decl in enumerate(plan['mathematical_declarations']):
 item,binding=next((item,b) for item in astis_publication.load() for b in item['bindings'] if b['declaration']==decl)
 current_digest=astis_publication.binding_digest(item,binding); audit=ROOT/'research-wiki/semantic-roundtrip/audits'/ (plan['audit_ids'][i]+'.json'); a=J(audit)
 assert a['state']==a['source_review']['state']=='accepted' and a['verdict']=='equivalent-after-elaboration'
 assert a['publication_binding_sha256']==current_digest==source['publication_bindings'][i]
 assert a['source_review']['review_run_sha256']==source['run_sha256']
 assert a['source_review']['run_artifact'].endswith(f'source-review61/source.{i}.review.json')
 assert a['publication_context']==astis_publication.review_context(item,binding)
 pubs.append(dict(declaration=decl,audit=pin(audit),binding_sha256=current_digest,native_source_review=pin(R/f'source-review61/source.{i}.review.json')))
dec=J(R/'anonymous-decoder/decoder-native-run.json'); db=(R/'anonymous-decoder/decoder-native-run.payload.json').read_bytes()
assert dec['decoder_payload_sha256']==H(db) and dec['decoder_run_sha256']==H(b'ASTIS-ANONYMOUS-DECODER-NATIVE-RUN-v1\0'+db)
dc=J(R/'anonymous-decoder/CLOSED_LAST.json'); assert dc['closed_last'] and dc['closure_readback_completed'] and dc['actual_foreground_readback']['exit_code']==0
assert not dec['source_text_visible'] and not dec['source_identity_visible'] and not dec['compiler_started']
fakes=[]
for f in J(R/'math-freeze.json')['inputs'][:5]:
 p=path(f['path']); text=astis.strip_lean_comments_and_strings(p.read_text(encoding='utf8')); hits=[dict(line=i,text=l) for i,l in enumerate(text.splitlines(),1) if astis.FORBIDDEN_REGEX.search(l)]
 assert not hits and not re.search(r'^\s*import\s+Tests(?:\.|\s|$)',text,re.M)
 fakes.append(dict(input=pin(p),zero_fake_closures=True,production_no_Tests_import=True,scanner='tools.astis strip_lean_comments_and_strings/FORBIDDEN_REGEX',hits=hits))
W(P/'fake-closure.json',dict(status='PASS',files=fakes,actual_PID=os.getpid(),compiler_log_no_sorryAx=True))
freeze=J(R/'math-freeze.json'); assert len(freeze['inputs'])==27
for f in freeze['inputs']: check(f)
# Compare the actual theorem header substring with complete sealed signature by exact LF bytes.
seals=[]
for i,f in enumerate(freeze['inputs'][:2]):
 text=path(f['path']).read_bytes().replace(b'\r\n',b'\n').decode(); h=(ROOT/f'runs/20261007-companion-priority/pbps-real-defect-root-preproof61/header{i}.lean').read_bytes().replace(b'\r\n',b'\n').decode()
 declaration=plan['mathematical_declarations'][i].rsplit('.',1)[1]; start=text.index('theorem '+declaration); actual=text[start:text.index(':= by',start)].rstrip();
 expected=h[h.index('theorem '+declaration):].rstrip() if 'theorem '+declaration in h else h.rstrip()
 # Sealed headers are bare theorem headers; exact suffix colon is preserved.
 assert actual==expected,(i,actual[:120],expected[:120]); seals.append(dict(declaration=plan['mathematical_declarations'][i],exact_LF_header_sha256=H(actual.encode()),seal=pin(ROOT/f'runs/20261007-companion-priority/pbps-real-defect-root-preproof61/header{i}.lean')))
state=astis_advance.current_advances(); assert state[SAU]['state']=='PROVED_LOCAL'; lanes=[k for k,v in state.items() if v.get('state')=='STABILIZING']; assert lanes==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel'],lanes
W(P/'native.review.json',dict(status='PASS',checked_commit=SCI,actual_reviewer_PID=os.getpid(),unique_qualified_pin_readbacks=len(verified),verified_pins=list(verified.values()),finite_history_mappings=list({(m['original']['path'],m['original']['raw_sha256']):m for m in resolutions}.values()),math_run_sha256=math['run_sha256'],named_math_payload_sha256=mp['named_mathematics_payload_sha256'],source_run_sha256=source['run_sha256'],source_named_raw_payload_sha256=source['named_source_payload_sha256'],decoder_domain_separated_run_sha256=dec['decoder_run_sha256'],decoder_named_raw_payload_sha256=dec['decoder_payload_sha256'],native_recipes='Math/source full sorted compact objects minus ONLY run_sha256; math named canonical object; source named raw file; decoder domain-prefix/NUL/raw-file whole run and raw named file.',publications=pubs,seals=seals,full_body_review='Reuse unchanged CLOSED independent-math61 full10private+2public+genuineTest mathematical analysis, exact frozen originals/currentGit match; inspected complete current public/private bodies and source slots.',current_state='PROVED_LOCAL',sole_STABILIZING=lanes,all_original_outcomes_preserved=True,remaining=J(R/'proved-local.json')['truth_boundary']))
print('NATIVE_REVIEW_PASS',len(verified),'qualified pins',len(resolutions),'resolved historical row occurrences')
