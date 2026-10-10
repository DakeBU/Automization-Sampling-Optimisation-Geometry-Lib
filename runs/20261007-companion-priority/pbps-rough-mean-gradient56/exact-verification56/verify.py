from common import *
import copy,gzip
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0,str(R/'tools'))
import astis,astis_publication,astis_advance
AID='ASTIS-SA-20261008-PBPSRoughMeanGradient';CID='ASTIS-SW-PBPS-rough-mean-gradient'
AUD=R/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261008-PBPSRoughMeanGradient.json';CELL=R/'research-wiki/frontier-cells'/f'{CID}.json'
assert git('rev-parse','HEAD')==BASE
frozen=strict('originals.pre-transition.json')
bindings=[];selfs=[]
def check(e,p=None):
 assert equal(e,p),(e,p);bindings.append({'expected':e,'actual':pin(p or e['path'])});return e
def full(p,field):
 x=selfcheck(p,field);selfs.append(x);return load(p)
W=B/'whole-math56';wr=full(W/'run.json','run_sha256');wh=full(W/'receipt.json','receipt_sha256');wl=full(W/'lease.json','lease_sha256')
assert wl['status']=='CLOSED' and wr['review_binding_sha256']==logical(wr['review_binding_payload'])
for e in wr['inputs']['inputs']+wr['outputs_before_run']:check(e)
for e in (wl['receipt'],wl['run'],wl['readback'],wl['compiler_closed_lease']):check(e)
wc=load(W/'checks.json')
for e in wc['native_full_self_checks']:
 d=load(e['input']['path']);check(e['input']);field=e['self_field'];h=logical({k:v for k,v in d.items() if k!=field});assert h==e.get('logical_sha256',e.get('whole_logical_sha256'))
for e in wc['actual_CLOSED_prior_leases']:check(e['input']);assert load(e['input']['path'])['status']=='CLOSED'
assert wh['verdict']=='ACCEPT_SCOPED_NO_MATHEMATICAL_BLOCKER' and load(W/'mathematical-reasons.json')['mathematical_repair_required']==False
S=B/'source-review56';sr=full(S/'reviewer.source.run.json','run_sha256');sc=full(S/'complete.json','content_self_sha256');sm=full(S/'manifest.json','content_self_sha256');report=full(S/'source.review.json','content_self_sha256');sl=full(B/'source.review.lease.json','content_self_sha256')
assert sr['run_sha256']=='340a5136e28a8da11bbf7e285b83894416b54d4f743df3cdf26ba24d535568a8' and sl['status']=='CLOSED'
assert sl['read_lease']==sl['write_lease']==sl['Python_lease']=='CLOSED' and sl['compiler_lease']=='NOT_STARTED_CLOSED'
adopt=load(B/'root.source56.adoption.json');maps={m['original']['path']:m for m in adopt['historical_review_input_snapshot_mapping']};assert set(maps)=={AUD.relative_to(R).as_posix(),CELL.relative_to(R).as_posix()}
iv=load(S/'input-verification.json');assert len(iv['inputs'])==432
historical=[]
for e in iv['inputs']:
 original=e['input'];raw=e['exactraw_snapshot'];lf=e['crlf_to_lf_snapshot'];check(raw);check(lf)
 assert original['raw_sha256']==raw['raw_sha256'] and original['lf_sha256']==raw['lf_sha256'] and original['bytes']==raw['bytes']
 assert path(raw['path']).read_bytes().replace(b'\r\n',b'\n')==path(lf['path']).read_bytes()
 if original['path'] in maps:
  m=maps[original['path']];assert m['original']==original and m['exactraw_snapshot']==raw
  assert not equal(original);historical.append({'original':original,'exact_reviewed_before_snapshot':raw,'current_admitted':pin(original['path']),'reason':'Only canonical audit/cell administrative source admission; full original raw/LF identity to immutable snapshot verified'})
 else:check(original)
