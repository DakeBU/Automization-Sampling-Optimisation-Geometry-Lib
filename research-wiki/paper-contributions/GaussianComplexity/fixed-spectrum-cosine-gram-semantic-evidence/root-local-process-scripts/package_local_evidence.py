from pathlib import Path
import sys,json
sys.dont_write_bytecode=True;sys.path.insert(0,'.astis/huanjian-gc-fixed-spectrum-detector-20261110')
from lossless_frozen_bundle import archive_exact,put_new,sha
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
E=Path('research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-cosine-gram-semantic-evidence')
R=Path('.astis/huanjian-resume-20261103')
dump=lambda x:(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
files={}
for root in ['.astis/semantic-neutral-20261110/cg_sg_1d7a46','.astis/semantic-neutral-20261110/cg_tc_8f2b60']:
    for p in sorted(Path(root).rglob('*')):
        if p.is_file() and not p.is_symlink():
            assert p.stat().st_mode&0o777==0o444,p
            assert 'PRIVATE' not in str(p)
            files[str(p)]=p.read_bytes()
pre=archive_exact(files,E/'independent-preproof-source-topology-all-phases.lossless-file-bytes.tar.gz')
put_new(E/'independent-preproof-source-topology-archive.json',dump(pre))
files={}
for p in sorted(R.glob('*cosine-gram*.receipt.json')):
    x=json.loads(p.read_bytes());lp=Path(x['log']);b=lp.read_bytes();assert sha(b)==x['log_sha256']
    files[str(p)]=p.read_bytes();files[str(lp.relative_to(Path.cwd()) if lp.is_absolute() else lp)]=b
names=['preseal-planning.json','additional-preseal-source-role-exposure.json','postseal-informal-planning.json','actual-environment-at-seal.json','statement-seal-v1.json','strict-statement-projection.json','StatementFormation.raw.lean.txt','statement-formation.json','producer-signature.draft.txt','consumer-signature.draft.txt','seal_statements.py','reserve_frontier_no_intake.py','prepare_normal_intake.py','admit_normal_intake_prepared.py','prepared-intake-safe-summary.json','normal-intake-attempted.once.json','root-confirmed-actual-intake-success.json','latest-main-owner-after-zero-query-complete-carry.json','producer-proof-v1.body.txt','consumer-proof-v1.body.txt','author_publication.py','attach_independent_decoder_and_map.py','export_selective_fresh_source.py','export_selective_fresh_source.attempt1.executed.py','check_isolated_static_reader.py','package_local_evidence.py','minimal-extra-law-definitions-for-fresh-source.pre-delivery-draft.raw.json','minimal-extra-law-definitions-for-fresh-source.json','minimal-extra-law-definitions.pure-v2.json','fresh-source-c63b08-scope-breach-and-restart.json']
names += [f'producer-attempt-v{i}.raw.lean.txt' for i in range(1,5)]
names += [f'consumer-attempt-v{i}.raw.lean.txt' for i in range(1,4)]
names += ['kernel-attempt-v1.raw.lean.txt']
for n in names:
    p=W/n;assert p.is_file(),p;files[str(p)]=p.read_bytes()
for p in sorted((W/'isolated-static-reader-current').rglob('*')):
    if p.is_file():files[str(p)]=p.read_bytes()
local=archive_exact(files,E/'actual-local-checks-and-authoring.lossless-file-bytes.tar.gz')
put_new(E/'actual-local-checks-lossless-archive.json',dump(local))
retired={}
S=Path('.astis/semantic-neutral-20261110/cg_src_c63b08')
for p in sorted(S.rglob('*')):
    if p.is_file() and not p.is_symlink():
        assert p.stat().st_mode&0o777==0o444,p
        retired[str(p.relative_to(S))]=p.read_bytes()
rr=archive_exact(retired,E/'non-authoritative-source-attempt-c63b08-all-original-files.lossless-file-bytes.tar.gz')
rr.update({'original_actor':'/root/cosine_gram_fresh_source_c63b08','status':'RETIRED_AS_FINAL_FRESH_SOURCE_GATE','authority':'No sourceV. Preserve all raw-source cognition, provisional comparison, real input-scope failures and exposure; not a mathematical refutation. A different actor restarts raw-first.'})
put_new(E/'non-authoritative-source-attempt-c63b08.archive-manifest.json',dump(rr))
diag={'class':'IMPLEMENTATION_FAILED','exact_statement_seal_unchanged_sha256':sha((W/'statement-seal-v1.json').read_bytes()),'no_mathematical_refutation_or_added_hypothesis':True,'proof_attempts':[{'producer1':'Needed explicit Field big-operator import, precise Fin-zero conditional normalization, folded matrix goal and square-root multiplication; source signatures unchanged.'},{'producer2':'One remaining Nat-to-Int zero coercion in a local cosine shorthand; finite-sum normalization errors still retained in full output.'},{'producer3':'Only finite-sum division orientation remained. A native build was started before these same two errors were cleared; that avoidable failed native command and misleading final-native LABEL remain actual failures, not a successful build. No identical native retry was run.'},{'producer4':'Diagnosed actual Finset.sum_div direction from its source, reversed the normalization; direct Lean and later real native P passed.'},{'consumer1':'Explicit transpose-entry reduction and exact vector-mean canonical rewrite were needed.'},{'consumer2':'Only vector mean remained because broad simp rewrote the identity Gaussian to stdGaussian before the desired vector-mean rule.'},{'consumer3':'Directly applied the existing canonical integral_id_multivariateGaussian, preserving all covariance/L2/integrability/internal normalization facts; direct and native complete pair passed.'}],'generated_provider_policy':{'handwritten_roots':2,'actual_owned':26,'generated':24,'all_reachable':True,'meaning':'Tactic certificates only, not24 new mathematical results. No postmerge purification claim.'},'process_attempts':'All anonymous-input regex false-positive, selective-export field-name failure and fresh-source scope breaches/restart are preserved with actual inputs/outputs; no decoder text/source/statement or normal API event was silently repaired.','actual_checks_archive':local['archive'],'original_frozen_source_topology_archive':pre['archive'],'retired_source_archive':rr['archive'],'private_full_foreign_baselines_not_archived':True,'sourceV_global_Goal_credit':False}
put_new(E/'actual-attempts-and-process-diagnostic.json',dump(diag))
print(json.dumps({'preproof_original_files':pre['file_count'],'preproof_archive_sha256':pre['sha256'],'actual_local_original_files':local['file_count'],'actual_local_archive_sha256':local['sha256'],'retired_source_files':rr['file_count'],'retired_source_archive_sha256':rr['sha256'],'private_baselines_exported':False,'sourceV':False}))
