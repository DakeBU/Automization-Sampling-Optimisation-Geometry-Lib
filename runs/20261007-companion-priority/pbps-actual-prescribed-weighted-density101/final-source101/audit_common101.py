from pathlib import Path
import json,hashlib,re,datetime
B=Path('runs/20261007-companion-priority');R=B/'pbps-actual-prescribed-weighted-density101';O=R/'final-source101';PRE=B/'pbps-actual-prescribed-path-reversal100/next-primary101'
def h(b):return hashlib.sha256(b).hexdigest()
def ref(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),raw_sha256=h(b),bytes=len(b))
def put(n,d):
 p=O/n;assert not p.exists(),p;p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return ref(p)
module=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPrescribedWeightedDensity.lean')
lesson=Path('website/content/declaration_lessons/pbps-actual-prescribed-weighted-density.json');pub=Path('website/content/publications/pbps-actual-prescribed-weighted-density.json')
primary=B/'phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
pp=R/'reviewer-packet101.json';p=json.loads(pp.read_bytes());pch=p['packet_sha256'];pd=dict(p);pd.pop('packet_sha256')
assert h(json.dumps(pd,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode())==pch=='ada43d2d1a5c74087e90387e5505ab9f8032418beb83f3ef56fff3c479903fb8'
binding=p['publication_binding_sha256'];assert binding=='53fd5e8723d4680bad200242460cc94ef8cb5c17e07e751ba646eadc10ecd3b1'
assert all(v is False for v in p['anti_anchoring'].values())
old=json.loads((R/'reviewer-packet101.before-owner-erratum101.exactraw.snapshot.json').read_bytes())
old['roles']['formalizer']='companion_root_20261005';old['packet_sha256']=pch;assert old==p
assert h(module.read_bytes())=='b9c6e8ed0655b9c607eff38ecf74eb3a4555ff90184475e8dfc554bb96dcb3c0'
u=json.loads(lesson.read_bytes())['units'][0];pu=json.loads(pub.read_bytes())['items'][0]
for key,value in p['candidate_publication_context']['lesson'].items():assert u[key]==value,key
assert p['source']['original_text']==u['statement']==pu['statement']
decdir=Path('runs/semantic-roundtrip/anonymous101/decoder-native');dec=decdir/'decoder-run.json';dd=json.loads(dec.read_bytes())
assert h(dec.read_bytes())==p['blind_reconstruction']['decoder_run_sha256']
assert all(dd[k] is False for k in ['source_visible','proof_visible','source_identity_visible','source_text_visible'])
assert h(p['blind_reconstruction']['text'].encode())==p['blind_reconstruction']['text_sha256']
s=module.read_text(encoding='utf-8');lines=module.read_bytes().splitlines(keepends=True)
def span(a,b):return dict(path=module.as_posix(),line_start=a,line_end=b,raw_sha256=h(b''.join(lines[a-1:b])))
lit=s[s.index('    let c :'):s.index('\n\n',s.index('          ENNReal.ofReal (w y (R A))'))]
assert p['lean']['statement'][p['lean']['statement'].index('    let c :'):]==lit
s94=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPrescribedPathDensity.lean').read_text(encoding='utf-8');s94=s94[s94.index('theorem actual_prescribed_path_density_rewrite'):]
assert s[s.index('    let c :'):s.index('    let R :')]==s94[s94.index('    let c :'):s94.index('    ∀ y xRef :')]
names=re.findall(r'^    let ([^ :]+)',lit,re.M);assert len(names)==26
repair=R/'independent-index-clarification101/index-clarification-decision101.native.json'
assert h(repair.read_bytes())=='7bebc60b5df30eb76f5488fa208d3f1e55683909e91bd0904d52dbda5cce1775'
assert json.loads(repair.read_bytes())['after']['raw_sha256']==h(lesson.read_bytes())
topology=B/'pbps-weighted-density-preread101/independent-header-math101/source-topology-decision101.native.json';top=json.loads(topology.read_bytes())
kernel=R/'independent-whole-math101/fresh-kernel-receipt101.native.json';kr=json.loads(kernel.read_bytes())
assert kr['production_raw_sha256']==h(module.read_bytes()) and kr['exit_code']==0 and kr['terminal_closed']
