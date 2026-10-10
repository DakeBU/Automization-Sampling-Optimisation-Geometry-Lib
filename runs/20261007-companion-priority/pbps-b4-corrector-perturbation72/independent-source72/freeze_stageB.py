from pathlib import Path
import hashlib,json,os,sys,traceback
ROOT=Path('E:/Samplinglib')
RUN=ROOT/'runs/20261007-companion-priority/pbps-b4-corrector-perturbation72'
OWN=RUN/'independent-source72'
def sha(b):return hashlib.sha256(b).hexdigest()
def write(n,v):
 p=OWN/n;p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
code=0
try:
 assert not (OWN/'lease.final.json').exists()
 freeze=json.loads((RUN/'source-review.freeze72.json').read_text(encoding='utf-8'))
 rows=[]
 entries=freeze['inputs']+[freeze['native_reconstruction']]
 entries += [{'path':str(RUN/'source-review.freeze72.json')}]
 extra=['AutoSamplingTheory/ExampleCases/ProximalBPS/ActualCorrectorChange.lean','runs/20261007-companion-priority/pbps-b4-corrector-perturbation72/anonymous.0.decoder.json','runs/20261007-companion-priority/pbps-b4-corrector-perturbation72/anonymous.1.decoder.json','tools/astis_semantic_roundtrip_core.py','docs/theorem-publication-protocol.md','.agents/skills/astis-semantic-roundtrip/SKILL.md','lean-toolchain','lake-manifest.json']
 entries += [{'path':str(ROOT/e)} for e in extra]
 for i,e in enumerate(entries):
  p=Path(e['path']);b=p.read_bytes();lf=b.replace(b'\r\n',b'\n')
  if 'RAW_sha256' in e:assert sha(b)==e['RAW_sha256'] and len(b)==e['RAW_bytes'],str(p)
  if 'LF_sha256' in e:assert sha(lf)==e['LF_sha256'],str(p)
  rawdest=OWN/f'inputs/{i:02d}.exactraw.snapshot';rawdest.parent.mkdir(parents=True,exist_ok=True);rawdest.write_bytes(b)
  lfdest=OWN/f'inputs/{i:02d}.LF.snapshot';lfdest.write_bytes(lf)
  opaque='semantic-roundtrip/audits/' in p.as_posix()
  rows.append({'index':i,'path':p.relative_to(ROOT).as_posix(),'raw_bytes':len(b),'raw_sha256':sha(b),'lf_bytes':len(lf),'lf_sha256':sha(lf),'raw_snapshot':rawdest.relative_to(OWN).as_posix(),'lf_snapshot':lfdest.relative_to(OWN).as_posix(),'lf_recipe':'CRLF-to-LF only','semantic_read':'OPAQUE HASH/SNAPSHOT ONLY; no audit slots/deltas/verdicts' if opaque else 'authorized current input'})
 write('StageB.current-inputs.manifest.json',{'schema':'source72-current-finite-inputs-v1','input_count':len(rows),'inputs':rows,'prior_StageA':'reference-only preparation.inputs.json; no old254 replay/copy','canonical_or_old_closed_writes':False})
 units=[]
 for n in [0,1]:
  packet=json.loads((RUN/f'source-review.packet.{n}.json').read_text(encoding='utf-8'))
  logical=dict(packet); claimed=logical.pop('packet_sha256')
  canonical=sha(json.dumps(logical,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
  assert canonical==claimed,(n,canonical,claimed)
  mod=ROOT/packet['lean']['file'];assert mod.read_text(encoding='utf-8')==packet['candidate_publication_context']['current_lean_module']
  assert sha(mod.read_bytes())==packet['candidate_publication_context']['file']
  context=packet['candidate_publication_context'];lesson=context['lesson']
  view={'packet_index':n,'official_packet_sha256':claimed,'packet_RAW_sha256':sha((RUN/f'source-review.packet.{n}.json').read_bytes()),'declaration':packet['lean']['declaration'],'source':packet['source'],'lean_statement':packet['lean']['statement'],'blind_reconstruction':packet['blind_reconstruction'],'approved_output_contract':packet['output_contract'],'publication_binding_sha256':packet['publication_binding_sha256'],'lesson':lesson,'candidate_assumptions':context.get('candidate_assumptions'), 'context_keys':list(context)}
  write(f'StageB.packet.{n}.authorized-reviewview.json',view)
  text='\n'.join(f'{i}: {line}' for i,line in enumerate(mod.read_text(encoding='utf-8').splitlines(),1))+'\n'
  (OWN/f'StageB.module.{n}.whole-line-readview.txt').write_text(text,encoding='utf-8',newline='\n')
  units.append({'unit':n,'packet_sha256':claimed,'packet_RAW_sha256':view['packet_RAW_sha256'],'publication_binding_sha256':packet['publication_binding_sha256'],'module_RAW_sha256':context['file'],'whole_lines':len(mod.read_text(encoding='utf-8').splitlines()),'lesson_steps':len(lesson['steps']),'context_keys':list(context)})
 print(json.dumps({'actual_pid':os.getpid(),'exit_code':0,'inputs':len(rows),'units':units},ensure_ascii=True,indent=2))
except BaseException:
 code=1;traceback.print_exc()
finally:
 write('StageB.freeze.terminal.json',{'actual_pid':os.getpid(),'exit_code':code,'argv':sys.argv,'background':False,'writes_scope':OWN.relative_to(ROOT).as_posix()})
sys.exit(code)
