from flask import Flask, jsonify
from confluent_kafka import Producer
import json
import random

app = Flask(__name__)

# Kafka configuration
kafka_config = {
    'bootstrap.servers': "localhost:9092"
}

producer = Producer(kafka_config)

def generate_receipt():
    """ Function to generate a mock receipt """
    return {
        'storeID': random.randint(100, 999),
        'checkoutID': random.randint(1000, 9999),
        'products': [
            {
                'productID': random.randint(10000, 99999),
                'quantity': random.randint(1, 10)
            } for _ in range(random.randint(1, 5))
        ]
    }

@app.route('/generate-receipt', methods=['GET'])
def generate_and_send_receipt():
    """ Endpoint to generate and send a receipt to Kafka """
    receipt = generate_receipt()
    producer.produce('receipts_topic', json.dumps(receipt))
    producer.flush()
    return jsonify({"status": "success", "receipt": receipt})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
