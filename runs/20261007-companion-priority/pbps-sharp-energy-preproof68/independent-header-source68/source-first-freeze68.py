from pathlib import Path
import hashlib,json,os,datetime
ROOT=Path('E:/Samplinglib'); OWN=ROOT/'runs/20261007-companion-priority/pbps-sharp-energy-preproof68/independent-header-source68'; PRE=ROOT/'runs/20261007-companion-priority/pbps-first-corrector-energy-preproof67/independent-primary67'
def sha(b):return hashlib.sha256(b).hexdigest()
def write(p,o):p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
write(OWN/'lease.open.json',{'schema':1,'status':'OPEN','actor':'independent_header_source68','source_first':True,'canonical_writes_authorized':False,'proof_search_authorized':False,'opened_utc':now(),'pid':os.getpid()})
files=['runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html']
files += [str((PRE/f).relative_to(ROOT)).replace('\\','/') for f in ['source-proof-graph.json','source-input-regions.json','source-coverage-inventory.json','seven-source-semantic-slots.json','literal-formulas-and-conditions.json','lease.final.json','review-run.json','primary-source-decision.json','owned-manifest.json','source.corrector-sharp-energy-and-consumers-B3.rendered.txt','source.global-assumptions.rendered.txt','source.actual-joint-law.rendered.txt','source.same-root-polar-B2.rendered.txt','source.real-L2-spectral-conventions-D1.rendered.txt']]
files += ['.agents/skills/astis-semantic-roundtrip/SKILL.md','docs/theorem-publication-protocol.md','docs/proof-digestion-protocol.md']
entries=[];(OWN/'inputs').mkdir()
for i,f in enumerate(files):
 b=(ROOT/f).read_bytes(); lf=b.replace(b'\r\n',b'\n').replace(b'\r',b'\n'); r=f'inputs/source{i:02d}.RAW.snapshot';l=f'inputs/source{i:02d}.LF.snapshot';(OWN/r).write_bytes(b);(OWN/l).write_bytes(lf)
 entries.append({'path':f,'raw_snapshot':r,'raw_bytes':len(b),'raw_sha256':sha(b),'lf_snapshot':l,'lf_bytes':len(lf),'lf_sha256':sha(lf)})
assert entries[0]['raw_sha256']=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
write(OWN/'source-inputs.manifest.json',{'schema':1,'phase':'source-first-before-header-read','actor':'independent_header_source68','timestamp_utc':now(),'pid':os.getpid(),'entries':entries})
write(OWN/'negative.initial-console-truncation.json',{'kind':'observer-output-truncation','effect':'Combined protocol/source output reported truncation; full frozen native inputs retained. All review uses complete frozen files and bounded later displays. No source defect or missing coverage inferred.'})
for f in ['lease.final.json','owned-manifest.json','source-input-regions.json','source-coverage-inventory.json']:
 o=json.loads((PRE/f).read_text(encoding='utf8'));print(f, 'dict keys',list(o) if isinstance(o,dict) else ('list',len(o)));print(json.dumps(o,ensure_ascii=False)[:1100])
print('SOURCE_FIRST_FREEZE_EXIT_0',os.getpid(),len(entries),entries[0]['raw_sha256'])
