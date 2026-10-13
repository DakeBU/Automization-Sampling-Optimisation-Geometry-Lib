from pathlib import Path
import datetime, hashlib, json, re, sys
sys.stdout.reconfigure(encoding='utf8')
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent;C=O.parent
P=C/'independent-elab-review';OLD=C/'independent-source-topology59'
sha=lambda b:hashlib.sha256(b).hexdigest()
canon=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def pin(p):
 b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');return {'path':p.relative_to(R).as_posix(),'bytes':len(b),'lf_bytes':len(lf),'raw_sha256':sha(b),'lf_sha256':sha(lf)}
def put(n,x):
 p=O/n;assert not p.exists(),n;p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode());assert json.loads(p.read_bytes())==x;return pin(p)
def check(v):
 p=Path(v['path']); p=p if p.is_absolute() else R/p
 now=pin(p)
 for k in ['bytes','raw_sha256','lf_sha256']:assert now[k]==v[k],(p,k)
 if 'lf_bytes' in v:assert now['lf_bytes']==v['lf_bytes']
 return p
assert not (O/'lease.open.json').exists()
lease=json.loads((P/'lease.json').read_bytes());assert lease['status']=='CLOSED'
assert lease['actual_readback_exit_code']==0 and lease['resources']['compiler']=='ALL11_TERMINAL_CLOSED'
check(lease['run']);check(lease['receipt'])
prior_run=json.loads((OLD/'reviewer.primary.run.json').read_bytes());h=prior_run.pop('run_sha256');assert sha(canon(prior_run))==h
elab_run=json.loads((P/'run.json').read_bytes());elab_h=elab_run.pop('run_sha256');assert sha(canon(elab_run))==elab_h==lease['run_sha256']
put('lease.open.json',{'schema_version':1,'actor':'/root/next_primary59','status':'OPEN_FOREGROUND_EXACT_OVERLAY_SOURCE_REVIEW',
 'opened_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'external_proposer_closed':True,
 'compiler':'NOT_STARTED','original_source_only_and_topology_unchanged':True})
proposal=json.loads((P/'exact-proposal.json').read_bytes())
assert sha((P/'exact-proposal.json').read_bytes())=='f0d6a01ebe3b8ec9e5dde86f6812cc0d2c313dbe073d2aa589f5ec713a9e1a33'
eq=proposal['exact_compiled_equality'];assert eq['actual_exit_code']==0 and eq['compiler_status']=='CLOSED'
source=check(eq['source']);check(eq['stdout']);check(eq['stderr'])
assert eq==json.loads((P/'phase3/sealed-successor-definitional-equality.status.json').read_bytes())
src=source.read_bytes().replace(b'\r\n',b'\n').decode()
log=Path(eq['stdout']['path']).read_text(encoding='utf8')
assert 'sorryAx' not in log and 'sorry' not in src and 'axiom ' not in src
names=['actual_centered_selfadjoint_defect','actual_centered_defect_coercive_and_unit'];checks=[]
for i,x in enumerate(proposal['headers']):
 op=check(x['original']);sp=check(x['successor']);a=op.read_bytes().replace(b'\r\n',b'\n').decode();b=sp.read_bytes().replace(b'\r\n',b'\n').decode()
 changes=x['changes'];assert len(changes)==x['annotation_occurrences']==[7,4][i]
 parts=[];end=0
 for z in changes:
  s,t=z['start_original_LF_character'],z['end_original_LF_character'];assert s>=end and a[s:t]==z['original']
  assert (z['original'],z['replacement']) in [
   ('(1-T*T)','((1 : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν)-T*T)'),
   ('(1-T0*T0)','((1 : H0 →L[ℝ] H0)-T0*T0)')]
  parts.extend([a[end:s],z['replacement']]);end=t
 parts.append(a[end:]);assert ''.join(parts)==b
 stripped=b.replace('((1 : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν)-T*T)','(1-T*T)').replace('((1 : H0 →L[ℝ] H0)-T0*T0)','(1-T0*T0)')
 assert stripped==a and a.split(' :\n    let μ',1)[0]==b.split(' :\n    let μ',1)[0]
 definitions=[]
 for kind,header,next_decl in [('original',a,f'def annotated_signature{i}'),('annotated',b,f'theorem signatures{i}_definitionally_equal')]:
  expected=header.replace('theorem '+names[i],'def '+kind+'_signature'+str(i),1).replace(' :\n    let μ',' : Prop :=\n    let μ',1).strip()
  actual='def '+kind+'_signature'+str(i)+'\n'+src.split('def '+kind+'_signature'+str(i)+'\n',1)[1].split(next_decl,1)[0]
  assert actual.strip()==expected,(i,kind)
  definitions.append({'name':kind+'_signature'+str(i),'exact_frozen_header_body_matches':True})
 bridge=src.split(f'theorem signatures{i}_definitionally_equal',1)[1].split(f'#print axioms signatures{i}_definitionally_equal',1)[0]
 assert f'original_signature{i} hα hαβ hV hH hη hβη = annotated_signature{i} hα hαβ hV hH hη hβη := rfl' in bridge
 binder_block=a.split('theorem '+names[i]+'\n',1)[1].split(' :\n    let μ',1)[0]
 assert bridge.split(f' : original_signature{i}',1)[0].strip()==binder_block.strip()
 pattern=rf"'[^']*signatures{i}_definitionally_equal' depends on axioms: \[([^\]]+)\]"
 m=re.search(pattern,log,re.S);assert m
 axioms=[q.strip() for q in m.group(1).replace('\n','').split(',')]
 assert set(axioms)=={'propext','Classical.choice','Quot.sound'}
 checks.append({'header_index':i,'original':pin(op),'successor':pin(sp),'replacement_count':len(changes),
 'exact_text_reconstruction':True,'reverse_strip_equals_original':True,'binders_exactly_unchanged':True,
 'definition_source_matches_complete_headers':definitions,'named_rfl':f'AutoSamplingTheory.ExampleCases.ProximalBPS.CenteredDefectOperator.signatures{i}_definitionally_equal',
 'named_rfl_binder_and_body_readback':True,'proposer_compiler_EXIT0':eq['actual_exit_code'],
 'proposer_Lean_PID':next(v['pid'] for v in eq['observed_processes'] if v['exe']=='lean.exe'),'reported_axioms_checked_in_log':axioms})
