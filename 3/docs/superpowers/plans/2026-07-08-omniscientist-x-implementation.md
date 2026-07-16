### Task 1: keyanlun SKILL.md — 新增自动调度映射表 + Research Passport

**Files:**
- Modify: `~/.claude/skills/keyanlun/SKILL.md`（在"版权与致谢"section 之前插入）

**Interfaces:**
- Consumes: 无（对现有内容只增不改）
- Produces: 自动调度映射表（为 Task 2/3/4 的新 skill 提供路由入口）、Research Passport JSON schema

#### 改动说明
在现有 SKILL.md 的"参考文件索引"section 和"版权与致谢"section 之间，插入两个新 section。插入点位于 `## 版权与致谢` 这一行之前（约第 228-230 行）。

- [ ] **Step 1: 验证插入点**

运行以下命令确认插入点的准确位置和上下文：
```bash
grep -n "## 版权与致谢" ~/.claude/skills/keyanlun/SKILL.md
```
预期输出: `230:## 版权与致谢`（行号可能有 ±2 的偏差）

- [ ] **Step 2: 使用 Edit 工具插入新 section**

在 `## 版权与致谢` 之前插入以下内容（用 Edit 工具的 old_string 匹配 `## 参考文件索引` 到 `## 版权与致谢` 之间的内容来替换为带新增内容的版本）：

**old_string:**
```
---

## 版权与致谢
```

**new_string（在 old_string 的 `---` 和 `## 版权与致谢` 之间插入）:**
```markdown
---

## 自动调度映射表（v2 — OmniScientist X 网关）

> 定位到层级后，自动向用户推荐下游执行工具链。用户可跳过推荐直接指定工具。

| 层级 | 核心矛盾 | 推荐工具链 | 触发条件 |
|------|---------|-----------|---------|
| 第1层 | "选谁/选哪" | `advisor-search` → `advisor-analysis` → `research-compass` | 未选定导师/方向 |
| 第2层 | "做什么" | `literature-search` / `scientific-literature-retrieval` → `idea-generation` → `novelty-assessment` | 方向明确但无具体课题 |
| 第3层 | "靠不靠谱" | `mvp-validator` → `experiment-design` | 有 idea 待验证 |
| 第4层 | "怎么做" | `figure-storyboard` → `academic-paper` (full模式) 或 `paper-assembly` | idea 已验证 |
| 第5层 | "顺利通关" | `paper-assembly` → `slide-generation` | 小论文已完成 |
| 第6层 | "布局毕业" | `research-compass`（决策矩阵模式） | 即将毕业 |
| 第7层 | "指导+申请" | `survey-generation` → `research-compass` | 青年教师 |
| 游离层 | "回归正轨" | `toolkit-mindset` → 最低耗能动作 | 情绪/人际问题 |

**调度规则：**
1. 用户可跳过推荐，直接指定工具
2. 每步完成后自动更新 Research Passport
3. 工具链按顺序执行，前一步输出作为后一步输入
4. 当用户提供已有材料（如已有文献库），自动跳过已完成步骤

## Research Passport（科研护照 — v2 新增）

> 轻量状态文件，跨对话追踪科研进度。路径: `~/.hermes/research-passport.json`

### 数据结构

```json
{
  "project": "项目名称",
  "created": "ISO时间戳",
  "current_layer": 2,
  "layer_history": [
    {
      "layer": 1,
      "status": "completed",
      "started": "ISO时间戳",
      "completed": "ISO时间戳",
      "output_summary": "简要描述该层产出",
      "artifacts": ["产出文件路径"]
    }
  ],
  "five_steps_progress": {
    "搜": "completed",
    "聚": "completed",
    "分": "in_progress",
    "验": "pending",
    "合": "pending"
  },
  "active_tools": ["当前激活的工具"],
  "next_recommended": "下一步推荐工具",
  "milestones": [
    {"date": "YYYY-MM-DD", "event": "里程碑事件描述"}
  ],
  "last_updated": "ISO时间戳"
}
```

### 自动行为

- **对话开始时**：自动读取 passport，恢复上下文（如存在）
- **状态变更时**：层级推进或5步法步骤完成时自动更新
- **与 Material Passport 同步**：进入第4层时，与 `academic-pipeline` 的 Material Passport 双向同步
- **多项目支持**：每个项目一个 passport 文件（通过 `project` 字段区分）
- **手动查询**：用户说"查看科研进度"、"科研护照"时显示当前状态

### 初始化命令

当用户首次使用或开始新项目时，自动创建 passport：
```
用户: "开始新项目：羊肚菌AI品质预测"
→ 自动创建 ~/.hermes/research-passport.json
→ 定位层级：第2层（开题/找idea）
→ 推荐工具链：literature-search → idea-generation → novelty-assessment
```

---

## 版权与致谢
```

