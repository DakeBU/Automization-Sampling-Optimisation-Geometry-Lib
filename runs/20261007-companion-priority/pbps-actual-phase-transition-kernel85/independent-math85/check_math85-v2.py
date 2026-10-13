from pathlib import Path
import json
O=Path(__file__).parent
original=(O/'check_math85.py').read_text(encoding='utf8')
with (O/'reviewer-path-diagnosis85.json').open('x',encoding='utf8',newline='\n') as f:
 json.dump(dict(status='REVIEWER_RUN_SETUP_PATH_ERROR_ONLY',original_script='check_math85.py',observed_exit_code=1,observed_error="FileNotFoundError: E:/Samplinglib/website/content/declaration_publications/pbps-actual-phase-transition-kernel.json",cause='Reviewer input-freeze list used declaration_publications instead of repository publications directory.',scope='Before any compiler invocation; completed exact statement audit and raw/probe outputs retained unchanged. No candidate issue or production change.',native_full_trace_file_claimed=False,repair='This new immutable runner resumes at input-freeze with correct publications path; original script/artifacts retained.'),f,indent=2);f.write('\n')
setup=original[:original.index('raw=M.read_bytes()')]
resume=original[original.index('paths=[M,'):].replace("R/'website/content/declaration_publications/pbps-actual-phase-transition-kernel.json'","R/'website/content/publications/pbps-actual-phase-transition-kernel.json'")
exec(setup+"\np=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhysicalTimeMeasurability.lean'\nprobe=O/'FreshWholeModuleAxiomsKernelClosure85.lean'\n"+resume)
