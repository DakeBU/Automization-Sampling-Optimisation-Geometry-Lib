from pathlib import Path
import hashlib,json,subprocess,datetime
run=Path('runs/20261007-companion-priority/gaussian-sqrt-density-domain')
read=lambda p:json.loads(Path(p).read_text(encoding='utf-8'))
shared='fbafcea29c4e3d4a90e6401d20edc989c3df9d7a'
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==shared
repo=read(run/'reviewer.repository.ProofSeal.json');expo=read(run/'ExpositionSeal.json')
assert repo['status']=='accepted-scoped' and repo['checked_repository_commit']==shared
assert expo['verdict']=='accepted-scoped' and not expo['blocking']
assert read(run/'reviewer.repository.lease.json')['compiler_lease']=='CLOSED'
assert read(run/'reviewer.exposition.lease.json')['write_lease']=='CLOSED'
def bind(p):
    b=p.read_bytes();return dict(path=p.as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),lf_sha256=hashlib.sha256(b.replace(b'\r\n',b'\n')).hexdigest())
out=run/'seals-closeout.json';assert not out.exists()
out.write_text(json.dumps(dict(schema_version=1,status='independent-repository-and-static-exposition-seals-accepted-scoped',proof_commit='1de412105042ebcfe147d50a3d1022fb0514faad',shared_commit=shared,seals=[bind(run/p) for p in ['reviewer.repository.ProofSeal.json','ExpositionSeal.json']],leases=[bind(run/p) for p in ['reviewer.repository.lease.json','reviewer.exposition.lease.json']],truth_boundary='Actual Gaussian relative-density/square-root/entropy/gradient L2 domains and exact Dirichlet=Fisher/4; same actual true standardized RGO consumer, L0/E0/allpositiveeta. No GaussianLSI/T2, canonical KL/weak representative/Sobolev, FIRST4.6 W2, bias/fullLemma/algorithms/main/work/composition.',next_packet='Exact independent StatementSeal admitted prospective true canonical finite entropy and unique stationary proximal point; root has not yet claimed or implemented it.',reader_boundary='Scoped static only. Historical generated-site stamp precommit1de+dirty retained honestly; current fbaf sources and formal graph contents independently checked. RenderedQA/functionalCopyDownload/merge/postmergePURIFIED/live remain OPEN.',remote_ci='Forthcoming published closeout head requires own exact-head terminal remotechecks. Prior31 0e3 allfour PASS supplies no current32 credit.',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip()
paths=[p.as_posix() for p in run.rglob('*') if p.is_file()]
subprocess.run(['git','-c','core.autocrlf=false','add','-f','--pathspec-from-file=-','--pathspec-file-nul'],input=('\0'.join(paths)+'\0').encode('utf-8'),check=True)
subprocess.run(['git','commit','-q','-m','Record independent Gaussian density-domain repository and exposition seals'],check=True)
print(subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip())
