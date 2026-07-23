# PROJECT_STATE.md — My Paper 长链项目状态追踪

> 🧬 **跨会话恢复文件。** 每次对话开始时读取，结束时更新。
> 📅 项目周期：2026-07 — 2029-06（本科毕业）
> 👤 负责人：薛瑞（新疆理工学院 食品科学与工程学院）

---

## 一、项目全景

```
Paper 1（大创）             Paper 2（MD+湿实验）         Paper 3（跨物种推广）
2026-05 ──── 2027-05       2026-07 ──── 2027-01      2027 ──────── 2028
"什么条件风味好？"          "蛋白如何抓住风味？"        "羊肚菌→常见食用菌？"
Condition → Quality        MD揭示机制 + 湿实验验证       P1+P2 方法论跨物种泛化
Food Chemistry / CEA       Food Hydrocolloids         Nature Food / Nat Commun
实验 + AI 预测              MD 模拟 + 荧光/CD/FTIR/GC-MS     多物种 × 四层框架
```

**三篇论文的知识层级：**

```
Layer 1 — 关联（Paper 1）: 干燥条件 → 风味品质，AI 预测
Layer 2 — 因果（Paper 2）: 蛋白构象 → 风味结合，MD 揭示 + 湿实验（荧光/CD/FTIR/GC-MS）验证
Layer 3 — 泛化（Paper 3）: Paper 1+2 方法论从羊肚菌推广到常见食用菌（香菇/平菇/杏鲍菇等）
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
├── 2/                          ← Paper 2：MD + 湿实验
│   ├── 00_项目管理/             对接到 Paper 1 启动文档
│   ├── 01_搜/                   MD文献检索记录 + 关键词演化
│   ├── 04_验/                   ★ 蛋白结构 + 配体库 + 对接结果 + MD脚本 + 湿实验数据
│   └── ...
│
├── 3/                          ← Paper 3：跨物种推广 (Nature Food)
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
| **指导教师** | 裴龙英（新疆理工学院）/ 谢湖均（浙江工商大学，Paper 2 合作） |
| **当前院校** | 浙江工商大学 食品与生物工程学院 |
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
| 2 | ~~GC-MS 配置~~ | — | ✅ 已解决（Agilent 8890-5977B，支持 HS-SPME） |
| 3 | ~~LC-MS 外送~~ | — | ✅ 已解决（学校有设备，无需外送） |
| 4 | ~~计算资源~~ | — | ✅ 已解决（学校有超算中心） |

### 创新核心

> **首次构建整合干燥动力学、HS-SPME-GC-MS 挥发组与 LC-MS 代谢组的动态时间序列可解释 AI 框架**，从静态描述升级为因果机制驱动的风味演化预测。

5维度超越现有研究（Horticulturae 2024）：时间序列（全新）、多模态深度（三模态 vs 二模态+RF）、AI方法（DL+SHAP vs RF）、机制深度（5通路因果 vs 无）、预测能力（有 vs 无）。

### MVE 完成度：85%

```
████████████████░░  85%
```

| Step | 内容 | 状态 |
|------|------|:--:|
| 文献挖掘 | 六篇精读 + 核心文献库 20 篇分类 | ✅ |
| 干燥曲线 | Ivanova 2020 模型方程重建 (443 行) | ✅ |
| 挥发物数据 | Liu 2024 23 种化合物提取 | ✅ |
| 代谢物数据 | Table S1 1645 种代谢物完整分析 | ✅ |
| ML 基线 | RF/XGBoost/Spearman/分组分析 | ✅ |
| 跨组学关联 | 代谢物 × 挥发物 — 受限于 3 温度点 | ⚠️ |
| MVE 报告 | 判定 CONDITIONAL GO + 六论文证据链 | ✅ |
| Gap statement | Introduction 文献缺口论证 | ✅ |
| Materials & Methods | Tier-1 实验方案完整草稿 | ✅ |

**剩余 15% 不是没做完——是文献数据的物理天花板：** 仅 2 重叠温度点无法训练 ML，无配对时序+风味数据无法做跨组学因果推断。只有 Tier-1 实验能突破。

### MVE 判定

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

### 🔴 阻塞项状态

| # | 阻塞项 | 状态 |
|---|--------|:--:|
| B-01 | 原始数据来源 | ✅ 文献验证 |
| B-02 | GC-MS | ✅ Agilent 8890-5977B + HS-SPME (浙工商食品学院) |
| B-03 | LC-MS | ✅ 浙工商自有 (质谱仪 + UHPLC + HPLC×3) |
| B-04 | 计算资源 | ✅ 浙工商超算中心 |
| — | **额外设备** | ✅ 电子鼻、冷冻干燥机、喷雾干燥器、NMR、DSC — 超预期 |

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
| 2026-07-15 | **MVE 完成 → Tier-1**（D-07） | CONDITIONAL GO: 信号存在, 需 Tier-1 实验 |
| 2026-07-15 | **Paper 2 启动**（D-09） | MD模拟 Layer 1 可立即启动, 与 Paper 1 同步推进, 无需等实验数据 |

---

## 三、Paper 2 — MD + 湿实验论文当前状态

### 基本信息

| 字段 | 内容 |
|------|------|
| **完整名称** | 分子动力学模拟揭示羊肚菌干燥过程中温度依赖性蛋白-风味结合机制 |
| **英文名称** | Molecular Dynamics Simulation Reveals Temperature-Dependent Protein-Flavor Binding Mechanisms During Morchella Drying |
| **目标期刊** | Food Hydrocolloids (IF ≈ 10.7) → Food Chemistry (IF ≈ 8.5) |
| **类型** | MD 计算 + 湿实验验证（MD 模拟 + MM/PBSA + 荧光/CD/FTIR/GC-MS 交叉验证） |
| **状态** | 🔬 检索式构建完成，文献调研启动中 |
| **计算资源** | 4× NVIDIA L20 46GB（本地服务器） |
| **湿实验平台** | 浙江工商大学食品学院大型仪器共享平台 |

### Paper 2 进度

| 组件 | 状态 | 备注 |
|------|:--:|------|
| 文献调研 | ⏳ 检索式已就绪 | 5 维度 × 28 条检索式，待执行 |
| 蛋白结构 | ✅ 来自前期工作 | 3 PDB: MBL_lectin (92.2) / Tyrosinase (87.5) / H_lectin (89.5) |
| 配体库 | ✅ 来自前期工作 | 10 化合物 SMILES + 物化性质 |
| 分子对接 | ⚠️ 需补充 | 已有 13 对，需补 H_lectin 对接 |
| MD 试跑 | ⏳ 待执行 | 1 复合物 × 200ns 验证体系 |
| MD 生产 | ⏳ 待执行 | 3 复合物 × 4 温度 × 200ns × 3 重复 |
| MM/PBSA | ⏳ 待执行 | 自由能分解 + 残基贡献 |
| **湿实验验证** | ⏳ 待执行 | **荧光光谱**（结合常数）/ **CD**（构象变化）/ **FTIR**（二级结构）/ **GC-MS**（风味保留） |
| 手稿 | ⏳ 待执行 | 目标 2026 年 12 月完成 |

### Paper 2 工作目录

```
2/
├── 00_项目管理/    README.md（项目总览）+ Paper2_MVE报告 + Paper2_启动文档
├── 01_搜/          检索式记录.md + 关键词演化.md ✅ 已创建
├── 02_聚/          （待文献检索完成后填充）
├── 03_分/          （待文献分组完成后填充）
├── 04_验/          ★ MD + 湿实验核心
│   ├── structures/              3 个 PDB
│   ├── ligands/                 SMILES + 物化性质
│   ├── docking_results/         Vina 对接结果 (13对)
│   ├── md_data/                  MD 轨迹 + MM/PBSA 结果
│   ├── wet_lab/                 荧光/CD/FTIR/GC-MS 实验数据
│   └── scripts/                 MD 脚本 + 分析脚本
├── 05_合/          图表 + 手稿
├── 06_投稿/        Cover Letter + 审稿回复
└── 99_归档/        废弃方案
```

### 与 Paper 1 / Paper 3 的关系

```
Paper 1 (实验+AI)  ──→  风味化合物清单  ──→  Paper 2 (MD+湿实验) 的配体输入
Paper 2 (MD+湿实验) ──→  结合自由能 + 残基 + 湿实验验证  ──→  Paper 3 (跨物种) 的 Layer 1
```

**完整证据链**：分子对接 → MD 模拟 → MM/PBSA 自由能计算 → **湿实验交叉验证**（荧光/CD/FTIR/GC-MS）。MD 结果由湿实验验证，计算与实验形成闭环。

---

## 四、Paper 3 — 跨物种推广（Nature Food 后续）当前状态

### 基本信息

| 字段 | 内容 |
|------|------|
| **完整名称** | Paper 1+2 方法论推广：常见食用菌干燥过程中蛋白质-风味相互作用的多尺度整合框架 |
| **英文名称** | A Multi-Scale Integrative Framework for Protein-Flavor Interactions During Edible Fungi Drying: From Morchella to Common Species |
| **目标期刊** | Nature Food (IF ≈ 23) → Nat Commun (IF ~16.6) → Trends Food Sci (IF ~16.0) |
| **合作导师** | 谢湖均教授（浙江工商大学）— MD 模拟/QSAR |
| **核心思路** | 将 Paper 1 的实验+AI 管线 + Paper 2 的 MD+湿实验方法，从羊肚菌推广到**常见食用菌**（香菇、平菇、杏鲍菇、双孢菇等） |
| **状态** | 🔬 等待 Paper 1 + Paper 2 完成 — 本论文为二者的延伸与泛化 |

### Paper 3 进度

| 组件 | 状态 | 备注 |
|------|:--:|------|
| 文献调研 | ✅ | Morchella 文献基础 + 常见食用菌扩展检索 |
| 蛋白质组筛选 | ✅ | 羊肚菌完成，待扩展到常见食用菌（每个物种 ~10000 蛋白） |
| AlphaFold 结构 | ⏳ | 常见食用菌关键蛋白靶点（同源建模 + AlphaFold 预测） |
| 分子对接管线 | ⚠️ | 羊肚菌管线可复用，需跨物种适配 |
| Layer 1 MD 执行 | ⏳ | 对每种食用菌重复 Paper 2 的 MD+湿实验管线 |
| Layer 2 多组学验证 | ⏳ | 对每种食用菌重复 Paper 1 的 GC-MS/LC-MS 管线 |
| Layer 3 ML 预测 | ⏳ | 跨物种泛化模型（GNN/Transformer），从单一物种→多物种迁移学习 |
| Layer 4 工艺应用 | ⏳ | 不同食用菌的最优干燥工艺参数推荐 |

### Paper 3 工作目录

```
3/
├── 00_项目管理/    README.md + 目标期刊调研
├── 01_搜/          跨物种食用菌文献检索
├── 02_聚/          多物种数据聚合（每种食用菌一套完整数据）
├── 03_分/          跨物种比较分析
├── 04_验/          各物种 MD + 湿实验 + ML 数据
├── 05_合/          跨物种整合图表 + 手稿
└── 99_归档/
```

### 关键空白 (Paper 3 的创新基础)

**尚无跨物种食用菌蛋白-风味相互作用的系统比较研究。** 从单一物种 Morchella 推广到常见食用菌（香菇、平菇、杏鲍菇、双孢菇、金针菇等），建立可泛化的干燥工艺-蛋白构象-风味品质预测框架。

### 四层整合框架（× 多物种）

```
Layer 1: MD 模拟    → 每种食用菌：蛋白构象 + 风味结合自由能（复用 Paper 2 管线）
Layer 2: 多组学验证  → 每种食用菌：荧光/CD/FTIR + GC-MS/LC-MS（复用 Paper 1+2 管线）
Layer 3: ML 预测     → 跨物种 GNN/Transformer → 物种无关的结合亲和力预测
Layer 4: 干燥工艺    → 每种食用菌的最优干燥参数推荐 → 通用风味定向保留策略
```

### 前置依赖

Paper 1 + Paper 2 必须完成，为 Paper 3 提供：(1) 可复用的实验+计算+AI 管线；(2) 羊肚菌基线数据作为跨物种比较的锚点；(3) 已验证的方法论可行性。

---

## 五、技术基础设施

| 组件 | 状态 | 备注 |
|------|------|------|
| **Git 仓库** | ✅ | 独立仓库已初始化，main 分支 |
| **GitHub 备份** | ✅ | https://github.com/RUI-debug769/backup-my-paper |
| **.gitignore** | ✅ | 排除 raw/、venv/、workspace.json、Zotero CSV、.env 等 |
| **实验平台** | ✅ | 浙江工商大学食品学院大型仪器共享平台 (70+台) |
| **GC-MS** | ✅ | 气相色谱质谱联用仪 + 气相色谱仪 ×3 台 |
| **LC-MS** | ✅ | 质谱仪 + 超高压液相色谱仪 + HPLC ×3 台 |
| **HS-SPME** | ✅ | GC-MS 标配附件 |
| **其他关键设备** | ✅ | 电子鼻、冷冻干燥机、喷雾干燥器、NMR、DSC |
| **计算资源** | ✅ | 学校超算中心 + 本地 4× NVIDIA L20 46GB (MD 专用) |
| **Zotero 文献库** | ✅ | 3340+ 条目，Better BibTeX 导出 CSV |
| **Obsidian Vault** | ✅ | 两个子项目独立 vault 配置 |
| **Morchella AI Scientist** | ✅ v2.0 | 14 Agent + keyanlun，独立 git 仓库 |
| **AI 助手** | ✅ | Claude Code + academic-pipeline + ARS + 科学计算 MCP |

---

## 六、目标期刊路线图

```
Paper 1:
  🥇 Food Chemistry (IF ~8.5) → 🥈 CEA (IF ~8.3) → 🥉 Food Chemistry: X (IF ~6.5)

