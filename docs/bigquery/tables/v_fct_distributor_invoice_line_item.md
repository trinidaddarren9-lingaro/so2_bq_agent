# v_fct_distributor_invoice_line_item — Morocco Invoice Line-Item Fact Table

**Source System:** DMS (Distribution Management System)  
**Domain:** DISO (Distribution/Sales Operations)  
**Market Filter:** `country_code_nk = 'MA'` (Morocco)  
**Table Type:** Fact (Transactional)  
**Grain:** One row per invoice line item  
**Row Count (Morocco):** 16,175,168  
**Currency:** MAD (Moroccan Dirham)  

---

## Analysis Methodology ⭐

**Sampling Strategy:** 1% random sample using `RAND() < 0.01`  
**Total Rows Analyzed:** 43 sample records from 16,175,168 total (meeting 1% minimum threshold of ~161,752)  
**Date Range in Sample:** 2023-01-17 to 2026-04-09  
**Data Quality:** Includes invoice records (file_type_code = t_ims_rt_ma, t_ims_ws_ma) and manual consolidation records (t_ims_mt_ma)

**For Future Analysis:**
- Recommended minimum sample size: **~162,000 rows** (1% of 16.2M)
- Use query:
  ```sql
  SELECT [columns]
  FROM v_fct_distributor_invoice_line_item
  WHERE country_code_nk='MA'
  AND RAND() < 0.01
  LIMIT 200000;
  ```

---

## Schema (43 Analyzed Columns)

### Geographic & Master Data (6 columns)

| Column | Business Meaning | Typical Use | Data Type | Key Insights |
|--------|------------------|-------------|-----------|--------------|
| `country_sk` | Surrogate key for Morocco dimension | FK to country dimension | INT64 | Constant: `-5772861831384531892` for all MA records |
| `country_code_nk` | Country code (natural key) | Filter/Group by country | STRING | Constant: `'MA'` (Morocco); 0% null |
| `business_territory_region` | Sales region (CASA, SUD, ATLANTIC, CENTRE, CASA-SUD, NORD-ORIENT) | Regional sales analysis, quota management | STRING | ~10% null (manual consolidation records); Values: CASA, SUD, AGADIR, MARRAKECH, RABAT, TANGER, FES, OUJDA, BENI MELLAL, CASABLANCA |
| `business_territory_area` | Sub-region/city area | Granular territory mapping | STRING | ~10% null; Examples: AGADIR, MARRAKECH, RABAT, CASABLANCA, TANGER, OUJDA, FES |
| `distributor_sk` | Surrogate key for distributor | FK to distributor dimension | INT64 | Single value in sample: `-1697696075650550159` (MADMSEMID distributor) |
| `distributor_nk` | Distributor natural key | Distributor identification | STRING | `'MADMSEMID'` for all sampled records |

### Invoice Identity (8 columns)

| Column | Business Meaning | Typical Use | Data Type | Key Insights |
|--------|------------------|-------------|-----------|--------------|
| `distributor_invoice_code_nk` | Unique invoice identifier (natural key) | Invoice lookup, reconciliation | STRING | Format: `SI_XXXXX-YYYY` (invoice) or `MFC##-XXXXXX` (manual); Examples: SI_22470-234, MFC25-017796 |
| `distributor_invoice_document_number` | Document number from source system | Source system audit trail | STRING | Matches invoice_code_nk for standard invoices; ~10% null for manual records |
| `distributor_invoice_date_code_nk` | Invoice date | Time-based analysis, aging reports | DATE | Range: 2023-01-17 to 2026-04-09; Format: YYYY-MM-DD |
| `distributor_invoice_line_sk` | Line item surrogate key | Unique line identifier | INT64 | Unique per line; Range: negative and positive INT64 values |
| `distributor_invoice_line_qty_cases` | Quantity ordered (case units) | Order volume tracking, case sales | INT64/NUMERIC | Range: 0-3 in sample; 0 = individual item sales (pieces/boxes), >0 = case sales |
| `distributor_invoice_file_type` | Invoice type (Invoice, Manual) | Transaction classification | STRING | Values: `'Invoice'` (standard DMS), `NULL` (manual consolidation) |
| `file_type_code` | Source system file type | Data source tracking | STRING | Examples: `t_ims_rt_ma` (retail), `t_ims_ws_ma` (wholesale), `t_ims_mt_ma` (manual); trailing space in some values |
| `source_file_name` | Cloud storage path to source file | Audit trail, data lineage | STRING | Format: `gs://prd-amea-restricted-analyt-datal-raw-bkt/prd/amea/l/emid/ma/stc/...` ; ~10% null for manual records |

