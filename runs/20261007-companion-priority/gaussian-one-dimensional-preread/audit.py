from pathlib import Path
import json,hashlib,re,subprocess,sys,datetime
from html.parser import HTMLParser
R=Path('runs/20261007-companion-priority/gaussian-one-dimensional-preread')
UP=Path('runs/20261007-companion-priority/gaussian-functional-availability')
RD=Path('runs/20261007-companion-priority/gaussian-lsi-t2-readiness')
V='picard_commit_verifier_20261005'
def j(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
def desc(p):
 b=Path(p).read_bytes();return {'path':Path(p).as_posix(),'raw_sha256':sha(b),'lf_sha256':sha(b.replace(b'\r\n',b'\n')),'bytes':len(b)}
def write(p,x):Path(p).write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode())
assert not (R/'bounded-synthesis.json').exists()
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
write(R/'lease.open.json',{'status':'OPEN','actor':V,'base_head_observed':head,'read':'task-local-primary-and-API-audit','write':'this new run only','compiler':'NOT_REQUESTED','proof_search':False})
source=Path('runs/20261007-companion-priority/gaussian-transport-preread/source-primary.raw.snapshot.html')
assert desc(source)['raw_sha256']=='ec485cdad5fe140114be35eef93d19398e0cafcf21abb3fff1bdbbf462e5f94d'
raw=source.read_text(encoding='utf-8');lines=raw.splitlines(True);starts=[0]
for line in lines:starts.append(starts[-1]+len(line))
class Primary(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=False);self.stack=[];self.spans={}
 def offset(self):l,c=self.getpos();return starts[l-1]+c
 def handle_starttag(self,tag,attrs):
  if tag in {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}:return
  self.stack.append((tag,self.offset(),dict(attrs).get('id')))
 def handle_endtag(self,tag):
  for n in range(len(self.stack)-1,-1,-1):
   if self.stack[n][0]==tag:
    _,a,i=self.stack[n];self.stack=self.stack[:n]
    if i in {'S4.Ex8','S4.E6','S4.SS1.p4.2','S4.SS1.p4.3'}:self.spans[i]=(a,raw.find('>',self.offset())+1)
    break
p=Primary();p.feed(raw);assert len(p.spans)==4
primary=[]
for i,(a,b) in p.spans.items():
 frag=raw[a:b].encode();dst=R/('primary.'+i+'.raw.snapshot.html');dst.write_bytes(frag)
 primary.append({'id':i,'canonical_outer_fragment':desc(dst),'UTF8_start':len(raw[:a].encode()),'UTF8_end':len(raw[:b].encode()),'math_alttext':re.findall(r'alttext="([^"]+)"',frag.decode())})
write(R/'primary-api-read-order.json',{'primary_source':desc(source),'primary_outer_fragments':primary,'contract':'SPHMC v1 Lemma4.2 first4.6 invokes Gaussian LSI and Gaussian Talagrand independently; literal standardized law uses sqrt(eta) and arbitrary eta>0. Function LSI constant2 with actual32 energy Fisher/4 yields KL<=Fisher/2; no T2 conclusion from this audit.','exposure':'Read CLOSED readiness/minimal packet as pointers and primary observed-text before upstream bodies; exact raw MathML/outer fragments independently rechecked during this audit. No new anti-anchored source verdict or graph selfvalidation is produced.'})
local=[
 'AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/LogSobolev.lean',
 'AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/CanonicalLogSobolev.lean',
 'AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/WeightedC1GradientDomain.lean',
 'AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/CompactC1GradientDomain.lean',
 'AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/WeightedGradient.lean',
 'AutoSamplingTheory/TechnicalLemmas/Analysis/Calculus/Cutoff.lean',
 'AutoSamplingTheory/TechnicalLemmas/Measure/Product.lean',
 'AutoSamplingTheory/TechnicalLemmas/Measure/GaussianSqrtDensityDomain.lean',
 'AutoSamplingTheory/ExampleCases/SmoothedPicardHMC/StandardizedRGOSqrtDensity.lean',
 'AutoSamplingTheory/TechnicalLemmas/Probability/StdGaussianMoment.lean',
 'AutoSamplingTheory/TechnicalLemmas/InformationTheory/TiltedKL.lean',
 'AutoSamplingTheory/TechnicalLemmas/Measure/IsotropicGaussianDensity.lean',
 '.lake/packages/mathlib/Mathlib/Probability/CentralLimitTheorem.lean',
 '.lake/packages/mathlib/Mathlib/Probability/Distributions/Gaussian/Basic.lean',
 '.lake/packages/mathlib/Mathlib/Probability/Distributions/Gaussian/Multivariate.lean',
 '.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/LevyConvergence.lean',
 '.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/ProbabilityMeasure.lean',
 '.lake/packages/mathlib/Mathlib/Analysis/SpecialFunctions/Log/NegMulLog.lean',
 'lean-toolchain','lake-manifest.json']
