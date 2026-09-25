# POI_MASTER_MAPPING_SUMMARY

## Executive Summary
- **Total Target Columns:** 7
- **Mapped Columns:** 7 (100%)
- **Unmapped Columns:** 0

## Confidence Distribution
| Level | Count | Percentage |
|-------|-------|-----------|
| HIGH | 7 | 100% |
| MEDIUM | 0 | 0% |
| LOW | 0 | 0% |

**Average Combined Score:** 0.945

## Primary Source Identified
**v_manual_poi_ma** (SORSA Manual POI Master)
- Project: `dev-amea-analyt-sorsa-svc-38`
- Dataset: `dev_amea_p_ds_product_specific`
- Rows: 18,514 (100% Morocco)
- Columns: 24
- Coverage: **100% Morocco** - No filtering required
- Filter: **country_code_nk = 'MA'** (all rows already Morocco)

## Secondary Source
**v_dim_store** (DISO Store Dimension)
- Project: `prd-amea-analyt-diso-svc-7f`
- Rows: 43,324 (multi-country)
- Alternative for coordinates/naming
- Requires filtering: `country_cd_nk='MA'` AND `channel_code_nk='rt'`

## Morocco Filtering Strategy

### Primary Filter
- **No filter needed:** v_manual_poi_ma contains 100% Morocco POI data
- **Confirmation:** All records have country_code_nk='MA'
- **Strategy:** Use v_manual_poi_ma directly without filtering

### Data Characteristics
- **100% Complete Coverage:** All 18,514 POI records are Morocco retail stores
- **Coordinates:** 100% non-null for latitude/longitude (store_latitude, store_longitude)
- **Store Names:** 79.87% non-null (4,249 NULLs in 18,514)
- **Categories:** 100% non-null (main_category_name and sub_categ_name)

## Mapped Columns Detail

| # | Target Column | Primary Source | Secondary | Confidence | Coverage |
|---|---|---|---|---|---|
| 1 | poi_sok | v_manual_poi_ma.poi_sk | v_dim_store.store_sk | HIGH | 100% |
| 2 | country_iso_code | v_manual_poi_ma.country_code_nk | hardcoded 'MA' | HIGH | 100% |
| 3 | poi_code | v_manual_poi_ma.poi_sk | v_dim_store.store_code_nk | HIGH | 100% |
| 4 | poi_name | v_manual_poi_ma.store_name | v_dim_store names | HIGH | 80% |
| 5 | poi_type_name | v_manual_poi_ma.main_category_name | sub_categ_name | HIGH | 100% |
| 6 | latitude | v_manual_poi_ma.store_latitude | v_dim_store.store_latitude | HIGH | 100% |
| 7 | longitude | v_manual_poi_ma.store_longitude | v_dim_store.store_longitude | HIGH | 100% |

## Key Data Characteristics

### Data Quality
- **NULL Handling:** Only poi_name has 20% NULLs (4,249 records)
- **Coordinates:** 100% populated (18,514 records with valid lat/lon)
- **Categories:** Complete (100% non-null)
- **Duplicates:** poi_sk is unique key (no duplicates expected)

### Coverage Analysis
| Column | Non-Null Count | Null Count | % Non-Null |
|--------|---|---|---|
| poi_sk | 18,514 | 0 | 100% |
| country_code_nk | 18,514 | 0 | 100% |
| store_name | 14,265 | 4,249 | 79.87% |
| main_category_name | 18,514 | 0 | 100% |
| store_latitude | 18,514 | 0 | 100% |
| store_longitude | 18,514 | 0 | 100% |

### Category Distribution
POI Type Categories (main_category_name):
- Modern Trade (Supermarket, hypermarket, etc.)
- Traditional Trade (Local stores, kiosks, etc.)
- On-premise (Bars, restaurants, hotels)
- Other (Pharmacies, gas stations, etc.)

## Recommendations

### Approval Checklist
- [ ] Confirm v_manual_poi_ma as sole primary source
- [ ] Accept 80% store_name coverage (20% NULL acceptable)
- [ ] Verify coordinate precision (lat/lon decimal places)
- [ ] Confirm POI category hierarchy matches target classification
- [ ] Accept 100% coverage for geographic coordinates
- [ ] Validate poi_sk uniqueness in source

### Next Steps
1. **Phase 2 - Data Validation:** Review sample of 1% (185 POIs)
2. **Phase 3 - SQL Development:** Build simple extraction (no complex joins)
3. **Phase 4 - QA:** Validate against v_dim_store (for reconciliation)

## Technical Details
- **Expected Output:** 18,514 POI records (100% of source)
- **Processing Time:** <1 second (small dimension table)
- **Estimated Bytes Scanned:** <50MB
- **Join complexity:** Minimal (self-contained table)
- **Data freshness:** Updated via manual upload pipeline (SORSA dev)

## Important Notes
- **Unique Reference:** v_manual_poi_ma is Morocco-exclusive system
- **Completeness:** Provides 100% POI coverage for Morocco retail
- **Reliability:** Manual data entry (expect data quality review)
- **Coordinates:** Critical for geo-analytics and visualization
