from confluent_kafka import Consumer, KafkaException
import json

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
            print(f"Alert: Product {product['productID']} is under 10% stock!")

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
        check_stock_and_alert(receipt)

except KeyboardInterrupt:
    pass
finally:
    consumer.close()
