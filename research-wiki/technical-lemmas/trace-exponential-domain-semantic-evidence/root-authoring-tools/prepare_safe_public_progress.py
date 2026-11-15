"""Create a reviewable public child without private ancestry or ref mutation."""
from pathlib import Path
import subprocess,json,os,hashlib,argparse
r=Path.cwd();w=r/'.astis/huanjian-gc-trace-mgf-domain-20261115'
ap=argparse.ArgumentParser();ap.add_argument('--source',required=True)
ap.add_argument('--advance-events',type=int,required=True);ap.add_argument('--discovery-events',type=int,required=True)
ap.add_argument('--readme-file',type=Path,required=True);ap.add_argument('--increment-file',type=Path,required=True)
args=ap.parse_args()
base='f1d58f14c02d638a6925cda143d5307a73aa8f9b';sourcebase='1db9b48ff3572a159608dce9b062cc0ed841d633'
ref='refs/heads/huanjian/gaussian-progress-public-20261114'
def git(*xs,inp=None,env=None):return subprocess.check_output(['git',*xs],cwd=r,input=inp,env=env)
assert git('rev-parse','HEAD').decode().strip()==args.source
assert git('rev-parse',ref).decode().strip()==base
allowed=['AutoSamplingTheory/TechnicalLemmas/Analysis/MatrixTraceExponentialBounds.lean',
 'Tests/GaussianComplexityTraceMgfDomain.lean',
 'research-wiki/frontier-cells/ASTIS-SHARED-REAL-TRACE-EXPONENTIAL-DOMAIN.json',
 'research-wiki/technical-lemmas/trace-exponential-domain-statement-seal.json',
 'research-wiki/technical-lemmas/trace-exponential-domain-semantic-evidence/',
 'research-wiki/semantic-roundtrip/audits/huanjian-trace-exponential-domain.json',
 'website/content/declaration_lessons/huanjian-trace-exponential-domain.json',
 'website/content/publications/huanjian-trace-exponential-domain.json',
 'runs/substantive_advances.jsonl','runs/substantive_discoveries.jsonl']
raw=git('diff','--raw','--no-abbrev','--no-renames','-z',sourcebase,args.source).split(b'\0')
assert raw[-1]==b'';raw=raw[:-1];assert len(raw)%2==0;rows=[]
for i in range(0,len(raw),2):
    oldmode,newmode,oldoid,newoid,status=raw[i].decode().removeprefix(':').split();path=raw[i+1].decode()
    assert status in ['A','M'] and any(path==p or p.endswith('/') and path.startswith(p) for p in allowed),path
    old_public=git('ls-tree',base,'--',path).decode().strip()
    if oldmode=='000000':assert not old_public,path
    else:assert old_public==f'{oldmode} blob {oldoid}\t{path}',path
    rows.append({'path':path,'old_mode':oldmode,'old_oid':oldoid,'mode':newmode,'oid':newoid,'status':status})
for path,key,target,count in [
 ('runs/substantive_advances.jsonl','advance_id','ASTIS-SA-20261115-TraceExponentialDomain',args.advance_events),
 ('runs/substantive_discoveries.jsonl','discovery_id','ASTIS-DISC-20261115-ScalarSelfadjointExponentialEnvelope',args.discovery_events)]:
    old=git('show',base+':'+path);new=git('show',args.source+':'+path);assert new.startswith(old)
    delta=[json.loads(v) for v in new[len(old):].splitlines()]
    assert len(delta)==count and all(v.get(key)==target for v in delta)
notes=['docs/gaussian-public-export/README.md','docs/gaussian-public-export/provenance.json']
inc=json.loads(args.increment_file.read_text());assert inc['local_source_commit']==args.source
assert inc['previous_public_commit']==base and inc['source_delta_base']==sourcebase
assert inc['source_history_not_parent'] is True
prov=json.loads(git('show',base+':'+notes[1]));old=prov['latest_incremental_progress']
history=prov.setdefault('incremental_progress_history',[])
if old not in history:history.append(old)
inc['owned_exact_path_mode_oid_delta']=rows;prov['latest_incremental_progress']=inc
payloads={notes[0]:git('show',base+':'+notes[0])+args.readme_file.read_bytes(),
 notes[1]:(json.dumps(prov,ensure_ascii=False,indent=2,sort_keys=True)+'\n').encode()}
idx=w/'public-progress.index.private';assert not idx.exists()
env=dict(os.environ,GIT_INDEX_FILE=str(idx),GIT_OPTIONAL_LOCKS='0')
beforehead=git('rev-parse','HEAD');ip=Path(git('rev-parse','--git-path','index').decode().strip());ip=ip if ip.is_absolute() else r/ip
ih=hashlib.sha256(ip.read_bytes()).hexdigest()
git('read-tree',base,env=env)
lines=[f"{v['mode']} {v['oid']}\t{v['path']}\n" for v in rows]
for path,b in payloads.items():
    oid=git('hash-object','-w','--stdin',inp=b).decode().strip();lines.append(f'100644 {oid}\t{path}\n')
git('update-index','--index-info',inp=''.join(lines).encode(),env=env)
tree=git('write-tree',env=env).decode().strip()
public=git('commit-tree',tree,'-p',base,inp=b'Publish reviewed Gaussian all-real trace exponential domain progress\n').decode().strip()
assert git('rev-list','--parents','-n','1',public).decode().split()[1:]==[base]
changed=git('diff-tree','--no-commit-id','--name-only','-r',base,public).decode().splitlines()
assert set(changed)=={v['path'] for v in rows}|set(notes)
assert git('rev-parse','HEAD')==beforehead and hashlib.sha256(ip.read_bytes()).hexdigest()==ih
out={'status':'ACTUAL_CANDIDATE_ONLY_PENDING_INDEPENDENT_PUBLIC_OBJECT_AND_ANCESTRY_REVIEW',
 'public_commit':public,'tree':tree,'sole_safe_parent':base,'local_source_commit':args.source,
 'source_delta_base':sourcebase,'ref':ref,'owned_exact_delta':rows,'only_two_other_paths':notes,
 'Root_HEAD_and_index_unchanged':True,'no_ref_update_or_push':True}
dest=w/'prepared-safe-public-progress.v1.json';assert not dest.exists()
dest.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='owned_exact_delta'}))
