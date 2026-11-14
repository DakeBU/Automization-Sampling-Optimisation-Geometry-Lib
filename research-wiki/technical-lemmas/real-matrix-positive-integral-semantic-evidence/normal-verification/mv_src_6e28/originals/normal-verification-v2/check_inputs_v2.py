from pathlib import Path
import json,hashlib,subprocess,shutil
R=Path('/Users/zhouhuanjian/ASTIS-GC');B=R/'.astis/semantic-neutral-20261112/mv_src_6e28/normal-verification-v2';F=B.parent/'final-anti-anchored-phase'
def h(b):return hashlib.sha256(b).hexdigest()
def read(p):return (R/p).read_bytes()
records=[]
def check(p,b):
 a=read(p);assert a==b,p;records.append({'path':p,'bytes':len(a),'sha256':h(a),'exact_equal':True})
port=json.loads((F/'portable-custody-manifest.json').read_bytes())
for x in port['records']:
 a=read(x['source_path']);assert len(a)==x['bytes'] and h(a)==x['sha256'];check(x['destination_path'],a)
for label,slug,epath,aname in [('S','huanjian-real-matrix-positive-integral','research-wiki/technical-lemmas/real-matrix-positive-integral-semantic-evidence','huanjian-real-matrix-positive-integral'),('P/v2','huanjian-gaussian-source-matrix-variance','research-wiki/paper-contributions/GaussianComplexity/source-matrix-variance-semantic-evidence','huanjian-gaussian-source-matrix-variance-uncentered')]:
 for k in ['declaration_lessons','publications']:check('website/content/'+k+'/'+slug+'.json',(F/label/(k+'.original.json')).read_bytes())
 for k in ['source-lean-map.draft.json','decoder-original-custody.json']:
  f=F/label/k
  if not f.exists():f=F/'P'/k
  check(epath+'/'+k,f.read_bytes())
 packet='anti-anchored-reviewer-packet.json' if label=='S' else 'anti-anchored-reviewer-packet.v2.json'
 check(epath+'/'+packet,(F/label/'anti-anchored-reviewer-packet.original.json').read_bytes())
 aid='huanjian-real-matrix-positive-integral.json' if label=='S' else 'huanjian-gaussian-source-matrix-variance.json'
 p=R/'research-wiki/semantic-roundtrip/audits'/aid
 if not p.exists():
  target=json.loads((F/label/'canonical-audit-overlay.portable.json').read_bytes())
  pp=[x for x in (R/'research-wiki/semantic-roundtrip/audits').glob('*.json') if json.loads(x.read_bytes()).get('id')==target.get('id')]
  assert len(pp)==1; p=pp[0]
 d=json.loads(p.read_bytes());orig=json.loads((F/label/'canonical-audit-overlay.portable.json').read_bytes())
 for k,v in orig.items():assert d[k]==v,(str(p),k)
 records.append({'path':str(p.relative_to(R)),'sha256':h(p.read_bytes()),'independent_overlay_fields_exact':True})
 # decoder originals exact neutral inputs/runs/reconstruction/freeze
 ld='neutral_decode_6a17' if label=='S' else 'neutral_decode_d204'
 for name in ['input.json','decoder-run.json','reconstruction.md','freeze-manifest.json']:
  check(epath+'/decoder-originals/'+ld+'/'+name,(F/('S' if label=='S' else 'P')/'decoder-originals'/name).read_bytes())
compiled=json.loads((B/'inputs/native/compile-results.json').read_bytes())
for x in compiled:
 p=x['module'].replace('.','/')+'.lean';a=read(p);assert h(a)==x['source_sha256'];assert subprocess.check_output(['git','show','9964c33c4599f85d27dc8687e8bd6fdb5c44ff49:'+p],cwd=R)==a
 records.append({'path':p,'sha256':h(a),'native_math_commit_and_current_equal':True})
pl='research-wiki/technical-lemmas/real-matrix-positive-integral-semantic-evidence/actual-PROVED_LOCAL-evidence.full.json';a=read(pl);assert h(a)=='3e5ea727729c5fcaaa5df8b74c77ac59c816438a10adc505bd1a95c9e8027cb6'
(B/'inputs/actual-PROVED_LOCAL-evidence.full.json').write_bytes(a)
append=read('research-wiki/technical-lemmas/real-matrix-positive-integral-semantic-evidence/actual-PROVED_LOCAL-append.exact.jsonl');assert h(append)=='33090842789407870af22abf997ef521d6cf29ac38ce5cb87aaec46d5e9f7204';assert json.loads(append)['evidence']==json.loads(a)
(B/'inputs/actual-PROVED_LOCAL-append.exact.jsonl').write_bytes(append)
source='.astis/huanjian-resume-20261103/2610.20492v1.html';assert h(read(source))=='6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915'
records.append({'path':source,'sha256':h(read(source)),'pinned_source_equal':True})
(B/'frozen-input-current-byte-checks.json').write_text(json.dumps({'records':records,'original_20_PL_fields':len(json.loads(a)),'all_pass':True},indent=2)+'\n')
print('PASS',len(records),'checks; original 20 fields preserved')
