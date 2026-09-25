#!/usr/bin/env python3
import csv
from collections import defaultdict

# Parse schema CSV
tables = defaultdict(
    lambda: {"columns": list(), "rows": 0, "project": "", "dataset": "", "table": ""}
)

with open(
    r"c:\Users\darren.trinidad\Documents\GitHub\Lingaro\exploration\ai-agent\docs\bigquery\sttm-morocco\sttm_morocco_schema.csv"
) as f:
    reader = csv.DictReader(f)
    for row in reader:
        table_path = row["table_path"]
        col_name = row["column_name"]
        data_type = row["type"]

        # Extract project.dataset.table
        parts = table_path.split(".")
        if len(parts) >= 3:
            project = parts[0]
            dataset = parts[1]
            table = ".".join(parts[2:])  # Handle complex table names

            if col_name not in tables[table_path]["columns"]:
                tables[table_path]["columns"].append(col_name)
            tables[table_path]["project"] = project
            tables[table_path]["dataset"] = dataset
            tables[table_path]["table"] = table
            tables[table_path]["rows"] = (
                int(row.get("total_rows", 0)) if row.get("total_rows") else 0
            )

# Print summary by table
print("=== SOURCE TABLE SUMMARY ===\n")
for table_path in sorted(tables.keys()):
    info = tables[table_path]
    col_count = len(info["columns"])
    short_name = info["table"]
    print(f"{short_name} ({info['project'][-2:]})")
    print(f"  Columns: {col_count} | Rows: {info['rows']:,}")
    print()

# Print detailed column lists for key tables
print("\n=== DETAILED COLUMNS BY KEY SOURCE TABLES ===\n")

# POI table columns
print("v_manual_poi_ma:")
for col in sorted(
    tables[
        "dev-amea-analyt-sorsa-svc-38.dev_amea_p_ds_product_specific.v_manual_poi_ma"
    ]["columns"]
):
    print(f"  - {col}")

print("\nv_fct_distributor_invoice_line_item:")
for col in sorted(
    tables[
        "prd-amea-analyt-diso-svc-7f.amea_ds_distributor_sellout.v_fct_distributor_invoice_line_item"
    ]["columns"]
)[:15]:
    print(f"  - {col}")
print("  ... and more")

print("\nv_dim_product:")
for col in sorted(
    tables["prd-amea-analyt-diso-svc-7f.amea_ds_distributor_sellout.v_dim_product"][
        "columns"
    ]
):
    print(f"  - {col}")

print("\nv_dim_store:")
for col in sorted(
    tables["prd-amea-analyt-diso-svc-7f.amea_ds_distributor_sellout.v_dim_store"][
        "columns"
    ]
)[:15]:
    print(f"  - {col}")
print("  ... and more")

print("\nt_dim_material:")
t_cols = sorted(
    tables["prd-amea-analyt-md-svc-7c.prd_amea_dc_md.t_dim_material"]["columns"]
)
for col in t_cols[:15]:
    print(f"  - {col}")
print(f"  ... and {len(t_cols)-15} more columns")
