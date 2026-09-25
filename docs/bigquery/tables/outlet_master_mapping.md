# outlet_master — Schema Mapping Guide

**Target Schema:** outlet_master (L1/Data Warehouse layer)  
**Source Tables:** v_dim_store (primary), v_fct_distributor_invoice_line_item (enrichment)  
**Market Focus:** Morocco (MA)  
**Grain:** One row per outlet/store  
**Primary Key:** outlet_sok (Surrogate Object Key — hashed identifier)  
**Status:** Mapping Framework (Store & Invoice Tables Only)  

---

## Complete Column Mapping Table

| # | outlet_master Column | Data Type | NOT NULL | BigQuery Source | Source Column | Transformation | Coverage | Notes |
|----|----------------------|-----------|----------|-----------------|---------------|-----------------|----------|-------|
| 1 | `outlet_sok` | STRING | YES | Derived | N/A | SHA256(country_iso_code \|\| outlet_code) | ✅ 100% | Surrogate key; Hash combines country + outlet code; PK |
| 2 | `country_iso_code` | STRING | YES | v_dim_store | country_cd_nk | UPPER(TRIM(country_cd_nk)) | ✅ 100% | Constant: 'MA' (Morocco); All stores filtered by country_cd_nk='MA' |
| 3 | `outlet_code` | STRING | YES | v_dim_store | store_code_nk | TRIM(store_code_nk) KEEP CASE | ✅ 100% | Format: M##_XXXXXX (Modern) or N##_XXXXXX (Neighborhood); Delivery key |
| 4 | `outlet_name` | STRING | NO | v_dim_store | area_description | UPPER(TRIM(area_description)) | ⚠️ ~100% (limited) | Geographic area name (e.g., AGADIR, RABAT); Covers all stores but ~2 unique values per region |
| 5 | `channel_name` | STRING | NO | v_dim_store | channel_name | UPPER(TRIM(channel_name)) | ✅ 100% | Constant: 'RT' (Retail Trade); All Morocco records are RT channel |
| 6 | `outlet_segment_code` | STRING | YES | v_dim_store | store_code_nk (prefix) | CASE WHEN store_code_nk LIKE 'M%' THEN 'MODERN_TRADE' ELSE 'NEIGHBORHOOD' END | ✅ 100% | Segment derived from code prefix; M=Modern (~27%), N=Neighborhood (~73%) |
| 7 | `outlet_tier_code` | STRING | NO | MISSING | N/A | NULL | ❌ 0% | Gap: No tier data in v_dim_store or invoices; Requires business tier assignment |
| 8 | `latitude` | DOUBLE | NO | v_dim_store | store_latitude | CAST(store_latitude AS FLOAT64) | ✅ 100% | WGS84 decimal; Range: 29.98–35.78°N (Morocco bounds valid) |
| 9 | `longitude` | DOUBLE | NO | v_dim_store | store_longitude | CAST(store_longitude AS FLOAT64) | ✅ 100% | WGS84 decimal; Range: -9.70 to -1.92°W (Morocco bounds valid) |
| 10 | `outlet_address` | STRING | NO | MISSING | N/A | NULL | ❌ 0% | Gap: v_dim_store has no address; v_fct has warehouse_description (~10% populated) |
| 11 | `outlet_start_date` | DATE | NO | v_fct_distributor_invoice_line_item | distributor_invoice_date_code_nk | MIN(distributor_invoice_date_code_nk) per store_sk | ⚠️ ~90% | Can derive from first invoice date; ~10% missing (manual records without store_sk link) |
| 12 | `outlet_close_date` | DATE | NO | MISSING | N/A | NULL | ❌ 0% | Gap: No close date in v_dim_store or invoices; Would require separate tracking |
| 13 | `outlet_status_name` | STRING | NO | Inferred | N/A | 'Active' (default) | ✅ 100% | Assume all v_dim_store records are active (no status field in source) |
| 14 | `outlet_status_mdlz_code` | STRING | NO | MISSING | N/A | NULL | ❌ 0% | Gap: Requires Mondelēz status code mapping (ACT, CLO, PSP) |
| 15 | `outlet_type_name` | STRING | NO | v_dim_store | channel_name | CASE WHEN channel_name='RT' THEN 'RETAIL_STORE' END | ✅ 100% | Derived from channel; All Morocco = 'RETAIL_STORE' |
| 16 | `outlet_type_distributor_code` | STRING | NO | v_dim_store | source_system_nk | 'DMS' (constant) | ✅ 100% | Source system identifier; All Morocco use DMS |
| 17 | `outlet_type_mdlz_code` | STRING | NO | MISSING | N/A | NULL | ❌ 0% | Gap: Requires Mondelēz outlet type mapping table |
| 18 | `outlet_group_name` | STRING | NO | MISSING | N/A | NULL | ❌ 0% | Gap: No outlet grouping in sources; Could infer 'EMID_NETWORK' |
| 19 | `outlet_group_code` | STRING | NO | v_dim_store | distributor_nk | UPPER(TRIM(distributor_nk)) | ✅ 100% | Constant: 'EMID' (single distributor for Morocco); Represents distributor network |
| 20 | `location_type_name` | STRING | NO | MISSING | N/A | NULL | ❌ 0% | Gap: No location type (urban/rural/highway) in either source |
| 21 | `location_level_1` | STRING | NO | Constant | N/A | 'MOROCCO' | ✅ 100% | Country level; Fixed constant for Morocco dataset |
| 22 | `location_level_2` | STRING | NO | v_fct_distributor_invoice_line_item + v_dim_store | business_territory_area + area_description | COALESCE(business_territory_area, area_description) | ⚠️ ~90% | Region from invoices (~10% null); Fallback to store area_description |
| 23 | `location_level_3` | STRING | NO | MISSING | N/A | NULL | ❌ 0% | Gap: City/town level not available; Requires reverse geocoding or external reference |
| 24 | `location_level_4` | STRING | NO | MISSING | N/A | NULL | ❌ 0% | Gap: District/neighborhood level not available |
| 25 | `location_level_5` | STRING | NO | MISSING | N/A | NULL | ❌ 0% | Gap: Sub-district level not available |
| 26 | `location_level_6` | STRING | NO | MISSING | N/A | NULL | ❌ 0% | Gap: Finest granularity not available |
| 27 | `has_vc` | BOOLEAN | NO | MISSING | N/A | NULL | ❌ 0% | Gap: No visicooler equipment data in either source |

