from pathlib import Path
import copy, contextlib, gzip, hashlib, io, json, subprocess, sys, tarfile

REPO = Path('/Users/zhouhuanjian/ASTIS-GC')
ROOT = Path(__file__).resolve().parent
PUB = ROOT / 'public'
PRIVATE = ROOT / 'private'
SOURCE = ROOT.parent
E = REPO / 'research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-threshold-semantic-evidence'
ADVANCE = 'ASTIS-SA-20261110-GaussianComplexityFixedSpectrumThreshold'
FRONTIER = REPO / 'research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-threshold.json'
AUDIT = REPO / 'research-wiki/semantic-roundtrip/audits/huanjian-fixed-spectrum-threshold.json'
DECL = 'AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumThreshold.eventual_actual_gaussian_threshold_small'
MATH = '521b422bad98d4297e86058b4a31e1f15aa4b064'
CARRIER = '7524a4155762365b1029fa795f87fad2eae05fd4'
VERIFIER = '/root/threshold_fresh_source'
LEDGER = REPO / 'runs/substantive_advances.jsonl'
DISCOVERY = REPO / 'runs/substantive_discoveries.jsonl'

def sha(b): return hashlib.sha256(b).hexdigest()
def canonical(x): return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def write(path,x): path.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def git(*args): return subprocess.run(['git',*args],cwd=REPO,check=True,stdout=subprocess.PIPE).stdout
def foreign_controls():
    paths = list((REPO/'research-wiki/frontier-cells').glob('*.json')) + list((REPO/'research-wiki/semantic-roundtrip/audits').glob('*.json'))
    return {str(p.relative_to(REPO)):p.read_bytes() for p in paths if p not in {FRONTIER,AUDIT}}

