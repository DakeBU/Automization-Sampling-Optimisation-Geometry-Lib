from common import *
m=J(P/'input.manifest.json');primary=J(P/'primary.first.json');matches(primary['primary_original']);b=path(primary['primary_original']['path']).read_bytes();checks=1
for r in primary['regions']:
 matches(r['raw_source_snapshot']);s,e=r['byte_range'];assert b[s:e]==path(r['raw_source_snapshot']['path']).read_bytes();checks+=1
supp=J(P/'source-cap.supplement.json');s,e=supp['byte_range'];matches(supp['raw_source_snapshot']);assert b[s:e]==path(supp['raw_source_snapshot']['path']).read_bytes();checks+=1
for r in m['qualified_input_snapshot_pairs']:matches(r['original']);matches(r['original'],r['exact_raw_snapshot']['path']);matches(r['exact_raw_snapshot']);checks+=3
for w in m['selected_API_windows']:
 matches(w['whole_original']);matches(w['exact_raw_selected_bytes']);matches(w['LF_selected_bytes']);raw=path(w['whole_original']['path']).read_bytes();part=b''.join(raw.splitlines(keepends=True)[w['line_start']-1:w['line_end']]);assert part==path(w['exact_raw_selected_bytes']['path']).read_bytes();assert part.replace(b'\r\n',b'\n')==path(w['LF_selected_bytes']['path']).read_bytes();checks+=3
for row in m['first3_candidate62_freeze_pins_verified']:matches(row);checks+=1
r=J(P/'run.json');assert H(C({k:v for k,v in r.items() if k!='run_sha256'}))==r['run_sha256'];assert H(C(r['named_source_API_payload']))==r['named_source_API_payload_sha256'];assert J(P/'payload.json')==r['named_source_API_payload'];
for k in ['receipt','inputs','payload_file']:matches(r[k]);checks+=1
out=J(P/'outputs.before-readback.json')
for row in out['artifacts']:matches(row)
assert len(J(P/'contracts.json')['route_max7'])==7
current=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip();W(P/'readback.json',dict(status='PASS_ACTUAL_FOREGROUND_READBACK',actual_PID=os.getpid(),source_API_input_pin_check_occurrences=checks,counts=dict(primary_original=1,source_regions=24,initial_primary_regions=23,supplemental_cap_regions=1,whole_original_snapshot_pairs=19,API_windows=16,candidate62_math_freeze_originals_checked=3,own_outputs_before_readback=len(out['artifacts']),actual_input_pin_check_occurrences=checks),opening_base=primary['checked_base_commit'],observed_HEAD_at_readback=current,base_scope='Source/API scout binds actual immutable source/provider raw bytes; no admission inferred if globalHEAD advances',whole_run_sha256=r['run_sha256'],distinct_named_source_API_payload_sha256=r['named_source_API_payload_sha256'],compiler='NOT_STARTED_CLOSED',no_canonical_Git_proof_state_mutations=True))
print('SCOUT63_READBACK_PASS',checks,'pin checks',current)
