from pathlib import Path
import hashlib,json,gzip,subprocess
r=Path(__file__).resolve().parent.relative_to(Path.cwd().resolve());out=r/'integration94';sha=lambda b:hashlib.sha256(b).hexdigest()
records=[]
for label in ['production1','production2-lf']:
    p=r/'checks94'/label/'stdout.log';raw=p.read_bytes();arch=Path(str(p)+'.gz');assert gzip.decompress(arch.read_bytes())==raw
    public=subprocess.check_output(['git','show','HEAD:'+p.as_posix()]);assert b'\n'.join(x.rstrip(b' \t') for x in raw.replace(b'\r\n',b'\n').split(b'\n')).rstrip(b'\n')+b'\n'==public
    p.write_bytes(public);records.append(dict(path=p.as_posix(),raw_sha256=sha(raw),archive=arch.as_posix(),public_sha256=sha(public),change='Existing committed public text; native RAW preserved by exact lossless science archive'))
p=Path('runs/substantive_advances.jsonl');raw=p.read_bytes();z=out/'pre-normalization-ledger94.raw.gz';assert not z.exists();z.write_bytes(gzip.compress(raw,mtime=0));assert gzip.decompress(z.read_bytes())==raw
public=b'\n'.join(x.rstrip(b' \t') for x in raw.replace(b'\r\n',b'\n').split(b'\n')).rstrip(b'\n')+b'\n'
assert [json.loads(x) for x in raw.splitlines() if x.strip()]==[json.loads(x) for x in public.splitlines() if x.strip()]
p.write_bytes(public);records.append(dict(path=p.as_posix(),raw_sha256=sha(raw),archive=z.as_posix(),public_sha256=sha(public),change='Line endings and terminal whitespace only; every JSON event unchanged'))
(out/'text-normalization94.json').write_text(json.dumps(records,indent=2)+'\n',encoding='utf8',newline='\n')
print('Preserved RAW evidence and normalized only three own files')
