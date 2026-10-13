from pathlib import Path
from html.parser import HTMLParser
import json, hashlib, re, struct, subprocess, sys, datetime, os
sys.stdout.reconfigure(encoding='utf8')
ROOT=Path('E:/Samplinglib'); B=ROOT/'runs/20261007-companion-priority/pbps-rough-mean-gradient56'; OUT=B/'exposition-seal56'
SCI='db2c1237cd56698ae560a8121abfcbf374ff8838'; HEAD='4a35307e4ca010e12bf5628b8b023c8449d9cce9'
def sha(b): return hashlib.sha256(b).hexdigest()
def canonical(j): return json.dumps(j,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf8')
def write(n,j,field='complete_object_sha256'):
    if field: j[field]=sha(canonical(j))
    (OUT/n).write_bytes((json.dumps(j,ensure_ascii=False,indent=2)+'\n').encode('utf8'))
    q=json.loads((OUT/n).read_bytes());
    if field:
        v=q.pop(field); assert sha(canonical(q))==v
    return j
def pin(p):
    p=Path(p); p=p if p.is_absolute() else ROOT/p; raw=p.read_bytes();lf=raw.replace(b'\r\n',b'\n')
    return {'path':str(p).replace('\\','/'),'bytes':len(raw),'raw_sha256':sha(raw),'lf_bytes':len(lf),'lf_sha256':sha(lf)}
inputs=[]
def take(p):
    q=pin(p);inputs.append(q); raw=Path(q['path']).read_bytes();i=len(inputs)
    name=f'{i:03d}.{Path(q["path"]).name}'
    (OUT/'inputs'/f'{name}.raw.snapshot').write_bytes(raw)
    (OUT/'inputs'/f'{name}.lf.snapshot').write_bytes(raw.replace(b'\r\n',b'\n'))
    assert (OUT/'inputs'/f'{name}.raw.snapshot').read_bytes()==raw
    assert (OUT/'inputs'/f'{name}.lf.snapshot').read_bytes()==raw.replace(b'\r\n',b'\n')
    return raw
(OUT/'inputs').mkdir(exist_ok=False)
initial=['publication-plan.json','verified.json','integration.notes.json','visual.inspection.json','root.integration.0.lease.json','source.review.lease.json']
for n in initial: take(B/n)
for n in ['result0.json','reviewer.source.run.json','source.review.json','manifest.json']:
    take(B/'source-review56'/n)
primary=ROOT/'runs/20261007-companion-priority/phase-pbps-primary-preread56'
for n in ['primary.contract.json','lease.json','A3.SS1.text.txt','A3.SS2.text.txt','A2.SS1.text.txt','A2.SS2.text.txt']:take(primary/n)
for p in ['website/content/publications/pbps-rough-mean-gradient.json','website/content/declaration_lessons/pbps-rough-mean-gradient.json','research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261008-PBPSRoughMeanGradient.json','AutoSamplingTheory/ExampleCases/ProximalBPS/RoughMeanGradient.lean','Tests/ProximalBPSRoughMeanGradient.lean','docs/evidence-routed-memory-protocol.md','docs/proof-digestion-protocol.md','.agents/skills/astis-semantic-roundtrip/SKILL.md']:take(p)
for n in ['L2MacroscopicMean.header.lf.snapshot.lean','MacroscopicEnergy.header.lf.snapshot.lean','SourceMeanGradientDomain.header.lf.snapshot.lean','actual_joint_block_rough_difference.header.lf.snapshot.lean','actual_sharp_endpoint_zero_gradient.header.lf.snapshot.lean','production.header.seal.normalized.lf.snapshot.lean']:take(B/'source-review56'/n)
notes=json.loads((B/'integration.notes.json').read_bytes()); checks=[]
for q in notes['checks']:
    actual=pin(q['path']); assert all(actual[k]==q[k] for k in ['bytes','raw_sha256','lf_sha256']),q['path'];take(q['path'])
for p in sorted(B.glob('integration.0.*.status.json')):
    j=json.loads(p.read_bytes()); assert j['exit_code']==0 and j['proof_commit']==SCI
    lp=Path(str(p).replace('.status.json','.log'));assert sha(lp.read_bytes())==j['log_raw_sha256']
    checks.append({'name':p.name,'status':pin(p),'log':pin(lp),'exit_code':0})
assert len(checks)==12
lease=json.loads((B/'root.integration.0.lease.json').read_bytes());assert lease['status']=='CLOSED' and lease['exit_code']==0
images=[]
for p in sorted((B/'visual-inspection56').iterdir()):
    take(p)
    if p.suffix=='.png':
        raw=p.read_bytes();assert raw[:8]==b'\x89PNG\r\n\x1a\n'; dims=struct.unpack('>II',raw[16:24]);assert dims==(1440,1800)
        images.append({'pin':pin(p),'width':dims[0],'height':dims[1],'independently_viewed_via_tool':'view_image original pixel resolution','visual_assessment':'Current reviewer actually viewed all four images before this sealing script; not inferred from root prose.'})
assert len(images)==4
vis=json.loads((B/'visual.inspection.json').read_bytes())
# All root visual receipt pins are checked recursively where a real file receipt appears.
def validate_embedded(j):
    if isinstance(j,dict):
        if 'path' in j and 'raw_sha256' in j and 'bytes' in j:
            a=pin(j['path']);assert a['bytes']==j['bytes'] and a['raw_sha256']==j['raw_sha256'];
            if 'lf_sha256' in j:assert a['lf_sha256']==j['lf_sha256']
        for x in j.values():validate_embedded(x)
    elif isinstance(j,list):
        for x in j:validate_embedded(x)
validate_embedded(vis)
captures=[]
for n in ['cdp.capture.json','proof.capture.json']:
    j=json.loads((B/'visual-inspection56'/n).read_bytes());captures.append({'path':n,'native':j})
def git(*args):
    r=subprocess.run(['git',*args],cwd=ROOT,capture_output=True);assert r.returncode==0,(args,r.stderr.decode(errors='replace'));return r.stdout
assert git('rev-parse','HEAD').decode().strip()==HEAD
git('merge-base','--is-ancestor',SCI,HEAD)
git_evidence=[]
for f in ['AutoSamplingTheory/ExampleCases/ProximalBPS/RoughMeanGradient.lean','Tests/ProximalBPSRoughMeanGradient.lean']:
    a=git('show',SCI+':'+f);b=git('show',HEAD+':'+f);c=(ROOT/f).read_bytes();assert a==b and a.replace(b'\r\n',b'\n')==c.replace(b'\r\n',b'\n')
    (OUT/(Path(f).name+'.science.raw.snapshot')).write_bytes(a)
    git_evidence.append({'path':f,'science_git_blob_sha256':sha(a),'integration_git_blob_sha256':sha(b),'worktree':pin(f),'science_to_integration_unchanged':True})
publication=json.loads((ROOT/'website/content/publications/pbps-rough-mean-gradient.json').read_bytes())['items'][0]
lesson=json.loads((ROOT/'website/content/declaration_lessons/pbps-rough-mean-gradient.json').read_bytes())['units'][0]
audit=json.loads((ROOT/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261008-PBPSRoughMeanGradient.json').read_bytes())
assert publication['statement']==lesson['statement'] and len(lesson['steps'])==6
assert audit['source_review']['state']=='accepted'
assert audit['publication_binding_sha256']=='fd5daf2f98df6433cbc40d33437826e256e1af0bf261d7fffa818292b03dbc5b'
lean=(ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/RoughMeanGradient.lean').read_text(encoding='utf8');a=lean.index('theorem actual_rough_mean_gradient');b=lean.index(' := by',a);signature=(lean[a:b].rstrip()+'\n').encode('utf8');assert len(signature)==1755 and sha(signature)=='fea2c3ade170bc0526d659f8c51abedaa0ce1a6186e75f0d8a2532b6608e94d8'
(OUT/'production.header.normalized.lf.snapshot.lean').write_bytes(signature)
htmlpath=ROOT/'_site/example-cases/samplewiki/companions/proximal-bouncy-particle.html';raw=htmlpath.read_bytes();s=raw.decode('utf8');start=s.index('<section id="pbps-rough-mean-gradient"');depth=0
for m in re.finditer(r'</?section\b[^>]*>',s[start:]):
    depth+=-1 if m.group().startswith('</') else 1
    if depth==0:end=start+m.end();break
node=s[start:end];(OUT/'rendered.companion.node.raw.snapshot.html').write_bytes(node.encode('utf8'))
class Inspect(HTMLParser):
    def __init__(self):super().__init__();self.classes={};self.details=[];self.codes=[];self.active=False;self.buf=[]
    def handle_starttag(self,t,attrs):
        q=dict(attrs)
        for c in q.get('class','').split():self.classes[c]=self.classes.get(c,0)+1
        if t=='details':self.details.append(q)
        if t=='code' and q.get('class')=='language-lean':self.active=True;self.buf=[]
    def handle_data(self,x):
        if self.active:self.buf.append(x)
    def handle_endtag(self,t):
        if t=='code' and self.active:self.codes.append(''.join(self.buf));self.active=False
p=Inspect();p.feed(node);assert len(p.details)==11 and all('open' not in d for d in p.details)
assert p.classes['proof-reader-equation']==8 and p.classes['proof-reader-step']==6 and len(p.codes)==2
assert p.codes[0].strip()==lean[a:b].strip() and p.codes[1].strip()==lean[a:].strip()
for i,c in enumerate(p.codes):(OUT/f'rendered.exact-lean-{i}.lf.snapshot.lean').write_bytes((c+'\n').encode('utf8'))
for step in lesson['steps']:assert step['title'] in node
site_graph=ROOT/'_site/data/underlying-lean-graph.json';g=json.loads(site_graph.read_bytes());focus='decl:AutoSamplingTheory.ExampleCases.ProximalBPS.RoughMeanGradient.actual_rough_mean_gradient';module='module:AutoSamplingTheory.ExampleCases.ProximalBPS.RoughMeanGradient'
edges=[e for e in g['edges'] if focus in (e['source'],e['target']) or module in (e['source'],e['target'])];ids={focus,module}
for e in edges:ids.update((e['source'],e['target']))
nodes=[n for n in g['nodes'] if n['id'] in ids]
slicej={'schema_version':1,'focus':focus,'module':module,'nodes':nodes,'edges':edges,'reference_contract':g['reference_contract'],'upstream_container':pin(site_graph),'slice_rule':'All edges incident to the exact declaration or its owner module, with their endpoint nodes; no adjacency inferred.'}
write('rendered.graph-focus.slice.json',slicej)
take(ROOT/'_site/lean-foundations.html')
sitepins={'companion_container':pin(htmlpath),'selected_section_utf8_character_offsets':[start,end],'selected_section':pin(OUT/'rendered.companion.node.raw.snapshot.html'),'graph_container':pin(site_graph),'graph_slice':pin(OUT/'rendered.graph-focus.slice.json'),'mutable_generated_site':'Containers pinned at actual read time; exact bounded node and focus slice saved. No whole-site inspection or live/main claim.'}
write('verification.json',{'schema_version':1,'git':{'science_commit':SCI,'integration_commit':HEAD,'ancestor_exit_code':0,'science_files':git_evidence},'checks':checks,'registry_count_reported_in_native_integration':notes['registry_count'],'root_jobs_reported':notes['root_jobs'],'tests_jobs_reported':notes['test_jobs'],'root_resource_lease':pin(B/'root.integration.0.lease.json'),'site':sitepins,'rendered':{'formula_containers':8,'steps':6,'details_closed':11,'closed_lean_step_details':6,'closed_exact_lean_details':2,'closed_ledger_details':3,'folded_statement_exact':True,'folded_full_theorem_proof_exact':True,'signature_utf8_lf_bytes':1755,'signature_sha256':sha(signature)},'images':images,'captures':captures,'limitations':'Existing check receipts independently verified, no compiler rerun. 11 closed details includes 3 reader ledgers, not 11 Lean proof blocks.'})
history=['Original creator CLOSED then changed three outputs; originals restored byte-exact from actual before snapshots, historical mutation retained.','Strict provider-body blindness false after original primary graph freeze; earlier overwritten context fragment survives only transcript.','Final56 source packet exposes complete candidate body; strict final body blindness false. Source-primary, StatementSeal and repaired topology predate implementation.','Original decoder six locator objects malformed; independent distinct operational repair accepted without rewriting/reclosing originals. Strict decoder identity blindness not asserted.','No candidate57 body or sourcegraph57 read in this scoped ExpositionSeal.']
report={'schema_version':1,'artifact_kind':'independent-scoped-exposition-seal','reviewer':'/root/next_primary56','independent_from_proving_writer':True,'verdict':'ACCEPT_SCOPED_DESKTOP_EXPOSITION_WITH_RETAINED_DEBT','blockers':[],'scope':'Only actual all-L2 closed compact-gradient image/sharp energy source edge, local 1440x1800 desktop companion node and exact graph focus at pinned integration HEAD; not PURIFIED/full reader/mobile/main/live.','science_commit':SCI,'integration_commit':HEAD,'publication_binding_sha256':audit['publication_binding_sha256'],'statement_signature_sha256':sha(signature),'source_review_reused':pin(B/'source-review56/result0.json'),'source_nodes':['PBPS2609.06905v1 C.1 dense compact-gradient/closedness passage','PBPS2609.06905v1 C.2 sharp coefficient estimate toward B.13','Own primary56 source-only sealed contract'], 'lean_nodes':{'target':focus,'parents':publication['proof_digestion']['existing_substrate'],'tests':['Tests.ProximalBPSRoughMeanGradient.actual_joint_block_rough_difference','Tests.ProximalBPSRoughMeanGradient.actual_sharp_endpoint_zero_gradient']},'lossless_expansion':{'original_assumptions':'C2 V, 0<alpha<=beta, global lower and upper Hessian bounds, eta>0 betaeta<=1; actual mu=tilted(-V), J=law(X,X+sqrt eta Z), nu=J.snd, literal every-y reflected S tilt.','quantifiers':'One exact dense closable compact-gradient G with closed closure and bounded linear T,K chosen before ALL arbitrary real L2(nu) AE classes. Actual(Tu,Ku) in Gbar graph; rough mean/fiber u and square L1 only AE nu.','finite_hilbert':'Finite real Hilbert/Borel with canonical volume and rank zero explicitly extends source Euclidean setting; disclosed, not a source assumption silently added.','constants':'c=(1-alpha eta)^2/[4(1+alpha eta)]; eta||Ku||^2<=c(||u||^2-||Tu||^2), source4eta. alpha eta1 allowed, no division by1-alpha eta.','six_steps':[{'number':i+1,'title':s['title'],'formula':s['formula'],'expand_to':s['lean']} for i,s in enumerate(lesson['steps'])],'compact_support':'Compact core input mean need not be compact. Actual same weighted-gradient closure admission precedes dense extension.','consumer':'Step6 identifies SAME T with actual joint parent by AE conditional mean uniqueness and yields BM(u-v) defect; endpoint forces entire K=0 with actual closed pair.','folding':'8 formula containers; six corresponding Lean-step details plus exact statement and exact full theorem/proof code, all folded initially; three additional folded reader ledgers. Code text matches current science bytes after only boundary whitespace normalization.'},'semantic_deltas':[{'kind':'disclosed-background-extension','detail':'finiteHilbert/Borel/rank0'},{'kind':'explicit-scoped-claim','detail':'compact-gradient closure; separately defined weak-H1 equivalence/full B13 not asserted'},{'kind':'notation-disambiguation','detail':'candidate S_y literal reflected law; source S_source residual block distinct'}],'graph_assessment':'Solid imports/module ownership distinguish compiled topology. Dashed name-scan reference list explicitly incomplete: three real parent names are present, incidental LogConcaveOn.prod remains scanner debt, not certified new dependency. Qualified labels wrap densely.','presentation_debt':[{'kind':'main-formula-horizontal-scroll','severity':'nonblocking-for-this-scoped-seal','detail':'Combined main formula exceeds desktop formula viewport; right end requires horizontal scroll. Six proof-step formulas including Step6 fit 1440 px.'},{'kind':'repeated-title-and-statement','severity':'nonblocking','detail':'Publication and lesson repeat title/statement and main formula.'},{'kind':'dense-inline-ascii-and-anchors','severity':'nonblocking','detail':'C2/L2/source/AE inline technical notation and long anchors need polish for broad readers.'},{'kind':'long-companion-page','severity':'reader-backpressure-debt','detail':'Actual bodyHeight319496; this seal inspected only bounded node/captures.'},{'kind':'wrapped-graph-labels-and-scan-noise','severity':'nonblocking','detail':'Qualified labels wrap; incidental LogConcaveOn.prod and incomplete namescan remain explicit.'}], 'remaining_boundary':['Separate weak-H1 equivalence','Full B13/Gamma defect-root inverse/halfturn','Dynamics/mixing/main theorem','Error/cost and actual-input composition','Full reader/mobile/live/main and postmerge purification'], 'historical_negatives':history,'compiler':'NOT_STARTED_CLOSED','repairs':[]}
write('exposition.review.json',report)
write('input.manifest.json',{'schema_version':1,'artifact_kind':'native-exact-raw-and-crlf-to-lf-input-manifest','inputs':inputs,'receipt_recipe':'SHA256(actual raw bytes); LF recipe replaces only CRLF with LF, no JSON reserialization. Input .raw/.lf snapshots read back byte-exact. Self field hashes complete object excluding only complete_object_sha256.'})
readbacks=[]
for q in inputs:
    actual=pin(q['path']);assert actual==q;readbacks.append(actual)
write('input.readbacks.json',{'schema_version':1,'count':len(readbacks),'all_match':True,'pins':readbacks})
print(json.dumps({'stage':'PREPARED','pid':os.getpid(),'input_count':len(inputs),'checks':len(checks),'images':len(images),'node_bytes':len(node.encode('utf8')),'graph_nodes':len(nodes),'graph_edges':len(edges),'verdict':report['verdict'],'process_expected_exit_code':0},ensure_ascii=False))
