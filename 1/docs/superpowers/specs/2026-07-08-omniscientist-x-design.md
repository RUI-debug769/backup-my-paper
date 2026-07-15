# OmniScientist X — 科研体系优化设计文档

> 日期: 2026-07-08 | 状态: 设计已确认 | 作者: 薛瑞 + Claude

---

## 一、背景与动机

用户基于《告别迷茫，高效产出：科研论7层攻略与5步实操法》材料，提出了 OmniScientist X 全生命周期科研智能体 Prompt。经逐项分析发现，该 Prompt 的核心方法论（7层导航、5步工作流、Contribution First、MVP验证等）**已存在于现有科研体系中**（主要是 keyanlun skill），但存在以下三个关键问题：

1. **方法论与执行层断裂**：keyanlun 提供7层导航 + 5步法框架，但无法自动路由到 ARS plugin 和 25+ 独立 skills
2. **关键执行环节模糊**：MVP验证、Figure故事线设计、量化决策在现有体系中"概念有但执行路径不具体"
3. **缺乏跨层状态追踪**：用户在不同层级间跳转时，没有统一的"科研护照"追踪进度

## 二、设计目标

在不重构现有体系的前提下，通过**最小增量改动**实现 OmniScientist X 的核心价值：

- keyanlun 增强网关能力（自动路由 + 状态追踪）
- 创建 3 个精悍补缺模块
- 现有 ARS plugin + 25 skills 完全不动

## 三、架构：三层整合模型

```
用户科研需求
     ↓
┌─────────────────────────────────────────────┐
│  L0: 网关层 (keyanlun 增强)                    │
│  7层诊断 → 自动调度 → Research Passport 追踪    │
│  改动: SKILL.md 新增 2 个 section                │
└─────────────────────────────────────────────┘
     ↓ 路由分发
┌─────────────────────────────────────────────┐
│  L1: 补缺模块 (3 个新 skill)                   │
│  mvp-validator / figure-storyboard /          │
│  research-compass                             │
│  改动: 在 ~/.claude/skills/ 下新建 3 个目录     │
└─────────────────────────────────────────────┘
     ↓ 执行调度
┌─────────────────────────────────────────────┐
│  L2: 执行层 (现有体系，不动)                    │
│  ARS plugin (academic-pipeline/papers/        │
│  reviewer) + 25+ 独立 skills                   │
└─────────────────────────────────────────────┘
```

## 四、L0 网关层 — keyanlun 增强

### 4.1 改造范围

**仅修改** `~/.claude/skills/keyanlun/SKILL.md`，在现有内容末尾新增两个 section。现有7层路由、5步法、17思维工具、8核心原则**完全不动**。

### 4.2 新增 Section：自动调度映射表

```markdown
## 自动调度映射表（v2 新增）

当定位到层级后，自动向用户推荐下游执行工具：

| 层级 | 核心矛盾 | 推荐工具链 | 触发条件 |
|------|---------|-----------|---------|
| 第1层 | "选谁/选哪" | advisor-search → advisor-analysis → research-compass | 用户未选定导师/方向 |
| 第2层 | "做什么" | literature-search / scientific-literature-retrieval → idea-generation → novelty-assessment | 方向明确但无具体课题 |
| 第3层 | "靠不靠谱" | mvp-validator → experiment-design | 有 idea 待验证 |
| 第4层 | "怎么做" | figure-storyboard → academic-paper(full) 或 paper-assembly | idea 已验证 |
| 第5层 | "顺利通关" | paper-assembly → slide-generation | 小论文已完成 |
| 第6层 | "布局毕业" | research-compass + 决策矩阵 | 即将毕业 |
| 第7层 | "指导+申请" | survey-generation + research-compass | 青年教师 |
| 游离层 | "回归正轨" | toolkit-mindset → 最低耗能动作 | 情绪/人际问题 |

调度规则：
- 用户可跳过推荐，直接指定工具
- 每步完成后自动更新 Research Passport
- 工具链按顺序执行，前一步输出作为后一步输入
- 当用户提供已有材料（如已有文献库），自动跳过已完成步骤
```

