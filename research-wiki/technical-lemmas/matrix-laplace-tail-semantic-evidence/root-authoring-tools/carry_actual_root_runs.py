from pathlib import Path
import json,hashlib,gzip
r=Path.cwd();base=r/'.astis/huanjian-resume-20261103'
e=r/'research-wiki/technical-lemmas/matrix-laplace-tail-semantic-evidence/root-actual-runs'
e.mkdir(parents=True,exist_ok=True); rows=[]
for p in sorted(base.glob('*-matrix-laplace-*.receipt.json')):
    v=json.loads(p.read_text());log=Path(v['log']);b=log.read_bytes()
    assert hashlib.sha256(b).hexdigest()==v['log_sha256']
    receipt=e/p.name
    if receipt.exists():assert receipt.read_bytes()==p.read_bytes()
    else:receipt.write_bytes(p.read_bytes())
    gz=e/(log.name+'.gz');payload=gzip.compress(b,mtime=0)
    if gz.exists():assert gzip.decompress(gz.read_bytes())==b
    else:gz.write_bytes(payload)
    rows.append({'receipt':str(receipt.relative_to(r)),'receipt_sha256':hashlib.sha256(receipt.read_bytes()).hexdigest(),
      'original_combined_stdout_stderr_log':str(log.relative_to(r)),
      'lossless_log_gzip':str(gz.relative_to(r)),'decoded_log_sha256':v['log_sha256'],
      'decoded_log_bytes':len(b),'exit_code':v['exit_code'],'command':v['command'],
      'actual_head_before':v['head_before'],'actual_head_after':v['head_after']})
out=e/'actual-run-custody.current.json'
out.write_text(json.dumps({'scope':'Actual existing ROOT recorder receipts and their original combined stdout/stderr streams only. Historical failures and their real exit codes retained. Compression is lossless, not reconstructed output or a new check. New source/metadata/public export identities are not retroactively claimed built.',
 'raw_originals_preserved_local':True,'records':rows},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'actual_receipts':len(rows),'failed_processes_preserved':sum(p['exit_code']!=0 for p in rows),'all_original_log_bytes_match_receipt_sha256':True}))
