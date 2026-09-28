# Copilot Agents — Configuration

This workspace has specialized BigQuery agents for different markets and use cases.

## Available Agents

### 1. BQ Agent (General AMEA BigQuery)
**Name**: `bq`  
**Description**: BigQuery agent for India and AMEA analytics  
**Instructions**: `.github/copilot-instructions.md`

**Invocation**:
```
@bq: Query the India outlet table for sales trends
```

**Use when**: India tables, multi-market analysis, general BigQuery work

---

### 2. BQ-Morocco Agent (Morocco Market Specialist)
**Name**: `bq-morocco`  
**Description**: BigQuery agent for Morocco market analysis with strict environment policy  
**Instructions**: `.github/copilot-instructions-morocco.md`  
**Agent Definition**: `.github/AGENTS_MOROCCO.md`

**Invocation**:
```
@bq-morocco: Analyze the outlet investment channel blocker table
```

Or use the longer form:
```
@bq-morocco: 
Check the t_manual_outlet_investment_channel_blocker_ma table
for uploads in the last 24 hours.
```

**Use when**: 
- Morocco `_ma` tables
- Manual upload analysis
- Data quality investigations
- Morocco-specific data

**What this agent does**:
✅ Automatically reads table environment from docs (NO asking)  
✅ Checks known issues before querying  
✅ Uses Morocco-specific SQL patterns  
✅ Handles manual upload data quality  
✅ Reports with environment reference  

---

## Strict Environment Policy (Morocco Agent)

**Key Feature**: Environment is determined from table documentation, **NOT from user request**.

```
Table Docs (Excel) → Conversion Script → Markdown (Environment: prod)
                                              ↓
                                    Agent reads docs
                                              ↓
                                    Queries prod ONLY
                                    (no user confirmation)
```

**Example**:
```
User: @bq-morocco: Check outlet data
Agent: Reads docs/bigquery/sttm/morocco_outlet.md
Agent: Sees: Environment: prod (LOCKED)
Agent: Queries prod (no asking you!)
```

---

## Agent Comparison

| Feature | BQ Agent | BQ-Morocco Agent |
| --- | --- | --- |
| Market | India/AMEA | Morocco Only |
| Environment | User specifies | From documentation (strict) |
| Manual uploads | Manual handling | Specialized patterns |
| Data quality | Basic checks | Morocco-specific issues |
| Documentation | `copilot-instructions.md` | `copilot-instructions-morocco.md` |
| Issues tracking | Optional | Required (`morocco_issues.md`) |
| SQL patterns | India-focused | Morocco `_ma` tables |

---

## How to Invoke

### In Copilot Chat

**Quick invoke**:
```
@bq-morocco: [your question about Morocco data]
```

**Examples**:

1. **Analyze a table**:
   ```
   @bq-morocco: How many rows in the outlet investment table?
   ```

2. **Check data quality**:
   ```
   @bq-morocco: Are there any null values in the products table?
   ```

3. **Track daily uploads**:
   ```
   @bq-morocco: Show me all batches loaded to the outlet table today
   ```

4. **Investigate issues**:
   ```
   @bq-morocco: Check the NPD table for the issue documented in morocco_issues.md
   ```

---

## Setup Requirements

Before invoking `@bq-morocco`, ensure:

1. ✅ Excel file converted to markdown:
   ```bash
   python scripts/convert_excel_to_md.py
   ```

2. ✅ Table docs generated in `docs/bigquery/sttm/`:
   ```
   morocco_outlet.md
   morocco_products.md
   morocco_issues.md
   ... etc
   ```

3. ✅ Each table doc has environment specified:
   ```markdown
   **Environment**: prod (STRICT)
   ```

---

## Agent Rules (Morocco)

The `@bq-morocco` agent enforces these rules:

### Rule 1: Use Documented Environment (STRICT)
- Reads environment from `docs/bigquery/sttm/table.md`
- Uses that environment for queries
- Does NOT ask user for environment confirmation

