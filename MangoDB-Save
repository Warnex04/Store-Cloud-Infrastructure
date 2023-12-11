from confluent_kafka import Consumer, KafkaException
import json
from pymongo import MongoClient

# Kafka Consumer Setup
consumer = Consumer({
    'bootstrap.servers': 'kafka:9092',
    'group.id': 'mongodb_consumer_group',
    'auto.offset.reset': 'earliest'
})
consumer.subscribe(['receipts_topic'])

# MongoDB Setup
client = MongoClient('mongodb://mongo:27017/')
db = client.receipts_db
collection = db.receipts

# Consuming messages
try:
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None: continue
        if msg.error():
            if msg.error().code() == KafkaException._PARTITION_EOF:
                continue
            else:
                print(msg.error())
                break

        receipt = json.loads(msg.value())
        collection.insert_one(receipt)

except KeyboardInterrupt:
    pass
finally:
    consumer.close()