- [ ] **Step 3: 验证插入结果**

```bash
# 检查 section 是否正确插入
grep -n "自动调度映射表" ~/.claude/skills/keyanlun/SKILL.md
grep -n "Research Passport" ~/.claude/skills/keyanlun/SKILL.md
# 确认版权与致谢 section 仍存在且完整
grep -A5 "## 版权与致谢" ~/.claude/skills/keyanlun/SKILL.md
```

- [ ] **Step 4: 提交改动**

```bash
cd "$(dirname ~/.claude/skills/keyanlun/SKILL.md)/../.."
git add skills/keyanlun/SKILL.md
git commit -m "feat(keyanlun): v2 新增自动调度映射表 + Research Passport

L0 网关增强: 7层自动路由到下游工具 + 跨对话科研状态追踪

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 2: 新建 mvp-validator skill

**Files:**
- Create: `~/.claude/skills/mvp-validator/SKILL.md`
- Create: `~/.claude/skills/mvp-validator/references/mvp-prompts.md`

**Interfaces:**
- Consumes: idea-generation 或 novelty-assessment 的输出（研究 idea 描述）
- Produces: JSON 格式 MVP 验证方案（core_hypotheses + mvp_plan + stop_conditions），供 experiment-design 消费

- [ ] **Step 1: 创建目录结构**

```bash
mkdir -p ~/.claude/skills/mvp-validator/references
```

- [ ] **Step 2: 创建 SKILL.md**

写入 `~/.claude/skills/mvp-validator/SKILL.md`:

```markdown
---
name: mvp-validator
description: MVP科研验证 — 将研究idea转化为可证伪假设 + 最低成本验证方案 + 量化止损条件。基于第一性原理检查创新等级。Use when you have a research idea and need to validate it before committing resources. Triggers on: 验证idea, MVP验证, 最小可行验证, 这个idea靠谱吗, validate research idea.
argument-hint: [research-idea]
---

# MVP Validator — 最小可行验证

将模糊的研究 idea 转化为可执行的验证方案。核心理念：**用最低成本证明或推翻核心假设，知道什么时候该放弃。**

## Input

- `$0` — 研究 idea 描述、novelty-assessment 输出、或 keyanlun 第3层传递的待验证 idea

## References

- MVP 验证 prompt 模板: `~/.claude/skills/mvp-validator/references/mvp-prompts.md`

## Workflow

### Step 1: 核心假设提取

从 idea 中拆出 1-3 个**可证伪**的核心假设：

- 追问: "如果这个假设错了，整个方向还成立吗？"
- 区分: **必要条件假设**（错了方向必死）vs **充分条件假设**（错了还可以调整）
- 每个假设必须有明确的验证方式

### Step 2: 第一性原理检查

- **为什么可能有效？** 从基础机制层面解释，不引用"前人用了这个方法"
- **是否存在反例？** 什么情况下这个逻辑会失效？
- **创新等级判定:**
  - **genuine**: 新科学问题 / 新机制 / 新理论
  - **incremental**: 换数据 / 换模型 / 换材料但有新 insight
  - **trivial**: 纯排列组合，无新 insight

### Step 3: 最小验证方案生成

- **最低成本路径**: 用已有数据 / 公开数据集 / 最少实验量能验证什么？
- **数据需求评估**: 标注已有 / 可获取 / 需采集
- **关键指标**: 每个指标有明确的成功/失败阈值
- **预估时间**: 现实估算，不是理想情况

### Step 4: 止损条件 + 备选方案

- **放弃条件**: 具体的、可量化的指标阈值（不是"效果不好"）
- **备选方向**: 如果这个 idea 不可行，下一个测什么？

## Output Format

