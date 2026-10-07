from pathlib import Path
import json,hashlib,re,subprocess,datetime
p=Path('.astis/gaussian-entropy33');sig=p/'source.signature.txt'
b=sig.read_bytes();s=b.replace(b'\r\n',b'\n').decode('utf-8')
body=re.sub(r'^theorem\s+\w+\s*\n','',s,count=1)
binders,conclusion=body.rsplit(' :\n',1)
probe=p/'StatementTypeProbe.lean';assert not probe.exists()
probe.write_text('import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.StandardizedRGOSqrtDensity\nimport AutoSamplingTheory.TechnicalLemmas.InformationTheory.TiltedKL\nopen MeasureTheory InnerProductSpace ProbabilityTheory\nopen scoped RealInnerProductSpace NNReal ENNReal\nnoncomputable section\n\n#check (∀ '+binders.lstrip()+',\n'+conclusion.rstrip()+'\n)\n',encoding='utf-8')
log=p/'root.statement-typecheck.0.log';record=p/'root.statement-typecheck.0.json';assert not log.exists()and not record.exists()
with log.open('wb')as out:result=subprocess.run(['lake','env','lean',probe.as_posix()],stdout=out,stderr=subprocess.STDOUT)
record.write_text(json.dumps(dict(schema_version=1,status='type-elaboration-pass'if result.returncode==0 else'type-elaboration-failed',exit_code=result.returncode,command=['lake','env','lean',probe.as_posix()],signature_raw_sha256=hashlib.sha256(b).hexdigest(),signature_lf_sha256=hashlib.sha256(s.encode()).hexdigest(),probe_path=probe.as_posix(),probe_raw_sha256=hashlib.sha256(probe.read_bytes()).hexdigest(),log_path=log.as_posix(),log_raw_sha256=hashlib.sha256(log.read_bytes()).hexdigest(),transformation='Remove only theorem/name header and replace declaration colon by forall comma; no theorem body/placeholder/search.',proof_search_or_theorem_bodies=False,production_edits=False,compiler_lease='CLOSED',closed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=2)+'\n',encoding='utf-8')
print('type-only PASS'if result.returncode==0 else log.read_text(encoding='utf-8')[-6000:])
raise SystemExit(result.returncode)
