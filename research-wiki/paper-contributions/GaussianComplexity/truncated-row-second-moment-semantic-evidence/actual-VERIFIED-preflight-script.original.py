from pathlib import Path
import concurrent.futures
import datetime
import hashlib
import json
import re
import subprocess
import sys

ROOT = Path('/Users/zhouhuanjian/ASTIS-GC')
HERE = Path(__file__).resolve().parent
E = ROOT / 'research-wiki/paper-contributions/GaussianComplexity/truncated-row-second-moment-semantic-evidence'
N = ROOT / '.astis/semantic-neutral-20261111/rc_native_68bc'
HEAD = 'b71212eaa20fac05c23286bfd01da31f343a5d09'
CANDIDATE = '86c9bb627c61955f2a47f492c59a044230536739'
PLOCAL_CARRIER = '0175bc3092572c0c092346e5aa79ea3bb30b361c'
ADVANCE = 'ASTIS-SA-20261111-GaussianComplexityTruncatedRowMoment'
OWNER = 'huanjian_gc_20261111_truncated_row_moment'
DECL = 'AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumTruncatedRowMoment.actual_truncated_row_second_moment'

def sha(b): return hashlib.sha256(b).hexdigest()
def readhash(p, expected):
    b = p.read_bytes(); assert sha(b) == expected, str(p); return {'path': str(p.relative_to(ROOT)), 'bytes': len(b), 'sha256': expected}
def run(argv):
    p = subprocess.run(argv, cwd=ROOT, capture_output=True)
    assert p.returncode == 0, (argv, p.stdout, p.stderr)
    return {'command': argv, 'exit_code': p.returncode, 'stdout': p.stdout.decode(), 'stderr': p.stderr.decode()}

assert run(['git','rev-parse','HEAD'])['stdout'].strip() == HEAD
assert run(['git','status','--porcelain=v1','--untracked-files=no'])['stdout'] == ''
files = {
 'AutoSamplingTheory/TechnicalLemmas/Probability/StdGaussianMoment.lean': 'f87a1c18284dbe58658c3c312f1015fa2eec0b203d5a1187618e5f43ea2a6e00',
 'AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumTruncatedRowMoment.lean': '1a97dd98ecc4e3965db20a91c1d22ca8520406ea22cbbfbd631579522d071310',
 'Tests/GaussianComplexityFixedSpectrumTruncatedRowMoment.lean': '0125f27884195dc6210ade46987373d0b4674ba067067a03d91dcd0d2828276e',
 'lean-toolchain':'302cd63c54178885b89e669f33b38f12f4dd7ae7e5cac537b3203e3768d8fb2b',
 'lake-manifest.json':'b83ca83b9cf7caa85fa8b023c2ff9a3fb7a7cce7e1c332e810c348535ec49c37'}
source_checks = []
for name, expected in files.items():
    current = (ROOT / name).read_bytes()
    assert sha(current) == expected
    for commit in [CANDIDATE, HEAD]:
        result = subprocess.run(['git','show',commit+':'+name], cwd=ROOT, capture_output=True)
        assert result.returncode == 0 and result.stdout == current, (commit,name)
    source_checks.append({'path':name,'sha256':expected,'exact_candidate_HEAD_worktree_equal':True})

binary = Path('/Users/zhouhuanjian/.elan/toolchains/leanprover--lean4---v4.33.0/bin/lean')
assert sha(binary.read_bytes()) == '1b370cfcbf44e80d1b004ab1b1ab9a4c73951f9f7c242140bcff9bc577576554'
version = run([str(binary),'--version'])
assert 'version 4.33.0, arm64-apple-darwin24.6.0' in version['stdout']
manifest = json.loads((ROOT/'lake-manifest.json').read_bytes())
def package_check(item):
    name=item['name']; path=ROOT/'.lake/packages'/name
    h=run(['git','-C',str(path),'rev-parse','HEAD'])
    s=run(['git','-C',str(path),'status','--porcelain=v1','--untracked-files=all','--ignore-submodules=none'])
    assert h['stdout'].strip()==item['rev'] and s['stdout']==''
    return {'name':name,'expected_rev':item['rev'],'actual_HEAD':h['stdout'].strip(),'complete_porcelain':s['stdout'],'commands':[h['command'],s['command']]}
