from faker import Faker
import random
import csv

def generate_fake_data(num_entries):
    fake = Faker()

    # Create a list to store fake data entries
    fake_data = []

    # Generate fake data entries
    for _ in range(num_entries):
        op = random.choice(['I', 'U', 'D'])
        replicadmstimestamp = fake.date_time_this_year()
        invoiceid = fake.unique.random_number(digits=5)
        itemid = fake.unique.random_number(digits=2)
        category = fake.word()
        price = round(random.uniform(10, 100), 2)
        quantity = random.randint(1, 5)
        orderdate = fake.date_this_decade()
        destinationstate = fake.state_abbr()
        shippingtype = random.choice(['2-Day', '3-Day', 'Standard'])
        referral = fake.word()

        # Append data to the list
        fake_data.append([op, replicadmstimestamp, invoiceid, itemid, category, price, quantity, orderdate, destinationstate, shippingtype, referral])

    return fake_data

def generate_csv_from_data(data, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        # Create a CSV writer
        csv_writer = csv.writer(csvfile, delimiter='\t')

        # Write the header
        csv_writer.writerow(['Op', 'replicadmstimestamp', 'invoiceid', 'itemid', 'category', 'price', 'quantity', 'orderdate', 'destinationstate', 'shippingtype', 'referral'])

        # Write the fake data
        csv_writer.writerows(data)

    print(f"CSV file '{output_file}' generated successfully.")

# Set the number of fake data entries to generate
num_entries = 10

# Generate fake data
fake_data = generate_fake_data(num_entries)

# Specify the output file name
output_file = "generated_fake_data.csv"

# Generate CSV file from fake data
generate_csv_from_data(fake_data, output_file)
