from pathlib import Path
import subprocess,json,hashlib,gzip,ast
r=Path(__file__).resolve().parent.relative_to(Path.cwd().resolve());out=r/'integration94/main-reconciliation'
git=lambda *a:subprocess.check_output(['git',*a]);sha=lambda b:hashlib.sha256(b).hexdigest()
names=['AutoSamplingTheory/TechnicalLemmas/Registry.lean','Tests/Basic.lean','runs/substantive_advances.jsonl','tools/tests/test_astis_publication.py','website/scripts/declaration_lessons.py']
rows=[]
for i,name in enumerate(names):
    vv={k:git('show',f':{stage}:{name}') for k,stage in [('base',1),('ours',2),('theirs',3)]}
    for k,b in vv.items():
        z=out/f'{i}.{k}.raw.gz'
        if z.exists():assert gzip.decompress(z.read_bytes())==b
        else:z.write_bytes(gzip.compress(b,mtime=0))
    norm={k:b.decode().replace('\r\n','\n') for k,b in vv.items()}
    if name=='tools/tests/test_astis_publication.py':
        current=norm['ours'];anchor='    def test_new_default_harness_schema_requires_publication(self):'
        addition='    def test_chapter_map_is_mathematical_and_keeps_the_affine_boundary(self):'+norm['theirs'].split('    def test_chapter_map_is_mathematical_and_keeps_the_affine_boundary(self):',1)[1].split(anchor,1)[0]
        assert addition.splitlines()[0] not in current
        current=current.replace(anchor,addition+anchor)
        old="markers = ['Lean statement ·', 'Proof roadmap',";assert current.count(old)==1
        current=current.replace(old,"markers = ['Mathematical statement', 'Lean statement ·', 'Proof roadmap',")
        ast.parse(current);Path(name).write_text(current,encoding='utf8',newline='\n')
        method='Union both new regression tests and all order markers; preserve literal Prop expansion and exact affine graph navigation checks.'
    elif name=='website/scripts/declaration_lessons.py':
        current=norm['ours'];old='The exact proof begins folded immediately after the mathematical argument.';new='The exact proof begins folded immediately after the mathematical argument; the statement is folded beside the claim above.'
        assert old in current and new in norm['theirs'];current=current.replace(old,new)
        assert 'statement_helpers' in current and 'helpers=proof_helpers' in current
        ast.parse(current);Path(name).write_text(current,encoding='utf8',newline='\n')
        method='Preserve both common source-adjacent statement placement and local literal Prop helper separation; retain upstream clarification text.'
    else:
        current=Path(name).read_text(encoding='utf8');assert '<<<<<<<' not in current
        method='Successful normalized three-way merge' if i==0 else 'Additive count544' if i==1 else 'Union every JSON event from both branches, preserving each branch order'
        if i==2:
            key=lambda x:json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False)
            now={key(json.loads(x)) for x in current.splitlines() if x.strip()}
            for b in norm.values():assert all(key(json.loads(x)) in now for x in b.splitlines() if x.strip())
    rows.append(dict(path=name,inputs={k:sha(b) for k,b in vv.items()},result_raw_sha256=sha(Path(name).read_bytes()),method=method))
saved=json.loads((r/'exact-commit-verification94/closed-RAW-manifest94.json').read_bytes())['preserved_collaborator_inputs']
for d in saved:assert sha(Path(d['path']).read_bytes())==d['raw_sha256'],d['path']
(out/'resolution.json').write_text(json.dumps(dict(ours=git('rev-parse','HEAD').decode().strip(),theirs=git('rev-parse','MERGE_HEAD').decode().strip(),records=rows,all21collaborator_RAWs_preserved=True,production94_changed=False,Goal_complete=False),indent=2)+'\n',encoding='utf8',newline='\n')
subprocess.run(['git','-c','core.autocrlf=false','add','--',*names],check=True)
assert not git('diff','--name-only','--diff-filter=U').strip()
subprocess.run(['git','diff','--cached','--check'],check=True)
subprocess.run(['git','commit','-q','--no-edit'],check=True)
print('MERGED_CURRENT_MAIN',git('rev-parse','HEAD').decode().strip())
