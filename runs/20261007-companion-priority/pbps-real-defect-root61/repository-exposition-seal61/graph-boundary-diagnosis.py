from common import *
negative=J(P/'graph.freshness.negative.json'); payload=J(P/'graph.exact-integration-input.payload.json')
for cid,c in payload['cells'].items():
 if c is not None: c['__path__']='research-wiki/frontier-cells/'+cid+'.json'
native_raw=H(C(payload)); lf_payload=dict(payload,lean=negative['diagnostic_LF_source_digest']); native_LF=H(C(lf_payload)); expected=negative['official_frozen_header']
W(P/'graph.after-native-adapter.input.payload.json',payload)
W(P/'graph.after-native-adapter.diagnosis.json',dict(status='GRAPH_DIGEST_STILL_DIFFERS_AFTER_EXACT_NATIVE_ADAPTER',actual_PID=os.getpid(),complete_native_raw_digest=native_raw,diagnostic_LF_source_graph_digest=native_LF,official_frozen_header=expected,LF_source_only_matches_official=native_LF==expected,complete_corrected_raw_payload=pin(P/'graph.after-native-adapter.input.payload.json'),actual_cell_loader=pin(ROOT/'tools/astis_frontier_cells.py'),source_rows=negative['source_rows'],source_raw_digest=negative['source_digest_actual_raw'],source_LF_digest=negative['diagnostic_LF_source_digest'],scope='Exact d1b integration tree/allitems/allreferencedcells with actual native __path__; no future sources read; raw source_digest versus LF diagnostic separately declared'))
print('RAW',native_raw,'LF_DIAGNOSTIC',native_LF,'EXPECTED',expected)