ref=j(RD/'upstream-reference.receipt.json');assert ref['revision']=='d0f506f0a695018265dccb33bcb05e2f5ca1c876'
fetch=j(UP/'upstream-fetch.json');external=[]
closure=ref['static_import_closures']['SLT/GaussianLSI/OneDimGLSICompSmo.lean']
for name in closure+['SLT/GaussianSobolevDense/Defs.lean','SLT/GaussianSobolevDense/Density.lean','SLT/GaussianLSI/OneDimGLSI.lean','LICENSE','lean-toolchain','lake-manifest.json']:
 rec=next(x for x in fetch['files'] if x['path']==name)
 path=Path(rec['local_snapshot']);assert desc(path)['raw_sha256']==rec['raw_sha256']
 external.append({**desc(path),'upstream_path':name,'pinned_url':rec['url']});local.append(path.as_posix())
local.extend([source.as_posix(),(RD/'audit.packet.json').as_posix(),(RD/'minimal-producer.packet.json').as_posix(),(RD/'upstream-reference.receipt.json').as_posix(),(UP/'upstream-fetch.json').as_posix()])
inputs=[]
for n,path in enumerate(dict.fromkeys(local)):
 before=desc(path);snapshot=R/('input.'+str(n).zfill(2)+'.raw.snapshot');snapshot.write_bytes(Path(path).read_bytes())
 inputs.append({**before,'snapshot':snapshot.as_posix()})
sys.path.insert(0,'tools');import astis
scans=[]
for rec in external:
 if not rec['upstream_path'].endswith('.lean'):continue
 text=Path(rec['path']).read_text(encoding='utf-8');clean=astis.strip_lean_comments_and_strings(text)
 hits=[{'line':i,'text':x.strip()} for i,x in enumerate(clean.splitlines(),1) if astis.FORBIDDEN_REGEX.search(x)]
 scans.append({'upstream_path':rec['upstream_path'],'input':rec,'direct_placeholder_hits':hits,'imports':re.findall(r'^(?:public )?import\s+([\w.]+)',text,re.M)})
assert all(not x['direct_placeholder_hits'] for x in scans)
searches=[]
for args in [
 ['rg','-n','entropy_subadd|entropy_chain|twoPoint|rothaus|han_inequality|bernoulli_logSobolev|gaussian_logSobolev','AutoSamplingTheory/TechnicalLemmas','--glob','*.lean'],
 ['rg','-n','-i','log.?sobolev|gaussian.*entropy|entropy.*gaussian','.lake/packages/mathlib/Mathlib','--glob','*.lean'],
 ['rg','-n','tendsto_iff_tendsto_charFun|tendsto_iff_forall_integral_tendsto','.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/LevyConvergence.lean','.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/ProbabilityMeasure.lean'],
 ['rg','-n','negMulLog_le_one_sub_self|negMulLog_nonneg|continuous_mul_log','.lake/packages/mathlib/Mathlib/Analysis/SpecialFunctions/Log/NegMulLog.lean']]:
 q=subprocess.run(args,capture_output=True);name=R/('search.'+str(len(searches))+'.raw.log');name.write_bytes(q.stdout+q.stderr)
 searches.append({'command':args,'exit_code':q.returncode,'raw_log':desc(name)})
write(R/'raw-source-API-evidence.json',{'status':'reference-and-local-API-inventory-only','ASTIS_Lean':'leanprover/lean4:v4.33.0','ASTIS_Mathlib':next(x for x in j('lake-manifest.json')['packages'] if x['name']=='mathlib')['rev'],'upstream_revision':ref['revision'],'upstream_Lean':ref['Lean'],'upstream_Mathlib':ref['Mathlib'],'license':'Apache-2.0 exact pinned LICENSE snapshot','external_inputs':external,'external_direct_and_transitive_import_scope':closure,'static_scan':scans,'actual_commands':searches,'compiler_started':False,'upstream_compilation_and_axiom_certificate':False,'local_producer_absence_scope':'Bounded name/semantic search; not exhaustive absence proof.'})
write(R/'input-inventory.json',{'inputs':inputs,'raw_LF_distinct':True,'compiler_started':False,'preserved_current33':True})
for rec in inputs:
 assert desc(rec['path'])['raw_sha256']==rec['raw_sha256'],rec['path']
print(json.dumps({'base_head_observed':head,'input_count':len(inputs),'external_static_Lean_files_scanned':len(scans),'placeholder_hits':0,'primary_fragments':len(primary),'compiler_started':False},ensure_ascii=False))
