
client = MongoClient("mongodb://127.0.0.1:27017")
db = client.COURT_CASES
cases = db.cases
