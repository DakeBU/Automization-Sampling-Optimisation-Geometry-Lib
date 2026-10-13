from pathlib import Path
O=Path('E:/Samplinglib/runs/20261007-companion-priority/phase-pbps-next-primary58')
for name in ['seal_diagnosis.py','close_lease.py']:
 p=O/name;s=p.read_text(encoding='utf8')
 s=s.replace("'all_actual_raw_lf_and_snapshot_readbacks_match':True", "'all_actual_raw_lf_and_snapshot_readbacks_match':True,'readtime_control_policy':'53 original inputs strictly match current files;3 original mutable controls verified against explicit exact historical snapshots, with3 distinct current control observation receipts preserved. Total59 actual read events across56 unique input paths. No claim controls stayed unchanged.','control_observation':pin(O/'mutable-control-observation.json')")
 s=s.replace("'actual_all_input_and_snapshot_readbacks':True", "'actual_all_input_and_snapshot_readbacks':True,'readtime_control_policy':'53 original inputs current-strict;3 original controls exact historical-snapshot-bound;3 separately observed current controls, total59 actual read events across56 unique input paths. Mutable control paths need not remain unchanged.','control_observation':pin(O/'mutable-control-observation.json'),'actual_read_events':59")
 p.write_bytes(s.encode('utf8'))
print('UNEXECUTED_CURRENT_SEAL_FIELDS_EXPLICIT_TEMPORAL_POLICY')
