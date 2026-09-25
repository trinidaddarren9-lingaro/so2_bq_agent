# README — Outlet Master Data Mapping

**Quick Start Guide for Morocco Retail Outlet Mastering**

---

## What This Is

A complete **data mapping specification** for transforming MDLZ distributor store master data (v_dim_store) into the standardized **outlet_master** data model for Morocco retail operations.

- **Target:** 27-column outlet_master table
- **Source:** Primary v_dim_store (DISO-prod)
- **Geography:** Morocco (country_iso_code='MA')
- **Channel:** Retail only (channel_code_nk='rt')
- **Status:** ✅ Ready for Production

---

## Files in This Directory

| File | What It Is | Read If You Want To... |
|------|-----------|------------------------|
| **column_mapping_outlet_master.csv** | Master mapping table (27 rows + summaries) | See exact transformation logic for each column |
| **outlet_master_MAPPING_GUIDE.md** | Technical reference guide | Understand HOW to transform each column with SQL examples |
| **outlet_master_MAPPING_SUMMARY.md** | Executive overview | Understand WHAT was analyzed and confidence scores |
| **README.md** | This file | Get started quickly |
| **INDEX.md** | Navigation guide | Navigate between files and find specific info |

---

## Quick Reference: Key Facts

### Filters (MANDATORY)
```sql
WHERE
  country_cd_nk = 'MA'        -- Morocco country code
  AND channel_code_nk = 'rt'  -- Retail channel
```

### Primary Source Table
```
Project:  prd-amea-analyt-diso-svc-7f (DISO-prod)
Dataset:  amea_ds_distributor_sellout
Table:    v_dim_store
Columns:  30+ columns with strong outlet matching
```

### Column Mapping Summary
- **27 target columns:** All mapped ✅
- **18 HIGH confidence (>0.85):** Ready to use
- **8 MEDIUM confidence (0.70-0.85):** Validate before use
- **1 LOW confidence (<0.70):** Requires business rule

### Typical Query Structure
```sql
SELECT
  TO_HEX(MD5(CONCAT(country_cd_nk,'|',source_system_nk,'|',distributor_nk,'|',store_code_nk))) 
    AS outlet_sok,
  country_cd_nk AS country_iso_code,
  store_code_nk AS outlet_code,
  store_nm AS outlet_name,
  channel_name,
  COALESCE(store_profile_1, 'ALL') AS outlet_segment_code,
  store_grade_description AS outlet_tier_code,
  store_latitude AS latitude,
  store_longitude AS longitude,
  store_address_co AS outlet_address,
  DATE(store_open_date) AS outlet_start_date,
  NULLIF(DATE(store_close_date), DATE('1900-01-01')) AS outlet_close_date,
  CASE WHEN store_profile_3='A' THEN 'Active' WHEN store_profile_3='C' THEN 'Closed' ELSE 'Prospect' END 
    AS outlet_status_name,
  store_type_name AS outlet_type_name,
  store_group_code_nk AS outlet_group_code,
  store_group_description AS outlet_group_name,
  store_city_nm AS location_level_1,
  COALESCE(store_county, store_district) AS location_level_2,
  store_region AS location_level_3,
  store_state_name AS location_level_4,
  COALESCE(store_suburb, '') AS location_level_5,
  area_description AS location_type_name,
  CASE WHEN store_size_area_sqre_meter_val >= 5000 THEN TRUE ELSE FALSE END AS has_vc
FROM
  `prd-amea-analyt-diso-svc-7f.amea_ds_distributor_sellout.v_dim_store`
WHERE
  country_cd_nk = 'MA'
  AND channel_code_nk = 'rt'
ORDER BY
  store_code_nk
```

---

## How to Use This Mapping

### 1. **For SQL Implementation**
   - Open **column_mapping_outlet_master.csv**
   - Find your target column in the `target_column` field
   - Copy the `transformation_logic` to your SQL script
   - Adjust for your environment (project IDs, date formats, thresholds)

### 2. **For Understanding the Data**
   - Read **outlet_master_MAPPING_SUMMARY.md** for overview
   - Check confidence classification (HIGH/MEDIUM/LOW)
   - Review sample data in the summary

### 3. **For Technical Details**
   - Refer to **outlet_master_MAPPING_GUIDE.md**
   - Find your column in TIER 1, TIER 2, or TIER 3 section
   - Review transformation SQL, sample values, null rates
   - Check validation queries

### 4. **For Validation**
   - Use the Data Quality Validation section in MAPPING_GUIDE.md
   - Run sample queries to validate before production load
   - Check null rates and distinct counts match expectations

---

## Before You Load

