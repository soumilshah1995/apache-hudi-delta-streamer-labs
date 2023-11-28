import uuid
import random
from faker import Faker
from datetime import datetime
import csv
import os
import time
global faker
faker = Faker()


def get_customer_data(total_customers=2):
    customers_array = []
    for i in range(0, total_customers):
        customer_data = {
            "customer_id": str(uuid.uuid4()),
            "name": faker.name(),
            "state": faker.state(),
            "city": faker.city(),
            "email": faker.email(),
            "created_at": datetime.now().isoformat().__str__(),
            "ts": str(datetime.now().timestamp()),  # Add timestamp field
        }
        customers_array.append(customer_data)
    return customers_array


def get_orders_data(customer_ids, order_data_sample_size=3):
    orders_array = []
    for i in range(0, order_data_sample_size):
        try:
            order_id = uuid.uuid4().__str__()
            customer_id = random.choice(customer_ids)
            order_data = {
                "order_id": order_id,
                "name": faker.text(max_nb_chars=20),
                "order_value": random.randint(10, 1000).__str__(),
                "priority": random.choice(["LOW", "MEDIUM", "HIGH"]),
                "order_date": faker.date_between(start_date='-30d', end_date='today').strftime('%Y-%m-%d'),
                "customer_id": customer_id,
                "ts": str(datetime.now().timestamp()),  # Add timestamp field
            }
            orders_array.append(order_data)
        except Exception as e:
            print(e)
    return orders_array


def save_to_tsv(data, file_name):
    keys = data[0].keys()  # Assuming all dicts in the list have the same keys
    with open(file_name, 'w', newline='') as tsv_file:
        tsv_writer = csv.DictWriter(tsv_file, fieldnames=keys, delimiter='\t')
        tsv_writer.writeheader()
        tsv_writer.writerows(data)


def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def generate_and_save_data(total_customers=50, order_data_sample_size=100):
    customers_data = get_customer_data(total_customers)
    customer_ids = [customer["customer_id"] for customer in customers_data]

    orders_data = get_orders_data(customer_ids, order_data_sample_size)

    # Create directories if they don't exist
    # create_directory_if_not_exists("customers")
    create_directory_if_not_exists("orders")

    # Save customer data as TSV
    # customer_file_name = f"customers/{uuid.uuid4()}_customers.csv"
    # save_to_tsv(customers_data, customer_file_name)

    # Save order data as TSV
    order_file_name = f"orders/{uuid.uuid4()}_orders.csv"
    print("File: ", order_file_name)
    save_to_tsv(orders_data, order_file_name)

while True:
    # Call the function to generate and save data
    generate_and_save_data()
    time.sleep(1)

