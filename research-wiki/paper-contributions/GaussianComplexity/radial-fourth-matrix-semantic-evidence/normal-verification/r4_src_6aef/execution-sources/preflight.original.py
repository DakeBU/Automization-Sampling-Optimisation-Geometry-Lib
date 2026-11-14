from pathlib import Path
import datetime, hashlib, json, os, stat, subprocess, sys, time

ROOT=Path.cwd()
BASE=ROOT/'.astis/semantic-neutral-20261111/r4_src_6aef/normal-verification'
LOCAL=BASE/'local-only';LOCAL.mkdir(parents=True,exist_ok=True)
E=ROOT/'research-wiki/paper-contributions/GaussianComplexity/radial-fourth-matrix-semantic-evidence'
OUT=E/'normal-verification/r4_src_6aef';OUT.mkdir(parents=True,exist_ok=True)
ADV='ASTIS-SA-20261111-GaussianComplexityRadialFourthMatrix'
ACTOR='/root/radial_fourth_fresh_source_6aef'
HEAD='3ba24f46ea74e4537e57824982dfee9f51aeac27'
MATH='69a3336dde302c4a34dbd88708ff6226b2bd0e87'
C=Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-radial-fourth-matrix.json')
sys.path.insert(0,str(ROOT))
from tools.astis_advance import _replay_advances, _replay_discoveries
def sha(b):return hashlib.sha256(b).hexdigest()
def enc(v):return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode()
def canon(v):return json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()
def git(*args):return subprocess.run(['git',*args],cwd=ROOT,check=True,capture_output=True).stdout
def binding(path):
    p=Path(path);b=p.read_bytes();return {'path':str(p.relative_to(ROOT) if p.is_absolute() else p),'bytes':len(b),'sha256':sha(b)}
assert git('rev-parse','HEAD').decode().strip()==HEAD
assert not (E/'actual-VERIFIED-independent-decision.json').exists()
assert not (OUT/'transition-attempted.once.json').exists()

# Private full snapshots: these are never part of the portable manifest.
advance_raw=(ROOT/'runs/substantive_advances.jsonl').read_bytes()
discovery_raw=(ROOT/'runs/substantive_discoveries.jsonl').read_bytes()
ar=[json.loads(x) for x in advance_raw.splitlines() if x.strip()]
dr=[json.loads(x) for x in discovery_raw.splitlines() if x.strip()]
states=_replay_advances(ar);discoveries=_replay_discoveries(dr)
assert states[ADV]['state']=='PROVED_LOCAL'
assert states[ADV]['owner_id']=='huanjian_gc_20261111_radial_fourth_matrix'
foreign={k:v for k,v in states.items() if k!=ADV};assert len(foreign)==303;assert len(discoveries)==43
older={}
for p in (ROOT/'research-wiki/frontier-cells').rglob('*'):
    if stat.S_ISREG(p.lstat().st_mode) and p!=ROOT/C:older[str(p.relative_to(ROOT))]=sha(p.read_bytes())
assert len(older)==463 and 'research-wiki/frontier-cells/README.md' in older
craw=(ROOT/C).read_bytes();cell=json.loads(craw)
assert cell['status']=='proved_locally' and cell['evidence']['independent_verification']==''
tracked={}
for rawname in git('ls-files','-z').split(b'\0'):
    if not rawname:continue
    name=os.fsdecode(rawname);p=ROOT/name
    if p.is_symlink():tracked[name]={'type':'symlink','sha256':sha(os.readlink(p).encode())}
    elif p.is_file():tracked[name]={'type':'file','sha256':sha(p.read_bytes())}
    elif p.is_dir():tracked[name]={'type':'directory'}
    else:tracked[name]={'type':'missing'}
baseline={'HEAD':HEAD,'advance_ledger_bytes':len(advance_raw),'advance_ledger_sha256':sha(advance_raw),
 'foreign_states':foreign,'foreign_states_sha256':sha(canon(foreign)),
 'discovery_states':discoveries,'discovery_states_sha256':sha(canon(discoveries)),
 'discovery_ledger_sha256':sha(discovery_raw),'older_frontier_files':older,'older_frontier_files_sha256':sha(canon(older)),
 'C':str(C),'C_before':cell,'C_raw_sha256':sha(craw),'tracked_files':tracked,
 'tracked_inventory_sha256':sha(canon(tracked)),
 'git_porcelain_before':git('status','--porcelain=v1','--untracked-files=all').decode()}
(LOCAL/'baseline.full.local-only.json').write_bytes(enc(baseline))
(LOCAL/'advances.prefix.original.local-only.jsonl').write_bytes(advance_raw)
(LOCAL/'discoveries.original.local-only.jsonl').write_bytes(discovery_raw)
(LOCAL/'C.before.original.local-only.json').write_bytes(craw)

