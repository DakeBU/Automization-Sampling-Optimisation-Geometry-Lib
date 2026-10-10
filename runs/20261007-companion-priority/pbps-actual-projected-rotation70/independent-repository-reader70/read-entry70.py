import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,hashlib,os
O=pathlib.Path(__file__).resolve().parent;R=O.parent;p=R/'final-reader-repository-packet70.json';b=p.read_bytes();h=hashlib.sha256(b).hexdigest();assert h=='4b98a34d129fcd9c0d8aa5352eb25b5b198a480585a6f37edfba2726e8cf5740'
(O/'entry.packet70.exactraw.json').write_bytes(b);(O/'entry.packet70.exactraw.json.LF').write_bytes(b.replace(b'\r\n',b'\n'))
x=json.loads(b);print('actual_pid',os.getpid(),'RAWbytes',len(b),'RAWsha',h);print('keys',list(x));print(json.dumps({k:v for k,v in x.items() if k not in ['inputs']},ensure_ascii=False,indent=2));print('inputs type',type(x.get('inputs')).__name__);print('first input',json.dumps(x.get('inputs',[None])[0],ensure_ascii=False));print('input count',len(x.get('inputs',[])))
