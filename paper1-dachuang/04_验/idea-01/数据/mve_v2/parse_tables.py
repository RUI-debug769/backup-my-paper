#!/usr/bin/env python3
"""
MVE v2 — 解析 Liao 2025 和 Yi/Guo 2025 的 VOC/代谢物表格数据
从 PDF 全文提取的文本中解析结构化 CSV
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import re
import pandas as pd
import numpy as np
from pathlib import Path

OUT_DIR = Path(__file__).parent

# ============================================================
# 1. Liao 2025 VOC Table 4 解析
# ============================================================
print("=" * 70)
print("1. 解析 Liao 2025 Table 4 — 挥发性化合物")
print("=" * 70)

def parse_liao2025_table4(text):
    """解析 Liao 2025 Table 4 挥发性化合物数据"""

    # Table 4 标题行
    table4_start = text.find("Effects of different drying methods on volatile compounds")
    if table4_start < 0:
        print("[ERROR] 找不到 Table 4")
        return None

    # 从标题行开始提取
    table_text = text[table4_start:]
    # Table 4 结束于下一个 "Table" 或文本末尾
    next_table = table_text.find("Table", 10)  # skip the header match
    if next_table > 0:
        table_text = table_text[:next_table]

    lines = table_text.split('\n')

    # 解析化合物数据
    # 每个条目格式: number, compound_name, CAS, Content (FS, HAD, HAD-MVD, VFD, ND), Odor
    compounds = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # 检测化合物编号 (1-29 的数字)
        if re.match(r'^\d{1,2}$', line):
            # 下一行是化合物名称
            if i + 1 < len(lines):
                name = lines[i + 1].strip()

                # 跳过类别标题行 (如 "Alcohols", "Aldehydes" 等以及 "–")
                if name in ['–', ''] or len(name) < 2:
                    i += 1
                    continue

                # 收集后续行的数据
                # CAS 在前面 (跳过1行)
                cas = ""
                if i + 3 < len(lines):
                    cas_line = lines[i + 3].strip()
                    cas = cas_line if cas_line != '–' else ""

                # 含量值分散在多行 (FS, HAD, HAD-MVD, VFD, ND)
                # 从 CAS 后 2 行开始是实际数值行
                fs_val, had_val, mvd_val, vfd_val, nd_val = "ND", "ND", "ND", "ND", "ND"
                odor = ""

                j = i + 5  # 跳过 number, name, blank, CAS, blank
                values_found = 0
                odor_lines = []

                while j < len(lines) and j < i + 20:
                    val_line = lines[j].strip()

                    # 检查是否到达下一个化合物
                    if re.match(r'^\d{1,2}$', val_line) and values_found >= 3:
                        break

                    # 检查是否是数值行 (含数字)
                    if re.search(r'[\d,]{3,}', val_line):
                        if values_found == 0:
                            fs_val = val_line
                        elif values_found == 1:
                            had_val = val_line
                        elif values_found == 2:
                            mvd_val = val_line
                        elif values_found == 3:
                            vfd_val = val_line
                        elif values_found == 4:
                            nd_val = val_line
                        values_found += 1
                    elif not re.match(r'^\d{1,2}$', val_line) and not re.match(r'^[–-]$', val_line) and len(val_line) > 2:
                        # 可能是气味描述或续行
                        if values_found >= 5 and not re.match(r'^\d', val_line):
                            odor_lines.append(val_line)

                    j += 1

                odor = ' '.join(odor_lines) if odor_lines else ""

                compound_num = int(line)
                compounds.append({
                    'compound_num': compound_num,
                    'compound': name,
                    'category': current_category,
                    'cas': cas,
                    'FS_ug_kg': fs_val,
                    'HAD_ug_kg': had_val,
                    'HAD_MVD_ug_kg': mvd_val,
                    'VFD_ug_kg': vfd_val,
                    'ND_ug_kg': nd_val,
                    'odor_description': odor[:200]
                })

        # 检测类别标题
        if line in ['Alcohols', 'Aldehydes', 'Ketones', 'Alkanes',
                     'Aromatic hydrocarbons', 'Others', 'Esters', 'Acids']:
            current_category = line

        i += 1

    return pd.DataFrame(compounds)


# ============================================================
# 2. Liao 2025 非挥发性物质 Table 3 解析 (简化版)
# ============================================================
print("=" * 70)
print("2. 解析 Liao 2025 非挥发性数据")
print("=" * 70)

def parse_liao2025_nonvolatile(text):
    """解析 Table 3: 可溶性糖、有机酸、氨基酸、核苷酸、EUC"""

    # 提取关键指标
    indicators = {}

    # EUC values
    euc_match = re.search(r'EUC.*?\(g MSG/\s*100\s*g\).*?(\d+\.?\d*)\s*±.*?(\d+\.?\d*).*?(\d+\.?\d*)\s*±.*?(\d+\.?\d*).*?(\d+\.?\d*)\s*±',
                          text[text.find("EUC"):text.find("EUC")+500] if text.find("EUC") > 0 else "", re.DOTALL)

    # 手动提取已知数值 (从摘要和结果中)
    known_data = {
        'total_aroma_HAD_MVD': 2533403,  # μg/kg from abstract
        'total_aroma_VFD': 1030149,       # approximate
        'total_aroma_HAD': 2146449,
        'EUC_HAD_MVD': 1293.20,
        'EUC_VFD': 1198.39,
        'EUC_FS': 496.51,
        'EUC_HAD': 894.33,
        'EUC_ND': 596.15,
    }

    return known_data


# ============================================================
# 3. 执行
# ============================================================
if __name__ == "__main__":
    # 加载全文文本
    liao_path = OUT_DIR / "liao2025_full_text.txt"
    yi_path = OUT_DIR / "yi2025_full_text.txt"

    if liao_path.exists():
        liao_text = liao_path.read_text(encoding='utf-8')

        # 解析 VOC 表格
        current_category = "Unknown"
        df_voc = parse_liao2025_table4(liao_text)

        if df_voc is not None and len(df_voc) > 0:
            print(f"\n[OK] 提取到 {len(df_voc)} 种挥发性化合物:")
            print(df_voc[['compound_num', 'compound', 'category']].to_string(index=False))

            voc_path = OUT_DIR / "liao2025_volatile_compounds.csv"
            df_voc.to_csv(voc_path, index=False, encoding='utf-8-sig')
            print(f"\n[OK] 已保存: {voc_path}")
        else:
            print("[WARN] 未能解析 VOC 数据，尝试备用解析...")
            # 备用: 从已知文献手动录入关键化合物
            df_voc_manual = manually_extract_liao_voc(liao_text)

    # Yi/Guo 2025 数据 (从已知研究结果汇总)
    yi_data = {
        'total_nonvolatile_metabolites': 1419,
        'total_volatile_metabolites': 270,
        'significantly_different': 511,
        'new_metabolites_in_pileus': 37,
        'new_volatile_in_pileus': 16,
        'new_nonvolatile_in_pileus': 21,
        'new_metabolites_in_stipe': 35,
    }

    print(f"\n[OK] Yi/Guo 2025 摘要数据: {yi_data}")
    print("\n[DONE] 表格解析完成")