def main():
    sys.path.insert(0,str(REPO))
    from tools import astis_advance as advance
    from tools.astis_publication import check_advance, binding_digest, load
    assert git('rev-parse','HEAD').decode().strip()==CARRIER
    assert not git('status','--porcelain=v1','--untracked-files=no')
    carrier_bytes=(E/'reviewed-metadata-carrier.json').read_bytes()
    assert sha(carrier_bytes)=='2ff1a1a22639d62bf3edbfc399ec5c6d436969f04815d307ce206e34ad16c187'
    carrier=json.loads(carrier_bytes)
    prior = {
      'phase1-manifest.json':'023597659d8e757bff7a7c5988379ba9a71c2ddef1fa9adbff1a226e73c25380',
      'phase2-manifest.json':'3cb7adc440d1ddd2cd7ac4774e40b0532857c6e251d6fbee531120fb3d5040c5',
      'phase3-manifest.json':'071c7269bd41ef490652787dd4ebe27a8fc1a1cec39a015c8cb2c4d925bfcc95',
      'schema-adapter-v2/manifest.json':'c75e732b66fdb73c01239afe36cd25bb6f6f67356305bd0605db99e64f340ddf'}
    for name,want in prior.items():
        p=SOURCE/name; assert sha(p.read_bytes())==want
        for row in json.loads(p.read_text())['files']:
            q=p.parent/row['path']; assert sha(q.read_bytes())==row['sha256']; assert q.stat().st_mode&0o222==0
    accepted=json.loads((SOURCE/'schema-adapter-v2/proposed-adapter-v2.json').read_text())
    audit=json.loads(AUDIT.read_text())
    assert {k:audit[k] for k in accepted}==accepted
    assert audit['source_review']['state']=='accepted'
    packet=json.loads((E/'fresh-source-reviewer-packet.json').read_text()); packetsha=packet.pop('packet_sha256')
    assert sha(canonical(packet))==packetsha=='5b3ec3efebec219955318a691b56ae758131ed6fa19b6af08b32ef2178282ac7'
    item=next(x for x in load() if x['id']=='huanjian-fixed-spectrum-threshold')
    binding=next(x for x in item['bindings'] if x['declaration']==DECL)
    assert binding_digest(item,binding)==packet['publication_binding_sha256']==carrier['binding_sha256']=='554191d5cee31cd5a2c56e52cdde685ee39219eb5f1ebe5f0a2c052b20821379'
    # A read-only exact current metadata gate, not a transition API or native rebuild.
    captured=io.StringIO()
    with contextlib.redirect_stdout(captured),contextlib.redirect_stderr(captured): check_advance([DECL],reviewed=True)
    (PUB/'preflight-current-metadata-gate.log').write_text(captured.getvalue())
    bytes_checked=[]
    for row in json.loads((SOURCE/'phase3-input-manifest.json').read_text())['files']:
        name=row['path']
        if name.startswith('.lake/') or name.endswith('fresh-source-reviewer-packet.json'): continue
        if name.endswith('huanjian-fixed-spectrum-threshold.json') and 'semantic-roundtrip/' in name: continue
        b=(REPO/name).read_bytes();assert sha(b)==row['sha256']
        if not name.startswith('.astis/'):
            assert b==git('show',MATH+':'+name)==git('show',CARRIER+':'+name)
        bytes_checked.append({'path':name,'sha256':sha(b),'commit_blob_comparison':not name.startswith('.astis/')})
    changes=git('diff','--name-only',MATH,CARRIER).decode().splitlines()
    allowed={str(FRONTIER.relative_to(REPO)),str(AUDIT.relative_to(REPO))}
    assert all(n in allowed or n.startswith(str(E.relative_to(REPO))+'/') for n in changes)
    metadata=[]
    for row in carrier['four_actual_metadata_checks']:
        p=REPO/row['receipt'];b=p.read_bytes();assert sha(b)==row['receipt_sha256'];receipt=json.loads(b)
        logpath=p.with_name(p.name.replace('.receipt.json','.log.gz'));log=gzip.decompress(logpath.read_bytes())
        assert sha(log)==receipt['log_sha256']==row['actual_log_sha256']
        assert receipt['exit_code']==0 and receipt['head_before']==receipt['head_after']==MATH
        (PUB/('gate-'+row['label']+'.receipt.json')).write_bytes(b)
        (PUB/('gate-'+row['label']+'.actual.log')).write_bytes(log)
        metadata.append({'label':row['label'],'receipt':receipt,'receipt_sha256':sha(b),'actual_log_sha256':sha(log)})
    archive_manifest=json.loads((E/'independent-native-fullmodule-static.archive-manifest.json').read_text())
    archive=REPO/archive_manifest['archive'];assert sha(archive.read_bytes())==archive_manifest['sha256']
    with tarfile.open(archive,'r:gz') as t:
        members={m.name:m for m in t.getmembers() if m.isfile()};assert len(members)==128
        data={r['path']:t.extractfile(members[r['path']]).read() for r in archive_manifest['files']}
    for row in archive_manifest['files']: assert sha(data[row['path']])==row['sha256'] and len(data[row['path']])==row['bytes']
    assert sha(data['freeze.json'])=='486033cf8c945e3a4af4dfaaa8a522e7491111dabe56123f58a7baee1d1609a3'
    report=json.loads(data['check-report.json']);kernel=json.loads(data['kernel-inventory.json']);reuse=json.loads(data['canonical-reuse.json'])
    assert report['candidate_commit']==MATH and report['fresh_native_checks_all_exit_zero'] and not report['mathematical_findings']
    assert report['binding']['computed_publication_binding_sha256']==carrier['binding_sha256']
    assert kernel['owned_count']==6 and kernel['handwritten_count']==4 and kernel['reachable_generated_proof_count']==2
    assert kernel['all_owned_reachable'] and kernel['all_axioms_standard'] and kernel['literal_elaborated_signature_check']
    assert all(set(r['axioms']) <= {'propext','Classical.choice','Quot.sound'} for r in kernel['rows'])
    assert len(reuse['objects'])==9 and report['fresh_parent_compilations']==0
    for row in reuse['objects']:
        assert sha((REPO/row['source']).read_bytes())==row['source_sha256'] and row['exit_code']==0
        module=row['source'].removesuffix('.lean')
        assert sha(data['oleans/'+module+'.olean'])==row['object_sha256']
    for row in report['identity']['packages']:
        assert git('-C',str(REPO/'.lake/packages'/row['name']),'rev-parse','HEAD').decode().strip()==row['expected']==row['actual']
    assert sha((REPO/'lean-toolchain').read_bytes())==reuse['toolchain_sha256']
    assert sha((REPO/'lake-manifest.json').read_bytes())==reuse['manifest_sha256']
    assert sha(Path(report['native_binary']['binary']).read_bytes())==report['native_binary']['sha256']
    receipt_names=['isolated-producer','isolated-Test','isolated-kernel-audit','static-lesson','native-binary','toolchain','canonical-object-reuse','exact-identity','final-exact-identity']
    native_receipts=[]
    for label in receipt_names:
        r=json.loads(data[label+'.receipt.json']);assert r['exit_code']==0
        for stream in ['stdout','stderr']:assert sha(data[label+'.'+stream+'.log'])==r[stream+'_sha256']
        native_receipts.append({'label':label,'receipt':r,'receipt_sha256':sha(data[label+'.receipt.json'])})
    selected=['freeze.json','check-report.json','kernel-inventory.json','canonical-reuse.json','syntax-inventory.json','local-reader-report.json','binding-check.json','isolated-kernel-audit.stdout.log']
    for name in selected:(PUB/('native-'+name)).write_bytes(data[name])
    # Baseline raw snapshots are private; no foreign raw is copied into public output.
    ledger=LEDGER.read_bytes();discovery=DISCOVERY.read_bytes();assert ledger.endswith(b'\n') and discovery.endswith(b'\n')
    records=[json.loads(line) for line in ledger.splitlines()];state=advance._replay_advances(records);own=state[ADVANCE]
    assert own['state']=='PROVED_LOCAL' and own['owner_id']=='huanjian_gc_20261110_fixed_spectrum_threshold'
    assert own['schema_version']==4 and own['publication_declarations']==[DECL]
    assert not [r for r in records if r.get('advance_id')==ADVANCE and r.get('to_state')=='VERIFIED']
    assert VERIFIER != own['owner_id']
    foreign={k:v for k,v in state.items() if k!=ADVANCE}; controls=foreign_controls()
    (PRIVATE/'advances.before.raw.jsonl').write_bytes(ledger);(PRIVATE/'discoveries.before.raw.jsonl').write_bytes(discovery)
    (PRIVATE/'foreign-advances.before.canonical.json').write_bytes(canonical(foreign))
    raw_controls=PRIVATE/'foreign-control-state.before.tar.gz'
    with tarfile.open(raw_controls,'w:gz') as t:
        for name,b in sorted(controls.items()):
            info=tarfile.TarInfo(name);info.size=len(b);info.mode=0o600;t.addfile(info,io.BytesIO(b))
    (PRIVATE/'git-index.before.raw').write_bytes(git('ls-files','--stage','-z'))
    (PRIVATE/'git-tracked-status.before.raw').write_bytes(git('status','--porcelain=v1','--untracked-files=no'))
    (PRIVATE/'git-untracked-status.before.raw').write_bytes(git('status','--porcelain=v1','--untracked-files=all'))
    (PRIVATE/'own-audit.before.raw.json').write_bytes(AUDIT.read_bytes())
    (PUB/'own-frontier.before.raw.json').write_bytes(FRONTIER.read_bytes())
    (PUB/'own-sau.before.json').write_bytes(json.dumps(own,ensure_ascii=False,indent=2).encode()+b'\n')
    guards={'ledger_before_bytes':len(ledger),'ledger_before_sha256':sha(ledger),'ledger_before_rows':len(records),'discoveries_before_sha256':sha(discovery),'foreign_advance_state_canonical_sha256':sha(canonical(foreign)),'foreign_advance_count':len(foreign),'foreign_control_file_count':len(controls),'foreign_control_file_hashes_sha256':sha(canonical({k:sha(v) for k,v in controls.items()})),'private_foreign_raw_archive_sha256':sha(raw_controls.read_bytes()),'git_index_before_sha256':sha((PRIVATE/'git-index.before.raw').read_bytes()),'own_audit_before_sha256':sha(AUDIT.read_bytes()),'own_frontier_before_sha256':sha(FRONTIER.read_bytes())}
    preflight={'decision':'PASS_READY_FOR_EXACTLY_ONE_NORMAL_SOURCEV_API','advance_id':ADVANCE,'verifier_id':VERIFIER,'actual_before_state':'PROVED_LOCAL','actual_owner':own['owner_id'],'checked_math_commit':MATH,'accepted_metadata_carrier':CARRIER,'current_HEAD':CARRIER,'metadata_carrier_only_selected_paths':changes,'current_reviewed_metadata_gate':'PASS; direct read-only check_advance([exact declaration],reviewed=True)','source_freezes':prior,'accepted_five_field_adapter_sha256':sha((SOURCE/'schema-adapter-v2/proposed-adapter-v2.json').read_bytes()),'packet_sha256':packetsha,'binding_sha256':carrier['binding_sha256'],'source_math_and_exposition_bytes_identical_at_math_carrier_and_worktree':bytes_checked,'native_archive_all_file_digests_verified':128,'native_freeze_sha256':sha(data['freeze.json']),'native_report_sha256':sha(data['check-report.json']),'native_receipts':native_receipts,'actual_metadata_gates':metadata,'private_preservation_guards':guards,'no_native_rebuild_at_carrier':True,'API_calls_so_far':0,'exposure':'The initial read-only git status listed existing foreign untracked filenames, including .atlas-upstream/. No contents of those artifacts were inspected. Foreign raw/state copies are machine preservation snapshots stored privately only. Native receipts were first opened after full source judgment and adapter froze.','truth_boundary':'Numeric C-family and private shifted diagonal law only; no original absolute-C concentration, rotated detector, algorithms/oracle/TV/cost/main theorem, STAB, shared integration, public browser/delivery, PURIFIED or whole-Goal claim.'}
    write(PUB/'preflight.json',preflight)
    for p in PRIVATE.iterdir():p.chmod(0o600)
    print(json.dumps({'preflight':'PASS','state':'PROVED_LOCAL','metadata_carrier':CARRIER,'private_guards':guards,'normal_transition_API_calls':0},indent=2))

if __name__=='__main__': main()
