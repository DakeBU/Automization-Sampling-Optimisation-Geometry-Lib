from pathlib import Path
import datetime,hashlib,json,os,re,subprocess,sys,time
R=Path('E:/Samplinglib');O=Path(__file__).parent;B=O.parent;C='8ec33d055fb8a9b3ba376d4113e388b00882026f';BASE='a50632d37112aa59b7368079a917add0c69d0852'
D='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteCountPath.actual_finite_count_path_law';CELL='ASTIS-SW-PBPS-actual-finite-count-path';M=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteCountPath.lean'
def sha(b):return hashlib.sha256(b).hexdigest()
def info(p):return dict(path=p.relative_to(R).as_posix(),raw_sha256=sha(p.read_bytes()),bytes=p.stat().st_size)
def save(n,v):
 with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
freeze=json.loads((O/'input-freeze93.json').read_bytes());assert freeze['status']=='PASS' and freeze['verified_commit']==C
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()==C
env=os.environ.copy();env['PATH']=str(R/'.astis/toolchain/lean-4.33.0-windows/bin')+os.pathsep+env['PATH'];env.pop('ELAN_TOOLCHAIN',None)
lake=str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe');py=[sys.executable,'-X','utf8']
with (O/'CurrentPublicKernel93.lean').open('x',encoding='utf8',newline='\n') as f:f.write('import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteCountPath\n#check @'+D+'\n#print axioms '+D+'\n')
with (O/'publication-reviewed93.py').open('x',encoding='utf8') as f:f.write("import sys\nsys.path[:0]=['E:/Samplinglib','E:/Samplinglib/tools']\nfrom tools.astis_publication import check_advance\ncheck_advance(["+repr(D)+"],reviewed=True)\nprint('PUBLICATION REVIEWED=TRUE PASS')\n")
receipts=[]
def run(n,cmd):
 t=time.monotonic();started=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with (O/(n+'.stdout.log')).open('xb') as out,(O/(n+'.stderr.log')).open('xb') as err:
  p=subprocess.Popen(cmd,cwd=R,env=env,stdout=out,stderr=err);print(n,'foreground PID',p.pid,flush=True);code=p.wait()
 receipt=dict(command=cmd,checked_commit=C,started_utc=started,ended_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),seconds=time.monotonic()-t,foreground_PID=p.pid,exit_code=code,terminal_closed=True,stdout=info(O/(n+'.stdout.log')),stderr=info(O/(n+'.stderr.log')))
 save(n+'.receipt.json',receipt);receipts.append(info(O/(n+'.receipt.json')));print(n,'EXIT',code,flush=True);assert code==0,n
for n,cmd in [('packet',py+['tools/astis_publication.py','packet','--cell',CELL]),('focused-module',[lake,'build','AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteCountPath']),('current-kernel',[lake,'env','lean',str(O/'CurrentPublicKernel93.lean')]),('contributor',py+['tools/astis_contributor_contract.py','check','--base',BASE]),('publication',py+['tools/astis_publication.py','check','--base',BASE]),('publication-reviewed',py+[str(O/'publication-reviewed93.py')]),('semantic',py+['tools/astis_semantic_roundtrip.py','check']),('frontier',py+['tools/astis_frontier_cells.py','check']),('committed-diff',['git','-c','core.whitespace=cr-at-eol','diff','--check',BASE,C])]:run(n,cmd)
packet=json.loads((O/'packet.stdout.log').read_bytes());assert len(packet['targets'])==1 and packet['targets'][0]['publication_binding_sha256']==freeze['publication_binding_sha256']
k=(O/'current-kernel.stdout.log').read_text(encoding='utf8');ax=re.search(r'depends on axioms:\s*\[([^]]+)\]',k,re.S);assert ax and set(x.strip() for x in ax[1].split(','))=={'propext','Classical.choice','Quot.sound'} and 'sorryAx' not in k
sys.path[:0]=[str(R),str(R/'tools')];from tools import astis
hits=astis.forbidden_pattern_hits();save('fake-closure-scan93.json',dict(verifier_id='/root/independent_whole_math93',verified_commit=C,algorithm='tools.astis.forbidden_pattern_hits()',scanned_files=len(astis.lean_source_files()),hits=hits,module=info(M)));assert not hits
for e in freeze['exact_commit_matches']+freeze['local_pinned_or_excluded_inputs']+freeze['all21collaborator_RAWs']:
 assert sha((R/e['path']).read_bytes())==e['raw_sha256'],'changed input '+e['path']
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()==C
save('checks-complete93.json',dict(status='PASS',verified_commit=C,verifier_id='/root/independent_whole_math93',receipts=receipts,standard_axioms_only=True,previous_exact_sealed_header_witness_reused_by_RAW=True,source_native_and_decoder_canonical_hash_recipes_checked=True,all21collaborator_RAWs_preserved=True,archive_count=freeze['archive_count'],source_main_aggregate_reader_Goal_completion=False))
print('EXACT SCIENCE93 CHECKS PASS',flush=True)
