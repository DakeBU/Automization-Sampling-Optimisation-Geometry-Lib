# PHASE1：独立原始来源语义冻结

身份：`/root/norm_fresh_source_640251`；角色仅 fresh anti-anchored source reviewer。本文不是形式化证明、候选陈述批准、解码结果或最终 fidelity verdict。第一次输入冻结早于任何候选/匿名重构曝光；此分析完全从归档原始论文形成。

来源：*On Complexity of Gaussian Sampling*，`2610.20492v1.html`，951991 bytes，SHA256 `6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915`。所读数学原文仅 S2、S4.SS1、完整 A3.SS4（C.4，包括 Ex160）；有理由的邻近补充仅 Theorem 3.1、Theorem 4.1、Lemma 4.6 的完整 statement，以及 S4.SS1 所引 [22] 的本篇 bibliography entry。每一补充的 exact-byte 范围与理由分别归档。

## 1. 原文直接给出的对象与术语

- S2：`A` 是实对称精度矩阵，`I_d ≼ A ≼ κ I_d`。它不是协方差矩阵。实际势函数 `f_A(x)=xᵀAx/2`，实际目标 `π_A=N(0,A⁻¹)`。此处没有允许任意额外加法常数的势函数自由度。
- S4.SS1 Eq11：固定整数 `d≥2` 和参数 `κ≥2`；`θ_i=(i−1/2)π/d`、`λ_i=(κ+1)/2+(κ−1)cos θ_i/2`，`Λ=diag(λ₁,…,λ_d)`。索引为 `i=1,…,d`。`O` 为实正交矩阵，`A=OΛOᵀ`。
- S4.SS1 的硬输入分布取 `O∼Haar(O(d))`，独立于算法私有随机性。谱是确定的，并可提供给算法；未知部分是 `O` 所表示的特征基。
- C.4 将同一实际二次势记作 `V_A(x)=xᵀAx/2`。记号由 `f_A` 换成 `V_A`，未引入另一势函数。原文逐项声称谱界、`C∞`、Hessian 为 `A`、1 强凸、κ 光滑、0 为唯一极小点、目标为 `N(0,A⁻¹)`。
- C.4 Ex160 的直接显示式为

  `Z_A=(2π)^(d/2)(det A)^(−1/2)=(2π)^(d/2)(det Λ)^(−1/2)`。

  紧接文字指出：`Λ` 固定，所以 `Z_A` 独立于 `O`，且在谱公开时已知。
- Lemma 4.6 的正式 statement 本身仅断言：对每个 `O∈O(d)`，`A=OΛOᵀ` 满足谱界。C.4 中的势函数正则性与 normalizer 是其证明文字中实际出现的附加数学内容；不能把它们误标为 Lemma 4.6 statement 中明写的额外分句。

## 2. 独立七语义槽

### Objects

原文对象为有限维实空间、实正交群、确定的余弦谱 `Λ`、任意旋转对应的实精度矩阵 `A`、实际二次势 `V_A=f_A`、对应中心高斯概率分布 `π_A`，以及该势的高斯归一化常数 `Z_A`。`O` 可作为硬输入随机变量，但归一化式是对每个正交 `O` 的同一确定性恒等式。不能把对象变成一对可任意给出的 scalar witnesses，或把 `A` 当作协方差。

### Domains

本 normalizer 来源场景沿用 S4.SS1 的 `d∈Z, d≥2` 与 `κ∈R, κ≥2`；`i∈{1,…,d}`，`x∈R^d`，`O∈O(d)`，`A,Λ∈R^(d×d)`。所有 `λ_i` 严格位于 `(1,κ)`，这是 C.4 从 Eq11 得到的事实。`det A` 和 `det Λ` 因此为正。π 常数为通常的圆周率，`π_A` 为概率分布，两者不能混同。

S2 的一般精度类另容许 `d≥1,κ≥1`；不能在未说明泛化时把该一般域自动当成 Eq11/C.4 的精确来源域。公式对其他正定矩阵的自然推广不属于本 phase1 的来源声明。

### Quantifiers

先固定公开参数 `d,κ` 并按 Eq11 定义整个谱，再对每个 `O∈O(d)` 定义 `A`、势和目标；同一 `Z_A` 显示式与 `O` 无关。定义势时对所有 `x∈R^d` 使用真实二次函数。这里不是“存在某个旋转使公式成立”，也不是“随机旋转时高概率成立”。