```json
{
  "idea": "原始idea描述",
  "core_hypotheses": [
    {
      "hypothesis": "可证伪的假设陈述",
      "type": "necessary | sufficient",
      "testable": true,
      "falsifiable": true,
      "verification_method": "如何验证",
      "if_wrong_impact": "critical | moderate | minor"
    }
  ],
  "first_principles_check": {
    "why_might_work": "基础机制层面解释",
    "counter_examples": ["已知反例或边界条件"],
    "innovation_level": "genuine | incremental | trivial",
    "innovation_justification": "判断依据"
  },
  "mvp_plan": {
    "minimal_cost_path": "最低成本验证路径描述",
    "data_required": {
      "already_have": ["已有数据"],
      "can_obtain": ["可获取但未获取"],
      "need_collect": ["需要从头采集"]
    },
    "key_metrics": [
      {
        "metric": "指标名称",
        "success_threshold": "成功阈值",
        "measurement": "测量方式"
      }
    ],
    "estimated_time": "预估完成时间"
  },
  "stop_conditions": [
    "具体可量化的放弃条件"
  ],
  "fallback_direction": "备选方向描述"
}
```

## Rules

- 每个核心假设必须可证伪 — "可能有效"不算假设
- 创新等级判定必须给出具体理由，不能直接标 genuine
- 止损条件必须是可量化的指标阈值，不能是模糊描述
- 最低成本路径必须优先使用已有数据 — 不要一上来就设计全套实验
- 当 idea 来自文献排列组合时，必须标注"需人工确认真实世界锚点"

## Related Skills

- **Upstream**: idea-generation, novelty-assessment, keyanlun 工具1.7
- **Downstream**: experiment-design, experiment-code
- **See also**: research-compass（多方向比较时先做 compass 再对选定方向做 mvp-validator）
```

- [ ] **Step 3: 创建 references/mvp-prompts.md**

写入 `~/.claude/skills/mvp-validator/references/mvp-prompts.md`:

```markdown
# MVP 验证 Prompt 模板

## 假设提取 Prompt

```
你是一个苛刻的科研评审人。阅读以下研究 idea，提取其中隐含的核心假设。

要求:
1. 每个假设必须是可证伪的陈述（可以被实验推翻）
2. 标注每个假设的类型: necessary（必要条件，错了方向就死）或 sufficient（充分条件，错了可以调整）
3. 对每个假设追问: "如果这个假设错了，整个方向还成立吗？"

Idea: {{idea}}
```

## 第一性原理检查 Prompt

```
回到最基础的物理/化学/生物/数学原理，不引用任何文献:

1. 为什么这个 idea 在基础机制层面可能成立？
2. 在什么边界条件下这个逻辑会失效？
3. 是否存在已知的反例？
4. 这个 idea 的核心是"新问题"还是"新方法解旧问题"？

基于以上，判断创新等级:
- genuine: 新科学问题、新机制、新理论
- incremental: 换数据/换模型/换材料但有新 insight
- trivial: 纯排列组合，无新 insight

Idea: {{idea}}
核心假设: {{hypotheses}}
```

## 止损条件 Prompt

```
对于以下研究 idea 和验证方案，定义具体的放弃条件。

要求:
- 条件必须是可量化的指标阈值（如 "RMSE > 0.3"，不是 "效果不好"）
- 区分: "这个 idea 不可行"vs"验证方案设计有问题"
- 每个条件标注: 达到后就直接放弃，还是先尝试调参 N 次

Idea: {{idea}}
MVP方案: {{mvp_plan}}
```

## MVE 评估维度（来自科研论 工具1.7）

| 维度 | 检查点 |
|------|--------|
| 真实世界锚点 | idea 是否来自真实问题，而非纯文献排列组合？ |
| 0→1 关键不确定性 | 是否存在一个关键未知？还是"1"天然存在？ |
| 验证粒度 | MVE 设计是否足够小？能否÷10？ |
| 备选路径 | 失败了有没有备选方向？ |
| 止损触发线 | 有没有明确的、不可协商的放弃条件？ |
```

- [ ] **Step 4: 验证文件**

```bash
# 确认文件存在且非空
wc -l ~/.claude/skills/mvp-validator/SKILL.md
wc -l ~/.claude/skills/mvp-validator/references/mvp-prompts.md
# 确认 frontmatter 有效
head -5 ~/.claude/skills/mvp-validator/SKILL.md
```

- [ ] **Step 5: 提交**

```bash
cd ~/.claude
git add skills/mvp-validator/
git commit -m "feat: 新增 mvp-validator skill — MVP科研验证

假设提取 → 第一性原理检查 → 最小验证方案 → 止损条件

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 3: 新建 figure-storyboard skill

**Files:**
- Create: `~/.claude/skills/figure-storyboard/SKILL.md`
- Create: `~/.claude/skills/figure-storyboard/references/storyboard-prompts.md`
- Create: `~/.claude/skills/figure-storyboard/references/figure-patterns.md`

