import datetime,hashlib,json,os,pathlib,subprocess,sys
ROOT=pathlib.Path('E:/Samplinglib'); OUT=pathlib.Path(__file__).resolve().parent
def sha(b): return hashlib.sha256(b).hexdigest()
def canon(x): return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def pin(p):
    b=p.read_bytes(); l=b.replace(b'\r\n',b'\n')
    return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(b),lf_bytes=len(l),raw_sha256=sha(b),lf_sha256=sha(l))
def write(n,x): (OUT/n).write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
def reader(phase):
    command=[sys.executable,str(OUT/'readback_source.py')]+(['final'] if phase=='final' else [])
    with (OUT/f'{phase}.readback.stdout.log').open('wb') as out,(OUT/f'{phase}.readback.stderr.log').open('wb') as err:
        proc=subprocess.Popen(command,cwd=ROOT,stdout=out,stderr=err); pid=proc.pid; code=proc.wait()
    assert code==0, (OUT/f'{phase}.readback.stderr.log').read_text()
    rec=dict(command=command,actual_foreground_pid=pid,exit_code=code,terminal_closed=True,stdout=pin(OUT/f'{phase}.readback.stdout.log'),stderr=pin(OUT/f'{phase}.readback.stderr.log'),scope='Native qualified exact raw/LF source/input/output readback; no Lean compiler or mathematical verification')
    write(f'{phase}.readback.receipt.json',rec); return rec
write('author.foreground.receipt.json',dict(actual_foreground_pid=37564,exit_code=0,terminal_tool_chunk='94d79d',scope='Current source decisions and exact original16 input snapshots; no compiler or canonical mutation'))
# Preserve complete literal decisions inside the named payload, separately from the whole-run hash.
payload=json.loads((OUT/'named-source-review.payload.json').read_bytes())
payload['full_sealed_decisions']=[json.loads((OUT/f'source.{i}.decision.sealed.json').read_bytes()) for i in range(2)]
write('named-source-review.payload.json',payload)
pre=reader('pre')
names=['author_source_review.py','readback_source.py','finalize_source.py','primary-boundary.before-packets.json','input.manifest.json','body-publication.scope-review.json','source.0.decision.sealed.json','source.1.decision.sealed.json','named-source-review.payload.json','author.foreground.receipt.json','pre.readback.stdout.log','pre.readback.stderr.log','pre.readback.receipt.json']
run=dict(schema_version=1,owner='/root/next_primary59',status='CLOSED_INDEPENDENT_POSTPROOF_SOURCE_CONTENT_REVIEW_NOT_VERIFIED',exact_original_lease_inputs=16,qualified_input_pairs=22,primary_regions=23,bounded_source_coverage='23 regions44 NODE/EXCLUDED items reused only after current statement/body/provider/formula comparison',private_providers_checked=26,formula_steps_checked=8,outputs=[pin(OUT/x) for x in names],named_source_payload_sha256=pin(OUT/'named-source-review.payload.json')['raw_sha256'],actual_foreground_pre_readback=pre,actual_foreground_finalizer_pid=os.getpid(),hash_recipe='SHA256 of UTF8 json.dumps(run,ensure_ascii=False,sort_keys=True,separators comma-colon) over entire run excluding ONLY run_sha256',excluded_from_run_hash=['run_sha256'],final_review_derivation='For each i final source.i.review.json is exact entire sealed source.i.decision.sealed.json plus the single review_run_sha256 field equal to this native logical run hash. Final foreground readback verifies exact equality; final receipt and CLOSEDLAST lease bind their raw/LF bytes, avoiding a circular hash self-reference.',named_payload_recipe='Raw SHA256 of complete named-source-review.payload.json, including full sealed decisions and qualified pins; distinct from whole-run logical hash',no_compiler=True,no_canonical_mutation=True,no_prior_postproof_verdict_read=True,no_decoder_credit=True,no_VERIFIED_or_PURIFIED_or_real_root_credit=True)
run['run_sha256']=sha(canon(run)); write('run.json',run)
for i in range(2):
    d=json.loads((OUT/f'source.{i}.decision.sealed.json').read_bytes()); d['review_run_sha256']=run['run_sha256']; write(f'source.{i}.review.json',d)
final=reader('final')
reviews=[pin(OUT/f'source.{i}.review.json') for i in range(2)]
write('native.receipt.json',dict(native_run=pin(OUT/'run.json'),native_run_sha256=run['run_sha256'],named_payload=pin(OUT/'named-source-review.payload.json'),final_reviews=reviews,actual_foreground_pre_readback=pre,actual_foreground_final_readback=final,actual_foreground_finalizer_pid=os.getpid(),closure_scope='Independent scoped source/exposition content accepted; root adoption, independent proof verification/stabilization/UI/full exposition/purification remain separate'))
receipt=pin(OUT/'native.receipt.json'); runpin=pin(OUT/'run.json')
print(json.dumps(dict(actual_foreground_finalizer_pid=os.getpid(),pre_readback_pid=pre['actual_foreground_pid'],final_readback_pid=final['actual_foreground_pid'],both_readback_exit_codes=[0,0],run_sha256=run['run_sha256'],named_source_payload_sha256=run['named_source_payload_sha256'],final_review_sha256=[x['raw_sha256'] for x in reviews]),ensure_ascii=True),flush=True)
# CLOSED-LAST: no subsequent filesystem operation. Both real reader child processes have exited0.
write('lease.json',dict(status='CLOSED',closed_last=True,owner='/root/next_primary59',closed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),run=runpin,native_run_sha256=run['run_sha256'],named_payload_sha256=run['named_source_payload_sha256'],native_receipt=receipt,final_reviews=reviews,actual_foreground_readback_pids=[pre['actual_foreground_pid'],final['actual_foreground_pid']],actual_foreground_readback_exit_codes=[0,0],actual_foreground_finalizer_pid=os.getpid(),scope='Original source review lease and all canonical/audit/production files remain unchanged. No VERIFIED, PURIFIED, Gamma or full-paper completion.'))
