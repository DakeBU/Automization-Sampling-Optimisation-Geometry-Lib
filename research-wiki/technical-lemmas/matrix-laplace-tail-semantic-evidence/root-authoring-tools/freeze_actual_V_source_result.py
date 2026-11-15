from pathlib import Path
import json,hashlib,subprocess,os
r=Path.cwd();w=r/'.astis/huanjian-gc-matrix-laplace-20261114'
E='research-wiki/technical-lemmas/matrix-laplace-tail-semantic-evidence/'
e=r/E;base='999b89925e95e463e0269148010f794dc27bb26a'
env=dict(os.environ,GIT_OPTIONAL_LOCKS='0')
def git(*a):return subprocess.check_output(['git',*a],cwd=r,env=env)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def cp(src,dst):
    dst.parent.mkdir(parents=True,exist_ok=True)
    if dst.exists():assert src.read_bytes()==dst.read_bytes()
    else:dst.write_bytes(src.read_bytes())
assert git('rev-parse','HEAD').decode().strip()==base
assert not git('diff','--cached','--name-only','-z')
n=e/'normal-verification/laplace_native_61e4'
normal=json.loads((n/'normal-V-outcome.public-summary.json').read_text())
assert normal['normal_API_calls']==1 and normal['actual_exit_code']==0
assert normal['original24_top_level_fields_unchanged'] is True
assert sha(n/'normal-V-outcome.public-summary.json')=='c39eda8a5bfb0dd694f12b1e25d13711d30e64168afb1c38be35481f8a367025'
cell='research-wiki/frontier-cells/ASTIS-SHARED-REAL-MATRIX-LAPLACE-TAIL.json'
assert sha(r/cell)=='75ad5982cd285a92c3804fd22b5bfc66af7ba11b17ccb88b177e7ce6596d3b6d'
privacy=w/'metadata-drafts/normal-V-public-selection'
for name,digest in [('normal-V-public-selection.36.v1.json','fe9cbfe641865e3f763ba13959cac8bb21cb09b44f22b96b7e04f141fb1ee2bc'),('normal-V36-selection-privacy-audit.v1.json','d5bf91b222aa5726e8aa107efc25912b17968b2d2523821f37e7caa684598bac')]:
    src=privacy/name;assert sha(src)==digest;cp(src,n/name)
cp(privacy/'privacy-review.v1.md',n/'privacy-review.v1.md')
for name in ['freeze_preV_reader_carrier.py','package_independent_verification36.py','freeze_actual_V_source_result.py','prepare_public_V_progress.py']:
    cp(w/name,e/'root-authoring-tools'/name)
for name in ['preV-carrier.v1.json','preV-actual-gates.v1.json','ROOT-one-independent-V-authorization.v1.json','preV-owned-stage-guard.v1.json']:
    cp(w/name,e/'metadata-custody'/name)
memory=json.loads((e/'local-cycle-memory.json').read_text())
memory.update({'normal_state':'VERIFIED','normal_PL_calls':1,'independent_V_calls':1,'ROOT_V_calls':0,
 'verified_carrier':base,'independent_verifier':'laplace_native_61e4_independent_verifier',
 'normal_V_public_outcome':str((n/'normal-V-outcome.public-summary.json').relative_to(r)),
 'normal_V_portable_resolution':str((n/'ROOT-original-reference-portable-resolution.v1.json').relative_to(r)),
 'cell_projection':'Independent verifier in a second separately guarded window; exact projected cell bytes preserved by ROOT.',
 'public_progress_commit':'3be3742810b87db7d9d8fac485427e97209c5f41',
 'public_scope':'At this source freeze, last actual public transport remains3be; the now-independent-V source result is ready for safe incremental export/privacy review/push. This is not a claim of that future transport.',
 'next':['Safe owned public export and independent actual-candidate privacy/ancestry review','Authorized actual public-ref push and readback','Next exact all-real scalar trace-exponential envelope/domain packet has source/topology admission; target proof/intake remain separate.'],
 'source_identity_qualification':'Actual Lean/native proof build remains immutable1d110. Neither preV999b, this result commit nor public-export identity is retroactively claimed built.'})
(e/'local-cycle-memory.json').write_text(json.dumps(memory,ensure_ascii=False,indent=2)+'\n')
subprocess.run(['python3',str(w/'carry_actual_root_runs.py')],cwd=r,env=env,check=True)
for path in ['runs/substantive_discoveries.jsonl',
 'AutoSamplingTheory/TechnicalLemmas/Probability/MatrixLaplaceTail.lean',
 'Tests/GaussianComplexityLaplaceTail.lean',
 'website/content/declaration_lessons/huanjian-matrix-laplace-tail.json',
 'website/content/publications/huanjian-matrix-laplace-tail.json',
 'research-wiki/semantic-roundtrip/audits/huanjian-matrix-laplace-tail.json',
 E+'PROVED_LOCAL-evidence.full.json']:
    assert (r/path).read_bytes()==git('show',base+':'+path),path
ledger='runs/substantive_advances.jsonl';old=git('show',base+':'+ledger);new=(r/ledger).read_bytes()
append=(n/'normal-V-exact-target-append.jsonl').read_bytes();assert new==old+append
assert hashlib.sha256(append).hexdigest()=='bf3c4ab12753e6eb2a70b70f25efbca7ac23f045373a8b03155bc116935eefd4'
rows=[json.loads(v) for v in append.splitlines()];assert len(rows)==1
assert rows[0]['advance_id']=='ASTIS-SA-20261114-MatrixLaplaceTail' and rows[0]['to_state']=='VERIFIED'
paths={p.decode() for p in git('diff','--name-only','-z').split(b'\0') if p}
paths|={p.decode() for p in git('ls-files','--others','--exclude-standard','-z','--',E).split(b'\0') if p}
assert {cell,ledger}.issubset(paths)
assert all(p in {cell,ledger} or p.startswith(E) for p in paths),sorted(paths)
for p in sorted(paths):
    assert (r/p).is_file() and not (r/p).is_symlink()
    subprocess.run(['git','add','--',p],cwd=r,env=env,check=True)
assert {p.decode() for p in git('diff','--cached','--name-only','-z').split(b'\0') if p}==paths
subprocess.run(['git','diff','--cached','--check'],cwd=r,env=env,check=True)
assert sha(r/cell)=='75ad5982cd285a92c3804fd22b5bfc66af7ba11b17ccb88b177e7ce6596d3b6d'
subprocess.run(['git','commit','-m','Record independent matrix Laplace verification and exact evidence'],cwd=r,env=env,check=True)
commit=git('rev-parse','HEAD').decode().strip();assert commit!=base
assert git('rev-list','--parents','-n','1',commit).decode().split()[1:]==[base]
assert not git('status','--porcelain','--untracked-files=no').strip()
out={'source_result_commit':commit,'parent_preV_carrier':base,
 'actual_independent_normal_V_calls':1,'ROOT_normal_V_calls':0,
 'exact_independent_cell_projection_sha256':sha(r/cell),
 'native_build_identity':'1d1103af694b9663a72b0d610004ed85c7c6b527',
 'source_and_original24_unchanged':True,'safe_public_export_not_yet_executed':True,
 'global_main_site_purification_fullpaper_remaining':True}
(w/'postV-source-result.v1.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
