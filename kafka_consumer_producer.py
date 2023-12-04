from kafka import KafkaConsumer, KafkaProducer
from pymongo import MongoClient
import json
from Receipt import *

# Setup MongoDB Client
mongo_client = MongoClient('localhost', 27017)
db = mongo_client['your_database']
collection = db['your_collection']

# Kafka Producer
producer = KafkaProducer(bootstrap_servers='localhost:9094')

def produce_receipt(receipt):
    try:
        receipt_data = {
            "store_name": receipt.store_name,
            "store_address": receipt.store_address,
            "seller_name": receipt.seller_name,
            "items": [{"name": item.name, "price": item.price, "quantity": item.quantity} for item in receipt.items],
            "total": receipt.total()
        }
        producer.send('your_topic', json.dumps(receipt_data).encode('utf-8'))
        producer.flush()
    except Exception as e:
        print(f'An error occurred: {e}')

# Kafka Consumer
consumer = KafkaConsumer(
    'your_topic',
    bootstrap_servers='localhost:9094',
    auto_offset_reset='earliest',
    group_id='your_group'
)

def consume_messages():
    try:
        for msg in consumer:
            # Deserialize the message data into a Receipt object
            data = json.loads(msg.value.decode('utf-8'))
            receipt = Receipt(data['store_name'], data['store_address'], data['seller_name'])
            
            for item_data in data['items']:
                item = Item(item_data['name'], item_data['price'], item_data['quantity'], item_data.get('threshold', 100))
                receipt.add_item(item.name, item.price, item.quantity)

                # Notify if the item quantity is below 10% of the threshold
                if item.is_below_threshold():
                    notification_message = f"Low stock alert for {item.name}: only {item.quantity} left in stock."
                    print(notification_message)
                    # Here you can integrate with an email service, SMS gateway, or any other notification system

            # Save the receipt to MongoDB
            collection.insert_one(data)

            # Print the receipt
            print(receipt)

    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()


# Example usage
if __name__ == "__main__":
    # Create a Receipt object and add items
    receipt = Receipt("Store Name", "Store Address", "Seller Name")
    receipt.add_item("Item 1", 10.99, 2)
    receipt.add_item("Item 2", 5.49, 5)

    # For producer
    produce_receipt(receipt)

    # For consumer
    consume_messages()