### Rule 2: Read Table Docs First
- Checks schema from `docs/bigquery/sttm/`
- Verifies via MCP `get_table_info`
- Never guesses column names

### Rule 3: Check Known Issues
- References `docs/bigquery/sttm/morocco_issues.md`
- Applies documented workarounds
- Adds validation queries if needed

### Rule 4: Estimate Cost Before Execution
- Dry-runs query to estimate bytes
- Shows cost estimate to user
- Waits for approval if > 1 GB

### Rule 5: Use Morocco-Specific Filters
- Partition on `date_loaded` or `date_col`
- Market filter: `country = 'MA'`
- Batch filters for manual uploads
- Never full table scans

### Rule 6: Report with Context
- Shows which environment was used
- References relevant docs/issues
- Includes data quality notes
- Links to `morocco_issues.md` if applicable

---

## Configuration Files

| File | Purpose |
| --- | --- |
| `.github/copilot-chat.yml` | Agent registration (name, description, instructions) |
| `.github/copilot-instructions-morocco.md` | Detailed Morocco rules & SQL patterns |
| `.github/AGENTS_MOROCCO.md` | Agent role & workflow definition |
| `docs/bigquery/sttm/README.md` | Morocco tables index |
| `docs/bigquery/sttm/STRICT_ENVIRONMENT_POLICY.md` | Environment policy explained |
| `scripts/convert_excel_to_md.py` | Excel → Markdown converter |

---

## Examples

### Example 1: First-Time Query
```
User: @bq-morocco: What Morocco tables do we have?

Agent:
Reading available table docs from docs/bigquery/sttm/
Found 15 Morocco tables:
- t_manual_outlet_investment_channel_blocker_ma (prod)
- t_manual_npd_surrogates_ma (dev)
- t_manual_products_ma (prod)
... [etc]

All tables documented with schemas, environments, and known issues.
```

### Example 2: Query with Strict Environment
```
User: @bq-morocco: How many outlet records were uploaded today?

Agent:
1. Reading docs/bigquery/sttm/morocco_outlet.md
2. Environment: prod (locked)
3. Getting schema via mcp_datal-prod
4. Checking for known issues...
5. Estimated cost: 234 MB
6. Ready to execute. Proceed? (yes/no)

User: yes

7. Executing query on mcp_datal-prod...
8. Results: 5,234 rows across 3 batches
9. Environment: prod (per table docs)
10. Quality: ✅ No issues found (per morocco_issues.md)
```

### Example 3: Data Quality Investigation
```
User: @bq-morocco: Check products table for data quality

Agent:
1. Reading docs/bigquery/sttm/morocco_products.md
2. Environment: prod (locked)
3. Checking morocco_issues.md for known issues
4. Found: Issue M042 - Some outlet_ids are null
5. Running validation query for issue M042...
6. Results: 42 rows affected
7. Workaround: [suggests filtered query]
8. Recommendation: Use provided workaround until data team fix is applied
```

---

## Troubleshooting

**Q: Agent not found?**
- A: Reload Copilot or refresh VS Code settings
- Check: `copilot-chat.yml` has `bq-morocco` agent registered

**Q: "Table not found" error?**
- A: Run conversion script first: `python scripts/convert_excel_to_md.py`
- Check: `docs/bigquery/sttm/` has generated markdown files

**Q: Agent asking for environment?**
- A: Ensure table markdown includes `**Environment**: value`
- Re-run conversion script to regenerate docs

**Q: Wrong environment being used?**
- A: Check table markdown: `**Environment**: [value]`
- Agent uses what's documented (user request overridden)

---

## Next Steps

1. **Ensure Excel is converted**:
   ```bash
   python scripts/convert_excel_to_md.py
   ```

2. **Verify table docs exist**:
   ```
   ls docs/bigquery/sttm/
   ```

3. **Try first query**:
   ```
   @bq-morocco: Show available Morocco tables
   ```

4. **Start analyzing**:
   ```
   @bq-morocco: [your Morocco BigQuery question]
   ```

---

**Agent ready to use! 🇲🇦**
