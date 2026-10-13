from pathlib import Path
import datetime,json,os,sys
sys.dont_write_bytecode=True
from math75 import ACTOR,OWN,MODULE,DECL,PARENT,MODSHA,can,sha,load,pin,check,save

assert not (OWN/'lease.final.json').exists()
inputs=load(OWN/'inputs.manifest.json')
for row in inputs['inputs']:
    assert check(row['original'])==check(row['snapshot'])
assert sha(MODULE.read_bytes())==MODSHA
fresh=load(OWN/'fresh-compiler.json')
assert fresh['terminal_EXIT']==0 and fresh['fresh_source_elaboration'] and not fresh['Lake_build_cache_replay']
for key in ['compiler_receipt','axiom_audit_receipt']:
    q=load(fresh[key]['path']);assert q['terminal_closed'] and q['terminal_EXIT']==0
audit=load(OWN/'literal-and-fake-closure-audit.json');assert audit['status']=='PASS' and not audit['fake_closure_hits']
observed=[
    dict(label='prepare-driver',PID=41108,terminal_EXIT=0,stdout_lastline=dict(status='PASS_PREPARE',inputs=14,PID=41108)),
    dict(label='fresh-compiler-driver',PID=32356,terminal_EXIT=0,stdout_lastline=dict(status='PASS_FRESH_DIRECT_SOURCE',Lean_PID=18716,axiom_PID=21324,terminal_EXIT=0)),
    dict(label='literal-fake-closure-driver',PID=37128,terminal_EXIT=0,stdout_lastline=dict(status='PASS_LITERAL_FAKE_CLOSURE',PID=37128,fake_closures=0))]
save('observed-tool-terminals.json',dict(evidence_origin='Actual foreground exec_command terminal completions observed by the independent reviewer; child commands additionally have full RAW stdout/stderr and native receipts.',terminals=observed,no_failed_probe_in_this_body_review=True))
groups=[
 dict(group=1,claim='Joint continuity of the actual integrated hazard',body='151-161',result='correct; joint continuous integrand and parametric finite-interval primitive'),
 dict(group=2,claim='Joint Borel measurability of the actual integrated hazard',body='188',result='correct; follows from group 1 with the actual Borel structure'),
 dict(group=3,claim='Finite-interval integrability of the actual rate along the actual flow',body='162-169',result='correct; continuous real-time integrand, arbitrary finite real endpoints'),
 dict(group=4,claim='Zero initial hazard, nonnegativity and monotonicity on NNReal time',body='170-181',result='correct; rate nonnegative and nested nonnegative intervals'),
 dict(group=5,claim='Exact finite-time threshold-crossing equivalence',body='269-287',result='correct; nonempty closed crossing set, bounded-below infimum membership and monotonicity; empty set yields infinity'),
 dict(group=6,claim='Infinity characterization, finite first-hit equality, positive-threshold positivity and zero threshold',body='288-326',result='correct; continuity/IVT rules out finite overshoot, without a.s.-finite premise'),
 dict(group=7,claim='Joint Borel measurability of actual extended hitting time',body='327-341',result='correct; all extended lower intervals reduce to joint Borel threshold events'),
 dict(group=8,claim='Actual Exp(1) pushforward probability and strict survival',body='342-368',result='correct; exact all-real strict-tail preimage plus exponential CDF, including possible mass at infinity'),
 dict(group=9,claim='Derived nonnegative actual energy cap and integrated cap',body='136-150,182-189',result='correct; actual73 energy conservation and actual74 same-energy rate bound, exact weighted SUM/half/sqrt factors'),
 dict(group=10,claim='Cap waiting lower bound and zero-cap positive-threshold infinity',body='369-390',result='correct; divide only under C>0, preserve infinity and e=0 branches')]
