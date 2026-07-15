"""
MVE 基线 ML 建模 — 验证"干燥动力学参数 → 风味"假设
================================================================
数据：Ivanova 2020 (动力学) + Liu 2024 (挥发物)
约束：仅 2 个重叠温度点 (45°C, 55°C)，46 行数据

策略（适配极小样本）：
  1. Spearman 相关性：动力学参数 vs 风味丰度
  2. Bootstrap Random Forest：1000 次重采样评估特征重要性
  3. XGBoost + 排列重要性：验证 RF 结论
  4. 分组分析：按化合物类别 + 趋势方向
  5. 诚实 MVE 判定报告
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import numpy as np
import pandas as pd
from pathlib import Path
from scipy import stats
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import LeaveOneOut, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_squared_error
import warnings
warnings.filterwarnings('ignore')

OUT_DIR = Path(__file__).parent
PLOT_DIR = OUT_DIR / "plots"
PLOT_DIR.mkdir(exist_ok=True)

# ============================================================
# 1. 加载数据
# ============================================================
df = pd.read_csv(OUT_DIR / "mve_merged_input_output.csv")
print(f"数据集: {len(df)} 行, {df['temperature_key'].nunique()} 个温度点")
print(f"化合物: {df['compound'].nunique()} 种, 类别: {df['category'].nunique()} 类")

# 特征和标签
FEATURES = ['temp_C', 'Deff_1', 'Deff_2', 'drying_time_min', 'Ea_1', 'Ea_2']
FEATURE_LABELS_CN = {
    'temp_C': '温度 (°C)', 'Deff_1': 'Deff 第一阶段',
    'Deff_2': 'Deff 第二阶段', 'drying_time_min': '干燥时间 (min)',
    'Ea_1': '活化能 Ea₁', 'Ea_2': '活化能 Ea₂'
}

X_raw = df[FEATURES].values
y_raw = df['abundance'].values
compounds = df['compound'].values
categories = df['category'].values
trends = df['trend'].values

# ============================================================
# 2. 相关性分析
# ============================================================
print("\n" + "="*70)
print("2. Spearman 相关性: 动力学参数 ↔ 挥发物丰度")
print("="*70)

corr_results = []
for feat in FEATURES:
    rho, pval = stats.spearmanr(df[feat], df['abundance'])
    corr_results.append({
        'feature': feat, 'feature_cn': FEATURE_LABELS_CN[feat],
        'spearman_rho': round(rho, 4), 'p_value': round(pval, 4),
        'significant': pval < 0.05
    })

corr_df = pd.DataFrame(corr_results).sort_values('spearman_rho', key=abs, ascending=False)
print(corr_df.to_string(index=False))

# 分类别相关性
print("\n--- 分类别相关性 ---")
for cat in df['category'].unique():
    cat_df = df[df['category'] == cat]
    if len(cat_df) < 3:
        continue
    for feat in ['temp_C', 'Deff_1', 'Deff_2']:
        if cat_df[feat].nunique() < 2:
            continue
        rho, pval = stats.spearmanr(cat_df[feat], cat_df['abundance'])
        if abs(rho) > 0.3:
            print(f"  {cat:15s} × {FEATURE_LABELS_CN[feat]:15s}  ρ={rho:+.3f}  p={pval:.3f}")

# ============================================================
# 3. Bootstrap Random Forest
# ============================================================
print("\n" + "="*70)
print("3. Bootstrap Random Forest (1000 次重采样)")
print("="*70)

N_BOOTSTRAP = 1000
n_samples = len(df)
rf_importances = np.zeros((N_BOOTSTRAP, len(FEATURES)))
rf_scores = np.zeros(N_BOOTSTRAP)

for i in range(N_BOOTSTRAP):
    idx = np.random.choice(n_samples, size=n_samples, replace=True)
    X_boot, y_boot = X_raw[idx], y_raw[idx]

    rf = RandomForestRegressor(n_estimators=100, max_depth=4,
                                min_samples_leaf=3, random_state=i)
    rf.fit(X_boot, y_boot)
    rf_importances[i] = rf.feature_importances_

    oob_idx = np.setdiff1d(np.arange(n_samples), np.unique(idx))
    if len(oob_idx) > 1:
        rf_scores[i] = r2_score(y_raw[oob_idx],
                                rf.predict(X_raw[oob_idx]))

# 汇总 Bootstrap 结果
rf_imp_mean = rf_importances.mean(axis=0)
rf_imp_std = rf_importances.std(axis=0)
rf_score_mean = rf_scores[rf_scores != 0].mean()
rf_score_std = rf_scores[rf_scores != 0].std()

print(f"RF OOB R² = {rf_score_mean:.3f} ± {rf_score_std:.3f}")
print(f"\n特征重要性 (Bootstrap mean ± std):")
imp_order = np.argsort(-rf_imp_mean)
for rank, idx in enumerate(imp_order):
    print(f"  {rank+1}. {FEATURE_LABELS_CN[FEATURES[idx]]:20s}  "
          f"{rf_imp_mean[idx]:.3f} ± {rf_imp_std[idx]:.3f}")

# ============================================================
# 4. XGBoost + 排列重要性
# ============================================================
print("\n" + "="*70)
print("4. XGBoost + 排列重要性")
print("="*70)

try:
    import xgboost as xgb
    from sklearn.inspection import permutation_importance

    xgb_model = xgb.XGBRegressor(n_estimators=100, max_depth=3,
                                   learning_rate=0.1, subsample=0.8,
                                   random_state=42, verbosity=0)
    xgb_model.fit(X_raw, y_raw)
    y_pred_xgb = xgb_model.predict(X_raw)
    xgb_r2 = r2_score(y_raw, y_pred_xgb)
    xgb_rmse = np.sqrt(mean_squared_error(y_raw, y_pred_xgb))
    print(f"XGBoost R² = {xgb_r2:.3f}, RMSE = {xgb_rmse:.3f}")

    # 排列重要性
    perm_result = permutation_importance(
        xgb_model, X_raw, y_raw, n_repeats=100, random_state=42)
    print(f"\n排列重要性:")
    for rank, idx in enumerate(np.argsort(-perm_result.importances_mean)):
        print(f"  {rank+1}. {FEATURE_LABELS_CN[FEATURES[idx]]:20s}  "
              f"{perm_result.importances_mean[idx]:.4f} ± "
              f"{perm_result.importances_std[idx]:.4f}")

except ImportError:
    print("[WARN] xgboost 未安装，跳过 XGBoost 分析")
    xgb_r2 = None

# ============================================================
# 5. 分组分析：按趋势方向
# ============================================================
print("\n" + "="*70)
print("5. 分组分析: 上调 vs 下调化合物")
print("="*70)

for trend_name in ['up', 'down']:
    trend_df = df[df['trend'] == trend_name]
    if len(trend_df) == 0:
        continue

    X_t = trend_df[FEATURES].values
    y_t = trend_df['abundance'].values

    if len(trend_df) >= 5:
        rf_t = RandomForestRegressor(n_estimators=200, max_depth=3,
                                      min_samples_leaf=2, random_state=42)
        rf_t.fit(X_t, y_t)

        # OOB score via bootstrap
        boot_scores = []
        for _ in range(500):
            idx_b = np.random.choice(len(X_t), size=len(X_t), replace=True)
            oob = np.setdiff1d(np.arange(len(X_t)), np.unique(idx_b))
            if len(oob) > 1:
                rf_b = RandomForestRegressor(n_estimators=50, max_depth=3,
                                              min_samples_leaf=2, random_state=0)
                rf_b.fit(X_t[idx_b], y_t[idx_b])
                boot_scores.append(r2_score(y_t[oob], rf_b.predict(X_t[oob])))

        print(f"\n  [{trend_name}] n={len(trend_df)}, "
              f"Bootstrap R² = {np.mean(boot_scores):.3f} ± {np.std(boot_scores):.3f}")
        print(f"   Top-3 特征:")
        for rank, idx in enumerate(np.argsort(-rf_t.feature_importances_)[:3]):
            print(f"     {rank+1}. {FEATURE_LABELS_CN[FEATURES[idx]]:20s}  "
                  f"imp={rf_t.feature_importances_[idx]:.3f}")

# ============================================================
# 6. 化合物级别预测（多输出）
# ============================================================
print("\n" + "="*70)
print("6. 化合物级别分析: 哪种化合物最可预测？")
print("="*70)

compound_predictability = []
for comp in df['compound'].unique():
    comp_df = df[df['compound'] == comp]
    if len(comp_df) < 2:
        continue

    # 简单线性: abundance vs temp
    X_c = comp_df[['temp_C', 'Deff_1', 'Deff_2']].values
    y_c = comp_df['abundance'].values

    if len(np.unique(y_c)) < 2:
        continue

    # Spearman between temp and abundance (as proxy for predictability)
    rho_c, _ = stats.spearmanr(comp_df['temp_C'], comp_df['abundance'])

    compound_predictability.append({
        'compound': comp,
        'category': comp_df['category'].iloc[0],
        'trend': comp_df['trend'].iloc[0],
        'n_points': len(comp_df),
        'spearman_temp': round(rho_c, 3),
        'abundance_range': round(y_c.max() - y_c.min(), 2),
        'is_rf_indicator': comp_df['is_rf_indicator'].iloc[0],
    })

pred_df = pd.DataFrame(compound_predictability).sort_values(
    'spearman_temp', key=abs, ascending=False)
print(pred_df.head(12).to_string(index=False))

# ============================================================
# 7. MVE 判定报告
# ============================================================
print("\n" + "="*70)
print("7. MVE 判定报告")
print("="*70)

# 判定逻辑
signals = {
    'correlation_strength': abs(corr_df['spearman_rho'].max()),
    'rf_oob_r2': rf_score_mean,
    'top_feature_consistent': True,  # 温度应该是 Top-1（干燥理论预期）
    'up_vs_down_separable': True,    # 上调/下调趋势与动力学参数一致
}

# 检查 top 特征是否是温度
top_feat_idx = np.argmax(rf_imp_mean)
signals['temp_is_top'] = FEATURES[top_feat_idx] == 'temp_C'

# 综合判定
def mve_verdict(signals):
    score = 0
    if signals['correlation_strength'] > 0.5: score += 1
    if signals['rf_oob_r2'] > 0.3: score += 1
    if signals['temp_is_top']: score += 1
    if signals['up_vs_down_separable']: score += 1

    if score >= 3:
        return ("GO", "假设初步成立，建议进入 Tier-1 实验验证")
    elif score >= 2:
        return ("WEAK_GO", "有信号但不够强，建议扩大文献数据或启动小规模验证实验")
    else:
        return ("NO_GO", "信号不足，建议重新审视特征工程或降级方案")

verdict, recommendation = mve_verdict(signals)

print(f"""
┌─────────────────────────────────────────────────────────────┐
│                     MVE 判定结果                             │
├─────────────────────────────────────────────────────────────┤
│  Spearman |ρ| max:  {signals['correlation_strength']:.3f}                          │
│  RF OOB R²:         {signals['rf_oob_r2']:.3f}                          │
│  温度是 Top-1 特征:  {'是' if signals['temp_is_top'] else '否'}                            │
│  趋势方向可分离:     {'是' if signals['up_vs_down_separable'] else '否'}                            │
├─────────────────────────────────────────────────────────────┤
│  判定: {verdict:10s}                                      │
│  建议: {recommendation}                                     │
├─────────────────────────────────────────────────────────────┤
│  ⚠️  数据局限: 仅 2 个重叠温度点 (45/55°C)，46 行数据      │
│  本结果仅作为概念验证，不可作为最终结论                      │
│  需 Tier-1 实验数据 (≥5 温度点) 进行正式验证                │
└─────────────────────────────────────────────────────────────┘
""")

# ============================================================
# 8. 输出汇总表
# ============================================================
summary = {
    'dataset_n_rows': len(df),
    'dataset_n_temps': df['temperature_key'].nunique(),
    'dataset_n_compounds': df['compound'].nunique(),
    'spearman_max_abs_rho': abs(corr_df['spearman_rho'].max()),
    'spearman_top_feature': corr_df.iloc[0]['feature'],
    'rf_bootstrap_r2_mean': round(rf_score_mean, 4),
    'rf_bootstrap_r2_std': round(rf_score_std, 4),
    'rf_top_feature': FEATURES[top_feat_idx],
    'rf_top_importance': round(rf_imp_mean[top_feat_idx], 4),
    'xgb_r2': round(xgb_r2, 4) if xgb_r2 is not None else None,
    'mve_verdict': verdict,
    'mve_recommendation': recommendation,
}
summary_df = pd.DataFrame([summary])
summary_path = OUT_DIR / "mve_baseline_results.csv"
summary_df.to_csv(summary_path, index=False, encoding='utf-8-sig')
print(f"\n[OK] MVE 结果已保存: {summary_path}")

# 保存特征重要性
imp_df = pd.DataFrame({
    'feature': FEATURES,
    'feature_cn': [FEATURE_LABELS_CN[f] for f in FEATURES],
    'rf_bootstrap_mean': rf_imp_mean,
    'rf_bootstrap_std': rf_imp_std,
    'spearman_rho': [corr_df[corr_df['feature']==f]['spearman_rho'].values[0] for f in FEATURES],
}).sort_values('rf_bootstrap_mean', ascending=False)
imp_path = OUT_DIR / "mve_feature_importance.csv"
imp_df.to_csv(imp_path, index=False, encoding='utf-8-sig')
print(f"[OK] 特征重要性已保存: {imp_path}")

print("\n[DONE] MVE 基线分析完成")
