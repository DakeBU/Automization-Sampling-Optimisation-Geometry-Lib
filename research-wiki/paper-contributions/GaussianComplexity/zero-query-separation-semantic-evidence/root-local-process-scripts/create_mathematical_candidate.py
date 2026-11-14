from pathlib import Path
import sys,json,hashlib,gzip,subprocess
sys.dont_write_bytecode=True;sys.path.insert(0,'tools')
import astis_publication as pub
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
E=Path('research-wiki/paper-contributions/GaussianComplexity/zero-query-separation-semantic-evidence')
sha=lambda b:hashlib.sha256(b).hexdigest()
dump=lambda x:(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
assert not (W/'first-mathematical-candidate-commit.json').exists()
s=json.loads((W/'statement-seal-v1.json').read_bytes());p=Path(s['producer']['planned_file']);t=Path(s['actual_private_consumer']['planned_file'])
cap=json.loads((E/'local-proof-capsule.json').read_bytes());assert cap['state']=='PROVED_LOCAL_NOT_SOURCE_VERIFIED'
pub.check_advance([s['producer']['name']],reviewed=False)
for n in ['record_proved_local.py','package_local_evidence.py','package_correspondence.py','check_isolated_static_reader.py','create_mathematical_candidate.py']:
    q=E/'root-local-process-scripts'/n;assert not q.exists();q.parent.mkdir(exist_ok=True);q.write_bytes((W/n).read_bytes())
for stem in ['20261110T135042105993Z-zero-query-package-lossless-preproof-and-actual-local-evidence','20261110T135258004915Z-zero-query-normal-PROVED_LOCAL-final-pair-kernel-and-preservation']:
    rp=Path('.astis/huanjian-resume-20261103')/(stem+'.receipt.json');x=json.loads(rp.read_bytes());log=Path(x['log']);assert x['exit_code']==0 and sha(log.read_bytes())==x['log_sha256']
    for dest,b in [(E/(stem+'.receipt.json'),rp.read_bytes()),(E/(stem+'.log.gz'),gzip.compress(log.read_bytes(),mtime=0))]:assert not dest.exists();dest.write_bytes(b)
extra=[p,t,Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-zero-query-separation.json'),E.parent/'zero-query-separation-statement-seal.json',Path('website/content/declaration_lessons/huanjian-zero-query-separation.json'),Path('website/content/publications/huanjian-zero-query-separation.json'),Path('research-wiki/semantic-roundtrip/audits/huanjian-zero-query-separation.json'),Path('runs/substantive_advances.jsonl')]
paths=sorted(set(extra+[q for q in E.rglob('*') if q.is_file()]))
assert all(q.is_file() for q in paths)
before=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
assert before=='37eea55086ce04651d5b8f8a7348bc16d1b157cb'
assert not subprocess.check_output(['git','diff','--cached','--name-only'])
raws={str(q):q.read_bytes() for q in paths}
subprocess.run(['git','add','-f','--']+list(raws),check=True)
staged=set(subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines());assert staged==set(raws),(staged^set(raws))
for n,b in raws.items():assert subprocess.check_output(['git','show',':'+n])==b,n
subprocess.run(['git','diff','--cached','--check'],check=True)
subprocess.run(['git','commit','-m','Prove actual Gaussian zero-query event gap with common-law consumer'],check=True)
commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
assert subprocess.check_output(['git','rev-parse',commit+'^'],text=True).strip()==before
for n,b in raws.items():assert subprocess.check_output(['git','show',commit+':'+n])==b,n
r={'commit':commit,'parent':before,'scope':'Immutable local mathematical candidate only. Actual working-layer Lean checks predate this commit; independent exact-candidate native/source/module/reader review and sourceV are pending. Not global integration, public history or Goal completion.','source_sha256':sha(p.read_bytes()),'Test_sha256':sha(t.read_bytes()),'publication_binding_sha256':cap['binding_sha256'],'files_exact_in_Git_tree':[{'path':n,'sha256':sha(b),'bytes':len(b)} for n,b in raws.items()],'no_push_no_shared_aggregator_graph_site_or_Registry_write':True}
(W/'first-mathematical-candidate-commit.json').write_bytes(dump(r))
print(json.dumps({'commit':commit,'files_exact':len(raws),'sourceV':False,'public':False}))
