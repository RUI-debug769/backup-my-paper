#!/usr/bin/env python3
"""
MVE v2 — 多策略 PDF 表格提取管线
=================================
PDF Router → Extractor Stack → Table Validator → Quality Score → Decision

策略栈 (按优先级):
  1. pdfplumber  — Digital PDF，速度快，准确度高
  2. PyMuPDF     — 通用性强，无需模型
  3. Camelot     — 专攻表格，lattice/stream 双模式
  4. magic-pdf   — 复杂 layout，OCR 兜底

Quality Gate:
  ≥95 → Accept
  80-94 → Human Review (flag)
  <80 → Retry with next extractor
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import json
import time
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
import pandas as pd
import numpy as np

OUT_DIR = Path(__file__).parent

# ============================================================
# Data structures
# ============================================================
@dataclass
class TableQuality:
    """表格提取质量评估"""
    completeness: float      # 单元格填充率
    row_col_consistency: float  # 行列一致性
    missing_cell_rate: float    # 缺失率
    numeric_rate: float         # 数值识别率
    overall_score: float        # 综合评分

    def verdict(self) -> str:
        if self.overall_score >= 95:
            return "ACCEPT"
        elif self.overall_score >= 80:
            return "REVIEW"
        else:
            return "RETRY"

@dataclass
class ExtractionResult:
    extractor: str
    tables: List[pd.DataFrame]
    quality: TableQuality
    elapsed_ms: float
    error: Optional[str] = None

# ============================================================
# Quality Validator
# ============================================================
class TableValidator:
    """评估表格提取质量"""

    @staticmethod
    def assess(df: pd.DataFrame) -> TableQuality:
        if df is None or df.empty:
            return TableQuality(0, 0, 1.0, 0, 0)

        total_cells = df.size
        missing = df.isna().sum().sum() + (df == '').sum().sum()
        missing_rate = missing / max(total_cells, 1)

        # 数值识别率
        numeric_cells = 0
        for col in df.columns:
            try:
                numeric_cells += pd.to_numeric(df[col], errors='coerce').notna().sum()
            except:
                pass
        numeric_rate = numeric_cells / max(total_cells, 1)

        # 行列一致性: 检查每行/列是否有相似的单元格数
        row_lengths = [len(df.iloc[i].dropna()) for i in range(len(df))]
        row_consistency = 1.0 - (np.std(row_lengths) / max(np.mean(row_lengths), 1)) if len(row_lengths) > 1 else 0.5
        row_consistency = max(0, min(1, row_consistency))

        completeness = 1.0 - missing_rate

        # 综合评分 (加权)
        score = (
            completeness * 40 +
            row_consistency * 25 +
            (1 - missing_rate) * 20 +
            numeric_rate * 15
        )
        score = min(100, score)

        return TableQuality(
            completeness=round(completeness * 100, 1),
            row_col_consistency=round(row_consistency * 100, 1),
            missing_cell_rate=round(missing_rate * 100, 1),
            numeric_rate=round(numeric_rate * 100, 1),
            overall_score=round(score, 1)
        )

# ============================================================
# PDF Router
# ============================================================
class PDFRouter:
    """根据 PDF 特征选择最优提取策略"""

    @staticmethod
    def classify(pdf_path: Path) -> str:
        """
        返回 PDF 类型: 'digital', 'scanned', 'mixed'
        """
        import fitz
        doc = fitz.open(str(pdf_path))
        total_chars = 0
        total_images = 0

        for page in doc:
            text = page.get_text()
            total_chars += len(text)
            images = page.get_images()
            total_images += len(images)

        page_count = doc.page_count
        doc.close()

        chars_per_page = total_chars / max(page_count, 1)
        images_per_page = total_images / max(page_count, 1)

        if chars_per_page > 500 and images_per_page < 3:
            return 'digital'
        elif chars_per_page < 100 and images_per_page > 3:
            return 'scanned'
        else:
            return 'mixed'

# ============================================================
# Extractor Stack
# ============================================================
class ExtractorStack:
    """多策略提取器"""

    def __init__(self, pdf_path: Path):
        self.pdf_path = pdf_path
        self.validator = TableValidator()
        self.results: List[ExtractionResult] = []

    def _try_pdfplumber(self, pages: Optional[List[int]] = None) -> ExtractionResult:
        """策略1: pdfplumber — 最佳 digital PDF 表格提取"""
        t0 = time.time()
        try:
            import pdfplumber
            tables = []
            with pdfplumber.open(str(self.pdf_path)) as pdf:
                target_pages = pages or range(len(pdf.pages))
                for page_num in target_pages:
                    if page_num >= len(pdf.pages):
                        break
                    page = pdf.pages[page_num]
                    page_tables = page.extract_tables()
                    for t in page_tables:
                        if t and len(t) > 1:
                            df = pd.DataFrame(t[1:], columns=t[0] if t[0] else None)
                            tables.append(df)

            if tables:
                quality = self.validator.assess(tables[0])
                elapsed = (time.time() - t0) * 1000
                return ExtractionResult('pdfplumber', tables, quality, elapsed)
            else:
                return ExtractionResult('pdfplumber', [], TableQuality(0,0,100,0,0), (time.time()-t0)*1000, "No tables found")
        except ImportError:
            return ExtractionResult('pdfplumber', [], TableQuality(0,0,100,0,0), 0, "pdfplumber not installed")
        except Exception as e:
            return ExtractionResult('pdfplumber', [], TableQuality(0,0,100,0,0), (time.time()-t0)*1000, str(e))

    def _try_pymupdf(self, pages: Optional[List[int]] = None) -> ExtractionResult:
        """策略2: PyMuPDF — 通用文本提取"""
        t0 = time.time()
        try:
            import fitz
            doc = fitz.open(str(self.pdf_path))
            tables = []

            target_pages = pages or range(doc.page_count)
            for page_num in target_pages:
                if page_num >= doc.page_count:
                    break
                page = doc[page_num]

                # 尝试内置 table detection (PyMuPDF >= 1.23)
                try:
                    page_tables = page.find_tables()
                    if page_tables and page_tables.tables:
                        for t in page_tables.tables:
                            df = pd.DataFrame(t.extract())
                            tables.append(df)
                except (AttributeError, NotImplementedError):
                    pass

                # Fallback: block-based extraction
                if not tables:
                    blocks = page.get_text("blocks")
                    # 简单分组: 相近 y 坐标的 block 视为同一行
                    rows = {}
                    for b in blocks:
                        y_key = round(b[1] / 20) * 20  # 20px tolerance
                        if y_key not in rows:
                            rows[y_key] = []
                        rows[y_key].append(b[4].strip())

                    if len(rows) > 3:
                        row_data = [rows[k] for k in sorted(rows.keys())]
                        # 转 DataFrame
                        max_cols = max(len(r) for r in row_data)
                        padded = [r + [''] * (max_cols - len(r)) for r in row_data]
                        df = pd.DataFrame(padded)
                        tables.append(df)

            doc.close()

            if tables:
                quality = self.validator.assess(tables[0])
                elapsed = (time.time() - t0) * 1000
                return ExtractionResult('PyMuPDF', tables, quality, elapsed)
            else:
                return ExtractionResult('PyMuPDF', [], TableQuality(0,0,100,0,0), (time.time()-t0)*1000, "No tables found")
        except Exception as e:
            return ExtractionResult('PyMuPDF', [], TableQuality(0,0,100,0,0), (time.time()-t0)*1000, str(e))

    def _try_camelot(self, pages: str = 'all') -> ExtractionResult:
        """策略3: Camelot — 专业表格提取 (lattice + stream)"""
        t0 = time.time()
        try:
            import camelot
            tables = []

            # Lattice mode (bordered tables)
            try:
                lattice_tables = camelot.read_pdf(str(self.pdf_path), pages=pages, flavor='lattice')
                for t in lattice_tables:
                    tables.append(t.df)
            except:
                pass

            # Stream mode (borderless tables)
            if not tables:
                try:
                    stream_tables = camelot.read_pdf(str(self.pdf_path), pages=pages, flavor='stream')
                    for t in stream_tables:
                        tables.append(t.df)
                except:
                    pass

            if tables:
                quality = self.validator.assess(tables[0])
                elapsed = (time.time() - t0) * 1000
                return ExtractionResult('Camelot', tables, quality, elapsed)
            else:
                return ExtractionResult('Camelot', [], TableQuality(0,0,100,0,0), (time.time()-t0)*1000, "No tables found")
        except ImportError:
            return ExtractionResult('Camelot', [], TableQuality(0,0,100,0,0), 0, "Camelot not installed")
        except Exception as e:
            return ExtractionResult('Camelot', [], TableQuality(0,0,100,0,0), (time.time()-t0)*1000, str(e))

    def extract(self, target_pages: Optional[List[int]] = None,
                max_strategies: int = 3) -> ExtractionResult:
        """
        按优先级尝试提取，直到质量达标或策略耗尽
        """
        pdf_type = PDFRouter.classify(self.pdf_path)
        print(f"  PDF 类型: {pdf_type}")

        # 策略栈 (按优先级)
        stack = [
            ('pdfplumber', lambda: self._try_pdfplumber(target_pages)),
            ('PyMuPDF',   lambda: self._try_pymupdf(target_pages)),
            ('Camelot',   lambda: self._try_camelot()),
        ]

        best_result = None
        for name, extractor_fn in stack[:max_strategies]:
            print(f"  → 尝试 {name}...")
            result = extractor_fn()

            if result.error:
                print(f"    ⚠️ {name}: {result.error}")
                self.results.append(result)
                continue

            if not result.tables:
                print(f"    ⚠️ {name}: 未找到表格")
                self.results.append(result)
                continue

            q = result.quality
            verdict = q.verdict()
            print(f"    {name}: Score={q.overall_score} | "
                  f"完整率={q.completeness}% | "
                  f"缺失率={q.missing_cell_rate}% | "
                  f"判定={verdict} | "
                  f"耗时={result.elapsed_ms:.0f}ms")

            self.results.append(result)

            if verdict == "ACCEPT":
                print(f"    ✅ {name} 达标，停止尝试")
                return result

            if best_result is None or result.quality.overall_score > best_result.quality.overall_score:
                best_result = result

        # 返回最佳结果
        if best_result:
            print(f"  → 返回最佳: {best_result.extractor} (Score={best_result.quality.overall_score})")
        return best_result

# ============================================================
# 执行
# ============================================================
if __name__ == "__main__":
    print("=" * 70)
    print("MVE v2 — 多策略 PDF 提取管线测试")
    print("=" * 70)

    # Test: Liao 2025
    pdf_path = Path(r"D:\Zotero\Data\storage\5A2698N2\Liao 等 - 2025 - Comparison of different drying processes of morchella sextelata changes in volatile and non-volatil.pdf")

    if pdf_path.exists():
        stack = ExtractorStack(pdf_path)
        result = stack.extract(target_pages=[6, 7])  # Pages 7-8 (Table 4)

        if result and result.tables:
            for i, df in enumerate(result.tables):
                print(f"\n--- Table {i+1} ({result.extractor}) ---")
                print(df.head(10).to_string())
                csv_path = OUT_DIR / f"liao2025_table{i+1}_{result.extractor}.csv"
                df.to_csv(csv_path, index=False, encoding='utf-8-sig')
                print(f"[OK] 已保存: {csv_path}")

        # 输出所有策略对比
        print("\n--- 策略对比 ---")
        for r in stack.results:
            print(f"  {r.extractor:15s} Score={r.quality.overall_score:5.1f} "
                  f"Tables={len(r.tables):2d} Time={r.elapsed_ms:6.0f}ms "
                  f"{'⚠️ '+r.error if r.error else ''}")
    else:
        print(f"[ERROR] PDF 不存在: {pdf_path}")

    print("\n[DONE]")
