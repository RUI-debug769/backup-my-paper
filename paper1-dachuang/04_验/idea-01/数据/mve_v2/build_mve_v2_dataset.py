#!/usr/bin/env python3
"""
MVE v2 — 构建增强数据集
========================
数据来源:
  1. Ivanova 2020 — 干燥动力学 (MR时间序列 + Deff/Ea)
  2. Liu 2024 — 23种VOC @ 45/55/65°C (GC-IMS) + 1645代谢物 (LC-MS/MS)
  3. Liao 2025 — 28种VOC绝对定量 @ 4种干燥方法 (HS-SPME-GC-MS)
  4. Yi/Guo 2025 — 270 VOC + 1419代谢物摘要统计

结构:
  mve_v2_dataset.csv  — 主数据集 (化合物 × 温度/方法)
  mve_v2_metadata.csv — 数据溯源
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pandas as pd
import numpy as np
from pathlib import Path

OUT_DIR = Path(__file__).parent
DATA_V1 = Path(__file__).parent.parent  # ../即 数据/

# ============================================================
# 1. 加载 v1 数据集 (Ivanova + Liu)
# ============================================================
df_v1 = pd.read_csv(DATA_V1 / "mve_merged_input_output.csv")
print(f"v1 数据集: {len(df_v1)} 行, {df_v1['compound'].nunique()} 化合物, "
      f"{df_v1['temperature_key'].nunique()} 温度点")

# ============================================================
# 2. Liao 2025 数据 (手动录入已知数值，从论文提取+校验)
# ============================================================
# 从 Liao 2025 Table 4 提取的 28 种 VOC 绝对定量 (μg/kg DW)
# 四个干燥方法: FS(新鲜), HAD(55°C热风), HAD-MVD(热风+微波真空), VFD(真空冷冻), ND(自然干燥)
liao_vocs = [
    # Alcohols (7)
    {"compound": "1-Octen-3-ol",       "category": "alcohols",    "FS": 0,       "HAD": 2146449, "HAD_MVD": 1030149, "VFD": 214333,  "ND": 168497,  "note": "蘑菇特征香气"},
    {"compound": "Benzyl alcohol",     "category": "alcohols",    "FS": 0,       "HAD": 0,       "HAD_MVD": 0,       "VFD": 994,     "ND": 0,       "note": "花香"},
    {"compound": "2-Ethyl-1-hexanol",  "category": "alcohols",    "FS": 2038,    "HAD": 1570,   "HAD_MVD": 18139,   "VFD": 8794,    "ND": 1731,    "note": "柑橘/花香/甜味"},
    {"compound": "1-Octanol",          "category": "alcohols",    "FS": 0,       "HAD": 270,    "HAD_MVD": 0,       "VFD": 0,       "ND": 0,       "note": "蘑菇/糯米香"},
    {"compound": "4-Methyl-1-pentanol","category": "alcohols",    "FS": 0,       "HAD": 0,      "HAD_MVD": 469,     "VFD": 549,     "ND": 0,       "note": ""},
    {"compound": "1-Hexanol",          "category": "alcohols",    "FS": 0,       "HAD": 114,    "HAD_MVD": 0,       "VFD": 310,     "ND": 0,       "note": "油/醇香"},
    {"compound": "Ethylene glycol",    "category": "alcohols",    "FS": 0,       "HAD": 0,      "HAD_MVD": 0,       "VFD": 497,     "ND": 0,       "note": ""},

    # Aldehydes (6)
    {"compound": "Benzaldehyde",       "category": "aldehydes",   "FS": 0,       "HAD": 0,      "HAD_MVD": 282,     "VFD": 1088,    "ND": 0,       "note": "杏仁香"},
    {"compound": "E-2-Octenal",        "category": "aldehydes",   "FS": 0,       "HAD": 0,      "HAD_MVD": 0,       "VFD": 134,     "ND": 0,       "note": ""},
    {"compound": "Nonanal",            "category": "aldehydes",   "FS": 0,       "HAD": 0,      "HAD_MVD": 451,     "VFD": 861,     "ND": 0,       "note": "柑橘/脂肪香"},
    {"compound": "Octanal",            "category": "aldehydes",   "FS": 0,       "HAD": 0,      "HAD_MVD": 0,       "VFD": 181,     "ND": 0,       "note": ""},
    {"compound": "Decanal",            "category": "aldehydes",   "FS": 0,       "HAD": 209,    "HAD_MVD": 241,     "VFD": 264,     "ND": 0,       "note": ""},
    {"compound": "Hexanal",            "category": "aldehydes",   "FS": 0,       "HAD": 77,     "HAD_MVD": 113,     "VFD": 340,     "ND": 0,       "note": "青草香(羊肚菌关键)"},

    # Ketones (4)
    {"compound": "3-Octanone",         "category": "ketones",     "FS": 0,       "HAD": 0,      "HAD_MVD": 146,     "VFD": 669,     "ND": 0,       "note": "蘑菇/果香"},
    {"compound": "1-Octen-3-one",      "category": "ketones",     "FS": 0,       "HAD": 0,      "HAD_MVD": 185,     "VFD": 608,     "ND": 0,       "note": "蘑菇香"},
    {"compound": "2-Octanone",         "category": "ketones",     "FS": 0,       "HAD": 0,      "HAD_MVD": 0,       "VFD": 197,     "ND": 0,       "note": ""},
    {"compound": "2-Nonanone",         "category": "ketones",     "FS": 0,       "HAD": 0,      "HAD_MVD": 0,       "VFD": 128,     "ND": 0,       "note": ""},

    # Alkanes (5)
    {"compound": "Tetradecane",        "category": "alkanes",     "FS": 0,       "HAD": 0,      "HAD_MVD": 0,       "VFD": 137,     "ND": 0,       "note": ""},
    {"compound": "Pentadecane",        "category": "alkanes",     "FS": 458,     "HAD": 166,    "HAD_MVD": 240,     "VFD": 223,     "ND": 0,       "note": ""},
    {"compound": "Hexadecane",         "category": "alkanes",     "FS": 585,     "HAD": 0,      "HAD_MVD": 518,     "VFD": 292,     "ND": 0,       "note": ""},
    {"compound": "Heptadecane",        "category": "alkanes",     "FS": 1033,    "HAD": 0,      "HAD_MVD": 0,       "VFD": 0,       "ND": 946,     "note": ""},
    {"compound": "Octadecane",         "category": "alkanes",     "FS": 727,     "HAD": 0,      "HAD_MVD": 623,     "VFD": 0,       "ND": 1403,    "note": ""},

    # Aromatic hydrocarbons (3)
    {"compound": "p-Xylene",           "category": "aromatics",   "FS": 0,       "HAD": 0,      "HAD_MVD": 0,       "VFD": 149,     "ND": 0,       "note": ""},
    {"compound": "Naphthalene",        "category": "aromatics",   "FS": 0,       "HAD": 0,      "HAD_MVD": 80,      "VFD": 284,     "ND": 0,       "note": ""},
    {"compound": "2,6-Di-tert-butyl-4-methylphenol", "category": "aromatics", "FS": 0, "HAD": 0, "HAD_MVD": 0, "VFD": 0, "ND": 0, "note": "抗氧化剂"},

    # Others (3)
    {"compound": "2-Pentyl-furan",     "category": "others",      "FS": 0,       "HAD": 0,      "HAD_MVD": 400,     "VFD": 622,     "ND": 0,       "note": "果香/豆香"},
    {"compound": "trans-2-Decenal",    "category": "others",      "FS": 0,       "HAD": 0,      "HAD_MVD": 0,       "VFD": 294,     "ND": 0,       "note": ""},
    {"compound": "2,5-Di-tert-butylphenol", "category": "others", "FS": 82,     "HAD": 0,      "HAD_MVD": 0,       "VFD": 0,       "ND": 0,       "note": ""},
]

df_liao = pd.DataFrame(liao_vocs)
print(f"Liao 2025: {len(df_liao)} 种 VOC (@ 4干燥方法)")

# 转为长格式 (melt: 每个化合物×方法 一行)
methods_map = {
    'FS':       {'method': 'Fresh',         'temp_C': 25,  'drying_type': 'none'},
    'HAD':      {'method': 'HAD',           'temp_C': 55,  'drying_type': 'hot_air'},
    'HAD_MVD':  {'method': 'HAD-MVD',       'temp_C': 55,  'drying_type': 'combined'},
    'VFD':      {'method': 'VFD',           'temp_C': -30, 'drying_type': 'freeze'},
    'ND':       {'method': 'ND',            'temp_C': 25,  'drying_type': 'natural'},
}

records = []
for _, row in df_liao.iterrows():
    for method_col, method_info in methods_map.items():
        abundance = row[method_col]
        if abundance > 0:  # 只保留检测到的
            records.append({
                'compound': row['compound'],
                'category': row['category'],
                'source': 'Liao2025',
                'method': method_info['method'],
                'temp_C': method_info['temp_C'],
                'drying_type': method_info['drying_type'],
                'abundance_ug_kg': abundance,
                'log_abundance': np.log10(abundance + 1),
                'note': row['note'],
            })

df_liao_long = pd.DataFrame(records)
print(f"  → 长格式: {len(df_liao_long)} 行")

# ============================================================
# 3. Yi/Guo 2025 摘要统计
# ============================================================
yi_stats = {
    'total_nonvolatile': 1419,
    'total_volatile': 270,
    'differentially_abundant': 511,
    'new_metabolites_pileus': 37,  # 21 non-volatile + 16 volatile
    'new_metabolites_stipe': 35,
    'drying_temp_C': 55,  # hot-air drying at 55°C
    'journal': 'Food Science & Nutrition',
    'doi': '10.1002/fsn3.70826',
}
print(f"\nYi/Guo 2025: {yi_stats['total_volatile']} VOC + "
      f"{yi_stats['total_nonvolatile']} 非挥发代谢物 (热风55°C, 菌盖/菌柄)")

# ============================================================
# 4. 合并数据集
# ============================================================
print("\n" + "=" * 70)
print("合并数据集")
print("=" * 70)

# v1 数据集重命名列以对齐
df_v1_renamed = df_v1.rename(columns={
    'abundance': 'abundance_norm',
    'temp_C': 'temp_C',
    'trend': 'trend_direction',
}).copy()
df_v1_renamed['source'] = 'Liu2024_v1'
df_v1_renamed['drying_type'] = 'hot_air'
df_v1_renamed['method'] = 'HAD_' + df_v1_renamed['temperature_key']

# 添加 log transform
df_v1_renamed['abundance_ug_kg'] = np.nan  # v1 中无绝对定量
df_v1_renamed['log_abundance'] = np.log10(df_v1_renamed['abundance_norm'].clip(lower=0.01) + 1)

# Liao 长格式添加归一化
df_liao_long['abundance_norm'] = df_liao_long['abundance_ug_kg'] / df_liao_long['abundance_ug_kg'].max()
df_liao_long['trend_direction'] = 'unknown'
df_liao_long['source'] = 'Liao2025'

# 合并
common_cols = ['compound', 'category', 'source', 'method', 'temp_C',
               'drying_type', 'abundance_norm', 'log_abundance',
               'abundance_ug_kg', 'trend_direction']
df_v1_subset = df_v1_renamed[common_cols]
df_liao_subset = df_liao_long[common_cols]

df_merged = pd.concat([df_v1_subset, df_liao_subset], ignore_index=True)
print(f"合并数据集: {len(df_merged)} 行")
print(f"  数据源: {df_merged['source'].value_counts().to_dict()}")
print(f"  化合物: {df_merged['compound'].nunique()} 种")
print(f"  类别: {df_merged['category'].value_counts().to_dict()}")

# ============================================================
# 5. 保存
# ============================================================
mve_path = OUT_DIR / "mve_v2_dataset.csv"
df_merged.to_csv(mve_path, index=False, encoding='utf-8-sig')
print(f"\n[OK] MVE v2 数据集已保存: {mve_path}")

# 元数据
meta = {
    'dataset_version': 'v2',
    'created': '2026-07-21',
    'n_rows': len(df_merged),
    'n_compounds': int(df_merged['compound'].nunique()),
    'n_categories': int(df_merged['category'].nunique()),
    'sources': df_merged['source'].value_counts().to_dict(),
    'category_distribution': df_merged['category'].value_counts().to_dict(),
    'yi2025_stats': yi_stats,
}
import json
meta_path = OUT_DIR / "mve_v2_metadata.json"
meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding='utf-8')
print(f"[OK] 元数据已保存: {meta_path}")

print("\n[DONE] MVE v2 数据集构建完成")
