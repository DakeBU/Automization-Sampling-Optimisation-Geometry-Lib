import hashlib,json,pathlib,re,subprocess,time
from datetime import datetime,timezone
R=pathlib.Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-actual-ordered-prefix92';D=B/'independent-all-n-fragment92'
def bind(p):
 b=p.read_bytes();return dict(path=p.as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
source=B/'Induction92.lean';raw=source.read_bytes();assert bind(source)['raw_sha256']=='c1a5bcd005361d8d3ee9964adcaaa550507966ad7d7b35f7ab414b615d06f6b6'
def declarations(text):
 matches=list(re.finditer(r'^(?:set_option maxHeartbeats \d+ in\n)?private (?:def|theorem) (\w+)',text,re.M));result={}
 for i,m in enumerate(matches):
  end=matches[i+1].start() if i+1<len(matches) else text.index('\nend\n',m.start())
  result[m.group(1)]=text[m.start():end].strip()
 return result
def normalized(s):
 s=re.sub(r'Ordered(?:Prefix|Base|Integral|Subtype|Algebra|Induction)92\.', 'NAMESPACE.',s)
 return re.sub(r'\s+',' ',s).strip()
current=declarations(raw.decode('utf-8').replace('\r\n','\n'));prior={}
parents=['Geometry92','Base92','Integrals92','SubtypeCoordinates92','Algebra92']
for name in parents:
 for n,v in declarations((B/(name+'.lean')).read_text(encoding='utf-8')).items():prior.setdefault(n,[]).append((name,v))
matches=[];mismatches=[]
for n,v in current.items():
 if n=='actual_prefix_all_integrals':continue
 found=[name for name,old in prior.get(n,[]) if normalized(old)==normalized(v)]
 (matches if found else mismatches).append({'declaration':n,'matching_source_fragments':found})
merge=dict(normalization='Whitespace and namespace qualification only; no mathematical tokens removed.',retained=matches,mismatches=mismatches,new_declaration='actual_prefix_all_integrals',parents=[bind(B/(name+'.lean')) for name in parents])
with (D/'merge-check92.json').open('x',encoding='utf-8') as f:json.dump(merge,f,indent=2)
assert not mismatches,mismatches
copy=D/'FreshAllNKernel92.lean';suffix=b'\nset_option pp.deepTerms true\n#check @OrderedInduction92.actual_prefix_all_integrals\n#print axioms OrderedInduction92.actual_prefix_all_integrals\n'
with copy.open('xb') as f:f.write(raw+suffix)
argv=[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env','lean',str(copy.relative_to(R))];start=time.monotonic()
with (D/'kernel.stdout.log').open('xb') as out,(D/'kernel.stderr.log').open('xb') as err:result=subprocess.run(argv,cwd=R,stdout=out,stderr=err)
receipt=dict(argv=argv,cwd=R.as_posix(),exit_code=result.returncode,duration_seconds=time.monotonic()-start,finished_utc=datetime.now(timezone.utc).isoformat(),terminal_closed=True,source=bind(source),copy=bind(copy),merge_check=bind(D/'merge-check92.json'),lake_manifest=bind(R/'lake-manifest.json'),stdout=bind(D/'kernel.stdout.log'),stderr=bind(D/'kernel.stderr.log'),scope='Actual all-n strict-prefix ENNReal integral theorem only; no fullA7 or canonical verification.')
with (D/'kernel.receipt.json').open('x',encoding='utf-8') as f:json.dump(receipt,f,indent=2)
print(json.dumps(receipt,indent=2));raise SystemExit(result.returncode)
