#!/usr/bin/env python3
"""
MVE v2 — 升级版 ML 建模
========================
方法:
  1. GPR (Gaussian Process Regression) — 小样本最优
  2. Bayesian Ridge — 不确定性量化
  3. ElasticNet — 正则化基线
  4. RF + XGBoost — 原 v1 基线
  5. 分类框架 — up/down/ns 三分类预测
  6. 效应量 — Cohen's d + Cliff's delta

验证:
  - LOOCV (Leave-One-Out)
  - Bootstrap CI (n=2000)
  - 排列检验 (n=1000)
  - 跨论文交叉验证 (Liu vs Liao)
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import numpy as np
import pandas as pd
from pathlib import Path
from scipy import stats
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.linear_model import BayesianRidge, ElasticNet
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, WhiteKernel, ConstantKernel
from sklearn.model_selection import LeaveOneOut, cross_val_score, cross_val_predict
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import r2_score, accuracy_score, f1_score, mean_squared_error, classification_report
import warnings
warnings.filterwarnings('ignore')

OUT_DIR = Path(__file__).parent
RNG = np.random.RandomState(42)

# ============================================================
# 1. 加载数据
# ============================================================
df = pd.read_csv(OUT_DIR / "mve_v2_dataset.csv")
print(f"MVE v2 数据集: {len(df)} 行, {df['compound'].nunique()} 化合物")
print(f"数据源: {df['source'].value_counts().to_dict()}")
print(f"类别分布: {df['category'].value_counts().to_dict()}")

# ============================================================
# 2. 特征工程
# ============================================================
# v2 修正: 只用真正的输入特征，避免数据泄漏
# 类别 one-hot 是标签结构信息，不应作为输入特征
# 只用: 温度、干燥类型编码 (物理层面可测量)
FEATURES_BASE = ['temp_C']

# 仅添加干燥类型和来源作为简单编码 (非化合物特异性)
df_feat = df.copy()
df_feat['is_hot_air'] = (df_feat['drying_type'] == 'hot_air').astype(int)
df_feat['is_freeze'] = (df_feat['drying_type'] == 'freeze').astype(int)
df_feat['is_natural'] = (df_feat['drying_type'] == 'natural').astype(int)
df_feat['is_combined'] = (df_feat['drying_type'] == 'combined').astype(int)
df_feat['is_fresh'] = (df_feat['drying_type'] == 'none').astype(int)
df_feat['source_is_liao'] = (df_feat['source'] == 'Liao2025').astype(int)

FEATURE_NAMES = FEATURES_BASE + ['is_hot_air', 'is_freeze', 'is_natural',
                                   'is_combined', 'is_fresh', 'source_is_liao']

X_df = df_feat[FEATURE_NAMES]

X = X_df.values.astype(float)
y_reg = df['abundance_norm'].values.astype(float)

# 分类标签: 基于 Liu 2024 的 trend_direction
# 对于 Liao 2025 数据，根据干燥方法 vs 新鲜推断趋势
def infer_trend(row):
    if row['trend_direction'] in ['up', 'down', 'ns']:
        return row['trend_direction']
    # Liao 2025: 推断趋势 (HAD vs FS)
    if row['source'] == 'Liao2025':
        if row['drying_type'] == 'none':
            return 'baseline'
        if row['abundance_norm'] > 0.1:
            return 'up'  # 干燥后出现 → 上调
        return 'ns'
    return 'unknown'

df['trend_inferred'] = df.apply(infer_trend, axis=1)
df_cls = df[df['trend_inferred'].isin(['up', 'down', 'ns'])]
y_cls = df_cls['trend_inferred'].values

df_cls_feat = df_cls.copy()
df_cls_feat['is_hot_air'] = (df_cls_feat['drying_type'] == 'hot_air').astype(int)
df_cls_feat['is_freeze'] = (df_cls_feat['drying_type'] == 'freeze').astype(int)
df_cls_feat['is_natural'] = (df_cls_feat['drying_type'] == 'natural').astype(int)
df_cls_feat['is_combined'] = (df_cls_feat['drying_type'] == 'combined').astype(int)
df_cls_feat['is_fresh'] = (df_cls_feat['drying_type'] == 'none').astype(int)
df_cls_feat['source_is_liao'] = (df_cls_feat['source'] == 'Liao2025').astype(int)

X_cls = df_cls_feat[FEATURE_NAMES].values.astype(float)

print(f"\n分类任务: {len(df_cls)} 样本, 类别分布: {dict(zip(*np.unique(y_cls, return_counts=True)))}")

# ============================================================
# 3. 回归模型对比
# ============================================================
print("\n" + "=" * 70)
print("3. 回归模型对比 (LOOCV)")
print("=" * 70)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

models_reg = {
    'Dummy (mean)':   ('baseline', None),
    'ElasticNet':     ('linear', ElasticNet(alpha=0.1, l1_ratio=0.5, max_iter=5000, random_state=42)),
    'BayesianRidge':  ('bayesian', BayesianRidge()),
    'GPR (RBF)':      ('gp', GaussianProcessRegressor(
        kernel=ConstantKernel() * RBF() + WhiteKernel(),
        normalize_y=True, random_state=42)),
    'RandomForest':   ('tree', RandomForestRegressor(n_estimators=200, max_depth=4, min_samples_leaf=3, random_state=42)),
}

try:
    import xgboost as xgb
    models_reg['XGBoost'] = ('tree', xgb.XGBRegressor(n_estimators=100, max_depth=3, learning_rate=0.1, random_state=42, verbosity=0))
except ImportError:
    pass

results_reg = []
for name, (mtype, model) in models_reg.items():
    if mtype == 'baseline':
        dummy_pred = np.full_like(y_reg, y_reg.mean())
        r2 = r2_score(y_reg, dummy_pred)
        rmse = np.sqrt(mean_squared_error(y_reg, dummy_pred))
        results_reg.append({'model': name, 'r2': r2, 'rmse': rmse, 'type': 'baseline'})
        print(f"  {name:20s} R²={r2:.4f}")
        continue

    # LOOCV
    loo = LeaveOneOut()
    y_pred = cross_val_predict(model, X_scaled, y_reg, cv=loo)
    r2 = r2_score(y_reg, y_pred)
    rmse = np.sqrt(mean_squared_error(y_reg, y_pred))

    # Bootstrap CI
    n_boot = 1000
    boot_r2 = []
    for _ in range(n_boot):
        idx = RNG.choice(len(y_reg), size=len(y_reg), replace=True)
        boot_r2.append(r2_score(y_reg[idx], y_pred[idx]))
    r2_ci_low = np.percentile(boot_r2, 2.5)
    r2_ci_high = np.percentile(boot_r2, 97.5)

    results_reg.append({
        'model': name, 'r2': round(r2, 4), 'rmse': round(rmse, 4),
        'r2_ci_low': round(r2_ci_low, 4), 'r2_ci_high': round(r2_ci_high, 4),
        'type': mtype
    })
    print(f"  {name:20s} R²={r2:.4f} [{r2_ci_low:.4f}, {r2_ci_high:.4f}], RMSE={rmse:.4f}")

# ============================================================
# 4. 分类模型 — 预测趋势方向
# ============================================================
print("\n" + "=" * 70)
print("4. 分类模型 — 预测 up/down/ns 趋势")
print("=" * 70)

X_cls_scaled = StandardScaler().fit_transform(X_cls)
le = LabelEncoder()
y_cls_enc = le.fit_transform(y_cls)

models_cls = {
    'RF Classifier': RandomForestClassifier(n_estimators=200, max_depth=4, random_state=42),
}

try:
    models_cls['XGBoost Classifier'] = xgb.XGBClassifier(n_estimators=100, max_depth=3, learning_rate=0.1, random_state=42, verbosity=0)
except:
    pass

for name, model in models_cls.items():
    loo = LeaveOneOut()
    y_pred = cross_val_predict(model, X_cls_scaled, y_cls_enc, cv=loo)
    acc = accuracy_score(y_cls_enc, y_pred)
    f1 = f1_score(y_cls_enc, y_pred, average='weighted')

    # 多数类基线
    majority_acc = max(np.bincount(y_cls_enc)) / len(y_cls_enc)

    print(f"  {name:25s} Accuracy={acc:.3f} (基线={majority_acc:.3f}), F1={f1:.3f}")
    print(f"    分类报告:\n{classification_report(y_cls_enc, y_pred, target_names=le.classes_, zero_division=0)}")

# ============================================================
# 5. 效应量分析
# ============================================================
print("=" * 70)
print("5. 效应量分析")
print("=" * 70)

def cohens_d(x, y):
    """Cohen's d 效应量"""
    nx, ny = len(x), len(y)
    dof = nx + ny - 2
    pooled_std = np.sqrt(((nx - 1) * np.var(x, ddof=1) + (ny - 1) * np.var(y, ddof=1)) / dof)
    if pooled_std < 1e-10:
        return 0.0
    return (np.mean(x) - np.mean(y)) / pooled_std

