# 00_项目管理 — 项目总览

---

## 项目基本信息

| 字段 | 内容 |
|------|------|
| **项目名称** | 多尺度整合框架揭示羊肚菌干燥过程中蛋白质-风味相互作用：分子动力学模拟、多组学与机器学习的融合 |
| **英文名称** | A Multi-Scale Integrative Framework Revealing Protein-Flavor Interactions During Morchella Drying: Integrating MD Simulation, Multi-Omics, and Machine Learning |
| **项目类型** | 后续研究项目（大创 Paper 1 的延伸与深化） |
| **目标期刊** | **Nature Food** (IF ≈ 20-25, JCR Q1) |
| **时间定位** | 2027-2028（大创结题后启动） |
| **负责人** | 薛瑞 |
| **潜在合作导师** | 谢湖均教授（浙江工商大学）— MD 模拟/QSAR 专长 |

---

## 核心科学问题

> **干燥过程中羊肚菌蛋白质构象变化如何通过分子水平的非共价/共价相互作用调控风味挥发性化合物的保留与释放？**

---

## 四层整合框架

```
Layer 1: 分子动力学模拟 (MD)
  └── 原子尺度：蛋白质构象变化 + 风味结合自由能 + 关键残基

Layer 2: 多组学验证
  └── 分子尺度：荧光/CD/FTIR + GC-MS 顶空定量

Layer 3: 机器学习预测
  └── 数据尺度：GNN/Transformer → 结合亲和力高通量预测

Layer 4: 干燥工艺应用
  └── 宏观尺度：aw 临界阈值 → 风味定向保留策略
```

---

## 与 Paper 1 / Paper 2 的关系

```
Paper 1 (大创 2026-2027)     Paper 2 (纯计算 2026-2027)     Paper 3 (后续 2027-2028)
───────────────────────     ────────────────────────     ─────────────────────────
"什么条件风味好"              "为什么会变化？"               "如何预测与调控？"
Condition → Quality         Mechanism at atomic scale    Prediction & Control
ML 预测 + 代谢通路            MD 模拟 + MM/PBSA            MD + 多组学 + ML 闭环
Food Chemistry              Food Hydrocolloids           Nature Food
```

Paper 1 提供：关键风味化合物清单、最优干燥条件、OAV 数据
Paper 2 提供：结合自由能 + 关键残基 + 温度效应曲线
Paper 3 在此基础上：多尺度整合、ML 预测、干燥工艺优化

---

## 差异化创新点

| 维度 | 现状（2026） | 本研究 |
|------|------------|--------|
| **研究对象** | 食用菌蛋白-风味 MD：0 篇 | **首次** |
| **模拟条件** | 所有 MD 均在溶液中进行 | **首次模拟干燥动态过程** |
| **方法整合** | MD 或 ML 单独使用 | **MD + 多组学 + ML 三合一闭环** |
| **机制深度** | "什么化合物变化了" | **"为什么变、怎么变的"（原子层面）** |

---

## 关键文献基础

| # | 文献 | 对本研究的作用 |
|---|------|--------------|
| 1 | Jin & Wei (2024) — MD for food protein-ligand interactions | MD 方法论基础 |
| 2 | Trends Food Sci (2026) — Multi-scale aroma-food interactions | 多尺度整合框架 |
| 3 | Dai et al. (2025) — Protein-flavor interactions review | 蛋白-风味机制全景 |
| 4 | Guo L et al. (2024) — Morchella GC-IMS+LC-MS+RF | 羊肚菌基线数据 |
| 5 | Schreurs M et al. (2024) — ML beer flavor Nat Commun | 方法论标杆 |

---

## 关联资源

- 本子大纲：`Nature_Food_Proposal_Outline.docx`（本目录）
- 大创论文目录：`C:\Users\26404\Desktop\My Paper\1\`
- 主项目：`C:\Users\26404\Desktop\Morchella_AI_Scientist`
- 谢湖均论文：`C:\Users\26404\Desktop\research\XieHujun_AI_Food_Papers\`
