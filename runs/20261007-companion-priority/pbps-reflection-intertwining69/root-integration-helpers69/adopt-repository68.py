from pathlib import Path
import hashlib, json, os, subprocess

r = Path('runs/20261007-companion-priority/pbps-sharp-energy68')
o = r/'independent-repository-exposition68'
load = lambda p: json.loads(Path(p).read_bytes())
sha = lambda b: hashlib.sha256(b).hexdigest()
canonical = lambda x: json.dumps(x, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()
native_lf = lambda b: b.replace(b'\r\n', b'\n').replace(b'\r', b'\n')

def check(p, z):
    b=Path(p).read_bytes(); lf=native_lf(b)
    assert len(b)==z['RAW_bytes'] and sha(b)==z['RAW_sha256'], p
    assert len(lf)==z['LF_bytes'] and sha(lf)==z['LF_sha256'], p

lease=load(o/'lease.final.json')
assert sha((o/'lease.final.json').read_bytes())=='85accd664a4e3838647a5d81157fab54242a6ed70ae12f729011c701f2fd6ebe'
assert lease['status']=='CLOSED_LAST' and lease['last_owned_write']=='lease.final.json'
assert lease['actor']=='/root/independent_header_source68'
check(o/'owned-manifest.json', lease['owned_manifest'])
m=load(o/'owned-manifest.json'); rows=m['rows']
assert m['LF_rule']=='Replace CRLF with LF, then remaining CR with LF; byte projection also retained for binary snapshots.'
assert len(rows)==m['entry_count']==392
assert sha(canonical(rows))==m['rows_canonical_sha256']==lease['owned_rows_canonical_sha256']
actual={p.relative_to(o).as_posix() for p in o.rglob('*') if p.is_file()}
assert actual=={z['path'] for z in rows}|{'owned-manifest.json','lease.final.json'}
assert len(actual)==lease['total_owned_file_count_including_manifest_and_final_lease']==394
last=(o/'lease.final.json').stat().st_mtime_ns
for z in rows:
    p=o/z['path']; check(p,z); assert p.stat().st_mtime_ns<=last,p
assert (o/'owned-manifest.json').stat().st_mtime_ns<=last
run=load(o/'review-run.json'); h=run.pop('run_sha256')
assert sha(canonical(run))==h==lease['whole_logical_run_sha256']=='039bb9c7f2c85e22263bf45ffaea3462faea42fed462a45299952ab119d8556c'
for key in ['complete_named_RAW_review','complete_named_RAW_decision','complete_named_RAW_input_payload','whole_logical_run_file','final_readback']:
    z=lease[key]; check(o/z['path'],z)
assert (o/'review-run.json').read_bytes()==(o/'complete-RAW-review.json').read_bytes()
i=load(o/'complete-RAW-input.json')
assert len(i['entries'])==i['entry_count']==lease['finite_input_count']==176
for z in i['entries']:
    check(z['source_path'],z)
    b=(o/z['raw_snapshot']).read_bytes(); lf=(o/z['lf_snapshot']).read_bytes()
    assert len(b)==z['RAW_bytes'] and sha(b)==z['RAW_sha256']
    assert lf==native_lf(b) and sha(lf)==z['LF_sha256']
d=load(o/'complete-RAW-decision.json')
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
assert d['checked_commit']==lease['checked_commit']==head=='3ad3b127b5a645be9cf71b3d14520b2d8fea3122'
assert d['verdict']=='ACCEPT_BOUNDED_SERIALIZED_REPOSITORY_SCOPED_READER_AND_CURRENT_GRAPH_WITH_EXPLICIT_DEBTS'
assert d['blocking_findings']==[] and d['independent_from_formalizer_and_stabilization_owner']
for key in ['repository_scoped_integration','scoped_local_reader_with_explicit_debts','current_graph_freshness_and_coverage','source_mathematics_reused_exactly']:
    assert d['acceptance'][key]
for key in ['full_Exposition_Seal','PURIFIED','remoteCI_main_live','wholeSAU_or_wholepaper_or_Goal_complete']:
    assert not d['acceptance'][key]
for z in d['final_cell_RAW']:
    b=Path(z['path']).read_bytes(); assert len(b)==z['bytes'] and sha(b)==z['raw_sha256']
assert sha(Path('_site/data/underlying-lean-graph.json').read_bytes())==d['current_graph_RAW_sha256']
g=load(o/'current-graph-and-integration.readback.json')
assert g['full_publication_graph_validator_errors']==[]
assert g['recomputed_publication_inputs_sha256']==d['publication_inputs_sha256']
for k in ['repository-graph-stage1','repository-reader-stage2','final_native_readback']:
    assert lease['actual_terminal_receipts'][k]['actual_exit_code']==0
for k in ['negative-stage1-v1','negative-stage1-v2']:
    assert lease['actual_terminal_receipts'][k]['actual_exit_code']==1
dest=r/'root.repository68.adoption.json'; assert not dest.exists()
payload=dict(schema='root-readonly-native-repository68-adoption-v1',actual_foreground_pid=os.getpid(),
    accepted_scoped_aggregate=True,accepted_current_graph=True,native_owned_file_count=394,finite_current_inputs=176,
    exact_science_commit=head,whole_logical_run_sha256=h,native_lease_RAW_sha256=sha((o/'lease.final.json').read_bytes()),
    native_RAW_payloads={k:lease[k] for k in ['complete_named_RAW_review','complete_named_RAW_decision','complete_named_RAW_input_payload']},
    final_cells=d['final_cell_RAW'],current_graph_publication_inputs_sha256=d['publication_inputs_sha256'],
    native_decision=d['verdict'],independent_reviewer=d['reviewer'],retained_nonblocking_debts=d['nonblocking_debts'],
    native_LF_recipe=m['LF_rule'],root_observer_LF_recipe='CRLF to LF only; distinct from this native recipe; RAW authority unchanged.',
    retained_root_adapter_negative='integration68/adopt-repository68/receipt.json: PID47964 EXIT1 used the wrong LF recipe; no native mutation.',
    zero_postclose_owned_writes=True,native_files_mutated=False,historical_INT66_freshness_withholding_unchanged=True,
    full_Exposition=False,PURIFIED=False,main_live=False,full_paper=False,whole_Goal_complete=False)
dest.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(dict(status='PASS_NATIVE_REPOSITORY68_ADOPTED',owned_files=394,current_inputs=176,accepted_scoped_aggregate=True,full_paper=False)))
