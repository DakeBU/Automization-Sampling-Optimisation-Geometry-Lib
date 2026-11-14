"""Read-only carrier/native/sourceV preflight. Never invokes transition_advance."""
from pathlib import Path
from hashlib import sha256
import io
import gzip
import json
import subprocess
import sys
import tarfile

sys.dont_write_bytecode=True
REPO=Path.cwd().resolve()
sys.path.insert(0,str(REPO))
from tools import astis_advance as adv
from tools.astis_publication import check_advance
ROOT=Path(__file__).resolve().parent
OWN=ROOT.parent
E=Path('research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-target-law-semantic-evidence')
NATIVE=Path('.astis/huanjian-gc-fixed-spectrum-target-law-20261110/independent-native-reader-4b8e73')
CARRIER='56dbffcda73fa78539777059f26a964d9b53fa0c'
MATH='8ee639d3aced826aa5b4e39fa6f8bedd3b830327'
AID='ASTIS-SA-20261110-GaussianComplexityFixedSpectrumTargetLaw'
DECL='AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumTargetLaw.actual_rotated_gaussian_target'
h=lambda b:sha256(b).hexdigest()
git=lambda *args:subprocess.run(['git',*args],capture_output=True,check=True).stdout
assert git('rev-parse','HEAD').decode().strip()==CARRIER
def save(name,data):
    out=ROOT/'preflight-inputs'/name
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_bytes(data)

paths=['AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumTargetLaw.lean',
       'Tests/GaussianComplexityFixedSpectrumTargetLaw.lean',
       'website/content/declaration_lessons/huanjian-fixed-spectrum-target-law.json',
       'website/content/publications/huanjian-fixed-spectrum-target-law.json',
       'lean-toolchain','lake-manifest.json']
identity=[]
for path in paths:
    before=git('show',MATH+':'+path);current=git('show',CARRIER+':'+path)
    assert current==before==Path(path).read_bytes()
    identity.append({'path':path,'sha256':h(current),'bytes':len(current)})
    save('carrier/'+path,current)
auditpath='research-wiki/semantic-roundtrip/audits/huanjian-fixed-spectrum-target-law.json'
old=json.loads(git('show',MATH+':'+auditpath))
newraw=git('show',CARRIER+':'+auditpath)
assert Path(auditpath).read_bytes()==newraw
new=json.loads(newraw)
proposal=json.loads((OWN/'phase3/canonical-five-field-audit-proposal.json').read_bytes())
assert h((OWN/'phase3/canonical-five-field-audit-proposal.json').read_bytes())=='966772dade74559edba0fd73d86f3480069dbd77da22e4b423d0b33b95059ade'
assert all(new[k]==v for k,v in proposal.items())
assert {k:v for k,v in old.items() if k not in proposal}=={k:v for k,v in new.items() if k not in proposal}
save('accepted-own-audit.exact.json',newraw)

nativepins={'independent-judgement.json':'de2714b49f2501d815428f1a6e6e22913284328463da37078c2150a2e2d0a8ad',
            'frozen-manifest.json':'f9bc3304954f52d129e7e04074b24b22bc5c92db107058a772faf548b136b6a5',
            'frozen-receipt.json':'40b2e7507b53735bd8cc21a1162a7e70fafaa03cc13806e0f8c7ddfe77ed975a'}
for name,pin in nativepins.items():
    b=(NATIVE/name).read_bytes();assert h(b)==pin
    save('original-native/'+name,b)
nmanifest=json.loads((NATIVE/'frozen-manifest.json').read_bytes())
for item in nmanifest['files']:
    b=(NATIVE/item['path']).read_bytes()
    assert len(b)==item['bytes'] and h(b)==item['sha256']
assert len(nmanifest['files'])==89

archives=[]
for manifestname,expected,count,origin in [
    ('independent-native-fullmodule-static.archive-manifest.json','22c843c570e1584a4718f03f78454280adec72493286448aa4e8d1b26942a6fb',92,NATIVE),
    ('independent-full-source-all-phases.archive-manifest.json','142d5514852937d6e7b925e1dca297cd730133ff4cd9497e7fea5abe44c7b309',113,OWN)]:
    mb=(E/manifestname).read_bytes();m=json.loads(mb);archive=Path(m['archive']);b=archive.read_bytes()
    assert h(b)==m['sha256']==expected and m['file_count']==count
    assert m['raw_foreign_snapshots_included'] is False
    assert git('show',CARRIER+':'+str(archive))==b
    assert git('show',CARRIER+':'+str(E/manifestname))==mb
    members={}
    with tarfile.open(fileobj=io.BytesIO(b),mode='r:gz') as tf:
        for member in tf.getmembers():
            assert member.isfile() and member.name not in members
            assert not member.name.startswith('/') and '..' not in Path(member.name).parts
            members[member.name]=tf.extractfile(member).read()
    assert set(members)=={x['path'] for x in m['files']} and len(members)==count
    for item in m['files']:
        value=members[item['path']]
        assert h(value)==item['sha256'] and len(value)==item['bytes']
        assert value==(origin/item['path']).read_bytes()
    if origin==OWN:
        expectedpaths=set()
        for phase,prefix in [(OWN,''),(OWN/'phase2','phase2/'),(OWN/'phase3','phase3/')]:
            pm=json.loads((phase/'manifest.json').read_bytes())
            expectedpaths.update(prefix+x['path'] for x in pm['files'])
            expectedpaths.update([prefix+'manifest.json',prefix+'freeze_receipt.json'])
        assert set(members)==expectedpaths
        assert not any('PRIVATE' in name or name.startswith('normal-sourceV/') for name in members)
    save('archive-manifests/'+manifestname,mb)
    archives.append({'archive':str(archive),'sha256':expected,'files':count,
                     'all_members_exact_to_original_freeze':True,'exact_in_carrier':True,
                     'raw_foreign_snapshots_included':False})

