# Ivanova et al. 2020 — 精读笔记

> Bulgarian Chemical Communications, 52(A): 39-46, 2020 | DOI: 10.34049/bcc.52.A.186
> 🎯 **唯一专门研究羊肚菌干燥动力学的论文！**
> 精读日期：2026-07-15

---

## 一、论文概要

| 字段 | 内容 |
|------|------|
| **标题** | Mathematical modeling of drying kinetics of Morchella esculenta mushroom |
| **作者** | Ivanova M, Katrandzhiev N, Dospatliev L, Papazov P, Denev P |
| **机构** | Trakia University + University of Food Technologies (保加利亚) |
| **年份** | 2020 |
| **对象** | 🍄 **Morchella esculenta**（羊肚菌！直接相关！） |
| **IF** | ~0.3 (低分但数据直接可用) |

---

## 二、实验设计

```
物种：Morchella esculenta（保加利亚 Batak 山采集）
切片：2 mm 厚
初始含水量：89.41% (w.b.)
干燥方式：热风烘箱 (fan oven)

温度梯度：
  35°C → 170 min 完成
  45°C → 150 min 完成
  55°C → 120 min 完成

两段降速干燥：所有温度下均观察到两个降速阶段
```

---

## 三、核心数据 🔬

### 3.1 干燥曲线 (Figures 2, 3) — 可数字化

| 图表 | 内容 |
|------|------|
| **Fig 2** | 含水量 (MC) vs 干燥时间 — 3 条曲线 |
| **Fig 3** | 水分比 (MR) vs 干燥时间 — 3 条曲线 |

### 3.2 最佳拟合模型 (Table 3) — 直接可用

| 温度 | 最佳模型 | R² | 模型方程 |
|------|---------|-----|---------|
| 35°C | **Logarithmic** | **0.9970** | MR = 1.2083·exp(-0.0099t) - 0.2256 |
| 45°C | **Midilli et al.** | **0.9920** | MR = 1.0085·exp(-0.0422·t^0.8229) - 0.0004t |
| 55°C | **Lewis** | **0.9868** | MR = exp(-0.03434·t) |
| 统一 | **Midilli et al.** | ≥0.987 | 三温度通用 |

### 3.3 有效水分扩散系数 Deff (Table 4) — 🔑 直接可用！

| 温度 | Deff₁ (第一阶段) ×10⁻⁹ m²/s | Deff₂ (第二阶段) ×10⁻⁹ m²/s |
|------|------|------|
| 35°C | **6.17** | **16.11** |
| 45°C | **8.72** | **18.01** |
| 55°C | **12.98** | **24.63** |

### 3.4 活化能 Ea

| 阶段 | Ea (kJ/mol) |
|------|------------|
| 第一阶段 | **31.26** |
| 第二阶段 | **17.75** |

---

## 四、MVE 数据提取评估

### 可直接使用的数值（无需数字化）

| 参数 | 35°C | 45°C | 55°C | 用途 |
|------|------|------|------|------|
| 干燥时间 (min) | 170 | 150 | 120 | 输入特征 |
| Deff₁ (×10⁻⁹) | 6.17 | 8.72 | 12.98 | 输入特征 |
| Deff₂ (×10⁻⁹) | 16.11 | 18.01 | 24.63 | 输入特征 |
| Ea₁ (kJ/mol) | — | — | 31.26 | 全局特征 |
| Ea₂ (kJ/mol) | — | — | 17.75 | 全局特征 |
| 模型 R² | 0.9970 | 0.9920 | 0.9868 | 数据质量指标 |

### 需数字化的图表

| 图表 | 数据量 | 难度 |
|------|--------|------|
| Fig 2 (MC vs t) | ~30 点 × 3 温度 | 🟢 容易 |
| Fig 3 (MR vs t) | ~30 点 × 3 温度 | 🟢 容易 |
| Fig 7 (Deff vs T) | 6 点 | 🟢 容易 |

---

## 五、三篇论文整合方案

```
Ivanova 2020 ──→ 干燥动力学参数
(BCC 2020)       Deff, Ea, MR(t), 模型方程
                 对象：Morchella esculenta ✅
                 
       + 
       
Liu 2024 ──────→ 挥发物 + 代谢物终点数据
(Horticulturae)  3 温度 (45/55/65°C), GC-IMS + LC-MS/MS
                 对象：Morchella sextelata ✅
                 
       +
       
Guo 2025 ──────→ LSTM 时序方法 + 超参数
(CEA, IF 8.3)    R²>0.99 干燥速率预测
                 实时干燥参数控制逻辑
                 对象：P. eryngii (方法可迁移)
```

### MVE 数据集构建

```
输入特征 (来自 Ivanova 2020):
  temp | DryingTime | Deff₁ | Deff₂ | Ea₁ | Ea₂

输出标签 (来自 Liu 2024):
  1-hexanol_abundance | hexanal_abundance | 
  valeraldehyde_abundance | acetic_acid_abundance | ...

模型方法 (来自 Guo 2025):
  LSTM 架构 | TBPTT | Adam(lr=0.01) | hidden_dim=4
```

### ⚠️ 关键限制：温度不完全对应

| 论文 | 温度 |
|------|------|
| Ivanova 2020 | 35, 45, 55°C |
| Liu 2024 | 45, 55, 65°C |

**重叠温度：45°C 和 55°C** — 这两个温度点可以直接关联！

---

## 六、MVE 数据优先级

| 优先级 | 行动 | 预计产出 |
|--------|------|---------|
| 🥇 | 数字化 Ivanova Fig 3 (MR vs t) | MR 时间序列 CSV |
| 🥇 | 数字化 Liu 2024 Fig 4 (挥发物柱状图) | 挥发物丰度 CSV |
| 🥈 | 构建 45°C+55°C 关联数据集 | 输入→输出映射 |
| 🥈 | 复现 Guo 2025 LSTM 模型 | Python 代码 |
| 🥉 | 下载 Liu 2024 Table S1 | 完整代谢物矩阵 |
