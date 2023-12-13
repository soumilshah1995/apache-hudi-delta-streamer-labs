# Import required libraries
from faker import Faker
from time import sleep
import random
import uuid
from datetime import datetime
from kafka_schema_registry import prepare_producer

# Configuration
KAFKA_BOOTSTRAP_SERVERS = ['localhost:19092']
SCHEMA_REGISTRY_URL = 'http://localhost:8081'
TOPIC_NAME = 'orders'
NUM_MESSAGES = 20
SLEEP_INTERVAL = 1

# Avro Schema
SAMPLE_SCHEMA = {
    "type": "record",
    "name": "Order",
    "fields": [
        {"name": "order_id", "type": "string"},
        {"name": "name", "type": "string"},
        {"name": "order_value", "type": "string"},
        {"name": "priority", "type": "string" },
        {"name": "order_date", "type": "string"},
        {"name": "customer_id", "type": "string"},
        {"name": "ts", "type": "string"}
    ]
}

# Kafka Producer
producer = prepare_producer(
    KAFKA_BOOTSTRAP_SERVERS,
    SCHEMA_REGISTRY_URL,
    TOPIC_NAME,
    1,
    1,
    value_schema=SAMPLE_SCHEMA,
)

# Faker instance
faker = Faker()


class DataGenerator:
    @staticmethod
    def get_orders_data():
        """
        Generate and return a dictionary with mock order data.
        """
        return {
            "order_id": str(uuid.uuid4()),
            "name": faker.text(max_nb_chars=20),
            "order_value": str(random.randint(10, 1000)),
            "priority": random.choice(["LOW", "MEDIUM", "HIGH"]),
            "order_date": faker.date_between(start_date='-30d', end_date='today').strftime('%Y-%m-%d'),
            "customer_id": str(uuid.uuid4()),
            "ts": str(datetime.now().timestamp()),
        }

    @staticmethod
    def produce_avro_message(producer, topic, data):
        """
        Produce an Avro message and send it to the Kafka topic.
        """
        producer.send(topic, data)


# Generate and send order data
for _ in range(NUM_MESSAGES):
    order_data = DataGenerator.get_orders_data()
    DataGenerator.produce_avro_message(producer, TOPIC_NAME, order_data)
    print("Order Payload:", order_data)
    sleep(SLEEP_INTERVAL)
