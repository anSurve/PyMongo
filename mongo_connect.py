from pymongo import MongoClient

client = MongoClient(
    "mongodb://admin:password123@localhost:27018/admin",
    serverSelectionTimeoutMS=5000
)

print(client.admin.command("ping"))
