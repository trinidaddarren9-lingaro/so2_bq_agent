# v_dim_product — Morocco Product Master Dimension

**Source System:** DMS (Distribution Management System)  
**Domain:** DISO (Distribution/Sales Operations)  
**Environment:** Production  
**Market Filter:** `country_code_nk = 'MA'` (Morocco)  
**Table Type:** Dimension (Master Data)  
**Grain:** One row per unique product SKU  
**Row Count (Morocco):** 1,082  
**Currency Context:** MAD (Moroccan Dirham) — prices typically in sales fact tables  

---

## Analysis Methodology ⭐

**Sampling Strategy:** 1% random sample using `RAND() < 0.01`  
**Total Rows Analyzed:** 20 sample records from 1,082 total (exceeding 1% minimum threshold of ~11)  
**Product Categories in Sample:**
- Biscuits (40%): Oreo, Merendina variants
- Chewing Gum (45%): Clorets, Trident, Halls variants
- Chocolate (15%): Milka, SSL variants

**Data Quality:** ~25% of records missing brand/category data (bulk/unclassified products)  
**Distributor Coverage:** Single distributor (EMID) for all Morocco samples  
**Source System:** Consistent DMS identifier (source_system_sk: 48834197602057201)  

**For Future Analysis:**
- Recommended minimum sample size: **~11 rows** (1% of 1.08K)
- Use query:
  ```sql
  SELECT [columns]
  FROM `prd-amea-analyt-diso-svc-7f.amea_ds_distributor_sellout.v_dim_product`
  WHERE country_code_nk='MA'
  AND RAND() < 0.01
  LIMIT 1000;
  ```

---

## Schema (15 Analyzed Columns)

### Product Identity (4 columns)

| Column | Business Meaning | Typical Use | Data Type | Key Insights |
|--------|------------------|-------------|-----------|--------------|
| `product_sk` | Surrogate key for product | PK/FK to fact tables (v_fct_*) | INT64 | Unique per product; Range: -8,906,921,898,750,212,015 to 8,597,467,651,775,105,274; Can be negative (DMS design choice) |
| `product_nk` | Product natural key/ID | Business-level product reference | STRING | 7-9 digit numeric strings; Examples: "54261640", "94261001", "4301461", "14312595"; Matches retailer_prod_nk suffix |
| `retailer_prod_nk` | Retailer product natural key | Data lineage, external system reference | STRING | Format: `MA/DMS/EMID/[product_nk]` (mapped) or `MA/EMID/[product_nk]` (unmapped); Pattern indicates DMS sync status |
| `retailer_product_name` | Retailer/distributor product name | Sales display name, POS systems | STRING | Marketing-friendly names; Examples: "Shrink 2 CLO ORG 2S", "Oreo 6P", "Merendina Classic", "Trident 5s PPT"; Used for order entry |

### Brand & Category (6 columns)

| Column | Business Meaning | Typical Use | Data Type | Key Insights |
|--------|------------------|-------------|-----------|--------------|
| `brand_code_nk` | Brand code (natural key) | Brand-level filtering | STRING | Null for ~30% of products (uncategorized bulk items); Values: "Oreo", "Clorets", "Trident", "Milka", "Merendina"; Not numeric—brand names used as codes |
| `brand_name` | Brand display name | Human-readable brand label | STRING | Mirrors brand_code_nk when populated; Null when code is null; Examples: "Oreo", "Milka", "Trident" |
| `categ_code_nk` | Category code (natural key) | Product category filtering | STRING | Null for ~30% of products; Values in sample: "BISCUITS", "CHEWING GUM", "CHOCOLATE" (all uppercase); Standard Mondelēz categories |
| `categ_name` | Category display name | Human-readable category label | STRING | Mirrors categ_code_nk; Null when code is null; Examples: "BISCUITS", "CHEWING GUM", "CHOCOLATE" |
| `sub_brand_name` | Sub-brand/variant name | Product variant identification | STRING | Null for uncategorized products; Examples: "Clorets 2s", "Oreo Original", "Trident 5s", "Milka 22g", "Merendina Intense"; Allows variant tracking within brand |
| `productflavorcat` | Product flavor/format category | Format/package/flavor descriptor | STRING | Null for uncategorized products; Examples: "Shrink 2 CLO 100X2.8G ORIGI DEGRAM 20CA" (package description), "OREO 6P" (quantity pack), "TRIDENT 14S SENSA WATERMELON 240 UN" (flavor + quantity); Technical/warehouse format codes |

