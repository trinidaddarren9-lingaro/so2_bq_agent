# POI Master Mapping - File Index

## Navigation Guide

### 📋 Files in This Directory

| File | Type | Purpose | Key Content |
|------|------|---------|---|
| **column_mapping_poi_master.csv** | CSV Data | Core mapping with source candidates | 7 target columns, v_manual_poi_ma primary source, perfect 100% scoring |
| **README.md** | Documentation | Quick start guide | Overview, Morocco-only source (no filter needed), 18,514 POIs, 100% coordinate coverage |
| **INDEX.md** | Navigation | This file - links all documents | File descriptions, navigation shortcuts, content summary, uniqueness of this mapping |
| **POI_MASTER_MAPPING_GUIDE.md** | Documentation | Detailed column analysis | Column breakdown with sample outlet data, coordinate precision, category taxonomy, coverage |
| **POI_MASTER_MAPPING_SUMMARY.md** | Documentation | Executive summary & approval | Perfect confidence (100% HIGH), v_manual_poi_ma analysis, NULL handling, geo-data quality |

## Quick Navigation

### For Business Users
1. Start with **README.md** (2-minute overview - emphasizes simplicity)
2. Review **POI_MASTER_MAPPING_SUMMARY.md** (approval checklist, coordinate coverage)
3. Check **POI_MASTER_MAPPING_GUIDE.md** for outlet type categories

### For Data Engineers
1. Open **column_mapping_poi_master.csv** (straightforward 7-column mapping)
2. Review **POI_MASTER_MAPPING_GUIDE.md** (source data structure, NULL handling)
3. Consult **POI_MASTER_MAPPING_SUMMARY.md** (Morocco-exclusive system notes)

### For Geo-Analytics Teams
1. **POI_MASTER_MAPPING_SUMMARY.md** (coordinate coverage: 100%, 18,514 locations)
2. **POI_MASTER_MAPPING_GUIDE.md** (latitude/longitude precision, category hierarchy)
3. **column_mapping_poi_master.csv** (source field names for coordinate validation)

## Content Summary

### column_mapping_poi_master.csv
- **Structure:** CSV with 9 rows (7 columns + 1 header + 1 SUMMARY)
- **Columns:** source_column, target_candidates, name_similarity_score, value_match_score, combined_score, reasons, selected_target, confidence, decision
- **Unique Feature:** All 7 columns have HIGH confidence (100% confidence distribution)
- **Average Score:** 0.945 (highest of the three tables)

### POI_MASTER_MAPPING_GUIDE.md
- **POI categories:** Modern trade, traditional trade, on-premise, other classifications
- **Coordinate validation:** Latitude/longitude precision, format, range checks
- **Sample outlets:** Real outlet examples from v_manual_poi_ma
- **Coverage notes:** 100% coordinate coverage, 80% store_name coverage

### POI_MASTER_MAPPING_SUMMARY.md
- **Key finding:** v_manual_poi_ma is 100% Morocco-exclusive (all 18,514 records are MA)
- **No filtering required:** Simplest mapping of the three tables
- **Perfect confidence:** All 7 columns scored HIGH (>0.85 combined score)
- **Geo-coverage:** 100% populated coordinates (critical for analytics)
- **Quality metric:** Store names 80% populated (4,249 NULLs acceptable)
- **Approval checklist:** 6 items, emphasizing coordinate validation

### README.md
- **Unique simplicity:** No complex joins, Morocco-only source
- **Source:** v_manual_poi_ma (18,514 rows, SORSA dev, 100% MA)
- **Output:** 18,514 unique POI records (all source data used)
- **Key feature:** 100% coordinate coverage for geo-mapping
- **Minimal filter logic:** Accept all 18,514 records without filtering

## Data Characteristics

| Aspect | Details |
|--------|---------|
| **Target Table** | l2_masterdata_in_v1_poi_master (7 columns) |
| **Primary Source** | v_manual_poi_ma (18,514 rows, SORSA dev, Morocco-only) |
| **Output Records** | 18,514 POI locations (100% of source) |
| **High Confidence** | 7 columns (100%) - PERFECT SCORE |
| **Medium Confidence** | 0 columns (0%) |
| **Unmapped Columns** | 0 |
| **Average Score** | 0.945 (highest of all three tables) |
| **Unique Aspect** | No country filter needed - source is 100% Morocco |
| **Coordinates** | 100% populated (18,514/18,514 locations) |

## Key Mappings Summary

**Perfect Alignment (All HIGH Confidence 0.90+):**
- poi_sok → v_manual_poi_ma.poi_sk (0.97)
- country_iso_code → v_manual_poi_ma.country_code_nk (0.97, hardcoded 'MA')
- poi_code → v_manual_poi_ma.poi_sk (0.94)
- poi_name → v_manual_poi_ma.store_name (0.97)
- poi_type_name → v_manual_poi_ma.main_category_name (0.95)
- latitude → v_manual_poi_ma.store_latitude (0.97)
- longitude → v_manual_poi_ma.store_longitude (0.97)

## NULL and Data Quality

| Column | Coverage | NULL Count | Notes |
|--------|----------|---|---|
| poi_sk | 100% | 0 | Unique key, always populated |
| country_code_nk | 100% | 0 | All 'MA' (Morocco) |
| store_name | 79.87% | 4,249 | Acceptable NULL rate (NULL = unnamed outlet) |
| main_category_name | 100% | 0 | Complete category classification |
| store_latitude | 100% | 0 | Critical for geo-analytics |
| store_longitude | 100% | 0 | Critical for geo-analytics |

## Unique Characteristics of This Mapping

✅ **ONLY Morocco-specific mapping** - v_manual_poi_ma is exclusively Morocco data
✅ **100% HIGH confidence** - All 7 columns perfect alignment
✅ **No filtering required** - Accept entire source table
✅ **Geo-complete** - 100% coordinate coverage (18,514 locations)
✅ **Simplest implementation** - Single source table, minimal joins
✅ **Manual curated data** - Mondelēz maintains POI directory manually

⚠️ **Manual data entry quality** - Consider validation process for store names
⚠️ **20% store name NULLs** - Some outlets lack registered names

## Usage Tips

- **CSV Import:** UTF-8 encoding, pipe (|) delimiter for candidate lists (though all are single-source)
- **No filtering:** Use all 18,514 records directly from v_manual_poi_ma
- **Coordinate validation:** Ensure lat/lon within Morocco bounds (Latitude: 21.3°-36.0°N, Longitude: -17.1°--1.0°W)
- **Category mapping:** Classify by main_category_name (Modern Trade, Traditional Trade, On-premise, Other)
- **Performance:** <1 second, <50MB scan (smallest table of three)

## Related Files
- Parent directory: `/STTM Morocco/`
- Sibling directories: `/product_master/`, `/invoice_line_item/`
- Source schema reference: `/docs/bigquery/sttm-morocco/sttm_morocco_schema.csv`
- MCP routing: `/docs/bigquery/mcp-servers.md`

## Why This Mapping is Unique

This POI mapping stands out because:
1. **100% PRIMARY SOURCE** - v_manual_poi_ma serves all 7 columns
2. **NO AMBIGUITY** - Each target column has one obvious source
3. **PERFECT CONFIDENCE** - All mappings scored >0.94 (highest alignment)
4. **MOROCCO-EXCLUSIVE** - Only this table is 100% country-specific
5. **GEO-COMPLETE** - Critical for location-based analytics
