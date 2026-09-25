# Product Master Mapping

## Overview
Mapping analysis for the `l2_masterdata_in_v1_product_master` dimension table (18 columns). This directory contains column-by-column analysis linking Mondelēz product master data from SAP and DATAL systems to the target SORSA schema.

## Files in This Directory

1. **column_mapping_product_master.csv** - Core mapping data with source candidates, scores, and rationale
2. **PRODUCT_MASTER_MAPPING_GUIDE.md** - Detailed column-by-column analysis with sample data and validation
3. **PRODUCT_MASTER_MAPPING_SUMMARY.md** - Executive summary with metrics, recommendations, and approval checklist
4. **README.md** (this file) - Quick start guide
5. **INDEX.md** - Navigation links between files

## Quick Start

### Primary Source
**t_dim_material** (SAP Material Master, AMEA region, 4.28M rows)
- Covers 18 columns including product codes, names, brands, and hierarchies
- Located in: `prd-amea-analyt-md-svc-7c.prd_amea_dc_md`

### Secondary Sources
- **v_cmdl_product_auom_fg_planningsku_amea** (DATAL) - EAN and weight
- **v_product_push_ma** (SORSA) - Morocco affordability metrics (80 rows)

### Morocco Filter
Requires region code filter via sales area or hardcoded region match. Expected output: **4,000-5,000 unique SKUs**.

## Key Mappings

| Target Column | Source | Confidence | Notes |
|---|---|---|---|
| mdlz_sku_code | t_dim_material.material_cd_nk | HIGH | SAP material number |
| product_name | t_dim_material.maktx | HIGH | Product description |
| brand_name | t_dim_material.brand | HIGH | Direct brand field |
| ean | t_dim_material.international_article_nm | HIGH | Barcode (62-70% coverage) |
| affordability | v_product_push_ma.msl | MEDIUM | Morocco-only (80 rows) |

## Methodology
- **Scoring Formula:** (0.4 × Name Similarity) + (0.6 × Value Match)
- **Confidence Levels:** HIGH >0.85, MEDIUM 0.5-0.85, LOW <0.5
- **High Confidence:** 13 columns (72%)
- **Medium Confidence:** 5 columns (28%) - mostly variant/packsize data

## Recommendations
1. Use SAP t_dim_material as primary source
2. Confirm region filter for Morocco
3. Address variant data (NULL or derive from hierarchy)
4. Test EAN coverage
5. Validate weight units

See **PRODUCT_MASTER_MAPPING_SUMMARY.md** for approval checklist and next steps.
