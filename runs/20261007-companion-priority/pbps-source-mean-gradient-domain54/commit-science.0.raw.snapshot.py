from pathlib import Path
import subprocess,json,hashlib,gzip,re
run=Path('runs/20261007-companion-priority/pbps-source-mean-gradient-domain54');base=run.parent
j=lambda p:json.loads(Path(p).read_text(encoding='utf-8'));sha=lambda b:hashlib.sha256(b).hexdigest()
def closed(p):
 d=j(p)
 for k in ['status','state','read','write','read_lease','write_lease','Python','Python_lease','python','compiler','compiler_lease']:
  if k in d:assert d[k] in ['CLOSED','NOT_STARTED_CLOSED'],(p,k,d[k])
assert (run/'proved-local.json').exists()
for n in ['source.review.lease.json','reviewer.source.lease.json','whole-proof-review54/lease.json','whole-proof-review54/compiler.lease.json','anonymous-decoder/lease.json']:closed(run/n)
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==j(run/'math-freeze.json')['checked_base_commit']
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip()
plan=j(run/'publication-plan.json');claim=j(run/'claim.json')
paths=list(claim['proposal']['proposed_files'])+['research-wiki/frontier-cells/'+x+'.json' for x in plan['active_cells']]+['research-wiki/semantic-roundtrip/audits/'+x+'.json' for x in plan['audit_ids']]+['website/content/'+folder+'/'+x+'.json' for folder in ['publications','declaration_lessons'] for x in plan['slugs']]+['runs/substantive_advances.jsonl']
folders=['pbps-source-mean-gradient-domain54','pbps-source-mean-gradient-domain-preproof54','pbps-source-mean-gradient-domain-preproof-review54','pbps-source-mean-gradient-domain-sourcegraph54','pbps-source-mean-gradient-domain-topology-review54','pbps-source-mean-gradient-domain-topology-overlay54','phase-pbps-primary-preread54','pbps-source-mean-gradient-domain-preread54']
for n in folders:paths += [p.as_posix() for p in (base/n).rglob('*') if p.is_file()]
remote=base/'pbps-literal-reflected-mean53/remote53'
paths += [p.as_posix() for p in remote.iterdir() if p.is_file()]
paths=list(dict.fromkeys(paths));assert all(Path(p).is_file() and Path(p).stat().st_size<100*1024*1024 for p in paths)
def stage(ps):subprocess.run(['git','-c','core.autocrlf=false','add','-f','--pathspec-from-file=-','--pathspec-file-nul'],input=('\0'.join(ps)+'\0').encode(),check=True)
stage(paths)
full=subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
raw=full.stdout;findings=[]
for line in raw.decode('utf-8').splitlines():
 m=re.match(r'^(.+?):([0-9]+): (trailing whitespace|new blank line at EOF|space before tab in indent).*$',line)
 if m:findings.append(dict(path=m[1],line=int(m[2]),kind=m[3]))
assert full.returncode in [0,2] and (full.returncode==0 or findings)
excluded=list(dict.fromkeys(x['path'] for x in findings))
for p in excluded:
 assert any(p.startswith((base/n).as_posix()+'/') for n in folders),('Authored canonical whitespace error',p)
 assert p in paths and not p.endswith(('publication-plan.json','proved-local.json','claim.json')),(p,'must diagnose authored artifact')
command=['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check','--','.']+[':(exclude)'+p for p in excluded]
authored=subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);assert authored.returncode==0,authored.stdout.decode()
diag=run/'whitespace-diagnosis54';diag.mkdir(exist_ok=False)
(diag/'staged.raw-whitespace.negative.log.gz').write_bytes(gzip.compress(raw,mtime=0));(diag/'staged.authored-whitespace.log').write_bytes(authored.stdout)
d=dict(full_staged_exit=full.returncode,findings=len(findings),full_negative_raw_sha256=sha(raw),gzip=dict(path=(diag/'staged.raw-whitespace.negative.log.gz').as_posix(),raw_sha256=sha((diag/'staged.raw-whitespace.negative.log.gz').read_bytes())),authored_check_exit=authored.returncode,authored_check_command=command,immutable_raw_artifacts=[dict(path=p,raw_sha256=sha(Path(p).read_bytes()),lf_sha256=sha(Path(p).read_bytes().replace(b'\r\n',b'\n')),findings=[x for x in findings if x['path']==p]) for p in excluded],scope='Exact emitted evidence/source/API/compiler/closed reviewer raw-byte artifacts retained unchanged; only actual diagnostic paths excluded. No blanket runs exclusion. Production/Test/canonical metadata authored check passes; no full staged whitespace PASS asserted.')
(diag/'diagnosis.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
paths += [p.as_posix() for p in diag.iterdir() if p.is_file()];stage(paths);subprocess.run(command,check=True)
actual=subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines();assert set(actual)==set(paths)
subprocess.run(['git','commit','-q','-m','Put the actual PBPS compact source mean in the genuine closed-gradient domain'],check=True)
print('54 science commit',subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'explicit files',len(paths),'immutable whitespace findings',len(findings),'paths',len(excluded))