judgement=json.loads((NATIVE/'independent-judgement.json').read_bytes())
assert judgement['verified_commit']==MATH
assert judgement['whole_module_read']['owned_count']==2
assert judgement['kernel_evidence']['recursive_axioms_both']==['propext','Classical.choice','Quot.sound']
assert judgement['kernel_evidence']['all_owned_reachable_from_consumer']
native_reports=[]
for stem in ['normal-module-pair','fresh-producer','fresh-producer-retry1','fresh-consumer','kernel-reader','kernel-reader-retry1']:
    rb=(NATIVE/(stem+'.receipt.json')).read_bytes();rec=json.loads(rb)
    log=(NATIVE/(stem+'.raw.log')).read_bytes()
    assert rec['HEAD']==MATH
    save('original-native/'+stem+'.receipt.json',rb)
    save('original-native/'+stem+'.raw.log',log)
    native_reports.append({'label':stem,'exit_code':rec['exit_code'],'elapsed_seconds':rec['elapsed_seconds'],
                           'HEAD':rec['HEAD'],'receipt_sha256':h(rb),'raw_log_sha256':h(log)})
assert [r['exit_code'] for r in native_reports]==[0,1,0,0,1,0]
for name in ['KernelReader.lean','KernelReader.attempt1.lean','native-artifacts.json','fake-closure.bounded.json','reader.static.json','reader.static.attempt1.json','check_reader.py','check_reader.attempt1.py']:
    save('original-native/'+name,(NATIVE/name).read_bytes())

gates=[]
for rp in sorted((E/'actual-review-layer-checks').glob('20261110T115103*.receipt.json')):
    rb=rp.read_bytes();rec=json.loads(rb)
    lp=rp.with_name(rp.name.replace('.receipt.json','.receipt.log.gz'));compressed=lp.read_bytes();raw=gzip.decompress(compressed)
    assert rec['exit_code']==0 and h(raw)==rec['log_sha256']
    assert rec['head_before']==rec['head_after']==MATH
    assert git('show',CARRIER+':'+str(rp))==rb and git('show',CARRIER+':'+str(lp))==compressed
    save('original-gates/'+rp.name,rb);save('original-gates/'+lp.name,compressed)
    gates.append({'receipt':str(rp),'receipt_sha256':h(rb),'gzip_log':str(lp),'gzip_sha256':h(compressed),
                  'raw_log_sha256':h(raw),'actual_gate_HEAD':rec['head_before'],'command':rec['command'],
                  'exit_code':rec['exit_code'],'elapsed_seconds':rec['elapsed_seconds']})
assert len(gates)==4

base=json.loads((OWN/'PRIVATE-normal-sourceV-baseline/baseline.private.json').read_bytes())
ledger=Path(base['ledger_path']).read_bytes()
assert ledger==(OWN/'PRIVATE-normal-sourceV-baseline/ledger-prefix.raw.jsonl').read_bytes()
states=adv._replay_advances([json.loads(x) for x in ledger.splitlines() if x.strip()])
assert {k:v for k,v in states.items() if k!=AID}==base['all_foreign_states']
assert states[AID]['state']=='PROVED_LOCAL' and states[AID]['owner_id']=='huanjian_gc_20261110_fixed_spectrum_target_law'
assert states[AID]['publication_declarations']==[DECL]
check_advance([DECL],reviewed=True)
report={'state':'NORMAL_SOURCEV_PREFLIGHT_PASS','metadata_checked_commit':CARRIER,'native_mathematical_candidate':MATH,
        'metadata_carrier_is_not_new_native_build':True,'mathematical_and_authored_six_files_identical':identity,
        'five_field_proposal_exactly_applied':True,'every_other_audit_field_value_unchanged':True,
        'accepted_audit_sha256':h(newraw),'archives':archives,'native_reports':native_reports,
        'native_judgement_sha256':nativepins['independent-judgement.json'],
        'independent_native_original_actor':'/root/targetlaw_module_reader_4b8e73',
        'original_native_reported_verifier_id':judgement['verifier_id'],
        'fresh_T_imports_own_fresh_P':True,'all_owned_count':2,'all_owned_reachable':True,'standard_axioms_only':True,
        'static_reader_scope_only_no_browser_or_global':True,'four_actual_gates':gates,
        'actual_check_advance_reviewed_true_passed_at_carrier':True,
        'private_full_foreign_baseline_frozen_outside_portable_directory':True,
        'all296_foreign_states_unchanged_before_API':True,'normal_transition_API_calls_so_far':0,
        'proof_owner_preserved':'huanjian_gc_20261110_fixed_spectrum_target_law',
        'actual_source_verifier_actor':'/root/targetlaw_fresh_source_9c7d21',
        'no_STAB_global_publication_purification_goal_credit':True}
(ROOT/'preflight-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'state':report['state'],'metadata_checked_commit':CARRIER,'native_mathematical_candidate':MATH,
                  'archive_member_counts':[92,113],'four_actual_gates_verified':True,
                  'reviewed_check_advance_passed':True,'normal_transition_API_calls_so_far':0},indent=2))
