# product_master — Schema Mapping Guide

**Target Schema:** product_master (L1/Data Warehouse layer)  
**Source Tables:** v_dim_product (primary), v_fct_distributor_invoice_line_item (enrichment)  
**Market Focus:** Morocco (MA)  
**Grain:** One row per unique product/SKU  
**Primary Key:** product_sok (Surrogate Object Key — hashed identifier)  
**Status:** Mapping Framework (Store & Invoice Tables Only)  

---

## Complete Column Mapping Table

| # | product_master Column | Data Type | NOT NULL | BigQuery Source | Source Column | Transformation | Coverage | Notes |
|----|----------------------|-----------|----------|-----------------|---------------|-----------------|----------|-------|
| 1 | `product_sok` | STRING | YES | Derived | N/A | SHA256(country_iso_code \|\| mdlz_sku_code) | ✅ 100% | Surrogate key; Hash combines country + MDLz SKU for uniqueness; PK |
| 2 | `country_iso_code` | STRING | YES | v_dim_product | country_code_nk | UPPER(TRIM(country_code_nk)) | ✅ 100% | Morocco = 'MA'; Constant for Morocco dataset; FK to country dimension |
| 3 | `mdlz_sku_code` | STRING | YES | v_dim_product | product_nk | TRIM(product_nk) KEEP CASE | ✅ 100% | Product natural key; Format: numeric SKU (e.g., 1792, 4034067); Delivery key |
| 4 | `basecode` | STRING | YES | MISSING | N/A | NULL | ❌ 0% | Gap: No basecode/material code in v_dim_product; Requires external product master or source system |
| 5 | `product_name` | STRING | NO | v_dim_product | productname | UPPER(TRIM(productname)) | ⚠️ ~70% | Product display name; ~30% null (unclassified/bulk items); Examples: OREO, MILKA, TRIDENT |
| 6 | `variant_name` | STRING | NO | v_fct_distributor_invoice_line_item | sub_brand_name | UPPER(TRIM(sub_brand_name)) | ⚠️ ~90% | Variant/product variant name; ~10% null in transactions; Fallback to sub_brand_name |
| 7 | `variant_sku` | STRING | NO | v_fct_distributor_invoice_line_item | source_product_code_nk | UPPER(TRIM(source_product_code_nk)) | ⚠️ ~90% | Variant SKU in source system; Format: MADMSEMID#### (~10% null in manual records) |
| 8 | `variant_weight_gram` | DOUBLE | NO | MISSING | N/A | NULL | ❌ 0% | Gap: No weight data in v_dim_product or invoices; Requires external product specification master |
| 9 | `ean` | STRING | NO | MISSING | N/A | NULL | ❌ 0% | Gap: No EAN/GTIN barcode in v_dim_product or invoices; Requires external master or GS1 data |
| 10 | `packsize` | STRING | NO | v_fct_distributor_invoice_line_item | distributor_invoice_line_uom_nk | UPPER(TRIM(distributor_invoice_line_uom_nk)) | ⚠️ ~100% (limited) | Pack-size descriptor from UOM; Values: Case, Box, Piece; Limited detail but 100% transaction coverage |
| 11 | `affordability` | DOUBLE | NO | v_fct_distributor_invoice_line_item | distributor_invoice_gross_unit_price_with_tax | CAST(distributor_invoice_gross_unit_price_with_tax AS FLOAT64) | ⚠️ ~90% | Price-tier indicator derived from unit price; ~10% null (manual consolidation records) |
| 12 | `ppg_code` | STRING | NO | MISSING | N/A | NULL | ❌ 0% | Gap: Price Package Group not in v_dim_product or invoices; Requires separate pricing hierarchy master |
| 13 | `subbrand_name` | STRING | NO | v_dim_product + v_fct | sub_brand_name | UPPER(TRIM(COALESCE(vfct.sub_brand_name, vdim.sub_brand_name))) | ⚠️ ~90% | Sub-brand display name; ~10% null in both sources; Examples: MILKA, TONIK, TUC, OREO, TRIDENT |
| 14 | `brand_name` | STRING | NO | v_dim_product | brand_name | UPPER(TRIM(brand_name)) | ⚠️ ~70% | Brand display name; ~30% null (unclassified/promotional items); L3 brand-monthly grain |
| 15 | `subcategory_name` | STRING | NO | MISSING | N/A | NULL | ❌ 0% | Gap: No subcategory in v_dim_product (only categ_name); Requires additional hierarchy level |
| 16 | `category_name` | STRING | NO | v_dim_product + v_fct | categ_name | UPPER(TRIM(COALESCE(vfct.categ_name, vdim.categ_name))) | ⚠️ ~90% | Category display name; ~10% null (manual records); Examples: CONFECTIONARY, BISCUITS, CHEWING GUM |
| 17 | `subsegment_name` | STRING | NO | MISSING | N/A | NULL | ❌ 0% | Gap: No subsegment in sources; Requires external category/segment hierarchy master |
| 18 | `segment_name` | STRING | NO | MISSING | N/A | NULL | ❌ 0% | Gap: No segment in sources; Requires external product segment classification master |