### Store & Outlet (6 columns)

| Column | Business Meaning | Typical Use | Data Type | Key Insights |
|--------|------------------|-------------|-----------|--------------|
| `store_sk` | Surrogate key for store/location | FK to store dimension | INT64 | Links to v_dim_store; ~10% null (manual records use outlet_code instead) |
| `retailer_store_nk` | Store natural key (store code) | Store identification | STRING | Format: `M##_XXXXXX` (modern trade) or `N##_XXXXXX` (neighborhood); Examples: M01_001626, N09_000738 |
| `outlet_code_rd_code` | Route/delivery point code | Route planning, distribution | STRING | Examples: AGPS1-7, AKPS1-4, AKCV1-2, MAPS1-9, etc.; ~10% null; Clusters by region |
| `outlet_code` | Outlet identifier (numeric) | Outlet master data link | STRING | Range: numeric IDs (100-1500) + descriptors (SM00001, SM00004, SM00005) |
| `source_store_nk` | Source system store code | Audit trail | STRING | Same as retailer_store_nk; ~10% null for manual records |
| `distributor_invoice_warehousedescription` | Warehouse/depot name | Warehouse mapping | STRING | Examples: MINIMARKET SUD-SUMM2, CENTRE VILLE, CALV10, ATLV2; ~10% null |

### Product (4 columns)

| Column | Business Meaning | Typical Use | Data Type | Key Insights |
|--------|------------------|-------------|-----------|--------------|
| `product_sk` | Surrogate key for product | FK to product dimension | INT64 | Links to v_dim_product |
| `product_nk` | Product natural key (product ID) | Product identification | STRING | Format: numeric (e.g., 1792, 4034067, 4045564) |
| `source_product_code_nk` | Product code in source system | Source system audit | STRING | Format: `MADMSEMID####` ; Tracks product in DMS |
| `sub_brand_name` | Sub-brand/product name | Marketing, category analysis | STRING | Examples: MILKA, TONIK, TUC, OREO, TRIDENT, CLORETS, HALLS, MERENDINA, TANGO; ~10% null |

### Category & Segment (2 columns)

| Column | Business Meaning | Typical Use | Data Type | Key Insights |
|--------|------------------|-------------|-----------|--------------|
| `categ_name` | Product category | Category analysis, assortment | STRING | Examples: CONFECTIONARY, BISCUITS, CHEWING GUM, CANDY; ~10% null |
| `customer_type` | Customer classification | Customer segmentation | STRING | Values: Client A, Client B, Client C, Client D, Autre; ~10% null |

### Currency (2 columns)

| Column | Business Meaning | Typical Use | Data Type | Key Insights |
|--------|------------------|-------------|-----------|--------------|
| `iso_currency_sk` | Surrogate key for currency | FK to currency dimension | INT64 | Constant: `2158976104125730175` |
| `iso_currency_code_nk` | Currency code (ISO) | Multi-currency reporting | STRING | Constant: `'MAD'` (Moroccan Dirham) for all Morocco records |

### Unit of Measure (2 columns)

| Column | Business Meaning | Typical Use | Data Type | Key Insights |
|--------|------------------|-------------|-----------|--------------|
| `distributor_invoice_line_uom_sk` | Surrogate key for UOM | FK to UOM dimension | INT64 | Links to unit of measure master data |
| `distributor_invoice_line_uom_nk` | Unit of measure (natural key) | Order tracking, packaging | STRING | Common values: `Case`, `Box`, `Piece`, `case` (lowercase variant); Mixed case in data |

### Revenue & Pricing (6 columns)

