# Phase 3：独立整模块、原文、fresh Lean 与静态讲解审查

**ACCEPT，严格绑定候选 commit `37645c774481c4cad19fc29bcaa76799da64db7d`、完整包 canonical SHA `74a47b3eb5d33d778a273873f34382f926370894a577114833d7dfb97d8f8ead` 与 publication binding `8ddbbdb086becb57b2b8212154d9f607b121f7955cfcce132927210eaa04b95c`。** 接受范围是完整生产模块、相邻私有 Test 消费者、所引 C.7 与 C.8 有限交换步骤的忠实边界，以及当前 authored lesson/publication 的静态数学内容。没有 source repair、阻断 delta 或假闭合。整篇论文、C.8 闭式、Lemma 4.5、latest-main 集成、全局 gates、运行时网页与 postmerge purification 不在本接受范围内。

Reviewer 为 `/root/cosine_fresh_source_5d8c2a`，不同于 formalizer `huanjian_gc_20261109_fixed_spectrum_cosine_expansion` 和 decoder `/root/decode_b4e6a1`。本人的 Phase 1 原文认知、Phase 2 接口比较已分别在候选实现暴露前冻结；该顺序及所有 topic/path/tool cues 已披露。没有从旧审查复制 verdict。

## 绑定与失败探针保留

完整包原字节为 29444 bytes，raw SHA `21430e38c832bc14491c93a37af49c862b1b2ba607615f57ec39a29fb135a4bf`。最初误把 canonical digest 当作 raw digest，随后含自 hash 字段的普通排序编码也未匹配，因而真实 HOLD 并冻结在父目录。parent 后续明确授权相同原字节，并给出规则：仅删除顶层 `packet_sha256`，`ensure_ascii=False,sort_keys=True,separators=(',',':')`，UTF-8 无末尾换行。本人重新计算成功后才读取完整包。该诊断不改原文、payload 或 sealed statement；旧 HOLD 与失败探针均保留。

完整包的 source、statement/hash、blind reconstruction/身份/hash 与 Phase 2 payload 逐值相同；current module 字符串与磁盘模块逐字节相同。当前 lesson（除包投影未携带的、已另外全文阅读的 boundary 字段）与包内 lesson 相同；publication 的 source/statement/formulae/assumptions/obligations 和当前 audit 的绑定也相同。root 的 source.original_text 仍按 faithful paraphrase 处理，不冒充逐字原文。其“内部证明”的说法在本阶段由源码、fresh 编译和 kernel 证据独立核验。

审查过生产文件全部 6043 bytes / 130 行（SHA `659d6baf40abad2c48e7fced98c6c46a07624817cf14ef2de5a8146e82522de7`），Test 全部 3612 bytes / 68 行（SHA `7deb7539b72061b79b82865a956ac6560f505884d4fcb3ebba92a3d5f58d4759`），lesson 全部 8858 bytes，publication 全部 6980 bytes。精确输入清单、原文元素片段、源码/缓存 hash 与命令 receipts 在本目录关联 JSON 中。只枚举了 preproof source-and-challenge archive 的成员名，没有用其中其他 reviewer 的报告、graph 或 verdict 决定本次结论。

## 原文对照与七槽

固定原文仍是 951991-byte HTML / SHA `6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915`。独立基准来自完整 C.7 陈述和证明 `A3.Thmtheorem7,A3.Ex133–137,A3.SS3.2`，完整 C.8 及消费点 `A3.Ex140,A3.SS3.p4.2`，必要 §4.1 网格和 Lemma 4.5 定义/相邻坐标变换；具体原字节区间与 fragment hashes 保持 Phase 1 绑定。

| 槽 | source / formal / reconstruction 的比较 | 结论 |
|---|---|---|
| objects | 字面 ρ=(√κ−1)/(√κ+1)、实倒谱函数和余弦级数一致；无项目自定义 predicate 或可选代表元。 | equivalent |
| domains | 全实角度；源文 j≥1 与 formal/reconstruction 的 j∈ℕ、频率和幂均 j+1 一一对应；N 项正模态无零模态重复。 | equivalent after index elaboration |
| quantifiers | κ≥2 固定在外，等式和绝对收敛分别对所有 θ；一致收敛阈值依赖 κ、ε，独立于 θ，适用于所有后续 N；没有跨 κ 一致性。 | equivalent |
| assumptions | 唯一 public premise 是源环境 κ≥2。r 是 literal let；0<r<1、非零分母、HasSum、可和与 uniform bound 都实际内部产生。 | equivalent with inherited context explicit；无 EXCESS |
| conclusion | 精确展开、norm 项 Summable、对同一 tsum 的 TendstoUniformly 三项均在 public 输出中，且 fresh kernel type 与匿名 statement definitionally equal。 | equivalent；无弱化 |
| scopes/senses | 实数函数级数及全 ℝ 角度一致性；复杂指数只是内部证明媒介。未把有限网格、Gaussian expectation 或 alias 闭式混入 C.7。 | equivalent |
| constant dependencies | 左端 2、括号常数 1、模态系数 2、外部 1/√κ、(-r) 的符号幂与两处 j+1 都保留。 | equivalent |