assert len(historical)==2
for e in sm['outputs']:check(e)
assert len(sm['outputs'])==889
for k in ('manifest','standard_result','native_run','source_report','operational_repair','operational_repair_closed_lease'):check(sc[k])
for e in sl['output_artifacts']:check(e)
res=load(S/'result0.json');audit=load(AUD)
assert res['verdict']=='equivalent-after-elaboration' and res['review_run_sha256']==sr['run_sha256'] and res['independent_from_formalizer'] and res['independent_from_decoder']
assert audit['state']=='accepted' and audit['verdict']==res['verdict'] and audit['source_review']['review_run_sha256']==sr['run_sha256']
q=adopt['canonical_nonblocking_delta_adapter'];assert q['native_deltas']==res['deltas'] and q['canonical_deltas']==audit['deltas'] and len(res['deltas'])==3
recomputed=[{'slot':d['slot'],'severity':'blocking' if d['blocking'] else 'informational','description':d['description'],'evidence':f"Independent source review classification: {d['classification']}; {'blocking' if d['blocking'] else 'nonblocking'}."} for d in res['deltas']]
assert recomputed==audit['deltas'] and all(not d['blocking'] for d in res['deltas'])
packet=full(B/'source.0.reviewer-packet.json','packet_sha256')
pub=load(R/'website/content/publications/pbps-rough-mean-gradient.json')['items'][0];lesson=load(R/'website/content/declaration_lessons/pbps-rough-mean-gradient.json');units=lesson.get('units',lesson.get('lessons',[]));assert len(units)==1
payload=copy.deepcopy(packet['candidate_publication_context']);del payload['candidate_assumptions'];payload['lesson']=units[0];payload['binding']={k:v for k,v in pub['bindings'][0].items() if k not in ('audit_id','legacy_audit_debt')}
assert logical(payload)==packet['publication_binding_sha256']==audit['publication_binding_sha256']==sr['publication_binding_sha256']
assert packet['lean']['statement_sha256']==sha(packet['lean']['statement'].encode())
P=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/RoughMeanGradient.lean';Q=R/'Tests/ProximalBPSRoughMeanGradient.lean'
assert P.read_text(encoding='utf-8')==packet['candidate_publication_context']['current_lean_module']
header=P.read_text(encoding='utf-8');header=header[header.index('theorem actual_rough_mean_gradient'):header.index(' := by')]+'\n';assert len(header.encode())==1755 and sha(header.encode())=='fea2c3ade170bc0526d659f8c51abedaa0ce1a6186e75f0d8a2532b6608e94d8'
assert P.read_bytes()==(W/'production.raw.snapshot.lean').read_bytes() and Q.read_bytes()==(W/'Tests.raw.snapshot.lean').read_bytes()
D=B/'anonymous-decoder';dr=full(D/'run.json','run_sha256');dl=full(D/'lease.json','closure_record_sha256');dp=full(D/'packet0.json','packet_sha256');dres=load(D/'result0.json')
assert dr['run_sha256']=='08dccc416d1c02f960f6026bfe11e196e77015cb548e5f84bbfed1154352f671' and dl['status']=='CLOSED' and not dres['source_text_visible'] and not dr['source_text_visible']
assert isinstance(dres['decoder'],str) and isinstance(dres['reconstructed_theorem_text'],str) and dres['decoder_run_sha256']==dr['run_sha256']
assert dres['reconstructed_theorem_text']==packet['blind_reconstruction']['text'] and sha(dres['reconstructed_theorem_text'].encode())==dres['reconstructed_text_sha256']
assert packet['blind_reconstruction']['decoder_packet_sha256']==dp['packet_sha256']
overlay=load(B/'decoder-locator-repair56/overlay.json');rr=full(S/'decoder-locator-review56/review.json','content_self_sha256');rrun=full(S/'decoder-locator-review56/reviewer.operational.run.json','content_self_sha256');rl=full(S/'decoder-locator-review56/lease.json','content_self_sha256')
assert rr['verdict']=='ACCEPT_EXACT_OPERATIONAL_LOCATOR_OVERLAY_ONLY' and rl['status']=='CLOSED' and overlay['operation_count']==rr['operation_count']==6
assert not overlay['closure_status_or_native_digest_mutated'] and not overlay['statement_or_reconstruction_or_source_change']
malformed=[]
def find(x,ptr=''):
 if isinstance(x,dict):
  if set(x)=={'Length'}:malformed.append(ptr)
  else:
   for k,v in x.items():find(v,ptr+'/'+k)
 elif isinstance(x,list):
  for i,v in enumerate(x):find(v,ptr+'/'+str(i))
