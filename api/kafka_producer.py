from kafka import KafkaProducer
import json

TOPIC = "api-requests"

producer = KafkaProducer(
    bootstrap_servers="127.0.0.1:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    request_timeout_ms=3000,
    max_block_ms=3000,
    api_version_auto_timeout_ms=3000
)

def send_event(data):
    try:
        producer.send(TOPIC, value=data)
        producer.flush(timeout=3)
        print("KAFKA PRODUCER:", data)
    except Exception as e:
        print(f"Kafka error: {e}")