#!/usr/bin/env python3
"""
MVE v2 — 直接从 PDF 提取表格数据（pymupdf 引擎）
目标论文: Liao 2025 (Food Chemistry: X), Yi/Guo 2025 (Food Science & Nutrition)
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import fitz  # pymupdf
import re
import pandas as pd
import numpy as np
from pathlib import Path

OUT_DIR = Path(__file__).parent
OUT_DIR.mkdir(parents=True, exist_ok=True)

# PDF 路径
import platform
if platform.system() == "Windows":
    PDF_LIAO = Path(r"D:\Zotero\Data\storage\5A2698N2\Liao 等 - 2025 - Comparison of different drying processes of morchella sextelata changes in volatile and non-volatil.pdf")
    PDF_YI = Path(r"D:\Zotero\Data\storage\QSD8SH79\Yi 等 - 2025 - Widely targeted metabolomics of Morchella Sextelata after hot-air drying.pdf")
else:
    PDF_LIAO = Path("/mnt/d/Zotero/Data/storage/5A2698N2/Liao 等 - 2025 - Comparison of different drying processes of morchella sextelata changes in volatile and non-volatil.pdf")
    PDF_YI = Path("/mnt/d/Zotero/Data/storage/QSD8SH79/Yi 等 - 2025 - Widely targeted metabolomics of Morchella Sextelata after hot-air drying.pdf")

# ============================================================
# 1. Liao 2025 — 提取 VOC 表格数据
# ============================================================
print("=" * 70)
print("1. Liao 2025 — 提取 VOC 数据")
print("=" * 70)

def extract_liao2025_tables(pdf_path):
    """提取 Liao 2025 的所有页面文本，定位并解析表格"""
    doc = fitz.open(str(pdf_path))
    print(f"  总页数: {doc.page_count}")

    # 提取所有页面文本
    all_text = []
    for page_num in range(doc.page_count):
        page = doc[page_num]
        text = page.get_text("text")
        all_text.append(f"=== PAGE {page_num + 1} ===\n{text}")

    full_text = "\n".join(all_text)

    # 保存完整文本
    text_path = OUT_DIR / "liao2025_full_text.txt"
    text_path.write_text(full_text, encoding='utf-8')
    print(f"  [OK] 全文已保存: {text_path} ({len(full_text)} 字符)")

    # 搜索表格关键词
    for keyword in ["Table 1", "Table 2", "Table 3", "Table 4", "Table 5",
                    "volatile", "VOC", "aroma", "μg/kg", "mg/100",
                    "HAD", "VFD", "HAD-MVD", "ND"]:
        count = full_text.count(keyword)
        if count > 0:
            print(f"  '{keyword}' 出现 {count} 次")

    # 查找挥发性物质表格 (通常在 §3.3-3.5)
    # 搜索 "Table" 附近的文本
    table_positions = []
    for m in re.finditer(r'Table\s+(\d+)', full_text):
        start = max(0, m.start() - 50)
        end = min(len(full_text), m.end() + 200)
        context = full_text[start:end].replace('\n', ' ')
        table_positions.append({
            'table_num': m.group(1),
            'position': m.start(),
            'context': context[:200]
        })

    for tp in table_positions:
        print(f"\n  Table {tp['table_num']} (pos {tp['position']}):")
        print(f"    {tp['context']}...")

    doc.close()
    return full_text

liao_text = extract_liao2025_tables(PDF_LIAO)

# ============================================================
# 2. Yi/Guo 2025 — 提取挥发物+代谢物表格数据
# ============================================================
print("\n" + "=" * 70)
print("2. Yi/Guo 2025 — 提取挥发物 + 代谢物数据")
print("=" * 70)

def extract_yi2025_tables(pdf_path):
    """提取 Yi/Guo 2025 表格数据"""
    doc = fitz.open(str(pdf_path))
    print(f"  总页数: {doc.page_count}")

    all_text = []
    for page_num in range(doc.page_count):
        page = doc[page_num]
        text = page.get_text("text")
        all_text.append(f"=== PAGE {page_num + 1} ===\n{text}")

    full_text = "\n".join(all_text)

    text_path = OUT_DIR / "yi2025_full_text.txt"
    text_path.write_text(full_text, encoding='utf-8')
    print(f"  [OK] 全文已保存: {text_path} ({len(full_text)} 字符)")

    # 搜索关键数据
    for keyword in ["Table", "volatile", "metabolite", "VIP", "fold change",
                    "GC-MS", "UHPLC", "up-regulated", "down-regulated",
                    "pileus", "stipe"]:
        count = full_text.count(keyword)
        if count > 0:
            print(f"  '{keyword}' 出现 {count} 次")

    # 查找 Table 位置
    for m in re.finditer(r'Table\s+(\d+)', full_text):
        start = max(0, m.start() - 50)
        end = min(len(full_text), m.end() + 200)
        context = full_text[start:end].replace('\n', ' ')
        print(f"\n  Table {m.group(1)} (pos {m.start()}):")
        print(f"    {context[:200]}...")

    doc.close()
    return full_text

yi_text = extract_yi2025_tables(PDF_YI)

print("\n[DONE] 文本提取完成。请查看输出文件以定位表格位置。")