find(dl);assert set(malformed)=={op['pointer'] for op in overlay['operations']} and len(malformed)==6
for op in overlay['operations']:
 x=dl
 for t in op['pointer'].strip('/').split('/'):x=x[int(t)] if isinstance(x,list) else x[t]
 assert x==op['before'] and isinstance(op['after'],str) and len(op['after'])==x['Length']
 e=op['actual_artifact'];check(e);preserved=D/path(e['path']).name;assert path(e['path']).read_bytes()==preserved.read_bytes()
for n in ('packet0.json','run.json','result0.json','lease.json','initial-lease.raw.snapshot.json'):assert (R/'.astis/decoder-56'/n).read_bytes()==(D/n).read_bytes()
assert load(D/'initial-lease.raw.snapshot.json')['status']=='OPEN'
for e in load(D/'binding-receipt.json')['output_artifacts']:check(e)
# One bounded Git change-entry inventory and cat-file batch; no whole-tree scan.
raw=subprocess.check_output(['git','diff-tree','--no-commit-id','--raw','--no-abbrev','-r','-z',BASE],cwd=R);parts=raw.split(b'\0');entries=[]
for i in range(0,len(parts)-1,2):
 meta=parts[i].decode().split();p=parts[i+1].decode();assert meta[4] in ('A','M') and not re.search(r'(?:57|58)(?:/|$)',p)
 entries.append({'path':p,'mode':meta[1],'Git_blob':meta[3],'status':meta[4]})
assert len(entries)==1361
buf=subprocess.check_output(['git','cat-file','--batch'],cwd=R,input=('\n'.join(e['Git_blob'] for e in entries)+'\n').encode());offset=0
for e in entries:
 end=buf.index(b'\n',offset);h=buf[offset:end].decode().split();size=int(h[2]);blob=buf[end+1:end+1+size];offset=end+1+size+1
 assert h[0]==e['Git_blob'] and h[1]=='blob' and blob.replace(b'\r\n',b'\n')==path(e['path']).read_bytes().replace(b'\r\n',b'\n'),e['path']
 e.update(current=pin(e['path']),Git_blob_bytes=len(blob),Git_blob_raw_sha256=sha(blob),Git_blob_LF_sha256=sha(blob.replace(b'\r\n',b'\n')))
assert offset==len(buf)
dump('Git-science.entries.json',{'status':'PASS','checked_commit':BASE,'actual_committed_entries':1361,'comparison':'Each actual Git blob against current CRLF-to-LF bytes, plus raw Git/current hashes and bytes; no projected tree hash','entries':entries})
fake=[]
for p in [P,Q,*[R/'AutoSamplingTheory/ExampleCases/ProximalBPS'/n for n in ('SourceMeanGradientDomain.lean','L2MacroscopicMean.lean','MacroscopicEnergy.lean')]]:
 code=astis.strip_lean_comments_and_strings(p.read_text(encoding='utf-8'));hits=[i for i,s in enumerate(code.splitlines(),1) if astis.FORBIDDEN_REGEX.search(s)];assert not hits;fake.append({'input':pin(p),'findings':hits})
