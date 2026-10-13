from pathlib import Path
import hashlib,json,subprocess,os,datetime,re,copy
R=Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-actual-prescribed-path-density94';W=B/'independent-whole-math94';D=W/'lf-transfer94'
S=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPrescribedPathDensity.lean';L=R/'website/content/declaration_lessons/pbps-actual-prescribed-path-density.json';P=R/'website/content/publications/pbps-actual-prescribed-path-density.json'
def sha(b):return hashlib.sha256(b).hexdigest()
def info(p):
 b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),raw_sha256=sha(b),bytes=len(b))
def write(n,b):
 p=D/n;assert not p.exists(),p;p.write_bytes(b);return p
def js(n,x):return info(write(n,(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()))
old=(W/'ActualPrescribedPathDensity.exactraw.lean').read_bytes();new=S.read_bytes()
assert sha(old)=='5065f542feea7024214159903ad3e7b81f6df9a6fcbf46afecace49397d786a0'
assert sha(new)=='60792981d3d2bac30d78a2373f7eed0002def8600e92553e9b5b0c87761599ec'
assert old==(B/'lf-transfer94/0.before.exactraw.snapshot').read_bytes()
assert old.count(b'\r\n')==671 and old.replace(b'\r\n',b'\n')==new and b'\r' not in new
assert len(old)-len(new)==671
o=json.loads((W/'exposition94/lesson.accepted.exactraw.json').read_bytes());n=json.loads(L.read_bytes());mask=copy.deepcopy(n)
regions=[]
for i,s in enumerate(mask['units'][0]['steps']):
 a=o['units'][0]['steps'][i]['lean_source_region'];b=s['lean_source_region']
 assert a['source_raw_sha256']==sha(old) and b['source_raw_sha256']==sha(new)
 b['source_raw_sha256']=a['source_raw_sha256']
 src=b''.join(new.splitlines(keepends=True)[b['start_line']-1:b['end_line']]);code=s['lean'].encode()
 assert src==code and sha(src)==b['exact_code_raw_sha256']
 regions.append(dict(step=i+1,start_line=b['start_line'],end_line=b['end_line'],code_now_physical_raw_exact=True,raw_sha256=sha(src)))
assert mask==o,'Changes beyond seven source RAW digests'
assert P.read_bytes()==(W/'exposition94/publication.accepted.exactraw.json').read_bytes()
oldwit=(W/'ExactSealedWholeWitness94.trial2.lean').read_bytes();assert oldwit.startswith(old)
wit=write('ExactSealedWholeWitness94.LF.lean',new+oldwit[len(old):])
write('ActualPrescribedPathDensity.LF.exactraw.lean',new);write('lesson.LF.exactraw.json',L.read_bytes())
paths=[S,L,P,W/'ActualPrescribedPathDensity.exactraw.lean',W/'ExactSealedWholeWitness94.trial2.lean',W/'whole-math-decision94.native.json',W/'closed-RAW-whole94.native.json',W/'exposition94/exposition-decision94.native.json',W/'exposition94/closed-RAW-exposition94.native.json',W/'exposition94/lesson.accepted.exactraw.json',W/'exposition94/publication.accepted.exactraw.json',B/'lf-transfer94/0.before.exactraw.snapshot',R/'runs/20261007-companion-priority/pbps-prescribed-path-density-preread94/Header94.lean',R/'runs/20261007-companion-priority/pbps-prescribed-path-density-preread94/root.statement-seal94.json',R/'lean-toolchain',R/'lake-manifest.json']
inputs=[info(p) for p in paths]
assert inputs[12]['raw_sha256']=='283fef6c66240aec21c4f34c72442d85e25db3f95dde1104a96cb3fe7d04e832'
js('byte-delta94.native.json',dict(status='PASS',production_before=info(paths[3]),production_after=info(S),exact_CRLF_replacements=671,no_other_bytes_changed=True,lesson_changed_paths=['/units/0/steps/'+str(i)+'/lean_source_region/source_raw_sha256' for i in range(7)],lesson_no_other_changes=True,publication_unchanged=True,regions=regions,witness_recipe='Exact previously accepted successful witness with its production-prefix bytes replaced by the independently checked LF production; suffix bytes unchanged.'))
env=os.environ.copy();env.pop('ELAN_TOOLCHAIN',None);checks=[]
for label,p in [('actual-production',S),('sealed-witness',wit)]:
 cmd=[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env','lean',str(p)];start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 r=subprocess.run(cmd,cwd=R,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 out=write(label+'.stdout.exactraw.log',r.stdout);err=write(label+'.stderr.exactraw.log',r.stderr)
 rec=dict(command=cmd,exit_code=r.returncode,started_utc=start,ended_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),ELAN_TOOLCHAIN_removed=True,input=info(p),stdout=info(out),stderr=info(err))
 js(label+'.receipt.native.json',rec);checks.append(rec)
 assert r.returncode==0,r.stdout.decode(errors='replace')
 axs=re.findall(r"'([^']+)' depends on axioms: \[([^]]+)\]",r.stdout.decode('utf8'));assert len(axs)==(1 if label=='actual-production' else 8)
 for d,a in axs:assert set(re.split(r',\s*',a.strip()))=={'propext','Classical.choice','Quot.sound'}
 js(label+'.axioms.native.json',dict(declarations=[dict(declaration=d,axioms=re.split(r',\s*',a.strip())) for d,a in axs]))
for i in inputs:assert info(R/i['path'])==i,i['path']
mathlib=subprocess.check_output(['git','-C','.lake/packages/mathlib','rev-parse','HEAD'],cwd=R).decode().strip();assert mathlib=='db584cd6d46c92f209a44c0f1c829460d327499d'
decision={'schema_version':1,'kind':'INDEPENDENT_BYTE_ONLY_MATH_EXPOSITION_TRANSFER','reviewer':'/root/independent_whole_math93','decision':'ACCEPT_LF_TRANSFER_OF_PRIOR_WHOLE_MATH_AND_EXPOSITION','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checked_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip(),'production_before_raw':sha(old),'production_after_raw':sha(new),'lesson_after':info(L),'publication_after':info(P),'basis':['Exactly671 CRLF pairs became LF; all other production bytes identical. No change to any Lean token, theorem type, proof body, declaration order or line number.','Lesson JSON structural comparison finds only the seven source_raw_sha256 updates. Prose, embedded code, formulas, line ranges and embedded hashes unchanged. Publication bytes unchanged.','All seven embedded Lean excerpts now match physical source slice bytes exactly, without newline normalization.','Fresh lean compilation on the actual production path EXIT0; full exact sealed-header witness EXIT0. Public theorem, six private helpers and witness retain only propext, Classical.choice and Quot.sound.','Original Header94 bytes unchanged; successful witness is derived from exact prior successful witness by replacing only the checked production prefix. Prior complete math and corrected exposition review credit transfers.'],'checks':checks,'mathlib_commit':mathlib,'inputs':inputs,'necessary_repairs':[],'retained_prior_evidence':'Earlier closed manifests and decisions untouched. This supplement records normalization explicitly and does not overwrite their historical source-byte bindings.','outside_scope':['new source fidelity verdict','visual acceptance','full A7','exact future science commit verification','SAU VERIFIED transition'],'production_or_public_edits_by_reviewer':False,'ledger_changed':False}
a=js('LF-transfer-decision94.native.json',decision)
manifest={'schema_version':1,'kind':'CLOSED_RAW_LF_TRANSFER','hash_recipe':'SHA256 exact bytes; manifest excludes itself.','inputs':inputs,'outputs':[info(p) for p in sorted(D.iterdir()) if p.is_file()],'closure':'All authored files in owned LF transfer directory before this manifest enumerated. Earlier closed review directories untouched.'}
m=js('closed-RAW-LF-transfer94.native.json',manifest)
for i in manifest['inputs']+manifest['outputs']:assert info(R/i['path'])==i
assert {p.name for p in D.iterdir() if p.is_file()}=={Path(i['path']).name for i in manifest['outputs']}|{'closed-RAW-LF-transfer94.native.json'}
print(json.dumps(dict(status='PASS',decision=a,manifest=m,lesson=info(L)),indent=2))
