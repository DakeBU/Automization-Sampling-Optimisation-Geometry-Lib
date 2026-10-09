from pathlib import Path
import hashlib,json,datetime,os,re
O=Path(r'E:/Samplinglib/runs/20261007-companion-priority/pbps-ambient-adjoint-preproof66/independent-type-diagnosis66')
R=O.parent; H=lambda b:hashlib.sha256(b).hexdigest()
def put(n,d): (O/n).write_bytes((json.dumps(d,sort_keys=True,indent=2,ensure_ascii=True)+'\n').encode('utf-8'))
def pin(p):
 b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');return dict(path=str(p).replace('\\','/'),RAW_bytes=len(b),RAW_sha256=H(b),LF_bytes=len(lf),LF_sha256=H(lf),normalization='CRLF bytes to LF only')
prior=[]
for scope,names in [('independent-header66',['lease.final.json','owned-manifest.json','review-run.json','complete-RAW-decisions.json']),('independent-primary66',['lease.final.json','source-proof-graph.json','source-coverage-inventory.json'])]:
 for n in names:
  p=R/scope/n
  if p.exists(): prior.append(pin(p))
put('closed-parent-reuse-pins.json',dict(schema='diagnosis66-closed-parent-reuse-v1',reuse_mode='exact pins only; no closed writes or repeated broad source audit',parents=prior))
inputmap=json.loads((O/'initial-inputs.json').read_bytes())
inputmap['RAW_LF_maps']=[pin(O/x['snapshot']) for x in inputmap['inputs']]
inputmap['closed_parent_exact_pins']=prior
inputmap['current_checked_parent_commit']='31ce36e7ca01b203696918672c33d29a337550c3'
inputmap['toolchain']='leanprover/lean4:v4.33.0'
inputmap['readback_preparation_pid']=os.getpid()
put('RAW-input-payload.json',inputmap)
contracts=[]
for i in range(2):
 hb=(O/('sealed.header%d.raw.lean'%i)).read_bytes();h=hb.decode('utf-8');split=h.index(' :\n',h.index('(h\u03b7 :'))
 binder=h[h.index('\n'):split];conclusion=h[split+3:]
 # Preserve the complete original body, including terminating newline, as literal bytes.
 pb=(O/('exact-Prop-expression%d.lean'%i)).read_bytes();p=pb.decode('utf-8');marker=' : Prop :=\n';a=p.index(marker,p.index('def exact_Prop_expression'))
 actual=p[a+len(marker):p.index('\n\n#check',a)]
 actual=actual.rstrip('\n');expected=conclusion.rstrip('\n')
 assert actual==expected,(i,'conclusion mismatch')
 pbinder=p[p.index('\n',p.index('def exact_Prop_expression')):a]
 assert pbinder==binder,(i,'binder mismatch')
 (O/('literal-conclusion%d.raw.lean'%i)).write_bytes(conclusion.encode('utf-8'))
 (O/('literal-binders%d.raw.lean'%i)).write_bytes(binder.encode('utf-8'))
 contracts.append(dict(header_index=i,header=pin(O/('sealed.header%d.raw.lean'%i)),original_public_binders=pin(O/('literal-binders%d.raw.lean'%i)),complete_original_conclusion=pin(O/('literal-conclusion%d.raw.lean'%i)),Prop_definition=pin(O/('exact-Prop-expression%d.lean'%i)),binder_bytes_equal=True,conclusion_bytes_equal_except_trailing_newline=True,original_hypotheses=['E real finite-dimensional inner-product normed group with measurable/Borel structure','V : E -> real, C2','alpha,beta nonnegative reals; 0<alpha; alpha<=beta','all x,v Hessian sandwich alpha||v||^2<=D2V(x)[v,v]<=beta||v||^2','eta real; 0<eta; beta*eta<=1 inclusive'],arguments_in_order=['E','all six E instances','V','alpha','beta','eta','h_alpha','h_alpha_beta','h_V','h_H','h_eta','h_beta_eta'],named_target_reapplication='exact_Prop_expression%d (E := E) (V := V) (alpha := alpha) (beta := beta) (eta := eta) h_alpha h_alpha_beta h_V h_H h_eta h_beta_eta'%i,application_is_definitional_unfolding_not_extra_premise=True))
put('exact-binder-conclusion-comparison.json',dict(schema='diagnosis66-exact-header-expression-equivalence-v1',contracts=contracts,source_math_repair=False,proof_ingredient_added=False))
leanbase=Path(r'C:/Users/admin/.elan/toolchains/leanprover--lean4---v4.33.0/src/lean/Lean')
slices=[]
for name,rel,start,end in [('CoreM','CoreM.lean',35,45),('MutualDef','Elab/MutualDef.lean',1232,1245),('PreDefinitionMain','Elab/PreDefinition/Main.lean',340,351),('BuiltinCommand','Elab/BuiltinCommand.lean',698,706)]:
 p=leanbase/rel;b=p.read_bytes();lines=b.splitlines(keepends=True);part=b''.join(lines[start-1:end]);n='lean-option-source.'+name+'.raw.lean';(O/n).write_bytes(part);slices.append(dict(full_source_pin=pin(p),lines_inclusive=[start,end],slice=pin(O/n)))
put('lean-option-source-map.json',dict(schema='diagnosis66-pinned-local-Lean-option-slices-v1',slices=slices,interpretation='Option exists and controls theorem async path. This does not identify the internal free-variable root cause. BuiltinCommand702 only suppresses option display; no unsupported scoped-in inference.'))
put('scope-negatives.json',dict(schema='diagnosis66-scope-negatives-v1',proof_search=False,theorem_proved=False,source_hypotheses_changed=False,canonical_writes=False,Git_ledger_Goal_SAU_writes=False,closed_scope_writes=False,source_candidate66_verdict=False,whole_paper_acceptance=False,PURIFIED=False,full_Exposition=False,blind_decoder_read=False,root_proof_BODY_read=False,root_proof_PID4060_status='Parent reports EXIT0; not independently read or verified here',route_freeze='No repeated unchanged default inline theorem retry; wrapper alternatives retired by distinct bounded probes'))
print(json.dumps(dict(preparation_pid=os.getpid(),contracts_verified=len(contracts),closed_pins=len(prior),Lean_source_slices=len(slices))))