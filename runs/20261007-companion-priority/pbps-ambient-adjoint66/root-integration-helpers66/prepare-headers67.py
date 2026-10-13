from pathlib import Path
import json,hashlib,subprocess
base=Path('runs/20261007-companion-priority');r=base/'pbps-first-corrector-energy-preproof67';old=base/'pbps-ambient-adjoint-preproof66';current=base/'pbps-ambient-adjoint66'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
assert load(r/'root.primary67.adoption.json')['classified_math_items']==344
assert load(current/'root.exact-verification66.adoption.json')['native_verified']
assert load(current/'integration66/mandatory-astis-check-final/receipt.json')['exit_code']==0
def write(name,s):
 p=r/name;assert not p.exists(),p;p.write_text(s,encoding='utf-8',newline='\n');return dict(path=p.as_posix(),raw_sha256=sha(p.read_bytes()),bytes=p.stat().st_size)
h0='''theorem positive_square_commutation
    {Ω : Type*} [MeasurableSpace Ω] (μ : Measure Ω)
    (G D : Lp ℝ 2 μ →L[ℝ] Lp ℝ 2 μ)
    (hG : G.IsPositive) (hD : D.IsPositive)
    (hCommute : Commute (G*G) D) : Commute G D
'''
h=(old/'header0.lean').read_text(encoding='utf-8')
assert h.startswith('theorem actual_ambient_adjoint_centered_decomposition')
h=h.replace('theorem actual_ambient_adjoint_centered_decomposition','theorem actual_same_root_inverse_commutation',1)
a='Γ.IsPositive ∧ Γ*Γ=(1 : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν)-T*T ∧'
assert h.count(a)==1;h=h.replace(a,a+'\n              Commute Γ T ∧',1)
a='ΓP.IsPositive ∧ ΓP*ΓP=(1 : HP →L[ℝ] HP)-A*A ∧'
assert h.count(a)==1;h=h.replace(a,a+'\n              Commute ΓP A ∧',1)
a='Inv*ΓP0=(1 : HP0 →L[ℝ] HP0) ∧\n                    ΓP0*Inv=(1 : HP0 →L[ℝ] HP0) ∧ ‖Inv‖ ≤ 1/γ ∧'
assert h.count(a)==1
extra='''
                    IsSelfAdjoint Inv ∧
                    ∃ A0 : HP0 →L[ℝ] HP0,
                      (∀ u : HP0, (A0 u : HP)=A (u : HP)) ∧
                      IsSelfAdjoint A0 ∧ Commute A0 ΓP0 ∧
                      A0*A0+ΓP0*ΓP0=(1 : HP0 →L[ℝ] HP0) ∧
                      Commute A0 Inv ∧'''
h=h.replace(a,a+extra,1)
t=h.replace('theorem actual_same_root_inverse_commutation','theorem genuine_actual_corrector_coefficient_consumer',1)
a='Commute A0 Inv ∧';assert t.count(a)==1
t=t.replace(a,a+'''\n                      IsSelfAdjoint (A0*Inv) ∧
                      (1 : HP0 →L[ℝ] HP0)+(A0*Inv)*(A0*Inv)=Inv*Inv ∧''',1)
headers=[write('header0-expanded.lean',h0),write('header1-expanded.lean',h),write('header2-expanded.lean',t)]
definitions=[]
for i,s in enumerate([h0,h,t]):
 name=s.splitlines()[0].split()[1];definition=s.replace('theorem '+name,'private def '+name+'_statement',1)
 if i==0:definition=definition.replace(' : Commute G D',' : Prop := Commute G D',1)
 else:
  marker=' :\n    let μ :=';assert definition.count(marker)==1;definition=definition.replace(marker,' : Prop :=\n    let μ :=',1)
 definitions.append(write(f'statement{i}.definition.lean',definition))
metadata=dict(status='UNSEALED_NEXT_STATEMENT_DRAFT_NO_PROOF_SEARCH',source_first_adoption=(r/'root.primary67.adoption.json').as_posix(),source_graph_RAW_sha256=load(r/'root.primary67.adoption.json')['source_graph_sha256'],checked_parent=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),headers=headers,private_literal_Prop_definitions=definitions,private_mathematical_providers=[],original_paper_callers_unchanged=True,auxiliary_positive_D='Reusable background leaf only. Actual consumer proves positivity of D=I+T internally from the actual selfadjoint contraction; no paper binder or certificate is added.',actual_delta='SAME Gamma/T commutation, SAME transported GammaP/A commutation, internally produced exact centered restriction A0, same Inv selfadjoint and centered commutations; genuine B23 coefficient selfadjointness and square identity consumer.',truth_boundary='No sharp B23 bound or full B21 rotation/energy identity, no full modified-energy/H1/dynamics/main/errors/expected costs/actual-input composition, no Goal completion.',representation='Private full literal proposition definitions only, reusing independently reviewed66 dependent-elaboration staging; no theorem is assumed or proved. Whole-module fresh review will be required after implementation.',SAU_claim=False,Statement_Seal=False,proof_search=False,compiled_theorem=False)
write('header-draft67.json',json.dumps(metadata,ensure_ascii=False,indent=2)+'\n')
print('Prepared source-derived67 unsealed header drafts only; original callers and actual objects retained, no proof or SAU claim.')
