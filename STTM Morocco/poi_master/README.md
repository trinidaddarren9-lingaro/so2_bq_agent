# POI Master Mapping

## Overview
Mapping analysis for the `l2_masterdata_in_v1_poi_master` dimension table (7 columns). This directory contains analysis linking Morocco point-of-interest (outlet) data from the manual POI master to the target SORSA schema.

## Files in This Directory

1. **column_mapping_poi_master.csv** - Core mapping data with source candidates, scores, and rationale
2. **POI_MASTER_MAPPING_GUIDE.md** - Detailed column-by-column analysis with sample data and validation
3. **POI_MASTER_MAPPING_SUMMARY.md** - Executive summary with metrics, recommendations, and approval checklist
4. **README.md** (this file) - Quick start guide
5. **INDEX.md** - Navigation links between files

## Quick Start

### Primary Source
**v_manual_poi_ma** (SORSA Manual POI Master, 18,514 rows)
- Morocco-exclusive point-of-interest/outlet directory
- 100% Morocco coverage - **NO FILTERING REQUIRED**
- Located in: `dev-amea-analyt-sorsa-svc-38.dev_amea_p_ds_product_specific`

### Secondary Source (for reconciliation only)
**v_dim_store** (43,324 rows) - Alternative store references from DISO

## Morocco Filter
**No filter required** - v_manual_poi_ma contains exclusively Morocco data (all 18,514 records). Expected output: **18,514 unique POIs**.

## Key Mappings

| Target Column | Source | Confidence | Coverage |
|---|---|---|---|
| poi_sok | v_manual_poi_ma.poi_sk | HIGH | 100% |
| country_iso_code | v_manual_poi_ma.country_code_nk | HIGH | 100% ('MA') |
| poi_code | v_manual_poi_ma.poi_sk | HIGH | 100% |
| poi_name | v_manual_poi_ma.store_name | HIGH | 80% |
| poi_type_name | v_manual_poi_ma.main_category_name | HIGH | 100% |
| latitude | v_manual_poi_ma.store_latitude | HIGH | 100% |
| longitude | v_manual_poi_ma.store_longitude | HIGH | 100% |

## Methodology
- **Scoring Formula:** (0.4 × Name Similarity) + (0.6 × Value Match)
- **Confidence Levels:** HIGH >0.85, MEDIUM 0.5-0.85, LOW <0.5
- **High Confidence:** 7 columns (100%)

## Data Characteristics
- **Total rows:** 18,514 (all Morocco)
- **Coordinates:** 100% populated (lat/lon pairs)
- **Store names:** 80% populated (4,249 NULLs in 18,514)
- **Categories:** 100% populated (retail type classification)
- **Uniqueness:** poi_sk is unique key

## Key Data Notes
- ✅ **100% geo-coverage** - All POIs have coordinates
- ✅ **Complete category data** - All outlets classified by type
- ✅ **Morocco-only system** - No filtering logic needed
- ⚠️ **20% name NULLs** - Some outlets lack store names (acceptable)

## Recommendations
1. Accept v_manual_poi_ma as sole source
2. Accept 80% store_name coverage (20% NULLs tolerable)
3. Use 100% coordinate coverage for geo-analytics
4. Validate category hierarchy meets business needs
5. Plan for coordinate precision validation

See **POI_MASTER_MAPPING_SUMMARY.md** for approval checklist and next steps.
