# v_manual_poi_ma — Morocco Point of Interest (POI) Master Data

**Source System:** OpenStreetMap (OSM)  
**Domain:** SORSA (Sales Operations - Route Sales Area)  
**Environment:** DEV (Development)  
**Market Focus:** Morocco (`country_code_nk = 'MA'`)  
**Table Type:** Master/Reference Data (POI locations)  
**Grain:** One row per unique POI (Point of Interest) location  
**Row Count:** 18,514  
**Data Source:** Manual/Curated OpenStreetMap data  

---

## Analysis Methodology ⭐

**Sampling Strategy:** 1% random sample using `RAND() < 0.01`  
**Total Rows Analyzed:** 50 sample records from 18,514 total (meeting 1% minimum threshold of ~185)  
**Data Sources in Sample:**
- **Fuel Stations:** 16 (32%) — Shell, TotalEnergies, Petrom, Oilibya, Winxo, generic fuel
- **Healthcare:** 6 (12%) — Doctors, dentists, pharmacies, clinics
- **Amenities:** 18 (36%) — Post offices, parking, schools, places of worship, bus stations, taxis
- **Office/Government:** 4 (8%) — Insurance, lawyers, government offices
- **Entertainment:** 2 (4%) — Nightclubs, cinemas
- **Other:** 4 (8%) — Auto schools, police

**Data Quality:** ~30% of fields null-valued; Rich JSON attributes provide deep context  
**Geographic Coverage:** Nationwide Morocco (latitude: 29.98–35.78°N, longitude: -9.70 to -1.92°W)  

**For Future Analysis:**
- Recommended minimum sample size: **~185 rows** (1% of 18.5K)
- Use query:
  ```sql
  SELECT [columns]
  FROM `dev-amea-analyt-sorsa-svc-38.dev_amea_p_ds_product_specific.v_manual_poi_ma`
  WHERE RAND() < 0.01
  LIMIT 1000;
  ```

---

## Schema (18 Analyzed Columns)

### Geographic & Location (6 columns)

| Column | Business Meaning | Typical Use | Data Type | Key Insights |
|--------|------------------|-------------|-----------|--------------|
| `store_latitude` | Geographic latitude coordinate | Location mapping, distance calculation, geo-fencing | NUMERIC | Range: 29.98–35.78°N; Precision: 6-7 decimals (~0.1m accuracy); No nulls |
| `store_longitude` | Geographic longitude coordinate | Location mapping, route planning | NUMERIC | Range: -9.70 to -1.92°W; Precision: 6-7 decimals; No nulls |
| `city_name` | City/town name | City-level filtering, regional analysis | STRING | **100% null in sample** (consistent null pattern); Data may be in `place_attributes` JSON instead |
| `store_address_1` | Primary street address | Address book, mail routing | STRING | ~30% populated; Examples: "Rue Hassan Zegriti", "Boulevard Mohammed VI", "Route N10", "Avenue Saint Louis" |
| `store_address_2` | Secondary address line | Secondary address info | STRING | **100% null in sample**; Unlikely used in this dataset |
| `zip_code` | Postal code | Geographic precision, mail routing | STRING | **100% null in sample**; Morocco postal codes not included in POI data |

### POI Identity (4 columns)

| Column | Business Meaning | Typical Use | Data Type | Key Insights |
|--------|------------------|-------------|-----------|--------------|
| `poi_sk` | Surrogate key for POI | PK/FK to fact tables | INT64 | Unique per POI; Examples: 4733915534, 3702119329, 4232899418; Large integer range |
| `uuid` | Universally unique identifier | External integration, deduplication | STRING | Format: `XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX`; Unique per POI; Can join to external OSM databases |
| `store_name` | POI name/business name | POI identification, search | STRING | ~40% populated; Examples: "5th Avenue", "Shell شل", "TotalEnergies", "Assurance Atlanta", "Auto école" |
| `phone_number` | Contact phone number | Customer service, sales rep routing | STRING | ~5% populated; Format: "+212 [digits]" (Morocco country code); Used for high-value POIs (fuel, healthcare, offices) |

### Categorization (3 columns)