plraw=(E/'actual-PROVED_LOCAL-evidence.full.json').read_bytes();assert sha(plraw)=='f4bc0bedf3a46a4232f369a55a28ce88cc33122bd9b2a50419912cc381030773'
appendraw=(E/'actual-PROVED_LOCAL-append.exact.jsonl').read_bytes();assert sha(appendraw)=='a46e0b650bf2aa227cc9b4d2ee322ec06204d947199019ab4575dd76481a6262'
pl=json.loads(plraw);append=json.loads(appendraw)
assert append['evidence']==pl and states[ADV]['latest_evidence']==pl
assert advance_raw.endswith(appendraw)
assert pl['formalizer_preseal_API_pristine'] is False and pl['preseal_exposure']['formalizer_API_pristine'] is False
(OUT/'PROVED_LOCAL-evidence.original.full.json').write_bytes(plraw)
(OUT/'PROVED_LOCAL-append.original.exact.jsonl').write_bytes(appendraw)

source=ROOT/'.astis/huanjian-resume-20261103/2610.20492v1.html'
assert sha(source.read_bytes())=='6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915'
native=E/'native-review/r4_native_7f24'
nr=(native/'portable/original-report.json').read_bytes();assert sha(nr)=='870c960a3d820f74e757d72a0c96937acc56c765dc795cd0c1d208488130fe54'
report=json.loads(nr);assert report['immutable_mathematical_candidate']==MATH and report['reviewer']!=ACTOR
assert report['independence']['formalizer_API_pristine'] is False and report['independence']['pristine_chronology_accepted'] is False
for name,expected in [('portable-custody-manifest.json','f0512103bd6e5a4569689ad24b53fd2d37d1db22078e72adcb774ec7027c1222'),('reproducibility-supplement-v1/supplement-custody-manifest.json','5ffed05db105097591ed374336e09071265f98d3ec742ef0f26cc44521a093b5')]:
    raw=(native/name).read_bytes();assert sha(raw)==expected
    for e in json.loads(raw)['mappings']:
        b=(native/e['destination']).read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256']
cert=json.loads((native/'portable/portable-native-execution-certificate.json').read_bytes())
native_receipts=[]
for p in sorted((native/'reproducibility-supplement-v1/actual-receipts').glob('*.receipt.json')):
    r=json.loads(p.read_bytes());assert r['returncode']==0
    e=next(x for x in cert['successful_actual_receipts'] if x['label']==r['label']);assert sha(p.read_bytes())==e['original_receipt_sha256']
    for suffix in ['stdout','stderr']:
        stream=p.with_name(p.name.replace('.receipt.json','.'+suffix));assert sha(stream.read_bytes())==r[suffix+'_sha256']==e[suffix+'_sha256']
    native_receipts.append(binding(p))
assert len(native_receipts)==6
for name,h in report['pinned_inputs'].items():
    p=ROOT/name;assert sha(p.read_bytes())==h;assert git('show',MATH+':'+name)==p.read_bytes()
for name in ['website/content/declaration_lessons/huanjian-gaussian-radial-fourth-matrix.json','website/content/publications/huanjian-gaussian-radial-fourth-matrix.json','lean-toolchain']:
    assert git('show',MATH+':'+name)==(ROOT/name).read_bytes()
binary=Path('/Users/zhouhuanjian/.elan/toolchains/leanprover--lean4---v4.33.0/bin/lean')
assert sha(binary.read_bytes())==cert['native_toolchain']['binary_sha256']
packagechecks=[]
for entry in cert['all9_packages']:
    pkg=ROOT/'.lake/packages'/entry['name']
    rev=subprocess.run(['git','-C',str(pkg),'rev-parse','HEAD'],check=True,capture_output=True,text=True).stdout.strip()
    porcelain=subprocess.run(['git','-C',str(pkg),'status','--porcelain=v1','--untracked-files=all'],check=True,capture_output=True).stdout
    assert rev==entry['manifest_revision']==entry['actual_revision'];assert not porcelain
    packagechecks.append({'name':entry['name'],'revision':rev,'FULL_porcelain_empty':True})
