from pathlib import Path
import json,hashlib,re,datetime
root=Path(r'E:\Samplinglib');stage=Path(__file__).parent
def sha(b):return hashlib.sha256(b).hexdigest()
def read(path):
    with path.open('rb') as handle:return handle.read()
def snapshot(name,data):
    with (stage/(name+'.raw.snapshot')).open('wb') as handle:handle.write(data)
    lf=data.replace(b'\r\n',b'\n')
    with (stage/(name+'.lf.snapshot')).open('wb') as handle:handle.write(lf)
    return {'raw_bytes':len(data),'raw_sha256':sha(data),'lf_bytes':len(lf),'lf_sha256':sha(lf)}
assert not (stage/'lease.open.json').exists()
inputs={}
for label,path in [('lesson',root/'website/content/declaration_lessons/pbps-l2-macroscopic-mean.json'),('publication',root/'website/content/publications/pbps-l2-macroscopic-mean.json')]:
    inputs[label]={'path':str(path),**snapshot(label,read(path))}
source=root/'AutoSamplingTheory/ExampleCases/ProximalBPS/L2MacroscopicMean.lean'
raw=read(source);text=raw.decode('utf-8');start=text.index('theorem actual_macroscopic_l2_mean');end=start+re.search(r'\s*:=\s*by\b',text[start:]).start()
header=text[start:end].encode('utf-8');inputs['science_header']={'path':str(source),'line_start':text.count('\n',0,start)+1,'line_end':text.count('\n',0,end)+1,**snapshot('science-header',header),'body_read':'No proof body emitted; binary read only to select exact header'}
testpath=root/'Tests/ProximalBPSL2MacroscopicMean.lean';raw=read(testpath);text=raw.decode('utf-8')
for name in ['actual_rough_difference_variance','rank_zero_actual_source_constant']:
    found=re.search(r'^(?:theorem|lemma)\s+'+re.escape(name)+r'\b',text,re.M)
    assert found,name
    start=found.start();end=start+re.search(r'\s*:=\s*by\b',text[start:]).start();data=text[start:end].encode('utf-8')
    inputs[name]={'path':str(testpath),'line_start':text.count('\n',0,start)+1,'line_end':text.count('\n',0,end)+1,**snapshot(name,data)}
    print(name,data.decode('utf-8'))
lesson=json.loads(read(stage/'lesson.raw.snapshot').decode('utf-8'))['units'][0]
formula=lesson['formula']
print('PARSED_FORMULA_PREFIX',repr(formula[:100]));print('PARSED_STEP4',repr(lesson['steps'][3]['formula']))
obj={'schema_version':1,'status':'OPEN_WAITING_EXACT_HEAD_AND_FOUR_1440X1800_BROWSER_CAPTURES','reviewer':'/root/sourcegraph_creator56','scope':'Independent local human exposition55 only; not source-blind or identity-blind; not validating56','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'inputs':inputs,'compiler':'NOT_STARTED_CLOSED','final_seal_written':False,'existing56_artifacts':'Immutable, no reads/writes required for this review','pending':['exact integration HEAD','four actual1440x1800 PNGs with matching DOM capture evidence','exact adjacent initially folded compiled Lean display binding']}
with (stage/'lease.open.json').open('w',encoding='utf-8',newline='\n') as handle:json.dump(obj,handle,indent=2);handle.write('\n')
