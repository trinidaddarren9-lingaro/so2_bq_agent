# BigQuery Table Documentation

This folder contains documentation for BigQuery tables used in the India/AMEA analytics platform.

## Folder Structure

```
docs/bigquery/
├── README.md              ← You are here
├── mcp-servers.md         ← MCP server routing (which server for which project)
└── tables/                ← One markdown file per table
    ├── v_outlet_in.md
    ├── v_sku_details_in.md
    ├── v_transaction_in.md
    └── ...
```

## Table Doc Template

When creating a new table doc, use this format:

```markdown
# <table_name>

## Fully Qualified Name
`project.dataset.table_or_view`

## MCP Server
`<server-name>` (e.g., `datal-prod`)

## Type
View / Table

## Description
Brief description of what this table contains and its business purpose.

## Schema

| Column | Type | Description |
|--------|------|-------------|
| col1 | STRING | ... |
| col2 | INT64 | ... |
| ... | ... | ... |

## Partitioning
- Partition column: `<column_name>`
- Partition type: DAY / MONTH / YEAR

## Clustering
- Clustering columns: `<col1>`, `<col2>`

## Common Use Cases
- Used for: ...
- Commonly joined with: ...

## Notes
- Any gotchas, known issues, or tips
```

## How This Grows

- **Copilot Agent** will auto-populate these docs when it encounters a table for the first time.
- It calls `get_table_info` via MCP, then creates the doc file using the template above.
- Over time, this becomes a living data dictionary.
