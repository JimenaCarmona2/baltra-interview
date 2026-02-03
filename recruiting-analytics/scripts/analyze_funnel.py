import csv
from io import StringIO
from datetime import datetime

def analyze_funnel(candidates_csv_text, logs_csv_text):
    VALID_STAGES = ['Evaluados', 'Citados', 'Entrevistados', 'Aceptados', 'Contratados']

    candidate_states = {}  # candidate_id -> funnel_state

    try:
        reader = csv.DictReader(StringIO(logs_csv_text))
        candidate_logs = {} # candidate_id -> list of {state, timestamp}

        for row in reader:
            try:
                candidate_id = int(row['candidate_id'])
                new_state = row['new_funnel_state'].strip() if row['new_funnel_state'] else None
                changed_at = row['changed_at'].strip() if row['changed_at'] else None

                if new_state and new_state in VALID_STAGES and changed_at:
                    candidate_logs.setdefault(candidate_id, []).append({
                        'state': new_state,
                        'timestamp': changed_at
                    })
            except (ValueError, KeyError):
                # Skip malformed rows
                continue

        # Get the most recent state for each candidate from logs
        for candidate_id, logs in candidate_logs.items():
            if logs:
                most_recent = max(logs, key=lambda x: x['timestamp'])
                candidate_states[candidate_id] = most_recent['state']

        reader = csv.DictReader(StringIO(candidates_csv_text))
        for row in reader:
            try:
                candidate_id = int(row['candidate_id'])
                funnel_state = row['funnel_state'].strip() if row['funnel_state'] else None

                # Use the state from logs if available, otherwise use the state from candidates.csv
                if candidate_id not in candidate_states:
                    if funnel_state and funnel_state in VALID_STAGES:
                        candidate_states[candidate_id] = funnel_state
                        # If no valid state anywhere, candidate is excluded

            except (ValueError, KeyError):
                continue

    except Exception as e:
        return {
            "error": f"Unexpected error: {str(e)}",
            "total_candidates": 0,
            "funnel_stages": {},
            "report_date": datetime.now().strftime("%Y-%m-%d")
        }

    stage_counts = {}
    for state in candidate_states.values():
        stage_counts[state] = stage_counts.get(state, 0) + 1

    total_candidates = len(candidate_states)

    funnel_stages = {
        stage: {
            "count": stage_counts.get(stage, 0),
            "percentage": round((stage_counts.get(stage, 0) / total_candidates * 100), 1)
            if total_candidates > 0 else 0.0
        }
        for stage in VALID_STAGES
    }

    return {
        "total_candidates": total_candidates,
        "funnel_stages": funnel_stages,
        "report_date": datetime.now().strftime("%Y-%m-%d")
    }