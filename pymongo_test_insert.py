from pymongo_get_database import get_database
dbname = get_database()
collection_name = dbname["blackScholesValues"]

item = {
    "StockPrice": "99.93",
    "StrikePrice": "70.00",
    "InterestRate": "0.05",
    "Volatility": "0.1",
    "TimeToExpiry": "20"
}

collection_name.insert_one(item)

item_details = collection_name.find()
for item in item_details:
    print(item)