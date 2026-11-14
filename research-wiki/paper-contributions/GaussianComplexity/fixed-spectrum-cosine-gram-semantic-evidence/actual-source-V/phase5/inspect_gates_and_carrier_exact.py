#!/opt/anaconda3/bin/python
import hashlib,io,json,pathlib,subprocess,tarfile
ROOT=pathlib.Path('/Users/zhouhuanjian/ASTIS-GC');BASE=pathlib.Path(__file__).resolve().parent
C='7359f552e3b9bdf27c2253703d879783f331c4e9';M='72e5d1405284f729f4eb600c5ae5dd556365b7e2'
def sha(b):return hashlib.sha256(b).hexdigest()
def blob(commit,path):
    p=subprocess.run(['git','show',commit+':'+path],cwd=ROOT,capture_output=True)
    assert p.returncode==0,(path,p.stderr.decode());return p.stdout
audit='research-wiki/semantic-roundtrip/audits/huanjian-fixed-spectrum-cosine-gram.json'
assert blob(C,audit)==(BASE.parent/'phase4/proposed-canonical-audit.json').read_bytes()
run='.astis/semantic-neutral-20261110/cg_src_7e41d9/phase3_freeze_execution.json'
assert sha(blob(C,run))=='49236e7104295ef18d2f0ebf5522fa7d1ce81651a642449dc65e7b9f529a132a'
unchanged=['AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumCosineGram.lean',
           'Tests/GaussianComplexityFixedSpectrumCosineGram.lean',
           'AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumGridAlias.lean',
           'website/content/declaration_lessons/huanjian-fixed-spectrum-cosine-gram.json',
           'website/content/publications/huanjian-fixed-spectrum-cosine-gram.json',
           'lean-toolchain','lake-manifest.json','runs/substantive_advances.jsonl']
for name in unchanged:assert blob(M,name)==blob(C,name),name
selected=json.loads((BASE/'inputs/accepted-review-metadata-commit.json').read_text())['all_selected_files_exact_in_Git_tree']
for row in selected:
    data=blob(C,row['path']);assert len(data)==row['bytes'] and sha(data)==row['sha256'],row['path']
E='research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-cosine-gram-semantic-evidence/'
archive=blob(C,E+'fresh-source-7e41d9-phases1-through4-all-original-files.lossless-file-bytes.tar.gz')
assert sha(archive)=='da7caa0e80bb367620b42c5f2834a02933147dd4d23511ece26e81da814d3963'
(BASE/'inputs/fresh-source-7e41d9-original-phases1-through4.tar.gz').write_bytes(archive)
archive_manifest=json.loads(blob(C,E+'fresh-source-7e41d9-all-original-files.archive-manifest.json'))
(BASE/'inputs/fresh-source-7e41d9-all-original-files.archive-manifest.json').write_bytes(blob(C,E+'fresh-source-7e41d9-all-original-files.archive-manifest.json'))
print('SOURCE_ARCHIVE_MANIFEST_KEYS',list(archive_manifest))
with tarfile.open(fileobj=io.BytesIO(archive),mode='r:gz') as tf:
    regular=[r for r in tf.getmembers() if r.isfile()]
    assert len(regular)==403,len(regular)
    own_verified=0
    for member in regular:
        name=member.name.removeprefix('./');data=tf.extractfile(member).read()
        local=BASE.parent/name
        if local.is_file():assert local.read_bytes()==data,name;own_verified+=1
    assert own_verified==403,(own_verified,len(regular))
R=ROOT/'.astis/huanjian-resume-20261103'
stems=['20261110T173442246471Z-cosine-gram-reviewed-carrier-publication',
       '20261110T173442246477Z-cosine-gram-reviewed-carrier-semantic',
       '20261110T173442246468Z-cosine-gram-reviewed-carrier-frontier',
       '20261110T173442246468Z-cosine-gram-reviewed-carrier-contributor']
gates=[]
(BASE/'gates').mkdir(exist_ok=True)
for stem in stems:
    rb=(R/(stem+'.receipt.json')).read_bytes();receipt=json.loads(rb)
    assert receipt['exit_code']==0 and receipt['head_before']==C and receipt['head_after']==C
    log=pathlib.Path(receipt['log']);lb=log.read_bytes();assert sha(lb)==receipt['log_sha256']
    (BASE/'gates'/(stem+'.receipt.json')).write_bytes(rb)
    (BASE/'gates'/(stem+'.log')).write_bytes(lb)
    gates.append({'stem':stem,'receipt_sha256':sha(rb),'log_sha256':sha(lb),'head':C,
                  'exit_code':0,'command':receipt['command'],'log_bytes':len(lb)})
    print('GATE',json.dumps(gates[-1]));print(lb.decode())
result={'metadata_carrier':C,'mathematical_native_checked_commit':M,'canonical_audit_equals_own_proposed_bytes':True,
        'original_run_artifact_exact_Git_path_verified':True,'unchanged_mathematical_and_control_Git_paths':unchanged,
        'all_selected_Git_files_verified':len(selected),'original_source_archive_files_verified':own_verified,
        'all_four_gates_at_exact_carrier':gates,'reader_HOLD_all_six_retained':True,
        'normal_SourceV_has_not_been_called':True}
(BASE/'carrier-and-gates-acceptance.json').write_text(json.dumps(result,indent=2)+'\n')
print('CARRIER_ACCEPTANCE',json.dumps(result,indent=2))