**Coverage Summary (Store & Invoice Tables Only):**
- ✅ **2/18 columns (11%)** — 100% complete; Direct constant mapping
- ⚠️ **6/18 columns (33%)** — Partial coverage (70-100%); Available from v_dim_product or v_fct with minor nulls
- ❌ **10/18 columns (56%)** — 0% coverage; Missing data sources; Requires external product masters

---

## Executive Summary

The `product_master` table is a comprehensive product reference layer designed for SKU-level analytics and category-based rule scoping. Based on analysis of two BigQuery source tables (v_dim_product, v_fct_distributor_invoice_line_item), the mapping framework identifies data sources, transformations, and coverage gaps.

---

## Source Data Coverage (Store & Invoice Tables Only)

**Primary Source:** v_dim_product (1,082 Morocco products)
- ✅ Core identity: product_sok, country_iso_code, mdlz_sku_code (product_nk)
- ⚠️ Taxonomy: brand_name (~70%), category_name (~90%), sub_brand_name (~90%)
- ⚠️ Display Names: productname (~70% populated; 30% unclassified)
- ❌ Basecode, variant details, weight, EAN, affordability, PPG code, segment/subsegment hierarchy

**Secondary Source:** v_fct_distributor_invoice_line_item (16.2M Morocco transactions)
- ✅ Transactional enrichment: source_product_code_nk, sub_brand_name, categ_name (~90% populated)
- ⚠️ Pricing Data: distributor_invoice_gross_unit_price_with_tax (can derive affordability; ~10% null)
- ⚠️ UOM: distributor_invoice_line_uom_nk (packsize descriptor; 100% coverage but limited detail)
- ❌ Weight, EAN, PPG code, segment hierarchy

**Coverage Gap Analysis:**
- v_dim_product contains ~15 columns analyzed from 20-record 1% sample
- v_fct contains ~43 columns; product-related fields limited to 4 (product_sk, product_nk, source_product_code_nk, sub_brand_name, categ_name)
- No product specification data (weight, EAN, basecode, PPG) in either source

---

## Implementation Roadmap

### Phase 1: MVP Core Product Mapping (High Priority) — 70% Coverage

**Goal:** Create product_master with directly mappable columns from v_dim_product

**Steps:**
1. ✅ Use v_dim_product as primary source (1,082 Morocco products)
2. ✅ Derive product_sok using SHA256(country_iso_code || mdlz_sku_code)
3. ✅ Map mdlz_sku_code directly from product_nk (natural key; no transformation)
4. ✅ Map product_name from productname (~70% coverage; NULL for 30% unclassified)
5. ✅ Map brand_name from brand_name (~70% coverage; NULL for promotional items)
6. ✅ Map category_name from categ_name (~90% coverage; ~10% null)
7. ✅ Map subbrand_name from sub_brand_name (~90% coverage)
8. ✅ Set constant value: country_iso_code='MA'

**SQL Pattern:**
```sql
SELECT
  TO_HEX(SHA256(CONCAT('MA', '::', product_nk))) as product_sok,
  'MA' as country_iso_code,
  product_nk as mdlz_sku_code,
  NULL as basecode,  -- TBD: Requires external master
  productname as product_name,
  NULL as variant_name,  -- Will populate in Phase 1b
  NULL as variant_sku,
  NULL as variant_weight_gram,
  NULL as ean,
  NULL as packsize,  -- Will populate in Phase 1b
  NULL as affordability,  -- Will populate in Phase 1b
  NULL as ppg_code,
  sub_brand_name as subbrand_name,
  brand_name,
  NULL as subcategory_name,
  categ_name as category_name,
  NULL as subsegment_name,
  NULL as segment_name
FROM `prd-amea-analyt-diso-svc-7f.amea_ds_distributor_sellout.v_dim_product`
WHERE country_code_nk='MA'
```

**Expected Output:** 1,082 product rows; 8/18 columns populated; 10 columns NULL

### Phase 1b: Transaction-Based Variant & Pricing Enhancement (High Priority)

**Goal:** Populate variant, UOM, and affordability from invoice transactions

**Steps:**
1. JOIN v_dim_product to v_fct_distributor_invoice_line_item on product_sk
2. Derive variant_name from sub_brand_name (transactional variant identifier)
3. Derive variant_sku from source_product_code_nk (source system variant code)
4. Derive packsize from distributor_invoice_line_uom_nk (UOM as pack descriptor)
5. Derive affordability from AVG(distributor_invoice_gross_unit_price_with_tax) per product
6. COALESCE(vfct.sub_brand_name, vdim.sub_brand_name) for subbrand_name and category_name

