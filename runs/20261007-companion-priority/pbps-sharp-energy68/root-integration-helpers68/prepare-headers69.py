from pathlib import Path
import hashlib, json, subprocess
root = Path.cwd()
r = root / 'runs/20261007-companion-priority/pbps-reflection-rotation-preproof69'
load = lambda p: json.loads(p.read_bytes())
sha = lambda b: hashlib.sha256(b).hexdigest()
primary = load(r / 'root.primary69.adoption.json')
assert primary['source_items'] == 419 and primary['source_only']
assert load(r.parent / 'pbps-root-commutation67/root.exact-verification67.adoption.json')['native_verified']
p = root / 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualRootCommutation.lean'
text = p.read_text(encoding='utf-8')
old_name = 'actual_same_root_inverse_commutation'
name = 'actual_reflection_intertwining'
start = text.index('private def ' + old_name + '_statement')
end = text.index('\ntheorem ' + old_name, start)
definition = text[start:end].rstrip() + '\n'
definition = definition.replace(old_name + '_statement', name + '_statement', 1)
anchor = '                          (∀ f : Lp ℝ 2 J, (∫ z, f z ∂J)=0 →'
assert definition.count(anchor) == 1
addition = '''                          let D : Hperp →L[ℝ] Hperp :=
                            R ∘L U.toContinuousLinearMap ∘L Hperp.subtypeL
                          (∀ h : Hperp, (D h : Lp ℝ 2 J)=
                            U (h : Lp ℝ 2 J)-P (U (h : Lp ℝ 2 J))) ∧
                          V0.adjoint ∘L D = -(A0 ∘L V0.adjoint) ∧
'''
definition = definition.replace(anchor, addition + anchor, 1)
expanded = definition.replace('private def ' + name + '_statement', 'theorem ' + name, 1)
assert expanded.count(' : Prop :=\n    let μ :=') == 1
expanded = expanded.replace(' : Prop :=\n    let μ :=', ' :\n    let μ :=', 1)
callers = definition[:definition.index(' : Prop :=')]
public = callers.replace('private def ' + name + '_statement', 'theorem ' + name, 1)
public += (' : ' + name + '_statement (E := E) (V := V) (α := α) (β := β) (η := η)'
           ' hα hαβ hV hH hη hβη\n')
def write(name_, content):
    target = r / name_
    assert not target.exists(), target
    target.write_text(content, encoding='utf-8', newline='\n')
    b = target.read_bytes()
    return dict(path=target.relative_to(root).as_posix(), RAW_bytes=len(b), RAW_sha256=sha(b),
                LF_sha256=sha(b.replace(b'\r\n', b'\n')))
items = [write('header0-expanded.lean', expanded), write('statement0.definition.lean', definition),
         write('header0-public.lean', public)]
metadata = dict(status='UNSEALED_NEXT_STATEMENT_DRAFT_NO_PROOF_SEARCH',
    source_first_adoption=(r / 'root.primary69.adoption.json').relative_to(root).as_posix(),
    source_graph_SHA256=primary['source_graph_sha256'],
    checked_parent=subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
    existing_verified_parent_RAW_sha256=sha(p.read_bytes()), headers=items,
    target_declaration='AutoSamplingTheory.ExampleCases.ProximalBPS.ReflectionIntertwining.' + name,
    proposed_file='AutoSamplingTheory/ExampleCases/ProximalBPS/ReflectionIntertwining.lean',
    exact_source_delta='All actual micro inputs h:kerP: SAME V0* D h=-A0(V0* h), with D=R U inclusion and its exact original-reflection compression semantics.',
    source_consumers=['B21 actual projected rotation A2.Ex15.m2', 'B4 error-component calculation A2.SS3.p8.m10'],
    retained_source_scope='Original V C2/global alpha,beta Hessians/positive capped eta; rank0 and alphaeta1; SAME actual law/conditional P/reflection U/root/centered inverse/polar V0. All existing parent conclusions retained.',
    no_new_public_premises=True, private_mathematical_providers=[],
    representation='One complete literal private Prop, with exactly original callers. D is the actual bounded compression, not a free operator premise or assumed provider.',
    truth_boundary='Intertwining only; actual centered g=U(P-Pperp)f rotation, B21 corrector change and B4 dynamics are subsequent independent obligations. No sharp-energy68 parent is invented. No main/errors/cost/composition/Exposition/PURIFIED/Goal claim.',
    focused_checks=['lake build AutoSamplingTheory.ExampleCases.ProximalBPS.ReflectionIntertwining'],
    SAU_claim=False, Statement_Seal=False, proof_search=False, compiled_theorem=False)
write('header-draft69.json', json.dumps(metadata, ensure_ascii=False, indent=2) + '\n')
print('Prepared source-first69 unsealed exact actual-intertwining header only; no proof search, SAU claim, or theorem completion.')