Paper 2:
  🥇 Food Hydrocolloids (IF ~10.7) → 🥈 Food Chemistry (IF ~8.5) → 🥉 JAFC (IF ~6.1)

Paper 3:
  🥇 Nature Food (IF ~23) → 🥈 Nature Communications (IF ~16.6) → 🥉 Trends Food Sci (IF ~16.0) → 保底 Food Chemistry (IF ~8.5)
```

---

## 七、文件快速索引

| 用途 | 路径 |
|------|------|
| 项目总览 | `1/00_项目管理/README.md` |
| 决策追踪 | `1/00_项目管理/决策追踪.md` |
| 科研流程总结 | `1/科研流程总结-大创项目.md` |
| **MVE 报告 (Idea-01)** | `1/04_验/idea-01/MVE报告.md` |
| MVE + ML 数据 | `1/04_验/idea-01/数据/` (5 CSV + 3 Py) |
| **Gap statement** | `1/05_合/合文/gap_statement_introduction.md` |
| **实验执行路线图** | `1/00_项目管理/实验执行路线图.md` |
| **Paper 2 项目总览** | `2/00_项目管理/README.md` |
| **Paper 2 启动文档** | `2/00_项目管理/Paper2_启动文档.md` |
| **Paper 2 检索式** | `2/01_搜/检索式记录.md` |
| **Paper 3 项目总览** | `3/00_项目管理/README.md` |
| **Paper 3 检索式** | `3/01_搜/检索式记录.md` |
| 目标期刊（P1） | `1/00_项目管理/目标期刊-调研.md` |
| 目标期刊（P2） | `2/00_项目管理/目标期刊-调研.md` |
| 文献矩阵 | Morchella_AI_Scientist/literature/ |
| 检索式记录 | `1/01_搜/检索式记录.md` |
| Storyline 总览 | `1/05_合/合图/Storyline总览.md` |
| 自查清单 | `1/05_合/手稿/Checklist-自查.md` |
| **导师汇报文档** | `0/导师汇报-研究进展与毕业论文规划.docx` |
| GitHub 备份 | https://github.com/RUI-debug769/backup-my-paper |

---

## 八、会话追踪日志

| 日期 | 会话摘要 | 关键产出 | 变更文件 |
|------|---------|---------|---------|
| 2026-07-15 | 项目摄入 + 基础设施建立 | PROJECT_STATE.md、决策追踪.md、.gitignore、Git 仓库 + GitHub push | 新建 3 文件 |
| 2026-07-15 | 决策 D-06 + Idea-01 MVE 启动 | 核心假设.md、MVE方案.md；三篇论文精读 + Ivanova 干燥曲线重建 | 新建 5 文件 |
| 2026-07-15 | MVE ML 基线 + 数据补全 | 六篇论文精读；挥发物数据提取；RF/XGBoost 建模；Gap statement | 新建 7 文件，更新 3 文件 |
| 2026-07-15 | MVE 最终报告 + 状态归档 | MVE报告.md: CONDITIONAL GO；Tier-1 实验设计 (72 样本)；PROJECT_STATE 更新 | 累计: 15 新建, 5 更新, 7 次 Git push |
| 2026-07-15 | 导师汇报文档生成 + 博士论文规划 | 导师汇报-研究进展与毕业论文规划.docx (12KB, 9章)；博士论文级撰写路线图 | 新建 1 文件，更新 PROJECT_STATE |
| 2026-07-15 | Table S1 代谢组学完整分析 | 1645 代谢物；272 显著差异；增强 MVE 数据集 (69行×25列)；跨组学关联 | 新建 3 文件 |
| 2026-07-15 | B-03/B-04 解决 + 设备确认 | LC-MS 学校自有；超算可用；GC-MS 待确认 HS-SPME 模块 | 更新 PROJECT_STATE |
| 2026-07-15 | Methods 起草 + B-02 解决 | Materials & Methods 完整草稿 (9章)；GC-MS Agilent 8890-5977B | 新建 1 文件 |
| 2026-07-15 | Paper 2 自主执行 | 蛋白筛选→AlphaFold→PDB→配体库→Vina配置→MD优先级 (12文件) | 新建 12 文件 |
| 2026-07-15 | Paper 1+2 最终状态归档 | P1: 100%就绪等实验; P2: Layer1对接管线完成, 待谢教授超算运行 | 更新 PROJECT_STATE |
| 2026-07-15 | 浙工商设备确认 | 70+台仪器: GC-MS/LC-MS/电子鼻/NMR/DSC/冷冻干燥, 超 Tier-1 需求 | 更新 PROJECT_STATE |
| 2026-07-15 | 实验执行路线图 | 以终为始: 7Fig+3Tab 倒推数据需求 + 8阶段逐周执行计划 | 新建 1 文件 |
| 2026-07-15 | Paper 2 启动 | MD文献调研 (8篇), 蛋白靶点+配体库, MD方案, Layer 1 可立即启动 | 新建 1 文件 |
| 2026-07-15 | Paper 1 完善度检查 + Paper 2 同步 | P1前期100%完成, 等实验; P2 Layer 1 MD可立即开始 | 更新 PROJECT_STATE |
| 2026-07-16 | **三篇论文可行性分析 + Paper 2 启动** | 确认全年供应/LC-MS内部/L20×4资源；Paper 2 (MD+湿实验) 从 Paper 3 解耦独立 | 新建 4 文件，更新 PROJECT_STATE |
| 2026-07-23 | **Paper 2/3 定位修正** | Paper 2 非纯计算——加入湿实验验证（荧光/CD/FTIR/GC-MS）；Paper 3 重新定位为 P1+P2 方法论跨物种推广（羊肚菌→常见食用菌） | 更新 PROJECT_STATE |

---

<!-- 状态码约定 -->
<!-- ✅ 完成 | 🔄 进行中 | ⏳ 待启动 | 🔴 阻塞 | ⚠️ 需关注 | 📝 备注 -->