Haar 抽样与算法随机性的独立性属于下界实验；归一化式自身无概率例外，不需要把随机性、算法或查询历史加入其数学前提。

“已知”在此指由固定/公开谱确定，不是对每个完全未知的一般 `A` 都允许免费得知其谱或 determinant。C.4 的明确条件是 spectrum public。

### Assumptions

明示来源前提为 S4.SS1 的 `d≥2,κ≥2`、Eq11 的具体谱构造及 `O` 正交；S2 规定实际势与目标含义。正定性、可逆性、谱界、光滑性、可测性、指数可积性及归一化常数正有限均应由这些对象的数学性质得到，不能仅为了某条实现路线便提升成该来源结论的独立 oracle/binder。

特别要区分：`A=OΛOᵀ` 是来源对象的定义；`det A=det Λ` 是构造的数学结果；高斯积分评价是证明 ingredient。后两者不能以“输入已满足 integral identity/determinant identity”为公开假设，随后再把消去假设的工作称作本文 normalizer 结果。

### Conclusion

Ex160 给出该实际势的归一化常数的精确值，先以 `det A` 表达，再以固定谱 `det Λ` 表达。结果由正 determinant 的正平方根分支解释。随后的结论是 `O` 独立性以及 spectrum public 时可由公开数据获知。

结论不只是一条形式符号定义 `Z_A := displayed expression`。要覆盖“Gaussian integration gives”的意义，还应保留该 scalar 与实际势积分/概率归一化之间的关联。怎样把这一关联写成 formal interface 要等 phase2 才比较；本 phase1 没有看过任何候选。

### Scopes and senses

这里的 normalization 是中心高斯实际势的 partition function，不是积分任意既有归一化高斯密度后得到的 1，也不是相对于一个已归一化 Gaussian base law 的 tilt factor。原文这几个限定片段没有显式写出 `Z_A := ∫ exp(−V_A(x)) dx`，所以“Lebesgue 积分作为 Z 的定义”在下一节明确列为标准约定推断，而不伪称是这些段落中的逐字定义。

势函数前面的 `1/2`、precision 的逆作为目标 covariance、实平方根的正支，均决定 `2π` 与 determinant 的负二分之一次幂。更换为 `exp(−xᵀAx)`、更换 base measure、或允许 `V_A+c`，会改变对象或其常数。源中的精确零点势已固定。

“known”是该 oracle-complexity 场景中的公开信息边界，不是位复杂度、浮点误差、实数运算次数或算法运行时间上界。归一化式本身既非 sampler，也非 TV 准确性定理。

### Constant dependencies

精确 scalar 的依赖只有 `d` 和完整谱 `λ₁,…,λ_d`；对 Eq11 固定家族可写为依赖 `d,κ`。它不依赖 `O`、算法、查询点、私有随机 seed、精度 `ε`、Theorem 4.1 的参数 `δ` 或任何隐藏误差概率。数值 `2` 与圆周率均为普适确定常数。

`Z_A` 的确切值有维数依赖与谱依赖；“独立于 O”绝不能误读为与 `d,κ` 都无关的 universal scalar。这里没有大 O 常数，也没有 `d₀` 阈值。后两者仅出现在另外的 lower-bound statements 中。

## 3. 明示来源、标准约定与推断分栏

| 项目 | 类别 | 冻结的解释与依据 |
|---|---|---|
| `f_A(x)=xᵀAx/2`, `π_A=N(0,A⁻¹)` | SOURCE_DIRECT | S2 定义与 S4.SS1 重申，C.4 再次指出目标。 |
| Eq11 谱、正交共轭、谱公开 | SOURCE_DIRECT | S4.SS1 原文。 |
| Ex160 的两个 determinant 表达式、`O` 独立、公开谱时已知 | SOURCE_DIRECT | C.4.p3 与显示式。 |
| `Z_A=∫_(R^d) exp(−V_A(x)) dx`，`dx` 为 Lebesgue | INFERENCE_STANDARD_CONVENTION | 由“potential/target”“Gaussian integration”“normalizing constant”及 Ex160 的系数共同确定的通常 partition-function 读法；限定原文未显式写定义。不是从 repo 名称或 candidate 推回。 |
| 目标 Lebesgue 密度为 `exp(−V_A)/Z_A` | INFERENCE_STANDARD_CONVENTION | 同一高斯/partition-function 约定；限定片段未逐字给 density 公式。 |
| `det Λ=∏_(i=1)^d λ_i` 以及正平方根 | INFERENCE_STANDARD_CONVENTION | `diag`、正谱与普通实 determinant/指数的标准含义，非额外算法假设。 |
| 正有限、可测/可积、可逆、对实际积分的联系 | SOURCE_IMPLICIT_OBLIGATIONS | 来源构造足以支持这些标准桥，但 C.4 没逐项展开；尚未在本 phase1 形式证明或独立证明。 |
| 固定公开数据可确定同一 normalizer | SOURCE_DIRECT + MODEL_SENSE | C.4 的明确公开谱结论；不扩张为运行时间或 numerical error theorem。 |
| 对任意 SPD 矩阵或 d=0 等的推广 | OUT_OF_SCOPE_INFERENCE | 不作为本次来源声明，也不凭通用知识纳入 exact source domain。 |

