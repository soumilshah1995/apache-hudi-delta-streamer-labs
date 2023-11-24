try:
    from kafka import KafkaProducer
    from faker import Faker
    import json
    from time import sleep
    import random
    import uuid
    from datetime import datetime
    print("All modules loaded ")
except Exception as e:
    print("error modules ", e)

producer = KafkaProducer(bootstrap_servers='localhost:9092')
_instance = Faker()

global faker
faker = Faker()


class DataGenerator(object):
    @staticmethod
    def get_customer_data():
        customer_data = {
            "customer_id": str(uuid.uuid4()),
            "name": faker.name(),
            "state": faker.state(),
            "city": faker.city(),
            "email": faker.email(),
            "created_at": datetime.now().isoformat().__str__(),
            "ts": str(datetime.now().timestamp()),
        }
        return customer_data

    @staticmethod
    def get_orders_data(customer_id):
        order_data = {
            "order_id": str(uuid.uuid4()),
            "name": faker.text(max_nb_chars=20),
            "order_value": str(random.randint(10, 1000)),
            "priority": random.choice(["LOW", "MEDIUM", "HIGH"]),
            "order_date": faker.date_between(start_date='-30d', end_date='today').strftime('%Y-%m-%d'),
            "customer_id": customer_id,
            "ts": str(datetime.now().timestamp()),
        }
        return order_data


for _ in range(20):
    # Generate and send customer data
    customer_data = DataGenerator.get_customer_data()
    customer_payload = json.dumps(customer_data).encode("utf-8")
    producer.send('customers', customer_payload)
    print("Customer Payload:", customer_payload)
    sleep(1)

    # Generate and send order data for each customer
    for i in range(3):  # Adjust the number of orders per customer as needed
        order_data = DataGenerator.get_orders_data(customer_data["customer_id"])
        order_payload = json.dumps(order_data).encode("utf-8")
        producer.send('orders', order_payload)
        print("Order Payload:", order_payload)
        sleep(1)
