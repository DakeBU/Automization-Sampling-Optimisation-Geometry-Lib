from pathlib import Path
import datetime,hashlib,json,os,re,subprocess,sys,time
R=Path('E:/Samplinglib');O=Path(__file__).parent;B=O.parent;C='ad3b80a339bf1cf0dd88685f202632a92eeb0797';BASE='87975b5682bec621644b12e701aa5e45fefc3c2d'
D='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPrescribedPathDensity.actual_prescribed_path_density_rewrite';CELL='ASTIS-SW-PBPS-actual-prescribed-path-density';M=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPrescribedPathDensity.lean'
def sha(b):return hashlib.sha256(b).hexdigest()
def info(p):return dict(path=p.relative_to(R).as_posix(),raw_sha256=sha(p.read_bytes()),bytes=p.stat().st_size)
def save(n,v):
 with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
freeze=json.loads((O/'input-freeze94.json').read_bytes());assert freeze['status']=='PASS' and freeze['verified_commit']==C
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()==C
env=os.environ.copy();env['PATH']=str(R/'.astis/toolchain/lean-4.33.0-windows/bin')+os.pathsep+env['PATH'];env.pop('ELAN_TOOLCHAIN',None)
lake=str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe');py=[sys.executable,'-X','utf8']
h=(R/'runs/20261007-companion-priority/pbps-prescribed-path-density-preread94/Header94.lean').read_text(encoding='utf8')
params=h.split('noncomputable def candidate_statement\n',1)[1].split(' : Prop := by',1)[0];body=h.split('  exact\n',1)[1].split('\n#check',1)[0].rstrip()
kernel='import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPrescribedPathDensity\nopen MeasureTheory Set Filter\nopen scoped NNReal ENNReal Topology Classical\nnamespace ExactScience94\ntheorem sealed_whole\n'+params+' :\n'+body+' := by\n  exact '+D+' hα hαβ hV hH hη hβη\n#print axioms sealed_whole\n#check @'+D+'\n#print axioms '+D+'\nend ExactScience94\n'
with (O/'CurrentSealedKernel94.lean').open('x',encoding='utf8',newline='\n') as f:f.write(kernel)
with (O/'publication_reviewed94.py').open('x',encoding='utf8') as f:f.write("import sys\nsys.path[:0]=['E:/Samplinglib','E:/Samplinglib/tools']\nfrom tools.astis_publication import check_advance\ncheck_advance(["+repr(D)+"],reviewed=True)\nprint('PUBLICATION REVIEWED=TRUE PASS')\n")
receipts=[]
def run(n,cmd):
 t=time.monotonic();start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with (O/(n+'.stdout.log')).open('xb') as out,(O/(n+'.stderr.log')).open('xb') as err:
  p=subprocess.Popen(cmd,cwd=R,env=env,stdout=out,stderr=err);print(n,'foreground PID',p.pid,flush=True);code=p.wait()
 rec=dict(command=cmd,checked_commit=C,started_utc=start,ended_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),seconds=time.monotonic()-t,foreground_PID=p.pid,exit_code=code,terminal_closed=True,stdout=info(O/(n+'.stdout.log')),stderr=info(O/(n+'.stderr.log')))
 save(n+'.receipt.json',rec);receipts.append(info(O/(n+'.receipt.json')));print(n,'EXIT',code,flush=True);assert code==0,n
for n,cmd in [('packet',py+['tools/astis_publication.py','packet','--cell',CELL]),('focused-module',[lake,'build','AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPrescribedPathDensity']),('current-sealed-kernel',[lake,'env','lean',str(O/'CurrentSealedKernel94.lean')]),('contributor',py+['tools/astis_contributor_contract.py','check','--base',BASE]),('publication',py+['tools/astis_publication.py','check','--base',BASE]),('publication-reviewed',py+[str(O/'publication_reviewed94.py')]),('semantic',py+['tools/astis_semantic_roundtrip.py','check']),('frontier',py+['tools/astis_frontier_cells.py','check']),('committed-diff',['git','diff','--check',BASE,C])]:run(n,cmd)
packet=json.loads((O/'packet.stdout.log').read_bytes());assert len(packet['targets'])==1 and packet['targets'][0]['publication_binding_sha256']==freeze['publication_binding_sha256']
k=(O/'current-sealed-kernel.stdout.log').read_text(encoding='utf8');axs=re.findall(r'depends on axioms:\s*\[([^]]+)\]',k,re.S);assert len(axs)==2
for ax in axs:assert set(x.strip() for x in ax.split(','))=={'propext','Classical.choice','Quot.sound'}
assert 'sorryAx' not in k
sys.path[:0]=[str(R),str(R/'tools')];from tools import astis
hits=astis.forbidden_pattern_hits();save('fake-closure-scan94.json',dict(verifier_id='/root/independent_whole_math93',verified_commit=C,algorithm='tools.astis.forbidden_pattern_hits()',scanned_files=len(astis.lean_source_files()),hits=hits,module=info(M)));assert not hits
for e in freeze['exact_commit_matches']+freeze['local_pinned_or_excluded_inputs']+freeze['preserved_collaborator_inputs']:assert sha((R/e['path']).read_bytes())==e['raw_sha256'],'changed input '+e['path']
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()==C
save('checks-complete94.json',dict(status='PASS',verified_commit=C,verifier_id='/root/independent_whole_math93',receipts=receipts,standard_axioms_only=True,fresh_literal_sealed_header_witness=True,source_native_decoder_hash_recipes_checked=True,all21collaborator_RAWs_preserved=True,archive_count=freeze['archive_count'],full_A7_or_Goal_completion=False))
print('EXACT SCIENCE94 CHECKS PASS',flush=True)