**Interfaces:**
- Consumes: 实验/分析结果摘要（来自 experiment-design 或 data-analysis）
- Produces: Figure 故事板（4-6 张 Figure 的层级规划），供 figure-generation / table-generation / academic-paper 消费

- [ ] **Step 1: 创建目录结构**

```bash
mkdir -p ~/.claude/skills/figure-storyboard/references
```

- [ ] **Step 2: 创建 SKILL.md**

写入 `~/.claude/skills/figure-storyboard/SKILL.md`:

```markdown
---
name: figure-storyboard
description: 论文故事线设计 — 用Figure讲好科研故事。从研究结果反推Figure规划，每张图标注科学问题映射、数据来源和逻辑链。Figure先行、文字填空。Use when you have results and need to plan the paper's visual narrative. Triggers on: 论文Figure规划, 故事线设计, 合图先行, paper figure plan, figure storyboard.
argument-hint: [research-findings]
---

# Figure Storyboard — 论文故事线设计

**核心理念：论文不是做完实验再设计图表，而是先用图表讲好故事，再往里面填文字。**

## Input

- `$0` — 研究问题 + 核心发现摘要 + 实验数据概览

## References

- 故事线设计 prompt: `~/.claude/skills/figure-storyboard/references/storyboard-prompts.md`
- 学科 Figure 组合模式: `~/.claude/skills/figure-storyboard/references/figure-patterns.md`

## Workflow

### Step 1: 故事线提取

从研究问题和核心发现中，提炼**一句话故事线**：

- 格式: "我们发现 [X因素] 通过 [Y机制] 影响 [Z结果]，且这种影响在 [A条件] 下被放大/抑制"
- 标注故事的起承转合: 已知 → Gap → 我们的方法 → 核心发现 → 机制 → 意义

### Step 2: Figure Panel 规划

按故事线设计 4-6 张 Figure，每张标注：

| 属性 | 说明 |
|------|------|
| 科学问题 | 这张图回答什么？ |
| 数据类型 | 用什么数据做这张图？ |
| 推荐图类型 | 示意图 / 数据图 / 表格 / 组合图 |
| 与前后关系 | 承接前一张 → 引出下一张 |

标准 Figure 结构（可根据学科调整）:

```
Figure 1: 科学问题与研究框架  →  引出方法
Figure 2: 方法体系与表征策略  →  为核心发现做铺垫
Figure 3: 核心发现（最重要）  →  引出机制解释
Figure 4: 机制解释与验证      →  引出普适性验证
Figure 5: 模型验证/应用预测   →  回到Figure 1形成闭环
```

### Step 3: 图文映射 + 下游对接

为每张 Figure 标注具体的下游执行工具:

```
Figure 1 (示意图)     → excalidraw-skill 或 TikZ
Figure 3-5 (数据图)  → figure-generation (Python/R)
Figure 2 (方法表)    → table-generation
完整故事线           → academic-paper (Introduction + Discussion)
```

## Output Format — Figure 故事板

```markdown
## 论文故事线
[一句话核心故事，标注起承转合]

## Figure 故事板

### Figure 1: [标题]
- **回答的科学问题**: ...
- **所需数据**: ...
- **推荐图类型**: ...
- **承接关系**: → 引出 Figure 2

### Figure 2: [标题]
- **回答的科学问题**: ...
- **所需数据**: ...
- **推荐图类型**: ...
- **承接关系**: Figure 1 → 为 Figure 3 铺垫

### Figure 3: [标题] ⭐核心
- **回答的科学问题**: ...
- **所需数据**: ...
- **推荐图类型**: ...
- **承接关系**: Figure 2 → 引出 Figure 4

### Figure 4: [标题]
- **回答的科学问题**: ...
- **所需数据**: ...
- **推荐图类型**: ...
- **承接关系**: Figure 3 → 引出 Figure 5

### Figure 5: [标题]
- **回答的科学问题**: ...
- **所需数据**: ...
- **推荐图类型**: ...
- **承接关系**: Figure 4 → 回到 Figure 1 形成闭环

## 下游执行计划
| Figure | 工具 | 输入数据 | 预计产出 |
|--------|------|---------|---------|
| 1 | excalidraw-skill | 无（纯设计） | 示意图 PNG |
| 3,4,5 | figure-generation | results.csv | matplotlib 代码 |
| 2 | table-generation | methods.json | LaTeX 表格 |

