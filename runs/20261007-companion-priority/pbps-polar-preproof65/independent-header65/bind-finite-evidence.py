import os,json,hashlib,re,datetime
from pathlib import Path
O=Path('E:/Samplinglib/runs/20261007-companion-priority/pbps-polar-preproof65/independent-header65');R=O.parent;W=Path('E:/Samplinglib')
def sha(b):return hashlib.sha256(b).hexdigest()
def write(n,v):(O/n).write_bytes((json.dumps(v,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode())
def snap(n,p,b=None):
 full=p.read_bytes();b=full if b is None else b;lf=b.replace(b'\r\n',b'\n').replace(b'\r',b'\n');(O/(n+'.raw')).write_bytes(b);(O/(n+'.lf')).write_bytes(lf);return {'name':n,'source_path':p.as_posix(),'source_full_raw_sha256':sha(full),'source_full_raw_bytes':len(full),'raw_snapshot':n+'.raw','lf_snapshot':n+'.lf','raw_sha256':sha(b),'lf_sha256':sha(lf),'raw_bytes':len(b)}
refs=[];checks=[]
for d,cn in [('type-header65','header.candidate.lean'),('type-consumer65','test.candidate.lean')]:
 rec=json.loads((R/d/'receipt.json').read_text(encoding='utf-8'));refs += [snap(d+'.'+n,R/d/n) for n in ['receipt.json','stdout.log','stderr.log']]
 for n in ['stdout','stderr']:
  b=(R/d/(n+'.log')).read_bytes();assert sha(b)==rec[n]['raw_sha256'] and len(b)==rec[n]['bytes']
 for x in rec['inputs']:
  p=Path(x['path']);assert sha(p.read_bytes())==x['raw_sha256'],p
 for x in rec['input_snapshots']:
  for key in ['exact_raw_snapshot','LF_snapshot']:
   z=x[key];assert sha(Path(z['path']).read_bytes())==z['raw_sha256']
 b=(R/cn).read_bytes();line=b[:b.index(b':= by')].count(b'\n')+1;s=(R/d/'stdout.log').read_text(encoding='utf-8');errs=[{'line':int(a),'column':int(c),'message':m} for a,c,m in re.findall(r'^.*?:(\d+):(\d+): error: (.*)$',s,re.M)]
 assert len(errs)==2 and {x['message'] for x in errs}=={'unknown tactic','unsolved goals'} and all(x['line']>=line for x in errs);assert rec['exit_code']==1 and rec['terminal_closed']
 checks.append({'candidate':cn,'candidate_raw_sha256':sha(b),'body_start_line':line,'errors':errs,'actual_Lean_pid':rec['actual_foreground_pid'],'actual_Lean_exit_code':1,'receipt_checked_science_parent':rec['checked_science_parent'],'all_receipt_and_input_raw_LF_hashes_verified':True,'all_errors_at_or_after_BODY':True,'compiler_success':False,'theorem_compiled':False})
p=W/'AutoSamplingTheory/ExampleCases/ProximalBPS/CenteredRootOrderInverse.lean';b=p.read_bytes();a=b.index(b'theorem actual_centered_root_order_inverse');z=b.index(b':= by',a);refs.append(snap('baseline64.actual.header',p,b[a:z]));base=b[a:z].decode('utf-8')
headers=[(R/n).read_text(encoding='utf-8') for n in ['header0.lean','header1.lean']]
def binder(s):return s[s.index('\n'):s.index('    let μ')]
assert binder(base)==binder(headers[0])==binder(headers[1])
# HP0 CompleteSpace is internal derived structure, the only inserted line in inherited prefix.
cut='                    ΓP0*Inv=(1 : HP0 →L[ℝ] HP0) ∧ ‖Inv‖ ≤ 1/γ'
def inherited(s):
 s=s[s.index('\n'):s.index(cut)+len(cut)];return s.replace('                letI : CompleteSpace HP0 := (innerSL ℝ qP).isClosed_ker.completeSpace_coe\n','')
assert inherited(base)==inherited(headers[0])==inherited(headers[1])
fulls=[(R/n).read_text(encoding='utf-8') for n in ['header.candidate.lean','test.candidate.lean']]
for h,s in zip(headers,fulls):
 a=s.index('\ntheorem ')+1;z=s.index(':= by',a);assert s[a:z].strip()==h.strip()
frags=[('tilted','MeasureTheory/Measure/Tilted.lean',40,63),('lpMeas','MeasureTheory/Function/ConditionalExpectation/AEMeasurable.lean',75,103),('condExpL2','MeasureTheory/Function/ConditionalExpectation/CondexpL2.lean',60,75),('innerSL','Analysis/InnerProductSpace/LinearMap.lean',155,177),('conjStarAlgEquiv','Analysis/InnerProductSpace/Adjoint.lean',894,914),('adjoint','Analysis/InnerProductSpace/Adjoint.lean',97,127),('orthogonalProjectionOnto','Analysis/InnerProductSpace/Projection/Basic.lean',94,120),('IsPositive','Analysis/InnerProductSpace/Positive.lean',260,282),('stdGaussian','Probability/Distributions/Gaussian/Multivariate.lean',51,77),('IsCondKernel','Probability/Kernel/Disintegration/Basic.lean',45,66)]
defs=[]
for name,rp,lo,hi in frags:
 p=W/'.lake/packages/mathlib/Mathlib'/rp;raw=p.read_bytes();lines=raw.splitlines(keepends=True);blob=b''.join(lines[lo-1:hi]);x=snap('definition.'+name,p,blob);x.update({'source_lines_inclusive':[lo,hi],'source_raw_byte_range':[sum(map(len,lines[:lo-1])),sum(map(len,lines[:hi]))]});refs.append(x);defs.append(x)
for n in ['lean-toolchain','lake-manifest.json']:refs.append(snap('environment.'+n,W/n))
write('finite-evidence-inputs.json',{'schema':'header65-finite-evidence-inputs-v1','inputs':refs,'definition_fragments':defs,'compiler_evidence':checks,'baseline64_input_binders_byte_identical':True,'inherited_prefix_through_Inv_byte_identical_after_removing_ONLY_internal_HP0_CompleteSpace_let':True,'candidate_header_exactly_matches_full_file_before_BODY':True,'no_Lean_run_by_this_reviewer':True,'negative_tool_observation':{'tool_chunk':'8a9744','overall_exit_code':0,'warning':'rg explicit wildcard path rejected by Windows; scoped second rg located the exact Tilted.lean file','mathematical_effect':'none'}})
print(json.dumps({'compiler_checks':checks,'baseline64_raw_sha256':sha(b),'binder_match':True,'inherited_prefix_match':True,'definition_fragments':len(defs),'frozen_evidence_inputs':len(refs)},ensure_ascii=False,sort_keys=True))
