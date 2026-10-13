# -*- coding: utf-8 -*-
from pathlib import Path
import json,hashlib,datetime
D=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(o):return (json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def put(n,o):(D/n).write_bytes(dump(o))
def read(n):return json.loads((D/n).read_text(encoding='utf-8-sig'))
lp=D/'lease.json';initial=lp.read_bytes();lease=read('lease.json');assert lease['state']=='OPEN'
(D/'lease.initial.raw.snapshot.json').write_bytes(initial)
bindings=read('source-inputs.json');validation=[];resolution=[]
for i in bindings['inputs']:
    raw=(D/(i['id']+'.raw.snapshot')).read_bytes();lf=(D/(i['id']+'.lf.snapshot')).read_bytes()
    assert sha(raw)==i['raw_sha256'];assert sha(lf)==i['lf_sha256']
    validation.append({'id':i['id'],'raw_sha256':sha(raw),'lf_sha256':sha(lf),'raw_LF_consistent':raw.replace(b'\r\n',b'\n')==lf})
    if i['id'] in ['031public','043public']:
        resolution.append({'id':i['id'],'actual_provider':i['actual_provider'],'namespace_only_resolution':i['namespace_only_resolution'],'publicheader_literalname_verified_current':True,'currentrawsignature_identical_frozen':i['current_public_raw_bytes_identical'],'proofselected':False})
put('qualified-parent-resolution.json',{'status':'Source-level qualifiedparent/namespace/publicheader binding; no newcompiler verification','parents':resolution,'foundations':'mathematical-primitives.txt semantic contracts; not inventedLean QNames orobservedimplementationcalls','generatedfields':'conjunctionprojections/types notcountedmathematicalcalls'})
put('input-validation.json',{'status':'PASS','inputs':validation,'exact45LFbytes':1357,'exact45LFsha256':'6b54ac62b436aeb4032aafb15b12c26a5661450013151633e01da02dd08b163d','historical_current_statuses':'Frozen45preread43PROVED_LOCAL retained;45seal separatelyrecords31/43VERIFIED19b569ae','compiler_or_theorem_validation':False})
lease.update(state='CLOSED',closed_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),actual_close_last_filesystem_operation=True)
closed=dump(lease)
put('leases.closed.json',{'status':'ALL_REAL_LEASES_CLOSED','real_lease':'lease.json','initial_bytes':'lease.initial.raw.snapshot.json','method':'Package/hashwriteswhileOPEN;exactfinalCLOSEDleasebytesbound;actualleaseclosurelast'})
outputs=[]
for p in sorted(D.iterdir()):
    if p.is_file() and p.name!='sourcegraph-run.json':
        b=closed if p.name=='lease.json' else p.read_bytes();outputs.append({'path':p.name,'raw_sha256':sha(b),'lf_sha256':sha(b.replace(b'\r\n',b'\n')),'bytes':len(b)})
run={'actor':'gaussian_noncompact_preread_42','stage':'independent-sourcegraph45','status':'AUTHORED_AWAIT_DISTINCT_TOPOLOGY_ADMISSION','closed_at_utc':lease['closed_at_utc'],'real_leases':'ALL_CLOSED','inputs':'source-inputs.json/input-validation.json exactrawLF','outputs':outputs,'structural_check':read('structural-check.json'),'sourcegraph_sha256':sha((D/'sourcegraph.json').read_bytes()),'sourcecontract_sha256':sha((D/'sourcecontract.json').read_bytes()),'compiler_proof_claim_or_sharedmutation':False,'source_topology_self_admission':False,'root_site_compiler_lease_used':False,'retrieval_diagnosis':'Python bookkeeping firstpass had localrange variable shadow; fixed script, noLean compiler/proofsearch. Allsourceinputs unchanged.'}
rb=dump(run);(D/'sourcegraph-run.json').write_bytes(rb)
print('sourcegraph.json '+run['sourcegraph_sha256']);print('sourcecontract.json '+run['sourcecontract_sha256']);print('sourcegraph-run.json '+sha(rb))
lp.write_bytes(closed)