audit_path=ROOT/'research-wiki/semantic-roundtrip/audits/huanjian-gaussian-radial-fourth-matrix.json'
audit=json.loads(audit_path.read_bytes())
if 'audits' in audit:assert len(audit['audits'])==1;audit=audit['audits'][0]
overlay=json.loads((ROOT/'.astis/semantic-neutral-20261111/r4_src_6aef/anti-anchored-review/audit-overlay.json').read_bytes())
for k,v in overlay.items():assert audit[k]==v
assert audit['publication_binding_sha256']==pl['publication_binding_sha256']=='128fff581c818c13f03d208c546c685e910ade6a30a202e7bee34ce60aa79179'
assert sha((ROOT/audit['source_review']['run_artifact']).read_bytes())==audit['source_review']['review_run_sha256']=='76c1cb645662f496e53e31fabe55d2966ca6bd0cb52f9bfa535b0a267f822f32'
for e in json.loads((ROOT/'.astis/semantic-neutral-20261111/r4_src_6aef/anti-anchored-review/portable-custody-manifest.json').read_bytes())['entries']:
    assert sha((ROOT/e['destination']).read_bytes())==e['sha256']

final_gates=[]
for p in sorted((ROOT/'.astis/huanjian-resume-20261103').glob('20261111T173737*-radial-fourth-matrix-final-reviewed-*.receipt.json')):
    d=json.loads(p.read_bytes());assert d['exit_code']==0;assert d['head_before']==d['head_after']==HEAD
    log=Path(d['log']);assert sha(log.read_bytes())==d['log_sha256'];final_gates.append({'receipt':binding(p),'log':binding(log),'exit_code':0,'assessed':True})
assert len(final_gates)==4

gatecmd=['/opt/anaconda3/bin/python','-B','-c',
 "from tools.astis_publication import check_advance; check_advance(['"+pl['publication_declarations'][0]+"'], reviewed=True); print('Independent normal reviewed publication admission gate passed.')"]
start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
gate=subprocess.run(gatecmd,cwd=ROOT,capture_output=True)
(OUT/'reviewed-publication-gate.stdout').write_bytes(gate.stdout);(OUT/'reviewed-publication-gate.stderr').write_bytes(gate.stderr)
gr={'argv':gatecmd,'cwd':str(ROOT),'started_utc':start,'elapsed_seconds':time.monotonic()-t,'exit_code':gate.returncode,
 'HEAD_before':HEAD,'HEAD_after':git('rev-parse','HEAD').decode().strip(),
 'stdout_sha256':sha(gate.stdout),'stderr_sha256':sha(gate.stderr),'readonly_gate_not_ledger_API':True}
(OUT/'reviewed-publication-gate.receipt.json').write_bytes(enc(gr));assert gate.returncode==0 and gr['HEAD_after']==HEAD
assert (ROOT/'runs/substantive_advances.jsonl').read_bytes()==advance_raw
assert (ROOT/'runs/substantive_discoveries.jsonl').read_bytes()==discovery_raw
assert (ROOT/C).read_bytes()==craw
assessment={'schema_version':1,'phase':'independent-normal-VERIFIED-preflight','actor':ACTOR,'advance':ADV,
 'metadata_HEAD':HEAD,'native_mathematical_candidate':MATH,
 'source_code_audit_reports_exact':True,'source_review_binding':audit['publication_binding_sha256'],
 'current_audit':binding(audit_path),'source_review_report':binding(ROOT/audit['source_review']['run_artifact']),
 'normal_reviewed_publication_gate':binding(OUT/'reviewed-publication-gate.receipt.json'),
 'native_original_report':binding(native/'portable/original-report.json'),'native_successful_receipts':native_receipts,
 'native_manifest':binding(native/'portable-custody-manifest.json'),'native_supplement':binding(native/'reproducibility-supplement-v1/supplement-custody-manifest.json'),
 'final_strict_gates':final_gates,'current_packages':packagechecks,
 'formalizer_API_pristine':False,'pristine_chronology_certified':False,
 'preservation_preconditions':{'foreign_FULL_replayed_states':len(foreign),'discoveries':len(discoveries),'older_frontier_regular_files':len(older),'README_included':True,'current_state':'PROVED_LOCAL','C_independent_verification_preexisting_empty':True},
 'proved_local_original_payload':binding(E/'actual-PROVED_LOCAL-evidence.full.json'),
 'proved_local_exact_append':binding(E/'actual-PROVED_LOCAL-append.exact.jsonl'),
 'normal_transition_API_calls_so_far':0,'decision':'Evidence warrants the single authorized independent PROVED_LOCAL -> VERIFIED transaction for the bounded local scope only.'}
(OUT/'preflight-assessment.json').write_bytes(enc(assessment))
print(json.dumps({'preflight':'accepted','metadata_HEAD':HEAD,'native_candidate':MATH,
 'foreign_FULL_states':len(foreign),'discovery_states':len(discoveries),'older_frontier_regular_files':len(older),
 'native_successful_original_receipts':len(native_receipts),'final_strict_gates':len(final_gates),
 'reviewed_publication_gate_exit':gate.returncode,'preflight_assessment_sha256':sha((OUT/'preflight-assessment.json').read_bytes()),
 'ledger_API_calls':0},indent=2))
