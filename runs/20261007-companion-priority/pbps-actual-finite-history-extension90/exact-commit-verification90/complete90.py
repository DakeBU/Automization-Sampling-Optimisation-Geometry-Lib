from pathlib import Path
import datetime,gzip,hashlib,json,os,re,subprocess,sys
R=Path('E:/Samplinglib');O=Path(__file__).parent;B=O.parent
PR=R/'runs/20261007-companion-priority/pbps-next-history-extension-preread90'
C='e8d38b3002f4562ef254205135c0d213f9efe410';BASE='d3bdf486a84f8edaac6930336879b87949fd113c';ME='/root/exact_verify77'
M='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteHistoryExtension.lean';MR='6cdc14328be5ec3ece3f028e6e1dd0185ee4031a8e651956ee0f55d4beebf029'
L='website/content/declaration_lessons/pbps-actual-finite-history-extension.json';P='website/content/publications/pbps-actual-finite-history-extension.json'
D='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteHistoryExtension.actual_finite_history_extension'
ID='ASTIS-SA-20261011-PBPSActualFiniteHistoryExtension';CELL='ASTIS-SW-PBPS-actual-finite-history-extension';A='research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualFiniteHistoryExtension.json'
BIND='b3a9241d785c8132839c366f260d5fbc3dcaa40aba8566560ec814e6c5716472';PACK='e05eb6e6f0301337eb17e14396af2577aeb852a022557b036c3e536735906000'
def path(p):
 p=Path(p);return p if p.is_absolute() else R/p
def rel(p):return path(p).relative_to(R).as_posix()
def sha(b):return hashlib.sha256(b).hexdigest()
def info(p):
 p=path(p);b=p.read_bytes();return dict(path=rel(p),raw_sha256=sha(b),bytes=len(b))
def load(p):return json.loads(path(p).read_bytes())
def save(n,v):
 with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
def git(*args):return subprocess.check_output(['git',*args],cwd=R,stderr=subprocess.PIPE)
def canon(v):return json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
assert git('rev-parse','HEAD').decode().strip()==C
freeze=load(O/'input-freeze90.json')
for g in ['exact_commit_matches','nested_mathlib_matches','local_fixed_primary_and_excluded_extracts','preexisting_collaborator_inputs']:
 for e in freeze[g]:assert info(e['path'])['raw_sha256']==e['raw_sha256']
cell_path='research-wiki/frontier-cells/'+CELL+'.json';blob=git('show',C+':'+cell_path);raw=path(cell_path).read_bytes()
assert raw==blob or raw.replace(b'\r\n',b'\n')==blob.replace(b'\r\n',b'\n')
cell=load(cell_path);assert cell['cell_id']==CELL and cell['status']=='proved_locally' and cell['graph_contribution']['focus_targets']==[D]
freeze['exact_commit_matches'].append(dict(**info(cell_path),git_blob_raw_sha256=sha(blob),exact_equal=raw==blob,newline_only_checkout_difference=raw!=blob,lossless_archive=None))
save('packet-target90.negative.json',dict(status='REVIEWER_WRONG_CELL_PACKET_TARGET_RETAINED',checked_commit=C,prior_packet=info(O/'packet.stdout.log'),prior_terminal_receipt=info(O/'packet.receipt.json'),wrong_target='ASTIS-SW-PBPS-actual-conditional-next-wait-density',correct_target=CELL,detected_by='Final packet publication binding assertion',mathematical_gate_failure=False,VERIFIED=False))
freeze['packet_target_correction']=info(O/'packet-target90.negative.json');freeze['actual_admitted_cell']=CELL
save('input-freeze90.authoritative.json',freeze)
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf8');env.pop('ELAN_TOOLCHAIN',None);env['PATH']=str(R/'.astis/toolchain/lean-4.33.0-windows/bin')+os.pathsep+env['PATH']
args=[sys.executable,'-X','utf8','tools/astis_publication.py','packet','--cell',CELL];start=now()
with (O/'packet90.stdout.log').open('xb') as out,(O/'packet90.stderr.log').open('xb') as err:
 child=subprocess.Popen(args,cwd=R,env=env,stdout=out,stderr=err);print('correct90 packet foreground PID',child.pid,flush=True);code=child.wait()
save('packet90.receipt.json',dict(command=args,cwd=str(R),checked_commit=C,actual_foreground_PID=child.pid,exit_code=code,terminal_closed=True,started_utc=start,finished_utc=now(),stdout=info(O/'packet90.stdout.log'),stderr=info(O/'packet90.stderr.log')));assert code==0
packet=load(O/'packet90.stdout.log');assert len(packet['targets'])==1 and packet['targets'][0]['publication_binding_sha256']==BIND and packet['targets'][0]['declaration']==D
for n in ['focused-module','current-kernel','contributor','publication','publication-reviewed','semantic','frontier']:
 rec=load(O/(n+'.receipt.json'));assert rec['exit_code']==0 and rec['terminal_closed'] and rec['checked_commit']==C
 for k in ['stdout','stderr']:assert info(rec[k]['path'])==rec[k]
text=path(O/'current-kernel.stdout.log').read_text('utf8');ax=re.search(r'depends on axioms:\s*\[([^]]+)\]',text,re.S);assert ax and {x.strip() for x in ax.group(1).split(',')}=={'propext','Classical.choice','Quot.sound'} and 'sorryAx' not in text
sys.path[:0]=[str(R),str(R/'tools')];from tools import astis
hits=astis.forbidden_pattern_hits();save('fake-closure-scan90.json',dict(verifier_id=ME,verified_commit=C,algorithm='tools.astis.forbidden_pattern_hits()',scanned_files=len(astis.lean_source_files()),hits=hits,module=info(M)));assert not hits
kernel=load(B/'independent-math90/kernel-dependency90.json')
for g in ['exact_commit_matches','nested_mathlib_matches','local_fixed_primary_and_excluded_extracts','preexisting_collaborator_inputs']:
 for e in freeze[g]:assert info(e['path'])['raw_sha256']==e['raw_sha256']
for e in load(O/'collaborator-preservation90.json')['RAWs']:assert info(e['path'])==e
assert git('rev-parse','HEAD').decode().strip()==C
save('checks-complete90.json',dict(status='PASS',verified_commit=C,verifier_id=ME,publication_binding_sha256=BIND,source_packet_sha256=PACK,standard_axioms_only=True,actual_public_parents=kernel['immediate_public_producers'],owned_count=11,private_immediate_count=18,transitive_ASTIS_constants=95,transitive_ASTIS_edges=170,source_coverage='One next-history strict finite transport step S87-I5/G86-11;28defs/sixanalytics/sevensemantic slots/six complete BODY formula regions. FullA7/global remain OPEN.',all21collaborator_RAWs_preserved=True,authoritative_freeze=info(O/'input-freeze90.authoritative.json'),wrong_prior_packet_diagnostic=info(O/'packet-target90.negative.json')))
print('EXACT SUCCESSOR SCIENCE90 ALL CHECKS PASS',flush=True)
