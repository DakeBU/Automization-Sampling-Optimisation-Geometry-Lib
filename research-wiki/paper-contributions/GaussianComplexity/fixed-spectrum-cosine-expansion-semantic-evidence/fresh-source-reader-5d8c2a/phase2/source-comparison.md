# Phase 2：选择性接口语义比较

独立接口 verdict：**equivalent（在原文继承的 κ≥2 环境内），无阻断语义 delta**。匿名声明与独立盲重建均保留 C.7 的三项结论。私有全 n 接口符合源文有限网格交换步骤的展开形状，是比该步骤所需 n 范围更广的中间式；它不等价于 C.8 的最终闭式，也不承载高斯期望、方差或偏差结论。**整模块、实际 private 状态、证明解除情况和 actual use 保持 HOLD，待另给 Phase 3 输入。**

本稿先核验了 Phase 1 冻结 manifest `20fdcb5cb1d0bd1b224c659ca24e0646ec8e69721aba5b88c156d7a8fb4377fa` 及其中全部文件。未改动 Phase 1。本阶段只收到选择性 payload `ab208db10205167699c1fbe71edf233d90a608716926b350a3997b868bece623` 与其 manifest `cb64dc5b599b074fd3ef588e693035e38d28b7525c37e4037725bae06b37d458`。完整键树先于内容检查；没有实现/module/proof、lesson、current publication context、旧 verdict/delta/repair 或图字段。输入 manifest 的 `source_fidelity_or_independence_verdict: false` 是“本包不授予 verdict”的元数据，不是一个先前结论；其 `excluded` 字段只列禁止内容。manifest 中 whitelist 的 lean/audit 名称是语义路径标签，实际 payload 键为 lean_statement/approved_definition_context；按本次明确授权逐字段核对后，没有额外内容。

## 原文重述与最小定义 context 的独立核对

`source.original_text` 是 root 的合成重述，**不是固定 HTML 的逐字原文**；它的 `text_sha256` 只绑定这段重述，不能替代 951991-byte 原文 SHA-256。本轮复读了原文 `S4.E11`、`S4.Thmtheorem5`、`A3.Thmtheorem7`、`A3.SS3.2`、`A3.Ex140`、`A3.SS3.p4.2`、`A3.Ex138`，用 Phase 1 的原字节/片段哈希定位。

重述里的 λ(θ) 字面定义与 §4.1 的 λ_i 公式一致；其倒数确为 C.7 左端，ρ 的定义与 Lemma 4.5 一致，κ≥2 来自原文环境。关于从 j≥1 到 j+1、第一 N 个正模态、固定 κ 对全部实角度一致收敛的说明，与冻结原文认知和本次匿名声明一致。重述中“bounds/nonzero/summability/uniform convergence are proved internally”是对应有责任分界的说明，**不是本阶段能够确认的实际实现事实**；接口只显示调用者未被要求提供这些 ingredient，是否真正内部解除要在 Phase 3 检查。

四条最小定义 context 均按所展示的字面 statement 独立检查：非负实平方根、实除法/范数/幂/余弦是标准对象；`Finset.range N` 的 0,…,N−1 与 j+1 对应模式 1,…,N；实数项范数的 Summable 表达绝对收敛；`TendstoUniformly ... atTop` 的正 ε、自然数阈值、所有后续 N 与所有实 θ 的量词准确。κ 位于这个一致性断言之外。无自定义项目 predicate 或隐蔽 bundled hypothesis 被提供。未查阅 Lean/Mathlib API，也未编译；以上是字面接口的数学语义核对。

## 七语义槽

