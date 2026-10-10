from common import *
import gzip
native=J(R/'exact-science-verification/native.review.json'); adoption=J(R/'root.exact-verification61.adoption.json'); maps=adoption['exact_historical_resolutions'][:]
# Each added SCI cell snapshot must itself match the exact original raw pin, not just LF.
for row in native['verified_pins']:
 if '/frontier-cells/' in row['path'] and path(row['path']).name in ['ASTIS-SHARED-l2-positive-real-square-root.json','ASTIS-SW-PBPS-real-defect-root.json']:
  try: matches(row); continue
  except AssertionError: pass
  n=path(row['path']).relative_to(ROOT).as_posix(); b=git('show',SCI+':'+n); dst=P/('science-cell-'+H(n.encode())+'.exactraw.snapshot.json'); dst.write_bytes(b); matches(row,dst); maps.append(dict(original=row,exact_raw_snapshot=pin(dst),authority='Exact named SCI Git blob raw equality to original native pin; no LF-to-raw reconstruction'))
def resolve(row):
 try: return matches(row),None
 except (AssertionError,FileNotFoundError):
  for m in maps:
   a=m['original']
   if path(a['path'])==path(row['path']) and a['raw_sha256']==row['raw_sha256'] and a['lf_sha256']==row.get('lf_sha256',a['lf_sha256']):
    matches(m['exact_raw_snapshot']); return matches(row,m['exact_raw_snapshot']['path']),m
  raise
verified=[]; used=[]
for row in native['verified_pins']:
 actual,m=resolve(row);verified.append(dict(original=row,actual=actual,historical_mapping=m));
 if m and m not in used:used.append(m)
selfchecks=[]
for folder,named in [('independent-math61','named_mathematics_payload'),('exact-science-verification','named_verification_payload'),('source-review61',None)]:
 run=J(R/folder/'run.json'); actual=H(C({k:v for k,v in run.items() if k!='run_sha256'})); assert actual==run['run_sha256']
 if named: payload=H(C(run[named])); assert payload==run[named+'_sha256']; recipe='SHA256 sorted compact UTF8 complete named object'
 else: matches(run['named_payload']); payload=pin(path(run['named_payload']['path']))['raw_sha256']; assert payload==run['named_source_payload_sha256'];recipe='SHA256 exact raw named source payload file bytes'
 lease=J(R/folder/'lease.json'); assert lease['status'] in ['CLOSED','CLOSEDLAST','CLOSED_LAST']
 if 'lease_sha256' in lease: assert H(C({k:v for k,v in lease.items() if k!='lease_sha256'}))==lease['lease_sha256']
 selfchecks.append(dict(folder=folder,complete_whole_run_sha256=actual,whole_recipe='SHA256 sorted compact UTF8 entire object omitting ONLY run_sha256',distinct_named_payload_sha256=payload,named_recipe=recipe,run=pin(R/folder/'run.json'),lease=pin(R/folder/'lease.json')))
dec=J(R/'anonymous-decoder/decoder-native-run.json'); dp=path(R/'anonymous-decoder/decoder-native-run.payload.json').read_bytes(); da=J(R/'root.decoder61.adoption.json');assert H(b'ASTIS-ANONYMOUS-DECODER-NATIVE-RUN-v1\0'+dp)==da['native_run_sha256'];assert H(dp)==da['named_decoder_payload_sha256']; dl=J(R/'anonymous-decoder/closed-lease.json');print('decoder lease keys',list(dl));selfchecks.append(dict(folder='anonymous-decoder',whole_run_sha256=da['native_run_sha256'],whole_recipe=da['run_hash_recipe'],distinct_named_payload_sha256=H(dp),named_recipe=da['payload_hash_recipe'],run=pin(R/'anonymous-decoder/decoder-native-run.json'),lease=pin(R/'anonymous-decoder/closed-lease.json'),source_identity_separation='Preserve original native source text/identity exposure, not invented decoder blindness'))
wh=J(R/'integration61/staging-whitespace/diagnosis.json'); gz=R/'integration61/staging-whitespace/full-staged-immutable-negative.raw.gz'; assert H(gzip.decompress(gz.read_bytes()))==wh['negative_raw_sha256'];assert len(wh['findings'])==332 and len(wh['exact_immutable_raw_paths'])==14 and wh['no_folder_exclusion']; assert wh['authored_complement_exit']==0 and not wh['full_staged_called_PASS']
freeze=J(R/'math-freeze.json'); [matches(row) for row in freeze['inputs']];assert len(freeze['inputs'])==27
W(P/'native.provenance.json',dict(status='PASS_UNCHANGED_NATIVE_SCIENCE_EVIDENCE',actual_PID=os.getpid(),verified_original_rows=len(verified),qualified_pins=verified,finite_exact_history_mappings=used,complete_native_self_checks=selfchecks,original_math_freeze_count=27,full_proof_review_reused='Complete independent body/10providers/Test reviewed in CLOSED math61; same SCI/integration LF/compiled source byte equality independently checked; no proof replay',original_science_entries=pin(R/'exact-science-verification/science.entries.json'),original_science_count=691,whitespace= dict(integration_findings=332,exact_immutable_path_count=14,raw_negative_sha256=wh['negative_raw_sha256'],gzip=pin(gz),diagnosis=pin(R/'integration61/staging-whitespace/diagnosis.json'),authored_complement_PASS=True,full_staged_PASS=False,science_findings=108,science_exact_paths=14)))
print('NATIVE_PROVENANCE_PASS',len(verified),'pins',len(used),'exact maps',len(selfchecks),'native self recipes')
