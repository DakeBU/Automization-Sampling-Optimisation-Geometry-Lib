from pathlib import Path
import sys,json,hashlib,gzip,subprocess
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent.relative_to(Path.cwd());E=Path('research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-target-law-semantic-evidence');R=Path('.astis/huanjian-resume-20261103')
sha=lambda b:hashlib.sha256(b).hexdigest();dump=lambda x:(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
candidate='8ee639d3aced826aa5b4e39fa6f8bedd3b830327'
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==candidate and not (W/'accepted-review-metadata-commit.json').exists()
gate_stems=['20261110T115103708723Z-target-law-reviewed-publication','20261110T115103709749Z-target-law-reviewed-semantic','20261110T115103708822Z-target-law-reviewed-frontier','20261110T115103708751Z-target-law-reviewed-contributor']
gates=[]
for stem in gate_stems:
    p=R/(stem+'.receipt.json');x=json.loads(p.read_bytes());assert x['exit_code']==0 and x['head_before']==candidate and x['head_after']==candidate and sha(Path(x['log']).read_bytes())==x['log_sha256'];gates.append(x)
d=E/'actual-review-layer-checks';assert not d.exists();d.mkdir()
for p in sorted(R.glob('*target-law*.receipt.json')):
    x=json.loads(p.read_bytes())
    if x['head_before']!=candidate:continue
    b=Path(x['log']).read_bytes();assert sha(b)==x['log_sha256'];(d/p.name).write_bytes(p.read_bytes());(d/(p.stem+'.log.gz')).write_bytes(gzip.compress(b,mtime=0))
for n in ['package_independent_native.py','apply_independent_reviews.py','create_review_metadata_carrier.py']:
    p=E/'root-local-process-scripts'/n;assert not p.exists();p.write_bytes((W/n).read_bytes())
ap=Path('research-wiki/semantic-roundtrip/audits/huanjian-fixed-spectrum-target-law.json');cp=Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-target-law.json')
assert json.loads(ap.read_bytes())['state']=='source-reviewed'
for n in ['AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumTargetLaw.lean','Tests/GaussianComplexityFixedSpectrumTargetLaw.lean','website/content/declaration_lessons/huanjian-fixed-spectrum-target-law.json','website/content/publications/huanjian-fixed-spectrum-target-law.json','lake-manifest.json','lean-toolchain']:
    assert Path(n).read_bytes()==subprocess.check_output(['git','show',candidate+':'+n]),n
paths=sorted([ap,cp]+[p for p in E.rglob('*') if p.is_file()]);raws={str(p):p.read_bytes() for p in paths}
assert not subprocess.check_output(['git','diff','--cached','--name-only'])
subprocess.run(['git','add','--']+list(raws),check=True)
staged=set(subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines());assert staged<=set(raws)
assert {'research-wiki/semantic-roundtrip/audits/huanjian-fixed-spectrum-target-law.json',str(cp)}<=staged
assert all(n.startswith(str(E)+'/') or n in [str(ap),str(cp)] for n in staged)
for n in staged:assert subprocess.check_output(['git','show',':'+n])==raws[n],n
subprocess.run(['git','diff','--cached','--check'],check=True)
subprocess.run(['git','commit','-m','Bind independent source native and reader reviews for Gaussian target law'],check=True)
commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
for n,b in raws.items():assert subprocess.check_output(['git','show',commit+':'+n])==b,n
x={'accepted_review_metadata_carrier_commit':commit,'mathematical_native_checked_commit':candidate,'sourceP_Test_lesson_publication_toolchain_manifest_exact_unchanged':True,'all_evidence_and_two_metadata_files_exact_in_Git_tree':len(raws),'four_actual_gate_receipts':gates,'normal_sourceV_API_calls':0,'scope':'Metadata and exact independent evidence carrier only. No fresh Lean run at this carrier, global integration, browser delivery, public history, purification or Goal completion.'}
(W/'accepted-review-metadata-commit.json').write_bytes(dump(x));print(json.dumps({'metadata_carrier':commit,'mathematical_native_checked_commit':candidate,'exact_files_in_Git_tree':len(raws),'sourceV':False}))
