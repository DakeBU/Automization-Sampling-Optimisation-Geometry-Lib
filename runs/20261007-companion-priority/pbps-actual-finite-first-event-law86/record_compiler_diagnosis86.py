from pathlib import Path
import hashlib,json
r=Path(__file__).parent
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest())
receipts=[]
for i in range(1,15):
 p=r/f'focused86.attempt{i}/receipt.json';q=json.loads(p.read_bytes());assert q['terminal_closed'];receipts.append(dict(attempt=i,exit_code=q['exit_code'],receipt=pin(p)))
final=r/'focused-complete86.attempt1/receipt.json';q=json.loads(final.read_bytes());assert q['terminal_closed'] and q['exit_code']==0 and q['public_anchor_implemented']
x=dict(status='COMPILER_API_AND_ELABORATION_ISSUES_RESOLVED_WITHOUT_STATEMENT_CHANGE',sealed_statement_changed=False,attempts=receipts,diagnoses=[
'Attempts1-3: continuous function vs pointwise continuity, real exp continuous API .rexp, and derivative algebra normalization. Internal FTC ingredient then compiled.',
'Attempts4-6: withDensity_apply is in MeasureTheory, not Measure; inf=min is definitional, so no nonexistent inf_eq_min rewrite. Density finite mass/CDF then compiled.',
'Attempts7-10: omega is reserved notation in the enabled scope; use sample binders. Parenthesize real coercion inside lambda. Supply untopD default0, finite WithTop cutoffs, explicit nonnegative coe inequality, and normalize coe0 in survival. Clock mass/CDF then compiled.',
'Attempts11-13: elaboration was expanding the stopped-clock definition during dependent expected-type matching. Explicitly identify the actual joint measurable clock and continuous hazard interfaces and synthesize their composition before matching the goal. No hazard assumption changed. One missing pair of parentheses in the final nonnegativity argument remained.',
'Attempt14: whole public anchor compiled EXIT0. Its old focused runner still carried the earlier partial-scope public_anchor_complete=false flag; that flag is an instrumentation error, not a theorem verdict. Preserve this native receipt unchanged. Successor focused-complete86 runner explicitly exercises the whole anchor and all5 internal lemmas after documentation/linter cleanup; final receipt EXIT0 binds the current exact module.'
],final_authoritative_focused_receipt=pin(final),same_shape_no_progress_loop=False,independent_review='pending',PROVED_LOCAL=False,VERIFIED=False,whole_paper_complete=False)
p=r/'compiler-diagnosis86.json';assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('14 native receipts retained; final full-scope receipt authoritative; no source statement repair')
