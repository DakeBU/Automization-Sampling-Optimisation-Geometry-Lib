from pathlib import Path
import copy, hashlib, json, os, subprocess, sys
root=Path.cwd();sys.path.insert(0,str(root/'tools'))
import astis_publication as pub, astis_semantic_roundtrip as rt
r=Path('runs/20261007-companion-priority/pbps-actual-hazard-clock75');o=r/'independent-source75'
load=lambda p:json.loads(Path(p).read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
def check(z):
 b=Path(z['path']).read_bytes();assert len(b)==z['RAW_bytes'] and sha(b)==z['RAW_sha256'] and sha(b.replace(b'\r\n',b'\n'))==z['LF_sha256'],z['path'];return b
def save(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def new(p,x):assert not Path(p).exists(),p;save(p,x)
assert sha((o/'lease.final.json').read_bytes())=='0312b2a441747bf989cf7d5f058d2e69177b6dd90766e1a10b1dd11a7bf49971'
out=Path(os.environ['ASTIS_FOREGROUND_OBSERVER_DIR'])
with (out/'native-readonly.stdout.log').open('wb') as s,(out/'native-readonly.stderr.log').open('wb') as e:
 p=subprocess.Popen([sys.executable,'-B','-X','utf8',str(o/'verify_closed75.py'),'--observed-close-exit','0'],stdout=s,stderr=e);code=p.wait()
assert code==0
readonly=load(out/'native-readonly.stdout.log');assert readonly['status']=='READONLY_PASS' and readonly['overlay_ready_for_exact_adoption'] and not readonly['source_admission_ready']
decision=load(o/'overlay75.decision.json');proposal=load(r/'review-input-metadata-overlay75/proposal.json')
assert sha((o/'overlay75.decision.json').read_bytes())=='65a16f2c2cdb5eca53507b040e1a66e86d5f39bcd29384314881b9819eb017db'
assert sha(can({k:v for k,v in decision.items() if k!='decision_sha256'}))==decision['decision_sha256']
assert decision['status']=='ACCEPTED_EXACT_THREE_FIELD_METADATA_OVERLAY_ONLY' and decision['field_count']==3 and decision['files']==2
assert not decision['source_admission_granted'] and not decision['mathematical_repair'] and not decision['source_repair']
assert decision['fresh_anti_anchored_source_reviewer_required'] and decision['same_neutral_inventory_in_all_three_fields']
assert decision['proposal_RAW']['RAW_sha256']==sha((r/'review-input-metadata-overlay75/proposal.json').read_bytes())=='dd507f079ab5a79c876eb22f606ddb0da4ebea55488570ebaa1c2f63a905e39b'
for z in decision['exact_pins']:
 assert z['unchanged'];check(z['exact_pin'])
changes=[]
for row,reviewed in zip(proposal['rows'],decision['rows'],strict=True):
 assert row['path']==reviewed['path'] and row['proposed']==reviewed['proposed']
 before=check(row['before']);assert check(row['current'])==before
 proposed=check(row['proposed']);original=load(row['before']['path']);expected=copy.deepcopy(original)
 for delta in row['changes']:
  keys=delta['json_pointer'].strip('/').split('/');parent=expected
  for k in keys[:-1]:parent=parent[int(k)] if isinstance(parent,list) else parent[k]
  assert parent[keys[-1]]==delta['old'];parent[keys[-1]]=copy.deepcopy(delta['new'])
 assert expected==json.loads(proposed)
 changes.append(dict(path=row['path'],before=row['current'],after=row['proposed'],json_pointers=[d['json_pointer'] for d in row['changes']]))
assert sum(len(z['json_pointers']) for z in changes)==3
ap=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSActualHazardClock.json');audit=load(ap)
assert audit['state']=='blind-reconstructed';old_packet=rt.decoder_packet(audit)
assert old_packet==load('.astis/decoder-75/packet.json')
(r/'audit.before-clean-review75.exactraw.snapshot.json').write_bytes(ap.read_bytes())
for row in proposal['rows']:Path(row['path']).write_bytes(check(row['proposed']))
item=load('website/content/publications/pbps-actual-hazard-clock.json')['items'][0]
audit['publication_binding_sha256']=pub.binding_digest(item,item['bindings'][0],pub.inputs())
audit['publication_context']=pub.review_context(item,item['bindings'][0],pub.inputs())
assert rt.decoder_packet(audit)==old_packet
save(ap,audit)
new(r/'source-review.clean.packet.json',rt.semantic_reviewer_packet(audit))
paths=[r/'source-review.clean.packet.json',ap,Path('research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-hazard-clock.json'),Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHazardClock.lean'),Path('website/content/publications/pbps-actual-hazard-clock.json'),Path('website/content/declaration_lessons/pbps-actual-hazard-clock.json'),r/'implementation-source-map75.json',r/'anonymous-decoder/decoded.root-adapter.json',r/'anonymous-decoder/reconstruction.json',r/'anonymous-decoder/run.json',r/'anonymous-decoder/CLOSED_LAST.json',r/'anonymous-decoder/parent-packet.json',Path('lean-toolchain'),Path('lake-manifest.json'),Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHarmonicFlow.lean'),Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualBounceRate.lean')]
for path in paths[1:7]:
 data=load(path) if path.suffix=='.json' else None
 def walk(v):
  if isinstance(v,dict):
   for k,w in v.items():
    assert k not in {'deltas','verdict','review_run_sha256'},(path,k)
    walk(w)
  elif isinstance(v,list):
   for w in v:walk(w)
 if data is not None:walk(data)
new(r/'source-review.clean.freeze75.json',dict(status='CLEAN_CURRENT75_REVIEW_INPUTS_FROZEN',inputs=[pin(p) for p in paths],prior_source_or_header_decisions_in_inputs=False,decoder_packet_unchanged=True,Lean_unchanged=True,source_review=False,VERIFIED=False))
new(r/'root.review-input-metadata75.adoption.json',dict(status='EXACT_INDEPENDENT_THREE_FIELD_METADATA_OVERLAY_APPLIED_ONLY',actual_root_PID=os.getpid(),native_lease=pin(o/'lease.final.json'),native_overlay_decision=pin(o/'overlay75.decision.json'),native_complete_payload=pin(o/'complete-named-review-decision-input-payload.json'),native_readonly=readonly,readonly_PID=p.pid,readonly_EXIT=code,changes=changes,whole_math_reuse_boundary='Whole mathematics and blind decoder bytes unchanged. Only independently accepted neutral inventory metadata replacement plus derived publication context/binding refresh. Historical reviewer inputs preserved; no reuse of exposed source verdict.',fresh_source_required=True,source_admission=False,PROVED_LOCAL=False,VERIFIED=False))
print('PASS75 exact independent metadata overlay applied; unchanged Lean/decoder; clean source-review packet frozen; source admission remains pending.')
