"""Semantic three-way reconciliation retaining both contributors' additions."""
from pathlib import Path
import subprocess,json,hashlib,gzip
r=Path(__file__).resolve().parent.relative_to(Path.cwd().resolve());out=r/'integration94/main-reconciliation';out.mkdir(exist_ok=False)
git=lambda *a:subprocess.check_output(['git',*a]);sha=lambda b:hashlib.sha256(b).hexdigest()
paths=git('diff','--name-only','--diff-filter=U').decode().splitlines()
expected={'AutoSamplingTheory/TechnicalLemmas/Registry.lean','Tests/Basic.lean','runs/substantive_advances.jsonl','tools/tests/test_astis_publication.py','website/scripts/declaration_lessons.py'}
assert set(paths)==expected
records=[]
for i,name in enumerate(paths):
    versions={k:git('show',f':{stage}:{name}') for k,stage in [('base',1),('ours',2),('theirs',3)]}
    for k,b in versions.items():
        z=out/f'{i}.{k}.raw.gz';z.write_bytes(gzip.compress(b,mtime=0));assert gzip.decompress(z.read_bytes())==b
    norm={k:b.replace(b'\r\n',b'\n') for k,b in versions.items()}
    if name=='runs/substantive_advances.jsonl':
        parse=lambda b:[json.loads(x) for x in b.splitlines() if x.strip()]
        base,ours,theirs=map(parse,[norm['base'],norm['ours'],norm['theirs']])
        assert ours[:len(base)]==base and theirs[:len(base)]==base
        key=lambda x:json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False)
        merged=ours+ [x for x in theirs[len(base):] if key(x) not in {key(y) for y in ours}]
        assert all(key(x) in {key(y) for y in merged} for x in ours+theirs)
        result=('\n'.join(key(x) for x in merged)+'\n').encode('utf8');code=0;method='Append both branches events after verified common prefix; preserve each branch order and every JSON event.'
    elif name=='Tests/Basic.lean':
        assert norm['ours'].count(b'formalizedTechnicalLemmaCount = 543')==1
        assert norm['theirs'].count(b'formalizedTechnicalLemmaCount = 487')==1
        # Compare all other text against the normalized three-way base.
        import re
        strip=lambda b:re.sub(rb'formalizedTechnicalLemmaCount = \d+',b'formalizedTechnicalLemmaCount = COUNT',b)
        assert strip(norm['base'])==strip(norm['ours'])==strip(norm['theirs'])
        result=norm['ours'].replace(b'formalizedTechnicalLemmaCount = 543',b'formalizedTechnicalLemmaCount = 544');code=0;method='Retain543 existing entries plus independently merged affine gradient entry; exact count tested by native_decide.'
    else:
        for k,b in norm.items():(out/f'{i}.{k}.merge-input').write_bytes(b)
        q=subprocess.run(['git','merge-file','-p',str(out/f'{i}.ours.merge-input'),str(out/f'{i}.base.merge-input'),str(out/f'{i}.theirs.merge-input')],capture_output=True)
        result=q.stdout;code=q.returncode;method='Normal three-way merge after CRLF/LF normalization; both branches retained.'
        (out/f'{i}.merge.stderr.log').write_bytes(q.stderr)
    assert code==0,(name,code,result[:2000])
    assert b'<<<<<<<' not in result and b'>>>>>>>' not in result
    Path(name).write_bytes(result)
    records.append(dict(path=name,inputs={k:sha(v) for k,v in versions.items()},result_raw_sha256=sha(result),method=method))
(out/'resolution.json').write_text(json.dumps(dict(ours=git('rev-parse','HEAD').decode().strip(),theirs=git('rev-parse','MERGE_HEAD').decode().strip(),records=records,production94_changed=False,Goal_complete=False),indent=2)+'\n',encoding='utf8',newline='\n')
print('Resolved five files with all branch additions retained; not yet committed')
