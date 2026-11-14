# PHASE2：匿名命题与实际 blind reconstruction 的独立来源比较

状态：`PROVISIONAL_EQUIVALENT_FOR_BOUNDED_ACTUAL_INTEGRAL_CORE`。这不是 Lean 编译证据、canonical audit 接受、最终 source V、PROVED_LOCAL 以上的状态转换或全 C.4 完成证明。PHASE1 原始来源契约保持原字节；本阶段没有倒改先前来源分析。

独立来源 reviewer：`/root/norm_fresh_source_640251`。唯一新增数学输入是父任务授权的 `phase2-selective-input.json`，17991 bytes，raw SHA256 `a095955e5c9a8740de8af494335507ec201ab4407cc5854986fc7a37f506c10c`。它包含匿名命题、plain minimal standard meanings、实际独立 decoder `/root/decode_691853` 的原样 reconstruction，以及 run/exposure 的机械字段投影。没有打开这些字段提及的原始 run、旧文件或实现路径。

PHASE1 manifest SHA256 `37aa749167ad7e814f36e4d2e1028e9b5316ab2326edcd0205efb1c1a2f5f2ec`，独立来源分析 SHA256 `f984c0d2414a1284009d476f341563365c752333529990b33f53e1db7f7d1e48`。本阶段比较依据是已经冻结的来源含义，而不是根据候选重写来源。

## 1. 字面命题究竟断言什么

对所有自然数 `d≥2`、实参数 `κ≥2` 与完整实正交群中的 `O`，局部定义零起始下标的余弦谱、其正交共轭 `A` 及实际权函数

`w(x)=exp(−(Σ_i x_i(Ax)_i)/2)=exp(−xᵀAx/2)`。

字面结论恰为合取：

1. `Integrable w volume`；
2. `∫_(R^d) w(x) dx = (2π)^(d/2) / sqrt(∏_i λ_i)`。

这里 `volume` 的批准最小语义是标准未归一化 Euclidean Lebesgue measure。`d/2` 是实数除法和实指数，没有奇数维整除问题。积分与可积性针对同一 weight 和同一 measure。`Integrable` 位于结论，未成为额外前提。

命题没有字面断言：`det A=det Λ`、`det Λ=∏λ_i`、目标概率分布是 `N(0,A⁻¹)`、某个 formal object `Z_A` 等于该积分、一个算法已获知谱/常数、完整 C.4 的正则性/极小点结论或任一 sampling lower bound。不能将 reconstruction 中的进一步数学解释冒充这些内容都已是 Lean conjunction 的一部分。

## 2. 七槽逐项比较

### Objects

**冻结来源：** S2/S4 的 `A` 是 precision，实际势为 `f_A=V_A=xᵀAx/2`，目标为 `N(0,A⁻¹)`；固定 Eq11 谱 `Λ` 经完整正交群旋转给 `A`。C.4 normalizer 是这一实际势的常数。

**匿名字面命题：** 局部定义的 `A=O·diag(diagonalValue)·Oᵀ` 与 `w=exp(−xᵀAx/2)` 正确保留实际 precision/potential 对象；所有乘法顺序正确。没有通过 project-owned alias 隐藏另一权函数、常数偏移势或外加归一化因子。没有把 `A` 改成 covariance。标准 `EuclideanSpace/WithLp.ofLp` 的批准语义只提供原向量的坐标。

**decoder：** 正确读成未归一化高斯型 weight；引入 `D` 是 diagonal 矩阵的说明性简写，不是另加存在对象。它没有声称 Lean 已命名/构造一个 Gaussian probability law。这与字面命题相符。

**结果：** bounded integral core 对象匹配。命名的 `Z_A` 与 `N(0,A⁻¹)` 关系仍属于 wider source-context obligation，而不是候选已有的字面结论。

### Domains

**冻结来源：** Eq11/C.4 使用整数 `d≥2`、实 `κ≥2`、`i=1,…,d`、`O∈O(d)`、`x∈R^d`。来源其他区域的 `d≥1,κ≥1` 一般精度类不能替换这一限定域。

