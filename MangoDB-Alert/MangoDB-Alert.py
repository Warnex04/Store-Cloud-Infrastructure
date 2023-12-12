from confluent_kafka import Consumer, KafkaError
import json
from pymongo import MongoClient

# MongoDB Setup
mongo_client = MongoClient('mongodb://mongo:27017/')
db = mongo_client.alerts_db
alerts_collection = db.stock_alerts

# Kafka Consumer Setup
consumer = Consumer({
    'bootstrap.servers': 'kafka:9092',
    'group.id': 'stock_alert_consumer_group',
    'auto.offset.reset': 'earliest'
})
consumer.subscribe(['receipts_topic'])

# Alert Logic
def check_stock_and_alert(receipt):
    for product in receipt['products']:
        if product['quantity'] < 10:
            alert_message = f"Alert: Product {product['productID']} is under 10% stock!"
            print(alert_message)
            # Save alert to MongoDB
            alert_document = {
                "productID": product['productID'],
                "message": alert_message,
                "quantity": product['quantity']
            }
            alerts_collection.insert_one(alert_document)

# Consuming messages
try:
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() != KafkaError._PARTITION_EOF:
                print(f"Kafka Error: {msg.error()}")
            continue

        receipt = json.loads(msg.value().decode('utf-8'))
        check_stock_and_alert(receipt)

except KeyboardInterrupt:
    pass
finally:
    consumer.close()
