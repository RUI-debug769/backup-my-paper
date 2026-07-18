# Idea-01 MVE 方案 — 文献数据概念验证

> 📅 创建：2026-07-15 | 决策 D-06：文献数据先行验证
> 🎯 目标：用 2-3 周，零实验成本，判断核心假设是否值得投入 Tier-1 实验

---

## 一、MVE 策略

```
不采一滴样，不跑一针 GC-MS，用已发表文献中的数据验证：
  干燥动力学参数 → AI 模型 → 风味演化预测
  这个因果链是否成立？
```

**核心思路：** 提取 ≥2 篇数据密集型论文中的干燥曲线 + 挥发物数据 → 构建结构化数据集 → 训练基线 ML 模型 → 判定信号强度。

---

## 二、目标文献（数据提取源）

### 主数据源（优先提取）

| # | 文献 | 可提取数据 | 优先级 |
|---|------|-----------|--------|
| 1 | **Guo L et al. 2024** Horticulturae | 4个温度(40/50/60/70°C)的挥发物(GC-IMS) + 代谢物(LC-MS)数据；有原始图表可数字化 | 🔴 最高 |
| 2 | **The Effects of Different Postharvest Drying Temperatures on the Volatile Flavor Components and Non-Volatile Metabolites of Morchella sextelata** (2024) | 多温度挥发物 + 非挥发代谢物变化 | 🔴 最高 |

### 补充数据源（干燥动力学）

| # | 文献 | 可提取数据 | 优先级 |
|---|------|-----------|--------|
| 3 | Mathematical modeling of drying kinetics of Morchella esculenta | 干燥曲线(MR vs t)、Deff、活化能 | 🟡 |
| 4 | Drying kinetic and artificial neural network modeling of mushroom | 蘑菇干燥 ANN 建模方法参考 | 🟡 |
| 5 | Comparison of different drying processes of Morchella sextelata | 不同干燥方式对比数据 | 🟢 |

### 方法论参考（不提取数据）

| # | 文献 | 用途 |
|---|------|------|
| 6 | Schreurs M et al. 2024 Nat Commun | ML 预测风味的特征工程方法论 |
| 7 | Machine learning for food flavor prediction and regulation (Trends Food Sci) | 综述：食品风味 ML 最佳实践 |

---

## 三、数据提取计划

### Step 1：Figures → 数字化数据（2-3天）

```
工具：WebPlotDigitizer (免费) / plotdigitizer Python 库
目标：从论文图表中提取数值数据

提取内容（按论文）：
  Guo L 2024:
    ├── 干燥曲线：各温度下 MR vs t 曲线
    ├── 挥发物热图/柱状图：各温度+时间点的化合物丰度
    └── PCA/PLS-DA 得分图（可选）
  
  Drying Temperature Effects 2024:
    ├── 挥发物变化图（各温度比较）
    └── 代谢物差异图
```

### Step 2：结构化数据集（1-2天）

```
目标格式：每行 = 一个观测（特定温度+时间点）

列：
  [输入特征]                    [输出标签]
  temp | time | MR | aw* |       compound_1_abundance |
  Deff*| ...                     compound_2_abundance |
                                 ...                   |
                                 flavor_index*         |

* 可推导/估算的列；flavor_index = OAV 加权综合指标（若阈值数据可用）

预计数据量：
  最低：2篇 × 4温度 × 3时间点 = 24 个观测
  理想：2篇 × 4温度 × 5时间点 = 40 个观测
  → 对于 RF/XGBoost 基线够用（小样本 + 强正则化）
```

### Step 3：基线模型训练（2-3天）

```python
# 伪代码 — 实际在 Morchella_AI_Scientist 项目中执行

模型序列：
  DummyRegressor (随机基线) → LinearRegression → RF → XGBoost

评估策略（小样本适配）：
  - Leave-One-Out CV (LOOCV) 而非 k-fold
  - 或 Bootstrap resampling (n=1000)
  - 报告 R² mean ± std, RMSE mean ± std

特征重要性分析：
  - RF feature_importances_
  - SHAP summary plot
  - 验证：Top 特征是否与干燥理论一致？
    (预期：温度 > 时间 > 水分比 > 其他)
```

