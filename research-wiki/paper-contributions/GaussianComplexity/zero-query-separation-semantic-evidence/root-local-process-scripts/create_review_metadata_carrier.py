from pathlib import Path
import sys,json,hashlib,gzip,subprocess
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent.relative_to(Path.cwd());E=Path('research-wiki/paper-contributions/GaussianComplexity/zero-query-separation-semantic-evidence');R=Path('.astis/huanjian-resume-20261103')
sha=lambda b:hashlib.sha256(b).hexdigest();dump=lambda x:(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
candidate='eed870294de059136900110ade59b4a292a126ad'
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==candidate and not (W/'accepted-review-metadata-commit.json').exists()
gate_stems=['20261110T141454565300Z-zero-query-reviewed-publication','20261110T141454564049Z-zero-query-reviewed-semantic','20261110T141454564893Z-zero-query-reviewed-frontier','20261110T141454565275Z-zero-query-reviewed-contributor']
gates=[]
for stem in gate_stems:
    p=R/(stem+'.receipt.json');x=json.loads(p.read_bytes());assert x['exit_code']==0 and x['head_before']==candidate and x['head_after']==candidate and sha(Path(x['log']).read_bytes())==x['log_sha256'];gates.append(x)
d=E/'actual-review-layer-checks';assert not d.exists();d.mkdir()
for p in sorted(R.glob('*zero-query*.receipt.json')):
    x=json.loads(p.read_bytes())
    if x['head_before']!=candidate:continue
    b=Path(x['log']).read_bytes();assert sha(b)==x['log_sha256'];(d/p.name).write_bytes(p.read_bytes());(d/(p.stem+'.log.gz')).write_bytes(gzip.compress(b,mtime=0))
for n in ['apply_independent_reviews.py','create_review_metadata_carrier.py']:
    p=E/'root-local-process-scripts'/n;assert not p.exists();p.write_bytes((W/n).read_bytes())
ap=Path('research-wiki/semantic-roundtrip/audits/huanjian-zero-query-separation.json');cp=Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-zero-query-separation.json')
assert json.loads(ap.read_bytes())['state']=='source-reviewed'
for n in ['AutoSamplingTheory/ExampleCases/GaussianComplexity/ZeroQuerySeparation.lean','Tests/GaussianComplexityZeroQuerySeparation.lean','website/content/declaration_lessons/huanjian-zero-query-separation.json','website/content/publications/huanjian-zero-query-separation.json','lake-manifest.json','lean-toolchain']:
    assert Path(n).read_bytes()==subprocess.check_output(['git','show',candidate+':'+n]),n
paths=sorted([ap,cp]+[p for p in E.rglob('*') if p.is_file()]);raws={str(p):p.read_bytes() for p in paths}
assert not subprocess.check_output(['git','diff','--cached','--name-only'])
subprocess.run(['git','add','-f','--']+list(raws),check=True)
staged=set(subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines());assert staged<=set(raws)
assert {'research-wiki/semantic-roundtrip/audits/huanjian-zero-query-separation.json',str(cp)}<=staged
assert all(n.startswith(str(E)+'/') or n in [str(ap),str(cp)] for n in staged)
for n in staged:assert subprocess.check_output(['git','show',':'+n])==raws[n],n
subprocess.run(['git','diff','--cached','--check'],check=True)
subprocess.run(['git','commit','-m','Bind independent Gaussian event-gap reviews and retain reader HOLD'],check=True)
commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
for n,b in raws.items():assert subprocess.check_output(['git','show',commit+':'+n])==b,n
x={'accepted_review_metadata_carrier_commit':commit,'mathematical_native_checked_commit':candidate,'sourceP_Test_lesson_publication_toolchain_manifest_exact_unchanged':True,'all_evidence_and_two_metadata_files_exact_in_Git_tree':len(raws),'four_actual_gate_receipts':gates,'normal_sourceV_API_calls':0,'scope':'Metadata and exact independent evidence carrier only. No fresh Lean run at this carrier, global integration, browser delivery, public history, purification or Goal completion.'}
(W/'accepted-review-metadata-commit.json').write_bytes(dump(x));print(json.dumps({'metadata_carrier':commit,'mathematical_native_checked_commit':candidate,'exact_files_in_Git_tree':len(raws),'sourceV':False}))