with concurrent.futures.ThreadPoolExecutor(max_workers=9) as pool:
    packages=list(pool.map(package_check,manifest['packages']))
assert len(packages)==9

review_checks=[]
for name, expected in {
 'independent-source-review-original.json':'86207f4e0ddacfd449765baa82e5b2e5364eb9cf42a81b4705d707dd4ce3c74f',
 'independent-source-review-overlay.json':'a969787e220eeeb60c8476b8e35369ca63a498235e559c2af925726f88b6d82c',
 'independent-native-and-static-review-original.json':'a79b9abdfed36545610d63055f3901b4a226c70ace089ee091277510ea73ca6c',
 'independent-native-and-static-custody-original.json':'3f40392a5e737857ad07438e4a9f1f1fa41be96dfc70479a315aa03a42b63280',
 'independent-native-and-static-portable-originals.tar.gz':'c22c86e7ba52b7e6c00467eb1ff7629f1548628060bdd6e6cf03034661028b71',
 'actual-PROVED_LOCAL-append.exact.jsonl':'a9f1da5135d71d5a3ca4182ce66f7c69f29608219707c4b7e63cb506dace0632',
 'actual-PROVED_LOCAL-evidence.full.json':'2629b80687a64141f4a3b809354ae3b323adcee8a6f44548c377b1072a75ce11',
 'preseal-exposure-correction.json':'1cc398074722d3e54ba5d86b64dfbc41088bb8bb7089b35c256df45b3a70936c'}.items():
    review_checks.append(readhash(E/name,expected))
native_manifest=json.loads((N/'manifest.json').read_bytes())
assert sha((N/'manifest.json').read_bytes())=='3f40392a5e737857ad07438e4a9f1f1fa41be96dfc70479a315aa03a42b63280'
for e in native_manifest['entries']:
    b=(N/e['path']).read_bytes(); assert len(b)==e['bytes'] and sha(b)==e['sha256'],e['path']
assert len(native_manifest['entries'])==73
native_receipts=[]
for name in ['native-build.json','CertificatesV3.receipt.json','Ownership.receipt.json','Inspect.receipt.json']:
    raw=(N/name).read_bytes(); data=json.loads(raw)
    for entry in data if isinstance(data,list) else [data]:
        assert entry['exit_code']==0
        assert str(ROOT/'.lake/build/lib/lean') not in entry['LEAN_PATH'].split(':')
        if 'stdout_sha256' in entry:
            prefix=name.removesuffix('.receipt.json')
            assert sha((N/(prefix+'.stdout.log')).read_bytes())==entry['stdout_sha256']
            assert sha((N/(prefix+'.stderr.log')).read_bytes())==entry['stderr_sha256']
    native_receipts.append({'path':str((N/name).relative_to(ROOT)),'sha256':sha(raw),'all_exit_codes':0})
log=(N/'CertificatesV3.stdout.log').read_text()
axioms=re.findall(r'^AXIOMS ([^:]+): \[(.*?)\]',log,flags=re.M|re.S)
assert len(axioms)==3
for name, body in axioms:
    assert {x.strip() for x in body.split(',')} == {'propext','Classical.choice','Quot.sound'},(name,body)
assert 'MODULE_OWNED_COUNT 3' in (N/'Ownership.stdout.log').read_text()
closure=[]
for name in list(files)[:3]:
    raw=(ROOT/name).read_text()
    matches=re.findall(r'\b(?:sorry|admit|axiom)\b|Prop\s*:=\s*True|:=\s*trivial',raw)
    assert not matches
    closure.append({'path':name,'forbidden_closure_matches':matches})

