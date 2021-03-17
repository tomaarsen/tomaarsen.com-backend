
import pymongo

# Initialize MongoDB database
client = pymongo.MongoClient("localhost:27017")
db = client["AGID"]