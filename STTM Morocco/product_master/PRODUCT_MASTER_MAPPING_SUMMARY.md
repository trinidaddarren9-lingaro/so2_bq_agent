# PRODUCT_MASTER_MAPPING_SUMMARY

## Executive Summary
- **Total Target Columns:** 18
- **Mapped Columns:** 18 (100%)
- **Unmapped Columns:** 0

## Confidence Distribution
| Level | Count | Percentage |
|-------|-------|-----------|
| HIGH | 13 | 72% |
| MEDIUM | 5 | 28% |
| LOW | 0 | 0% |

**Average Combined Score:** 0.895

## Primary Source Identified
**t_dim_material** (SAP Material Master, AMEA Region)
- Project: `prd-amea-analyt-md-svc-7c`
- Dataset: `prd_amea_dc_md`
- Rows: 4,277,004
- Columns: 384+
- Coverage: ~100% for AMEA region
- Filter: `is_current='Y'` AND region matching

## Secondary Sources
1. **v_cmdl_product_auom_fg_planningsku_amea** (DATAL, 680,589 rows)
   - EAN/barcode data (ean11: 62% non-null)
   - Physical dimensions
   - UOM conversions

2. **v_product_push_ma** (SORSA dev, 80 rows)
   - Morocco-specific product push data
   - Affordability metrics (limited)

## Morocco Filtering Strategy

### Country Filter
- **Primary:** Region code via sales area join or hardcoded region match
- **Strategy:** Filter t_dim_material via region code or via JOIN to sales area table
- **Coverage:** Expected ~4-5K unique product SKUs for Morocco

### Data Quality Notes
- Variant data (variant_name, variant_sku, variant_weight_gram): **LIMITED** - recommend NULL or hierarchy-based derivation
- EAN coverage: 62-70% (non-null)
- Material hierarchy nullability: High (~93% nulls in some fields)
- Affordability data: Morocco-only (v_product_push_ma, 80 rows)

## Mapped Columns Detail

| # | Target Column | Primary Source | Secondary | Confidence | Notes |
|---|---|---|---|---|---|
| 1 | product_sok | Generated PK | - | HIGH | Surrogate key, new sequence |
| 2 | country_iso_code | Hardcoded | - | HIGH | Always 'MA' |
| 3 | mdlz_sku_code | t_dim_material.material_cd_nk | DATAL.matnr | HIGH | SAP material number |
| 4 | basecode | t_dim_material_salesarea.basecode_cd | t_dim_material | HIGH | Mdlz internal code |
| 5 | product_name | t_dim_material.maktx | DATAL.maktx | HIGH | SAP product description |
| 6 | variant_name | v_product_push_ma.description | - | MEDIUM | Limited (80 rows) |
| 7 | variant_sku | t_dim_material.international_article_nm | - | HIGH | EAN variant |
| 8 | variant_weight_gram | t_dim_material.net_weight_vl | DATAL.brgew | HIGH | Net weight grams |
| 9 | ean | t_dim_material.international_article_nm | DATAL.ean11 | HIGH | EAN/UPC barcode |
| 10 | packsize | v_cmdl_product_auom_fg_planningsku_amea.meabm | - | MEDIUM | Derived from UOM (11%) |
| 11 | affordability | v_product_push_ma.msl | - | MEDIUM | MSL proxy (80 rows) |
| 12 | ppg_code | t_dim_material.product_hierarchy_cd | salesarea | HIGH | Price/product group |
| 13 | subbrand_name | t_dim_material.brand | - | HIGH | SAP brand field |
| 14 | brand_name | t_dim_material.brand | - | HIGH | SAP brand field |
| 15 | subcategory_name | t_dim_material.material_group_3_cd | - | HIGH | Most specific category |
| 16 | category_name | t_dim_material.material_group_2_cd | - | HIGH | Mid-level category |
| 17 | subsegment_name | t_dim_material.division_cd | - | HIGH | Business subsegment |
| 18 | segment_name | t_dim_material.division_cd | - | HIGH | Business segment (unit) |

## Recommendations

### Approval Checklist
- [ ] Confirm SAP t_dim_material as primary source
- [ ] Verify region filter criteria for Morocco
- [ ] Decide on variant_name handling (NULL vs derivation)
- [ ] Confirm affordability metric (MSL vs alternative)
- [ ] Validate packsize lookup requirement
- [ ] Test EAN coverage against target requirements
- [ ] Confirm weight units and conversions

### Next Steps
1. **Phase 2 - Data Validation:** Sample 1% of Morocco-filtered data
2. **Phase 3 - SQL Development:** Build extraction query with all JOINs
3. **Phase 4 - QA:** Validate row counts, distinct values, NULL rates

## Technical Details
- **Expected Output:** 4,000-5,000 unique product records
- **Processing Time:** ~10-20 seconds (SAP table size)
- **Estimated Bytes Scanned:** 500MB-1GB (full table scan required, apply filters early)
