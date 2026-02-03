---
name: recruiting-analytics
description: Analyzes recruiting funnel data from CSV files and generates monthly summary reports. Use when you need to extract candidate statistics, calculate funnel conversion rates, or prepare recruiting performance summaries.
---

# Recruiting Analytics Skill

This skill helps analyze recruiting funnel data and generate monthly reports.

## How to Use

1. Load candidate data from CSV files
2. Run the analysis script: `python scripts/analyze_funnel.py`
3. Use the output to generate formatted reports

## Input Files Example

- `candidates.csv` - Candidate information
- `candidate_funnel_logs.csv` - Funnel state transitions

See [references/data_schema.md](references/data_schema.md) for detailed field descriptions.

## Analysis Script

Run the analysis:
```bash
python scripts/analyze_funnel.py candidates.csv candidate_funnel_logs.csv
```

## Output Format Example

```json
{
  "total_candidates": 1000,
  "funnel_stages": {
    "Evaluados": {"count": 970, "percentage": 97.0},
    "Citados": {"count": 412, "percentage": 41.2},
    "Entrevistados": {"count": 52, "percentage": 5.2},
    "Aceptados": {"count": 31, "percentage": 3.1},
    "Contratados": {"count": 21, "percentage": 2.1}
  },
  "report_date": "2026-01-30"
}
```

## Error Handling

The script handles:
- **Missing files** - Returns error message with zero candidates
- **Malformed rows** - Skipped without stopping execution
- **Invalid funnel states** - Ignored (only valid: Evaluados, Citados, Entrevistados, Aceptados, Contratados)
- **Invalid data types** - Non-integer IDs or malformed timestamps are skipped
- **Empty files** - Works correctly, returns 0 candidates

When errors occur, returns:
```json
{
  "error": "Error description",
  "total_candidates": 0,
  "funnel_stages": {},
  "report_date": "YYYY-MM-DD"
}
```