decoder 重建逐项保留以上内容。现在另核验了 archived decoder input 的 canonical/raw hash、run hash 和重建文本 hash 链；输入仅含匿名 statement 与四条标准 context，未含 source/anchor/declaration/audit identity。decoder 自报 source_text_visible=false 与其暴露日志相符，actor 与本人不同，且未作 zero-ambient-cues 声明。这些是当前可见流程记录的验证，不声称能证明未记录的外部行为不存在。

## 完整生产模块覆盖

模块只有八个 Mathlib imports、BigOperators/Filter 打开、namespace、两个 private theorem 和一个 public theorem；没有 scoped variable、axiom、定义替身、default/fallback 或别的公开数学输出。fresh 环境枚举也恰好找到生产三声明和 Test 一声明。

| 源码范围 | 审查内容和实际结果 |
|---|---|
| production 1–13,130 | 只引入标准 Mathlib 语义和记号；无隐藏公共参数或项目外 premise。 |
| `radius_bounds` 15–22 | 由 κ≥2、sqrt 非负与平方恒等式推出 √κ>1 和字面半径在 (0,1)。此证明实际被 public producer 使用；不是 theorem-shaped 输入证书。 |
| `cosine_series_value` 24–73 | 私有通用 r∈[0,1) 引理。构造 z=−r exp(iθ)，核对复范数和 cast/De Moivre，建立真正 HasSum，取实部，计算 normSq 和逆实部；D>0 在内部证明；去零模态后完成 (1−r²)/D。它是原文共轭几何求和的等价实部路线，不是额外 source 假设或 source repair。 |
| public signature 75–87 | 全部三项源结论；唯一 hκ；无 d、n、U、矩阵或收敛证书。 |
| public proof 88–128 | 调用两个 private helpers；hgeom/hmajor 产生绝对与全角度一致收敛；hs0/hsden/hspec/h1r 解除分母；hparam/hnorm 实际证明精确归一化，最终 field algebra 不是预设展开等式。 |

该模块不是 public wrapper：它含真正几何 HasSum、取实部、归一化与一致收敛构造；两个 private provider 都可达。有限 canonicality 查询在 `AutoSamplingTheory/TechnicalLemmas` 和 GaussianComplexity 模块范围内只命中本模块的相应展开/helper，没有发现重复公开接口。此查询不声称穷尽全球数学库的等价定理。现有通用 Mathlib 几何求和、实部与 uniform majorant 定理被实际复用；没有为 reuse 计数制造 wrapper 或将 private helpers 冒充 Registry/shared-node 信用。

## Test 和实际消费者

Test 1–6 仅 imports/notation；7–16 的精确 type 与 Phase 2 私有匿名 signature 在 fresh kernel 环境 definitionally equal。网格 `Fin d` 的 i.val+1/2 对应源文 (i_source−1/2)，其中 i_source=i.val+1；eigenvalue、r、总和归一化均相同。d≥2 是源网格范围，编译器提示 hd 未被证明体引用；它不影响正确性，也未进入 public C.7 premise。

17–28 定义 θ/eigenvalue/r/w/f/g；29 真正取得 public producer 的 heq 和 habs；30–36 从 habs 得 hs，再得 hsg/hlin；37–52 用 heq 逐点归一化倒谱；53–55 用 hsg 真正交换有限和与无穷级数；56–68 因式分解与有限和线性完成目标。没有把期望或 alias 值作为假设，也没有只检查声明名字或重新假设展开。

这不只来自源码命名。独立 fresh 导入后，编译的 consumer proof body 有且仅有一个直接公开 ASTIS parent：`actual_inverse_spectrum_cosine_expansion`。kernel 中的局部依赖进一步显示：

```text
producer hκ → And.casesOn … heq / habs
hs       references habs
hsg      references hs
hlin     references hs
heigen   references heq
hscalar  references heigen and hlin
hexchange references hsg; value head = @Summable.tsum_finsetSum
```