decision=dict(status='ACCEPTED_MATHEMATICS_ONLY',reviewer=ACTOR,actor=ACTOR,checked_parent=PARENT,declaration=DECL,
    ten_clauses_mathematically_correct=True,minimum_mathematical_repair=[],fake_closures=0,
    rank_zero_allowed=True,alphaeta_one_allowed=True,zero_energy_allowed=True,e_zero_allowed=True,infinite_clock_allowed=True,
    original_six_callers_preserved=True,public_telescope_and_private_literal_exact_sealed_v2=True,eight_actual_definitions=True,
    private_primitive_helper_is_proved_not_provider=True,new_public_proof_premises=[],hidden_cap_premise=False,
    hidden_almost_sure_finite_premise=False,WellFoundedLT_used=False,joint_Borel_not_claimed_clock_continuity=True,
    strict_survival_preimage_exact_on_all_real_thresholds=True,separate_support_or_zero_atom_lemma_claimed=False,
    source_review=False,VERIFIED=False,new_VERIFIED_transition=False,new_source_acceptance=False,
    decoder_review=False,reader_acceptance=False,PURIFIED=False,full_Exposition_Seal=False,
    Goal_complete=False,main=False,live=False,whole_paper=False,
    mathematical_groups=groups,
    documentation_debts=[dict(lines='8-9',issue='Frozen introductory comment retains prospective statement only/no theorem proof wording despite the actual compiled proof bodies.',classification='historical documentation only; no mathematical repair and no canonical mutation by reviewer')],
    open_boundaries=['recursive stochastic path construction','independent repeated exponential sampling','nonexplosion','Markov process or terminal-state kernel','invariance or mixing','cost/composition/full paper','source/decoder/reader/purification admissions'],
    no_failed_probe_in_this_bounded_body_review=True)
save('decision.json',decision)
review=(OWN/'named.whole-body-mathematics75.md').read_text(encoding='utf8')
payload=dict(name='Complete independent whole-BODY mathematics75 decision, exact candidate and finite inputs',
    reviewer=ACTOR,checked_parent=PARENT,decision=decision,full_exact_module_UTF8=MODULE.read_bytes().decode('utf8'),
    input_manifest=inputs,full_named_mathematical_review_UTF8=review,fresh_compiler=fresh,
    literal_fake_closure_audit=audit,observed_actual_terminal_completions=observed,
    scope='Mathematics-only; no independent final source verdict, decoder acceptance, VERIFIED or repository publication admission.')
save('complete.named.RAW-payload.json',payload)
run=dict(status='ACCEPTED_MATHEMATICS_ONLY',reviewer=ACTOR,checked_parent=PARENT,source_review=False,VERIFIED=False,
    candidate_module=pin(MODULE),input_manifest=inputs,decision=decision,decision_pin=pin(OWN/'decision.json'),
    complete_named=pin(OWN/'complete.named.RAW-payload.json'),named_review=pin(OWN/'named.whole-body-mathematics75.md'),
    fresh_compiler=fresh,literal_fake_closure_audit=pin(OWN/'literal-and-fake-closure-audit.json'),
    observed_tool_terminals=pin(OWN/'observed-tool-terminals.json'),
    whole_logical_recipe='SHA256 of sorted-key compact UTF8 JSON with ensure_ascii=False and allow_nan=False, removing ONLY top-level run_sha256.',
    LF_pin_recipe='Replace CRLF byte pairs with LF ONLY; RAW remains authoritative, including binary outputs.',
    own_unique_scope=OWN.as_posix(),no_canonical_Git_ledger_site_writes=True,actual_close_writer_PID=os.getpid())
run['run_sha256']=sha(can(run));save('run.json',run)
entries=[pin(p) for p in sorted(OWN.rglob('*'),key=lambda p:p.as_posix()) if p.is_file() and p.name not in {'native.manifest.json','lease.final.json'}]
manifest=dict(entries=entries,entry_count=len(entries),logical_entries_sha256=sha(can(entries)),
    recipe='Sorted relative traversal, entries are complete exact RAW/LF file pins of all owned files except this manifest and the last-write lease; canonical sorted compact UTF8 JSON hash of entries.')
save('native.manifest.json',manifest)
lease=dict(status='CLOSED_LAST',reviewer=ACTOR,actor=ACTOR,VERIFIED=False,writer_PID=os.getpid(),
    writer_terminal_EXIT_contract=0,postclose_owned_writes_forbidden=True,final_owned_write=True,
    manifest=pin(OWN/'native.manifest.json'),owned_files=len(entries)+2,run_sha256=run['run_sha256'],
    closure_logical_sha256=manifest['logical_entries_sha256'],closed_UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    external_readonly_command='math75.py readonly; readonly observer must run after this writer terminal EXIT0, with no owned output writes.')
save('lease.final.json',lease)
print(json.dumps(dict(status='CLOSED_LAST',writer_PID=os.getpid(),owned_files=lease['owned_files'],manifest_entries=len(entries),
    input_count=inputs['input_count'],run_sha256=run['run_sha256'],lease_RAW_sha256=sha((OWN/'lease.final.json').read_bytes()),
    complete_named_RAW_sha256=run['complete_named']['RAW_sha256'],complete_named_RAW_bytes=run['complete_named']['RAW_bytes'],
    logical_entries_sha256=manifest['logical_entries_sha256'],terminal_EXIT_contract=0)),flush=True)
