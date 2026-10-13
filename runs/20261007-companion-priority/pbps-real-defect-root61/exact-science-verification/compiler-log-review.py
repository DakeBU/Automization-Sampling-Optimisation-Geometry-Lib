from common import *
import re
build=J(P/'focused.status.json'); assert build['exit_code']==0 and build['terminal_closed']
log=(P/'focused.stdout.log').read_text(encoding='utf8'); records=re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]+)\]",log)
assert len(records)==4 and all([a.strip() for a in v.split(',')]==['propext','Classical.choice','Quot.sound'] for n,v in records),records
assert 'sorryAx' not in log and 'Build completed successfully (3916 jobs).' in log
W(P/'compiler-parser.0.diagnosis.json',dict(status='PARSER_NEGATIVE_PRESERVED',actual_tool_chunk='749802',wrapper_PID=26148,wrapper_exit=1,compiler_PID=38692,compiler_exit=0,original_script=pin(P/'compile.py'),failure='Post-compiler parser assumed exactly two single-line axiom records; actual replay includes four wrapped parent/public records.',repair='Distinct read-only parser accepts exact bracket-delimited standard3 records; no compiler reinvocation, no proof change.'))
W(P/'compiler.json',dict(status='PASS',checked_commit=SCI,focused=build,source_pre=pin(P/'compiler.inputs.before.json'),source_post=pin(P/'compiler.inputs.after.json'),toolchain=pin(P/'toolchain.pin.json'),axiom_records=[dict(declaration=n,axioms=[a.strip() for a in v.split(',')]) for n,v in records],compiler='CLOSED_EXIT0',one_nonforced_invocation=True,parser_negative=pin(P/'compiler-parser.0.diagnosis.json'),actual_log_reviewer_PID=os.getpid(),scope='Focused target only; full mandatory root and aggregate deferred to serialized integration'))
print('ACTUAL_COMPILER_CLOSED',build['actual_PID'],'EXIT0',len(records),'standard3 records')
