from pathlib import Path
import json, hashlib, gzip, copy, subprocess, re, sys, datetime, io, contextlib
ROOT=Path('/Users/zhouhuanjian/ASTIS-GC')
sys.path.insert(0,str(ROOT))
from tools import astis_advance as advance
from tools import astis_publication as publication
BASE=ROOT/'research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-normalizer-semantic-evidence'
PUB=BASE/'fresh-source-reader-640251/verification-transition'
PRIV=ROOT/'.astis/huanjian-fixed-spectrum-normalizer-20261108/fresh-source-640251/verification-transition'
OUTS=[PUB,PRIV]
H=lambda b:hashlib.sha256(b).hexdigest()
C=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
auth=json.loads((PUB/'root-normal-source-V-authorization.exact.json').read_text())
assert H((PUB/'root-normal-source-V-authorization.exact.json').read_bytes())=='171c08eea892a374e2326cee23e17282c7b7c673ca406a5c27b5b5115f14e6ac'
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==auth['checked_immutable_commit']
ledger=ROOT/'runs/substantive_advances.jsonl'
before=ledger.read_bytes()
assert H(before)==auth['advance_ledger_before_sha256']
records=[json.loads(line) for line in before.splitlines() if line.strip()]
states=advance._replay_advances(records)
own=states[auth['advance_id']]
assert own['state']=='PROVED_LOCAL'
assert own.get('owner_id') and own['owner_id']!=auth['authorized_actor']
assert not [x for x in states.values() if x['state']=='STABILIZING']
foreign={k:H(C(v)) for k,v in states.items() if k!=auth['advance_id']}
assert len(foreign)==auth['required_preservation']['foreign_advance_states']==283
canonical=ROOT/'research-wiki/semantic-roundtrip/audits/huanjian-fixed-spectrum-normalizer.json'
canonical_before=canonical.read_bytes()
assert H(canonical_before)==auth['canonical_audit_before_sha256']
proposal=BASE/'fresh-source-reader-640251/phase3/proposed-accepted-canonical-audit.json'
proposal_bytes=proposal.read_bytes()
assert H(proposal_bytes)==auth['authorized_exact_accepted_audit_sha256']
accepted=json.loads(proposal_bytes)
target='AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumNormalizer.actual_normalizing_integral'
assert own['publication_declarations']==[target]
assert accepted['state']=='accepted' and accepted['source_review']['reviewer']==auth['authorized_actor']
assert accepted['source_review']['review_run_sha256']==auth['independent_review_run_sha256']
assert accepted['publication_binding_sha256']==auth['publication_binding_sha256']
pins=json.loads((BASE/'full-review-input-pins.json').read_text())
for p,h in pins['exact_inputs'].items():
    assert H((ROOT/p).read_bytes())==h,p
frontiers={p.relative_to(ROOT).as_posix():H(p.read_bytes()) for p in sorted((ROOT/'research-wiki/frontier-cells').rglob('*.json'))}
assert len(frontiers)==auth['required_preservation']['all_raw_frontier_JSON_files']==443
old=json.loads((BASE/'initial-queue-and-frontier-protection.json').read_text())
assert len(old['all442_old_frontier_hashes'])==442
assert all(frontiers[p]==h for p,h in old['all442_old_frontier_hashes'].items())
discovery=ROOT/'runs/substantive_discoveries.jsonl'
discovery_hash=H(discovery.read_bytes())
assert discovery_hash==old['discovery_ledger_sha256']
frozen={}
for side,prefix in [('public',BASE/'fresh-source-reader-640251'),('private',ROOT/'.astis/huanjian-fixed-spectrum-normalizer-20261108/fresh-source-640251')]:
    for phase in ['phase1','phase2','phase3']:
        for p in sorted((prefix/phase).rglob('*')):
            if p.is_file():frozen[p.relative_to(ROOT).as_posix()]=H(p.read_bytes())
assert H((BASE/'fresh-source-reader-640251/phase3/freeze-manifest.json').read_bytes())==auth['independent_phase3_manifest_sha256']
tracked=subprocess.check_output(['git','ls-files'],cwd=ROOT,text=True).splitlines()
protected_names={'README.md','AGENTS.md','lean-toolchain','lake-manifest.json'}
protected_names.update(p for p in tracked if re.search(r'(^|[/_.-])models?([/_.-]|$)',p,re.I))
protected={p:H((ROOT/p).read_bytes()) for p in sorted(protected_names) if (ROOT/p).is_file()}
registry=publication.roundtrip.load_registry()
prospective=copy.deepcopy(registry)
found=[i for i,a in enumerate(prospective['audits']) if a['id']==accepted['id']]
assert len(found)==1
prospective['audits'][found[0]]=accepted
issues=publication.roundtrip.validate_registry(prospective)
assert not issues,issues
actual_loader=publication.roundtrip.load_registry
capture=io.StringIO()
try:
    publication.roundtrip.load_registry=lambda *a,**k:prospective
    with contextlib.redirect_stdout(capture):
        publication.check_advance([target],reviewed=True)
finally:
    publication.roundtrip.load_registry=actual_loader
    publication.inputs.cache_clear()
    publication.load.cache_clear()
assert ledger.read_bytes()==before
assert canonical.read_bytes()==canonical_before
baseline={
 'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'head':auth['checked_immutable_commit'],'advance_id':auth['advance_id'],
 'ledger_before_sha256':H(before),'ledger_before_bytes':len(before),
 'canonical_before_sha256':H(canonical_before),
 'accepted_proposal_sha256':H(proposal_bytes),
 'own_before':own,'foreign_state_hashes':foreign,
 'all_raw_frontier_hashes':frontiers,'foreign_frontier_hashes':old['all442_old_frontier_hashes'],
 'discovery_ledger_sha256':discovery_hash,
 'frozen_review_file_hashes':frozen,'protected_README_config_model_file_hashes':protected,
 'models_and_original_proof_owner_guard':'Own owner retained; all foreign replayed objects including model fields and tracked model/config files protected. No model API/config operation authorized.',
 'prospective_validate_registry_issues':issues,
 'prospective_normal_publication_check_reviewed_true':'PASS with accepted audit in memory only; actual canonical still unchanged.',
 'normal_V_API_calls_so_far':0,'STAB':[]}
payloads={
 'before-ledger.lossless.jsonl.gz':gzip.compress(before,mtime=0),
 'before-canonical-audit.exact.json':canonical_before,
 'before-own-advance.json':(json.dumps(own,ensure_ascii=False,indent=2)+'\n').encode(),
 'preflight-baseline.json':(json.dumps(baseline,ensure_ascii=False,indent=2)+'\n').encode(),
 'preflight-publication.log':capture.getvalue().encode()}
for out in OUTS:
    for name,b in payloads.items():
        with (out/name).open('xb') as handle:handle.write(b)
print(json.dumps({'status':'FULL_PREFLIGHT_PASS_CANONICAL_AND_LEDGER_UNCHANGED','proof_owner':own['owner_id'],'own_state':own['state'],'foreign_states':len(foreign),'all_raw_frontiers':len(frontiers),'foreign_frontiers':len(old['all442_old_frontier_hashes']),'frozen_review_files':len(frozen),'protected_README_config_model_files':len(protected),'prospective_registry_issues':len(issues),'prospective_publication_gate':'PASS','preflight_baseline_sha256':H(payloads['preflight-baseline.json']),'normal_V_API_calls':0},ensure_ascii=False,indent=2))