**Coverage Summary (Store & Invoice Tables Only):**
- ✅ **12/27 columns (44%)** — 100% complete; Direct mapping from v_dim_store
- ⚠️ **2/27 columns (7%)** — Partial coverage (90%); Enhanced from v_fct via MIN invoice date
- ❌ **13/27 columns (48%)** — 0% coverage; Missing data sources; Requires external implementation

---

## Executive Summary

The `outlet_master` table is a comprehensive outlet/store reference layer designed for ML model inputs and business analytics. Based on analysis of three BigQuery source tables (v_dim_store, v_manual_poi_ma, v_dim_product), the mapping framework identifies data sources, transformations, and coverage gaps.

---

## Source Data Coverage (Store & Invoice Tables Only)

**Primary Source:** v_dim_store (43,324 Morocco RT stores)
- ✅ Core identity: outlet_sok, country_iso_code, outlet_code
- ✅ Coordinates: latitude, longitude (WGS84, fully validated)
- ✅ Segment & Type: outlet_segment_code (M/N prefix), outlet_type_name (RT → RETAIL_STORE)
- ✅ Channel & Group: channel_name ('RT'), outlet_group_code ('EMID')
- ⚠️ Name: area_description (geographic area only; e.g., AGADIR, RABAT; not specific outlet name)
- ❌ Address, status, dates, tier, location hierarchy levels 3-6

