from flask import Flask, request
from confluent_kafka import Producer
import json

app = Flask(__name__)
producer = Producer({'bootstrap.servers': 'kafka:9092'})

@app.route('/receipt', methods=['POST'])
def post_receipt():
    receipt_data = request.json
    producer.produce('receipts_topic', json.dumps(receipt_data))
    producer.flush()
    return {"status": "success"}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