## 数据缺口
- [ ] Figure 3 需要补充 X 数据（当前缺失）
- [ ] Figure 5 需要额外验证实验 Y
```

## Rules

- Figure 数量 4-6 张，超过 6 张说明故事线不够聚焦 → 合并或移到 Supplementary
- 每张图必须能回答一个明确的科学问题 — "锦上添花"的图移到 Supplementary
- 数据不够就标注缺口，先出已有数据的图 → 反向驱动实验设计
- 故事线必须能在一句话内说完 — 不能说清楚说明还没想清楚
- Figure 3 是论文的"心脏" — 这是审稿人最先看的图，必须最强

## Related Skills

- **Upstream**: experiment-design, data-analysis, keyanlun 工具1.8（合.图先行）
- **Downstream**: figure-generation, table-generation, academic-paper, excalidraw-skill
- **See also**: paper-assembly（完整论文组装流程）
```

- [ ] **Step 3: 创建 references/storyboard-prompts.md**

写入 `~/.claude/skills/figure-storyboard/references/storyboard-prompts.md`:

```markdown
# Figure 故事线 Prompt 模板

## 故事线提取 Prompt

```
你是一位经验丰富的科学传播者。你的任务是将以下研究提炼成一条"一句话故事线"。

要求:
1. 格式: "我们发现 [X因素] 通过 [Y机制] 影响 [Z结果]"
2. 必须标注故事的起承转合
3. 标注核心发现与已有研究的关键差异点
4. 如果一条说不完，说明故事可能还不够聚焦

研究问题: {{research_question}}
核心发现: {{key_findings}}
实验数据概览: {{data_summary}}
```

## Figure Panel 规划 Prompt

```
基于以下故事线和可用数据，设计 4-6 张 Figure 的层级布局。

要求:
1. 每张图必须回答一个明确的科学问题
2. 标注每张图与前后图的逻辑关系（为什么放在这个位置？）
3. Figure 3 必须是核心发现 — 这是论文的"心脏"
4. Figure 5 必须回应 Figure 1 提出的科学问题
5. 如果某张图去掉不影响故事完整性 → 移到 Supplementary

故事线: {{storyline}}
可用数据: {{available_data}}
目标期刊/学科: {{target_venue}}
```

## 图文映射 Prompt

```
为每张 Figure 推荐最佳可视化工具和图表类型。

要求:
1. 示意图优先考虑 excalidraw-skill（快速设计）或 TikZ（精确控制）
2. 数据图选择: 比较→柱状图/箱线图, 趋势→折线图, 相关性→散点图, 分布→直方图/密度图
3. 标注每张图需要的数据列和统计方法
4. 标注当前缺失的数据

Figure 规划: {{figure_plan}}
```

## 故事线自检清单

- [ ] 故事线能在 30 秒内口头讲清楚吗？
- [ ] Figure 3（核心发现）是否足够强？弱了是否应该重新设计实验？
- [ ] 每张 Figure 去掉后，故事还完整吗？（不完整→保留；完整→移到 SI）
- [ ] Figure 1 和 Figure 5 是否形成了清晰的"问题→答案"闭环？
- [ ] 有没有"不知道怎么解释所以先画个图"的 Figure？（有→回到实验设计）
```

- [ ] **Step 4: 创建 references/figure-patterns.md**

写入 `~/.claude/skills/figure-storyboard/references/figure-patterns.md`:

```markdown
# 学科常见 Figure 组合模式

## 模式1: 计算/建模类论文

```
Figure 1: 问题定义 + 模型架构概览（示意图）
Figure 2: 方法细节 + 与 baseline 的区别（流程图 + 对比表）
Figure 3: 主实验结果（大表或多 panel 对比图）⭐
Figure 4: 消融实验 / 组件分析（柱状图）
Figure 5: 案例分析 / 可视化 / 误差分析
```

## 模式2: 实验科学类论文（化学/材料/生物）

```
Figure 1: 科学问题 + 研究策略（示意图）
Figure 2: 材料/样品表征（TEM/SEM/XRD 多 panel）
Figure 3: 核心性能数据（多条曲线对比）⭐
Figure 4: 机理分析（原位表征 / 理论计算 / 对照实验）
Figure 5: 普适性验证 / 应用展示
```

## 模式3: 食品科学类论文

```
Figure 1: 研究框架 + 假设（流程图）
Figure 2: 实验设计 + 分析方法（方法概览图/表）
Figure 3: 品质/活性/结构核心结果（多 panel）⭐
Figure 4: 机制解释（相关性 + 通路/机制示意图）
Figure 5: 模型验证 / 应用预测 / 贮藏稳定性
```

## 模式4: 社会科学/教育类论文

```
Figure 1: 理论框架 / 概念模型（框图）
Figure 2: 研究设计与方法（流程图 + 样本描述表）
Figure 3: 主要发现（结构方程模型路径图 / 回归系数表）⭐
Figure 4: 分组比较 / 调节效应 / 中介效应
Figure 5: 理论贡献 + 实践启示（总结性示意图）
```

## 通用原则

1. **Figure 3 法则**: 无论什么学科，Figure 3 都是论文的"心脏" — 核心发现
2. **Inverted Pyramid**: Figure 1（最广）→ Figure 3（最核心）→ Figure 5（最广）
3. **每张图独立可读**: 单独看每张图和图注应能理解基本结论
4. **颜色一致性**: 同一样品/条件在所有图中使用相同颜色
5. **SI 不是垃圾桶**: 只有真正支撑论证的图放正文，其余不放入（而非全塞进 SI）
```