gates=[]
for stamp,kind,expected in [
 ('20261111T054246308757Z','publication','5b1d345b0507b22d1ed69289846e2df8d75305f9d4c0c80fbedbf95227e8ed79'),
 ('20261111T054246308753Z','contributor','c0285d3af9bfdcd5eb3ce6d5ef488513d82f5d89028a39bf22d82c227c42289f'),
 ('20261111T054246308753Z','semantic','1339a9c3e9c2c4f7f1793a6b721101a8e768945544602cd04c599ea2d371aaa4'),
 ('20261111T054246308755Z','frontier','b1c67f53d2e8814bc8651ad3b363418ebd43db5fdafbfd3b04a905ccd36aba18')]:
    prefix=ROOT/'.astis/huanjian-resume-20261103'/(stamp+'-radial-row-second-moment-final-reviewed-'+kind)
    rp=prefix.with_suffix('.receipt.json');lp=prefix.with_suffix('.log')
    r=json.loads(rp.read_bytes());assert r['exit_code']==0 and r['head_before']==HEAD and r['head_after']==HEAD
    assert sha(lp.read_bytes())==expected==r['log_sha256']
    gates.append({'kind':kind,'receipt':str(rp.relative_to(ROOT)),'receipt_sha256':sha(rp.read_bytes()),'log_sha256':expected,'exit_code':0,'HEAD':HEAD})

sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tools'))
from tools import astis_advance as advance
from tools.astis_publication import check_advance
ledger=(ROOT/'runs/substantive_advances.jsonl').read_bytes()
records=[json.loads(line) for line in ledger.splitlines() if line.strip()]
states=advance._replay_advances(records); own=states[ADVANCE]
assert len(states)==303 and own['state']=='PROVED_LOCAL' and own['owner_id']==OWNER
own_events=[x for x in records if x.get('advance_id')==ADVANCE]
assert [x.get('to_state') for x in own_events if x.get('event')=='transition']==['CLAIMED','EXPLORING','PROVED_LOCAL']
assert own['latest_evidence']==json.loads((E/'actual-PROVED_LOCAL-evidence.full.json').read_bytes())
original_ledger=subprocess.run(['git','show',PLOCAL_CARRIER+':runs/substantive_advances.jsonl'],cwd=ROOT,capture_output=True)
assert original_ledger.returncode==0 and original_ledger.stdout==ledger
check_advance([DECL],reviewed=True)
report={'kind':'Independent immutable preflight before exactly one normal PROVED_LOCAL to VERIFIED',
 'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'verifier':'/root/radial_cov_fresh_source_42df',
 'metadata_HEAD':HEAD,'mathematical_native_candidate':CANDIDATE,'original_PROVED_LOCAL_carrier':PLOCAL_CARRIER,
 'source_runtime_file_checks':source_checks,'runtime_binary_sha256':sha(binary.read_bytes()),'actual_lean_version':version,
 'package_checks':packages,'review_and_PLOCAL_checks':review_checks,'native_manifest_entries_rehashed':73,
 'native_receipts':native_receipts,'actual_owned_axioms':{name:[x.strip() for x in body.split(',')] for name,body in axioms},
 'source_fake_closure_scan':closure,'final_real_gate_receipts':gates,'live_reviewed_advance_gate':'PASS',
 'advance_count':303,'foreign_advance_count':302,'state_before':'PROVED_LOCAL',
 'formalizer_API_pristine':False,'chronology_or_pristineness_certified':False,
 'decision':'Normal VERIFIED is warranted only for the canonical single-row identities and bounded native/static evidence.',
 'HOLD':['Original joint Gaussian row-law/integral transport','real desktop/mobile rendering','full-site navigation/index/graph/copy/download/public integration','stabilization/whole-paper/whole-Goal/purification'],
 'snapshot_exports_performed':False,'canonical_mutations_performed':False,'normal_V_calls_performed':0}
(HERE/'immutable-preflight-original.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'preflight':'PASS','metadata_HEAD':HEAD,'mathematical_candidate':CANDIDATE,'native_entries_verified':73,'foreign_advance_count':302,'normal_V_calls':0,'report_sha256':sha((HERE/'immutable-preflight-original.json').read_bytes())},indent=2))
