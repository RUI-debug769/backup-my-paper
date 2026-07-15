"""
从 Ivanova et al. 2020 Table 3 模型方程重建 Morchella esculenta 干燥曲线
输出：MR 时间序列 + Deff/Ea 参数 → CSV
"""
import numpy as np
import pandas as pd
from pathlib import Path

OUT_DIR = Path(__file__).parent

# ============================================================
# 1. 实验参数 (Ivanova 2020 Table 2 & Table 4)
# ============================================================
experiments = {
    "T35": {
        "temp_C": 35,
        "drying_time_min": 170,
        "slice_mm": 2.0,
        "MC_initial_wb": 89.41,
        "Deff_1": 6.17e-9,    # m²/s, first falling rate
        "Deff_2": 16.11e-9,   # m²/s, second falling rate
        "Ea_1": 31.26,        # kJ/mol, first period
        "Ea_2": 17.75,        # kJ/mol, second period
    },
    "T45": {
        "temp_C": 45,
        "drying_time_min": 150,
        "slice_mm": 2.0,
        "MC_initial_wb": 89.41,
        "Deff_1": 8.72e-9,
        "Deff_2": 18.01e-9,
        "Ea_1": 31.26,
        "Ea_2": 17.75,
    },
    "T55": {
        "temp_C": 55,
        "drying_time_min": 120,
        "slice_mm": 2.0,
        "MC_initial_wb": 89.41,
        "Deff_1": 12.98e-9,
        "Deff_2": 24.63e-9,
        "Ea_1": 31.26,
        "Ea_2": 17.75,
    },
}

# ============================================================
# 2. 最佳拟合模型方程 (Ivanova 2020 Table 3)
# ============================================================

def log_model(t, k=0.0099, a=1.2083, c=-0.2256):
    """Logarithmic model — 35°C 最佳 (R²=0.9970)"""
    return a * np.exp(-k * t) + c

def midilli_model(t, k=0.0422, a=1.0085, b=-0.0004, n=0.8229):
    """Midilli et al. model — 45°C 最佳 (R²=0.9920)"""
    return a * np.exp(-k * t**n) + b * t

def lewis_model(t, k=0.03434):
    """Lewis model — 55°C 最佳 (R²=0.9868)"""
    return np.exp(-k * t)

# 每个温度的最佳模型
BEST_MODELS = {
    "T35": (log_model, {"k": 0.0099, "a": 1.2083, "c": -0.2256}),
    "T45": (midilli_model, {"k": 0.0422, "a": 1.0085, "b": -0.0004, "n": 0.8229}),
    "T55": (lewis_model, {"k": 0.03434}),
}

# 统一 Midilli et al. 模型参数 (三温度通用)
UNIFIED_MIDILLI = {
    "T35": {"k": 0.0128, "a": 0.9895, "b": -0.0009, "n": 0.9744},   # R²=0.9969
    "T45": {"k": 0.0422, "a": 1.0085, "b": -0.0004, "n": 0.8229},   # R²=0.9920
    "T55": {"k": 0.0323, "a": 1.0099, "b": 0.0001,  "n": 1.0247},   # R²=0.9871
}

# ============================================================
# 3. 重建 MR 时间序列
# ============================================================
def reconstruct_mr_curves(time_step=1.0):
    """用最佳拟合模型生成 MR 时间序列"""
    records = []

    for exp_id, exp in experiments.items():
        t_max = exp["drying_time_min"]
        t = np.arange(0, t_max + time_step, time_step)

        # 最佳模型
        best_fn, best_params = BEST_MODELS[exp_id]
        mr_best = best_fn(t, **best_params)
        mr_best = np.clip(mr_best, 0.0, 1.0)  # clamp to valid range

        # 统一 Midilli 模型
        uni_params = UNIFIED_MIDILLI[exp_id]
        mr_unified = midilli_model(t, **uni_params)
        mr_unified = np.clip(mr_unified, 0.0, 1.0)

        for i, ti in enumerate(t):
            records.append({
                "experiment": exp_id,
                "temp_C": exp["temp_C"],
                "time_min": round(ti, 1),
                "MR_best_model": round(mr_best[i], 6),
                "MR_unified_midilli": round(mr_unified[i], 6),
                "Deff_1_m2s": exp["Deff_1"],
                "Deff_2_m2s": exp["Deff_2"],
                "Ea_1_kJmol": exp["Ea_1"],
                "Ea_2_kJmol": exp["Ea_2"],
                "drying_time_total_min": exp["drying_time_min"],
                "slice_mm": exp["slice_mm"],
            })

    return pd.DataFrame(records)

