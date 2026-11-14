#!/usr/bin/env python3
from pathlib import Path
import subprocess,os,json,hashlib,datetime,sys
HERE=Path(__file__).resolve().parent
ROOT=Path('/Users/zhouhuanjian/ASTIS-GC')
HELD='02fb93c64e4222f112e57c97ced2a548235cd0f6'
BASE='6819e686116e6f18df3ef0e638c6ca24bde7dd8d'
ENV={k:os.environ[k] for k in ('HOME','PATH','LANG','LC_ALL','TMPDIR') if k in os.environ}
ENV.update({'PYTHONUNBUFFERED':'1','GIT_OPTIONAL_LOCKS':'0'})
sha=lambda b:hashlib.sha256(b).hexdigest()
def command(label,argv):
 d=HERE/'commands'/label;d.mkdir(parents=True,exist_ok=False)
 start={'argv':list(map(str,argv)),'cwd':str(ROOT),'effective_env':ENV,'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'held_metadata_HEAD':HELD,'actual_math_compiled_commit':'e654e98642350a615c473bc8190fbc1d47fe52bd','runner_sha256':sha(Path(__file__).read_bytes())}
 (d/'start.json').write_text(json.dumps(start,indent=2))
 with (d/'stdout').open('wb') as out,(d/'stderr').open('wb') as err:r=subprocess.run(start['argv'],cwd=ROOT,env=ENV,stdout=out,stderr=err)
 end={**start,'exit':r.returncode,'ended_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 for name in ('stdout','stderr'):
  b=(d/name).read_bytes();end[name]={'source':str(d/name),'bytes':len(b),'sha256':sha(b)}
 (d/'result.json').write_text(json.dumps(end,indent=2));print(label,'ACTUAL_EXIT',r.returncode,flush=True)
 return r.returncode,(d/'stdout').read_bytes()
def snapshot(label,index):
 rc,b=command(label+'-HEAD',['git','rev-parse','HEAD']);assert rc==0
 head=b.decode().strip();ib=index.read_bytes();snap={'head':head,'index_path':str(index),'index_bytes':len(ib),'index_sha256':sha(ib),'time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 (HERE/(label+'-snapshot.json')).write_text(json.dumps(snap,indent=2));return snap
rc,b=command('bootstrap-index-path',['git','rev-parse','--git-path','index']);assert rc==0
index=Path(b.decode().strip());index=index if index.is_absolute() else ROOT/index
before=snapshot('before',index);assert before['head']==HELD,(before,HELD)
gates=[('01-publication',['python3','tools/astis_publication.py','check','--base',BASE]),('02-semantic-roundtrip',['python3','tools/astis_semantic_roundtrip.py','check']),('03-contributor-contract',['python3','tools/astis_contributor_contract.py','check','--base',BASE]),('04-frontier-cells',['python3','tools/astis_frontier_cells.py','check'])]
results=[];failure=None
for label,argv in gates:
 rc,_=command(label,argv)
 current=snapshot('after-'+label,index)
 stable=current['head']==before['head'] and current['index_sha256']==before['index_sha256'] and current['index_bytes']==before['index_bytes']
 results.append({'label':label,'argv':argv,'exit':rc,'HEAD_index_stable':stable})
 if rc!=0 or not stable:
  failure=label;break
after=snapshot('final',index)
result={'held_metadata_HEAD':HELD,'base':BASE,'actual_math_compiled_commit':'e654e98642350a615c473bc8190fbc1d47fe52bd','reader_author_commit':'1d0dedf3aac3c2ff72ee96566461e29e38a2eeae','before':before,'after':after,'gates':results,'failure':failure,'not_run_after_failure':[x[0] for x in gates[len(results):]],'all_four_actual_zero':len(results)==4 and all(x['exit']==0 and x['HEAD_index_stable'] for x in results),'normalV':'not run','other_build_browser_or_gates':'not run','no_status_transition':'no writes to C/ledger/audits/index/shared tracked files by this runner'}
(HERE/'gate-summary.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2),flush=True)
sys.exit(0 if result['all_four_actual_zero'] else 1)