def cliffs_delta(x, y):
    """Cliff's delta — 非参数效应量 (对非正态分布鲁棒)"""
    nx, ny = len(x), len(y)
    greater = 0
    for xi in x:
        for yi in y:
            if xi > yi: greater += 1
            elif xi < yi: greater -= 1
    return greater / (nx * ny)

# 按温度分组 (Liu 2024 数据)
liu_data = df[df['source'] == 'Liu2024_v1']
for feat in ['abundance_norm', 'log_abundance']:
    print(f"\n  {feat} 效应量 (Liu 2024, 45°C vs 55°C):")
    lt = liu_data[liu_data['temp_C'] == 45][feat].values
    mt = liu_data[liu_data['temp_C'] == 55][feat].values
    if len(lt) > 0 and len(mt) > 0:
        d = cohens_d(mt, lt)
        cd = cliffs_delta(mt, lt)
        # 排列检验
        combined = np.concatenate([lt, mt])
        obs_diff = np.abs(np.mean(mt) - np.mean(lt))
        perm_diffs = []
        for _ in range(2000):
            RNG.shuffle(combined)
            perm_diffs.append(np.abs(np.mean(combined[:len(mt)]) - np.mean(combined[len(mt):])))
        p_perm = np.mean(np.array(perm_diffs) >= obs_diff)
        print(f"    Cohen's d = {d:+.3f}, Cliff's delta = {cd:+.3f}, 排列p = {p_perm:.4f}")
        print(f"    |d|>0.8(大): {'是' if abs(d)>0.8 else '否'}, "
              f"|d|>0.5(中): {'是' if abs(d)>0.5 else '否'}")