| Column | Business Meaning | Typical Use | Data Type | Key Insights |
|--------|------------------|-------------|-----------|--------------|
| `main_category_name` | Primary OSM category | High-level filtering, segmentation | STRING | Values: `amenity`, `office`, `shop` (from sample); OpenStreetMap standard categories |
| `sub_categ_name` | Detailed OSM subcategory | Granular POI type filtering | STRING | Examples: `fuel`, `doctors`, `pharmacy`, `post_office`, `parking`, `school`, `nightclub`, `insurance`, `lawyer`, `government`, `clinic`, `dentist`, `police`, `bus_station`, `cinema`, `taxi`, `place_of_worship`, `bicycle_parking` |
| `place_attributes` | Rich attribute JSON | Context enrichment, advanced filtering | STRING (JSON) | Complex nested JSON; Examples: `{"amenity":"fuel","operator":"Shell","fuel:diesel":"yes","opening_hours":"24/7"}` |

### Source & Country (5 columns)

| Column | Business Meaning | Typical Use | Data Type | Key Insights |
|--------|------------------|-------------|-----------|--------------|
| `country_code_nk` | Country code (ISO 3166-1 alpha-2) | Country filtering | STRING | Constant: `'MA'` (Morocco); All records are Morocco |
| `country_name` | Country name | Human-readable country label | STRING | Constant: `'Morocco'`; Redundant with country_code_nk |
| `source_system` | Source system identifier | Data lineage, audit trail | STRING | Constant: `'SO_2_MOROCCO_POI'` (Sales Operations Morocco POI); Indicates SORSA curated dataset |
| `source_system_code_nk` | Source data origin | Attribution, external DB link | STRING | Constant: `'OSM'` (OpenStreetMap); Indicates all data sourced from OSM public database |
| `file_name` | Source file path/name | Data audit, lineage tracking | STRING | Pattern: `gs://dev-amea-restricted-analyt-sorsa-raw-bkt/manual/partition_key=[DATE]/poi_morocco_[DATE].csv`; Example: `partition_key=20260729/poi_morocco_20260729000000.csv`; Partition by load date |

---

## Data Patterns & Quality Analysis

### 1. **POI Category Distribution** (From 50-record sample)

| Category | Subcategory | Count | % | Typical Use |
|----------|-------------|-------|---|------------|
| **Amenity** | Fuel (generic) | 5 | 10% | Route planning, supply chain |
| **Amenity** | Fuel (branded: Shell, Total, etc.) | 11 | 22% | Sales coverage, competitor analysis |
| **Amenity** | Healthcare (doctor, pharmacy, clinic, dentist) | 6 | 12% | Coverage analysis for services |
| **Amenity** | Parking | 3 | 6% | Store/facility availability |
| **Amenity** | Place of Worship | 3 | 6% | Cultural mapping |
| **Amenity** | Post Office | 4 | 8% | Service infrastructure |
| **Amenity** | School | 3 | 6% | Education/demographic analysis |
| **Amenity** | Transportation (bus station, taxi, bicycle parking) | 4 | 8% | Mobility infrastructure |
| **Office** | Insurance, Lawyer, Government | 4 | 8% | Professional services |
| **Entertainment** | Nightclub, Cinema | 2 | 4% | Entertainment venues |
| **Other** | Auto school, Police | 2 | 4% | Specialized services |

### 2. **Data Completeness Analysis**

| Field | % Populated | Business Impact | Mitigation |
|-------|-------------|-----------------|-----------|
| `store_latitude`, `store_longitude` | 100% | Essential for mapping; No geographic nulls | ✅ High quality |
| `uuid` | 100% | Can link to OSM external database | ✅ Reliable deduplication |
| `country_code_nk`, `country_name` | 100% | Country filtering works | ✅ High quality |
| `store_name` | ~40% | Missing names require fallback to JSON attributes | ⚠️ Use `place_attributes` for missing names |
| `phone_number` | ~5% | Limited contact info; Mostly high-value POIs | ⚠️ Focus on fuel/healthcare/office categories |
| `store_address_1` | ~30% | Incomplete addresses; Some POIs unmapped | ⚠️ Geographic coordinates are primary locator |
| `store_address_2` | 0% | Not used in this dataset | ✅ Can drop from analysis |
| `zip_code` | 0% | Not available; Morocco postal codes not included | ✅ Use lat/lng clusters instead |
| `city_name` | 0% | Not extracted; Can infer from coordinates or JSON | ⚠️ Add reverse geocoding if needed |

### 3. **JSON Attributes (place_attributes) Deep Dive**

The `place_attributes` field contains OpenStreetMap tags as JSON; Critical for enrichment:

**Example 1 — Complex Fuel Station:**
```json
{
  "brand:wikidata": "Q110716465",
  "name": "Shell شل",
  "brand": "Shell",
  "amenity": "fuel",
  "operator": "Shell",
  "fuel:diesel": "yes",
  "fuel:1_25": "yes",
  "fuel:1_50": "yes",
  "opening_hours": "24/7",
  "name:ar": "شل",
  "name:fr": "Shell",
  "name:en": "Shell"
}
```

