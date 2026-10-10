import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,hashlib,os,datetime
O=pathlib.Path(__file__).resolve().parent;R=O.parent;ROOT=pathlib.Path('E:/Samplinglib');H=lambda b:hashlib.sha256(b).hexdigest()
assert (O/'stageA-freeze71.terminal-receipt.json').exists()
assert json.loads((O/'stageA-freeze71.terminal-receipt.json').read_bytes())['exit_code']==0
inputs=[]
for p,n in [(R/'header71.named-literal.proposed.lean','candidate71.header.exactraw.lean'),(R/'header71.proposal.json','candidate71.proposal.exactraw.json'),(ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualProjectedRotation.lean','parent70.compiled-module.exactraw.lean')]:
 b=p.read_bytes();l=b.replace(b'\r\n',b'\n');assert not (O/n).exists();(O/n).write_bytes(b);(O/(n+'.LF')).write_bytes(l)
 inputs.append({'original_path':str(p),'snapshot':n,'RAW_bytes':len(b),'RAW_sha256':H(b),'LF_snapshot':n+'.LF','LF_bytes':len(l),'LF_sha256':H(l),'LF_recipe':'replace ONLY CRLF byte pairs with LF','original_mtime_ns':p.stat().st_mtime_ns})
assert inputs[2]['RAW_sha256']=='03a0721ae952f744d0bfdf568039b77f7035bec0a50642f8bc8ebc895273b998'
x={'schema':'prospective-header71-stageB-exact-candidate-inputs-v1','actual_pid':os.getpid(),'first_header_read_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'expectations_frozen_before_header_read':True,'expectation_RAW_sha256':H((O/'stageA.source-expectations71.before-header.frozen.json').read_bytes()),'inputs':inputs,'input_count':len(inputs),'no71_proof_or_compile':True}
(O/'stageB.candidate-input-manifest.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(x,ensure_ascii=False));print('CANDIDATE HEADER\n'+'\n'.join(str(i+1)+': '+s for i,s in enumerate((O/'candidate71.header.exactraw.lean').read_text(encoding='utf-8').splitlines())));print('PROPOSAL\n'+(O/'candidate71.proposal.exactraw.json').read_text(encoding='utf-8'))