### 4.3 新增 Section：Research Passport

```markdown
## Research Passport（科研护照）— v2 新增

轻量状态文件，路径: `~/.hermes/research-passport.json`

### 数据结构
{
  "project": "项目名称",
  "created": "2026-07-08T...",
  "current_layer": 2,
  "layer_history": [
    {
      "layer": 1,
      "status": "completed",
      "started": "...",
      "completed": "...",
      "output_summary": "选定XX方向，导师YY",
      "artifacts": ["advisor-analysis.md"]
    }
  ],
  "five_steps_progress": {
    "搜": "completed",
    "聚": "completed",
    "分": "in_progress",
    "验": "pending",
    "合": "pending"
  },
  "active_tools": ["idea-generation"],
  "next_recommended": "mvp-validator",
  "last_updated": "2026-07-08T..."
}

### 自动行为
- 对话开始时自动读取 passport，恢复上下文
- 每次层级或5步法状态变更时自动更新
- 与 academic-pipeline 的 Material Passport 双向同步（当进入第4层时）
- 支持多项目并行：每个项目一个 passport 文件
```

## 五、L1 补缺模块一 — `mvp-validator`

### 5.1 解决的问题

keyanlun 工具 1.7 定义了 MVE（最小可行验证）概念，但执行路径模糊。本模块将其具体化为可操作的验证工作流。

### 5.2 触发方式

- 直接调用: `/mvp-validator "研究idea描述"`
- keyanlun 第3层自动路由触发
- 上游依赖: idea-generation / novelty-assessment 的输出

### 5.3 工作流

```
Step 1: 核心假设提取
  → 从 idea 中拆出 1-3 个可证伪的核心假设
  → 追问: "如果这个假设错了，整个方向还成立吗？"
  → 区分"必要条件假设"和"充分条件假设"

Step 2: 第一性原理检查
  → 为什么可能有效？（基础机制层面）
  → 是否存在反例或边界条件？
  → 区分创新等级: genuine / incremental / trivial

Step 3: 最小验证方案生成
  → 最低成本验证路径（数据/时间/设备）
  → 需要什么数据？标注: 已有 / 可获取 / 需采集
  → 关键指标 + 成功/失败阈值
  → 预估时间

Step 4: 止损条件 + 备选方案
  → 什么情况下应该放弃这个 idea？
  → 备选方向是什么？
```

### 5.4 输出格式

```json
{
  "idea": "原始idea描述",
  "core_hypotheses": [
    {
      "hypothesis": "可证伪的假设陈述",
      "testable": true,
      "falsifiable": true,
      "if_wrong_impact": "critical | moderate | minor"
    }
  ],
  "first_principles_check": {
    "why_might_work": "基础机制解释",
    "counter_examples": ["已有反例或边界条件"],
    "innovation_level": "genuine | incremental | trivial",
    "innovation_justification": "判断依据"
  },
  "mvp_plan": {
    "minimal_cost_path": "最低成本验证路径描述",
    "data_required": {
      "already_have": ["已有数据1"],
      "can_obtain": ["可获取数据1"],
      "need_collect": ["需采集数据1"]
    },
    "key_metrics": [
      {"metric": "指标名", "success_threshold": "阈值", "measurement": "测量方式"}
    ],
    "estimated_time": "预估时间"
  },
  "stop_conditions": [
    "具体可量化的放弃条件"
  ],
  "fallback_direction": "备选方向描述"
}
```

### 5.5 文件结构

```
~/.claude/skills/mvp-validator/
├── SKILL.md
└── references/
    └── mvp-prompts.md    # 假设提取、第一性原理检查、止损判断的 prompt 模板
```

### 5.6 与其他模块的关系

- **上游**: idea-generation, novelty-assessment, keyanlun 工具1.7
- **下游**: experiment-design, experiment-code
- **复用**: novelty-assessment 的 harsh critic persona、keyanlun 的"做减法"和"行动导向"原则