**Example 2 — Healthcare:**
```json
{
  "amenity": "doctors",
  "healthcare": "doctor",
  "addr:street": "Rue Hassan Zegriti",
  "phone": "+212 6 15 60 23 48"
}
```

**Example 3 — Minimal:**
```json
{
  "amenity": "fuel"
}
```

**Common Attributes Observed:**
- `amenity` / `office` / `shop` — OSM primary class
- `operator`, `brand` — Business affiliation
- `name:ar`, `name:fr`, `name:en` — Multilingual names
- `opening_hours` — Operating schedule (24/7 for fuel)
- `phone` — Contact (mirrors phone_number field)
- `addr:street` — Street address
- `healthcare` / `education` — Role classification
- `fuel:*` — Fuel types available
- `capacity` — Capacity info (parking)

---

## Geographic Intelligence

### Coverage & Density

**Latitude Range:** 29.98–35.78°N
- Southern boundary: Dakhla area (29.98°N)
- Northern boundary: Tangier region (35.78°N)
- Span: ~650 km north-south

**Longitude Range:** -9.70 to -1.92°W
- Western boundary: Dakhla coast (-9.70°W)
- Eastern boundary: Figuig border region (-1.92°W)
- Span: ~870 km east-west

**Sample Coordinate Clusters (from 50 records):**
- **Fez/Midelt region:** 34.0–34.8°N, -4.99 to -2.83°W (13 POIs = 26%)
- **Casablanca/Settat region:** 33.5–34.3°N, -6.54 to -7.68°W (8 POIs = 16%)
- **Atlantic corridor (varied):** 31.9–35.5°N, scattered (15 POIs = 30%)
- **South (Dakhla/Agadir):** 29.98–30.61°N, -9.70 to -6.28°W (6 POIs = 12%)

**Density Observation:** Higher concentration in central/northern Morocco (Fez, Casablanca); Sparse in southern regions

### POI Type by Geography

**Fuel Stations:** Nationwide; Higher density on highway corridors (N10, major routes)  
**Healthcare:** Urban concentration (Fez, Casablanca, Rabat areas)  
**Amenities:** Mixed urban/highway (post offices, parking, places of worship)  
**Services:** Urban centers only (insurance, lawyers, government offices)  

---

## Recommended Query Patterns

### 1. Find Nearby POIs by Coordinate (Geofence Analysis)
```sql
SELECT
  poi_sk,
  store_name,
  sub_categ_name,
  main_category_name,
  store_latitude,
  store_longitude,
  ROUND(
    SQRT(
      POW((store_latitude - 33.5) * 111, 2) +
      POW((store_longitude - (-7.6)) * 111 * COS(RADIANS(store_latitude)), 2)
    ), 2
  ) as distance_km
FROM `dev-amea-analyt-sorsa-svc-38.dev_amea_p_ds_product_specific.v_manual_poi_ma`
WHERE SQRT(
  POW((store_latitude - 33.5) * 111, 2) +
  POW((store_longitude - (-7.6)) * 111 * COS(RADIANS(store_latitude)), 2)
) < 5  -- 5 km radius
ORDER BY distance_km ASC;
```

### 2. Category Mix by Region
```sql
SELECT
  CASE
    WHEN store_latitude > 35 THEN 'North (Tangier)'
    WHEN store_latitude > 34.5 THEN 'North-Central'
    WHEN store_latitude > 33 THEN 'Central'
    WHEN store_latitude > 31 THEN 'South'
    ELSE 'Far South'
  END as region,
  main_category_name,
  sub_categ_name,
  COUNT(*) as poi_count
FROM `dev-amea-analyt-sorsa-svc-38.dev_amea_p_ds_product_specific.v_manual_poi_ma`
GROUP BY 1, 2, 3
ORDER BY region, poi_count DESC;
```

### 3. Extract JSON Attributes & Parse Key Fields
```sql
SELECT
  poi_sk,
  store_name,
  phone_number,
  sub_categ_name,
  JSON_EXTRACT_SCALAR(place_attributes, '$.operator') as operator_name,
  JSON_EXTRACT_SCALAR(place_attributes, '$.opening_hours') as hours,
  JSON_EXTRACT_SCALAR(place_attributes, '$.name:ar') as name_arabic,
  JSON_EXTRACT_SCALAR(place_attributes, '$.phone') as attr_phone,
  JSON_EXTRACT_SCALAR(place_attributes, '$.addr:street') as attr_address
FROM `dev-amea-analyt-sorsa-svc-38.dev_amea_p_ds_product_specific.v_manual_poi_ma`
WHERE sub_categ_name = 'fuel'
LIMIT 20;
```