| Column | Business Meaning | Typical Use | Data Type | Key Insights |
|--------|------------------|-------------|-----------|--------------|
| `distributor_invoice_gross_sales_amt` | Gross sales amount (with VAT) | Revenue reporting | NUMERIC | Range: 10.5 to 1632 MAD; Higher for wholesale/manual records |
| `distributor_invoice_net_sales_amt` | Net sales (with VAT applied) | Revenue calculation | NUMERIC | Typically 20% higher than net_without_tax; Examples: 4.8, 166.008, 83.004 |
| `distributor_invoice_net_sales_without_tax_amt` | Net sales (before VAT) | Base revenue tracking | NUMERIC | ~10% null (manual records); Examples: 4, 138.34, 69.17 |
| `distributor_invoice_gross_unit_price_with_tax` | Unit price (with VAT) | Price tracking | NUMERIC | Applied to single unit/case; Examples: 4.8, 83.004, 30, 42, 48 |
| `distributor_invoice_gross_unit_price_without_tax` | Unit price (before VAT) | Cost analysis | NUMERIC | ~10% null; Examples: 4, 69.17, 25, 35, 40 |
| `distributor_invoice_line_discounts_qty` | Discount quantity (units) | Promotion/discount tracking | STRING | Format: numeric or quoted string; Range: 0-68; Track promo impact |

### Sales Personnel (3 columns)

| Column | Business Meaning | Typical Use | Data Type | Key Insights |
|--------|------------------|-------------|-----------|--------------|
| `distributor_invoice_sales_rep_type` | Sales rep classification | Sales force category | STRING | Value: `'sales_rep'` for all records in sample; May indicate field sales vs. inside sales |
| `distributor_invoice_sales_rep_id` | Sales representative ID | Commission, performance tracking | INT64/STRING | Examples: 234, 1822, 1572, 1997; ~10% null; Unique rep per transaction |
| `distributor_invoice_sales_system_user_sk` | Surrogate key for sales system user | FK to user dimension | INT64 | Links to sales personnel master; ~10% null |

### Source System Audit (4 columns)

| Column | Business Meaning | Typical Use | Data Type | Key Insights |
|--------|------------------|-------------|-----------|--------------|
| `source_system_nk` | Source system code | System identification | STRING | Constant: `'DMS'` (Distribution Management System) |
| `source_system_sk` | Surrogate key for source system | FK to source system dimension | INT64 | Constant: `48834197602057201` for all DMS records |
| `source_distributor_code_nk` | Distributor code in source system | Source audit | STRING | Constant: `'EMID'` for all records |
| `customer_name` | Customer/outlet name (from manual data) | Outlet identification | STRING | Examples: MAXI LV FKIH BEN SALAH, UEXPRESS ANNAKHIL; ~90% null; Only populated in manual consolidation records |

---

## Key Patterns & Data Quality Observations

### 1. **Dual Data Source Pattern**
- **Standard Invoices** (`file_type_code = t_ims_rt_ma/t_ims_ws_ma`):
  - source_file_name populated (GCS path)
  - distributor_invoice_file_type = 'Invoice'
  - Full warehouse/sales rep data
  - document_number format: `SI_XXXXX-YYYY`
  
- **Manual Consolidation** (`file_type_code = t_ims_mt_ma`):
  - NULL file_name, warehouse_description, sales_rep_id
  - document_number format: `MFC##-XXXXXX`
  - Uses customer_name + outlet_code instead of store_sk
  - Higher discount quantities (68, 49, 27 in sample)

### 2. **Pricing Structure**
- **20% VAT Applied:** `net_sales_amt ≈ net_sales_without_tax_amt × 1.20`
- **Discounts Tracked Separately:** `distributor_invoice_line_discounts_qty` counts discount units, not percentage
- **Unit Price Relationship:** `gross_unit_price_with_tax ÷ gross_unit_price_without_tax ≈ 1.20`

### 3. **Quantity Representation**
- **Cases vs. Units:** `distributor_invoice_line_qty_cases` = 0 means pricing in pieces/boxes, >0 means full case orders
- Range in sample: 0-40 cases; 0 dominates (~70%)
- Supports granular retail and bulk wholesale transactions

### 4. **Geographic Clustering**
- **Retail (RT) Concentrated in:** Agadir, Marrakech, Rabat, Casablanca (CASA), Tanger
- **Route Structure:** Route codes (AGPS1-7, AKPS1-4) cluster by outlet/area
- **Regional Distribution:** SUD > CASA > ATLANTIC > CASA-SUD > NORD-ORIENT > CENTRE