- [ ] **Step 5: 验证文件**

```bash
ls -la ~/.claude/skills/figure-storyboard/
ls -la ~/.claude/skills/figure-storyboard/references/
wc -l ~/.claude/skills/figure-storyboard/SKILL.md
```

- [ ] **Step 6: 提交**

```bash
cd ~/.claude
git add skills/figure-storyboard/
git commit -m "feat: 新增 figure-storyboard skill — 论文故事线设计

故事线提取 → Figure 1-5 规划 → 下游工具对接 + 4种学科Figure模式

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 4: 新建 research-compass skill

**Files:**
- Create: `~/.claude/skills/research-compass/SKILL.md`
- Create: `~/.claude/skills/research-compass/references/compass-prompts.md`
- Create: `~/.claude/skills/research-compass/references/decision-matrix.md`

**Interfaces:**
- Consumes: 候选选项列表 + 评估场景（来自 keyanlun 第1/6/7层路由）
- Produces: JSON 格式决策矩阵（weighted_scores + sensitivity_analysis + recommended_path），写入 Research Passport

- [ ] **Step 1: 创建目录结构**

```bash
mkdir -p ~/.claude/skills/research-compass/references
```

- [ ] **Step 2: 创建 SKILL.md**

写入 `~/.claude/skills/research-compass/SKILL.md`:

```markdown
---
name: research-compass
description: 科研决策罗盘 — 多选项半定量比较工具。将keyanlun的概率思维工具化为加权决策矩阵+敏感性分析。不做单一推荐，呈现"在不同优先级下的最优选择"。Use when choosing between research directions, advisors, career paths, or research layouts. Triggers on: 选方向, 选哪个, 对比选择, 决策矩阵, research decision, which direction.
argument-hint: [options-to-compare]
---

# Research Compass — 科研决策罗盘

将 keyanlun 的"分子/分母""模糊的正确""选择权 vs 选择"原则工具化。**不做单一推荐**——呈现不同优先级下的最优选择，决策权始终在人手中。

## Input

- `$0` — 候选选项（至少2个）+ 决策场景（选导师/选方向/选idea/职业选择/研究布局）

## References

- 评估维度定义: `~/.claude/skills/research-compass/references/compass-prompts.md`
- 决策矩阵模板: `~/.claude/skills/research-compass/references/decision-matrix.md`

## Workflow

### Step 1: 维度定义

根据决策场景自动推荐评估维度，用户可增减和调整权重:

| 场景 | 预设维度 |
|------|---------|
| 选导师 | 发文率 / 延毕率 / 毕业去向 / 指导风格 / 课题组氛围 |
| 选方向 | 论文容量 / 竞争强度 / 实验周期 / 设备条件 / 可承接性 |
| 选idea | 新颖性 / 可行性 / 数据可得性 / 发表潜力 / 后续扩展 |
| 职业选择 | 收入上限 / 稳定性 / 成长空间 / 工作强度 / 地理位置 |
| 研究布局 | 基金命中率 / 学生吸引力 / 合作网络 / 周期 / 风险 |

### Step 2: 证据收集（半定量打分）

每个维度 1-5 分，标注证据来源和置信度:

- **1**: 很弱/不利
- **3**: 中等
- **5**: 很强/有利
- 追求"模糊的正确"而非"精确的错误"
- 每个分数标注证据来源（WoS检索 / 个人观察 / 他人经验 等）

### Step 3: 决策矩阵输出

