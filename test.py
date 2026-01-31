import os
import pymongo
from dotenv import load_dotenv
load_dotenv()

client = pymongo.MongoClient(os.getenv("MONGO_DB_URL"))
# Hardcode these just for this test to be sure
db = client["ConcreteStrengthDatabase"] 
col = db["ConcreteData"]

print(f"Connection Status: SUCCESS")
print(f"Total Records Found: {col.count_documents({})}")