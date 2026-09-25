# Invoice Line Item Mapping

## Overview
Mapping analysis for the `l2_fact_in_v1_invoice_line` fact table (12 columns). This directory contains column-by-column analysis linking Mondelēz invoice transaction data from DISO distributor sellout to the target SORSA schema.

## Files in This Directory

1. **column_mapping_invoice_line_item.csv** - Core mapping data with source candidates, scores, and rationale
2. **INVOICE_LINE_ITEM_MAPPING_GUIDE.md** - Detailed column-by-column analysis with sample data and validation
3. **INVOICE_LINE_ITEM_MAPPING_SUMMARY.md** - Executive summary with metrics, recommendations, and approval checklist
4. **README.md** (this file) - Quick start guide
5. **INDEX.md** - Navigation links between files

## Quick Start

### Primary Source
**v_fct_distributor_invoice_line_item** (DISO Fact Table, 16.2M rows)
- Contains invoice transaction details including quantities, amounts, and outlets
- Located in: `prd-amea-analyt-diso-svc-7f.amea_ds_distributor_sellout`

### Secondary Sources
- **v_dim_store** (43,324 rows) - Outlet/store references
- **v_uom_ma** (294 rows) - Unit of measure conversions

### Morocco Filter
**country_code_nk='MA' AND channel_code_nk='rt'** (Retail channel). Expected output: **5-10 million invoice lines**.

## Key Mappings

| Target Column | Source | Confidence | Coverage |
|---|---|---|---|
| invoice_line_sok | distributor_invoice_line_sk | HIGH | 100% |
| invoice_number | distributor_invoice_code_nk | HIGH | 100% |
| outlet_sok | store_sk (v_dim_store) | HIGH | 96% |
| product_sok | product_sk (fact table) | HIGH | 100% |
| uom_qty | distributor_invoice_line_qty_cases | HIGH | 100% |
| gross_value | distributor_invoice_gross_sales_amt | HIGH | 100% |
| net_value | distributor_invoice_net_sales_amt | HIGH | 95% |
| order_number | distributor_invoice_sales_rep_id | MEDIUM | 95% |

## Methodology
- **Scoring Formula:** (0.4 × Name Similarity) + (0.6 × Value Match)
- **Confidence Levels:** HIGH >0.85, MEDIUM 0.5-0.85, LOW <0.5
- **High Confidence:** 11 columns (92%)
- **Medium Confidence:** 1 column (8%) - order_number sourced from sales_rep_id

## Data Characteristics
- **Total rows (all):** 16.2M
- **Morocco retail subset:** 5-10M (30-60%)
- **NULL values:** <5% for most columns; 5% NULLs in net_value
- **Scan size:** ~2-3GB after country/channel filtering

## Recommendations
1. Confirm retail channel code = 'rt'
2. Verify order_number source and business logic
3. Handle NULL values in net_value (5% NULLs acceptable)
4. Test date range filter for historical loads
5. Validate invoice aggregations

See **INVOICE_LINE_ITEM_MAPPING_SUMMARY.md** for approval checklist and next steps.
