from pathlib import Path
import hashlib,json,os
o=Path('runs/20261007-companion-priority/pbps-bounce-rate-preread74');pre=o.parent/'pbps-bounce-rate-preproof74'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def check(z):
 b=Path(z['path']).read_bytes();assert len(b)==z['RAW_bytes'] and sha(b)==z['RAW_sha256'] and sha(b.replace(b'\r\n',b'\n'))==z['LF_sha256'],z['path'];return b
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
lp=o/'lease.final.json';assert sha(lp.read_bytes())=='6489e088c1783b15495899d1234aecd3a490fdaafa578eba4b8924f70a2e2c28'
l=load(lp);assert l['status']=='CLOSED_LAST' and l['owned_files']==26;check(l['manifest']);rows=load(l['manifest']['path'])['owned_files'];assert len(rows)==24
assert {p.resolve() for p in o.rglob('*') if p.is_file()}=={Path(z['path']).resolve() for z in rows}|{lp.resolve(),Path(l['manifest']['path']).resolve()}
for z in rows:
 check(z);assert Path(z['path']).stat().st_mtime_ns<=lp.stat().st_mtime_ns
run=load(o/'run.json');h=sha(can({k:v for k,v in run.items() if k!='run_sha256'}));assert h==run['run_sha256']==l['run_sha256']=='8af15894b1054212a347336eb08b5848469afaa1ceb737dc20632ae26fc795ed'
assert len(run['inputs'])==30
for z in run['inputs']:check(z)
check(l['complete_named']);check(l['decision'])
pre.mkdir(exist_ok=True);adopt=pre/'root.preread74.adoption.json';assert not adopt.exists()
adopt.write_text(json.dumps(dict(status='ACCEPTED_SOURCE_FIRST_PLAN_ONLY_NOT_PROOF',actual_root_PID=os.getpid(),native_whole_logical_run_sha256=h,native_lease=pin(lp),native_complete_named=l['complete_named'],finite_inputs=30,prospective_six_callers=True,VERIFIED=False,Goal_complete=False),indent=2)+'\n',encoding='utf8',newline='\n')
old=Path('runs/20261007-companion-priority/pbps-harmonic-flow-preproof73/header73.proposed.lean').read_text(encoding='utf8')
start=old.index('    {E : Type*}');end=old.index(' : Prop :=',start);binders=old[start:end]
imports='''import AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularization
import Mathlib.Analysis.InnerProductSpace.Projection.Reflection
import Mathlib.MeasureTheory.Constructions.BorelSpace.Basic

/-!
Chen--Chewi--Lu--Zhang arXiv:2609.06905v1, Section2 (reflection), Algorithm1,
AppendixA.1 Ex4--6. Actual zero-safe Borel bounce and energy-layer rate bound.
This statement asserts no random path, clock, Markov kernel or nonexplosion.
-/
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBounceRate
open InnerProductSpace
open scoped ContDiff NNReal Topology
noncomputable section
set_option autoImplicit false

'''
literal=''' : Prop :=
    let c : E → E → E := fun y xRef => y - η • gradient V xRef
    let h : E → E → E := fun xRef x => gradient V x - gradient V xRef
    let R : E → E → E := fun n p =>
      p - (2 * inner ℝ p n / ‖n‖ ^ 2) • n
    let S : E → (E × E) → (E × E) := fun xRef z =>
      (z.1, R (h xRef z.1) z.2)
    let rate : E → (E × E) → ℝ := fun xRef z =>
      Real.sqrt η * max 0 (inner ℝ z.2 (h xRef z.1))
    let H : E → E → (E × E) → ℝ := fun y xRef z =>
      (η⁻¹ * ‖z.1 - c y xRef‖ ^ 2 + ‖z.2‖ ^ 2) / 2
    Measurable (fun a : E × (E × E) => S a.1 a.2) ∧
    Continuous (fun a : E × (E × E) => rate a.1 a.2) ∧
    Measurable (fun a : E × (E × E) => rate a.1 a.2) ∧
    (∀ p : E, R 0 p = p) ∧
    (∀ n p : E, R n (R n p) = p ∧ ‖R n p‖ = ‖p‖ ∧
      inner ℝ (R n p) n = -inner ℝ p n) ∧
    (∀ xRef : E, ∀ z : E × E,
      (S xRef z).1 = z.1 ∧ S xRef (S xRef z) = z) ∧
    (∀ y xRef : E, ∀ z : E × E,
      H y xRef (S xRef z) = H y xRef z) ∧
    (∀ xRef : E, ∀ z : E × E, 0 ≤ rate xRef z ∧
      rate xRef (S xRef z) =
        Real.sqrt η * max 0 (-inner ℝ z.2 (h xRef z.1)) ∧
      rate xRef z - rate xRef (S xRef z) =
        Real.sqrt η * inner ℝ z.2 (h xRef z.1)) ∧
    (∀ xRef x p : E, h xRef x = 0 →
      S xRef (x,p) = (x,p) ∧ rate xRef (x,p) = 0) ∧
    (∀ y xRef : E, ∀ z₀ : E × E,
      0 ≤ H y xRef z₀ ∧
      ∀ z : E × E, H y xRef z = H y xRef z₀ →
        ‖z.2‖ ≤ Real.sqrt (2 * H y xRef z₀) ∧
        ‖z.1 - c y xRef‖ ≤ Real.sqrt (2 * η * H y xRef z₀) ∧
        rate xRef z ≤ Real.sqrt η * (β : ℝ) *
          Real.sqrt (2 * H y xRef z₀) *
          (Real.sqrt (2 * η * H y xRef z₀) + ‖c y xRef - xRef‖))
'''
signature='theorem actual_bounce_rate_energy_laws\n'+binders+' :\n    actual_bounce_rate_energy_statement hα hαβ hV hH hη hβη := by\n'
header=imports+'private def actual_bounce_rate_energy_statement\n'+binders+literal+'\n'+signature
p=pre/'header74.proposed.lean';assert not p.exists();p.write_text(header,encoding='utf8',newline='\n')
q=pre/'header74.typecheck.lean';assert not q.exists();q.write_text(imports+'private def actual_bounce_rate_energy_statement\n'+binders+literal+'\n#check actual_bounce_rate_energy_statement\nend AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBounceRate\n',encoding='utf8',newline='\n')
seal=dict(status='SEALED_BEFORE_PROOF_SEARCH_PENDING_INDEPENDENT_HEADER_REVIEWS',actual_root_PID=os.getpid(),header=pin(p),typecheck_predicate_only=pin(q),private_literal_is_specification_not_provider=True,original_six_caller_prefix_byte_equal_to73=True,original73_header=pin('runs/20261007-companion-priority/pbps-harmonic-flow-preproof73/header73.proposed.lean'),ten_conjunction_clauses=True,zero_extension='Total real division is0 at normal0; separate R0=id and zero-rate clauses force the exact source extension.',source_anchors=['S2.E4.m1','S3.E4.m1','alg1 steps6-7/S3.E9.m1','A1.Ex4--6','A1.SS2.p3 Borel bridge'],source_plan=pin(o/'plan74.json'),truth_boundary='Statement only, no theorem/proof/provider/clock/process/nonexplosion/kernel/main/cost/composition or Goal credit.',no_formal_parent73=True)
(pre/'root.statement-seal74.json').write_text(json.dumps(seal,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('PASS74 source-first CLOSED26 adopted and exact ten-clause statement sealed; NO proof search/implementation. Six binders byte-equal to73.')