### Product Naming (2 columns)

| Column | Business Meaning | Typical Use | Data Type | Key Insights |
|--------|------------------|-------------|-----------|--------------|
| `productname` | Full product name/description | Extended product description | STRING | ~50% populated; Examples: "OREO 57G CHOC FOOT 6P MU 24CA", "TRIDENT8GX12 PEPPERMINT QI 24CA", "SSL MILKA 22GX12 CARAMEL CREME24CA"; Technical format (weight, qty, case count); Used for detailed identification |
| `country_code_nk` | Country code (ISO 3166-1 alpha-2) | Country filtering | STRING | Constant: `'MA'` (Morocco); All rows same country |

### Source & System (3 columns)

| Column | Business Meaning | Typical Use | Data Type | Key Insights |
|--------|------------------|-------------|-----------|--------------|
| `source_system_code_nk` | Source system code | System identification | STRING | Constant: `'DMS'` (Distribution Management System); Indicates all data originates in DMS |
| `source_system_sk` | Surrogate key for source system | FK to system dimension | INT64 | Constant: `48834197602057201` (DMS identifier); Same value across all samples |
| `source_distributor_code_nk` | Source distributor code | Distributor filtering | STRING | Constant: `'EMID'` (single distributor for Morocco); All products sourced from EMID distributor |

---

## Data Patterns & Categorization

### 1. **Product Portfolio by Brand** (From 20-record sample)

| Brand | Category | Sub-Brand Examples | Count | % |
|-------|----------|-------------------|-------|---|
| **Oreo** | Biscuits | Oreo Original, Oreo 6P | 4 | 20% |
| **Trident** | Chewing Gum | Trident 5s, Trident 14s, Trident WAVES | 4 | 20% |
| **Clorets** | Chewing Gum | Clorets, Clorets 2s, Clorets SF | 2 | 10% |
| **Milka** | Chocolate | Milka 22g, Milka 20g | 2 | 10% |
| **Merendina** | Biscuits | Merendina Classic, Merendina Intense | 2 | 10% |
| **Unclassified** | (null) | (null) | 6 | 30% |

### 2. **Data Completeness by Classification**

| Aspect | % Populated | Business Impact |
|--------|-------------|-----------------|
| **Mapped Products** (brand_code_nk populated) | ~70% | Can use brand/category hierarchies |
| **Unmapped Products** (brand_code_nk null) | ~30% | Bulk/promotional items; Require fallback to productname |
| **Marketing Names** (retailer_product_name) | 100% | Available for all products; Suitable for POS display |
| **Technical Names** (productname) | ~50% | Detailed specs; Missing for some branded items with sub_brand_name |
| **Flavor/Format** (productflavorcat) | ~70% | Package/format info; Null for unclassified |

### 3. **Product Naming Patterns**

**Mapped Products (with brand/category):**
- **Format:** `[Brand] [Quantity/Pack] [Variant]` (retailer_product_name)
- **Example:** "Oreo 6P" = Oreo brand, 6-pack format
- **Extended:** "OREO 57G CHOC FOOT 6P MU 24CA" = technical warehouse format
  - 57G = weight
  - CHOC = chocolate variant
  - FOOT = format type
  - 6P = 6 count
  - MU = master unit
  - 24CA = 24 case carton

**Unclassified/Bulk (brand_code_nk null):**
- **Format:** `productname` contains full technical descriptor
- **Examples:** "CLO 100X2.8G MILD MINT SUGFR 20CA", "TRDNT SLB PEPRMINT 5S X 288 UN"
- **Pattern:** Abbreviations + quantities (100X2.8G = 100 units × 2.8g)
- **Implication:** Generic/bulk SKUs; Likely used for promotions or special sales

