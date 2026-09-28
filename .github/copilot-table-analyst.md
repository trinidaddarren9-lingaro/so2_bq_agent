Use the existing MCP connections to analyze this BigQuery table. MCP connection details and usage instructions are available at:

docs\bigquery\mcp-servers.md

Table: {{TABLE_PATH}}

Filter — apply this BEFORE any analysis, and include it in every query:
{{FILTER}}

Analyze ONLY these columns:
{{COLUMNS}}

Goal:
Understand the table’s purpose and the meaning/use of the listed columns.

For the filtered data only:
1. State the table purpose and row grain.
2. For each listed column, provide:
   - business meaning;
   - typical use;
   - data type;
   - a short insight from the filtered data, such as null rate, distinct values, range, common pattern, or likely key role.
3. Highlight important relationships, measures, likely join keys, and data-quality observations—only where supported by the listed columns.
4. Clearly distinguish assumptions from evidence supported by the filtered data.

Rules:
- Apply the provided filter before any profiling, sampling, aggregation, or analysis.
- **Sampling Methodology:** Always query at least 1% of the filtered table for data profiling:
  1. First, execute: `SELECT COUNT(*) FROM {{TABLE_PATH}} WHERE {{FILTER}}`
  2. Calculate 1% threshold: `ceil(count * 0.01)`
  3. Query sample using: `LIMIT ceil(count * 0.01)` or `QUALIFY RAND() < 0.01`
  4. Document in markdown: Include the sampling approach and total row count in "Analysis Methodology" section
- Do not analyze, describe, sample, or reference columns outside `{{COLUMNS}}`.
- A column required only for `{{FILTER}}` may be used to filter, but must not be analyzed or documented unless included in `{{COLUMNS}}`.
- Use only the existing configured MCP connections; do not create or modify MCP configuration.
- Keep the output concise and useful.

Save concise Markdown documentation to:

docs\bigquery\tables\{{TABLE_NAME}}.md