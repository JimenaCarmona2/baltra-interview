## Candidates CSV Schema

- candidate_id: Unique identifier (integer, primary key)
- business_unit_id: Business unit (integer)
- phone: Phone number (string)
- name: Candidate name (string)
- created_at: Creation timestamp (timestamp)
- funnel_state: Current funnel stage (string)

## Candidates Funnel Logs CSV Schema

- id: Unique identifier (integer, primary key)
- candidate_id: Candidate identifier (integer, foreign key to candidates)
- previous_funnel_state: Previous funnel stage (string)
- new_funnel_state: Current funnel stage (string)
- changed_at: Changed timestamp (timestamp)

## Valid Funnel States

1. Evaluados
2. Citados
3. Entrevistados
4. Aceptados
5. Contratados

**Note**: A candidate's current state should be determined by their most recent entry in `candidate_funnel_logs.csv` OR by `funnel_state` in `candidates.csv` if no logs exist.