"""One actual intake after exact source admission; exclusive marker, no replay."""
from pathlib import Path
import hashlib,json,os,stat,subprocess,sys,tarfile
sys.dont_write_bytecode=True
sys.path.insert(0,'tools')
import astis_advance as advance
import astis_frontier_cells as frontiers
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
C=Path('research-wiki/frontier-cells/ASTIS-SHARED-MATRIX-BERNSTEIN-EXPONENTIAL-QUADRATIC.json')
SP=Path('research-wiki/technical-lemmas/matrix-bernstein-exponential-statement-seal.json')
E=Path('research-wiki/technical-lemmas/matrix-bernstein-exponential-semantic-evidence')
L=Path('runs/substantive_advances.jsonl')
D=Path('runs/substantive_discoveries.jsonl')
ADV='ASTIS-SA-20261114-MatrixBernsteinExponentialQuadratic'
OWNER='huanjian_20261114_matrix_bernstein_exponential'
SG=Path('.astis/semantic-neutral-20261113/bernstein_mgf_sg_c410')
TC=Path('.astis/semantic-neutral-20261114/bernstein_mgf_tc_29d8')
IF=Path('.astis/semantic-neutral-20261114/bernstein_mgf_interface_7c92')
sha=lambda b:hashlib.sha256(b).hexdigest()
dump=lambda o:(json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode()
git=lambda *a:subprocess.check_output(['git',*a])
def create(p,b):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('xb') as f:f.write(b)
def fingerprint(p):
 st=p.lstat()
 if stat.S_ISLNK(st.st_mode):return {'mode':stat.S_IMODE(st.st_mode),'kind':'symlink','target':os.readlink(p)}
 assert stat.S_ISREG(st.st_mode)
 return {'mode':stat.S_IMODE(st.st_mode),'kind':'regular','bytes':st.st_size,'sha256':sha(p.read_bytes())}
head=git('rev-parse','HEAD').decode().strip()
assert head=='19eaadc52297606595ee5095de95742d4e6394f0'
assert not git('diff','HEAD','--name-only') and not git('diff','--cached','--name-only')
assert not any(p.exists() for p in [C,SP,E,W/'normal-intake-attempted.once.json',W/'preproof-baseline.private.json'])
sealraw=(W/'statement-seal.unclaimed.v1.json').read_bytes()
assert sha(sealraw)=='c3103a9e8d08fea6c83f35201fce953af4dd93e88a1a3d7d647fc4deaaddeb7a'
seal=json.loads(sealraw)
P,T=[seal[k]['planned_file'] for k in ['producer','actual_private_consumer']]
assert not Path(P).exists() and not Path(T).exists()
dp=TC/'graph-challenge-v2-focused/decision.v2.json'
assert sha(dp.read_bytes())=='b5a5e81d7f110c40a1fdb6ee0ba6c03003a9bf18d04dea907e3105fa5de6ede7'
decision=json.loads(dp.read_bytes())
assert decision['verdict']=='ACCEPTED_SCOPED_SOURCE_TOPOLOGY_AND_INTERNAL_PORT_RECORDS_FOR_EXACT_P_T'
assert not decision['blocking_findings']
critical={**decision['exact_input_hashes'],str(dp):sha(dp.read_bytes()),
 str(TC/'graph-challenge-v2-focused/FINAL-MANIFEST.v2.json'):'ce7577ca64a21c5e1960b1db29b304cf2d5ae05609faafe429e560703817ce27',
 str(IF/'audit-report.json'):'ebe0eb35b03d715790a1b6c12dff231a2cccb6693a9b00f97aa5ea41d898c711'}
for p,h in critical.items():assert sha(Path(p).read_bytes())==h,p
for x in json.loads((SG/'v2-selected-target/MANIFEST.v2.json').read_bytes())['artifacts']:
 b=(SG/'v2-selected-target'/x['path']).read_bytes()
 assert len(b)==x['bytes'] and sha(b)==x['sha256']
assert decision['P_signature_sha256']==seal['producer']['signature_sha256']
assert decision['T_signature_sha256']==seal['actual_private_consumer']['signature_sha256']
for entry in [seal['formation'],seal['definition_typing']]:
 r=json.loads(Path(entry['receipt']).read_bytes())
 assert r['exit_code']==0 and sha(Path(r['log']).read_bytes())==r['log_sha256']==entry['log_sha256']
envraw=(W/'actual-environment-before-intake.json').read_bytes()
assert json.loads(envraw)['HEAD']==head
cell=json.loads((W/'candidate-frontier-cell.unclaimed.v1.json').read_bytes())
kwargs=json.loads((W/'candidate-proposal-kwargs.unclaimed.v1.json').read_bytes())
proposal=advance.AdvanceProposal(**kwargs);proposal.validate()
assert proposal.advance_id==ADV and proposal.created_by==OWNER and proposal.frontier_cell==C.stem
assert cell['statement_seal']['sha256']==sha(sealraw)
assert cell['reuse_plan']['planned_existing_P_parents']==[]
assert cell['consumer_scope']['compiled_consumer_credit'] is False
assert len(cell['consumers'])==2 and cell['consumer_scope']['second_source_required_route']['state'].startswith('FUTURE_')
assert not frontiers.validate_cells(frontiers.load_cells()+[{**cell,'__path__':str(C)}])
def no_private_maps(o):
 if isinstance(o,dict):
  for k,v in o.items():
   if k in {'all_foreign_states','all_existing_frontier_hashes','all_existing_tracked_fingerprints',
    'actual_control_fingerprints','full_states'}:
    assert isinstance(v,(int,bool)), 'private map/list payload refused'
   if k=='tracked_git_index':raise AssertionError('opaque whole index payload refused')
   no_private_maps(v)
 elif isinstance(o,list):
  for v in o:no_private_maps(v)
for root in [SG,TC,IF]:
 for p in root.rglob('*'):
  if p.is_file() and '__pycache__' not in p.parts:
   assert not p.is_symlink() and not any('.private.' in part for part in p.parts)
   if p.suffix=='.json':no_private_maps(json.loads(p.read_bytes()))
before=L.read_bytes();states=advance._replay_advances([json.loads(x) for x in before.splitlines()])
assert ADV not in states
assert states['ASTIS-SA-20261113-GaussianComplexitySourceGramRealization']['state']=='VERIFIED'
discover=D.read_bytes();ds=advance._replay_discoveries([json.loads(x) for x in discover.splitlines()])
index=git('ls-files','--stage','-z');cache={}
def cached(p):
 if str(p) not in cache:cache[str(p)]=fingerprint(p)
 return cache[str(p)]
tracked={}
for entry in index.split(b'\0'):
 if entry:
  _,n=entry.split(b'\t',1);p=Path(os.fsdecode(n));tracked[str(p)]=cached(p)
controls={}
for root in [Path('runs'),*[Path('.astis')/n for n in ['control','queues','runtime','harness','state','locks']]]:
 if root.is_dir() and not root.is_symlink():
  for p in root.rglob('*'):
   if p.is_file() or p.is_symlink():controls[str(p)]=cached(p)
for p in Path('.astis').iterdir():
 if p.is_file() and any(s in p.name.lower() for s in ['queue','control','goal','steer','execution']):controls[str(p)]=cached(p)
foreign_frontiers={str(p):sha(p.read_bytes()) for p in C.parent.rglob('*') if p.is_file() and not p.is_symlink()}
assert L.read_bytes()==before and D.read_bytes()==discover and git('ls-files','--stage','-z')==index
create(W/'preproof-baseline.private.json',dump({'head':head,'ledger_sha256':sha(before),'ledger_bytes':len(before),
 'all_foreign_states':states,'all_existing_frontier_hashes':foreign_frontiers,'tracked_git_index':index.decode(),
 'all_existing_tracked_fingerprints':tracked,'actual_control_fingerprints':controls,
 'scope':'PRIVATE full preservation only; never export snapshots/full maps/index.'}))
create(W/'preproof-discoveries.private.json',dump({'ledger_sha256':sha(discover),'full_states':ds,'scope':'PRIVATE only'}))
originals={}
for root in [SG,TC,IF]:
 for p in sorted(root.rglob('*')):
  if p.is_file() and '__pycache__' not in p.parts:
   assert not p.is_symlink() and not any('.private.' in part for part in p.parts)
   originals[str(p)]={'sha256':sha(p.read_bytes()),'bytes':p.stat().st_size}
for p in [Path('.astis/semantic-neutral-20261113/bernstein_raw_intake_74ab/Tro11-User-Friendly-preprint.pdf'),
 Path('.astis/huanjian-resume-20261103/2610.20492v1.html')]:
 originals[str(p)]={'sha256':sha(p.read_bytes()),'bytes':p.stat().st_size}
E.mkdir();archive=E/'independent-preproof-originals.tar.gz'
with tarfile.open(archive,'x:gz') as tf:
 for n in originals:tf.add(n,arcname=n,recursive=False)
with tarfile.open(archive,'r:gz') as tf:
 assert len(tf.getmembers())==len(originals)
 for n,x in originals.items():
  b=tf.extractfile(n).read();assert len(b)==x['bytes'] and sha(b)==x['sha256']
create(E/'independent-preproof-originals.manifest.json',dump({'files':originals,'archive_sha256':sha(archive.read_bytes()),
 'scope':'Only assigned source/TC/type-interface preparation units and pinned primary inputs; no private state/index/control snapshots.',
 'private_guards_exported':False}))
admission={'exact_seal_sha256':sha(sealraw),'critical_inputs':critical,
 'distinct_topology_decision':decision['verdict'],'source_record_repair':'ImmutableSGv2+exact3edgev3supplement; priorHOLD/failures preserved.',
 'binder_policy':'P source real nonempty deterministic one-sided spectral-cap component; actual Gaussian T has sole hq plus auxiliary all s>0, no stochastic certificates or extra main theorem premises.',
 'all_internal_proof_ports_open':22,'source_only':True,'new_target_proofs':0,'source_original_files':len(originals),
 'private_visibility':'Existing private types compiled, ordinary aliases unavailable; reuse supported public parents with internal radius derivation, no fake private formal edge.',
 'source_attribution':'Tropp2011 is independently matched external background, not a supplied Gaussian paper citation.'}
create(E/'preproof-source-admission.json',dump(admission));create(SP,sealraw)
create(E/'actual-environment-before-intake.original.json',envraw)
cell['statement_seal']['status']='EXACT_TYPES_FORMED;DISTINCT_SOURCE_TOPOLOGY_AND_BINDER_PREPARATION_ACCEPTED;ALL_PROOF_PORTS_OPEN'
cell['evidence'].pop('draft_metadata_only',None)
cell['evidence']['source_admission']={'file':str(E/'preproof-source-admission.json'),'sha256':sha(dump(admission))}
cell['evidence']['actual_environment']={'file':str(E/'actual-environment-before-intake.original.json'),'sha256':sha(envraw)}
cell['reservation_only']='Source-admitted exact shared P/T target; normal intake pending; no theorem proof.'
create(C,dump(cell));assert not frontiers.validate_cells(frontiers.load_cells())
assert L.read_bytes()==before and git('ls-files','--stage','-z')==index
create(W/'normal-intake-attempted.once.json',dump({'advance_id':ADV,'before_ledger_sha256':sha(before),
 'source_admission_sha256':sha(dump(admission)),'normal_calls_requested':3,'no_replay':True}))
ev={'statement_seal_sha256':sha(sealraw),'independent_topology':admission['distinct_topology_decision'],
 'truth_boundary':cell['truth_boundary'],'formalizer_API_pristine':False}
advance.propose_advance(proposal)
advance.transition_advance(ADV,'CLAIMED',worker_id=OWNER,evidence=ev)
advance.transition_advance(ADV,'EXPLORING',worker_id=OWNER,evidence=ev)
after=L.read_bytes();assert after.startswith(before);append=after[len(before):]
events=[json.loads(x) for x in append.splitlines()]
assert len(events)==3 and all(x['advance_id']==ADV for x in events)
now=advance._replay_advances([json.loads(x) for x in after.splitlines()])
own=now.pop(ADV);assert own['state']=='EXPLORING' and own['owner_id']==OWNER and now==states
assert git('ls-files','--stage','-z')==index
for p,fp in {**tracked,**controls}.items():
 if p!=str(L):assert fingerprint(Path(p))==fp
for p,h in foreign_frontiers.items():assert sha(Path(p).read_bytes())==h
assert D.read_bytes()==discover
cell['evidence']['normal_API_calls']=3
cell['reservation_only']='Normal ledger EXPLORING; all new P/T proof obligations open.'
C.write_bytes(dump(cell));assert not frontiers.validate_cells(frontiers.load_cells())
create(E/'normal-EXPLORING-append.exact.jsonl',append)
summary={'state':'EXPLORING','actual_API_calls':3,'append_sha256':sha(append),
 'foreign_full_advances_preserved':len(states),'foreign_full_discoveries_preserved':len(ds),
 'foreign_regular_frontier_files_preserved':len(foreign_frontiers),
 'existing_tracked_fingerprints_preserved':len(tracked),'historical_control_fingerprints_preserved':len(controls),
 'control_count_qualification':'Captured historical runs and named actual control roots, not a literal queue count.',
 'source_original_files':len(originals),'private_guards_exported':False,'target_proof_calls':0,'ROOT_V_calls':0}
create(E/'normal-intake-preservation.json',dump(summary))
for p in sorted(W.iterdir()):
 if p.is_file() and '.private.' not in p.name and p.suffix in {'.py','.lean','.json','.txt','.md','.png'}:
  create(E/'intake-originals'/p.name,p.read_bytes())
R=Path('.astis/huanjian-resume-20261103')
for p in sorted(R.glob('*unclaimed-bernstein-*.receipt.json')):
 r=json.loads(p.read_bytes());log=Path(r['log'])
 assert sha(log.read_bytes())==r['log_sha256']
 for x in [p,log]:create(E/'intake-originals/actual-runs'/x.name,x.read_bytes())
paths=[C,SP,L,*[p for p in sorted(E.rglob('*')) if p.is_file()]]
spec=W/'normal-intake-paths.private.nul';create(spec,b'\0'.join(str(p).encode() for p in paths)+b'\0')
subprocess.run(['git','add','-f','--pathspec-from-file='+str(spec),'--pathspec-file-nul'],check=True)
assert set(git('diff','--cached','--name-only').decode().splitlines())==set(map(str,paths))
subprocess.run(['git','diff','--cached','--check','--',str(C),str(SP),str(L)],check=True)
subprocess.run(['git','commit','--quiet','-m','Admit one shared Bernstein exponential bound with exact Gaussian consumer'],check=True)
out={'intake_commit':git('rev-parse','HEAD').decode().strip(),**summary}
create(W/'actual-normal-intake-commit.json',dump(out));print(json.dumps(out))
