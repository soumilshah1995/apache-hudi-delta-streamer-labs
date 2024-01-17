# Import required libraries
from faker import Faker
from time import sleep
import random
import uuid
from datetime import datetime
from kafka_schema_registry import prepare_producer

# Configuration
KAFKA_BOOTSTRAP_SERVERS = ['localhost:7092']
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
        {"name": "priority", "type": "string"},
        {"name": "order_date", "type": "string"},
        {"name": "customer_id", "type": "string"},
        {"name": "ts", "type": "string"},
        {"name": "OP", "type": "string"}  # Add the 'OP' column to the Avro Schema
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
    def get_orders_data(operation='I'):
        """
        Generate and return a dictionary with mock order data.
        :param operation: The operation type ('I' for insert, 'U' for update, 'D' for delete)
        """
        return {
            "order_id": str(uuid.uuid4()),
            "name": faker.text(max_nb_chars=20),
            "order_value": str(random.randint(10, 1000)),
            "priority": random.choice(["LOW", "MEDIUM", "HIGH"]),
            "order_date": faker.date_between(start_date='-30d', end_date='today').strftime('%Y-%m-%d'),
            "customer_id": str(uuid.uuid4()),
            "ts": str(datetime.now().timestamp()),
            "OP": operation  # Add the 'OP' column with the specified operation type
        }

    @staticmethod
    def produce_avro_message(producer, topic, data):
        """
        Produce an Avro message and send it to the Kafka topic.
        """
        producer.send(topic, data)


# Generate and send order data
# for _ in range(NUM_MESSAGES):
#     # Use random.choice to select a random operation type ('I', 'U', or 'D')
#     operation_type = random.choice(['I', 'U', 'D'])
#     order_data = DataGenerator.get_orders_data(operation=operation_type)
#     print(order_data, type(order_data))
#     break
    # DataGenerator.produce_avro_message(producer, TOPIC_NAME, order_data)
    # print("Order Payload:", order_data)
    # sleep(SLEEP_INTERVAL)



order_data = {
    'order_id': 'e23cdeec-5f1b-4b2b-8ed7-7d1a505603d5',
    'name': 'Show beat federal.',
    'order_value': '898',
    'priority': 'MEDIUM',
    'order_date': '2023-12-21',
    'customer_id': '2ac220b5-2524-4977-95fc-c93080cf0e6a',
    'ts': '170549934',
    'OP': 'D'
}
DataGenerator.produce_avro_message(producer, TOPIC_NAME, order_data)
print("Order Payload:", order_data)
sleep(SLEEP_INTERVAL)
