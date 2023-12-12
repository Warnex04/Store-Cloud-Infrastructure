from flask import Flask, jsonify
from confluent_kafka import Producer
import json
import random

app = Flask(__name__)

# Kafka configuration
kafka_config = {
    'bootstrap.servers': "kafka:9092"  # Changed from localhost:9092 to kafka:9092
}

producer = Producer(kafka_config)

def generate_receipt():
    """ Function to generate a mock receipt """
    return {
        'storeID': random.randint(100, 999),
        'checkoutID': random.randint(1000, 9999),
        'products': [
            {
                'productID': random.randint(100, 999),
                'quantity': random.randint(1, 100),
                'price': round(random.uniform(1.0, 100.0), 2)
            }
            for _ in range(random.randint(1, 10))
        ]
    }

@app.route('/receipt', methods=['POST'])
def post_receipt():
    receipt = generate_receipt()
    producer.produce('receipts_topic', json.dumps(receipt))
    producer.flush()
    return jsonify(receipt), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
