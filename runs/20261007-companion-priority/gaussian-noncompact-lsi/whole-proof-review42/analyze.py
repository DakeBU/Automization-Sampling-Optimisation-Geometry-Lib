import collections,hashlib,json,pathlib,re,subprocess
ROOT=pathlib.Path('E:/Samplinglib')
OUT=ROOT/'runs/20261007-companion-priority/gaussian-noncompact-lsi/whole-proof-review42'
def H(b):return hashlib.sha256(b).hexdigest()
def put(n,d):
 with (OUT/n).open('xb') as f:f.write((json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode())
rows=[]
for line in (OUT/'reachability.log').read_text(encoding='utf-8').splitlines():
 if line.startswith('ASTIS_REACHABLE|'):
  _,name,kind,deps=line.split('|',3);rows.append(dict(name=name,kind=kind,direct_local_constants=deps.split(';') if deps else []))
assert rows and len({x['name'] for x in rows})==len(rows)
names=[x['name'] for x in rows]
sources=subprocess.check_output(['rg','--files','AutoSamplingTheory','Tests'],cwd=str(ROOT)).decode().splitlines()
modules={p.replace('\\','/').removesuffix('.lean').replace('/','.'):p.replace('\\','/') for p in sources if p.endswith('.lean')} if hasattr(str,'removesuffix') else {p.replace('\\','/')[:-5].replace('/','.'):p.replace('\\','/') for p in sources if p.endswith('.lean')}
reached={};unmapped=[]
for row in rows:
 name=row['name'];part=name[name.find('AutoSamplingTheory.'):] if 'AutoSamplingTheory.' in name else name[name.find('Tests.'):]
 matches=[m for m in modules if part==m or part.startswith(m+'.')]
 if not matches:unmapped.append(name);continue
 m=max(matches,key=len);reached.setdefault(m,dict(path=modules[m],constants=[]))['constants'].append(name)
def strip(text):
 out=[];i=0;depth=0;string=False
 while i<len(text):
  c=text[i:i+2]
  if depth:
   if c=='/-':depth+=1;i+=2;continue
   if c=='-/':depth-=1;i+=2;continue
   out.append('\n' if text[i]=='\n' else ' ');i+=1;continue
  if string:
   if text[i]=='\\':out.extend('  ');i+=2;continue
   if text[i]=='"':string=False
   out.append('\n' if text[i]=='\n' else ' ');i+=1;continue
  if c=='/-':depth=1;out.extend('  ');i+=2;continue
  if c=='--':
   e=text.find('\n',i)
   if e<0:e=len(text)
   out.extend(' '*(e-i));i=e;continue
  if text[i]=='"':string=True;out.append(' ');i+=1;continue
  out.append(text[i]);i+=1
 return ''.join(out)
hits=[];patterns={'axiom-or-placeholder':r'\b(?:axiom|sorry|admit|sorryAx)\b','Prop-True':r'\bProp\s*:=\s*True\b','trivial-closure':r':=\s*trivial\b'}
for m,d in reached.items():
 p=ROOT/d['path'];raw=p.read_bytes();code=strip(raw.decode('utf-8'))
 d.update(raw_sha256=H(raw),lf_sha256=H(raw.replace(b'\r\n',b'\n')))
 for label,pat in patterns.items():
  for x in re.finditer(pat,code):hits.append(dict(path=d['path'],line=code[:x.start()].count('\n')+1,class_=label,token=x.group()))
axioms=[x for x in rows if x['kind']=='axiom']
allprivate=[x for x in names if '.GaussianLogSobolev.' in x and x.startswith('_private.')]
expected=['entropy_dilation_bound','gradient_mul','cutoff_energy_bound','cutoff_gradient_eventually_eq','cutoff_integral_limits']
private=[x for x in allprivate if any(x.endswith('.'+y) for y in expected)]
generated_aux=[x for x in allprivate if x not in private]
assert len(private)==5 and all(any(x.endswith('.'+y) for x in private) for y in expected)
source=(ROOT/'AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/GaussianLogSobolev.lean').read_text(encoding='utf-8')
sig=(ROOT/'runs/20261007-companion-priority/gaussian-noncompact-lsi-preproof42/signature.prospective.txt').read_bytes().replace(b'\r\n',b'\n')
public=source[source.index('theorem gaussian_logSobolev_of_contDiff'):];assert public.startswith(sig.decode().rstrip()+' := by')
assert len(re.findall(r'^private theorem ',source,re.M))==5
assert not unmapped and not hits and not axioms
direct=(OUT/'direct.log').read_text(encoding='utf-8');aset=re.findall(r"'([^']+)' depends on axioms: \[([^\]]+)\]",direct,re.S);assert len(aset)==4
for name,aa in aset:assert {x.strip() for x in aa.split(',')}=={'propext','Classical.choice','Quot.sound'}
reach=(OUT/'reachability.log').read_text(encoding='utf-8');assert reach.count('Declarations are sorry-free!')==2
assert '(Fin 0)' in (OUT/'ReachabilityProbe.lean').read_text()
put('reachability.analysis.json',dict(status='PASS',root_targets=4,compiled_reachable_ASTIS_Test_constants=len(rows),compiled_local_axiom_declarations=axioms,compiled_reachable_source_modules=len(reached),unmapped_constants=unmapped,fake_closure_hits=hits,public691_LF_signature_exact=True,public691_LF_sha256=H(sig),all5_new_private_providers_reachable=private,standard_axioms=[dict(declaration=n,axioms=[x.strip() for x in a.split(',')]) for n,a in aset],rank0_specialization_typecheck_pass=True,sorry_free_roots=2,scope='Actual compiled ASTIS/Test type/value expression-call closure, stops at Mathlib imports; root standard3 axioms cover transitive kernel axioms. Whole reached local source tokens scanned excluding nested comments/strings, not whole-site/global source scan.',compiled_rows=rows,reached_modules=reached,scan_patterns=patterns))
print(json.dumps(dict(reached_constants=len(rows),reached_local_modules=len(reached),private_providers=len(private),fake_hits=hits,local_axioms=axioms,signature691=True,standard3_sets=4)))