这一分栏不提出 source repair。`SOURCE_IMPLICIT_OBLIGATIONS` 表示来源证明省略的标准数学展开，不表示论文命题已被判假，也不授权增加新前提。

## 4. 原文证明结构与尚未展开的桥

C.4 的实际顺序是：Eq11 角度/余弦范围 → eigenvalue 严格范围 → 正交共轭谱界；随后实际势的 Hessian/正则性、强凸光滑和唯一极小点；随后目标 `N(0,A⁻¹)`；随后“Gaussian integration gives” Ex160；最后固定谱推出 `O` 独立和 public spectrum 下已知。这里只记录原文结构，不提供新的证明。

与 normalizer 有关、正式覆盖时必须成为内部 dependency/已证明事实的桥：

1. **GAUSSIAN_INTEGRAL_BRIDGE**：把该实际 `exp(−xᵀAx/2)` 的 Lebesgue 积分评价为 `(2π)^(d/2)(det A)^(−1/2)`，含正定域、可积性、实量值/positive finite 语义。C.4 仅以“Gaussian integration”一句调用，没有 theorem 编号或外部 citation。
2. **ORTHOGONAL_DETERMINANT_BRIDGE**：从构造与正交性得到 `det A=det Λ`，而非额外接受 determinant equality 为来源输入。C.4 把它压在第二个等号中，没有展开。
3. **ACTUAL_TARGET_NORMALIZATION_BRIDGE**：把 `N(0,A⁻¹)` 与该势的 normalized Lebesgue density 联系起来，不能只将一个同名 scalar 与一个同名 Gaussian law 并列。
4. **DEFINEDNESS_BRIDGE**：`A⁻¹`、正 determinant 的负半次幂、积分值的正有限性等由原对象保证。C.4 的谱界/正定性支持这些含义，来源未列 technical hypotheses 清单。
5. **PUBLIC_DATA_BRIDGE**：固定谱给同一 determinant、同一 scalar；“known”是相对于给定公共输入。此桥不含关于旋转的 oracle 回复，也不含 sampling procedure。

本次没有调用或搜索 Mathlib、Samplinglib、实现 API，亦没有给以上桥编写证明。它们不是任意添加的 mathematical assumption，不能把本 phase1 文本作为已编译叶子使用。

S4.SS1 引用 [22, Section 9.2] 说明余弦谱+随机旋转构造的来源：[22] OpenAI (2026), *Subpolynomial query complexity for well-conditioned log-concave sampling*, OpenAI Math Release preprint OAI:Subpolynomial-query-complexity-for-well-conditioned-log-concave-sampling-September-26-2026。这里仅归档本篇 bibliography 原文，未获取、阅读或采信该外部 paper 的定理。C.4 Gaussian integration 段没有引用 [22]，不能把构造 provenance 自动当作积分公式的 formal dependency。Remark 4.2 所指 Lemma 4.4/4.5 是算法/目标二次统计比较的另外路线，不是 C.4 normalizer identity 的前提；其 statements/proofs未读。

## 5. 两条主下界与准确度/成本的精确边界

补充读取的均为原始 HTML 中完整 theorem statements，不含它们的 proofs。

**Theorem 3.1：** 对每个整数 `d≥1`、`κ≥4`、`0<ε≤1/16`，

`Q_G(d,κ,ε) ≥ (1/256) min{ d, √κ log(1+d/(√κ ε)) }`。

**Theorem 4.1：** 对每个固定 `δ∈(0,1)`，存在只按 `δ` 标记的 `d₀(δ)`，使得对每个整数 `d≥d₀(δ)`、`2≤κ≤d^(1−δ)`、`0<ε≤1/10`，

`Q_G(d,κ,ε) ≥ (δ/256) √κ log d`。