# 按类别分析效应量
print(f"\n  分类别 Cohen's d (Liu 2024, 45°C→55°C, abundance_norm):")
for cat in liu_data['category'].unique():
    cat_data = liu_data[liu_data['category'] == cat]
    lt = cat_data[cat_data['temp_C'] == 45]['abundance_norm'].values
    mt = cat_data[cat_data['temp_C'] == 55]['abundance_norm'].values
    if len(lt) > 0 and len(mt) > 0:
        d = cohens_d(mt, lt)
        cd = cliffs_delta(mt, lt)
        print(f"    {cat:15s} d={d:+.3f}, Cliff's δ={cd:+.3f}, n_lt={len(lt)}, n_mt={len(mt)}")

# ============================================================
# 6. 跨论文验证: Liu 2024 vs Liao 2025
# ============================================================
print("\n" + "=" * 70)
print("6. 跨论文交叉验证")
print("=" * 70)

# 重叠化合物
liu_compounds = set(df[df['source']=='Liu2024_v1']['compound'])
liao_compounds = set(df[df['source']=='Liao2025']['compound'])
overlap = liu_compounds & liao_compounds
print(f"  Liu 2024: {len(liu_compounds)} 化合物")
print(f"  Liao 2025: {len(liao_compounds)} 化合物")
print(f"  重叠: {len(overlap)} 种: {overlap}")

# 类别级趋势一致性
liu_cat_trends = {}
for cat in df[df['source']=='Liu2024_v1']['category'].unique():
    cat_data = df[(df['source']=='Liu2024_v1') & (df['category']==cat)]
    lt_mean = cat_data[cat_data['temp_C']==45]['abundance_norm'].mean()
    mt_mean = cat_data[cat_data['temp_C']==55]['abundance_norm'].mean()
    liu_cat_trends[cat] = 'up' if mt_mean > lt_mean else 'down'

liao_cat_trends = {}
for cat in df[df['source']=='Liao2025']['category'].unique():
    cat_data = df[(df['source']=='Liao2025') & (df['category']==cat)]
    fresh = cat_data[cat_data['drying_type']=='none']['abundance_norm'].mean()
    had = cat_data[cat_data['drying_type']=='hot_air']['abundance_norm'].mean()
    if fresh == 0 and had > 0:
        liao_cat_trends[cat] = 'up'
    elif had == 0 and fresh > 0:
        liao_cat_trends[cat] = 'down'
    else:
        liao_cat_trends[cat] = 'ns'

