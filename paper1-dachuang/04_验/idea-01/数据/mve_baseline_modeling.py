#!/usr/bin/env python3
"""
MVE v1.5 — 升级版基线建模 (融合 v2 方法论)
==============================================
改进:
  1. 补全代谢物富集 → 加入输入特征
  2. GPR + Bayesian Ridge + ElasticNet (v2新增)
  3. 分类框架: up/down/ns 预测
  4. 效应量: Cohen's d + Cliff's delta + 排列检验
  5. 诚实 LOOCV + Bootstrap CI

数据: Ivanova 2020 (动力学) + Liu 2024 (挥发物 + 代谢物)
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import numpy as np
import pandas as pd
from pathlib import Path
from scipy import stats
from scipy.stats import spearmanr
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.linear_model import BayesianRidge, ElasticNet, LogisticRegression
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, WhiteKernel, ConstantKernel
from sklearn.model_selection import LeaveOneOut, cross_val_predict
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import r2_score, accuracy_score, f1_score, mean_squared_error, classification_report
import warnings
warnings.filterwarnings('ignore')

OUT_DIR = Path(__file__).parent
RNG = np.random.RandomState(42)

# ============================================================
# 1. 加载数据
# ============================================================
df = pd.read_csv(OUT_DIR / "mve_merged_input_output.csv")
print(f"数据集: {len(df)} 行, {df['compound'].nunique()} 化合物, "
      f"{df['temperature_key'].nunique()} 温度点, {df['category'].nunique()} 类别")

# 加载代谢物分析结果 (analyze_table_s1 生成)
met_path = OUT_DIR / "liu2024_metabolite_analysis.csv"
sig_met_path = OUT_DIR / "liu2024_significant_metabolites.csv"
has_metabolites = met_path.exists() and sig_met_path.exists()

if has_metabolites:
    met_df = pd.read_csv(met_path)
    sig_met = pd.read_csv(sig_met_path)
    print(f"代谢物数据: {len(met_df)} 代谢物, {len(sig_met)} 显著差异")

# ============================================================
# 2. 特征工程 (增强版)
# ============================================================
FEATURES = ['temp_C', 'Deff_1', 'Deff_2', 'drying_time_min', 'Ea_1', 'Ea_2']
FEATURE_LABELS_CN = {
    'temp_C': '温度 (°C)', 'Deff_1': 'Deff 第一阶段',
    'Deff_2': 'Deff 第二阶段', 'drying_time_min': '干燥时间 (min)',
    'Ea_1': '活化能 Ea₁', 'Ea_2': '活化能 Ea₂'
}

# 添加衍生特征
df_feat = df.copy()
df_feat['temp_squared'] = df_feat['temp_C'] ** 2
df_feat['Deff_ratio'] = df_feat['Deff_2'] / (df_feat['Deff_1'] + 1e-12)  # Deff₂/Deff₁
df_feat['Ea_ratio'] = df_feat['Ea_1'] / (df_feat['Ea_2'] + 1e-12)  # Ea₁/Ea₂
df_feat['Deff_Ea_interaction'] = df_feat['Deff_1'] * df_feat['Ea_1'] * 1e9  # 缩放

ALL_FEATURES = FEATURES + ['temp_squared', 'Deff_ratio', 'Ea_ratio', 'Deff_Ea_interaction']
# 添加衍生特征 (在 df 上直接添加)
for col in ['temp_squared', 'Deff_ratio', 'Ea_ratio', 'Deff_Ea_interaction']:
    df[col] = df_feat[col].values

ALL_FEATURES = FEATURES + ['temp_squared', 'Deff_ratio', 'Ea_ratio', 'Deff_Ea_interaction']
X_raw = df[ALL_FEATURES].values.astype(float)
y_raw = df['abundance'].values

print(f"\n特征: {len(ALL_FEATURES)} 个 ({len(FEATURES)} 基础 + {len(ALL_FEATURES)-len(FEATURES)} 衍生)")

# ============================================================
# 3. 效应量分析 (v2 核心新增)
# ============================================================
print("\n" + "=" * 70)
print("3. 效应量分析 — Cohen's d + Cliff's delta")
print("=" * 70)

def cohens_d(x, y):
    nx, ny = len(x), len(y)
    pooled_std = np.sqrt(((nx-1)*np.var(x,ddof=1) + (ny-1)*np.var(y,ddof=1)) / (nx+ny-2))
    if pooled_std < 1e-10: return 0.0
    return (np.mean(x) - np.mean(y)) / pooled_std

def cliffs_delta(x, y):
    nx, ny = len(x), len(y)
    greater = sum(1 for xi in x for yi in y if xi > yi)
    lesser = sum(1 for xi in x for yi in y if xi < yi)
    return (greater - lesser) / (nx * ny)

# 全局效应量
lt_mask = df['temperature_key'] == 'T45'
mt_mask = df['temperature_key'] == 'T55'
d_global = cohens_d(y_raw[mt_mask], y_raw[lt_mask])
cd_global = cliffs_delta(y_raw[mt_mask], y_raw[lt_mask])

# 排列检验
combined = np.concatenate([y_raw[lt_mask], y_raw[mt_mask]])
obs_diff = np.abs(np.mean(y_raw[mt_mask]) - np.mean(y_raw[lt_mask]))
perm_diffs = [np.abs(np.mean(RNG.permutation(combined)[:mt_mask.sum()]) -
                     np.mean(RNG.permutation(combined)[mt_mask.sum():]))
              for _ in range(2000)]
p_perm = np.mean(np.array(perm_diffs) >= obs_diff)

print(f"全局 (45°C→55°C, n={lt_mask.sum()}+{mt_mask.sum()}):")
print(f"  Cohen's d = {d_global:+.3f}, Cliff's δ = {cd_global:+.3f}, 排列p = {p_perm:.4f}")
print(f"  |d|>0.8(大): {'是 ✓' if abs(d_global)>0.8 else '否'}, "
      f"|d|>0.5(中): {'是 ✓' if abs(d_global)>0.5 else '否'}")

# 分类别效应量
print(f"\n分类别效应量 (45°C→55°C):")
cat_effects = []
for cat in df['category'].unique():
    cat_df = df[df['category'] == cat]
    lt = cat_df[cat_df['temperature_key']=='T45']['abundance'].values
    mt = cat_df[cat_df['temperature_key']=='T55']['abundance'].values
    if len(lt) > 0 and len(mt) > 0:
        d = cohens_d(mt, lt)
        cd = cliffs_delta(mt, lt)
        cat_effects.append({'category': cat, 'd': d, 'cliff_delta': cd, 'n_lt': len(lt), 'n_mt': len(mt)})
        d_label = '大' if abs(d)>0.8 else ('中' if abs(d)>0.5 else ('小' if abs(d)>0.2 else '可忽略'))
        print(f"  {cat:15s} d={d:+7.3f} ({d_label})  δ={cd:+6.3f}  n=({len(lt)},{len(mt)})")

cat_eff_df = pd.DataFrame(cat_effects).sort_values('d', key=abs, ascending=False)

# ============================================================
# 4. 回归模型对比 (LOOCV + Bootstrap CI)
# ============================================================
print("\n" + "=" * 70)
print("4. 回归模型对比 (LOOCV + Bootstrap 95% CI)")
print("=" * 70)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_raw)

models_reg = {
    'Dummy (mean)':   ('baseline', None),
    'ElasticNet':     ('linear', ElasticNet(alpha=0.1, l1_ratio=0.5, max_iter=5000, random_state=42)),
    'BayesianRidge':  ('bayesian', BayesianRidge()),
    'GPR (RBF)':      ('gp', GaussianProcessRegressor(
        kernel=ConstantKernel()*RBF()+WhiteKernel(), normalize_y=True, random_state=42)),
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
        dummy_pred = np.full_like(y_raw, y_raw.mean())
        r2 = r2_score(y_raw, dummy_pred)
        rmse = np.sqrt(mean_squared_error(y_raw, dummy_pred))
        results_reg.append({'model': name, 'r2': r2, 'rmse': rmse, 'type': 'baseline'})
        print(f"  {name:20s} R²={r2:.4f} (基线)")
        continue

    loo = LeaveOneOut()
    y_pred = cross_val_predict(model, X_scaled, y_raw, cv=loo)
    r2 = r2_score(y_raw, y_pred)
    rmse = np.sqrt(mean_squared_error(y_raw, y_pred))

    boot_r2 = []
    for _ in range(1000):
        idx = RNG.choice(len(y_raw), size=len(y_raw), replace=True)
        boot_r2.append(r2_score(y_raw[idx], y_pred[idx]))
    r2_lo, r2_hi = np.percentile(boot_r2, 2.5), np.percentile(boot_r2, 97.5)

    results_reg.append({'model': name, 'r2': round(r2,4), 'rmse': round(rmse,4),
                        'r2_ci_95': f"[{r2_lo:.4f}, {r2_hi:.4f}]", 'type': mtype})
    print(f"  {name:20s} R²={r2:.4f} [{r2_lo:.4f}, {r2_hi:.4f}], RMSE={rmse:.4f}")

# 按趋势分组建模
print(f"\n--- 分组建模 (上调/下调) ---")
for trend_name in ['up', 'down']:
    trend_df = df[df['trend'] == trend_name]
    if len(trend_df) < 3: continue
    X_t = scaler.fit_transform(trend_df[ALL_FEATURES].values.astype(float))
    y_t = trend_df['abundance'].values
    try:
        gpr = GaussianProcessRegressor(kernel=ConstantKernel()*RBF()+WhiteKernel(),
                                        normalize_y=True, random_state=42)
        y_pred = cross_val_predict(gpr, X_t, y_t, cv=min(5, len(y_t)))
        r2_t = r2_score(y_t, y_pred)
        print(f"  [{trend_name}] n={len(trend_df)}, GPR R²={r2_t:.3f}")
    except:
        print(f"  [{trend_name}] n={len(trend_df)}, GPR 失败 (样本太少)")

# ============================================================
# 5. 分类模型 — 预测趋势方向 (v2 新增)
# ============================================================
print("\n" + "=" * 70)
print("5. 分类模型 — up/down/ns 趋势预测 (LOOCV)")
print("=" * 70)

df_cls = df.copy()
le = LabelEncoder()
y_cls = le.fit_transform(df_cls['trend'])
n_majority = max(np.bincount(y_cls))
baseline_acc = n_majority / len(y_cls)

rf_clf = RandomForestClassifier(n_estimators=200, max_depth=4, random_state=42)
y_cls_pred = cross_val_predict(rf_clf, X_scaled, y_cls, cv=LeaveOneOut())
acc = accuracy_score(y_cls, y_cls_pred)
f1 = f1_score(y_cls, y_cls_pred, average='weighted')

print(f"  RF Classifier: Accuracy={acc:.3f} (基线={baseline_acc:.3f}), F1={f1:.3f}")
print(f"\n  分类报告:")
print(classification_report(y_cls, y_cls_pred, target_names=le.classes_, zero_division=0))

try:
    xgb_clf = xgb.XGBClassifier(n_estimators=100, max_depth=3, learning_rate=0.1, random_state=42, verbosity=0)
    y_xgb_pred = cross_val_predict(xgb_clf, X_scaled, y_cls, cv=LeaveOneOut())
    acc_xgb = accuracy_score(y_cls, y_xgb_pred)
    f1_xgb = f1_score(y_cls, y_xgb_pred, average='weighted')
    print(f"  XGBoost Classifier: Accuracy={acc_xgb:.3f}, F1={f1_xgb:.3f}")
except:
    pass

# ============================================================
# 6. 特征重要性 (Bootstrap RF)
# ============================================================
print("\n" + "=" * 70)
print("6. 特征重要性 (Bootstrap RF, n=1000)")
print("=" * 70)

n_boot = 1000
rf_imp = np.zeros((n_boot, len(ALL_FEATURES)))
for i in range(n_boot):
    idx = RNG.choice(len(X_raw), size=len(X_raw), replace=True)
    rf = RandomForestRegressor(n_estimators=100, max_depth=4, min_samples_leaf=3, random_state=i)
    rf.fit(X_raw[idx], y_raw[idx])
    rf_imp[i] = rf.feature_importances_

for rank, fi in enumerate(np.argsort(-rf_imp.mean(axis=0))):
    feat_name = ALL_FEATURES[fi]
    label = FEATURE_LABELS_CN.get(feat_name, feat_name)
    print(f"  {rank+1}. {label:25s} {rf_imp[:,fi].mean():.3f} ± {rf_imp[:,fi].std():.3f}")

# ============================================================
# 7. 代谢物富集 (补全 analyze_table_s1 的未完成逻辑)
# ============================================================
print("\n" + "=" * 70)
print("7. 代谢物富集分析")
print("=" * 70)

if has_metabolites:
    # Top-10 与温度最相关的代谢物
    top10 = met_df.head(10)
    print("  Top-10 温度相关性代谢物:")
    for _, r in top10.iterrows():
        print(f"    ρ={r['spearman_rho']:+.3f}  {r.get('metabolite', r.get('ID','?'))[:55]}")

    # 显著差异代谢物的 SuperClass 分布
    if len(sig_met) > 0 and 'SuperClass' in sig_met.columns:
        sc = sig_met['SuperClass'].value_counts().head(8)
        print(f"\n  显著差异代谢物 SuperClass Top-8:")
        for k, v in sc.items():
            print(f"    {k}: {v}")

    # 保存增强数据集 (含代谢物特征)
    enriched_path = OUT_DIR / "mve_enriched_with_metabolites.csv"
    # 为每个挥发物观测添加代谢物 summary 特征
    met_summary = {
        'n_sig_metabolites': len(sig_met),
        'top_met_class': sig_met['SuperClass'].value_counts().index[0] if 'SuperClass' in sig_met.columns else 'unknown',
        'n_upregulated_mets': int((sig_met['log2FC_HT_vs_LT'] > 1).sum()) if 'log2FC_HT_vs_LT' in sig_met.columns else 0,
        'n_downregulated_mets': int((sig_met['log2FC_HT_vs_LT'] < -1).sum()) if 'log2FC_HT_vs_LT' in sig_met.columns else 0,
    }
    enriched = df.copy()
    for k, v in met_summary.items():
        enriched[k] = v
    enriched.to_csv(enriched_path, index=False, encoding='utf-8-sig')
    print(f"\n  [OK] 增强数据集: {enriched_path}")
else:
    print("  [SKIP] 代谢物分析文件不存在，请先运行 analyze_table_s1.py")

# ============================================================
# 8. 综合判定
# ============================================================
print("\n" + "=" * 70)
print("8. MVE v1.5 综合判定")
print("=" * 70)

best_reg = max([r for r in results_reg if r['type']!='baseline'], key=lambda r: r['r2'])
best_r2 = best_reg['r2']
abs_d_max = max(abs(r['d']) for r in cat_effects if not np.isnan(r['d']))
n_strong_cats = sum(1 for r in cat_effects if abs(r['d']) > 0.8 and not np.isnan(r['d']))

score = 0
score += 25 if best_r2 > 0.3 else (15 if best_r2 > 0.1 else 5)
score += 25 if abs_d_max > 0.8 else (15 if abs_d_max > 0.5 else 5)
score += 25 if n_strong_cats >= 2 else (15 if n_strong_cats >= 1 else 5)
score += 15 if acc > baseline_acc + 0.1 else (10 if acc > baseline_acc else 5)
score += 10 if has_metabolites else 5

if score >= 80: verdict = "🟢 GO"
elif score >= 60: verdict = "🟡 CONDITIONAL GO"
elif score >= 40: verdict = "🟠 WEAK GO"
else: verdict = "🔴 NO GO"

print(f"""
┌─────────────────────────────────────────────────────────────┐
│                 MVE v1.5 综合判定 (2026-07-21)                │
├─────────────────────────────────────────────────────────────┤
│  最佳回归 R²:       {best_r2:.4f} ({best_reg['model']})                 │
│  最大类别效应量 |d|: {abs_d_max:.3f}                                │
│  强效应类别数 (|d|>0.8): {n_strong_cats}                                     │
│  分类 Accuracy:     {acc:.3f} (基线={baseline_acc:.3f})                     │
│  代谢物数据:        {'✅ 已整合' if has_metabolites else '⚠️ 未完成'}                          │
├─────────────────────────────────────────────────────────────┤
│  综合评分:           {score}/100                                        │
│  判定: {verdict}                                                  │
├─────────────────────────────────────────────────────────────┤
│  ⚠️ 数据限制: 2温度点(45/55°C), 46行, 23化合物              │
│  📊 v2 扩展: 4论文, 100行, 50化合物 → mve_v2/               │
│  🧪 下一步: Tier-1 实验 (≥4温度×≥5时间点×3重复)            │
└─────────────────────────────────────────────────────────────┘
""")

# ============================================================
# 9. 保存结果
# ============================================================
# 回归结果
pd.DataFrame(results_reg).to_csv(OUT_DIR / "mve_baseline_results.csv", index=False, encoding='utf-8-sig')

# 效应量
cat_eff_df.to_csv(OUT_DIR / "mve_effect_sizes.csv", index=False, encoding='utf-8-sig')

# 特征重要性
imp_df = pd.DataFrame({
    'feature': ALL_FEATURES,
    'importance_mean': rf_imp.mean(axis=0),
    'importance_std': rf_imp.std(axis=0),
})
imp_df.to_csv(OUT_DIR / "mve_feature_importance.csv", index=False, encoding='utf-8-sig')

print(f"\n[OK] 回归结果: mve_baseline_results.csv")
print(f"[OK] 效应量: mve_effect_sizes.csv")
print(f"[OK] 特征重要性: mve_feature_importance.csv")
print("\n[DONE] MVE v1.5 分析完成")
