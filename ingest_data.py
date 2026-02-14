import json
import pymongo
from pymongo import MongoClient

# MongoDB connection string
MONGO_URI = "mongodb://admin:password123@localhost:27018/admin"

def ingest_data():
    try:
        # Connect to MongoDB
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        # Check connection
        client.admin.command('ping')
        print("Connected to MongoDB successfully.")

        # Select database and collection
        db = client['history_db']
        collection = db['english_historical_events']

        # Custom JSON decoder to handle duplicate 'event' keys
        def handle_duplicates(pairs):
            d = {}
            events = []
            for k, v in pairs:
                if k == 'event':
                    events.append(v)
                else:
                    d[k] = v
            
            if events:
                # If we found 'event' keys, store them as a list under 'events'
                # Check if 'events' key already exists to avoid overwriting (though unlikely in this specific file structure)
                if 'events' in d:
                     d['events'].extend(events)
                else:
                     d['events'] = events
            return d

        print("Reading and parsing JSON file...")
        with open('data/historical_events.json', 'r', encoding='utf-8') as file:
            # parsing the json with the custom hook
            data = json.load(file, object_pairs_hook=handle_duplicates)

        # The structure is likely {'result': {'count': '...', 'events': [ ... ]}}
        if 'result' in data and 'events' in data['result']:
            events_list = data['result']['events']
            count = len(events_list)
            print(f"Found {count} events to ingest.")
            
            if count > 0:
                print("Inserting events into MongoDB...")
                # insert_many is more efficient for large lists
                result = collection.insert_many(events_list)
                print(f"Successfully inserted {len(result.inserted_ids)} documents.")
            else:
                print("No events found in the 'events' list.")
        else:
             print("Unexpected JSON structure. Keys found:", data.keys())
             if 'result' in data:
                 print("Keys in 'result':", data['result'].keys())

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    ingest_data()
