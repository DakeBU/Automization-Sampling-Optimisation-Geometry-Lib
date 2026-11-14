#!/opt/anaconda3/bin/python
import hashlib,json,pathlib,subprocess
ROOT=pathlib.Path('/Users/zhouhuanjian/ASTIS-GC');BASE=pathlib.Path(__file__).resolve().parent
C='7359f552e3b9bdf27c2253703d879783f331c4e9';M='72e5d1405284f729f4eb600c5ae5dd556365b7e2'
E='research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-cosine-gram-semantic-evidence/'
paths=[E+'mechanical-independent-source-attachment.json',E+'review-metadata-carrier-scope.json',
       'research-wiki/semantic-roundtrip/audits/huanjian-fixed-spectrum-cosine-gram.json']
(BASE/'inputs').mkdir(exist_ok=True)
records=[]
for command in [['git','rev-parse',C+'^'],['git','diff','--stat',M,C],['git','diff','--name-status',M,C]]:
    proc=subprocess.run(command,cwd=ROOT,capture_output=True);assert proc.returncode==0
    name='carrier-'+str(len(records))+'.stdout';(BASE/'inputs'/name).write_bytes(proc.stdout)
    records.append({'argv':command,'returncode':proc.returncode,'stdout_snapshot':'inputs/'+name,
                    'stdout_sha256':hashlib.sha256(proc.stdout).hexdigest(),'stderr':proc.stderr.decode()})
    print('GIT',json.dumps(records[-1]));print(proc.stdout.decode())
for rel in paths:
    proc=subprocess.run(['git','show',C+':'+rel],cwd=ROOT,capture_output=True);assert proc.returncode==0
    name=pathlib.Path(rel).name;(BASE/'inputs'/name).write_bytes(proc.stdout)
    records.append({'source':rel,'commit':C,'snapshot':'inputs/'+name,'bytes':len(proc.stdout),
                    'sha256':hashlib.sha256(proc.stdout).hexdigest(),'returncode':proc.returncode,'stderr':proc.stderr.decode()})
    print('INPUT',json.dumps(records[-1]))
    if name!='huanjian-fixed-spectrum-cosine-gram.json':print(proc.stdout.decode())
W='.astis/huanjian-gc-fixed-spectrum-cosine-gram-20261110/accepted-review-metadata-commit.json'
data=(ROOT/W).read_bytes();(BASE/'inputs/accepted-review-metadata-commit.json').write_bytes(data)
records.append({'source':W,'snapshot':'inputs/accepted-review-metadata-commit.json','bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
print('W',data.decode())
(BASE/'input_inventory.json').write_text(json.dumps(records,indent=2)+'\n')
