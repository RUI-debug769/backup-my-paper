#!/usr/bin/env python3
"""
MVE v2 — Liao 2025 VOC 数据手动录入 + Yi/Guo 2025 摘要统计
策略: PDF文本解析不稳定, 直接用pymupdf读取table区域 + 手工校验
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import fitz
import pandas as pd
from pathlib import Path

OUT_DIR = Path(__file__).parent
PDF_LIAO = Path(r"D:\Zotero\Data\storage\5A2698N2\Liao 等 - 2025 - Comparison of different drying processes of morchella sextelata changes in volatile and non-volatil.pdf")

def extract_table_blocks():
    """使用 pymupdf 提取 Table 4 所在页面(Page 7)的文本块"""
    doc = fitz.open(str(PDF_LIAO))
    page = doc[6]  # Page 7 (0-indexed)

    blocks = page.get_text("blocks")
    print(f"Page 7: {len(blocks)} text blocks")

    for i, block in enumerate(blocks):
        x0, y0, x1, y1, text, block_type, block_no = block
        text_clean = text.strip()[:120]
        if len(text_clean) > 10:
            print(f"  Block {i}: y={y0:.0f}-{y1:.0f}, type={block_type}: {text_clean}...")

    doc.close()

def extract_table_blocks_p8():
    """Page 8 (continued table)"""
    doc = fitz.open(str(PDF_LIAO))
    page = doc[7]  # Page 8 (0-indexed)

    blocks = page.get_text("blocks")
    print(f"\nPage 8: {len(blocks)} text blocks")

    for i, block in enumerate(blocks):
        x0, y0, x1, y1, text, block_type, block_no = block
        text_clean = text.strip()[:120]
        if len(text_clean) > 5:
            print(f"  Block {i}: y={y0:.0f}-{y1:.0f}: {text_clean}...")

    doc.close()

if __name__ == "__main__":
    extract_table_blocks()
    extract_table_blocks_p8()