**匿名字面命题：** `d:ℕ` 且 `2≤d`、`κ:ℝ` 且 `2≤κ`，完整实 orthogonal group，所有实 Euclidean vectors，完全一致。`Fin d` 的 `i.val=0,…,d−1` 对应来源 `j=i.val+1`，故 `(i.val+1/2)π/d` 对应 `(j−1/2)π/d`；乘积和坐标均只是同一 d 项的重编号。group 要求转置两侧乘积为 identity，与有限方阵的标准完整正交群含义相同，并未限制到 determinant-one subgroup。

**decoder：** 重编号、实 κ、奇数维实指数、完整 group 的两种 determinant sign 均正确，没有扩张到任意 SPD 矩阵或任意谱。

**结果：** 数学域一致，只有纯表示差异。没有把来源边界扩大到 `d<2`、`κ<2`、复数或不同测度。

### Quantifiers

**冻结来源：** 先固定 `d,κ` 与具体公开谱，再对每个 `O`，形成同一实际势家族；normalizer 恒等式是 pointwise-in-O，不是高概率事件。Haar/seed 独立性仅属于 lower-bound input experiment。

**匿名字面命题：** 隐式 `d,κ` 仍为全称量词；`hd,hκ` 只是不等式证明参数；`O` 全称。四个 let 是确定定义，覆盖同一合取结论，不是额外假设或存在量词。没有在两个 conjuncts 间重选参数。

**decoder：** 正确区分这一 deterministic identity 与随机抽取 O；没有加 Haar、independence 或算法输入的前提。

**结果：** 量词一致。省去 Haar 不是来源缺失：normalizer identity 本身适用于每个 O。不能从这种正确省略反过来声称整个 sampling lower-bound 随机实验都已形式化。

### Assumptions

**冻结来源：** 仅需来源 d/κ 域、Eq11 构造与 O 正交；正谱、正定性、可积性及 determinant identity 是构造的结果/内部桥，不应新增为 public premises。

**匿名字面命题：** 没有 integrability、Gaussian integral evaluation、determinant identity、额外 regularity、oracle、概率 good event 或 positivity witness 的前提。weight 的真实公式完整显露。批准标准语义说明 real sqrt/division/integral 的 totalization，没有额外输入一个非零条件。

**decoder：** 随后解释 positivity、SPD、determinant identity 均可由输入得到；它正确标为派生事实，未把它们纳入假设。来源 C.4 已给严格谱区间，所以这些解释与独立冻结的来源认识一致。但这些 decoder prose 不是这些事实的 Lean 编译证据。

**结果：** 未发现 excess binder。可积性从 source-implicit finite normalizer 变成明确结论，是定义意义的显式保留，不是给来源加条件。

### Conclusion

**冻结来源：** Ex160 显示 `(2π)^(d/2)(det A)^(−1/2)=(2π)^(d/2)(det Λ)^(−1/2)` 作为实际势的 `Z_A`；紧随 `O` 独立与 spectrum public 时 known。

**匿名字面命题：** 结论为实际 weight 的可积性与积分等于谱乘积平方根分母。它确实评价实际积分，既没有把 Z 仅定义成 desired RHS，也没有把 integral identity 放进前提。

`det(diag λ)=∏λ_i`、正交 determinant invariance、正数上的 inverse-square-root 记法，是它与来源两种 determinant 表达式对照所需的标准等价桥。严格正谱来自同一来源域，平方根取正支，不构成新来源假设。

**decoder：** 对 literal conjunction 的主陈述正确。它另说 `det A=∏λ_i`、正性和 `O` 不变性，属于 derived commentary；不能报告成候选逐字包含三条额外 theorem conclusions。

**结果：** 在“实际积分的 scalar value”这一 bounded normalizer core，乘积写法与来源值数学等价；不属于字面逐符号 exact。对整条 Ex160 determinant chain、formal Gaussian-law density link 和 algorithmic known predicate 的 blanket acceptance，当前输入不充分。这里保留 scope/deduction residuals，而非假装这些命题已是当前 Lean statement 的 conjuncts。

### Scopes and senses