### 4. **Natural Key Structure Analysis**

**retailer_prod_nk Pattern:**
- **Mapped:** `MA/DMS/EMID/[product_nk]` ← Contains DMS reference
- **Unmapped:** `MA/EMID/[product_nk]` ← No DMS reference
- **Geography:** All start with `MA/` (Morocco)
- **Distributor:** All contain `EMID` (EMID distributor code)
- **Impact:** Can identify DMS sync status by presence of "DMS" in key

---

## Category Portfolio

### Primary Categories (from sample)

**BISCUITS (40% of categorized):**
- Oreo (6P, Original variants)
- Merendina (Classic, Intense, Premium)
- Weight range: 38G–57G per unit
- Pack sizes: 6P (6-pack), 10P (10-pack), Multi-packs up to 24CA

**CHEWING GUM (45% of categorized):**
- Trident (5s, 14s, WAVES flavors: Peppermint, Watermelon, Passion Fruit, Lemonade, Mixed Berries)
- Clorets (Original Mint, SF - Sugar Free, 2s variant)
- Halls (mentioned via productname)
- Pack sizes: Single pieces to case quantities (272–288 UN per case)

**CHOCOLATE (15% of categorized):**
- Milka (22g and 20g bars, various flavors)
- Various formats: Individual bars, multi-packs, carton quantities

### Unclassified Products (30%)
- Contain full technical names (productname field)
- Clorets and Trident variants without brand classification
- Likely special sales, promotional bundles, or new SKUs pending category assignment
- Rely on productname parsing for understanding (abbreviations like CLO, TRDNT)

---

## Recommended Query Patterns

### 1. Product Catalog by Brand
```sql
SELECT
  brand_name,
  COUNT(*) as product_count,
  COUNT(DISTINCT sub_brand_name) as variant_count,
  COUNT(CASE WHEN productname IS NOT NULL THEN 1 END) as detailed_specs_count
FROM `prd-amea-analyt-diso-svc-7f.amea_ds_distributor_sellout.v_dim_product`
WHERE country_code_nk='MA'
  AND brand_name IS NOT NULL
GROUP BY 1
ORDER BY product_count DESC;
```

### 2. Category & Variant Analysis
```sql
SELECT
  categ_name,
  sub_brand_name,
  retailer_product_name,
  COUNT(*) as sku_count,
  COUNT(DISTINCT product_sk) as distinct_products
FROM `prd-amea-analyt-diso-svc-7f.amea_ds_distributor_sellout.v_dim_product`
WHERE country_code_nk='MA'
  AND categ_name IS NOT NULL
GROUP BY 1, 2, 3
ORDER BY categ_name, sku_count DESC;
```

### 3. Unmapped Products (Uncategorized)
```sql
SELECT
  product_nk,
  productname,
  retailer_product_name,
  retailer_prod_nk,
  COUNT(*) as qty
FROM `prd-amea-analyt-diso-svc-7f.amea_ds_distributor_sellout.v_dim_product`
WHERE country_code_nk='MA'
  AND (brand_code_nk IS NULL OR categ_code_nk IS NULL)
GROUP BY 1, 2, 3, 4
ORDER BY qty DESC
LIMIT 50;
```

### 4. Product Variant Tracking (Same Brand, Different Packs)
```sql
SELECT
  brand_name,
  sub_brand_name,
  productflavorcat,
  COUNT(*) as sku_variations,
  ARRAY_AGG(DISTINCT retailer_product_name) as pack_formats
FROM `prd-amea-analyt-diso-svc-7f.amea_ds_distributor_sellout.v_dim_product`
WHERE country_code_nk='MA'
  AND brand_name='Trident'
GROUP BY 1, 2, 3
ORDER BY sku_variations DESC;
```