## 六、L1 补缺模块二 — `figure-storyboard`

### 6.1 解决的问题

keyanlun 提出"合.图先行"（合.图/表/公式先行于合.文），但缺少从研究结果到具体 Figure 规划的桥梁。本模块填补这个缺口。

### 6.2 触发方式

- 直接调用: `/figure-storyboard "研究问题 + 核心发现描述"`
- keyanlun 第4层路由触发，在 academic-paper 之前执行
- 上游依赖: 实验/分析结果（至少初步结果）

### 6.3 工作流

```
Step 1: 故事线提取
  → 从研究问题和核心发现中提炼"一句话故事线"
  → 例: "我们发现X因素通过Y机制影响Z结果，且这种影响在A条件下被放大"
  → 标注故事的"起承转合"

Step 2: Figure Panel 规划
  → 按故事线设计 4-6 张 Figure 的层级关系
  → 每张图标注:
    - 回答什么科学问题？
    - 使用什么数据？
    - 和前后图的关系是什么？
    - 推荐图表类型

Step 3: 图文映射 + 下游对接
  → 为每张 Figure 标注所需的数据分析、统计方法
  → 输出可直接对接 figure-generation / table-generation / excalidraw-skill
```

### 6.4 输出格式 — Figure 故事板

```
## 论文故事线
[一句话核心故事]

## Figure 故事板

### Figure 1: 科学问题与研究框架
- 回答: 为什么要研究这个？已知什么？Gap 在哪？
- 数据: 文献总结 + 概念框架
- 图类型: 示意图/流程图
- 承接: → 引出 Figure 2 的方法体系

### Figure 2: 方法体系
- 回答: 怎么研究？技术路线是什么？
- 数据: 实验设计概览
- 图类型: 方法流程图或表
- 承接: → 为 Figure 3 提供技术背景

### Figure 3: 核心发现
- 回答: 最重要的实验结果是什么？
- 数据: 主要实验数据
- 图类型: 多 panel 组合图
- 承接: → 解释 Figure 4 中的机制

### Figure 4: 机制解释
- 回答: 为什么会有这样的结果？
- 数据: 机制验证实验
- 图类型: 相关性分析 + 机制示意图
- 承接: → Figure 5 验证普适性

### Figure 5: 验证与应用
- 回答: 这个发现有多大适用范围？
- 数据: 验证实验/模型预测
- 图类型: 预测 vs 实测对比图
- 收尾: → 回到 Figure 1 的科学问题，形成闭环

## 下游对接
- Figure 1 (示意图) → excalidraw-skill 或 TikZ
- Figure 3,4,5 (数据图) → figure-generation (Python/R)
- Figure 2 (表) → table-generation
- 完整故事线 → academic-paper (Introduction + Discussion 写作依据)
```

### 6.5 文件结构

```
~/.claude/skills/figure-storyboard/
├── SKILL.md
└── references/
    ├── storyboard-prompts.md    # 故事线提取、panel 规划的 prompt
    └── figure-patterns.md       # 各学科常见 Figure 组合模式
```

### 6.6 与其他模块的关系

- **上游**: experiment-design, data-analysis 的结果
- **下游**: figure-generation, table-generation, academic-paper
- **复用**: keyanlun "合.图先行"方法论、ARS structure_architect_agent

## 七、L1 补缺模块三 — `research-compass`

### 7.1 解决的问题

keyanlun 强调"选择远比努力重要"和"概率思维"，但缺少将多选项量化为可比较数据的工具。本模块将"分子/分母""模糊的正确""选择权 vs 选择"等原则工具化。

### 7.2 触发方式

- 直接调用: `/research-compass "选项A vs 选项B vs 选项C"`
- keyanlun 第1层（选方向）、第6层（职业选择）、第7层（研究布局）自动触发

### 7.3 核心设计原则

**不做单一推荐，而是呈现"在不同优先级下的最优选择"**。科研决策是价值判断，不是数学优化——工具只负责让比较"可见、可量化"。

### 7.4 工作流

