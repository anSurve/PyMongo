import json

try:
    with open('data/historical_events.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        print("Keys in result:", data.get('result', {}).keys())
        if 'events' in data.get('result', {}):
            print("Type of event:", type(data['result']['events']))
            if isinstance(data['result']['events'], list):
                 print("Count of events:", len(data['result']['events']))
            else:
                 print("Single event found (likely overwrote others)")
except Exception as e:
    print("JSON load failed:", e)
