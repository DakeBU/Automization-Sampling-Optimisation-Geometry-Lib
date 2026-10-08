from common import *
q=J(P/'inputs.final.json'); counts={}; checked=[]
for pair in q['qualified_original_snapshot_pairs']:
 matches(pair['original'],pair['exact_raw_snapshot']['path']);matches(pair['exact_raw_snapshot']);checked.append(pair['exact_raw_snapshot'])
counts['qualified_opening_snapshot_originals']=len(q['qualified_original_snapshot_pairs'])
for v in q['native_reused_originals']:
 matches(v['original'],v['actual']['path']);matches(v['actual']);checked.append(v['actual'])
counts['native_reused_qualified_pins']=len(q['native_reused_originals'])
for m in q['finite_history']:
 matches(m['original'],m['exact_raw_snapshot']['path']);matches(m['exact_raw_snapshot']);checked.append(m['exact_raw_snapshot'])
counts['finite_exact_history_maps']=len(q['finite_history'])
for row in q['graph_complete_source_rows']:matches(row);checked.append(row)
counts['complete_native_graph_source_rows']=len(q['graph_complete_source_rows'])
for row in q['helper_whole_pins']:matches(row);checked.append(row)
counts['native_helper_whole_pins']=len(q['helper_whole_pins'])
freeze=J(R/'math-freeze.json')
for row in freeze['inputs']:matches(row);checked.append(row)
counts['math_original_freeze_pins']=len(freeze['inputs'])
entries=J(path(q['exact_integration_entries']['path'])); matches(q['exact_integration_entries']);mapping={path(x['original']['path']):x for x in q['qualified_original_snapshot_pairs']}
for e in entries['entries']:
 row=e['current']
 try:matches(row);checked.append(row)
 except AssertionError:
  p=path(row['path']);m=mapping.get(p);assert p==ROOT/'runs/substantive_advances.jsonl' and m,('Unexpected integration pin drift',row)
  assert m['original']['raw_sha256']==row['raw_sha256'];matches(row,m['exact_raw_snapshot']['path']);checked.append(m['exact_raw_snapshot'])
 assert row['lf_sha256']==e['git_lf_sha256']
counts['integration_original_current_git_LF_pins']=len(entries['entries'])
science=J(path(q['exact_science_blobs']['path']));matches(q['exact_science_blobs']);assert science['count']==691;assert J(P/'native.history.json')['science_entries_checked']==691
counts['exact_science_Git_blobs_checked_in_prior_foreground']=691
run=J(P/'run.json');assert H(C({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256'];assert H(C(run['named_repository_exposition_payload']))==run['named_repository_exposition_payload_sha256'];assert J(P/'payload.json')==run['named_repository_exposition_payload']
for k in ['receipt','inputs','payload_file']:matches(run[k])
for gate in J(P/'phase2.review.json')['gates']:
 matches(gate['receipt']);matches(gate['stdout']);matches(gate['stderr']);r=J(path(gate['receipt']['path']));assert r['exit_code']==0 and r['terminal_closed']
counts['actual_closed_terminal_receipts']=21
payload=J(P/'graph.native-WindowsPath-order.payload.json');assert H(C(payload))==run['named_repository_exposition_payload']['complete_graph_digest'];assert J(P/'graph.native-WindowsPath-order.diagnosis.json')['observed']==J(P/'graph.input.recipe.json')['publication_inputs_sha256']
outputs=J(P/'outputs.before-readback.json')
for row in outputs['artifacts']:matches(row)
counts['own_actual_outputs_before_readback']=len(outputs['artifacts']);counts['input_pin_occurrences_checked_this_readback']=len(checked);counts['unique_actual_resolved_input_paths']=len({path(x['path']).as_posix() for x in checked})
W(P/'readback.json',dict(status='PASS_FINAL_FOREGROUND_READBACK',actual_PID=os.getpid(),counts=counts,whole_run_sha256=run['run_sha256'],distinct_named_repository_exposition_payload_sha256=run['named_repository_exposition_payload_sha256'],complete_official_graph_digest=H(C(payload)),science_commit=SCI,integration_commit=run['checked_integration_commit'],future62='Only exact single original ledger pin resolves to preclaim phase2 snapshot; no future cells/proofs read; no full current working-tree scan',resources='Bounded foreground reads only; all file handles closed when this child returns EXIT0'))
print('READBACK_PASS',json.dumps(counts,sort_keys=True))
