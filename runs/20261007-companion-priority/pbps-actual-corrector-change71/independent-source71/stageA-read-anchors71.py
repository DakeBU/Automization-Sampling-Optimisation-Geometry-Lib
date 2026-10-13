import sys
sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding='utf-8')
import json, pathlib, hashlib
repo = pathlib.Path('E:/Samplinglib')
out = pathlib.Path(__file__).parent
old = repo / 'runs/20261007-companion-priority/pbps-corrector-change-preproof71/independent-header-source71'
names = ['stageA.source-expectations71.before-header.frozen.json', 'stageA.finite-source255-and-target18-coverage.frozen.json', 'stageA.anti-anchoring-exposure.frozen.json', 'stageA.source-first-provenance-and-reuse.json', 'stageA.independent-RAW-math-inventory.json', 'stageA.primary-input-manifest.json', 'source-first71.source.formulas.exact.json', 'source-first71.source.math.inventory.json', 'lease.final.json', 'owned-manifest.json']
pins=[]
for n in names:
    p=old/n;b=p.read_bytes();o=json.loads(b)
    pins.append({'path':p.relative_to(repo).as_posix(),'raw_bytes':len(b),'raw_sha256':hashlib.sha256(b).hexdigest(),'lf_sha256':hashlib.sha256(b.replace(b'\r\n',b'\n')).hexdigest()})
    print('\nFILE',n,'BYTES',len(b))
    if n in names[:4]:print(json.dumps(o,ensure_ascii=False,indent=2))
    elif n=='stageA.finite-source255-and-target18-coverage.frozen.json':print(json.dumps(o,ensure_ascii=False,indent=2))
    else:print(json.dumps({k:(v if not isinstance(v,list) else {'count':len(v),'first':v[:1]}) for k,v in o.items()},ensure_ascii=False,indent=2)[:9000])
gpath=repo/'runs/20261007-companion-priority/pbps-actual-projected-rotation70/independent-source70/stageA.source-proof-graph70.frozen.json'
b=gpath.read_bytes();g=json.loads(b);pins.append({'path':gpath.relative_to(repo).as_posix(),'raw_bytes':len(b),'raw_sha256':hashlib.sha256(b).hexdigest(),'lf_sha256':hashlib.sha256(b.replace(b'\r\n',b'\n')).hexdigest()})
print('\nPRIOR70 STAGEA GRAPH',json.dumps(g,ensure_ascii=False,indent=2))
(out/'stageA.read-only-anchor-pins.json').write_text(json.dumps({'schema':'source71-stageA-read-only-anchor-pins-v1','lf_recipe':'bytes.replace(CRLF, LF) only','inputs':pins},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
o=json.loads((out/'stageA.primary255.reparsed-inventory.json').read_bytes());print('\nCURRENT INVENTORY SHAPE',json.dumps(o,ensure_ascii=False)[:4000])