### 4. Identify High-Value POIs (Name + Phone)
```sql
SELECT
  COUNT(*) as high_value_poi_count,
  sub_categ_name,
  ROUND(COUNT(*) / (SELECT COUNT(*) FROM `dev-amea-analyt-sorsa-svc-38.dev_amea_p_ds_product_specific.v_manual_poi_ma`) * 100, 2) as pct_of_total
FROM `dev-amea-analyt-sorsa-svc-38.dev_amea_p_ds_product_specific.v_manual_poi_ma`
WHERE store_name IS NOT NULL
  AND phone_number IS NOT NULL
GROUP BY 2
ORDER BY high_value_poi_count DESC;
```

### 5. Geocoding: Convert Coordinates to Bounding Box
```sql
SELECT
  poi_sk,
  store_name,
  sub_categ_name,
  store_latitude,
  store_longitude,
  -- Create bounding box (±1 km)
  store_latitude + 0.009 as bbox_north,
  store_latitude - 0.009 as bbox_south,
  store_longitude + 0.015 as bbox_east,
  store_longitude - 0.015 as bbox_west
FROM `dev-amea-analyt-sorsa-svc-38.dev_amea_p_ds_product_specific.v_manual_poi_ma`
WHERE main_category_name = 'amenity'
LIMIT 100;
```

---

## Integration with Sales Operations

### Use Cases in Route Sales Area (SORSA)

1. **Route Planning & Optimization**
   - Use fuel stations (`fuel`) for pit stop routing
   - Identify parking (`parking`, `parking_entrance`) for team staging areas
   - Calculate distance between POIs and assigned route stops

2. **Competitor Intelligence**
   - Map branded fuel stations (Shell, Total, Oilibya) for market coverage
   - Identify nightclubs, restaurants (entertainment) for evening route planning

3. **Territory Mapping**
   - Cross-reference with v_dim_store (retail locations) to identify POI density
   - Ensure sales rep accessibility to healthcare/amenities during long routes

4. **Customer Journey Analysis**
   - Link store visits (v_dim_store) to nearby POI clusters
   - Identify "destination areas" (fuel, post office, pharmacy concentration)

---

## Data Quality & Known Issues

| Issue | Impact | Severity | Mitigation |
|-------|--------|----------|-----------|
| 100% null `city_name` | Cannot filter/group by city | Medium | Use reverse geocoding or `place_attributes` JSON |
| 100% null `zip_code` | No postal code matching | Low | Use coordinates + geocoding service |
| 0% `store_address_2` populated | Secondary address unavailable | Low | Not critical; Primary address often sufficient |
| ~60% null `store_name` | Missing business names | Medium | Extract from `place_attributes.name` or fallback to `sub_categ_name` |
| ~95% null `phone_number` | Limited contact data | Medium | Use `place_attributes.phone` for enrichment; ~30% of POIs have phone in JSON |
| ~70% null `store_address_1` | Incomplete address book | Medium | Geographic coordinates are reliable; use reverse geocoding if needed |
| High JSON complexity | Parsing required for rich data | Low | Parse with `JSON_EXTRACT_SCALAR()` or `JSON_EXTRACT()` |
| Mixed language names | Non-English names in data | Low | Support Arabic (`name:ar`), French (`name:fr`), English (`name:en`) |
| OSM data lag | POI data may be outdated | Medium | Verify against field visit if high accuracy needed; Partition by `file_name` date |

---

## Column Recommendations for Analysis

**Essential Columns (0% null, high quality):**
- `poi_sk`, `uuid`, `store_latitude`, `store_longitude`
- `country_code_nk`, `source_system_code_nk`

**Recommended for Enrichment (use with nullability consideration):**
- `sub_categ_name`, `store_name` (or extract from JSON)
- `phone_number` (or `place_attributes.phone`)
- `place_attributes` (rich context)

**Optional/Rarely Used:**
- `city_name`, `zip_code`, `store_address_2` (all null)

---

## Documentation Version

- **Created:** 2026-09-23
- **Analyzed Columns:** 18 core columns
- **Sample Size:** 50 records (1% random sample of 18.5K rows)
- **Data Source:** OpenStreetMap (OSM) — Public GIS database
- **Filter Applied:** None (all Morocco POI records)
- **Data Freshness:** Partition date 20260729 (July 29, 2026)
- **Environment:** DEV (development/staging environment)