- 加权评分 + 排名
- **敏感性分析**: 如果最重要的维度权重翻倍，结果会变吗？
- **关键风险**: 排名最高的选项有什么隐藏风险？
- **推荐路径**: 短期做什么 + 长期做什么（而非只选一个）

## Output Format

```json
{
  "scenario": "选导师 | 选方向 | 选idea | 职业选择 | 研究布局",
  "assessor": "用户标识",
  "timestamp": "ISO时间戳",
  "confidence": "high | medium | low",
  "options": ["选项A", "选项B", "选项C"],
  "dimensions": [
    {
      "name": "维度名称",
      "weight": 0.20,
      "description": "评分标准说明",
      "scores": {"选项A": 4, "选项B": 3, "选项C": 2},
      "evidence": {"选项A": "证据描述 (来源, 置信度)", "选项B": "...", "选项C": "..."}
    }
  ],
  "weighted_scores": {"选项A": 3.85, "选项B": 3.10, "选项C": 2.65},
  "sensitivity_analysis": [
    {
      "dimension_varied": "变动维度名",
      "variation": "权重翻倍",
      "result": {"选项A": 4.10, "选项B": 3.30, "选项C": 2.50},
      "rank_change": false
    }
  ],
  "key_risks": [
    {"option": "选项A", "risk": "风险描述", "mitigation": "缓解措施"}
  ],
  "recommended_path": {
    "short_term": "短期行动（0-6月）",
    "long_term": "长期方向（6-18月）",
    "rationale": "为什么不只选一个"
  }
}
```

## Rules

- **不替人决策**: 呈现分析结果，不做"你应该选A"的断言
- **必须标注证据来源**: 每个分数说清楚依据是什么，置信度多少
- **必须做敏感性分析**: 权重是主观的，必须测试权重变化是否颠覆结论
- **模糊的正确 > 精确的错误**: 不要为了算分而编造精确数字
- **考虑选择权**: 短期路径应最大化未来的选择权，而非锁定单一方向

## Related Skills

- **Upstream**: keyanlun（第1/6/7层路由触发）
- **Downstream**: mvp-validator（选定方向后验证idea）
- **See also**: keyanlun 思维工具（分子分母/幸存者偏差/模糊的正确/选择权vs选择/以终为始）
```

- [ ] **Step 3: 创建 references/compass-prompts.md**

写入 `~/.claude/skills/research-compass/references/compass-prompts.md`:

```markdown
# 科研决策罗盘 Prompt 模板

## 维度定义 Prompt

```
用户面临以下决策场景，请推荐评估维度。

要求:
1. 推荐 4-6 个独立维度（不重叠）
2. 每个维度有明确的 1-5 评分标准
3. 默认权重总和为 1.0
4. 维度应与用户的核心诉求对齐

场景: {{scenario}}
候选选项: {{options}}
用户背景: {{user_context}}
```

## 证据评分 Prompt

```
对以下选项在每个维度上打分（1-5）。

要求:
1. 追求"模糊的正确"而非"精确的错误"
2. 每个分数标注证据来源 + 置信度 (high/medium/low)
3. 没有证据的维度坦诚标注"需进一步调研"
4. 不要因为某个选项整体印象好就给所有维度高分（光环效应）

选项: {{options}}
维度: {{dimensions}}
```

## 敏感性分析 Prompt

```
对以下决策矩阵做敏感性分析。

要求:
1. 逐维度测试: 如果该维度权重翻倍，排名会变吗？
2. 如果去掉最高分和最低分维度，排名会变吗？
3. 标注: 哪个维度对结果最敏感？
4. 如果结论对权重变化高度敏感 → 说明需要更多证据

决策矩阵: {{decision_matrix}}
```

## keyanlun 思维工具注入

在评分时，自动应用以下原则:

| 原则 | 应用方式 |
|------|---------|
| **分子/分母** | 看总量不只看个案 — 例如评估发文率时看全组平均而非只看最优秀的 |
| **幸存者偏差** | 区分"成功案例的光环"和"沉默大多数的真相" |
| **模糊的正确** | 1-5 分足够，不追求小数点后两位 |
| **选择权 vs 选择** | 短期路径优先保持灵活性，而非过早锁定 |
| **以终为始** | 从最终目标倒推当前应看重的维度 |
```

- [ ] **Step 4: 创建 references/decision-matrix.md**

写入 `~/.claude/skills/research-compass/references/decision-matrix.md`:

```markdown
# 决策矩阵模板

## 标准模板（Markdown 展示用）

