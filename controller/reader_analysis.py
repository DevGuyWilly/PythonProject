def analyze_top_readers(data):
    """Analyze reading time for each user."""
    reader_times = {}

    for entry in data:
        if entry.get('event_type') == 'pagereadtime':
            uuid = entry.get('visitor_uuid')
            read_time = entry.get('event_readtime', 0)
            reader_times[uuid] = reader_times.get(uuid, 0) + read_time

    reader_profiles = [{'uuid': uuid, 'total_time_mins': round(time / (1000 * 60), 2),
                        'total_time_hours': round(time / (1000 * 60 * 60), 2)} for uuid, time in reader_times.items()]
    reader_profiles.sort(key=lambda x: x['total_time_mins'], reverse=True)

    return reader_profiles[:10] 