import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,hashlib,datetime,os
O=pathlib.Path(__file__).resolve().parent;R=O.parent;ROOT=pathlib.Path('E:/Samplinglib');H=lambda b:hashlib.sha256(b).hexdigest()
inputs=[]
def snapshot(p,n):
 raw=p.read_bytes();lf=raw.replace(b'\r\n',b'\n');target=O/n;assert not target.exists();target.write_bytes(raw);(O/(n+'.LF')).write_bytes(lf)
 inputs.append({'original_path':str(p),'snapshot':n,'RAW_bytes':len(raw),'RAW_sha256':H(raw),'LF_snapshot':n+'.LF','LF_bytes':len(lf),'LF_sha256':H(lf),'LF_recipe':'CRLF-only','original_mtime_ns':p.stat().st_mtime_ns})
for n in ['review-run.json','slot-decisions.json','reconstruction.utf8.txt','native-manifest.json','lease.json','decoded0.json','complete-reconstruction-decision-input.raw.json','parent-packet0.json']:
 snapshot(R/'anonymous-decoder'/n,'blind70.'+n)
for p,n in [(ROOT/'tools/astis_site.py','reader.astis_site.exactraw.py'),(ROOT/'website/scripts/declaration_lessons.py','reader.declaration_lessons.exactraw.py'),(ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ReflectionIntertwining.lean','parent69.ReflectionIntertwining.exactraw.lean'),(ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/GaussianReflection.lean','parent.GaussianReflection.exactraw.lean'),(ROOT/'tools/astis_semantic_roundtrip_core.py','schema.current-core.exactraw.py'),(R/'reader-helper-targeted-tests70/receipt.json','reader.root-focused-tests.receipt.exactraw.json'),(R/'reader-helper-pycompile70/receipt.json','reader.root-pycompile.receipt.exactraw.json')]:snapshot(p,n)
p=O/'stageB.supplemental-input-manifest.json';p.write_text(json.dumps({'schema':'source70-stageB-supplemental-fixed-inputs-v1','actual_pid':os.getpid(),'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'input_count':len(inputs),'inputs':inputs,'scope':'native blind binding; three-module static scoped reader scanner; schema; root test receipts only','no_whole_site_or_browser_execution':True},ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
for n in ['native-manifest.json','lease.json','slot-decisions.json']:
 print('READ blind '+n+'\n'+(O/('blind70.'+n)).read_text(encoding='utf-8'))
print(json.dumps({'actual_pid':os.getpid(),'input_count':len(inputs),'reader_test_receipts':[json.loads((O/n).read_bytes()) for n in ['reader.root-focused-tests.receipt.exactraw.json','reader.root-pycompile.receipt.exactraw.json']]},ensure_ascii=True))
