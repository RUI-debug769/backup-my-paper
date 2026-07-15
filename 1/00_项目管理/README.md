# 00_项目管理 — 项目总览

---

## 项目基本信息

| 字段 | 内容 |
|------|------|
| **项目名称** | 多模态 AI 驱动羊肚菌干燥动态风味演化预测 |
| **英文名称** | Multimodal AI-Driven Dynamic Flavor Evolution Prediction for Morchella Drying |
| **项目类型** | 大学生创新创业训练计划（大创） |
| **项目周期** | 2026年5月 — 2027年5月 |
| **负责人** | 薛瑞（新疆理工学院 食品科学与工程学院 食检25-2班） |
| **指导教师** | 裴龙英 |
| **团队成员** | 5人 |
| **主项目路径** | `C:\Users\26404\Desktop\Morchella_AI_Scientist` |
| **AI 辅助系统** | Morchella AI Scientist v2.0（14 Agent + keyanlun 七层模型驱动） |

---

## 核心科学问题

> **干燥如何调控代谢转化与挥发性风味演化？AI 如何预测风味品质动态？**

---

## 研究框架

```
干燥动力学（热质传递：Deff, 活化能, 水分比, aw）
    +
挥发组学 volatilomics（HS-SPME-GC-MS → OAV 加权风味标签）
    +
代谢组学 metabolomics（LC-MS 非靶向 → 差异代谢物 → 通路富集）
    ↓
多模态时序数据融合（6-8 个干燥时间点采样）
    ↓
ML 基线（LR / RF / XGBoost）→ 深度学习（LSTM / Transformer）
    ↓
SHAP 可解释性 → 特征→化合物→通路映射
    ↓
5条代谢通路因果机制模型 → 风味动态预测 + 干燥工艺反向优化
```

---

## 差异化创新点

| 维度 | 已有研究（Horticulturae 2024 等） | 本项目 |
|------|------|--------|
| **时间维度** | 静态终点比较 | **动态时间序列**（6-8个采样点） |
| **数据模态** | 最多 GC-IMS + LC-MS | 干燥动力学 + **HS-SPME-GC-MS + LC-MS** 三模态 |
| **AI 方法** | Random Forest（特征重要性） | RF→XGBoost→**深度学习 + SHAP 因果解释** |
| **机制深度** | "化合物随干燥变化"描述 | **5条代谢通路因果机制模型** |
| **预测能力** | 无 | **干燥参数→风味动态预测（目标 R²>0.90）** |

---

## 技术栈

| 层 | 工具/技术 |
|----|----------|
| **实验** | 热泵干燥、微波干燥、电子鼻 PEN3、HS-SPME-GC-MS、LC-MS、质构仪 |
| **编程** | Python, TensorFlow/Keras, PyTorch, Scikit-learn, XGBoost, SHAP |
| **AI 辅助** | Claude Code + keyanlun 七层模型 + 14 Agent 科研管线 |
| **文献** | Zotero（3340+ 条目）、PubMed、bioRxiv、Web of Science |
| **知识管理** | Obsidian vault |

---

## 目标期刊（按优先序）

1. **Food Chemistry** (IF ≈ 8.5) — 食品分析化学顶刊
2. **Computers and Electronics in Agriculture** (IF ≈ 8.3) — AI+干燥方向
3. **Food Chemistry: X** (IF ≈ 6.5) — 已有羊肚菌干燥论文基础

详见 [`目标期刊-调研.md`](目标期刊-调研.md)

---

## keyanlun 进度

| 五步法 | 状态 | 产出 |
|--------|------|------|
| **【搜】** | ✅ 完成 | 31篇文献矩阵 + Zotero 3340篇全库筛选 |
| **【聚】** | ✅ 完成 | PDF仓库（已读/待读）+ 趋势地图 |
| **【分】** | ✅ 完成 | 7个空白机会卡（G01-G07）+ 差异化重定位 |
| **【验】** | 🔄 进行中 | 假设已生成（H1/H0），MVE 方案已设计，待执行 |
| **【合】** | ⏳ 待启动 | 图表骨架 + 手稿待数据产出 |

---

## 关键里程碑

- [x] 2026-07-09：Morchella AI Scientist 系统初始化（14 Agent）
- [x] 2026-07-14：文献矩阵 12→31 篇 + Horticulturae 2024 对标发现
- [ ] 待定：Phase 1 MVE 先导实验（72-108组）
- [ ] 待定：AI 模型基线训练
- [ ] 2027-05：大创结题 + 首篇 SCI 投稿

---

## 关联资源

- 主项目：`C:\Users\26404\Desktop\Morchella_AI_Scientist`
- 文献矩阵：`literature/literature_matrix.md`
- 机会清单：`literature/opportunity_list.md`
- 路线图：`ROADMAP.md`
- 实验决策：`knowledge/Ideas/decision_volatile_platform.md`
