# Invoice Line Item Mapping - File Index

## Navigation Guide

### 📋 Files in This Directory

| File | Type | Purpose | Key Content |
|------|------|---------|---|
| **column_mapping_invoice_line_item.csv** | CSV Data | Core mapping with source candidates | 12 target columns, source options (v_fct_distributor_invoice_line_item primary), scoring, confidence |
| **README.md** | Documentation | Quick start guide | Overview, primary/secondary sources, Morocco RT filter, expected output (5-10M rows), key mappings |
| **INDEX.md** | Navigation | This file - links all documents | File descriptions, navigation shortcuts, content summary, usage tips |
| **INVOICE_LINE_ITEM_MAPPING_GUIDE.md** | Documentation | Detailed column analysis | Per-column breakdown with sample values, type validation, NULL handling, data quality notes |
| **INVOICE_LINE_ITEM_MAPPING_SUMMARY.md** | Documentation | Executive summary & approval | Confidence metrics (92% HIGH), volume estimates, approval checklist, performance considerations |

## Quick Navigation

### For Business Users
1. Start with **README.md** (2-minute overview)
2. Review **INVOICE_LINE_ITEM_MAPPING_SUMMARY.md** (approval checklist, data volume)
3. Check **INVOICE_LINE_ITEM_MAPPING_GUIDE.md** for detailed validation

### For Data Engineers
1. Open **column_mapping_invoice_line_item.csv** (scoring and business logic)
2. Review **INVOICE_LINE_ITEM_MAPPING_GUIDE.md** (data quality and NULL handling)
3. Consult **INVOICE_LINE_ITEM_MAPPING_SUMMARY.md** (performance and filtering strategy)

### For Data Analysts
1. **INVOICE_LINE_ITEM_MAPPING_SUMMARY.md** (volume, coverage, quality metrics)
2. **INVOICE_LINE_ITEM_MAPPING_GUIDE.md** (NULL distributions, data samples)
3. **column_mapping_invoice_line_item.csv** (candidate sources ranked by score)

## Content Summary

### column_mapping_invoice_line_item.csv
- **Structure:** CSV with 14 rows (12 columns + 1 header + 1 SUMMARY)
- **Columns:** source_column, target_candidates, name_similarity_score, value_match_score, combined_score, reasons, selected_target, confidence, decision
- **Score Range:** 0.0-1.0 (higher = better match)
- **Confidence:** HIGH (>0.85), MEDIUM (0.5-0.85), LOW (<0.5)

### INVOICE_LINE_ITEM_MAPPING_GUIDE.md
- **Column details:** Types (STRING, DATE, FLOAT64), sample values, validation rules
- **NULL handling:** Coverage percentages (95-100% for most, 95% for net_value)
- **Type validation:** Compatibility checks between source and target
- **Morocco filter impact:** Volume reduction from 16.2M to 5-10M rows (30-60%)

### INVOICE_LINE_ITEM_MAPPING_SUMMARY.md
- **Metrics:** 12 total columns, 12 mapped (100%), HIGH confidence: 11 (92%), MEDIUM: 1 (8%)
- **Primary source:** v_fct_distributor_invoice_line_item (DISO fact, 16.2M rows)
- **Secondary sources:** v_dim_store (outlets), v_uom_ma (unit conversions)
- **Filter logic:** country_code_nk='MA' AND channel_code_nk='rt'
- **Performance:** ~30-60 seconds, 2-3GB scanned, 3-table join complexity
- **Approval items:** 7-item checklist for stakeholder validation

### README.md
- **Overview:** Fact table purpose and schema context
- **Quick start:** Source tables and Morocco retail filter
- **Volume estimates:** 5-10M invoice lines (30-60% of 16.2M total)
- **Key mappings:** 8 core columns with confidence levels
- **Recommendations:** Validation and QA checkpoints

## Data Characteristics

| Aspect | Details |
|--------|---------|
| **Target Table** | l2_fact_in_v1_invoice_line (12 columns) |
| **Primary Source** | v_fct_distributor_invoice_line_item (16.2M rows, DISO fact) |
| **Morocco Output** | 5-10 million invoice lines (30-60% of total) |
| **High Confidence** | 11 columns (92%) |
| **Medium Confidence** | 1 column (8%) - order_number |
| **Unmapped Columns** | 0 |
| **Average Score** | 0.915 |
| **Key Filter** | country_code_nk='MA' AND channel_code_nk='rt' |
| **Estimated Scan** | 2-3 GB (DISO production volume) |

## Key Mappings Summary

**Tier 1 - Highest Confidence (>0.95):**
- invoice_line_sok → distributor_invoice_line_sk (0.95)
- invoice_number → distributor_invoice_code_nk (0.97)
- invoice_date → distributor_invoice_date_code_nk (0.97)
- outlet_sok → store_sk (0.925)
- product_sok → product_sk (0.95)
- uom_qty → distributor_invoice_line_qty_cases (0.95)
- gross_value → distributor_invoice_gross_sales_amt (0.97)
- net_value → distributor_invoice_net_sales_amt (0.97)

**Tier 2 - Medium Confidence (0.85-0.95):**
- order_number → sales_rep_id (0.835, MEDIUM)

## NULL and Data Quality

| Column | Coverage | NULL Count | Notes |
|--------|----------|---|---|
| invoice_line_sok | 100% | 0 | Primary key, always populated |
| distributor_invoice_code_nk | 100% | 0 | Invoice identifier |
| net_value | 95% | 805K/16M | Acceptable NULL rate |
| sales_rep_id (order_number) | 95% | 800K+ | Fallback available |
| Other columns | 95-100% | <5% | High quality data |

## Usage Tips

- **CSV Import:** UTF-8 encoding, pipe (|) delimiter for candidate lists
- **Filter effectiveness:** country_code_nk='MA' + channel='rt' reduces from 16.2M to 5-10M (~40-60% reduction)
- **NULL handling:** 5% NULLs in net_value acceptable for reporting; use gross_value as fallback
- **Date range:** Configurable via distributor_invoice_date_code_nk (recommend post-2024-01-01)
- **Performance:** Test on sample (<5% of table) before full scan

## Related Files
- Parent directory: `/STTM Morocco/`
- Sibling directories: `/product_master/`, `/poi_master/`
- Source schema reference: `/docs/bigquery/sttm-morocco/sttm_morocco_schema.csv`
- MCP routing: `/docs/bigquery/mcp-servers.md`
