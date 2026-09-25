# MCP Server Routing Table

Use this to pick the correct MCP server for any BigQuery table or project.

## Server Map

### DATAL — Data Lake

| Server Name | Environment | GCP Project |
|---|---|---|
| `datal-dev` | 🟢 Dev | `dev-amea-analyt-datal-svc-db` |
| `datal-qa` | 🟡 QA | `qa-amea-analyt-datal-svc-91` |
| `datal-prod` | 🔴 Prod | `prd-amea-analyt-datal-svc-df` |

### DISO — Distribution / Sales Ops

| Server Name | Environment | GCP Project |
|---|---|---|
| `diso-dev` | 🟢 Dev | `dev-amea-analyt-diso-svc-63` |
| `diso-qa` | 🟡 QA | `qa-amea-analyt-diso-svc-ee` |
| `diso-prod` | 🔴 Prod | `prd-amea-analyt-diso-svc-7f` |

### COEX — Commercial Excellence

| Server Name | Environment | GCP Project |
|---|---|---|
| `coex-dev` | 🟢 Dev | `dev-amea-analyt-coex-svc-6c` |
| `coex-prod` | 🔴 Prod | `prd-amea-analyt-coex-svc-40` |

### SOPR — Sales Operations

| Server Name | Environment | GCP Project |
|---|---|---|
| `sopr-prod` | 🔴 Prod | `prd-amea-analyt-sopr-svc-7f` |

### CPS

| Server Name | Environment | GCP Project |
|---|---|---|
| `cps-prod` | 🔴 Prod | `prd-amea-analyt-cps-svc-c6` |

### SORSA

| Server Name | Environment | GCP Project |
|---|---|---|
| `sorsa-dev` | 🟢 Dev | `dev-amea-analyt-sorsa-svc-38` |

---

## How to Pick the Right Server

1. Identify the **GCP project** in the table's fully-qualified name  
   e.g., `prd-amea-analyt-diso-svc-7f.dataset.table` → project = `prd-amea-analyt-diso-svc-7f`
2. Match project to the table above → server = `diso-prod`
3. Call tools as `mcp_diso-prod_<tool_name>`

## MCP Tool Names Format

```
mcp_<server-name>_<tool>
```

Examples:
- `mcp_datal-prod_get_table_info`
- `mcp_diso-dev_list_dataset_ids`
- `mcp_coex-prod_execute_sql`
- `mcp_sopr-prod_list_table_ids`

---

## ⚠️ Missing Servers

The following GCP projects have known tables but **NO MCP server configured**:

| GCP Project | Domain | Action Needed |
|---|---|---|
| `prd-amea-analyt-ctpm-svc-8c` | CTPM (Trade Promo?) | Add to `mcp.json` |
| `prd-amea-analyt-rtat-svc-29` | RTAT (Retail Audit?) | Add to `mcp.json` |

If you need to query tables in these projects, add them to:
`C:\Users\darren.trinidad\AppData\Roaming\Code\User\mcp.json`