```
Step 1: 维度定义
  → 根据层级自动推荐评估维度
  → 用户可增减维度、调整权重
  → 每个维度有明确的评分标准 (1-5)

Step 2: 证据收集（半定量）
  → 每个维度打分 1-5
  → 标注证据来源 + 置信度 (high/medium/low)
  → 追求"模糊的正确"而非"精确的错误"

Step 3: 决策矩阵输出
  → 加权评分 + 敏感性分析
  → 关键风险标注
  → 给出"短期+长期"组合路径
```

### 7.5 按层级预设评估维度

| 层级 | 场景 | 预设维度 |
|------|------|---------|
| 第1层 | 选导师 | 发文率 / 延毕率 / 毕业去向 / 指导风格 / 课题组氛围 |
| 第1层 | 选方向 | 论文容量 / 竞争强度 / 实验周期 / 设备条件 / 可承接性 |
| 第2层 | 选idea | 新颖性 / 可行性 / 数据可得性 / 发表潜力 / 后续扩展 |
| 第6层 | 职业选择 | 收入上限 / 稳定性 / 成长空间 / 工作强度 / 地理位置 |
| 第7层 | 研究布局 | 基金命中率 / 学生吸引力 / 合作网络 / 周期 / 风险 |

### 7.6 输出格式

```json
{
  "scenario": "选研究方向",
  "assessor": "用户标识",
  "confidence": "medium",
  "options": ["方向A", "方向B", "方向C"],
  "dimensions": [
    {"name": "论文容量", "weight": 0.20, "scores": {"方向A": 5, "方向B": 3, "方向C": 4}},
    {"name": "竞争强度", "weight": 0.20, "scores": {"方向A": 2, "方向B": 4, "方向C": 3}},
    {"name": "实验周期", "weight": 0.15, "scores": {"方向A": 5, "方向B": 2, "方向C": 3}},
    {"name": "设备条件", "weight": 0.15, "scores": {"方向A": 5, "方向B": 3, "方向C": 2}},
    {"name": "可承接性", "weight": 0.30, "scores": {"方向A": 4, "方向B": 3, "方向C": 2}}
  ],
  "weighted_scores": {"方向A": 4.05, "方向B": 3.10, "方向C": 2.75},
  "sensitivity_analysis": [
    {"dimension_varied": "设备条件", "weight_doubled": {"方向A": 4.40, "方向B": 3.25, "方向C": 2.40}},
    {"dimension_varied": "竞争强度", "weight_doubled": {"方向A": 3.75, "方向B": 3.50, "方向C": 2.85}}
  ],
  "key_risks": [
    {"option": "方向A", "risk": "纯计算可能被质疑缺少机制深度", "mitigation": "验证阶段加入湿实验"}
  ],
  "evidence_sources": [
    {"dimension": "论文容量", "source": "WoS检索近5年发文量", "details": "方向A: 2300篇, 方向B: 870篇"}
  ],
  "recommended_path": {
    "short_term": "方向A快速出成果",
    "long_term": "A+B交叉: AI驱动的机制研究"
  }
}
```

### 7.7 与 keyanlun 思维工具的映射

| compass 机制 | 对应思维工具 | 说明 |
|-------------|------------|------|
| 加权评分 | 分子/分母 | 看总量，不只看个案 |
| 敏感性分析 | 模糊的正确 | 不追求精确数字 |
| 证据来源标注 | 幸存者偏差 | 区分信号和噪声 |
| 短期/长期路径 | 选择权 vs 选择 | 先获得选择权再比较选项 |

### 7.8 文件结构

```
~/.claude/skills/research-compass/
├── SKILL.md
└── references/
    ├── compass-prompts.md      # 各层级评估维度定义 + 评分标准
    └── decision-matrix.md      # 决策矩阵模板 + 敏感性分析方法
```

### 7.9 与其他模块的关系

- **上游**: keyanlun 第1/6/7层诊断结果
- **下游**: 将决策结果写入 Research Passport，驱动下一层级的工具链
- **复用**: keyanlun 9项思维工具（分子分母/幸存者偏差/模糊的正确/选择权vs选择/以终为始）