**冻结来源：** 来源用“Gaussian integration/normalizing constant”，但限定原文没逐字定义 `Z=∫exp(−V)dx`。PHASE1 已将 Lebesgue partition-function 读法明确列为标准约定推断，而非来源逐字定义。

**匿名字面命题：** 直接明确了整空间 Euclidean Lebesgue measure 与未归一化 weight，符合该冻结标准约定；不存在相对于 normalized Gaussian law 的期望或球面/截断积分。`1/2` 与 `2π` 配对正确。可积性 conclusion 防止把 Bochner integral 的不积分时零默认值当作完整高斯积分评价。

**decoder：** 对以上量/measure 和 totalization 的辨别正确。它拒绝将该命题扩大为 named probability law、采样复杂度或误差界，符合实际 input。

**结果：** 没有发现 measure/sense 漂移。来源 convention 的非逐字性仍诚实保留；当前 candidate 是该 convention 的清楚实现，而不是让 candidate 倒过来“证明”来源原文曾明写 dx。

### Constant dependencies

**冻结来源：** normalizer 只依赖维数与完整确定谱，Eq11 家族因此只依赖 `d,κ`；不依赖 O、seed、算法、ε 或 δ。

**匿名字面命题：** RHS 只用 `d,κ`，含全谱有限积、常数 `2,π` 和实指数，直接具有同一依赖关系。无隐藏大 O 常数、`d₀` 或误差参数。weight 和 A 仍依赖 O，这不与积分值 O-independent 混淆。

**decoder：** 将 O-independent value 说明为相同 RHS 的派生性质，正确；并未声称每个 O 得到同一 pointwise weight。它也正确说 κ 是输入上界参数，不强行定义为精确 condition number 或精确 maximal eigenvalue。

**结果：** 数值依赖匹配。公开数据可确定 scalar 的数学意义由这个依赖支持；具体算法“知道”的 model predicate 未在 statement 中形式化。

## 3. 字面结论与 decoder 派生说明的边界

| 内容 | 字面候选中位置 | decoder 中的位置 | 本 reviewer 的判断 |
|---|---|---|---|
| weight 的真实二次指数公式 | 四个 let 中的 weight | 直接重述 | 一致。 |
| 可积性 + actual integral/product formula | 唯一合取结论 | 明确编号 (1)(2) | 一致。 |
| strict λ bounds、SPD、w>0、sqrt denominator>0 | 不是额外 conclusion/conjunct | 后续“可由输入推出” | 来源支持的派生说明；不能据 prose 计为已编译叶子。 |
| `det A=∏λ_i` | 不在字面 conclusion | 明确称派生等价改写 | 数学上符合来源，但需 determinant bridge；没有因 decoder 说明而自动变成该 Lean theorem 的字面 assertion。 |
| value independent of O | 由全称 O 和相同 RHS 的确定依赖得到 | 正确说明 derived property | bounded core 的直接语义后果；未见单独 invariance declaration，亦不要求这一层才能理解本命题。 |
| `N(0,A⁻¹)` 的 formal law/density link | 未出现 | 明确未主张 named probability law | 保留 wider source-context obligation。 |
| public spectrum 时 algorithm knows Z | 未出现 formal algorithm/knowledge | 仅谈显式数值依赖，无算法 claim | 只能支持数学数据依赖，不给 oracle/runtime/TV theorem。 |

不存在需要更改来源数学前提才能解释候选的差异；没有提出 repair。存在表述层面的真实差别和范围边界，见 typed delta 文件。它们不能被 `compiled:true` 或 decoder 的派生 prose 抹去。

## 4. 对 blind decoder 的 ambient historical labels 的诚实评估

输入中的 exposure record 明确不是“零 ambient 信息”。decoder 可见 repo/cwd/packet/task labels，以及历史 permission text 中 `fixed-spectrum-query`、`fixed-spectrum-determinant`、`fixed-spectrum-admissibility`、Eq6、Ex70/71/72、GC integration、Gaussian-affinity branch、GitHub numbers 等字符串。这些是实际的主题/身份线索，可能使人联想到已有 Gaussian/fixed-spectrum 工作；它们具有一般 anchoring 风险，不能因为未打开文件就当作不存在。

