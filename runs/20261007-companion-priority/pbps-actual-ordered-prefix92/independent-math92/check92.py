import pathlib,json,hashlib,re,subprocess,time
from datetime import datetime,timezone
R=pathlib.Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-actual-ordered-prefix92';D=B/'independent-math92'
def bind(p):
 b=p.read_bytes();return dict(path=p.as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def put(n,v):
 with (D/n).open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
src=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualOrderedPrefix.lean';raw=src.read_bytes();assert bind(src)['raw_sha256']=='46c637205d601786472e789bf4706a77b18ea6dad423ab33d1ac39491e71e111';s=raw.decode('utf-8').replace('\r\n','\n')
seal=json.loads((B/'root.statement-seal92.json').read_text(encoding='utf-8'))['expanded_literal_Prop'];statement=s.split('def actual_ordered_prefix_statement',1)[1].split('set_option maxHeartbeats',1)[0]
norm=lambda x:re.sub(r'\s+',' ',x).strip()
assert norm(statement)==norm(seal)
prototype=(B/'Complete92.lean').read_text(encoding='utf-8');assert bind(B/'Complete92.lean')['raw_sha256']=='66d6c6029beae874ada32d7e011de7731ee0bd22124fbd84ee4cd5ba9323a400'
ns='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualOrderedPrefix'
def body(text):return norm(text[text.index('private theorem measurable_cons_zero'):].replace(ns,'OrderedComplete92'))
assert body(s)==body(prototype)
ind=(B/'Induction92.lean').read_text(encoding='utf-8');indbody=ind[ind.index('private theorem measurable_cons_zero'):ind.rindex('\nend\n')].strip()
prodbody=s[s.index('private theorem measurable_cons_zero'):s.index('private theorem law_and_mass_of_all_tests')].strip()
assert norm(prodbody.replace(ns,'OrderedInduction92'))==norm(indbody)
closure=(B/'MeasureClosure92.lean').read_text(encoding='utf-8');oldclosure=closure[closure.index('private theorem law_and_mass_of_all_tests'):closure.index('\nend\n')].strip()
newclosure=s[s.index('private theorem law_and_mass_of_all_tests'):s.index('def actual_ordered_prefix_statement')].strip()
assert norm(newclosure)==norm(oldclosure)
clean=re.sub(r'/\-[\s\S]*?\-/','',s);assert not re.search(r'\b(?:sorry|admit|axiom)\b|Prop\s*:=\s*True|:=\s*trivial',clean)
put('static-check92.native.json',dict(source=bind(src),seal=bind(B/'root.statement-seal92.json'),exact_expanded_statement_match=True,prototype_namespace_only_match=True,all_induction_body_preserved=True,measure_closure_body_preserved=True,fake_closure_scan='PASS',checked_base_HEAD=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()))
old=R/'runs/20261007-companion-priority/pbps-actual-absolute-next-event-time91/independent-math91/FreshWholeSourceKernelClosure91.lean';suffix=old.read_text(encoding='utf-8').split('set_option pp.universes true',1)[1];suffix='\nset_option pp.universes true'+suffix;suffix=suffix.replace('ActualAbsoluteNextEventTime','ActualOrderedPrefix').replace('actual_absolute_next_event_time','actual_ordered_prefix')
copy=D/'FreshWholeSourceKernel92.lean'
with copy.open('xb') as f:f.write(raw+suffix.encode('utf-8'))
argv=[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env','lean',str(copy.relative_to(R))];start=time.monotonic()
with (D/'kernel.stdout.log').open('xb') as out,(D/'kernel.stderr.log').open('xb') as err:result=subprocess.run(argv,cwd=R,stdout=out,stderr=err)
receipt=dict(argv=argv,cwd=R.as_posix(),exit_code=result.returncode,duration_seconds=time.monotonic()-start,finished_utc=datetime.now(timezone.utc).isoformat(),terminal_closed=True,source=bind(src),copy=bind(copy),lake_manifest=bind(R/'lake-manifest.json'),stdout=bind(D/'kernel.stdout.log'),stderr=bind(D/'kernel.stderr.log'))
put('kernel.receipt.native.json',receipt);print(json.dumps(receipt,indent=2));raise SystemExit(result.returncode)