**Secondary Source:** v_fct_distributor_invoice_line_item (16,175,168 Morocco transactions)
- ✅ First Invoice Date: Derive outlet_start_date via MIN(distributor_invoice_date_code_nk) per store_sk (~90% coverage; ~10% manual records without store_sk link)
- ⚠️ Geographic Refinement: business_territory_area and business_territory_region available (~90% populated; ~10% null for manual consolidation records)
- ⚠️ Warehouse Info: distributor_invoice_warehousedescription (sparse; ~10% populated)
- ❌ Address, tier, close date, Mondelēz codes, location hierarchy

---

## Implementation Roadmap

### Phase 1: MVP Direct Store Mapping (High Priority) — 100% Direct Coverage

**Goal:** Create outlet_master with all directly mappable columns from v_dim_store

**Steps:**
1. ✅ Use v_dim_store as primary source (43,324 Morocco RT stores)
2. ✅ Derive outlet_sok using SHA256(country_iso_code || outlet_code)
3. ✅ Map outlet_code directly from store_code_nk (no transformation)
4. ✅ Map outlet_name from area_description (geographic area name; limited detail but 100% coverage)
5. ✅ Infer outlet_segment_code from store_code_nk prefix (M=Modern Trade, N=Neighborhood)
6. ✅ Map coordinates from store_latitude/longitude (100% coverage, WGS84 validated)
7. ✅ Set constant values: country_iso_code='MA', channel_name='RT', location_level_1='MOROCCO'
8. ✅ Derive outlet_type_name from channel_name (all RT → 'RETAIL_STORE')
9. ✅ Set outlet_type_distributor_code='DMS', outlet_group_code='EMID'
10. ✅ Default outlet_status_name='Active' (assumption: all current records active)

**SQL Pattern:**
```sql
SELECT
  TO_HEX(SHA256(CONCAT('MA', '::', store_code_nk))) as outlet_sok,
  'MA' as country_iso_code,
  store_code_nk as outlet_code,
  area_description as outlet_name,
  channel_name,
  CASE WHEN store_code_nk LIKE 'M%' THEN 'MODERN_TRADE' ELSE 'NEIGHBORHOOD' END as outlet_segment_code,
  NULL as outlet_tier_code,
  store_latitude as latitude,
  store_longitude as longitude,
  NULL as outlet_address,
  NULL as outlet_start_date,  -- Will populate in Phase 1b
  NULL as outlet_close_date,
  'Active' as outlet_status_name,
  NULL as outlet_status_mdlz_code,
  'RETAIL_STORE' as outlet_type_name,
  'DMS' as outlet_type_distributor_code,
  NULL as outlet_type_mdlz_code,
  NULL as outlet_group_name,
  distributor_nk as outlet_group_code,
  NULL as location_type_name,
  'MOROCCO' as location_level_1,
  area_description as location_level_2,  -- Limited; repeats outlet_name
  NULL as location_level_3,
  NULL as location_level_4,
  NULL as location_level_5,
  NULL as location_level_6,
  NULL as has_vc
FROM `prd-amea-analyt-diso-svc-7f.amea_ds_distributor_sellout.v_dim_store`
WHERE country_cd_nk='MA' AND lower(channel_name)='rt'
```

**Expected Output:** 43,324 outlet rows; 10/27 columns populated (100%); 17 columns NULL

### Phase 1b: Invoice-Based Start Date Enhancement (High Priority)

**Goal:** Populate outlet_start_date from first invoice date per store

**Steps:**
1. JOIN v_dim_store to v_fct_distributor_invoice_line_item on store_sk
2. GROUP BY store_sk; find MIN(distributor_invoice_date_code_nk)
3. Merge outlet_start_date back to outlet_master
4. Handle ~10% of stores without invoice history (no start date; assume recently added)

**SQL Pattern:**
```sql
WITH store_first_invoice AS (
  SELECT
    store_sk,
    MIN(distributor_invoice_date_code_nk) as first_invoice_date
  FROM `prd-amea-analyt-diso-svc-7f.amea_ds_distributor_sellout.v_fct_distributor_invoice_line_item`
  WHERE country_code_nk='MA'
  GROUP BY store_sk
)
UPDATE outlet_master om
SET outlet_start_date = sfi.first_invoice_date
FROM store_first_invoice sfi
WHERE om.outlet_sok = TO_HEX(SHA256(CONCAT('MA', '::', sfi.store_sk)))  -- Requires store_sk tracking
```