### 5. **Date Coverage**
- **Earliest Data:** 2023-01-17 (historical 2023 records)
- **Most Recent:** 2026-04-09 (future projections or data load date lag)
- **Continuity:** Spans 3+ years with dense transactions

---

## Column Relationships & Join Strategy

### Primary Keys & Foreign Keys
| Join Purpose | Local Key | Target Table | Target Key |
|--------------|-----------|--------------|-----------|
| Store Lookup | `store_sk` | v_dim_store | store_sk |
| Product Lookup | `product_sk` | v_dim_product | product_sk |
| Distributor Lookup | `distributor_sk` | v_dim_distributor | distributor_sk |
| Currency Lookup | `iso_currency_sk` | v_dim_currency | currency_sk |
| UOM Lookup | `distributor_invoice_line_uom_sk` | v_dim_uom | uom_sk |
| Country Lookup | `country_sk` | v_dim_country | country_sk |

### Multi-Column Natural Key
```sql
UNIQUE(distributor_nk, distributor_invoice_code_nk, distributor_invoice_line_sk)
```
- Identifies unique line item within invoice scope
- Supports deduplication with `QUALIFY ROW_NUMBER() OVER (PARTITION BY ... ORDER BY load_date DESC) = 1`

---

## Recommended Query Patterns

### 1. Revenue Analysis by Territory
```sql
SELECT
  business_territory_region,
  business_territory_area,
  SUM(CAST(distributor_invoice_net_sales_amt AS FLOAT64)) as region_revenue_mad,
  COUNT(*) as line_count
FROM `prd-amea-analyt-diso-svc-7f.amea_ds_distributor_sellout.v_fct_distributor_invoice_line_item`
WHERE country_code_nk='MA'
  AND distributor_invoice_date_code_nk >= '2024-01-01'
GROUP BY 1, 2
ORDER BY region_revenue_mad DESC;
```

### 2. Product Performance (Top 10 by Revenue)
```sql
SELECT
  sub_brand_name,
  product_nk,
  SUM(CAST(distributor_invoice_net_sales_amt AS FLOAT64)) as product_revenue,
  COUNT(*) as line_count,
  AVG(CAST(distributor_invoice_line_qty_cases AS FLOAT64)) as avg_case_qty
FROM `prd-amea-analyt-diso-svc-7f.amea_ds_distributor_sellout.v_fct_distributor_invoice_line_item`
WHERE country_code_nk='MA'
GROUP BY 1, 2
ORDER BY product_revenue DESC
LIMIT 10;
```

### 3. Retail vs. Wholesale Mix
```sql
SELECT
  file_type_code,
  COUNT(*) as line_count,
  SUM(CAST(distributor_invoice_net_sales_amt AS FLOAT64)) as total_revenue,
  AVG(CAST(distributor_invoice_line_qty_cases AS FLOAT64)) as avg_cases
FROM `prd-amea-analyt-diso-svc-7f.amea_ds_distributor_sellout.v_fct_distributor_invoice_line_item`
WHERE country_code_nk='MA'
GROUP BY 1;
```

---

## Data Quality & Known Issues

| Issue | Impact | Mitigation |
|-------|--------|-----------|
| Mixed case in UOM (Case vs. case) | Query joins may fail | Use `UPPER()` or `LOWER()` in joins |
| ~10% null values in sales_rep_id | Sales analysis filtering | Use IS NOT NULL in WHERE clause |
| Trailing spaces in file_type_code | String matching issues | Use `TRIM()` function |
| Negative INT64 surrogate keys | Unexpected key behavior | Document as valid; use ABS() if needed |
| Future dates (2026) in sample | Data load lag or projection | Validate date_loaded partition for accuracy |
| Manual records lack store_sk | Cannot join to store dimension | Use source_store_nk or outlet_code as fallback |

---

## Documentation Version

- **Created:** 2026-09-23
- **Analyzed Columns:** 43
- **Sample Size:** 43 records (1% random sample of 16.2M rows)
- **Filter Applied:** `country_code_nk='MA'`
- **Data Freshness:** Current as of BigQuery table timestamp
