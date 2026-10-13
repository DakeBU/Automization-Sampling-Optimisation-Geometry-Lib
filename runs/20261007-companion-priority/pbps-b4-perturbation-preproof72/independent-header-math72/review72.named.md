# Independent prospective-header mathematics review 72

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