**SQL Pattern:**
```sql
WITH product_variant_pricing AS (
  SELECT
    vdim.product_sk,
    vdim.product_nk,
    vfct.sub_brand_name as transactional_variant_name,
    vfct.source_product_code_nk as transactional_variant_sku,
    vfct.distributor_invoice_line_uom_nk as transactional_packsize,
    AVG(vfct.distributor_invoice_gross_unit_price_with_tax) as avg_unit_price,
    COALESCE(vfct.sub_brand_name, vdim.sub_brand_name) as refined_subbrand,
    COALESCE(vfct.categ_name, vdim.categ_name) as refined_category
  FROM `prd-amea-analyt-diso-svc-7f.amea_ds_distributor_sellout.v_dim_product` vdim
  LEFT JOIN `prd-amea-analyt-diso-svc-7f.amea_ds_distributor_sellout.v_fct_distributor_invoice_line_item` vfct
    ON vdim.product_sk = vfct.product_sk
    AND vfct.country_code_nk='MA'
  WHERE vdim.country_code_nk='MA'
  GROUP BY vdim.product_sk, vdim.product_nk, vfct.sub_brand_name, vfct.source_product_code_nk, 
           vfct.distributor_invoice_line_uom_nk, vdim.sub_brand_name, vdim.categ_name, vfct.categ_name
)
UPDATE product_master pm
SET 
  variant_name = pvp.transactional_variant_name,
  variant_sku = pvp.transactional_variant_sku,
  packsize = pvp.transactional_packsize,
  affordability = pvp.avg_unit_price,
  subbrand_name = pvp.refined_subbrand,
  category_name = pvp.refined_category
FROM product_variant_pricing pvp
WHERE pm.mdlz_sku_code = pvp.product_nk AND pm.country_iso_code='MA'
```

**Expected Output:** All 1,082 products with variant_name, variant_sku, packsize, affordability populated (~90% coverage); subbrand_name and category_name refined; 8/18 columns now populated + 6 enhanced

### Phase 2: Product Specification Hierarchy (Medium Priority)

**Goal:** Add basecode, subcategory, subsegment, and segment from external product master

**Steps:**
1. Obtain basecode/material code mapping from DMS product master or Mondelēz standard catalog
2. Implement subcategory_name (requires additional hierarchy level beyond categ_name)
3. Implement subsegment_name and segment_name (requires category-to-segment mapping)
4. Join product_master to external master on mdlz_sku_code or product_nk

**Expected Coverage:** 100% for mapped fields; Requires external master availability

---

## Known Constraints & Assumptions

### Data Constraints
1. **Source Limitation:** Only v_dim_product + v_fct_distributor_invoice_line_item; No product specification data (weight, EAN, basecode)
2. **Single Market:** Morocco only (country_iso_code = 'MA')
3. **Product Sample Size:** 1,082 unique products; v_dim_product 1% sample analyzed (20 records)
4. **Null Distribution:** ~30% of products have NULL product_name (unclassified/promotional items); ~10% null brand_name
5. **Transaction Bias:** Variant data skewed toward frequently-invoiced products; Rare SKUs may have sparse transaction data

### Business Assumptions
1. **mdlz_sku_code = product_nk:** Product natural key serves as SKU identifier
2. **Variant from Sub-Brand:** sub_brand_name treated as variant indicator (e.g., MILKA, OREO, TRIDENT)
3. **No Multi-Level Hierarchy:** Category_name is leaf level; subcategory/segment require external master
4. **Affordability from Unit Price:** Price-tier indicator derived from average transaction unit price (with VAT)
5. **UOM as Packsize:** Unit of measure (Case, Box, Piece) used as pack-size descriptor (limited semantic detail)

---

## Recommendations for Implementation

### High Priority (Phase 1 Implementation)
1. **Phase 1 MVP:** Create product_master from v_dim_product (8 columns, 70-100% coverage) — 1 week
2. **Phase 1b Enhancement:** Add variant, packsize, affordability from v_fct invoices (~90% coverage) — 3 days
3. Validate NULL distribution against business expectations for unclassified products

### Medium Priority (External Data Required)
1. **Basecode/Material Code:** Obtain from DMS product master or Mondelēz source system
2. **Product Weight & EAN:** Source from product specification master or GS1 registry
3. **Hierarchy Levels:** Implement subcategory_name, subsegment_name, segment_name via external master

### Low Priority (Advanced Features)
1. **PPG Code:** Implement price package group once pricing hierarchy finalized
2. **Variant Weight:** Add variant-level weight if product specifications available
3. **Affordability Refinement:** Segment affordability by outlet type or channel for more granular pricing tiers
