# PROJECT_STATE.md — My Paper 长链项目状态追踪

> 🧬 **跨会话恢复文件。** 每次对话开始时读取，结束时更新。
> 📅 项目周期：2026-07 — 2029-06（本科毕业）
> 👤 负责人：薛瑞（新疆理工学院 食品科学与工程学院）

---

## 一、项目全景

```
Paper 1（大创）                      Paper 2（后续）
2026-05 ──────── 2027-05            2027 ──────── 2028
"什么条件风味好？"        ──→        "为什么这个条件风味好？"
Condition → Quality                 Mechanism → Principle
Food Chemistry / CEA                Nature Food
```

### 项目文件结构

```
My Paper/
├── 1/                          ← Paper 1：大创项目
│   ├── 00_项目管理/            会议记录 + README + 目标期刊调研
│   ├── 01_搜/                  文献检索记录 + 原始题录导出
│   ├── 02_聚/                  PDF仓库（已读/待读）
│   ├── 03_分/                  分组记录 + 候选Idea + 空白机会卡
│   ├── 04_验/                  3 Idea（idea-01主攻/02辅助/03远期）+ MVE方案
│   ├── 05_合/                  图表规划 + 手稿骨架 + 自查清单
│   ├── 06_投稿/                Cover Letter + 审稿意见 + 最终稿
│   ├── 07_实验数据/            原始数据 + 分析脚本 + 实验记录
│   └── 99_归档/                废弃idea + 早期版本
│
├── 2/                          ← Paper 2：Nature Food 后续
│   └── (same structure)
│
├── Zotero_Export_All.csv       ← 3340+ 参考文献全库（2026-07-14导出）
├── PROJECT_STATE.md            ← 本文件
└── .obsidian/                  ← Obsidian vault 配置
```

---

## 二、Paper 1 — 大创项目当前状态

### 基本信息

| 字段 | 内容 |
|------|------|
| **完整名称** | 多模态 AI 驱动羊肚菌干燥动态风味演化预测 |
| **英文名称** | Multimodal AI-Driven Dynamic Flavor Evolution Prediction for Morchella Drying |
| **类型** | 大学生创新创业训练计划 |
| **周期** | 2026-05 → 2027-05 |
| **指导教师** | 裴龙英 |
| **团队** | 5人 |
| **主项目路径** | `C:\Users\26404\Desktop\Morchella_AI_Scientist` |
| **AI 系统** | Morchella AI Scientist v2.0（14 Agent + keyanlun） |

### keyanlun 五步法进度

| 阶段 | 状态 | 产出 | 完成日期 |
|------|------|------|---------|
| 【搜】文献检索 | ✅ 完成 | 31篇矩阵、Zotero 3340篇全库筛选 | 2026-07-14 |
| 【聚】知识组织 | ✅ 完成 | PDF仓库（已读/待读）、趋势地图 | 2026-07-14 |
| 【分】空白发现 | ✅ 完成 | 7个机会卡（G01-G07）、差异化重定位 | 2026-07-14 |
| 【验】假设验证 | ✅ MVE 完成 | CONDITIONAL GO, 六篇论文, ML 基线, MVE 报告 | 2026-07-15 |
| 【合】整合写作 | 🔄 启动中 | Gap statement 已撰写 | 2026-07-15 |
| 【投稿】 | ⏳ 待启动 | — | — |

### 🔴 当前阻塞项（需决策）

| # | 阻塞项 | 影响 | 优先级 |
|---|--------|------|--------|
| 1 | ~~原始数据来源~~ | — | ✅ 已解决（D-06：文献数据验证） |
| 2 | **GC-MS 机时** — HS-SPME-GC-MS 上机预约周期？ | 决定 Tier-2 时间线 | 🔴 P0 |
| 3 | **LC-MS 外送** — 非靶向代谢组费用？（~500-800元/样） | 决定样本量 | 🟡 P1 |
| 4 | **计算资源** — 本地 GPU or 远程服务器？ | 决定模型复杂度 | 🟡 P1 |

### 创新核心

