# INVOICE_LINE_ITEM_MAPPING_SUMMARY

## Executive Summary
- **Total Target Columns:** 12
- **Mapped Columns:** 12 (100%)
- **Unmapped Columns:** 0

## Confidence Distribution
| Level | Count | Percentage |
|-------|-------|-----------|
| HIGH | 11 | 92% |
| MEDIUM | 1 | 8% |
| LOW | 0 | 0% |

**Average Combined Score:** 0.915

## Primary Source Identified
**v_fct_distributor_invoice_line_item** (DISO Fact Table)
- Project: `prd-amea-analyt-diso-svc-7f`
- Dataset: `amea_ds_distributor_sellout`
- Rows: 16,159,112 total (estimated 5-10M for Morocco RT channel)
- Columns: 73
- Coverage: Multi-country, requires filtering

## Secondary Sources
1. **v_dim_store** (DISO Store Dimension, 43,324 rows)
   - Outlet references and location data
   - Channel filtering (RT = Retail)
   - Country filtering (MA = Morocco)

2. **v_uom_ma** (SORSA dev, 294 rows)
   - Morocco-specific UOM conversions

3. **v_manual_poi_ma** (SORSA dev, 18,514 rows)
   - POI/store references for outlet

## Morocco Filtering Strategy

### Primary Filter Columns
- **country_code_nk = 'MA'** (from v_fct_distributor_invoice_line_item)
- **channel_code_nk = 'rt'** (Retail channel from v_dim_store)

### Data Volume Estimates
- **Total invoice lines:** 16,159,112 rows
- **Morocco subset:** ~5-10M rows (30-60% estimated)
- **Date range:** Post 2024-01-01 (configurable)

### NULL Handling
- distributor_invoice_net_sales_amt: 5% NULLs (805K in 16M)
- Other columns: <5% NULLs except category fields

## Mapped Columns Detail

| # | Target Column | Primary Source | Secondary | Confidence | Coverage |
|---|---|---|---|---|---|
| 1 | invoice_line_sok | distributor_invoice_line_sk | - | HIGH | 100% |
| 2 | invoice_number | distributor_invoice_code_nk | - | HIGH | 100% |
| 3 | invoice_line_number | distributor_invoice_line_sk (seq) | - | HIGH | 100% |
| 4 | outlet_sok | store_sk (v_dim_store) | retailer_store_nk | HIGH | 96% |
| 5 | product_sok | product_sk (fact) | product_nk | HIGH | 100% |
| 6 | uom_sok | distributor_invoice_line_uom_sk | - | HIGH | 100% |
| 7 | invoice_date | distributor_invoice_date_code_nk | - | HIGH | 100% |
| 8 | invoice_type_name | distributor_invoice_file_type | file_type_code | HIGH | 95% |
| 9 | order_number | distributor_invoice_sales_rep_id | invoice_code | MEDIUM | 95% |
| 10 | uom_qty | distributor_invoice_line_qty_cases | - | HIGH | 100% |
| 11 | gross_value | distributor_invoice_gross_sales_amt | - | HIGH | 100% |
| 12 | net_value | distributor_invoice_net_sales_amt | - | HIGH | 95% |

## Key Data Characteristics

### Data Quality
- **Duplicate rows:** Check distributor_invoice_code_nk + line_number uniqueness
- **Date range:** Configurable via distributor_invoice_date_code_nk
- **Missing channels:** ~5% missing channel_code_nk, fallback to default logic
- **NULL outlets:** ~4% store_sk NULL, recommend handling in WHERE clause

### Performance Considerations
- **Table size:** 16.2M rows (DISO production)
- **Partitioning:** Likely partitioned by country_code_nk or date
- **Index strategy:** Scan country_code_nk='MA' AND channel_code_nk='rt'
- **Estimated scan:** 2-3GB (16.2M rows in DISO volume)

## Recommendations

### Approval Checklist
- [ ] Confirm invoice_number = distributor_invoice_code_nk
- [ ] Verify order_number source (sales_rep_id vs invoice_code)
- [ ] Decide NULL handling for net_value (5% NULLs)
- [ ] Confirm retail channel code = 'rt'
- [ ] Validate currency handling (iso_currency_code_nk)
- [ ] Test Morocco filter effectiveness (expected 30-60% reduction)
- [ ] Confirm date range for historical load

### Next Steps
1. **Phase 2 - Data Validation:** Sample 1% of Morocco RT data (~100K rows)
2. **Phase 3 - SQL Development:** Build fact table extraction
3. **Phase 4 - QA:** Validate invoice aggregations vs source

## Technical Details
- **Expected Output:** 5-10M invoice line records
- **Processing Time:** ~30-60 seconds (large fact table)
- **Estimated Bytes Scanned:** 2-3GB
- **Join complexity:** 3 tables (fact + dim_store + product reference)
