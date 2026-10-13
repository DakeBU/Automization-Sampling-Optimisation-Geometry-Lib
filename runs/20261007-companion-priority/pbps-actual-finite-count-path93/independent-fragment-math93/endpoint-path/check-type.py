from pathlib import Path
import hashlib,json,subprocess,datetime,time,re
R=Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-actual-finite-count-path93';O=B/'independent-fragment-math93/endpoint-path'
def raw(p):
 b=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'raw_sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def save(name,x):
 with (O/name).open('x',encoding='utf-8') as f:json.dump(x,f,indent=2)
specs=[('ActualEndpointNullity93','e6d786ac2f0888339f132ec0a8b9c36d0c12ecdc154c84207be336adaba88a06','EndpointInterfaces93','actual_fixed_horizon_endpoint_nullity','actual-endpoint-nullity2-explicit-api'),('ActualPathIdentification93','6d1f590625f7912bfa3af730400db84d8f3c365aec33c127e0a39a1ab5824b04','PathInterfaces93','actual_history_path_identification','actual-path-identification2-scalar-api')]
inputs=[raw(R/'lake-manifest.json'),raw(R/'runs/20261007-companion-priority/pbps-finite-count-path-preread93/Header93.lean')]
for name,h,ns,theorem,lane in specs:
 p=B/(name+'.lean');assert raw(p)['raw_sha256']==h;inputs.append(raw(p));(O/(name+'.exactraw.lean')).write_bytes(p.read_bytes())
 for f in ['receipt.json','stdout.log','stderr.log']:inputs.append(raw(B/'focused93'/lane/f))
 j=json.loads((B/'focused93'/lane/'receipt.json').read_text());assert j['exit_code']==0 and j['source_raw_sha256']==h
 text=p.read_text(encoding='utf-8-sig');assert not re.search(r'\b(sorry|admit|axiom)\b|Prop\s*:=\s*True|:=\s*trivial',text)
 suffix='\nnamespace '+ns+'\nset_option pp.explicit true in\nset_option pp.fullNames true in\nset_option pp.deepTerms true in\n#check '+theorem+'\nend '+ns+'\n'
 fresh=O/(name+'.FreshType.lean');fresh.write_text(text+suffix,encoding='utf-8')
 cmd=[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env','lean',str(fresh.relative_to(R))];t=time.monotonic();start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with (O/(name+'.type.stdout.log')).open('xb') as stdout,(O/(name+'.type.stderr.log')).open('xb') as stderr:proc=subprocess.run(cmd,cwd=R,stdout=stdout,stderr=stderr)
 receipt={'argv':cmd,'started_utc':start,'elapsed_seconds':time.monotonic()-t,'exit_code':proc.returncode,'terminal_closed':True,'original':raw(p),'fresh_input':raw(fresh),'source_unchanged':raw(p)['raw_sha256']==h}
 save(name+'.type.receipt.native.json',receipt);print(json.dumps(receipt),flush=True)
 assert proc.returncode==0
save('inputs.native.json',{'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),'inputs':inputs})