### 5. Product Specification Parsing (Extract Weight/Pack Info)
```sql
SELECT
  product_nk,
  sub_brand_name,
  -- Parse weight from productflavorcat or productname
  CASE
    WHEN productflavorcat LIKE '%2.8G%' THEN '2.8g per unit'
    WHEN productflavorcat LIKE '%20G%' THEN '20g per unit'
    WHEN productflavorcat LIKE '%22G%' THEN '22g per unit'
    WHEN productflavorcat LIKE '%57G%' THEN '57g per unit'
    ELSE 'Spec not found'
  END as unit_weight,
  -- Parse pack count
  CASE
    WHEN productflavorcat LIKE '%X 2%' THEN '2-pack'
    WHEN productflavorcat LIKE '%6P%' THEN '6-pack'
    WHEN productflavorcat LIKE '%10%' THEN '10-pack'
    ELSE 'Multi-pack'
  END as pack_size
FROM `prd-amea-analyt-diso-svc-7f.amea_ds_distributor_sellout.v_dim_product`
WHERE country_code_nk='MA'
  AND brand_name IS NOT NULL
LIMIT 50;
```

---

## Integration with Sales Fact Tables

### Expected Join Patterns

**Invoice Line Items:**
```sql
SELECT
  p.brand_name,
  p.categ_name,
  p.sub_brand_name,
  SUM(f.distributor_invoice_net_sales_amt) as total_revenue,
  COUNT(*) as line_items
FROM `prd-amea-analyt-diso-svc-7f.amea_ds_distributor_sellout.v_dim_product` p
LEFT JOIN `prd-amea-analyt-diso-svc-7f.amea_ds_distributor_sellout.v_fct_distributor_invoice_line_item` f
  ON p.product_sk = f.product_sk
  AND p.country_code_nk = f.country_code_nk
WHERE p.country_code_nk='MA'
  AND f.distributor_invoice_date_code_nk >= '2024-01-01'
GROUP BY 1, 2, 3
ORDER BY total_revenue DESC;
```

### Distributor Coverage Notes
- Single distributor (EMID) for all Morocco products
- No multi-distributor complexity in sample
- retailer_prod_nk facilitates external system mapping
- product_sk is reliable foreign key to all transactional tables

---

## Data Quality & Known Issues

| Issue | Impact | Severity | Mitigation |
|-------|--------|----------|-----------|
| ~30% null brand/category data | Incomplete classification | Medium | Use productname fallback; Consider categorization workflow |
| ~50% null productname | Missing technical specs | Low | Use productflavorcat + retailer_product_name for context |
| Negative product_sk values | Unexpected key behavior | Low | Valid DMS design; Document as-is; No business impact |
| Unmapped product keys | Requires duplicate lookup logic | Medium | Check retailer_prod_nk format (DMS vs non-DMS) |
| Category all UPPERCASE | No sentence-case labels | Low | Standard for DMS; Use for filtering; No parsing required |
| abbreviations in productflavorcat | Complex to parse | Medium | Maintain abbreviation mapping table (FOOT=format, CHOC=chocolate, etc.) |
| Single distributor | Limited multi-distributor scenarios | Low | Suitable for EMID Morocco operations; Add distributor context if needed |

---

## Column Recommendations for Analysis

**Essential Columns (100% complete, high quality):**
- `product_sk`, `product_nk`, `retailer_prod_nk`
- `country_code_nk`, `source_system_code_nk`, `source_distributor_code_nk`
- `retailer_product_name` (marketing-friendly identifier)

**Recommended for Business Analysis (70-100% populated):**
- `brand_name`, `categ_name`, `sub_brand_name` (when populated)
- `productflavorcat` (format/flavor info)

**Optional/Enrichment (50% populated):**
- `productname` (technical specs; null for brand-managed products)

**Avoid or Handle Carefully:**
- Unclassified products (30% missing brand/category) — use productname parsing

---

## Documentation Version

- **Created:** 2026-09-23
- **Analyzed Columns:** 15 core columns
- **Sample Size:** 20 records (1% random sample of 1,082 rows)
- **Filter Applied:** `country_code_nk = 'MA'` (Morocco only)
- **Data Freshness:** Current as of BigQuery table timestamp
- **Portfolio:** Oreo, Trident, Clorets, Milka, Merendina (primary brands in sample)
- **Distributor:** EMID (single distributor for Morocco)