第二条中的量词顺序不可把 `d₀` 改为依赖 `κ,ε`；也不可删掉上界 `κ≤d^(1−δ)`、large-d 边界或固定 δ 的限定。第一条不具有该 large-d/κ上界限制，但其 κ、ε 域和不同 log/min 表达式也不能借第二条替代。对数采用通常数学自然对数约定；限定原文没有另给底数，这是 `INFERENCE_STANDARD_CONVENTION`。

S2 给出两条结果共同使用的模型：

- `Q_G` 为满足统一 TV 精度的最小固定整数查询 cap 的 infimum。算法的 queries、stopping 和 output 是 seed 与先前 oracle replies 的 Borel functions，seed 与输入独立。
- `T` 是每个 admissible input、每个 seed realization 下均成立的 deterministic cap。它不是 expected query bound，也不是仅以高概率成立的 query cap。
- 对每个固定输入 `A`，输出分布 `ρ_A^Alg` 包含全部算法随机性。精度是 `sup_(A∈A_(d,κ)) TV(ρ_A^Alg,π_A)≤ε`，即输出 law 在 seed 平均后的精度，且对输入 uniform。不是每个 seed 都产生一个 TV-close law 的陈述。
- `TV(P,Q)=sup_B |P(B)−Q(B)|=(1/2)∫|p−q|dλ`；`B` 可测，`λ` 为任意共同 dominating measure。bounded test `h∈[0,1]` 的期望差上界为 TV，不应随意加入另一规范的 factor 2。
- exact first-order response 同时给 `f_A(x)` 与 `Ax`；value+gradient、gradient-only 与 matrix-vector query complexities 相同。这里是 exact oracle calls，未给 bit precision、浮点成本、实数算术成本或所有计算步骤的 wall-clock/runtime 定理。
- `ε` 是 sampling TV tolerance，不是 `Z_A` 的 relative/additive numerical tolerance。C.4 normalizer 显示式为精确数学表达式，没有用 ε，也没有声称从 sampler 估计 Z 的成本。
- S4 的 deterministic spectrum 可公开，normalizer 因而公开，但 eigenbasis 仍未知。这说明该构造的采样困难不能只归因于未知 Z。不能据此主张“已知 Z 就已构造 exact sampler”或把这两条 sampling lower bounds 改写成 fixed-spectrum integration lower bounds。

第一条的 hidden-determinant-sign 证明和第二条的算法/目标测试证明未读，因此不在本冻结中宣称其完整证明覆盖、上界最优性或任何加强 lower-bound model theorem。这里准确冻结的是 statement 与 S2 所定义的共同模型。

## 6. Typed remaining boundary 与阶段停止

| 类型 | 尚待事项 | 当前可作的结论 |
|---|---|---|
| REVIEW_PHASE2_PENDING | 后续匿名 Lean statement 与真正 blind reconstruction 尚未输入 | 仅冻结来源含义；无候选比较/接受 verdict。 |
| SOURCE_CONVENTION_IMPLICIT | 限定原文没显式写 Z 的 integral/base-measure 定义 | 上述 Lebesgue partition-function 解释是明确标注的标准约定推断；后续应检验 candidate 是否保持实际势语义。 |
| STANDARD_BRIDGE_UNEXPANDED | Gaussian integral、determinant invariance、actual target normalization、正有限/definedness | 必须在实现内部证明或复用已审计事实；当前未给 proof credit，不可转成 excess public premise。 |
| PUBLIC_INFORMATION_SCOPE | public/fixed spectrum 与 unknown rotation 的边界 | 仅确认源中文义；不生成 numerical complexity 或 generic unknown-A 免费谱假设。 |
| OUT_OF_SCOPE_PROOFS | Theorem 3.1/4.1、Lemma 4.4/4.5 证明、外部 [22] 内容 | 不宣布这些证明审计完成，不由 normalizer 审阅给整篇下界 badge。 |
| FINAL_MODULE_REVIEW_PENDING | canonical whole module、critical ancestors、reader 尚未输入 | 仅第二冻结完成后才进入最终 review；当前绝不预先审核。 |

失败分类为 `NONE`：没有发现/验证来源反例，没有判断 source-invalid/API-blocked，也没有尝试 implementation。本次只产出独立 source evidence。过程文档约束角色隔离和审阅方式，不增加任何数学假设。PHASE1 到此停止，文件一经 freeze 不再改写；后续信息必须写入新 phase2，而不能倒灌本分析。