> **首次构建整合干燥动力学、HS-SPME-GC-MS 挥发组与 LC-MS 代谢组的动态时间序列可解释 AI 框架**，从静态描述升级为因果机制驱动的风味演化预测。

5维度超越现有研究（Horticulturae 2024）：时间序列（全新）、多模态深度（三模态 vs 二模态+RF）、AI方法（DL+SHAP vs RF）、机制深度（5通路因果 vs 无）、预测能力（有 vs 无）。

### MVE 结果

| 指标 | 结果 |
|------|------|
| **判定** | 🟡 CONDITIONAL GO |
| 类别级相关性 | Esters ρ=-0.89, Hydrocarbons ρ=+0.89 |
| ML 全局 R² | 无法训练 (仅 2 重叠温度点) |
| 方法论可行性 | ✅ 3 篇独立论文 AI R²>0.96 |
| **根因** | 文献中无同时采集时序动力学 + 时序风味的研究 |
| **Gap statement** | 已撰写 → `1/05_合/合文/gap_statement_introduction.md` |

### Tier-1 实验设计（MVE 输出）

```
温度: 45, 55, 65, 75°C (4 水平)
时间点: 0, 1.5, 3, 5, 7, 终点 h (6 水平)
重复: 3 生物学重复
总样本: 72 组
检测: MR + HS-SPME-GC-MS + LC-MS/MS + 色差/收缩率
```

### ⚠️ 文献引用纠正

| 项目文档原称 | 实际论文 |
|------------|---------|
| "Guo L 2024 (Horticulturae)" | **Liu T** et al. 2024, Horticulturae 10, 812 |
| — | **Guo J** et al. 2025, CEA 230, 109929 (杏鲍菇) |

### 关键决策记录

| 日期 | 决策 | 原因 |
|------|------|------|
| 2026-07-09 | GC-IMS → HS-SPME-GC-MS | 实验室无 GC-IMS；GC-MS 定性/OAV 更契合 |
| 2026-07-09 | 分层 MVE 路线 | Tier-1 即使缺 GC-MS 也可成文 |
| 2026-07-14 | 差异化重定位 | Horticulturae 2024 已三模态联合 → 创新调整为动态时序+DL+SHAP+因果 |
| 2026-07-14 | G07 Digital Twin 远期储备 | 写入 Discussion 展望提升论文高度 |
| 2026-07-14 | 主攻 Idea-01（G01+G02+G04 三合一） | 创新性最高、差异化最显著 |
| 2026-07-15 | **文献数据先行验证**（D-06） | 无需等实验，立即启动 MVE；用已发表论文数据验证核心假设 |
| 2026-07-15 | **MVE 完成 → Tier-1**（D-07） | CONDITIONAL GO: 信号存在(\|ρ\|≈0.9)但文献数据不足，需 Tier-1 实验 |

---

## 三、Paper 2 — Nature Food 后续项目当前状态

### 基本信息

| 字段 | 内容 |
|------|------|
| **完整名称** | 多尺度整合框架揭示羊肚菌干燥过程中蛋白质-风味相互作用 |
| **英文名称** | A Multi-Scale Integrative Framework Revealing Protein-Flavor Interactions During Morchella Drying |
| **目标期刊** | Nature Food (IF ≈ 23) |
| **时间定位** | 2027-2028（大创结题后启动） |
| **潜在合作** | 谢湖均教授（浙江工商大学）— MD 模拟/QSAR |
| **状态** | ⏳ 概念阶段 — Proposal Outline 已起草 |

### 四层整合框架

```
Layer 1: MD 模拟    → 原子尺度：蛋白构象 + 风味结合自由能
Layer 2: 多组学验证  → 分子尺度：荧光/CD/FTIR + GC-MS 顶空定量
Layer 3: ML 预测     → 数据尺度：GNN/Transformer → 结合亲和力
Layer 4: 干燥工艺    → 宏观尺度：aw 阈值 → 风味定向保留策略
```

### 前置依赖

Paper 1 必须产出：关键风味化合物清单、最优干燥条件、OAV 数据 — 这些是 Paper 2 的输入。

---

## 四、技术基础设施