# ============================================================
# 4. 生成干燥速率 (DR = -dMR/dt)
# ============================================================
def add_drying_rate(df):
    """计算干燥速率"""
    df = df.copy()
    df["DR_per_min"] = np.nan
    for exp_id in df["experiment"].unique():
        mask = df["experiment"] == exp_id
        exp_df = df[mask].sort_values("time_min")
        mr = exp_df["MR_best_model"].values
        t = exp_df["time_min"].values
        dr = np.zeros_like(mr)
        dr[1:] = -(mr[1:] - mr[:-1]) / (t[1:] - t[:-1])
        dr[0] = dr[1]  # forward-fill first point
        df.loc[mask, "DR_per_min"] = dr
    return df

# ============================================================
# 5. 生成 MVE 特征汇总表
# ============================================================
def make_summary_table(df):
    """每个实验一条汇总记录（用于 ML 输入）"""
    summaries = []
    for exp_id in df["experiment"].unique():
        exp_df = df[df["experiment"] == exp_id]
        row = {
            "experiment": exp_id,
            "temp_C": exp_df["temp_C"].iloc[0],
            "drying_time_min": exp_df["drying_time_total_min"].iloc[0],
            "Deff_1_mean": exp_df["Deff_1_m2s"].iloc[0],
            "Deff_2_mean": exp_df["Deff_2_m2s"].iloc[0],
            "Ea_1_mean": exp_df["Ea_1_kJmol"].iloc[0],
            "Ea_2_mean": exp_df["Ea_2_kJmol"].iloc[0],
            "MR_final": exp_df[exp_df["time_min"] == exp_df["time_min"].max()]["MR_best_model"].values[0],
            "DR_max": exp_df["DR_per_min"].max(),
            "DR_mean": exp_df["DR_per_min"].mean(),
        }
        summaries.append(row)
    return pd.DataFrame(summaries)

# ============================================================
# 6. 执行 + 输出
# ============================================================
if __name__ == "__main__":
    import sys, io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    # 重建曲线
    df = reconstruct_mr_curves(time_step=1.0)
    df = add_drying_rate(df)

    # 保存完整时间序列
    ts_path = OUT_DIR / "ivanova2020_mr_timeseries.csv"
    df.to_csv(ts_path, index=False, encoding="utf-8-sig")
    print(f"✅ 时间序列已保存: {ts_path} ({len(df)} 行)")

    # 保存汇总特征表
    summary = make_summary_table(df)
    sum_path = OUT_DIR / "ivanova2020_features_summary.csv"
    summary.to_csv(sum_path, index=False, encoding="utf-8-sig")
    print(f"✅ 特征汇总已保存: {sum_path}")

    # 打印预览
    print("\n📊 特征汇总预览:")
    print(summary.to_string(index=False))

    print(f"\n📈 每个实验的时间点数:")
    for exp_id in df["experiment"].unique():
        print(f"  {exp_id}: {len(df[df['experiment']==exp_id])} 个时间点")

    # 验证：打印每个实验的 5 个代表性时间点
    print("\n🔍 MR 时间序列抽样验证:")
    for exp_id in df["experiment"].unique():
        exp_df = df[df["experiment"] == exp_id].sort_values("time_min")
        sample_indices = np.linspace(0, len(exp_df)-1, 5, dtype=int)
        for idx in sample_indices:
            row = exp_df.iloc[idx]
            print(f"  {exp_id} | t={row['time_min']:6.1f} min | MR={row['MR_best_model']:.4f} | DR={row['DR_per_min']:.4f}")
        print()