同一记录指出：没有打开这些标签指向的文件，没有读取 source/production/Test/proof/audit/other-agent record，也没有搜索或尝试定位来源；当前 source title、version、anchor 和 target declaration 没有显式提供。Eq6/Ex70 等是历史标签，现有证据不能将它们等同于当前 C.4/Ex160 锚点。匿名 packet 本身没有当前 source/audit/declaration identity；其 mathematical structure 本身当然可被辨认，这是 reconstruction 的允许输入。

可支持的限定结论为：**依据所供 run/exposure 记录，这是 source-text-blind reconstruction，带有已披露的 repository/historical-label ambient identity cues；不是强意义的完全无身份线索实验。** 未发现当前原文、exact source identity/anchor/target declaration 被显式泄露的证据，也未发现 reconstruction 依靠来源特有但候选没有的信息补充定理：它没有添加来源的 `Z_A` 名称、Gaussian law assertion、public-spectrum algorithm prose 或 lower-bound constants。这与 statement-only reconstruction 相容，但不能证明任何人绝无潜在识别或历史记忆。

本 reviewer 只见 root 机械投影在 envelope 内的 provenance；没有打开原始 decoder run/manifest/neutral-input 文件，也没有独立监控其全部历史。因此 negative exposure 事实是**按记录报告**，不是本 reviewer 重新审计 filesystem/tool history 后作出的无条件保证。已直接重新计算 anonymous statement 与 reconstructed text 的 UTF-8 SHA256；原始 run/manifest 的 hashes 仅检验了 envelope 内字段一致，没有伪称原始 payload已由本 reviewer重开核验。

方法学处理：保留这一 qualifying exposure；不称“零 leak/零 cue”，也不因未经确立的历史标签关系便虚构一个 current source-anchor exposure。若任何后续原始 run 证据显示实际 source/anchor/target-declaration 暴露，应重新判定 blind evidence；本阶段没有这种新增证据。

## 5. Provisional 判断与仍未覆盖的义务

**Provisional fidelity：** 对固定 Eq11 谱族上的 actual Euclidean-Lebesgue Gaussian integral core，七槽未发现与已冻结来源矛盾的差异；结论以谱乘积形式给出来源同一 scalar，显式提供 source-implicit integrability，并保持 exact parameter/measure/potential/constant scope。判断为 `PROVISIONAL_EQUIVALENT_FOR_BOUNDED_ACTUAL_INTEGRAL_CORE`，带有 documented ambient-label qualification。

这只是在来源与匿名 statement/reconstruction 之间的语义比较。它不接纳以下未覆盖项：

- formal proof 的真实性、axiom cleanliness、导入/作用域影响、项目自定义意义或 current module 与匿名 statement 的逐字绑定；输入 `compiled:true` 只是 metadata，本 reviewer 未运行 Lean，也未见 compiler receipt。
- Ex160 的两个 determinant expressions 与谱乘积写法之间的实际 formal bridge、formal `Z_A` 与 actual integral 的定义绑定、以及 formal probability law `N(0,A⁻¹)` 的 density/normalization bridge。它们不需要成为额外 public assumptions；是否由当前模块/先祖证成要等明确授权的 full-context review。
- “已知”作为 oracle-model claim、强凸/κ-smooth/唯一极小点、Lemma 4.6 全 statement 的其他 formal interfaces、两条主 sampling lower bounds 或任何 numerical/bit/runtime/TV guarantee。本匿名 statement 没给 ε、δ、query budget 或算法对象，不能据其 normalizer 公式给这些来源项目 credit。
- 最终 source V、reader/publication exposition、module/critical-ancestor 语义、所有未读取的来源 proofs 与 [22] 外部内容。

失败分类 `NONE`；没有数学反例或 source-invalid 判定，没有 source repair。第二次 freeze 后停止；只有后续单独授权才读取 canonical wholemodule/critical ancestors/reader/real Lean evidence，并且不能倒改 PHASE1/PHASE2 原始冻结。