### Step 4：判定（1天）

| 结果 | R² 范围 | 判定 | 行动 |
|------|---------|------|------|
| 🟢 强信号 | > 0.70 | 假设初步成立 | 进入 Tier-1 实验验证 |
| 🟡 弱信号 | 0.40-0.70 | 有潜力但需更多/更好数据 | 扩大文献数据 or 启动小规模验证实验 |
| 🔴 无信号 | < 0.40 | 假设可能不成立 | 重新审视特征工程 or 降级为 Idea-01' |

---

## 四、执行时间线

```
Week 1 (7/15-7/22):
  Day 1-2: 精读 Guo L 2024 + Drying Temp Effects 2024，标记所有可提取图表
  Day 3-5: WebPlotDigitizer 数字化提取 → CSV
  Day 6-7: 数据清洗 + 特征工程

Week 2 (7/22-7/29):
  Day 8-10: 基线模型训练（Dummy → LR → RF → XGBoost）
  Day 11-12: LOOCV 交叉验证 + 超参数调优
  Day 13-14: SHAP 分析 + 结果可视化

Week 3 (7/29-8/5):
  Day 15-17: 撰写 MVE 报告（方法 + 结果 + 判定）
  Day 18-19: 基于结果更新研究假设
  Day 20-21: 决策节点：Go/No-Go Tier-1 实验
```

---

## 五、技术执行环境

| 组件 | 位置 |
|------|------|
| **代码** | `C:\Users\26404\Desktop\Morchella_AI_Scientist\experiments\mve_literature_validation\` |
| **提取数据** | `1/04_验/idea-01/数据/` (CSV 格式) |
| **分析 Notebook** | Jupyter notebook，与主项目一致 |
| **模型环境** | Python 3.x + scikit-learn + xgboost + shap |

---

## 六、风险与缓解

| 风险 | 概率 | 缓解 |
|------|------|------|
| 论文图表无法精确数字化 | 中 | 选 ≥2 篇互相验证；标记数字化不确定度 |
| 不同论文数据不可合并（实验条件差异大） | 中 | 先单篇分析 → 再尝试合并；加 study_id 作为随机效应 |
| 数据量太少（< 20 观测） | 中 | 用 LOOCV + Bootstrap；降低模型复杂度（RF max_depth 限制） |
| 挥发物单位不统一 | 高 | 统一转为相对丰度（% 或 Z-score）；不做绝对定量比较 |
| Guo L 2024 数据仅有静态终点 | 高 | 找补充论文提供时间序列；若无 → 退化为静态对比验证 |

---

## 七、交付物

MVE 完成后产出：

- [ ] `数据/` — 所有数字化提取的 CSV 文件（含提取来源标注）
- [ ] `mve_report.md` — MVE 结果报告（方法/结果/判定/下一步）
- [ ] `mve_analysis.ipynb` — 完整分析 Notebook（可复现）
- [ ] 更新 `核心假设.md` — 基于 MVE 结果修正假设
- [ ] 决策记录 → `../../00_项目管理/决策追踪.md`

---

## 八、Go/No-Go 标准

**Go (进入 Tier-1 实验) 条件：**
- R² > 0.60（干燥参数对风味有预测能力）
- 至少 ≥2 篇独立文献数据支持
- Top-3 重要特征与干燥理论一致
- Tier-1 实验方案已就绪（设备/预算/时间 OK）

**No-Go (降级 or 转向) 条件：**
- R² < 0.40 且无法通过特征工程改善
- 所有文献数据合并后仍无法建模
- 发现根本性逻辑漏洞（如干燥参数本身就不含风味信息）
