# Product Master Mapping - File Index

## Navigation Guide

### 📋 Files in This Directory

| File | Type | Purpose | Key Content |
|------|------|---------|---|
| **column_mapping_product_master.csv** | CSV Data | Core mapping with source candidates | 18 target columns, source options, scoring (0.0-1.0 scale), confidence levels, business reasoning |
| **README.md** | Documentation | Quick start guide | Overview, key mappings, primary/secondary sources, filter strategy, quick methodology |
| **INDEX.md** | Navigation | This file - links all documents | File descriptions, content summary, usage guide |
| **PRODUCT_MASTER_MAPPING_GUIDE.md** | Documentation | Detailed column analysis | Column-by-column breakdown with sample values, type matching, validation rules, coverage percentages |
| **PRODUCT_MASTER_MAPPING_SUMMARY.md** | Documentation | Executive summary & approval | Confidence distribution, primary source (t_dim_material), metrics, approval checklist, next steps |

## Quick Navigation

### For Business Users
1. Start with **README.md** (2-minute overview)
2. Review **PRODUCT_MASTER_MAPPING_SUMMARY.md** (approval checklist)
3. Check **PRODUCT_MASTER_MAPPING_GUIDE.md** for detailed column analysis

### For Data Engineers
1. Open **column_mapping_product_master.csv** (scoring and logic)
2. Review **PRODUCT_MASTER_MAPPING_GUIDE.md** (validation details)
3. Consult **PRODUCT_MASTER_MAPPING_SUMMARY.md** for performance notes

### For Data Analysts
1. **PRODUCT_MASTER_MAPPING_SUMMARY.md** (coverage and quality metrics)
2. **PRODUCT_MASTER_MAPPING_GUIDE.md** (sample data and distributions)
3. **column_mapping_product_master.csv** (full source options)

## Content Summary

### column_mapping_product_master.csv
- **Structure:** CSV with 20 rows (18 columns + 1 header + 1 SUMMARY)
- **Columns:** source_column, target_candidates, name_similarity_score, value_match_score, combined_score, reasons, selected_target, confidence, decision
- **Score Range:** 0.0-1.0 (higher = better match)
- **Confidence:** HIGH (>0.85), MEDIUM (0.5-0.85), LOW (<0.5)

### PRODUCT_MASTER_MAPPING_GUIDE.md
- **Per-column analysis:** name, type, sample values, source options
- **Validation logic:** Type checking, NULL rate analysis, format compatibility
- **Coverage notes:** Data availability percentages, quality flags
- **Morocco filters:** Region/country filtering requirements

### PRODUCT_MASTER_MAPPING_SUMMARY.md
- **Metrics:** Total columns (18), mapped (18), unmapped (0), confidence distribution
- **Primary source:** t_dim_material (SAP, 4.28M rows, AMEA region)
- **Secondary sources:** DATAL (680K rows), v_product_push_ma (80 rows)
- **Approval checklist:** 7 items for stakeholder sign-off
- **Next steps:** 4-phase roadmap to production implementation

### README.md
- **Overview:** Table purpose and schema context
- **Quick start:** Source tables, Morocco filter logic, expected output volume
- **Key mappings:** Top 5 columns with critical dependencies
- **Recommendations:** Action items for mapping validation

## Data Characteristics

| Aspect | Details |
|--------|---------|
| **Target Table** | l2_masterdata_in_v1_product_master (18 columns) |
| **Primary Source** | t_dim_material (4.28M rows, SAP AMEA) |
| **Morocco Output** | ~4,000-5,000 unique SKUs |
| **High Confidence** | 13 columns (72%) |
| **Medium Confidence** | 5 columns (28%) |
| **Unmapped Columns** | 0 |
| **Average Score** | 0.895 |

## Key Mappings Summary

**Tier 1 - Highest Confidence (>0.95):**
- product_name → t_dim_material.maktx (0.97)
- ean → t_dim_material.international_article_nm (0.955)
- brand_name → t_dim_material.brand (0.97)

**Tier 2 - High Confidence (0.85-0.95):**
- mdlz_sku_code, basecode, category_name, segment_name, etc.

**Tier 3 - Medium Confidence (0.70-0.85):**
- variant_name (0.775)
- packsize (0.70)
- affordability (0.865)

## Usage Tips

- **CSV Import:** Use UTF-8 encoding, pipe (|) delimiter for candidate lists
- **Scoring interpretation:** Combined score = (0.4 × name_sim) + (0.6 × value_match)
- **NULL handling:** Check coverage percentages in GUIDE; medians are safe fallbacks
- **Filter logic:** All Morocco queries must include region filter via sales area

## Related Files
- Parent directory: `/STTM Morocco/`
- Sibling directories: `/invoice_line_item/`, `/poi_master/`
- Source schema reference: `/docs/bigquery/sttm-morocco/sttm_morocco_schema.csv`
- MCP routing: `/docs/bigquery/mcp-servers.md`
