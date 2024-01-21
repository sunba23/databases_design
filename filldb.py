import psycopg2
from random import choice, randint
from faker import Faker
from datetime import datetime, timedelta

# Database connection parameters
db_params = {
    'host': 'localhost',
    'database': 'mpk',
    'user': 'postgres',
    'password': 'postgre'
}

# Create a connection to the database
conn = psycopg2.connect(**db_params)
cur = conn.cursor()

# Create a Faker object to generate random data
fake = Faker()

# Insert data into the tables
for _ in range(100):  # You can adjust the number of rows you want to insert
    # Insert data into the UserType table
    cur.execute("INSERT INTO UserType (Name) VALUES (%s);", (fake.random_element(elements=('Admin', 'User', 'Guest')),))

    # Insert data into the Carriers table
    cur.execute("INSERT INTO Carriers (Name) VALUES (%s);", (fake.company(),))

    # Insert data into the Line table
    cur.execute("INSERT INTO Line (LineNumber) VALUES (%s);", (randint(100, 999),))

    # Insert data into the VehicleType table
    cur.execute("INSERT INTO VehicleType (Name) VALUES (%s);", (fake.random_element(elements=('Car', 'Bus', 'Truck')),))

    # Insert data into the Amenities table
    amenity_name = fake.word()
    amenity_description = fake.sentence()
    cur.execute("INSERT INTO Amenities (Name, Description) VALUES (%s, %s);", (amenity_name, amenity_description))

    # Insert data into the Course table
    cur.execute("INSERT INTO Course (CourseNumber) VALUES (%s);", (randint(1, 10),))

    # Insert data into the Route table
    route_name = fake.street_name()
    route_description = fake.sentence()
    cur.execute("INSERT INTO Route (Name, Description) VALUES (%s, %s);", (route_name, route_description))

    # Insert data into the Obstacles table
    obstacle_description = fake.sentence()
    cur.execute("INSERT INTO Obstacles (Description) VALUES (%s);", (obstacle_description,))

# Commit the changes and close the connection
conn.commit()
conn.close()