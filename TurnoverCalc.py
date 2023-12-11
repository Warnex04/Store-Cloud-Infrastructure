from pymongo import MongoClient

client = MongoClient('mongodb://mongo:27017/')
db = client.receipts_db
collection = db.receipts

def calculate_turnover():
    turnover = 0
    for receipt in collection.find():
        for product in receipt['products']:
            turnover += product['price'] * product['quantity']
    return turnover

if __name__ == '__main__':
    print("Total turnover:", calculate_turnover())
