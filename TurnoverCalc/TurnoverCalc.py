from pymongo import MongoClient

client = MongoClient('mongodb://mongo:27017/')
db = client.receipts_db
collection = db.receipts

def calculate_turnover():
    turnover = 0
    for receipt in collection.find():
        for product in receipt.get('products', []):  # Safely get products list
            price = product.get('price', 0)  # Default price to 0 if not found
            quantity = product.get('quantity', 0)  # Default quantity to 0 if not found
            turnover += price * quantity
    return turnover

if __name__ == '__main__':
    print("Total turnover:", calculate_turnover())
