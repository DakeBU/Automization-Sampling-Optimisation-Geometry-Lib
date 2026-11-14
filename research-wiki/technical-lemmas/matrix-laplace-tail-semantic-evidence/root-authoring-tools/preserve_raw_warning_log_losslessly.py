from pathlib import Path
import json,hashlib,gzip
r=Path.cwd();w=r/'.astis/huanjian-gc-matrix-laplace-20261114'
e=r/'research-wiki/technical-lemmas/matrix-laplace-tail-semantic-evidence'
rel='local-math-originals/20261114T121442230413Z-matrix-laplace-T-confirmed-global-selfadjoint-sum-API.log'
p=e/rel;raw=p.read_bytes();expected='44a5ef4c3922b1aab2a4427c5effb61285df5141df6e2fdb8a798cbdc225bab4'
assert hashlib.sha256(raw).hexdigest()==expected
gz=e/(rel+'.gz');assert not gz.exists();gz.write_bytes(gzip.compress(raw,mtime=0))
assert gzip.decompress(gz.read_bytes())==raw
local=w/'local-only-original-log-copy'/p.name;local.parent.mkdir(exist_ok=True)
assert not local.exists();p.rename(local)
report={'failure_class':'GIT_TEXT_WHITESPACE_CHECK_ON_EXACT_RAW_LOG_NOT_MATHEMATICAL_FAILURE',
 'trigger':'Actual git diff --check rejected three preserved Lean linter lines ending in a space. Raw evidence must not be trimmed or reconstructed.',
 'historical_plain_public_path':str(p.relative_to(r)),
 'historical_exact_public_commit':'b3da3101e19255327ccedbc49730915f578e10e5',
 'current_public_lossless_gzip':str(gz.relative_to(r)),
 'decoded_raw_sha256':expected,'gzip_sha256':hashlib.sha256(gz.read_bytes()).hexdigest(),
 'raw_bytes':len(raw),'direct_original_recorder_log_still_local':'.astis/huanjian-resume-20261103/'+p.name,
 'extra_raw_local_copy':str(local.relative_to(r)),
 'all_original_bytes_including_warning_trailing_spaces_preserved':True,
 'earlier_checkpoint_path_is_historical':'The unchanged original checkpoint cites the historical plain path. This custody record supplies the current gzip resolution; the b3da public original also remains in immutable history.',
 'proof_source_and_actual_receipts_unchanged':True,'new_build_or_verdict':False}
(e/'root-warning-log-lossless-custody.v2.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'raw_bytes_preserved':len(raw),'raw_sha256':expected,'no_raw_normalization':True}))
