import os, json, hashlib, subprocess, datetime, pathlib, re
R=pathlib.Path('E:/Samplinglib')
B=R/'runs/20261007-companion-priority/pbps-ordered-history-iteration-preread91'
O=B/'independent-header-math91'
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def desc(p,scope=None):
    p=pathlib.Path(p); p=p if p.is_absolute() else R/p
    data=p.read_bytes(); d={'path':p.relative_to(R).as_posix(),'raw_sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)}
    if scope:d['read_scope']=scope
    return d
def write(name,data):
    p=O/name
    with p.open('x',encoding='utf8',newline='\n') as f: json.dump(data,f,ensure_ascii=False,indent=2);f.write('\n')
    return desc(p)
inputs=[]
def inp(p,scope): inputs.append(desc(p,scope));return pathlib.Path(p) if pathlib.Path(p).is_absolute() else R/p
header=inp(B/'header91.proposed.lean','whole private Prop; full mathematical/definition/type audit')
assert desc(header)['raw_sha256']=='b8bba160f6134c7927167a0a34d99971ce75023ef7ea04f738a91b6862da2680'
for name in ['header-review91.packet.json','root.source91.adoption.json','source-proof-graph91.accepted-successor.json','pre-fetch91.workspace-RAW.json']:
    inp(B/name,'exact source/candidate/baseline binding; no source verdict substituted for mathematics')
for name in ['independent-primary-math-reconstruction91.v2.json','closed-RAW-manifest91.first-half.v2.json','source-topology91.decision.json','closed-RAW-manifest91.second-half.json']:
    inp(B/'independent-topology91'/name,'immutable independent primary-first/source-topology evidence reused unchanged')
for path in ['lean-toolchain','lake-manifest.json','.astis/toolchain/lean-4.33.0-windows/bin/lake.exe','.astis/toolchain/lean-4.33.0-windows/bin/lean.exe','.lake/packages/mathlib/Mathlib/MeasureTheory/Group/Prod.lean','.lake/packages/mathlib/Mathlib/MeasureTheory/Group/Measure.lean','.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Prod.lean']:
    inp(path,'pinned configuration/executable or bounded translation/product API inspection')
parent=inp('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteHistoryExtension.lean','complete private Prop and public signature only, lines1-122; no parent BODY used to establish source topology')
density=inp('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualConditionalNextWaitDensity.lean','private literal statement and public signature only')
inp('runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html','hash-only current recheck; primary-before-header substantive read preserved in first-half91')
raw=header.read_bytes(); (O/'header91.original.exactraw.lean').write_bytes(raw)
text=raw.decode('utf8'); par=parent.read_text(encoding='utf8')
def literal(s):return s[s.index('    let c :'):s.index('    ∀ y xRef :')]
assert literal(text)==literal(par)
bind=lambda s:s[s.index('    {E :'):s.index('    let c :')]
assert bind(text)==bind(par)
definitions=re.findall(r'^    let ([^ :]+)',literal(text),re.M)
prefix={'status':'BYTE_IDENTICAL_TO_ACTUAL90','six_analytic_binders':['hα','hαβ','hV','hH','hη','hβη'],'typeclass_and_binder_prefix_raw_sha256':hashlib.sha256(bind(text).encode()).hexdigest(),'model_prefix_raw_sha256':hashlib.sha256(literal(text).encode()).hexdigest(),'literal_model_definitions':definitions,'model_definition_count':len(definitions),'source_model_parent':desc(parent),'differences':'none in six-binder prefix or fourteen model lets; new local packaging derives absolute observer and guarded transport'}
write('definition-readback91.json',prefix)
probe=text.replace('\nend\nend AutoSamplingTheory.', '\n#check actual_absolute_next_event_time_statement\n\nend\nend AutoSamplingTheory.')
assert probe!=text
(O/'header91.private-check.lean').write_text(probe,encoding='utf8',newline='\n')
write('input-freeze91.json',{'utc':utc(),'reviewer_id':'/root/exact_verify77','context_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),'mathlib_commit':subprocess.check_output(['git','-C','.lake/packages/mathlib','rev-parse','HEAD'],cwd=R,text=True).strip(),'inputs':inputs,'snapshots':[desc(O/'header91.original.exactraw.lean'),desc(O/'header91.private-check.lean')],'no_Lean_BODY_or_proof':True})
env=dict(os.environ,PYTHONUTF8='1'); receipts=[]
for name,file in [('header-original91','header91.original.exactraw.lean'),('header-private-check91','header91.private-check.lean')]:
    args=[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env',str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lean.exe'),str(O/file)]
    start=utc()
    with (O/(name+'.log')).open('xb') as log:
        p=subprocess.Popen(args,cwd=R,env=env,stdout=log,stderr=subprocess.STDOUT);pid=p.pid;code=p.wait()
    receipt=write(name+'.receipt.json',{'utc_start':start,'utc_end':utc(),'argv':args,'cwd':R.as_posix(),'environment_overrides':{'PYTHONUTF8':'1'},'process_id':pid,'terminal_exit_code':code,'source':desc(O/file),'log':desc(O/(name+'.log')),'foreground_waited':True,'typecheck_only_no_proof':True})
    receipts.append(receipt);print(json.dumps({'receipt':receipt,'exit':code}),flush=True)
write('terminal91.json',{'utc':utc(),'receipts':receipts,'all_terminal':True,'native_trajectory':'two foreground whole-header elaborations; no theorem proof or tactics generated'})