```markdown
## Research Compass — {{scenario}}

评估人: {{assessor}} | 日期: {{date}} | 置信度: {{confidence}}

### 评分矩阵

| 维度 (权重) | {{option_1}} | {{option_2}} | {{option_3}} |
|------------|-------------|-------------|-------------|
{% for dim in dimensions %}| {{dim.name}} ({{dim.weight * 100}}%) | {{dim.scores.option_1}} | {{dim.scores.option_2}} | {{dim.scores.option_3}} |
{% endfor %}
| **加权总分** | **{{weighted.option_1}}** | **{{weighted.option_2}}** | **{{weighted.option_3}}** |

### 敏感性分析

| 变动 | {{option_1}} | {{option_2}} | {{option_3}} | 排名变化? |
|------|-------------|-------------|-------------|----------|
| 原始 | {{w1}} | {{w2}} | {{w3}} | - |
{% for sa in sensitivity %}| {{sa.dimension}} 权重翻倍 | {{sa.result.option_1}} | {{sa.result.option_2}} | {{sa.result.option_3}} | {{sa.rank_change}} |
{% endfor %}

### 关键风险

{% for risk in key_risks %}
⚠️ **{{risk.option}}**: {{risk.risk}}
   缓解: {{risk.mitigation}}
{% endfor %}

### 推荐路径

- **短期 (0-6月):** {{short_term}}
- **长期 (6-18月):** {{long_term}}
- **理由:** {{rationale}}

### 证据来源

{% for dim in dimensions %}
- **{{dim.name}}**: {{dim.evidence_summary}}
{% endfor %}
```

## 敏感性分析方法

### 方法1: 单维度权重翻倍

```
for each dimension d:
    new_weights = original_weights
    new_weights[d] *= 2
    normalize new_weights to sum 1.0
    recompute weighted scores
    check if ranking changes
```

### 方法2: 去掉极值维度

```
去掉权重最高的维度 → 重新计算 → 排名变了吗？
去掉权重最低的维度 → 重新计算 → 排名变了吗？
```

### 方法3: 等权重基线

```
所有维度等权重 → 排名是什么样的？
如果等权重排名与加权排名差异大 → 权重设置驱动了结论
```

### 结果解读

- **结论稳健**: 所有敏感性分析排名不变
- **结论敏感**: 某维度权重翻倍导致排名反转 → 该维度的打分需要更多证据支撑
- **无差别**: 所有选项得分接近 → 可以基于"非量化因素"（兴趣、导师关系等）选择
```

- [ ] **Step 5: 验证文件**

```bash
ls -la ~/.claude/skills/research-compass/
ls -la ~/.claude/skills/research-compass/references/
wc -l ~/.claude/skills/research-compass/SKILL.md
```

- [ ] **Step 6: 提交**

```bash
cd ~/.claude
git add skills/research-compass/
git commit -m "feat: 新增 research-compass skill — 科研决策罗盘

多维度加权决策矩阵 + 敏感性分析 + keyanlun思维工具注入

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## 验证清单

全部 4 个任务完成后，执行以下集成验证:

- [ ] **V1: keyanlun 路由测试**

在 Claude Code 中测试 keyanlun 是否能正确推荐工具链:
```
用户: "我想做食品科学机器学习但不知道具体做什么"
→ 应定位到第1-2层 → 推荐 literature-search → idea-generation → novelty-assessment
```

- [ ] **V2: 新 skill 可发现性测试**

```bash
# 确认所有新 skill 的 YAML frontmatter 可被系统识别
grep -l "name:" ~/.claude/skills/mvp-validator/SKILL.md
grep -l "name:" ~/.claude/skills/figure-storyboard/SKILL.md
grep -l "name:" ~/.claude/skills/research-compass/SKILL.md
```

- [ ] **V3: 现有 skill 未受影响**

```bash
# 快速抽查几个现有 skill 仍可正常读取
head -5 ~/.claude/skills/idea-generation/SKILL.md
head -5 ~/.claude/skills/experiment-design/SKILL.md
head -5 ~/.claude/skills/novelty-assessment/SKILL.md
```

- [ ] **V4: Research Passport 初始化测试**

```bash
# 确认 passport 路径可用，测试 JSON 格式
echo '{"project":"test","current_layer":1,"created":"2026-07-08T00:00:00Z","last_updated":"2026-07-08T00:00:00Z"}' > ~/.hermes/research-passport.json
python3 -m json.tool ~/.hermes/research-passport.json > /dev/null && echo "JSON valid" || echo "JSON invalid"
rm ~/.hermes/research-passport.json  # 清理测试文件
```
