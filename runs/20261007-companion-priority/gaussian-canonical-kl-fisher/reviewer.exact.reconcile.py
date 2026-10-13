from pathlib import Path
import json,datetime,hashlib,sys,subprocess
r=Path(r'E:/Samplinglib');run=r/'runs/20261007-companion-priority/gaussian-canonical-kl-fisher';prefix=run.relative_to(r).as_posix();load=lambda p:json.loads((r/p).read_text(encoding='utf-8-sig'));sha=lambda b:hashlib.sha256(b).hexdigest();lf=lambda b:b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
def bind(p):
 b=(r/p).read_bytes();return {'path':p,'raw_sha256':sha(b),'lf_sha256':sha(lf(b)),'bytes':len(b)}
def delta(a,b,p=''):
 if a==b:return []
 if isinstance(a,dict) and isinstance(b,dict):
  out=[]
  for k in sorted(set(a)|set(b)):
   if k not in a or k not in b:out.append(p+'/'+k)
   else:out+=delta(a[k],b[k],p+'/'+k)
  return out
 if isinstance(a,list) and isinstance(b,list) and len(a)==len(b):
  out=[]
  for i,(aa,bb) in enumerate(zip(a,b)):out+=delta(aa,bb,p+'/'+str(i))
  return out
 return [p]
canonical='research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261007-StandardizedRGOKLFisher.json';before=load(prefix+'/source-admission-before.1.raw.snapshot.audit.json');after=load(canonical)
print('ADMINAUDIT',delta(before,after))
cell='research-wiki/frontier-cells/ASTIS-SW-SPHMC-standardized-rgo-kl-fisher.json';cbefore=load(prefix+'/source.review.raw-snapshots/043.raw');cafter=load(cell);print('ADMINCELL',delta(cbefore,cafter))
# Explicit final leases, distinct from immutable historical OPEN capture.
leases=[prefix+'/compiler.lease.json',prefix+'/whole-proof-review43/reviewer.math.lease.json',prefix+'/anonymous-decoder/lease.json',prefix+'/source.review.primary-first.lease.json',prefix+'/source.review.lease.json',prefix+'/source.review.repair1.lease.json',prefix+'/exposition-provenance-overlay/author.lease.json','runs/20261007-companion-priority/gaussian-canonical-kl-fisher-preproof43/compiler.lease.json','runs/20261007-companion-priority/gaussian-canonical-kl-fisher-preproof-review43/reviewer.primary.lease.json','runs/20261007-companion-priority/gaussian-canonical-kl-fisher-preproof-review43/reviewer.statement.lease.json','runs/20261007-companion-priority/gaussian-canonical-kl-fisher-source-graph43/leases.closed.json','runs/20261007-companion-priority/gaussian-canonical-kl-fisher-source-graph43/finalization.lease.json','runs/20261007-companion-priority/gaussian-canonical-kl-fisher-source-topology-review43/reviewer.topology.lease.json','runs/20261007-companion-priority/gaussian-canonical-kl-fisher-source-topology-review43/reviewer.repaired1.lease.json','runs/20261007-companion-priority/gaussian-canonical-kl-fisher-topology-overlay43/author.lease.json']
lout=[]
for p in leases:
 j=load(p);fields={k:v for k,v in j.items() if k in ['status','read','write','Python','compiler','read_lease','write_lease','Python_lease','compiler_lease','compiler_started','opened_utc','closed_utc','closed_at_utc','compiler_closed_utc','all_leases','review_run_sha256','lease_run_sha256','run_hash']};print(p,fields);lout.append({'binding':bind(p),'final_fields':fields})
chronology=[{'stage':'source primary first closed','utc':load(prefix+'/source.review.primary-first.lease.json')['closed_utc']},{'stage':'wholemath lease opened','utc':load(prefix+'/whole-proof-review43/reviewer.math.lease.json')['opened_utc']},{'stage':'anonymous reconstruction finalized','utc':load(prefix+'/anonymous-decoder/run.json')['execution_payload']['chronology'][2]['timestamp_utc']},{'stage':'wholemath compiler finished','utc':load(prefix+'/whole-proof-review43/reviewer.math.lease.json')['compiler_closed_utc']},{'stage':'wholemath review closed','utc':load(prefix+'/whole-proof-review43/reviewer.math.lease.json')['closed_utc']},{'stage':'original source review closed','utc':load(prefix+'/source.review.lease.json')['closed_utc']},{'stage':'overlay source review closed','utc':load(prefix+'/source.review.repair1.lease.json')['closed_utc']},{'stage':'proof committed','utc':subprocess.check_output(['git','show','-s','--format=%cI','19b569ae0fe37c97da0f98b4d1f4933ebabc7052'],cwd=r).decode().strip()},{'stage':'exact verifier opened','utc':load(prefix+'/reviewer.exact.lease.open.raw.snapshot.json')['opened_utc']}]
times=[datetime.datetime.fromisoformat(x['utc'].replace('Z','+00:00')) for x in chronology];assert times==sorted(times)
prev='runs/20261007-companion-priority/gaussian-noncompact-lsi/';ps=load(prev+'repository-seal.ProofSeal.json');pg=ps['required_repository_Lean_gate'];pci=load(prev+'repository-seal.remote-ci.01a09f2d.retry1.audit.json');assert all(x['headSha']=='01a09f2ddb39390168a280da993dee53294e0b6c' and x['conclusion']=='success' and x['status']=='completed' for x in pci['runs'])
for p in [pg['status'],pg['raw_log'],pg['root_foreground_lease']]:assert bind(p['path'])==p
out={'current_metadata_projection':{'audit_before':bind(prefix+'/source-admission-before.1.raw.snapshot.audit.json'),'audit_after':bind(canonical),'audit_changed_paths':delta(before,after),'cell_before':bind(prefix+'/source.review.raw-snapshots/043.raw'),'cell_after':bind(cell),'cell_changed_paths':delta(cbefore,cafter),'interpretation':'Only source-review admission/state and PROVED_LOCAL administration after reviewed source1 frozen input. No Lean/source/reconstruction/statement or publication context change.'},'final_stage_leases':lout,'chronology':chronology,'chronology_monotone':True,'chronology_limits':'Original source-body and repair opening captures lack their own wallclock field; primary-before-body contract and exact immutable input snapshots retained. No invented initial decoder read time; executionpayload explicitly reports initial timestamp null.','previous_aggregate42':{'credit':'PREVIOUS_AGGREGATE_ONLY','proofseal':bind(prev+'repository-seal.ProofSeal.json'),'root_gate':pg,'terminal_remote_receipt':bind(prev+'repository-seal.remote-ci.01a09f2d.retry1.audit.json'),'remote_runs':pci['runs'],'current43_gate':False,'merge_live_credit':False}}
(run/'reviewer.exact.admission-reconciliation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
