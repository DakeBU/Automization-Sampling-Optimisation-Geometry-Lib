from pathlib import Path
import hashlib,json,os,subprocess,sys
root=Path.cwd();r=Path('runs/20261007-companion-priority/pbps-ambient-adjoint66');d=r/'independent-math66'
load=lambda p:json.loads(p.read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def pin(p):
    b=p.read_bytes();return dict(path=p.as_posix(),bytes=len(b),raw_sha256=sha(b))
def check(x):
    b=Path(x['path']).read_bytes();lf=b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
    assert len(b)==x['raw_bytes'] and sha(b)==x['raw_sha256']
    assert len(lf)==x['lf_bytes'] and sha(lf)==x['lf_sha256']
def write(p,x):
    assert not p.exists(),p
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
lease=load(d/'lease.final.json');run=load(d/'run.json')
assert sha((d/'lease.final.json').read_bytes())=='c2f4c941bfe3a7ed09ab050253d0ad46818cc21d3f95c2d1e9d89ec736ebffcc'
assert lease['status']=='CLOSED_LAST' and lease['last_owned_write'] and lease['final_owned_file_count']==133
logical=sha(json.dumps({k:v for k,v in run.items() if k!='run_sha256'},ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
assert logical==run['run_sha256']==lease['whole_logical_run_sha256']=='3313a5ed421f2dcfb6535dbecb828bc0f013fbd572b42267d69886114ce445d1'
assert sha((d/'mathematical-review.named.raw.json').read_bytes())==lease['complete_named_RAW_review_sha256']=='feacfe6fb97bd20971111eff3d799de1cf266a9a99717d3b8dc14a786d155bca'
owned={Path(x['path']).resolve().relative_to(d.resolve()).as_posix() for x in lease['all_owned_except_this_final_lease']}|{'lease.final.json'}
assert owned=={p.relative_to(d).as_posix() for p in d.rglob('*') if p.is_file()} and len(owned)==133
for x in lease['all_owned_except_this_final_lease']:check(x)
assert (d/'lease.final.json').stat().st_mtime_ns>=max(p.stat().st_mtime_ns for p in d.rglob('*') if p.is_file())
out=r/'math-adoption66';out.mkdir(exist_ok=False)
post=subprocess.run([sys.executable,'-B',str(d/'close66.py'),'postclose'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
(out/'postclose.stdout.log').write_bytes(post.stdout);(out/'postclose.stderr.log').write_bytes(post.stderr)
assert post.returncode==0,post.stderr.decode(errors='replace')
post_result=json.loads(post.stdout);assert post_result['writes']==0 and post_result['owned_files']==133
proposal=load(r/'presentation-overlay66/proposal.json');overlay=load(r/'presentation-overlay66/applied.json')
assert overlay['status']=='EXACT_INDEPENDENTLY_REVIEWED_FOUR_CATALOGUE_FIELDS_APPLIED'
allowed={Path(x['canonical']).resolve():x['before']['raw_sha256'] for x in proposal['entries']}
ap=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261009-PBPSAmbientAdjointCorrector.json').resolve()
allowed[ap]='771b002ca6add4d530102948950798cbfffb7b6d12d8bff4a268da8f2a07f39c'
inputs=load(d/'inputs.manifest.json')['inputs'];assert len(inputs)==38
resolutions=[]
for x in inputs:
    check(x['RAW_snapshot']);check(x['LF_snapshot'])
    original=x['original'];p=Path(original['path']);b=Path(x['RAW_snapshot']['path']).read_bytes()
    assert sha(b)==original['raw_sha256'] and len(b)==original['raw_bytes']
    assert Path(x['LF_snapshot']['path']).read_bytes()==b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
    if p.read_bytes()!=b:
        assert p.resolve() in allowed and original['raw_sha256']==allowed[p.resolve()]
        resolutions.append(dict(original=original,exact_native_frozen_RAW=x['RAW_snapshot'],exact_native_frozen_LF=x['LF_snapshot'],approved_current=pin(p),reason='Exact bounded decoder/catalogue advancement; original mathematical input remains the named frozen bytes.'))
assert len(resolutions)==5
for x in load(d/'inputs.api-supplement.json')['inputs']:
    check(x['original']);check(x['RAW_snapshot']);check(x['LF_snapshot'])
focused=load(d/'focused.result.json');structure=load(d/'structural-math-check.result.json');review=load(d/'mathematical-review.json')
assert focused['status']=='PASS' and focused['Lake_jobs']==3946 and focused['Lake_replay_present']
assert focused['fresh_main_proof_compiled'] and focused['fresh_genuine_Test_proof_compiled']
assert all(x['standard3_only'] and set(x['exact_axioms'])=={'propext','Classical.choice','Quot.sound'} for x in focused['exact_public_axiom_parsing'])
for file,pid in [('fresh-main.receipt.json',35940),('fresh-Test.receipt.json',50788)]:
    x=load(d/file);assert x['exit_code']==0 and x['terminal_closed'] and x['actual_foreground_pid']==pid
assert structure['status']=='PASS' and structure['whole_main_and_Test_read'] and len(structure['all6_literal_BODY_formula_steps'])==6
for step in structure['all6_literal_BODY_formula_steps']:
    q=step['source_region'];b=Path(q['path']).read_bytes();span=b''.join(b.splitlines(keepends=True)[q['start_line']-1:q['end_line']])
    assert sha(b)==q['source_raw_sha256'] and sha(span)==q['exact_code_raw_sha256'] and step['literal_BODY_match']
assert review['status']==run['status']=='ACCEPTED_BOUNDED_PRECOMMIT_MATHEMATICS'
assert not review['VERIFIED_transition'] and not lease['source_verdict_consumed']
write(r/'root.math66.adoption.json',dict(status='INDEPENDENT_PRECOMMIT_MATHEMATICS66_ACCEPTED',actual_root_pid=os.getpid(),native_whole_logical_run_sha256=logical,native_complete_named_RAW_sha256=lease['complete_named_RAW_review_sha256'],native_lease=pin(d/'lease.final.json'),native_owned_files=133,frozen_inputs=38,actual_used_API_inputs=4,root_read_only_postclose=post_result,literal_BODY_steps=6,fresh_main_pid=35940,fresh_Test_pid=50788,Lake_replay_separately_classified=True,finite_historical_resolutions=resolutions,original_publication_catalogue_blocker_retained=True,separately_reviewed_exact_catalogue_resolution=pin(r/'presentation-overlay66/applied.json'),source_verdict_consumed=False,exact_SCI66_verification=False,PROVED_LOCAL=False,VERIFIED=False,full_paper_Goal=False))
print('PASS math66 CLOSED133/38 frozen+4 API inputs; fresh both standard3,6 literal BODY steps; five explicit historical maps, separately reviewed catalogue resolution. No source/commit verification claim.')