put('exact-comparison.json',{'schema_version':1,'proposal':pin(P/'exact-proposal.json'),'checks':checks,
 'total_annotation_occurrences':11,'source_body':pin(source),'stdout':pin(Path(eq['stdout']['path'])),
 'compiler_rerun_by_this_actor':False,'evidence_boundary':'Reused proposer CLOSED exact compiler receipt/source/log; independent byte/header/binder/RFL-source/log checking. No new compiler or actual theorem proof.'})

input_files=[P/'exact-proposal.json',C/'header0.lean',C/'header1.lean',
 P/'header0.successor-proposed.lean',P/'header1.successor-proposed.lean',source,
 Path(eq['stdout']['path']),Path(eq['stderr']['path']),P/'phase3/sealed-successor-definitional-equality.status.json',
 P/'receipt.json',P/'lease.json',OLD/'source-statement.preproof-review.json',OLD/'source-proof-graph.json',
 OLD/'source-coverage.manifest.json']
(O/'inputs').mkdir(exist_ok=True);indexed=[]
for i,p in enumerate(input_files):
 op=O/'inputs'/f'{i:03d}.{p.name}.exactraw.snapshot';assert not op.exists();op.write_bytes(p.read_bytes())
 indexed.append({'index':i,'qualified_input':pin(p),'immutable_exactraw_snapshot':pin(op),'copy_exact':p.read_bytes()==op.read_bytes()})
put('input.manifest.json',{'schema_version':1,'indexed_inputs':indexed,'input_count':len(indexed),
 'reference_only_native_runs':[pin(P/'run.json'),pin(OLD/'reviewer.primary.run.json')],
 'native_run_hashes_checked':{'proposer':elab_h,'own_prior_source':h},
 'primary_reuse':'Prior31 source regions/independent graph/source statement kept immutable; no new mathematical/source assumption or topology delta requiring source re-extraction.',
 'recursive_evidence_copy':False,'compiler':'NOT_STARTED'})