**Expected Output:** ~90% of outlets (39,000+) with outlet_start_date; ~10% remain NULL

### Phase 2: Geographic Hierarchy Refinement from Invoices (Medium Priority)

**Goal:** Enhance location_level_2 from invoice territory data

**Steps:**
1. JOIN v_dim_store to v_fct_distributor_invoice_line_item on store_sk
2. Use business_territory_area and business_territory_region from invoices
3. COALESCE(business_territory_area, area_description) for location_level_2
4. Update location_level_2 in outlet_master

**Expected Coverage:** ~90% (manual consolidation records ~10% null; fallback to area_description)

---

## Known Constraints & Assumptions

### Data Constraints
1. **Source Limitation:** Only v_dim_store + v_fct_distributor_invoice_line_item; No POI, product, or external reference tables
2. **Single Market:** Morocco only (country_iso_code = 'MA')
3. **Single Distributor:** EMID for all Morocco records
4. **Single Channel:** RT (Retail Trade) only; other channels would require separate dimension
5. **Name Limitation:** area_description provides geographic area only (e.g., AGADIR), not specific outlet name
6. **Address Gap:** No address data available in either source table
7. **Location Hierarchy Gap:** Only 2 levels available (country, region); location_level_3-6 require external geocoding

### Business Assumptions
1. **Active Status Default:** All current v_dim_store records are active (no status field in source)
2. **Segment from Code:** Modern Trade inferred from M-prefix; Neighborhood from N-prefix
3. **No Close Dates:** No outlet_close_date available; would require separate SCD2 or status tracking
4. **First Invoice = Open Date:** outlet_start_date approximated from first invoice; May not reflect actual open date
5. **Manual Record Exclusion:** ~10% of invoices have no store_sk link (manual consolidation); These stores won't get start_date

---

## Recommendations for Implementation

### High Priority (Phase 1 Implementation)
1. **Phase 1 MVP:** Create outlet_master from v_dim_store (12 columns, 100% coverage) — 1 week
2. **Phase 1b Enhancement:** Add outlet_start_date from v_fct invoices (~90% coverage) — 3 days
3. **Phase 2 Refinement:** Enhance location_level_2 from invoice territories — 2 days

### Medium Priority (External Data Required)
1. **Outlet Name:** Replace area_description with proper store names (requires business data)
2. **Address:** Implement outlet_address (requires external GIS or manual entry)
3. **Location Hierarchy:** Implement location_level_3-6 via reverse geocoding API (Google Maps, PostGIS)

### Low Priority (Business Logic Required)
1. **Tier Assignment:** Implement outlet_tier_code (business-defined rules needed)
2. **Close Dates:** Implement outlet_close_date (requires SCD2 tracking or status dimension)
3. **Mondelēz Codes:** Implement outlet_status_mdlz_code, outlet_type_mdlz_code (mapping tables needed)
4. **has_vc:** Implement visicooler flag (requires equipment master table)

---

## Implementation Status & Next Steps

**Current Analysis Scope:** v_dim_store + v_fct_distributor_invoice_line_item only (Morocco market)

**Coverage Achieved:**
- ✅ **12/27 columns (44%):** 100% direct mapping from v_dim_store
- ⚠️ **2/27 columns (7%):** Enhanced coverage from v_fct invoices (outlet_start_date ~90%, location_level_2 refined)
- ❌ **13/27 columns (48%):** Requires external data or business logic

**Estimated Implementation Timeline:**
- Phase 1 MVP: 1 week (43,324 outlets, 12 columns populated)
- Phase 1b Enhancement: 3 days (add outlet_start_date from invoices)
- Phase 2 Refinement: 2 days (enhance location_level_2 from territories)
- **Total Phase 1-2:** ~10 days

**Business Blockers for Phase 3:**
- Outlet proper names (currently using geographic area only)
- Outlet tier classification rules
- Close date tracking (requires SCD2 or separate tracking)
- Visicooler equipment status (requires separate master)
