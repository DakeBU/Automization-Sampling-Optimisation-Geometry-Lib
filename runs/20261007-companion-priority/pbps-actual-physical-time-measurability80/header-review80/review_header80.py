from pathlib import Path
import hashlib, json, os, re, subprocess, datetime

ROOT = Path('E:/Samplinglib')
OUT = ROOT / 'runs/20261007-companion-priority/pbps-actual-physical-time-measurability80/header-review80'
HEADER = ROOT / 'runs/20261007-companion-priority/pbps-actual-physical-time-measurability80/header80.proposed.lean'
def raw(p):
    b=p.read_bytes()
    return {'path':p.relative_to(ROOT).as_posix(),'RAW_bytes':len(b),'RAW_sha256':hashlib.sha256(b).hexdigest()}
def write(name,data):
    p=OUT/name
    with p.open('x',encoding='utf-8',newline='\n') as f: json.dump(data,f,ensure_ascii=False,indent=2); f.write('\n')
    return raw(p)
def text(p): return p.read_text(encoding='utf-8')
assert raw(HEADER)['RAW_sha256']=='1b51f58a987d8b59bcb1b5280a8817af984d7fad4b09962ad8a229198f9f5215'
parent79=ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhysicalTimeCover.lean'
parent76=ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteJumpRecursion.lean'
parent73=ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHarmonicFlow.lean'
scope=ROOT/'runs/20261007-companion-priority/pbps-physical-time-measurability-preread80/independent-scope-review80'
paths=[HEADER,HEADER.parent/'prospective-inputs80.json',parent79,parent76,parent73,ROOT/'lean-toolchain',ROOT/'lake-manifest.json',scope/'review-manifest80-final.json',scope/'independent-source-topology-review80.json',scope/'independent-scope-review80.json',scope/'independent-primary-topology-refinement80.json',scope.parent/'source-freeze80.json',scope.parent/'source-topology-clarification80.json']
freeze=write('input-freeze80.json',{'reviewer':'/root/exact_verify77','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'inputs':[raw(p) for p in paths]})
h=text(HEADER); a=text(parent79); b=text(parent76)
def binders(s):
    start=s.index('    {E : Type*}')
    return s[start:s.index(' : Prop :=',start)+len(' : Prop :=')]
assert binders(h)==binders(a)==binders(b)
def defs(s):
    start=s.index('    let ')
    end=s.index('\n    ∃ Z',start) if '\n    ∃ Z' in s[start:] else s.index('\n    ∀ y',start) if '\n    ∀ y' in s[start:] else s.index('\n    (∀ y',start)
    chunks=re.split(r'(?=^    let )',s[start:end],flags=re.M)
    return {re.match(r'    let (\S+) ',v)[1]:v.rstrip() for v in chunks if v}
dh,da,db=defs(h),defs(a),defs(b)
assert len(dh)==11 and set(dh)==set(da)
assert all(dh[n]==da[n] for n in dh)
common=set(dh)&set(db)
assert len(common)==9 and all(dh[n]==db[n] for n in common)
readback=write('definition-readback80.json',{'status':'PASS','candidate':raw(HEADER),'binder_block_exact_text_equals_79_and_76':True,'six_analytic_binders':['hα','hαβ','hV','hH','hη','hβη'],'actual_literal_definitions':list(dh.keys()),'actual_literal_definition_count':11,'canonical_sample_definitions':list(dh.keys())[:2],'all_11_let_definitions_exact_text_equal_79_after_CRLF_normalization':True,'all_9_common_let_definitions_exact_text_equal_76_after_CRLF_normalization':True,'comparison':'Whitespace inside definitions retained; only line endings normalized and trailing block whitespace ignored. This checks source text, not a claim of independent kernel defeq certification.','definition_SHA256_normalized_UTF8':{n:hashlib.sha256(v.encode()).hexdigest() for n,v in dh.items()},'tuple_type':'((E × E) × (E × E)) × (NNReal × (Nat → Real))','tuple_projection_readback':{'a.1.1.1':'y','a.1.1.2':'xRef','a.1.2':'z0','a.2.1':'finite physical time','a.2.2':'canonical real threshold sample'}})
snapshot=OUT/'header80.exact-snapshot.lean'
with snapshot.open('xb') as f:f.write(HEADER.read_bytes())
assert raw(snapshot)['RAW_sha256']==raw(HEADER)['RAW_sha256']
cmd=['E:/Samplinglib/.astis/toolchain/lean-4.33.0-windows/bin/lake.exe','env','lean',snapshot.relative_to(ROOT).as_posix()]
env=os.environ.copy();env['PYTHONUTF8']='1'
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (OUT/'typecheck80.stdout.log').open('xb') as so,(OUT/'typecheck80.stderr.log').open('xb') as se:
    proc=subprocess.Popen(cmd,cwd=ROOT,env=env,stdout=so,stderr=se)
    code=proc.wait()
receipt=write('typecheck80.receipt.json',{'status':'PASS' if code==0 else 'FAIL','reviewer':'/root/exact_verify77','command_argv':cmd,'cwd':str(ROOT),'start_utc':start,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':code,'process_waited_foreground':True,'candidate':raw(HEADER),'compiled_exact_snapshot':raw(snapshot),'stdout':raw(OUT/'typecheck80.stdout.log'),'stderr':raw(OUT/'typecheck80.stderr.log'),'repair_overlay':None,'scope':'Complete named private Prop and its in-namespace #check, without any theorem BODY. Typecheck earns no proof or final source acceptance credit.'})
print(json.dumps({'freeze':freeze,'definition_readback':readback,'receipt':receipt,'exit_code':code},ensure_ascii=False))
