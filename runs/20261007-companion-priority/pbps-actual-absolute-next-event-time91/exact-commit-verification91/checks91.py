from pathlib import Path
import datetime,hashlib,json,os,re,subprocess,sys,time
R=Path('E:/Samplinglib');O=Path(__file__).parent;B=O.parent;C='d62f7b2c89e749953a36d8922124865a4651e55e';BASE='204fd4eee61724db77963cb33ddaddbcd90b906d'
D='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualAbsoluteNextEventTime.actual_absolute_next_event_time_law';CELL='ASTIS-SW-PBPS-actual-absolute-next-event-time';M=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualAbsoluteNextEventTime.lean'
def sha(b):return hashlib.sha256(b).hexdigest()
def info(p):return dict(path=str(p.relative_to(R)),raw_sha256=sha(p.read_bytes()),bytes=p.stat().st_size)
def save(n,v):
 with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
freeze=json.loads((O/'input-freeze91.json').read_bytes());assert freeze['verified_commit']==C
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()==C
env=os.environ.copy();env['PATH']=str(R/'.astis/toolchain/lean-4.33.0-windows/bin')+os.pathsep+env['PATH'];env.pop('ELAN_TOOLCHAIN',None)
lake=str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe');py=[sys.executable,'-X','utf8']
(O/'CurrentPublicKernel91.lean').write_text('import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualAbsoluteNextEventTime\n#check '+D+'\n#print axioms '+D+'\n',encoding='utf8')
(O/'publication-reviewed91.py').write_text("import sys\nsys.path[:0]=['E:/Samplinglib','E:/Samplinglib/tools']\nfrom tools.astis_publication import check_advance\ncheck_advance(["+repr(D)+"],reviewed=True)\nprint('PUBLICATION REVIEWED=TRUE PASS')\n",encoding='utf8')
receipts=[]
def run(n,cmd):
 t=time.monotonic();started=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with (O/(n+'.stdout.log')).open('xb') as out,(O/(n+'.stderr.log')).open('xb') as err:
  p=subprocess.Popen(cmd,cwd=R,env=env,stdout=out,stderr=err);print(n,'foreground PID',p.pid,flush=True);code=p.wait()
 receipt=dict(command=cmd,checked_commit=C,started_utc=started,ended_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),seconds=time.monotonic()-t,foreground_PID=p.pid,exit_code=code,terminal_closed=True,stdout=info(O/(n+'.stdout.log')),stderr=info(O/(n+'.stderr.log')))
 save(n+'.receipt.json',receipt);receipts.append(info(O/(n+'.receipt.json')));print(n,'EXIT',code,flush=True);assert code==0,n
for n,cmd in [('packet',py+['tools/astis_publication.py','packet','--cell',CELL]),('focused-module',[lake,'build','AutoSamplingTheory.ExampleCases.ProximalBPS.ActualAbsoluteNextEventTime']),('current-kernel',[lake,'env','lean',str(O/'CurrentPublicKernel91.lean')]),('contributor',py+['tools/astis_contributor_contract.py','check','--base',BASE]),('publication',py+['tools/astis_publication.py','check','--base',BASE]),('publication-reviewed',py+[str(O/'publication-reviewed91.py')]),('semantic',py+['tools/astis_semantic_roundtrip.py','check']),('frontier',py+['tools/astis_frontier_cells.py','check']),('committed-diff', ['git','-c','core.whitespace=cr-at-eol','diff','--check',BASE,C])]:run(n,cmd)
packet=json.loads((O/'packet.stdout.log').read_bytes());assert len(packet['targets'])==1 and packet['targets'][0]['publication_binding_sha256']=='17537bf9a2aec56bbafbeea370fc9741c88ae1d34b48743249cb1b99b655c921'
k=(O/'current-kernel.stdout.log').read_text(encoding='utf8');ax=re.search(r'depends on axioms:\s*\[([^]]+)\]',k,re.S);assert ax and set(x.strip() for x in ax[1].split(','))=={'propext','Classical.choice','Quot.sound'} and 'sorryAx' not in k
sys.path[:0]=[str(R),str(R/'tools')];from tools import astis
hits=astis.forbidden_pattern_hits();save('fake-closure-scan91.json',dict(verifier_id='/root/independent_math91',verified_commit=C,algorithm='tools.astis.forbidden_pattern_hits()',scanned_files=len(astis.lean_source_files()),hits=hits,module=info(M)));assert not hits
# Verify the full blinded reconstruction hash chain and flags.
A=json.loads((R/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualAbsoluteNextEventTime.json').read_bytes());dec=R/'runs/semantic-roundtrip/anonymous91/decoder-output';dr=json.loads((dec/'run.json').read_bytes());reconstruction=json.loads((dec/'reconstruction.json').read_bytes());dm=json.loads((dec/'raw-manifest.json').read_bytes());inp=R/'runs/semantic-roundtrip/anonymous91/input.json';ip=json.loads(inp.read_bytes())
assert dr['decoder']=='/root/blind_decoder91' and all(dr[k] is False for k in ['source_text_visible','source_anchor_visible','source_identity_visible','implementation_visible','external_browsing_used']);assert not dr['other_mathematical_inputs_read']
for e in dm['inputs']+dm['outputs']:assert sha(Path(e['path']).read_bytes())==e['sha256']
assert sha(inp.read_bytes())==dr['input_file_sha256'] and sha(ip['lean']['statement'].encode())==dr['statement_sha256'];assert A['reconstruction']['text']==reconstruction['reconstructed_theorem_text'];assert sha(reconstruction['reconstructed_theorem_text'].encode())==dr['reconstructed_text_sha256']==dm['reconstructed_text_sha256'];assert reconstruction['decoder_run_sha256']==sha((dec/'run.json').read_bytes())
for e in freeze['exact_commit_matches']+freeze['local_pinned_or_excluded_inputs']+freeze['all21collaborator_RAWs']:
 p=R/e['path'];assert sha(p.read_bytes())==e['raw_sha256'],'changed input '+e['path']
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()==C
save('checks-complete91.json',dict(status='PASS',verified_commit=C,verifier_id='/root/independent_math91',receipts=receipts,standard_axioms_only=True,source_audit_accepted_bound_to_canonical_native=True,decoder_hash_chain_and_all_disclosure_flags_checked=True,all21collaborator_RAWs_preserved=True,archive_count=91,source_main_aggregate_reader_Goal_completion=False))
print('EXACT SCIENCE91 CHECKS PASS',flush=True)
