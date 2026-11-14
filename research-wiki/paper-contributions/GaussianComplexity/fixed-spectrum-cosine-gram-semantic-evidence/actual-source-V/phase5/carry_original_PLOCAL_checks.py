#!/opt/anaconda3/bin/python
import gzip,hashlib,json,pathlib
ROOT=pathlib.Path('/Users/zhouhuanjian/ASTIS-GC');BASE=pathlib.Path(__file__).resolve().parent
capsule=json.loads((BASE/'original-proof-capsule.stdout').read_text().split('\n',1)[1]) if False else json.loads((ROOT/'research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-cosine-gram-semantic-evidence/local-proof-capsule.json').read_text())
out=BASE/'original-PLOCAL-checks';out.mkdir(exist_ok=True)
records=[]
for row in capsule['actual_checks']:
    rp=ROOT/row['receipt'];raw=rp.read_bytes();receipt=json.loads(raw)
    assert hashlib.sha256(raw).hexdigest()==row['receipt_sha256']
    lp=pathlib.Path(receipt['log']);size=lp.stat().st_size
    # Exact authorized own-check paths only; no ignored-directory inventory or
    # foreign/private kernel dump discovery. Preserve bytes without printing.
    log=lp.read_bytes();h=hashlib.sha256(log).hexdigest()
    assert h==row['actual_log_sha256']==receipt['log_sha256']
    (out/rp.name).write_bytes(raw)
    packed=gzip.compress(log,mtime=0);dest=out/(lp.name+'.gz');dest.write_bytes(packed)
    assert gzip.decompress(packed)==log
    records.append({'original_receipt':row['receipt'],'receipt_snapshot':str((out/rp.name).relative_to(BASE)),
                    'receipt_raw_sha256':hashlib.sha256(raw).hexdigest(),
                    'original_log':str(lp.relative_to(ROOT)),'log_original_bytes':len(log),'log_original_sha256':h,
                    'lossless_gzip_snapshot':str(dest.relative_to(BASE)),'gzip_bytes':len(packed),
                    'gzip_sha256':hashlib.sha256(packed).hexdigest(),'actual_head':receipt['head_before'],
                    'exit_code':receipt['exit_code'],'scope':'Original PLOCAL execution evidence, not the later immutable fresh native run.'})
(BASE/'original-PLOCAL-checks-manifest.json').write_text(json.dumps(records,indent=2)+'\n')
print(json.dumps(records,indent=2))