| 槽 | 原文 | 匿名 formal | 独立 reconstruction | relation / delta / reason |
|---|---|---|---|---|
| 对象 | 实倒谱函数；ρ=(√κ−1)/(√κ+1)；余弦级数。 | 相同的显式实表达式与 `let r`；无另给代表元。 | 同一定义的 r、a_j、S、S_N；S 与 S_N 是解释用记号。 | **equivalent**；无对象 delta。解码未引入新可选参数或外部指定和值。 |
| 域 | θ∈ℝ；正模态 j≥1；κ 用源文环境。 | κ、θ∈ℝ；j,N∈ℕ；每项频率/幂均 j+1。 | ℕ={0,1,…}，第 j 项是正模态 j+1；空和 S_0=0。 | **equivalent by index shift**；源文第 m≥1 项等于 formal 的 j=m−1 项；无遗漏常数项或重复零模态。 |
| 量词 | 对每个固定允许 κ，每个实 θ 的公式与绝对收敛；对 θ 一致。 | `∀ {κ} (hκ : 2≤κ), let r, (...) ∧ (...) ∧ TendstoUniformly ...`。 | 先 κ、再 r、再三项合取；ε 后选 N₀，N₀ 对全部 θ 和 N≥N₀ 有效。 | **equivalent**；无交换 ∀θ 与 ∃N₀；N₀ 可依赖 κ、ε，不可依赖 θ；未添加跨 κ 一致性。 |
| 假设 | κ≥2 为 §4.1 / Lemma 4.5 环境；ρ 为定义。0<ρ<1 等在源证明中使用。 | 唯一数学 premise 是 hκ；r 为字面 let；收敛在结论中。 | 明确同一唯一 premise；无半径/可和性/指定和值证书。 | **equivalent with inherited premise made explicit**；无 excess binder。接口未把 ingredient 变成调用者前提；其实际证明方式本阶段未知。 |
| 结论 | 展开等式、绝对收敛、对 θ 一致收敛三项。 | 第一合取规定精确和值；第二合取是 norm 项 Summable；第三合取的部分和收敛到同一 tsum。 | 三项逐一重建且各自保持指定对象。 | **equivalent**；无缺项。总化 tsum 的离源情况不扩大本命题含义：本命题同时结论性断言每个 θ 的绝对可和性。源证明 Ex137 的显式上界/收敛率未作为独立源声明要求，故不构成遗漏结论。 |
| 范围/意义 | 最终是实函数等式；全 ℝ 角度一致；复指数只是证明媒介。 | 实余弦、实 tsum、实 norm；uniform limit 是未缩放正模态级数；公式另外保留常数与倍数。 | 同样说明未缩放 S_N→S；无 Gaussian、矩阵、d、n 或概率律。 | **equivalent**；没有把实角度换成有限网格，或把一致性缩成逐点；没有把 C.7 扩成期望/别名闭式。 |
| 常数依赖/归一化 | `2/[κ+1+(κ−1)cosθ]`；括号内 1+2×正模态；外部 1/√κ；(-ρ)^j。 | 四个位置逐字保持，幂/频率同时移位；没有新 C 或外加阈值。 | 同样保留 1、2、1/√κ、负号幂与阈值依赖。 | **equivalent**；无缩放、符号或参数依赖 delta。 |

对 formal↔reconstruction 的七槽复核也未见遗漏或增强。decoder 的解释性文字“没有实质歧义”不是本 reviewer 的依据；判定来自上表与先冻结的原文认知。输入报告 decoder 为 `/root/decode_b4e6a1`，与本 reviewer 不同，并声明 `source_text_visible=false`；本阶段没有打开其 packet/run 原件，因此仅绑定这组已给文本/身份/hash，不把该标志独自当作完整 decoder 独立性认证。

## 私有全 n 中间式

匿名 signature 的域为 d∈ℕ、d≥2、κ∈ℝ、κ≥2、任意 n∈ℕ。`Fin d` 的 0-based i 对应源文 i_source=i.val+1：`(i.val+1/2)π/d` 正是 `(i_source−1/2)π/d`。其 eigenvalue 和 r 与源文字面定义一致；没有除以 d 的平均化。

signature 断言

\[
\sum_i\frac{\cos(n\theta_i)}{\lambda_i}
=\frac1{\sqrt\kappa}\left[
\sum_i\cos(n\theta_i)
+2\sum_{j\ge0}(-r)^{j+1}\sum_i\cos(n\theta_i)\cos((j+1)\theta_i)
\right].
\]

这是把 C.7 的倒谱展开乘以有限确定性权重 cos(nθ_i)，并把有限 i 和与级数交换后的接口形状。n=0 对应无权倒谱和；1≤n<d 对应 `Ex140` 的 μ_n 有限和输入。此层展开本身无需把 1≤n<d 搬到 C.7 的参数中；任意 n 的声明是一条中间式的范围扩大，并非源 C.8 闭式的范围扩大。

相对 `A3.SS3.p4.2`：**faithful algebraic intermediate with generalized n scope**，没有看到调用者收敛前提。相对完整 Fact C.8：**not equivalent / intermediate only**。signature 未含 `∑cos(kθ_i)` 的离散别名值、积化和差、j=n/2ad±n 的类别划分或最终分母 1+r^(2d) 的闭式。其全 n 范围不能给这些仅在指定源范围内推导的分类授予新范围。这个接口也未把有限谱和识别为 M、μ_n 的高斯期望，没有方差、四阶矩、|μ_n|/M 或 d−n≥√κ 条件下的偏差界。

本轮确认的是“匿名私有接口的含义和源文中间步骤相容”。实际声明是否 private、是否由 C.7 构造、是否解除了可和/除法条件、是否被真实消费者调用，以及是否使用了额外全局/scoped 参数，都尚无实现证据；这些保持 Phase 3 HOLD。当前不授予 C.8 或 Lemma 4.5 完成信用。

## 本阶段结论和暴露边界

接口比较通过：`INTERFACE_EQUIVALENT_NO_BLOCKING_DELTA`，修复需求为 none。没有数学 proof、Lean 运行、API 检索或 sourceV。只读白名单 payload/manifest、自己的已冻 Phase 1 与指定固定原文；没有追寻或打开 `parent_canonical_packet_sha256` 指向的完整父包。已明确暴露匿名 formal statement、独立 reconstruction、最小 context、私有消费者 signature 及允许的 source 身份；因此 Phase 2 之后也不作 zero cues 声称。

本轮冻结后暂停；整模块与 actual use 的 HOLD 只能由另给的严格 Phase 3 输入解除。