| 组件 | 状态 | 备注 |
|------|------|------|
| **Git 仓库** | ✅ | 独立仓库已初始化，main 分支 |
| **GitHub 备份** | ✅ | https://github.com/RUI-debug769/backup-my-paper |
| **.gitignore** | ✅ | 排除 raw/、venv/、workspace.json、Zotero CSV、.env 等 |
| **Zotero 文献库** | ✅ | 3340+ 条目，Better BibTeX 导出 CSV |
| **Obsidian Vault** | ✅ | 两个子项目独立 vault 配置 |
| **Morchella AI Scientist** | ✅ v2.0 | 14 Agent + keyanlun，独立 git 仓库 |
| **AI 助手** | ✅ | Claude Code + academic-pipeline + ARS + 科学计算 MCP |

---

## 五、目标期刊路线图

```
Paper 1:
  🥇 Food Chemistry (IF ~8.5) → 🥈 CEA (IF ~8.3) → 🥉 Food Chemistry: X (IF ~6.5)

Paper 2:
  🥇 Nature Food (IF ~23) → 🥈 Nature Communications (IF ~16.6) → 🥉 Trends Food Sci (IF ~16.0) → 保底 Food Chemistry (IF ~8.5)
```

---

## 六、文件快速索引

| 用途 | 路径 |
|------|------|
| 项目总览 | `1/00_项目管理/README.md` |
| 决策追踪 | `1/00_项目管理/决策追踪.md` |
| 科研流程总结 | `1/科研流程总结-大创项目.md` |
| **MVE 报告 (Idea-01)** | `1/04_验/idea-01/MVE报告.md` |
| MVE + ML 数据 | `1/04_验/idea-01/数据/` (5 CSV + 3 Py) |
| **Gap statement** | `1/05_合/合文/gap_statement_introduction.md` |
| Paper 2 大纲 | `2/Nature_Food_Proposal_Outline.docx` |
| Paper 2 总览 | `2/00_项目管理/README.md` |
| 目标期刊（P1） | `1/00_项目管理/目标期刊-调研.md` |
| 目标期刊（P2） | `2/00_项目管理/目标期刊-调研.md` |
| 文献矩阵 | Morchella_AI_Scientist/literature/ |
| 检索式记录 | `1/01_搜/检索式记录.md` |
| Storyline 总览 | `1/05_合/合图/Storyline总览.md` |
| 自查清单 | `1/05_合/手稿/Checklist-自查.md` |
| **导师汇报文档** | `0/导师汇报-研究进展与毕业论文规划.docx` |
| GitHub 备份 | https://github.com/RUI-debug769/backup-my-paper |

---

## 七、会话追踪日志

| 日期 | 会话摘要 | 关键产出 | 变更文件 |
|------|---------|---------|---------|
| 2026-07-15 | 项目摄入 + 基础设施建立 | PROJECT_STATE.md、决策追踪.md、.gitignore、Git 仓库 + GitHub push | 新建 3 文件 |
| 2026-07-15 | 决策 D-06 + Idea-01 MVE 启动 | 核心假设.md、MVE方案.md；三篇论文精读 + Ivanova 干燥曲线重建 | 新建 5 文件 |
| 2026-07-15 | MVE ML 基线 + 数据补全 | 六篇论文精读；挥发物数据提取；RF/XGBoost 建模；Gap statement | 新建 7 文件，更新 3 文件 |
| 2026-07-15 | MVE 最终报告 + 状态归档 | MVE报告.md: CONDITIONAL GO；Tier-1 实验设计 (72 样本)；PROJECT_STATE 更新 | 累计: 15 新建, 5 更新, 7 次 Git push |
| 2026-07-15 | 导师汇报文档生成 + 博士论文规划 | 导师汇报-研究进展与毕业论文规划.docx (12KB, 9章)；博士论文级撰写路线图 | 新建 1 文件，更新 PROJECT_STATE |

---

<!-- 状态码约定 -->
<!-- ✅ 完成 | 🔄 进行中 | ⏳ 待启动 | 🔴 阻塞 | ⚠️ 需关注 | 📝 备注 -->
