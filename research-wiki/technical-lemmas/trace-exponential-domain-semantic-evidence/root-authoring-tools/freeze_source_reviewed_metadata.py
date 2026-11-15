from pathlib import Path
import hashlib,json,subprocess,os
r=Path.cwd();w=r/'.astis/huanjian-gc-trace-mgf-domain-20261115'
e=r/'research-wiki/technical-lemmas/trace-exponential-domain-semantic-evidence'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=r,env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'})
assert git('rev-parse','HEAD').decode().strip()=='30172847ec40c24426f0b39afc4887719810eca0'
assert not git('diff','--cached','--name-only').strip(),'Preserve any actual foreign staged work'
b=json.loads((w/'preservation-baseline.private.json').read_text())
for name,h in b['all_existing_frontier_sha256'].items():assert sha(r/name)==h,name
tools=['apply_publication_and_prepare_context.py','author_source_correspondence.py','attach_actual_decodes.py',
 'prepare_reader_preview_v1.py','package_reviewed_native_preproof.py','apply_independent_locator_overlay.py',
 'prepare_safe_public_progress.py','repair_renderer_source_scopes.py','attach_source_review_successor.py',
 'refresh_current_frontier_after_source.py','package_normal_discovery_and_root_runs.py']
for name in tools:
    p=e/'root-authoring-tools'/name;assert not p.exists();p.write_bytes((w/name).read_bytes())
allowed=['research-wiki/frontier-cells/ASTIS-SHARED-REAL-TRACE-EXPONENTIAL-DOMAIN.json',
 'research-wiki/semantic-roundtrip/audits/huanjian-trace-exponential-domain.json',
 'website/content/declaration_lessons/huanjian-trace-exponential-domain.json',
 'website/content/publications/huanjian-trace-exponential-domain.json',
 'research-wiki/technical-lemmas/trace-exponential-domain-semantic-evidence/',
 'runs/substantive_discoveries.jsonl']
changed=git('diff','--name-only').decode().splitlines()
assert all(any(p==a or a.endswith('/') and p.startswith(a) for a in allowed) for p in changed),changed
git('add','--',*allowed)
staged=git('diff','--cached','--name-only').decode().splitlines()
assert staged and all(any(p==a or a.endswith('/') and p.startswith(a) for a in allowed) for p in staged)
assert not any('.atlas' in p.lower() or 'local-private-guards' in p or 'index.private' in p or 'preservation-baseline' in p for p in staged)
git('diff','--cached','--check')
git('commit','-m','Record independent source and native review of Gaussian trace domains')
commit=git('rev-parse','HEAD').decode().strip()
out={'commit':commit,'parent':'30172847ec40c24426f0b39afc4887719810eca0',
 'mathematics_rebuilt_by_independent_native_at':'30172847ec40c24426f0b39afc4887719810eca0',
 'source_binding':'e44190bca918ce5a1e8f4ff5fc942c56ea400deb7a10af9929a698ef22a9d45c',
 'exact_owned_staged_paths':staged,'normal_PL_calls':0,'normal_V_calls':0,
 'typed_CM_normal_validation_calls':1,'reader_runtime':'Running separately; no result/acceptance claimed here',
 'future_identity_build_qualification':'No Lean build of this metadata-only identity claimed; exact P/T unchanged from actually rebuilt immutable301728.'}
p=w/'source-reviewed-metadata-commit.v1.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='exact_owned_staged_paths'}))
