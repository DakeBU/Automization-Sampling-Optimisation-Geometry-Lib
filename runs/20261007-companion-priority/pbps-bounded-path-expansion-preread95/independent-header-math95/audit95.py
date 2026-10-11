import pathlib,json,hashlib,re,subprocess
ROOT=pathlib.Path('E:/Samplinglib'); OUT=pathlib.Path(__file__).resolve().parent
HEADER=OUT.parent/'Header95.lean'
def sha(b):return hashlib.sha256(b).hexdigest()
def norm(b):return b.decode('utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def compact(s):return re.sub(r'\s+','',s)
def save(p,v):(OUT/p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
inputs=[]
def read(p):
 p=pathlib.Path(p);p=p if p.is_absolute() else ROOT/p;b=p.read_bytes();inputs.append({'path':p.relative_to(ROOT).as_posix(),'raw_sha256':sha(b),'bytes':len(b)});return b
header=read(HEADER);(OUT/'Header95.exactraw.snapshot').write_bytes(header)
p93='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteCountPath.lean';p94='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPrescribedPathDensity.lean'
b93=read(p93);b94=read(p94);h=norm(header);s93=norm(b93);s94=norm(b94)
def lets(s):
 matches=list(re.finditer(r'^    let (\S+)',s,re.M));d={}
 for i,m in enumerate(matches):
  end=matches[i+1].start() if i+1<len(matches) else s.index('    ∃ Z',m.start())
  d[m.group(1)]=s[m.start():end].strip()
 return d
# The accepted93 private literal statement and public body duplicate the same lets.
s93=s93[s93.index('private def actual_finite_count_path_law_statement'):] if 'private def actual_finite_count_path_law_statement' in s93 else s93[s93.index('    let c : E → E → E :='):]
s93=s93[:s93.index('    ∃ Z')]
def decls(s):
 ms=list(re.finditer(r'^    let (\S+)',s,re.M));return {m.group(1):s[m.start():ms[i+1].start() if i+1<len(ms) else len(s)].strip() for i,m in enumerate(ms)}
hlets=decls(h[h.index('    let c :'):h.index('    ∃ Z')]);l93=decls(s93)
comparisons={k:compact(v)==compact(l93[k]) for k,v in hlets.items() if k!='wgt'}
start='    ∃ Z :';end='      (∀ y xRef : E, ∀ z₀ : E × E, ∀ T : ℝ≥0,'
z95=h[h.index(start):h.index(end)]
full93=norm(b93);z93=full93[full93.index(start):];z93=z93[:z93.index('      (∀ n : ℕ, ∀ T : ℝ≥0,')]
check={'inherited_let_definitions_whitespace_equivalent':comparisons,'same_measurable_Z_raw_arcs_fallback_fixed_parameter_AE0':compact(z95)==compact(z93),'candidate_contains_exact_six_hypotheses':all(x in h for x in ['(hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)','(hH : ∀ x v : E,','(hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1)']),'production93_raw_sha256':sha(b93),'production94_raw_sha256':sha(b94),'candidate_raw_sha256':sha(header)}
assert all(comparisons.values()) and check['same_measurable_Z_raw_arcs_fallback_fixed_parameter_AE0']
run94=ROOT/'runs/20261007-companion-priority/pbps-actual-prescribed-path-density94'
for suffix in ['checks94/header95-type-only/receipt.json','checks94/header95-type-only/stdout.log','checks94/header95-type-only/stderr.log','independent-whole-math94/whole-math-decision94.native.json','independent-whole-math94/lf-transfer94/LF-transfer-decision94.native.json','exact-commit-verification94/verified.json']:
 read(run94/suffix)
read('lean-toolchain');read('lake-manifest.json')
save('literal-interface-comparison.native.json',check);save('inputs.native.json',inputs)
print(json.dumps(check,ensure_ascii=False,indent=2))
