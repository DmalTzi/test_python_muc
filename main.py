from pymongo import MongoClient

mongo_url = "mongodb+srv://hdrproject:50230@cluster0.ktm1unb.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(mongo_url)

db = client.HDRProjecct
collection = db.histories
data = collection.find_one({"StudentNumber":412344})
print(data)