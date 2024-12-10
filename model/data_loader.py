import json

def load_json_data(file_path):
    """Load JSON data from a file with newline-delimited JSON objects."""
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data.append(json.loads(line.strip()))
            except json.JSONDecodeError:
                continue  # Skipping malformed lines
    return data 