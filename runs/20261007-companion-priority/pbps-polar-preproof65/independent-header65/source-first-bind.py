import os,json,hashlib,datetime
from pathlib import Path
O=Path('E:/Samplinglib/runs/20261007-companion-priority/pbps-polar-preproof65/independent-header65');S=O.parent/'independent-primary65'
def sha(b):return hashlib.sha256(b).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(n,v):(O/n).write_bytes((json.dumps(v,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode())
write('lease.open.json',{'schema':'header65-owned-lease-v1','status':'OPEN','owner':'/root/independent_source64','owned_root':O.as_posix(),'opened_utc':now(),'create_pid':os.getpid(),'scope':'new independent-header65 only','future_candidate_seen_at_open':False})
start=now();pins={'source-proof-graph.json':'d2df300e034f799bc30dba724e4595682310f76c567e83316603a3a372e7f5f8','source-coverage-inventory.json':'605a1e7e3a4d583198d147a5207316cb62febb66ca0b9651e6372595728ffc45','residual-next-header.json':'89c0e89b915577ae94b52c781356fdb130533438c4bf4d53688d2ee70751986f','lease.final.json':'484c7e4eb3ce900d957de8a35590399d2593158344f7d5b2565901e53232abbf','owned-manifest.json':'af1e768364b0e57d1b3b0e8e2b4e49dfa853e4b286dbdb938e0b9b67b14e66f3'}
refs=[]
for n,h in pins.items():
 b=(S/n).read_bytes();assert sha(b)==h;(O/('source-first.'+n)).write_bytes(b);refs.append({'path':(S/n).as_posix(),'snapshot':'source-first.'+n,'raw_sha256':sha(b),'raw_bytes':len(b),'lf_sha256':sha(b.replace(b'\r\n',b'\n').replace(b'\r',b'\n'))})
for n in ['negative-boundaries.json','source-inputs.json']:
 b=(S/n).read_bytes();manifest=json.loads((S/'owned-manifest.json').read_text(encoding='utf-8'));entry=next(x for x in manifest['all_preclosure_owned_files'] if x['filename']==n);assert sha(b)==entry['raw_sha256'];(O/('source-first.'+n)).write_bytes(b);refs.append({'path':(S/n).as_posix(),'snapshot':'source-first.'+n,'raw_sha256':sha(b),'raw_bytes':len(b),'lf_sha256':entry['lf_sha256']})
c=json.loads((S/'source-coverage-inventory.json').read_text(encoding='utf-8'));assert c['math_count']==len(c['math_items'])==280 and c['missing_alttext_count']==c['annotation_mismatch_count']==0
P=Path('E:/Samplinglib/runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html');assert sha(P.read_bytes())=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
write('source-first-seal.json',{'schema':'header65-source-first-seal-v1','source_read_start_utc':start,'source_read_end_utc':now(),'candidate_read_before_this_seal':False,'source_raw_sha256':'d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760','closed_PRIMARY65_status':'CLOSED_LAST','source_snapshot_bindings':refs,'math_inventory_count':280,'missing_alttext':0,'annotation_mismatch':0,'source_topology_independent_of_future65':True,'source_summary':'B16: actual B0:HP0->Hperp=ker P; SAME Gamma0 and centered inverse J; V=B0 J, B0=V Gamma0, V*V=I; first corrector B0*=Gamma0 V*, contraction and range-complement annihilation; no onto or new H1/floor/small-step premise.','scope':'Candidate header acceptance only; no proof search or SAU/Goal/canonical writes.'})
print(json.dumps({'source_first_seal_raw_sha256':sha((O/'source-first-seal.json').read_bytes()),'source_first_end_utc':now(),'bound_source_files':len(refs),'math_items':280,'candidate_seen':False}))