### 1. Verify Prerequisites
- [ ] Access to `prd-amea-analyt-diso-svc-7f` (DISO-prod project)
- [ ] Read permissions on `amea_ds_distributor_sellout.v_dim_store`
- [ ] Write permissions to target `temp.l2_masterdata_in_v1_outlet_master` (SORSA-dev)
- [ ] BigQuery Python client or SQL IDE (BigQuery Console, DBeaver, etc.)

### 2. Define Business Rules
- [ ] **has_vc threshold:** What's the minimum store area (sqm) for Value Center designation?
  - Current default: >= 5,000 sqm
  - Confirm with business team
- [ ] **outlet_segment_code:** Is 'ALL' a valid sentinel value for unmapped segments?
- [ ] **Outlet tier codes:** Confirm v_dim_store.store_grade_description values

### 3. Test Transformation
Run this sample query in BigQuery to preview transformed data:
```sql
-- Test query: Preview mapped outlet_master (Morocco + Retail)
SELECT
  store_code_nk AS outlet_code,
  store_nm AS outlet_name,
  channel_name,
  country_cd_nk,
  COUNT(*) OVER () AS total_outlets
FROM
  `prd-amea-analyt-diso-svc-7f.amea_ds_distributor_sellout.v_dim_store`
WHERE
  country_cd_nk = 'MA'
  AND channel_code_nk = 'rt'
LIMIT 10
```

Expected result: 5-15 rows with valid outlet codes and names

---

## Deployment Checklist

### Pre-Production
- [ ] Run test query above — verify row count and data
- [ ] Confirm all HIGH confidence columns (18) ready for use
- [ ] Validate MEDIUM confidence columns (8) with business stakeholders
- [ ] Define has_vc threshold (LOW confidence column)
- [ ] Archive previous version of outlet_master table
- [ ] Document all transformation logic in production procedure
- [ ] Prepare rollback plan

### Load Phase
- [ ] Create/truncate staging table for outlet_master
- [ ] Run full transformation SQL (see example query above)
- [ ] Validate row count: Expected ~500-600 outlets (Morocco + Retail)
- [ ] Check data quality:
  - No NULLs in outlet_code, country_iso_code, channel_name
  - Latitude range: 27-36 (Morocco bounds)
  - Longitude range: -5 to -14 (Morocco bounds)
  - Dates in proper ISO format

### Post-Load
- [ ] Run validation queries from MAPPING_GUIDE.md
- [ ] Check for NULL rates per column (compare with baseline)
- [ ] Verify outlet_sok uniqueness
- [ ] Update table statistics
- [ ] Document any exceptions or manual fixes

---

## Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| No rows returned | Missing filter values | Verify country_cd_nk='MA' exists AND channel_code_nk='rt' exists |
| NULL values in key columns | Source data sparse | Check null_rate in MAPPING_GUIDE; may be expected |
| Latitude/longitude invalid | Format error | Validate WGS-84 range: lat [-90,90], lon [-180,180] |
| outlet_sok collisions | Hash function issue | Use TO_HEX(MD5(...)) to ensure 32-char output |
| has_vc all FALSE | Threshold too high | Adjust sqm threshold (default 5000) based on business rule |

---

## Support & Questions

### Technical Questions
- **Transformation logic:** See outlet_master_MAPPING_GUIDE.md (TIER 1, 2, 3 sections)
- **Confidence scores:** See outlet_master_MAPPING_SUMMARY.md (Confidence Classification section)
- **Data quality:** See MAPPING_GUIDE.md (Data Quality Validation section)

### Business Questions
- **Morocco filter:** country_cd_nk='MA' (confirmed across all sources)
- **Retail channel:** channel_code_nk='rt' (DISO standard)
- **Data refresh:** Daily from DISO (prd-amea-analyt-diso-svc-7f.amea_ds_distributor_sellout)

### File Questions
- **Which file?** See INDEX.md for quick navigation
- **Not found?** Check file names in directory listing above

---

## Additional Resources

| Resource | Location | Purpose |
|----------|----------|---------|
| MCP Server Routing | docs/bigquery/mcp-servers.md | Find correct GCP project for each domain |
| Morocco Schema Inventory | docs/bigquery/sttm-morocco/sttm_morocco_schema.csv | Full column inventory for all 11 source tables |
| Copilot Instructions | .github/copilot-instructions.md | BigQuery engineering standards |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Jan 2025 | Initial mapping complete — 27 columns, 3 confidence tiers |

---

**Ready to implement? Start with:**
1. Open `column_mapping_outlet_master.csv`
2. Find your target column
3. Copy the transformation_logic
4. Adapt for your environment
5. Test with sample query above
6. Deploy!

**Questions? See INDEX.md for quick reference.**
