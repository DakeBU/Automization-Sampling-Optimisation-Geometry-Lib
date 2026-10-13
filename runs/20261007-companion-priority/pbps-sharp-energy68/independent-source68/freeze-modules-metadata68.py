from pathlib import Path
import json,hashlib,os,datetime
R=Path('E:/Samplinglib');O=R/'runs/20261007-companion-priority/pbps-sharp-energy68/independent-source68';B=R/'runs/20261007-companion-priority/pbps-sharp-energy68';P=json.loads((O/'final-inputs/004.RAW.snapshot').read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def write(n,o):(O/n).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
files=[R/json.loads((O/f'final-inputs/{i:03d}.RAW.snapshot').read_text())['lean']['file'] for i in range(3)]
for s in P['slugs']:files += [R/f'website/content/publications/{s}.json',R/f'website/content/declaration_lessons/{s}.json']
files += [R/f'research-wiki/frontier-cells/{s}.json' for s in P['active_cells']]
files += [R/f'research-wiki/semantic-roundtrip/audits/{a}.json' for a in P['audit_ids']]
files += [B/'prose-and-span-overlay68-v2'/f for f in ['proposal.json','0.before.exactraw.snapshot.json','0.after.exactraw.snapshot.json','1.before.exactraw.snapshot.json','1.after.exactraw.snapshot.json']]
files += [R/'website/scripts/publication_reader.py',R/'website/scripts/inline_lean.py']
entries=[]
for i,p in enumerate(files):
 b=p.read_bytes();lf=b.replace(b'\r\n',b'\n').replace(b'\r',b'\n');a=f'final-inputs/current{i:03d}.RAW.snapshot';z=f'final-inputs/current{i:03d}.LF.snapshot';(O/a).write_bytes(b);(O/z).write_bytes(lf);entries.append({'path':p.relative_to(R).as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_bytes':len(lf),'LF_sha256':sha(lf),'raw_snapshot':a,'lf_snapshot':z})
write('final-inputs.modules-metadata.manifest.json',{'schema':1,'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_pid':os.getpid(),'entries':entries,'no_prior67_final_source_review_input':True,'root_or_math_review_conclusions_included':False})
write('negative.schema-display-truncation.json',{'kind':'OBSERVER_SCHEMA_DISPLAY_TRUNCATION','effect':'Bounded context schema display also printed publication-plan full private definitions, causing a clipped console. Complete plan/module/packet RAW inputs remain separately frozen. Subsequent displays omit nested private definitions and use focused module/step slices.','actual_command_pid':40744,'authoritative_tool_exit':0,'source_defect':False})
for i in range(3):
 p=json.loads((O/f'final-inputs/{i:03d}.RAW.snapshot').read_text());c=p['candidate_publication_context'];module=(R/p['lean']['file']).read_bytes();lf=module.replace(b'\r\n',b'\n').replace(b'\r',b'\n');assert c['current_lean_module']==lf.decode('utf8');print('MODULE',i,p['lean']['file'],'RAW',sha(module),'LF',sha(lf),'CONTEXT_FILE_HASH',c['file'],'BINDING',p['publication_binding_sha256'],'CTX_SHA',sha(json.dumps(c,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()))
for a in P['audit_ids']:
 audit=json.loads((R/f'research-wiki/semantic-roundtrip/audits/{a}.json').read_text());rec=audit['reconstruction'];print('AUDIT',a,'KEYS',list(audit),'RECON_BINDINGS',{k:v for k,v in rec.items() if k not in ['text'] and not isinstance(v,(dict,list))})
print('CURRENT_MODULES_METADATA_FREEZE_EXIT_0',os.getpid(),len(entries))