common_cats = set(liu_cat_trends.keys()) & set(liao_cat_trends.keys())
consistent = sum(1 for c in common_cats if liu_cat_trends[c] == liao_cat_trends[c])
print(f"\n  类别趋势一致性: {consistent}/{len(common_cats)} ({100*consistent/max(len(common_cats),1):.0f}%)")
for c in sorted(common_cats):
    match = '✓' if liu_cat_trends[c] == liao_cat_trends[c] else '✗'
    print(f"    {match} {c:15s}  Liu={liu_cat_trends[c]:4s}  Liao={liao_cat_trends[c]:4s}")

# ============================================================
# 7. MVE v2 综合判定
# ============================================================
print("\n" + "=" * 70)
print("7. MVE v2 综合判定")
print("=" * 70)

best_reg = max(results_reg, key=lambda r: r['r2'] if r['type'] != 'baseline' else -999)
has_overlap = len(overlap) > 0
trend_consistency = consistent / max(len(common_cats), 1) if common_cats else 0
max_d = max(abs(cohens_d(
    liu_data[liu_data['temp_C']==55]['abundance_norm'].values,
    liu_data[liu_data['temp_C']==45]['abundance_norm'].values
)), 0.1)

signals = {
    'best_reg_r2': best_reg['r2'],
    'best_model': best_reg['model'],
    'overlap_compounds': len(overlap),
    'trend_consistency': round(trend_consistency, 2),
    'cohens_d_45vs55': round(max_d, 3),
    'compound_coverage': df['compound'].nunique(),
    'n_sources': df['source'].nunique(),
    'class_accuracy_vs_baseline': 0,  # will be filled
}

# 综合评分 (0-100)
score = 0
score += 25 if signals['best_reg_r2'] > 0.3 else (15 if signals['best_reg_r2'] > 0.1 else 5)
score += 25 if abs(signals['cohens_d_45vs55']) > 0.8 else (15 if abs(signals['cohens_d_45vs55']) > 0.5 else 5)
score += 25 if signals['trend_consistency'] > 0.7 else (15 if signals['trend_consistency'] > 0.5 else 5)
score += 15 if signals['compound_coverage'] > 40 else (10 if signals['compound_coverage'] > 23 else 5)
score += 10 if signals['n_sources'] >= 3 else (7 if signals['n_sources'] >= 2 else 3)

if score >= 80:
    verdict = "🟢 GO — 强烈建议进入 Tier-1 实验"
elif score >= 60:
    verdict = "🟡 CONDITIONAL GO — 建议 Tier-1，需关注弱信号维度"
elif score >= 40:
    verdict = "🟠 WEAK GO — 有信号但需加强数据后重评估"
else:
    verdict = "🔴 NO GO — 建议重新审视核心假设"

print(f"""
┌─────────────────────────────────────────────────────────────┐
│                    MVE v2 最终判定                            │
├─────────────────────────────────────────────────────────────┤
│  回归最佳 R²:       {signals['best_reg_r2']:.4f} ({signals['best_model']})          │
│  效应量 |d|:        {signals['cohens_d_45vs55']:.3f}                              │
│  跨论文趋势一致性:   {signals['trend_consistency']:.0%}                              │
│  化合物覆盖:         {signals['compound_coverage']} 种 (v1: 23)                       │
│  数据源:             {signals['n_sources']} 篇独立论文                              │
│  重叠化合物:         {signals['overlap_compounds']} 种                              │
├─────────────────────────────────────────────────────────────┤
│  综合评分:           {score}/100                                │
│  判定: {verdict}                    │
├─────────────────────────────────────────────────────────────┤
│  ⚠️ 根本限制: 仅 2 个重叠温度点 (文献数据固有局限)          │
│  Tier-1 实验: ≥4 温度 × ≥5 时间点 × 3 重复 才能突破          │
└─────────────────────────────────────────────────────────────┘
""")

# ============================================================
# 8. 保存结果
# ============================================================
results_df = pd.DataFrame(results_reg)
results_path = OUT_DIR / "mve_v2_regression_results.csv"
results_df.to_csv(results_path, index=False, encoding='utf-8-sig')
print(f"[OK] 回归结果: {results_path}")

summary_path = OUT_DIR / "mve_v2_summary.json"
import json
summary = {**signals, 'score': score, 'verdict': verdict}
summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding='utf-8')
print(f"[OK] 判定摘要: {summary_path}")

print("\n[DONE] MVE v2 建模分析完成")