`Summable.of_norm`、`Summable.mul_left`、`Summable.tsum_mul_left` 和 `Summable.tsum_finsetSum` 都存在于实际 proof body's direct constants。保存的编译项在开始处也明确显示 `have hs := fun i => Summable.of_norm (habs (θ i))`。因此“消费了 producer 的等式与绝对可和性”及“实际有限交换”在本阶段获得独立 kernel 证据。

私有结论的 n 是任意自然数：n=0 提供无权倒谱和的展开，1≤n<d 提供 μ_n 的确定性有限和展开。它只是原文 `p4.2` 的 generalized deterministic intermediate；未给 Gaussian 二阶矩/正交目标法则桥、离散 alias 消去、C.8 exact closed forms、方差或 normalized bias。源 1≤n<d 和后续 d−n≥√κ 的用途没有被抹掉。

## 独立 fresh Lean / kernel 证据

实际执行的 Lean 是本机 v4.33.0，commit `d8b18978322de05a8f3dba51ef03cf5461676c17`。`lean-toolchain` SHA 为 `302cd63c54178885b89e669f33b38f12f4dd7ae7e5cac537b3203e3768d8fb2b`；`lake-manifest.json` SHA 为 `b83ca83b9cf7caa85fa8b023c2ff9a3fb7a7cce7e1c332e810c348535ec49c37`。九个 package 的实际 git HEAD 逐个匹配 manifest 且 tracked clean；所有直接 Mathlib import 的 source bytes 也与该 package pinned git blob 相同。

本 reviewer 新建此前不存在的 `fresholean/` 并放在 LEAN_PATH 第一位，依次重新编译生产模块和 Test（两者 exit 0），再编译独立 kernel probe、consumer term probe 和 focused-binding probe（均 exit 0）。`lean --deps` 明确证明 Test 解析到新生产 olean，kernel probes 解析到新 Test olean；未以 root 的旧 olean、receipt 或日志代替检查。依赖包现有 oleans 按任务许可复用，没有重建整个 Mathlib；其 source/pin 与实际解析路径独立记录，未声称逐一重建整个依赖闭包。

四个声明的 ConstantInfo 都是带实际 proof Expr 的 `thmInfo`。producer 的直接公开 ASTIS parents 为空，直接 private ASTIS parents 正是两个 helpers；consumer 的直接公开 ASTIS parent 恰好是 producer。四者 `#print axioms` 的递归集合均且仅为 `[propext, Classical.choice, Quot.sound]`，无 sorryAx 或其他假设闭合。匿名 public / private types 的 definitionally-equal 检查均通过；独立 public example 也由新 producer 通过 kernel。

除初始包绑定 HOLD 外，保留了三个本地非数学失败：Cli 无预构建 lib 目录导致首个环境脚本 assertion（九个 pin 检查已成功，后续只略过未存在的无用 library path）；误把 registry index 当作 exact audit object 所在处（后续 literal-id 查询定位了相关 audit）；focused-output 后处理最初未允许 pretty printer 的 `@` 前缀（未重跑 Lean，只修正解析规则）。所有原探针和诊断保留，没有改候选或 sealed 接口来消除失败。

## 静态 authored-reader 数学内容

逐项审查当前 lesson 的 statement/formula、五条 assumptions、S_N notation、六个 steps 的 text/formula/Lean explanation、dependency lists、source attribution/scope、tests 与完整 boundary；publication 的相应项目/obligation/binding/assumption differences 也全部读取并核对。步骤 1 的 r∈(0,1)、步骤 2 的实部几何和、步骤 3 的 D 与去零模态、步骤 4 的两条归一化恒等式、步骤 5 的 geometric majorant、步骤 6 的 weighted finite-grid interchange 均与源码和源文边界一致。C.7 公共假设与内部 ingredient、全实角度固定 κ 一致性、全自然 n 私有中间式与后续源范围都明说，没有由本结果冒领 C.8/Lemma 4.5 或全文信用。

`reading_layout=progressive` 和文字要求先展示展开、其余折叠，是已检查的静态 authored metadata。**未生成/打开网页，未做 runtime、Chrome、移动布局或视觉 QA。** 因此本报告不把 static-reader review 说成浏览器验收，也不授予整站 reader/Exposition Seal。

最终本地数学/语义/整模块 verdict 为 ACCEPT，canonical fidelity verdict 为 `equivalent-after-elaboration`。本目录给出 accepted-audit proposal 供串行集成者审阅，但未修改实际 audit、publication、tracked file、ledger、Goal 或 commit；未运行 sourceV、项目 API、aggregate/site/browser 或网络。后续 latest-main 与全局 gates 保持原门槛。