## 八、整合：完整科研工作流

### 8.1 典型用户旅程（从零到论文）

```
用户: "我想做食品科学方向的机器学习研究，但不知道具体做什么"
  ↓
keyanlun L0 网关: 定位到第1层 → 第2层
  ↓
[搜] scientific-literature-retrieval: WoS + Scopus 检索
  ↓
[聚] 文献导入 Zotero → literature-review 标注
  ↓
[分] keyanlun 粗分/细分 → 发现 3 个潜在方向
  ↓
research-compass: 3个方向决策矩阵 → 选定方向A
  ↓
idea-generation: 生成 5 个具体 idea
  ↓
novelty-assessment: 排除 2 个已被发表的 → 剩 3 个
  ↓
mvp-validator: 对 top idea 做最小可行验证方案
  ↓
[验] experiment-design → experiment-code → 跑实验
  ↓
figure-storyboard: 根据实验结果设计 Figure 故事线
  ↓
[合.图] figure-generation + table-generation 出图
  ↓
[合.文] academic-paper(full) 写论文
  ↓
academic-paper-reviewer 审稿模拟
  ↓
投稿
```

### 8.2 跨层状态追踪

所有进展自动写入 `~/.hermes/research-passport.json`，下次对话自动恢复：

```json
{
  "project": "羊肚菌AI品质预测",
  "current_layer": 4,
  "five_steps_progress": {
    "搜": "completed",
    "聚": "completed",
    "分": "completed",
    "验": "completed",
    "合": "in_progress"
  },
  "milestones": [
    {"date": "2026-07-01", "event": "选定方向: 多模态融合预测"},
    {"date": "2026-07-05", "event": "MVP验证通过"},
    {"date": "2026-07-08", "event": "Figure故事板完成"}
  ],
  "next_recommended": "academic-paper (Introduction 写作)"
}
```

## 九、实施计划概要

### 9.1 改动清单

| 序号 | 类型 | 组件 | 改动内容 | 优先级 |
|------|------|------|---------|--------|
| 1 | 修改 | keyanlun/SKILL.md | 新增"自动调度映射表" + "Research Passport" section | P0 |
| 2 | 新建 | skills/mvp-validator/ | SKILL.md + references/mvp-prompts.md | P0 |
| 3 | 新建 | skills/figure-storyboard/ | SKILL.md + references/storyboard-prompts.md + figure-patterns.md | P1 |
| 4 | 新建 | skills/research-compass/ | SKILL.md + references/compass-prompts.md + decision-matrix.md | P1 |

### 9.2 不改动的组件

- ARS plugin (academic-pipeline, academic-paper, academic-paper-reviewer) — 完全不动
- 25+ 独立科研 skills — 完全不动
- keyanlun 现有7层路由、5步法、17思维工具 — 完全不动
- scientific-literature-retrieval skill — 不动，作为 literature-search 的补充被调度

### 9.3 风险与注意事项

1. **keyanlun SKILL.md 已较长**（约240行），新增内容需精简控制在50行以内
2. **Research Passport 与 Material Passport 的双向同步**需注意字段映射，避免冲突
3. **三个新模块均为轻量 skill**，各自 SKILL.md 控制在 100 行以内，不引入新的 plugin agent
4. **不引入新的 MCP 工具或外部依赖**，所有新模块复用现有脚本（novelty_check.py 等）

## 十、成功标准

- [ ] keyanlun 定位层级后，能自动推荐下游工具链
- [ ] mvp-validator 能将模糊 idea 转化为可证伪假设 + 量化止损条件
- [ ] figure-storyboard 能输出 4-6 张 Figure 的故事板，每张标注"回答什么/用什么数据"
- [ ] research-compass 能输出多维度加权决策矩阵 + 敏感性分析
- [ ] Research Passport 正确追踪状态，跨对话可恢复
- [ ] 现有所有 skill 和 plugin 功能不受影响
