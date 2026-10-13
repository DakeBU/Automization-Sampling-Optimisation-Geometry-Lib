from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys
r=Path(__file__).parent;root=Path.cwd();pre=r.parent/'pbps-actual-position-l2-preread109'
seal=json.loads((pre/'root.statement-seal109.json').read_bytes());assert seal['status'].startswith('SEALED_BEFORE_PROOF')
header=(pre/'Header109.lean').read_text(encoding='utf8')
assert hashlib.sha256((pre/'Header109.lean').read_bytes()).hexdigest()==seal['header']['raw_sha256']
ns='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPositionL2Averaging'
s=header.split('#check candidate')[0].replace('PBPSActualPositionL2Candidate109',ns).replace('def candidate','private def actual_position_l2_statement').replace('/- Prospective type-only statement. No proof, seal or claim yet. -/','/- Actual Gaussian momentum averaging on the same PBPS process and phase operator. -/')
binders=header.split('def candidate',1)[1].split(' : Prop := by',1)[0]
s+='set_option maxHeartbeats 2200000\nset_option maxRecDepth 12000\n'
s+='theorem actual_position_l2_averaging'+binders+' : actual_position_l2_statement hα hαβ hV hH hη hβη := by\n'+(r/'proof109.txt').read_text(encoding='utf8')
s+='\n#print axioms actual_position_l2_averaging\nend\nend '+ns+'\n'
p=root/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPositionL2Averaging.lean';p.write_text(s,encoding='utf8',newline='\n')
out=r/'focused109'/sys.argv[1];out.mkdir(parents=True,exist_ok=False);(out/'module.exactraw.lean').write_bytes(p.read_bytes())
env=os.environ.copy();env['PATH']=str(root/'.astis/toolchain/lean-4.33.0-windows/bin')+os.pathsep+env['PATH'];env.pop('ELAN_TOOLCHAIN',None);env['PYTHONUTF8']='1';env['LEAN_NUM_THREADS']='2'
cmd=[str(root/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env','lean',str(p)]
q=subprocess.run(cmd,capture_output=True,env=env);(out/'stdout.log').write_bytes(q.stdout);(out/'stderr.log').write_bytes(q.stderr)
d=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),argv=cmd,exit_code=q.returncode,terminal_closed=True,module_raw_sha256=hashlib.sha256(p.read_bytes()).hexdigest())
(out/'receipt.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf8',newline='\n');print((q.stdout+q.stderr).decode(errors='replace')[-14000:]);print(json.dumps(d));sys.exit(q.returncode)
