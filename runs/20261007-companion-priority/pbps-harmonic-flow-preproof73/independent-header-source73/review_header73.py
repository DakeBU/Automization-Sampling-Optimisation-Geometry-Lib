from pathlib import Path
import json,hashlib,os,sys,traceback,re
ROOT=Path('E:/Samplinglib');RUN=ROOT/'runs/20261007-companion-priority/pbps-harmonic-flow-preproof73';OWN=RUN/'independent-header-source73'
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_bytes())
def pin(p):
 b=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_sha256':sha(b.replace(b'\r\n',b'\n')),'LF_recipe':'CRLF-to-LF only; preserve all other bytes'}
def write(n,x):
 p=OWN/n;assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
code=0
try:
 assert not (OWN/'lease.final.json').exists()
 h=RUN/'header73.proposed.lean';raw=h.read_bytes();assert len(raw)==3228 and sha(raw)=='a8a7f0f891906e4635d8b77046ee59ddcc3b3cbaeb37f22e6eff00d26b88a27d'
 prior=RUN/'header-typecheck73/header.exactraw.txt';old=prior.read_bytes();assert sha(old)=='9762ae48420d4ed39bdba3b439b1a07216e7661d459b277c167fd0d2244b95eb'
 assert raw.split(b'/-!',1)[0]==old.split(b'/-!',1)[0] and raw.split(b'-/',1)[1]==old.split(b'-/',1)[1]
 s=raw.decode('utf-8');assert s.rstrip().endswith(':= by')
 left=s.split('private def actual_harmonic_flow_statement',1)[1].split(' : Prop :=',1)[0]
 pub=s.split('theorem actual_harmonic_flow_laws',1)[1].split(' :\n    actual_harmonic_flow_statement',1)[0]
 assert left==pub
 assert re.findall(r'\((h\w+)\s*:',left)==['hα','hαβ','hV','hH','hη','hβη']
 assert s.count('    let ')==3
 inputs=[]
 for i,p in enumerate([h,RUN/'header-proposal73.json',RUN/'header-typecheck73/receipt.json',prior]):
  b=p.read_bytes();rd=OWN/f'header-inputs/{i}.exactraw.snapshot';ld=OWN/f'header-inputs/{i}.LF.snapshot';rd.parent.mkdir(exist_ok=True);rd.write_bytes(b);ld.write_bytes(b.replace(b'\r\n',b'\n'));r=pin(p);r.update(RAW_snapshot=rd.relative_to(OWN).as_posix(),LF_snapshot=ld.relative_to(OWN).as_posix());inputs.append(r)
 write('StageB.header-current-inputs73.manifest.json',{'inputs':inputs,'input_count':4,'prior_StageA':'StageA.source-expectations73.before-header.frozen.json remained unchanged and predated this candidate read','typing_credit':'receipt50512 EXIT0 formed target private Prop only; exact later change is one attribution doccomment; neither version is a proved theorem','other_header_math_or_source_verdict_consumed':False})
 labels=[('joint_continuity',[32,33],'Global domain ((E×E)×(ℝ×(E×E))) exactly bundles y,xRef,t,x,p. V/eta fixed; actual center depends on actual gradient. No local/restricted subset or eta=0 claim.',['JOINT-CONT','GRAD-CONT']),('joint_Borel_measurability',[34,35],'Same entire domain and output E×E; finite-dimensional Borel product typing, continuity⇒measurable must be produced internally. No supplied measurability certificate.',['JOINT-CONT']),('initial_identity',[36,36],'For all y,xRef,z, Phi0 z=z. z is arbitrary initial(x,p), not a Gaussian-support restriction.',['INIT']),('all_real_composition',[37,38],'For every real s,t, same y,xRef and z, Phi_(s+t) z=Phi_s(Phi_t z); explicit source-derived all-real extension, needs internal SCALE/TRIG.',['GROUP','SCALE']),('two_sided_inverse',[39,41],'Both Phi_-t(Phi_t z)=z and Phi_t(Phi_-t z)=z with same parameters; consequence of group/init. No arbitrary inverse flow witness.',['GROUP','INIT']),('both_exact_ODE_derivatives',[42,47],'HasDerivAt w.r.t. time only: dX=sqrteta P, dP=−sqrteta^-1(X−y)−sqrteta gradientV(xRef). Fixed reference gradient, not current position gradient.',['ODE-X','ODE-P','DERIVATIVE','CENTER','SCALE']),('nonnegative_exact_energy',[48,48],'Same explicit H and eta>0 give nonnegativity for every phase point; ENERGY dependency repair remains separately reviewed.',['ENERGY','ENERGY-NONNEG']),('energy_invariance',[49,50],'For all real t, H(Phi_t z)=H(z) with same y,xRef. H is weighted SUM of squared E norms, not product max norm. Flow only; no bounce/path credit.',['FLOW-ENERGY','NORM-CANCEL']),('pi_endpoint',[51,52],'Phi_pi z=(2 c−z.1,−z.2); position independent of temporary initial momentum. No random terminal Algorithm1 law.',['HALF-TURN'])]
 lines=s.splitlines()
 # Source ranges below are exact candidate line ranges, inspected rather than
 # inferred proof coverage (candidate has no BODY).
 assert lines[31].strip().startswith('Continuous') and lines[47].strip().startswith('(∀ y xRef') and len(labels)==9
 rows=[]
 for name,(a,b),reason,nodes in labels:
  snippet='\n'.join(lines[a-1:b])+'\n';rows.append({'conjunct':name,'start_line':a,'end_line':b,'candidate_exact_LF':snippet,'candidate_LF_sha256':sha(snippet.encode()),'source_nodes':nodes,'independent_source_decision':'ACCEPT_PROSPECTIVE_CONCLUSION','source_comparison':reason})
 write('StageB.nine-conjuncts-source-review73.json',{'conjunct_count':9,'header':pin(h),'conjuncts':rows,'scope':'complete target literal and public type only; no Lean proof/BODY exists or has been reviewed'})
 write('StageB.actual-binder-definition-review73.json',{'header':pin(h),'six_private_and_public_caller_prefixes_exact_equal':True,'six_names':['hα','hαβ','hV','hH','hη','hβη'],'prospective20_semantic_inventory':'SOURCE4/STANDING6/TYPING10/EXCESS0 retained after coordinate bundling and repeated universal scope expansion','z_coordinate_expansion':'z:E×E universally and without restriction is exactly arbitrary x=z.1 and p=z.2; y/xRef universal separately. hH bound variables x,v have separate local scope.','joint_domain_expansion':'(E×E)×ℝ×(E×E) is right-associated after the first parenthesized pair: a.1=(y,xRef), a.2.1=t, a.2.2=z=(x,p). The displayed projections are exact.','definitions':[{'name':'c','exact':'fun y xRef => y - η • gradient V xRef','source':'S3.E4.m1','decision':'SAME_ACTUAL_CENTER_NO_PROVIDER'},{'name':'Phi','exact':'(c+cos(t)•(x−c)+(sqrteta*sin(t))•p,(-sin(t)/sqrteta)•(x−c)+cos(t)•p)','source':'S4.E5.m1/A1.Ex2.m1+m2','decision':'EXACT_SAME_CENTER_COEFFICIENT_SIGNS'},{'name':'H','exact':'(eta^-1*||x−c||²+||p||²)/2','source':'A1.Ex4','decision':'EXACT_WEIGHTED_SUM'}],'private_Prop_semantics':'literal target specification containing all definitions and nine conclusions, no mathematical provider or additional premise. Public theorem asserts exactly that same literal with six original callers. It ends empty :=by and has no proof credit.','boundary_cases':{'rank0':'all vectors/gradient/norms0; formulas and nine conclusions do not require Nontrivial','alphaeta1':'original<=cap preserved; no 1−alphaeta denominator or strict cap','eta':'positive source scale retained; no extra nonzero convenience binder','zero_energy':'no division by H; fixed(c,0) covered by literal formula','zero_normal':'no bounce normal in header; R0/id and discontinuity stay future excluded'},'existing_gradient_producer':'same imported Calculus.Gradient continuous_gradient_of_contDiff_one can supply joint continuity internally from hV loweredC1 and finite-dimensional completeness','no72_dependency':True,'optional_Flow_packaging':'not required: literal Phi plus two-sided group laws meets source contract; no arbitrary Flow supplied','required_mathematical_or_binder_repair':False,'typing_history_comment_only_change':True})
 print(json.dumps({'actual_pid':os.getpid(),'exit_code':0,'header':pin(h),'nine_conjuncts_checked':9,'six_callers_exact':True,'header_math_or_binder_repair':False,'source_topology_repair_distinct_review_pending':True},indent=2))
except BaseException:code=1;traceback.print_exc()
finally:
 (OWN/'StageB.header-review.terminal.json').write_text(json.dumps({'actual_pid':os.getpid(),'exit_code':code,'argv':sys.argv,'background':False},indent=2)+'\n',encoding='utf-8',newline='\n')
sys.exit(code)
