"""Finish pre-API intake after binding the preserved frontier boundary explicitly."""
from pathlib import Path
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
src=(W/'complete_gram_intake_after_search_labels.py').read_text()
# Replay only read-only checks/context recovery; no metadata rewriting or file copies.
prefix=src[:src.index('cell=json.loads(C.read_bytes())')]
exec(compile(prefix,'<read-only-preserved-intake-context>','exec'))
cell=json.loads(C.read_bytes());boundary=cell['truth_boundary']
errors=frontiers.validate_cells(frontiers.load_cells());assert not errors,errors
assert not (W/'normal-intake-attempted.once.json').exists()
create(E/'intake-originals/finalize_gram_intake_after_context_binding.py',Path(__file__).read_bytes())
create(E/'intake-originals/intake-context-binding-diagnosis.json',dump({'failure_class':'IMPLEMENTATION_FAILED','previous_continuation_stop':'NameError boundary before proposal construction and before all API calls','correction':'Explicitly recover boundary from unchanged frontier truth_boundary. Shared checks/context are read-only; preserve all existing originals.','new_target_proofs':0,'new_API_calls_before_this_tail':0}))
for p in sorted(Path('.astis/huanjian-resume-20261103').glob('*source-gram-realization-*.receipt.json')):
 r=json.loads(p.read_bytes());lp=Path(r['log']);assert sha(lp.read_bytes())==r['log_sha256']
 for f in [p,lp]:
  dest=E/'intake-originals/actual-runs'/f.name
  if dest.exists():assert dest.read_bytes()==f.read_bytes()
  else:create(dest,f.read_bytes())
main=(W/'start_gram_sau.py').read_text();tail=main[main.index('proposal=advance.AdvanceProposal'):]
exec(compile(tail,'<normal-intake-tail-with-all-explicit-context>','exec'))