review={
 'schema_version':1,'actor':'/root/next_primary59','status':'EXACT_SYNTAX_OVERLAY_ACCEPTED',
 'verdict':'ACCEPT_DEFINITIONALLY_EQUAL_IDENTITY_OPERATOR_TYPE_ANNOTATIONS_NO_SOURCE_REPAIR',
 'proposal':pin(P/'exact-proposal.json'),'original_and_successor_headers':checks,
 'proposer':'/root/whole_math52','proposer_native_closed_run':pin(P/'run.json'),'proposer_native_run_sha256':elab_h,
 'own_prior_source_review':pin(OLD/'source-statement.preproof-review.json'),
 'own_prior_topology':pin(OLD/'source-proof-graph.json'),'own_prior_coverage':pin(OLD/'source-coverage.manifest.json'),
 'independence':'Distinct from overlay creator; own prior source-first extraction reused unchanged. No current59 theorem/proof bodies read; named complete Proposition definitions and their rfl equality controls inspected.',
 'syntax_delta':{'full_identity_type':'Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν','centered_identity_type':'H0 →L[ℝ] H0',
 'receiver_semantics':'ContinuousLinearMap.IsPositive now has an explicitly typed identity receiver; full and centered real operator algebras remain distinct.',
 'positive_API_diagnostic_scope':'Proposer phase4 exact IsSelfAdjoint.one(R) API diagnosis remains scoped compiler evidence; it is not a new theorem hypothesis or accepted complete mathematical proof.',
 'counts':[7,4],'only_eleven_identity_numeral_types_changed':True},
 'binder_definition_fidelity':[
 'All ambient E/real Hilbert/FiniteDimensional(E)/Borel binders and original C2/two-Hessian/alpha<=beta/positive cappedeta retained exactly.',
 'No probability, CFC, selfadjointness, centered preservation, closedness, finiteL2 or Nontrivial binder added; probability/kernel/U/M/T/q/T0 stay derived existential conclusions.',
 'mu/J/nu/Lambda/F/P and literalS density, SAME actual operators andAE representatives unchanged.',
 'Exact qAE1/pairing/Tq=q, H0=ker(innerSL real q), membership integralzero and entire boundedT0 subtype action unchanged.',
 'FullD=I-T*T positivity/constantkernel/quadratic identity and centeredD0 positivity/subtype identity/norm defect unchanged.',
 'Test sharp rho=(1-alphaeta)/(1+alphaeta), delta=4alphaeta/(1+alphaeta)^2 and centered IsUnitD0 unchanged.',
 'Rank0/subsingletonH0 and t1endpoint remain legal; no1-t division or fullD inverse introduced.'
 ],
 'EXCESS_count':0,'mathematical_statement_change':False,'source_assumption_repair':False,
 'source_topology_delta':'NONE; existing reviewed source model/adapters/exclusions retained. This overlay does not grant independent coverage approval beyond prior named coverage reviews.',
 'blockers':[],'accepted_adoption_scope':'Root may adopt these exact successor headers as a separately recorded elaboration clarification while preserving originals, diagnostics and prior source chronology. This does not grant complete theorem/Test proof acceptance.',
 'remaining_boundary':'Full59 theorem/Test proof/compiler/fake-closure/independent proof+source review/commit/integration/publication/purification. Real Gamma positive root/uniqueness/B11/B15/B16, weakH1, halfturn/dynamics/main/errors/cost/composition remain excluded.',
 'PROVED_or_VERIFIED_or_Gamma_admission':False,'compiler_by_reviewer':'NOT_STARTED',
 'diagnostics':'Initial native waiting respected until proposer CLOSED; no compiler launched. Exact raw/LF snapshots and native hashes read back in this review.'}
put('source-overlay-review.json',review)
payload={'payload_name':'independent-source59-exact-elaboration-syntax-overlay',
 'proposal':pin(P/'exact-proposal.json'),'source_overlay_review':pin(O/'source-overlay-review.json'),
 'exact_comparison':pin(O/'exact-comparison.json'),'input_manifest':pin(O/'input.manifest.json'),
 'source_repair':False,'compiler_by_reviewer':'NOT_STARTED','formal_admission':False}
put('named-source-overlay.payload.json',payload)
print(json.dumps({'status':'EXACT_SYNTAX_OVERLAY_ACCEPTED','annotation_occurrences':[7,4],
 'indexed_exactraw_inputs':len(indexed),'named_rfl_equalities':2,'EXCESS':0,
 'compiler_by_reviewer':'NOT_STARTED','scope':'Syntax/API clarification only; no PROVED/VERIFIED/Gamma/fullpaper'}))
