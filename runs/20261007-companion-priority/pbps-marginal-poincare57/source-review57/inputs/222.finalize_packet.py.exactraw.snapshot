from pathlib import Path
import sys, json
sys.dont_write_bytecode = True
from build_packet import ROOT, OUT, SELF, native, pin, write, now

def check_inputs():
    manifest=native(OUT/'input-manifest.json')
    for record in manifest['source_inputs']+manifest['postfreeze_inputs']:
        if 'raw_sha256' not in record: continue
        assert pin(ROOT/record['path'])==record, record['path']
    for name in ['graph.packet.json','source-only-freeze.json','coverage.citation-supplement.json','binder-and-reuse-audit.json','lease.open.json']:
        native(OUT/name)
    graph=native(OUT/'graph.packet.json')
    ids={n['id'] for n in graph['nodes']}; assert len(ids)==len(graph['nodes'])
    for e in graph['edges']:
        assert all(p in ids for p in e['parents']) and e['consumer'] in ids
        assert e['consumer_use_site'] and e['conditional_discharge']
    freeze=native(OUT/'source-only-freeze.json')
    citations=native(OUT/'coverage.citation-supplement.json')
    for r in freeze['coverage']+citations['coverage']:
        assert r['disposition'] in ['NODE','EXCLUDED'] and r['reason']
        if r['disposition']=='NODE': assert r['node_id'] in ids
    assert freeze['chronology']['prospective_statement_read'] is False
    assert graph['independent_review']['status']=='PENDING'

check_inputs()
if sys.argv[1:]==['--check']:
    lease=native(OUT/'lease.json'); assert lease['state']=='CLOSED'
    for p in lease['outputs']: assert pin(ROOT/p['path'])==p, p['path']
    print(json.dumps(dict(status='READONLY_CHECK_OK',exit_code=0,closed_lease=pin(OUT/'lease.json'))))
else:
    assert not sys.argv[1:] and not (OUT/'lease.json').exists(), 'Do not overwrite closed lease'
    # Snapshot proposal JSONs are pinned byte copies; they intentionally retain their original native schema.
    for p in OUT.glob('*.json'):
        x=json.loads(p.read_bytes())
        if SELF in x: native(p)
    write('complete.json',dict(schema_version=1,actor='/root/sourcegraph57',status='SOURCE_GRAPH_PACKET_COMPLETE_REVIEW_PENDING',checked_at=now(),source_first_process=dict(chunk_id='fe4245',exit_code=0),candidate_binding_process=dict(chunk_id='7c355d',exit_code=0),native_objects_checked=True,source_raw_lf_inputs_checked=True,graph_edge_references_checked=True,coverage_dispositions_checked=True,compiler_started=False,proof_started=False,production_or_ledger_written=False,independent_review_pending=True,source_or_Lean_admission=False))
    outputs=[pin(p) for p in sorted(OUT.iterdir()) if p.is_file() and p.name!='lease.json']
    for p in outputs: assert pin(ROOT/p['path'])==p
    lease=write('lease.json',dict(schema_version=1,actor='/root/sourcegraph57',state='CLOSED',closed_at=now(),outputs=outputs,input_manifest=pin(OUT/'input-manifest.json'),finalizer='Synchronous bundled Python; no compiler/helper/background process; all file handles closed; this lease is final file written; enclosing tool must observe EXIT0',compiler_started=False,proof_started=False,review_status='PENDING_DISTINCT_SOURCE_REVIEW',mathematical_admission=False,hash_contract='Complete native object minus only declared content_self_sha256; UTF8 ensure_ascii=False sorted compact JSON. Raw/LF byte hashes are separately pinned.'))
    assert native(OUT/'lease.json')['state']=='CLOSED'
    print(json.dumps(dict(status='CLOSED_LAST_FINALIZER_OK',exit_code=0,lease=lease,output_count=len(outputs))))
