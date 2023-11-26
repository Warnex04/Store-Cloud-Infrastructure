from confluent_kafka import Producer, Consumer, KafkaError
from pymongo import MongoClient
import sys

# Setup MongoDB Client
mongo_client = MongoClient('localhost', 27017)
db = mongo_client['your_database']
collection = db['your_collection']

# Function to deliver reports from Kafka producer
def delivery_report(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

# Kafka Producer
p = Producer({'bootstrap.servers': 'localhost:9092'})

def produce_receipt(receipt):
    try:
        receipt_data = {
            "store_name": receipt.store_name,
            "store_address": receipt.store_address,
            "seller_name": receipt.seller_name,
            "items": [{"name": item.name, "price": item.price, "quantity": item.quantity} for item in receipt.items]
        }
        p.produce('your_topic', json.dumps(receipt_data).encode('utf-8'), callback=delivery_report)
        p.poll(0)
    except BufferError:
        print('Local producer queue is full ({} messages awaiting delivery): try again'.format(len(p)))
    p.flush()

# Kafka Consumer
c = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'your_group',
    'auto.offset.reset': 'earliest'
})
def consume_messages():
    c.subscribe(['your_topic'])

    try:
        while True:
            msg = c.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(msg.error())
                    break

            # Deserialize the message data into a Receipt object
            data = json.loads(msg.value().decode('utf-8'))
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
            receipt_data = {
                "store_name": receipt.store_name,
                "store_address": receipt.store_address,
                "seller_name": receipt.seller_name,
                "items": [{"name": item.name, "price": item.price, "quantity": item.quantity} for item in receipt.items],
                "total": receipt.total()
            }
            collection.insert_one(receipt_data)

            # Print the receipt
            print(receipt)

    except KeyboardInterrupt:
        pass
    finally:
        c.close()


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
