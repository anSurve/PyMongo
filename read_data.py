from pymongo import MongoClient

# MongoDB connection string
MONGO_URI = "mongodb://admin:password123@localhost:27018/admin"

def read_data():
    try:
        # Connect to MongoDB
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        # Check connection
        client.admin.command('ping')
        print("Connected to MongoDB successfully.")

        # Select database and collection
        db = client['history_db']
        collection = db['english_historical_events']

        # Get total count
        count = collection.count_documents({})
        print(f"Total documents in 'english_historical_events': {count}")

        if count == 0:
            print("Collection is empty.")
            return

        # Read and print the first 5 documents
        # print("\nFetching first 5 documents:")
        # cursor = collection.distinct("category2")
        
        # for doc in cursor:
        #     print(doc)

        cursor = collection.aggregate([
            {
                "$match": {"category2": {"$ne": None}}
            },
            {
                "$group": {
                    "_id": "$category2",
                    "count": {"$sum": 1}
                }
            },
            {
                "$sort": {"count": -1}
            },
            {
                "$limit": 10
            },
            {
                "$project": {
                    "_id": 1,
                    "count": 1
                }
            }
        ])

        for doc in cursor:
            print(doc)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    read_data()
