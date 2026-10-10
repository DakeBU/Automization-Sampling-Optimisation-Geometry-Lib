from pathlib import Path
import datetime
import hashlib
import json
import os
import re
import sys

ROOT = Path('E:/Samplinglib')
PRE = ROOT / 'runs/20261007-companion-priority/pbps-b4-perturbation-preproof72'
OWN = PRE / 'independent-header-math72'
EXPECTED = {
    'generic': 'd1435ac883ab1ba0d2b763a8094664d3eba18970a0fa8ff9cd051dc2966fdd8a',
    'actual': 'bb6eaa684a81dbf74d7778e8fa6e98f15c1b443fa3c1e0ec4d2b36560b1ab88d',
}

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def lf(raw):
    return raw.replace(b'\r\n', b'\n')

def canonical_json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(',', ':'), allow_nan=False).encode('utf-8')

def write_json(name, value):
    (OWN / name).write_bytes((json.dumps(value, ensure_ascii=False, indent=2,
                                      sort_keys=True, allow_nan=False) + '\n').encode('utf-8'))

def literal(raw, name):
    text = lf(raw).decode('utf-8')
    start = text.index('private def ' + name)
    end = text.index('\ntheorem ', start)
    return text[start:end].rstrip('\n')

assert not (OWN / 'CLOSED_LAST.json').exists(), 'closed directories are immutable'
OWN.mkdir(parents=True, exist_ok=True)
sources = [
    ('generic', PRE / 'header72.generic.proposed.lean', 'input01.generic.raw.lean', 'full candidate header'),
    ('actual', PRE / 'header72.actual.named-literal.proposed.lean', 'input02.actual.raw.lean', 'full candidate private literal and public theorem type'),
    ('current71', ROOT / 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualCorrectorChange.lean', 'input03.current71.raw.lean', 'full file read; complete private literal and public theorem type checked, implementation not used as mathematical derivation'),
    ('parent70', ROOT / 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualProjectedRotation.lean', 'input04.parent70.raw.lean', 'mathematical inspection restricted to lines 1-143; full finite file preserved only for an exact RAW pin'),
    ('review_guidance', ROOT / '.agents/skills/astis-semantic-roundtrip/SKILL.md', 'input05.review-guidance.raw.md', 'independence and truth-boundary guidance; this is prospective mathematics, not a completed round trip'),
]
raws = {}
inputs = []
for role, path, snapshot, scope in sources:
    raw = path.read_bytes()
    raw.decode('utf-8')
    if role in EXPECTED:
        assert sha(raw) == EXPECTED[role], 'candidate changed: ' + role
    raws[role] = raw
    (OWN / snapshot).write_bytes(raw)
    inputs.append({
        'role': role, 'source_absolute_path': path.as_posix(),
        'snapshot': snapshot, 'bytes': len(raw), 'raw_sha256': sha(raw),
        'crlf_to_lf_only_sha256': sha(lf(raw)), 'inspection_scope': scope,
        'normalization': 'bytes.replace(CRLF, LF) only; no strip, Unicode normalization, or lone-CR replacement',
    })

old = literal(raws['current71'], 'actual_corrector_change_statement')
new = literal(raws['actual'], 'actual_corrector_perturbation_statement')
old_tail = 'C gP gV-C fP fV= -‖fP‖^2+‖fV‖^2)'
new_tail = ('C gP gV-C fP fV= -‖fP‖^2+‖fV‖^2 ∧\n'
            '                                (∀ u v r : HP0,\n'
            '                                  C (u+ΓP0 r) (v-A0 r)-C u v=\n'
            '                                    inner ℝ u (Inv r)+‖r‖^2/2))')
assert new.count(new_tail) == 1
recovered = new.replace('actual_corrector_perturbation_statement',
                        'actual_corrector_change_statement', 1).replace(new_tail, old_tail, 1)
assert recovered == old, 'candidate changed a 71 literal clause'
witnesses_old = re.findall(r'∃ ([A-Za-z0-9_\u0370-\u03ff]+)\s*:', old)
witnesses_new = re.findall(r'∃ ([A-Za-z0-9_\u0370-\u03ff]+)\s*:', new)
assert witnesses_old == witnesses_new
assert witnesses_old[:12] == ['S', 'e', 'U', 'T', 'Γ', 'q', 'ΓP0', 'Inv', 'A0', 'B0', 'V0', 'R']
assert witnesses_old[12:] == ['fP', 'gP']
callers_old = re.findall(r'\((h(?:αβ|α|V|H|βη|η))\s*:', old)
callers_new = re.findall(r'\((h(?:αβ|α|V|H|βη|η))\s*:', new)
assert callers_old == callers_new == ['hα', 'hαβ', 'hV', 'hH', 'hη', 'hβη']

review = '''# Independent prospective-header mathematics review 72

审查人：/root/header_math72。审查对象是两个 exact pinned、无证明且未编译的候选 header；root 是唯一 canonical writer。本目录只提供 prospective-header 数学审核，不是 Lean 编译证据、严格盲解码、paper source review、PROVED_LOCAL、VERIFIED 或 B.4 完成证据。

结论：两个候选均为 **ACCEPT_PROSPECTIVE_HEADER_MATH**；没有发现需要修改数学 statement 的缺条件、假前提或错误符号。最小具体 repair：无。后续 Lean elaboration/implementation/编译和独立 source-facing review 仍须单独完成。此次没有运行 Lean、修改 canonical、Git、ledger 或 Goal，也没有进行 Lean proof search。

## 1. 精确输入与审查隔离

完整有限输入及 exact RAW、CRLF→LF-only SHA-256 见 inputs72.json，并保存五个 RAW 文件。两个候选 RAW SHA：

- generic: d1435ac883ab1ba0d2b763a8094664d3eba18970a0fa8ff9cd051dc2966fdd8a
- actual: bb6eaa684a81dbf74d7778e8fa6e98f15c1b443fa3c1e0ec4d2b36560b1ab88d

两个候选当前没有 CRLF，因此 LF-only SHA 与 RAW SHA 相同。规范化仅做 CRLF bytes→LF bytes，绝不 strip、改 Unicode 或替换独立 CR。

读取了现存 ActualCorrectorChange.lean 的完整 private literal/type；对必要父 API ActualProjectedRotation.lean 的数学检查只到 public type（第143行）。初次工具返回过现存71完整实现，但本推导没有引用其证明步骤。未读任何71审查 verdict/decoder/source 或另一72 source proposal/verdict。另读取 semantic-roundtrip skill 的独立性和真假边界规范；该 skill 的完整编译后 round-trip 工作流没有被冒称已执行。已见候选72具体数学，本 agent 不得再担任 strict blind decoder72。

## 2. 通用实 Hilbert 恒等式

记 I=Inv、K=A I、C(u,v)=(‖u‖²−‖v‖²)/2−⟨K u,v⟩。候选给出有界实线性算子 A,G,I 的自伴性、IG=GI=Id、A I=I A、A²+G²=Id。全部算子在同一个完整实内积空间 H 上。

独立自然公式推导如下，未提供 Lean 证明实现。由 IG=Id 得 K G=A。直接展开两组平方范数与交叉内积：

Δ := C(u+G r,v−A r)−C(u,v)
 = ⟨u,G r⟩+⟨v,A r⟩+(‖G r‖²−‖A r‖²)/2
   +⟨A I u,A r⟩−⟨A r,v⟩+‖A r‖².

实内积的对称性消去 ⟨v,A r⟩−⟨A r,v⟩。A 和 I 自伴给出 ⟨A I u,A r⟩=⟨u,I A² r⟩。A,G 自伴且 A²+G²=Id 给出 ‖A r‖²+‖G r‖²=‖r‖²。又因为 IG²=G，

G+I A²=I G²+I A²=I(G²+A²)=I.

因此 Δ=⟨u,I r⟩+‖r‖²/2，正是候选的符号、参数顺序与系数。特别是 v 项全消，右端无需额外正性、维数、正则性或概率条件。

候选给定结构足够。该展开实际不需要额外使用 hAInv 与 hGInv；它们是可保留的接口冗余，而非缺条件。若另一实现路线需要 A 与 G 交换，现有 A I=I A 和两侧逆已能推出 A G=G A，无需增加 public binder。I 的自伴性也可由 G 自伴与两侧逆导出，但候选已显式给出。Completeness 支持当前 adjoint API；上述自然公式无需新增完备性假设。

结构不是非平凡空间上的空前提：A=0、G=Id、I=Id 满足全部结构；G 不必正，A=0、G=−Id、I=−Id 同样成立。纯 generic leaf 的正确性不需要 B.21 或 actual-reflection 结论作为逻辑父边。

## 3. Actual consumer：caller、同一 witness 与继承条款

private statement 和 public theorem 的六个原 analytic caller 均保持：hα、hαβ、hV、hH、hη、hβη。未把任何 generic algebra 假设交还 caller。有限维实 E、Borel 可测结构、V∈C²、Hessian 的 α/β 双界、α>0、η>0 和 βη≤1 全部逐字保留，没有增加高阶正则性或严格步长端点限制。

十二个全局 common witnesses 仍是同一个原有嵌套作用域中的 S,e,U,T,Γ,q,ΓP0,Inv,A0,B0,V0,R；没有重新选择根或逆，也没有拆成相互无关联的存在量词。fP 和 gP 是原有的两个后续 f-dependent witnesses，不计入十二个全局 witnesses。

实际 f 仍是任意 mean-zero 的 Lp(J) 输入；fP 是其指定 conditional expectation，fperp=R f，fV=V0* fperp。实际输出仍明确为 g=U(P f−(f−P f))，并内部保留 mean-zero、gP 的 conditional expectation、gperp=R g、gV=V0* gperp 与 projected rotation。μ,J,ν,Λ,F、P、M、A、B、ΓP、qP、HP0、γ、Hperp、D 的定义均保留。

机器检查只把唯一新增末尾 conjunct 删除，并把 private def 名改回原名，所得完整 private literal 与当前71 literal 完全相同（仅为比较统一 CRLF→LF）。这不只是核对最后一行：保留了全部概率、kernel、同-law、等距同构、投影、根与逆、polar、D-intertwining、actual-input mean/energy/rotation，以及原 C gP gV−C fP fV=−‖fP‖²+‖fV‖² 的71结论。

新增 ∀u v r 的恒等式是同一 C 作用域内的结论，放在原 gP witness 之后，不是新的前提。供 generic leaf 的内部映射为 H=HP0、A=A0、G=ΓP0、I=Inv：

| generic 所需结构 | actual 候选内部已保留的证据 |
|---|---|
| 实 Hilbert/complete H | HP0 的三个显式 letI；HP0 是 innerSL(qP) 的闭核 |
| A 自伴 | IsSelfAdjoint A0 |
| G 自伴 | ΓP0.IsPositive，故自伴 |
| I 自伴 | IsSelfAdjoint Inv |
| A 与 I 交换 | Commute A0 Inv |
| I G=Id 与 G I=Id | Inv*ΓP0=1 与 ΓP0*Inv=1 |
| A²+G²=Id | A0*A0+ΓP0*ΓP0=1 |

同根边界是 Γ 的正平方根结构，经 e 搬运得到 ΓP，再限制到 HP0 得 ΓP0。其逆仅在 HP0；没有对含常数方向的全部 HP 声称 ΓP 可逆。与当前71的 integration 父边可用于保留旧结论和这组 actual witnesses；新 algebra 本身不依赖 B.21。

## 4. rank-zero 与端点

若 H={0}，所有向量与算子作用都为0，endomorphism 的 Id 也是零映射；两侧逆与平方等式没有矛盾，目标为0=0。若 E 零维导致 actual centered HP0={0}，同样不要求 Nontrivial HP0，‖Inv‖=0≤1/γ。不能因零空间中的单位环退化而额外加入 rank>0。

由 α>0、η>0、α≤β 与 βη≤1 可得 0<αη≤1，因此 γ=2√(αη)/(1+αη) 满足0<γ≤1。允许 αη=1；这时 γ=1。现有 ΓP0≥Id、正性和 A0²+ΓP0²=Id 使 ΓP0=Id、A0=0（零空间亦成立），恒等式退化为 C(u+r,v)−C(u,v)=⟨u,r⟩+‖r‖²/2。没有需要改成 βη<1 的奇点。

η=0 或 α=0 从来不在 actual caller 范围内。generic 在非零 H 上不允许不可逆 G=0；这是显式 inverse 结构的边界，不是隐藏假设。generic 未声称随 G 的谱逼近0得到统一常数。

## 5. 精确数学边界与后续 admissibility

候选为任意 r∈HP0 提供 algebra identity。它没有定义真实 refresh perturbation rρ、对应的真实 perturbed observable/conditional representative、ρ 的分布或 measurable/integrable 结构，也没有声明任意 r 就是真实 rρ。由此不能宣称 actual refresh perturbation 已接通、source B.4 已完成或全-paper composition 已完成。

本审核接受的是 prospective-header 数学：继承当前71命题的同一 witnesses，再内部适用上述 generic identity 的 statement 形状可行。现存71证明/编译历史及候选 Lean elaboration 未在本轮验证；源 Ex28–Ex34 的文字与全部源覆盖也未读，故 source attribution/fidelity 留给隔离的 source reviewer。无需数学 repair；不能把这些待办改写成已证明事实。

## 6. 封存规则

run72.json 的 run_sha256 对整个 logical JSON 计算，只删除顶层 run_sha256；所有其他字段和嵌套内容均保留。规范序列化为 UTF8、ensure_ascii=False、sort_keys=True、separators=(",",":"), allow_nan=False。owned-manifest72.json 固定本目录有限 owned files；CLOSED_LAST.json 是 writer 的最后一次文件写入。随后 writer 直接返回 EXIT0；实际终端 EXIT0 和外部只读 validator 的 PID/EXIT0 通过父任务消息报告，不能写回 CLOSED 目录。
'''

(OWN / 'review72.named.md').write_bytes(review.encode('utf-8'))
write_json('inputs72.json', {'schema': 1, 'inputs': inputs})
checks = {
    'exact_added_tail_occurrences': 1,
    'removing_only_added_tail_and_renaming_private_def_restores_current71_literal': True,
    'six_analytic_callers': callers_old,
    'twelve_global_common_witnesses': witnesses_old[:12],
    'remaining_f_dependent_witnesses': witnesses_old[12:],
    'same_existential_order_and_scope_by_full_literal_equality': True,
    'current71_private_literal_lf_sha256': sha(old.encode('utf-8')),
    'recovered_current71_private_literal_lf_sha256': sha(recovered.encode('utf-8')),
    'candidate_actual_private_literal_lf_sha256': sha(new.encode('utf-8')),
    'lean_implementation_or_proof_search_performed': False,
}
write_json('literal-check72.json', checks)
run = {
    'schema': 1,
    'review_id': 'PBPS-PRE72-INDEPENDENT-HEADER-MATH72',
    'reviewer': '/root/header_math72',
    'review_kind': 'independent-prospective-header-mathematics',
    'utc_timestamp': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'writer_pid': os.getpid(),
    'prospective_header_verdict': {'generic': 'ACCEPT_PROSPECTIVE_HEADER_MATH', 'actual': 'ACCEPT_PROSPECTIVE_HEADER_MATH'},
    'minimum_mathematical_repair': None,
    'compiled': False, 'proved': False, 'source_fidelity_review_completed': False,
    'cannot_serve_as_strict_blind_decoder72': True,
    'inputs': inputs,
    'literal_checks': checks,
    'derived_assumptions_audit': [
        {'generic': 'H real complete inner product space', 'actual': 'HP0 explicit normed/inner/complete letI', 'returned_to_original_caller': False},
        {'generic': 'A selfadjoint', 'actual': 'retained IsSelfAdjoint A0', 'returned_to_original_caller': False},
        {'generic': 'G selfadjoint', 'actual': 'retained ΓP0.IsPositive implies selfadjoint', 'returned_to_original_caller': False},
        {'generic': 'Inv selfadjoint', 'actual': 'retained IsSelfAdjoint Inv', 'returned_to_original_caller': False},
        {'generic': 'Commute A Inv', 'actual': 'retained Commute A0 Inv', 'returned_to_original_caller': False, 'redundant_for_displayed_derivation': True},
        {'generic': 'Inv*G=1', 'actual': 'retained Inv*ΓP0=1', 'returned_to_original_caller': False},
        {'generic': 'G*Inv=1', 'actual': 'retained ΓP0*Inv=1', 'returned_to_original_caller': False, 'redundant_for_displayed_derivation': True},
        {'generic': 'A*A+G*G=1', 'actual': 'retained A0*A0+ΓP0*ΓP0=1', 'returned_to_original_caller': False},
    ],
    'mathematical_boundaries': {
        'rank_zero_allowed': True, 'alpha_eta_one_endpoint_allowed': True,
        'arbitrary_r_identified_as_actual_r_rho': False,
        'full_B4_completion': False,
        'generic_requires_B21_logical_parent': False,
        'actual_can_retain71_integration_parent': True,
        'same_root_same_inverse_same_centered_space': True,
    },
    'independence': {
        'read_current71_review_verdict_decoder_or_source': False,
        'read_other72_sourceproposal_or_verdict': False,
        'reviewed_exact_uncompiled_headers': True,
        'no_external_source_or_recursive_history_copied': True,
    },
    'failed_processes_in_this_review': [],
    'terminal_rendering_note': 'One early ad-hoc stdout displayed Unicode names through a Windows code-page mismatch; the process exited 0 and the files here are explicit UTF8.',
    'named_review_sha256': sha((OWN / 'review72.named.md').read_bytes()),
    'writer_terminal_exit_evidence': 'must be observed from exec terminal; not asserted before writer termination',
    'external_readonly_terminal_exit_evidence': 'reported separately to parent after CLOSED; no post-CLOSED writes',
    'wholelogical_hash_rule': 'remove ONLY the top-level run_sha256, canonical_json entire remaining object, SHA256',
}
run['run_sha256'] = sha(canonical_json(run))
write_json('run72.json', run)

names = sorted(p.name for p in OWN.iterdir() if p.is_file() and p.name not in {'owned-manifest72.json', 'CLOSED_LAST.json'})
manifest = {
    'schema': 1, 'owner': '/root/header_math72',
    'owned_directory': OWN.as_posix(), 'writer_pid': os.getpid(),
    'files': [{'path': name, 'bytes': (OWN / name).stat().st_size,
               'raw_sha256': sha((OWN / name).read_bytes())} for name in names],
    'self_and_close_marker_excluded_to_avoid_hash_recursion': ['owned-manifest72.json', 'CLOSED_LAST.json'],
    'closed_directory_exact_file_set': sorted(names + ['owned-manifest72.json', 'CLOSED_LAST.json']),
}
write_json('owned-manifest72.json', manifest)
closed = {
    'status': 'CLOSED', 'owner': '/root/header_math72', 'writer_pid': os.getpid(),
    'last_file_written': 'CLOSED_LAST.json',
    'manifest_raw_sha256': sha((OWN / 'owned-manifest72.json').read_bytes()),
    'run_sha256': run['run_sha256'],
    'writer_exit_contract': 'no file writes after this marker; return exit 0; actual exit recorded by terminal',
    'utc_timestamp': datetime.datetime.now(datetime.timezone.utc).isoformat(),
}
write_json('CLOSED_LAST.json', closed)
sys.stdout.reconfigure(encoding='utf-8')
print(json.dumps({'writer_pid': os.getpid(), 'run_sha256': run['run_sha256'],
                  'status': 'CLOSED', 'next_action': 'read-only external verification'}, ensure_ascii=True))
sys.exit(0)