log=(O/'focused.log').read_text(encoding='utf-8');assert 'Build completed successfully (3899 jobs)' in log and 'sorryAx' not in log
closures=[{'declaration':n,'axioms':[s.strip() for s in a.split(',')]} for n,a in re.findall(r"'([^']+)' depends on axioms: \[(.*?)\]",log,re.S) if n==TARGET or n.startswith('Tests.ProximalBPSRoughMeanGradient.')]
assert len(closures)==3 and all(set(x['axioms'])=={'propext','Classical.choice','Quot.sound'} for x in closures)
wd=load(B/'whitespace-diagnosis56/diagnosis.json');gb=path(wd['gzip']['path']).read_bytes();assert sha(gb)==wd['gzip']['raw_sha256'];plain=gzip.decompress(gb);assert sha(plain)==wd['full_negative_raw_sha256'] and wd['findings']==48200 and wd['authored_check_exit']==0
whitespace_paths=sorted(set(m.group(1).decode('utf8') for m in re.finditer(rb'(?m)^(.+?):[0-9]+: (?:trailing whitespace|new blank line at EOF|space before tab in indent|indent with spaces|tab in indent)',plain)))
assert len(whitespace_paths)==116,(len(whitespace_paths),whitespace_paths[:3])
dump('immutable-whitespace.paths.json',{'status':'RETAINED_FULL_NEGATIVE_NOT_PASS','findings':48200,'diagnostic_paths':116,'paths':whitespace_paths,'gzip':pin(wd['gzip']['path']),'decompressed_raw_sha256':sha(plain),'authored_complement_gate':'PASS only in retained sequential batches64; no blanket folder exclusion or full-staged PASS'})
astis_publication.check_advance([TARGET],reviewed=True)
state=astis_advance._replay_advances([json.loads(s) for s in (R/'runs/substantive_advances.jsonl').read_text(encoding='utf8').splitlines() if s.strip()]);assert state[AID]['state']=='PROVED_LOCAL' and state[AID]['owner_id']!=ACTOR
stabilizing=[k for k,v in state.items() if v['state']=='STABILIZING'];assert stabilizing==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
assert load(CELL)['status']=='proved_locally'
for p,n in [(CELL,'cell.before.raw.snapshot.json'),(AUD,'audit.before.raw.snapshot.json'),(R/'runs/substantive_advances.jsonl','ledger.before.raw.snapshot.jsonl')]: (O/n).write_bytes(p.read_bytes())
dump('checks.json',{'status':'PASS','checked_commit':BASE,'strict_math_originals':418,'reused_math_distinct_inputs':423,'unchanged_complete_math_receipt':pin(W/'receipt.json'),'unchanged_math_run':pin(W/'run.json'),'source432_originals_checked':432,'source_current_admin_before_mapping':historical,'source889_manifest_outputs_plus_manifest_complete':891,'native_complete_self_checks':selfs,'actual_raw_LF_pin_checks_count':len(bindings),'actual_raw_LF_pin_checks':bindings,'source_native_run':pin(S/'reviewer.source.run.json'),'source_audit':pin(AUD),'canonical_informational_delta_adapter':q,'full_native_publication_binding_sha256':logical(payload),'exact_statement':{'LF_bytes':1755,'LF_sha256':sha(header.encode())},'actual_science_Git_entries':1361,'Git_evidence':pin(O/'Git-science.entries.json'),'fake_closure_scan':fake,'axiom_closures':closures,'source_exposure':sr['exposure_and_negative_chronology'],'decoder_locator_overlay':pin(B/'decoder-locator-repair56/overlay.json'),'separately_reviewed_exact6_overlay':pin(S/'decoder-locator-review56/review.json'),'native_decoder_run':pin(D/'run.json'),'preserved_original_malformed_slots':malformed,'reviewed_publication_gate':'actual astis_publication.check_advance([TARGET], reviewed=True) PASS','current_SAU_state':'PROVED_LOCAL','current_cell_state':'proved_locally','sole_STABILIZING':stabilizing,'immutable_whitespace_debt':pin(O/'immutable-whitespace.paths.json'),'remaining_boundary':wh['remaining_truth_boundary'],'math_blockers':[],'source_blockers':[]})
print(json.dumps({'status':'PASS','checked_commit':BASE,'Git_entries':1361,'math_originals':418,'source_originals':432,'source_outputs':891,'historical_mappings':2,'native_self_checks':len(selfs),'actual_pin_checks':len(bindings),'fake_closure_findings':0,'standard3_closures':3},ensure_ascii=False))
