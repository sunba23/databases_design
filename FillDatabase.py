import psycopg2
from random import choice, randint
from faker import Faker
from datetime import datetime, timedelta
import random

# Database connection parameters
db_params = {
    'host': 'localhost',
    'database': 'Bazury',
    'user': 'postgres',
    'password': 'Sianuga123'
}

# Create a connection to the database
conn = psycopg2.connect(**db_params)
cur = conn.cursor()
print("Connected to the database")
# Create a Faker object to generate random data
fake = Faker()

conn.autocommit = True

# # # Create tables
# cur.execute("INSERT INTO information_schema.\"UserType\" (Name) VALUES (%s);", ('Admin',))
# Insert data into the tables

vehicle_types = ['Metro', 'Bus', 'Tram']
user_type = ['Admin', 'User', 'Guest']
carriers = ['Shelton-Mcpherson', 'Harris PLC', 'Watkins PLC', 'Lutz Group', 'Skinner PLC', 'Nicholson, Cline and Jones', 'Rogers, Soto and Galloway', 'Cooper-Bartlett', 'Moore-Horn', 'Martin, May and Stone']
amenities = ['Wheelchair Accessible', 'Air Conditioning', 'Wifi', 'Jacuzzi', 'TV', 'Bar', 'Restaurant', 'Toilet', 'Bed', 'Shower', 'Cinema', 'Bowling']
obstacles = ['Traffic', 'Roadworks', 'Accident', 'Weather', 'Other']

vehicleNumber = 3000
routeNumber = 3000
stopsNumber = 6000
lineNumber = 200
scheduleNumber = 50000
userNumber = 10000
ticketNumber = 10000
journeyNumber = 10000

random.shuffle(vehicle_types)
random.shuffle(user_type)
random.shuffle(carriers)
random.shuffle(amenities)
random.shuffle(obstacles)


# List of table names to clear
tables_to_clear = ["\"Vehicle\"", "\"User\"", "\"UserType\"", "\"Carriers\"", "\"Line\"", "\"VehicleType\"", "\"Amenities\"", "\"Course\"", "\"Route\"", "\"Obstacles\"", "\"Stop\"", "\"RouteObstacles\"", "\"RouteStops\"", "\"LineRoutes\"", "\"Schedule\"", "\"Ticket\"", "\"Journey\"", "\"Transfer\"", "\"CarrierVehicle\"", "\"VehicleAmenity\""]

for table_name in tables_to_clear:
    # Use the DELETE statement to clear the table
    delete_query = f"DELETE FROM information_schema.{table_name};"
    cur.execute(delete_query)

print("Cleared the tables")
i=0
for vehicle_type in vehicle_types:
    cur.execute("INSERT INTO information_schema.\"VehicleType\" (VehicleTypeID, Name) VALUES (%s,%s);", ( i+1,vehicle_type))
    i+=1
print("VehicleTypes added")
i=0
for user in user_type:
    cur.execute("INSERT INTO information_schema.\"UserType\" (UserTypeID,Name) VALUES (%s,%s);", (i+1,user))
    i+=1
print("UserTypes added")
i=0
for carrier in carriers:
    cur.execute("INSERT INTO information_schema.\"Carriers\" (CarrierID,Name) VALUES (%s,%s);", (i+1,carrier))
    i+=1
print("Carriers added")
i=0
for amenity in amenities:
    cur.execute("INSERT INTO information_schema.\"Amenities\" (AmenityID,Name) VALUES (%s,%s);", (i+1,amenity))
    i+=1
print("Amenities added")
i=0
for obstacle in obstacles:
    cur.execute("INSERT INTO information_schema.\"Obstacles\" (ObstacleID,Description) VALUES (%s,%s);", (i+1,obstacle))
    i+=1
print("Obstacles added")



for _ in range(vehicleNumber):
    license_plate = fake.license_plate()
    vehicle_type_id = randint(1, 3)
    cur.execute("INSERT INTO information_schema.\"Vehicle\" (VehicleID,RegistrationNumber, VehicleTypeID) VALUES (%s, %s, %s);", (_+1,license_plate+str(randint(1,100)+_), vehicle_type_id))
    cur.execute("INSERT INTO information_schema.\"CarrierVehicle\" (CarrierID, VehicleID) VALUES ( %s, %s);", ( randint(1, len(carriers)),_+1 ))
    cur.execute("INSERT INTO information_schema.\"VehicleAmenity\" (VehicleID, AmenityID) VALUES ( %s, %s);", ( _+1, randint(1, len(amenities))))


for _ in range(6000):
    cur.execute('INSERT INTO information_schema.\"Stop\" (StopID,Name) VALUES (%s,%s);', (_+1,fake.street_name() + " " + fake.street_suffix() +" "+str(randint(1,37))))

for _ in range (userNumber):

    email = fake.email().split("@")
    email = email[0] + str(_) + "@" + email[1]

    username = fake.user_name() + str(_)
    cur.execute("INSERT INTO information_schema.\"User\" (UserID,Username,Password,Email,CreatedAt,UserTypeID) VALUES (%s,%s,%s,%s,%s,%s);", (_+1,username,fake.password(),email,fake.date_time_between(start_date='-5y', end_date='now'),randint(1,len(user_type))))

lineList = []
for _ in range (200):
    lineList.append(_+1)

random.shuffle(lineList)

for _ in range(lineNumber):
    cur.execute("INSERT INTO information_schema.\"Line\" (LineID,LineNumber) VALUES (%s,%s);", (_+1,random.choice(lineList)))
print("Lines added")
for _ in range(routeNumber):
    cur.execute("INSERT INTO information_schema.\"Route\" (RouteID,Name,Description) VALUES (%s,%s,%s);", (_+1,fake.city() + fake.city(),fake.sentence()))
print("Routes added")
for _ in range (4000):
    cur.execute("INSERT INTO information_schema.\"Course\" (CourseID, VehicleID,LineID) VALUES (%s, %s,%s);", (_+1, randint(1, vehicleNumber),randint(1,len(lineList))))
print("Courses added")
for _ in range (300):
    cur.execute("INSERT INTO information_schema.\"RouteObstacles\" (RouteObstacleID,RouteID,ObstacleID) VALUES (%s,%s,%s);" ,(_+1,randint(1,routeNumber),randint(1,len(obstacles))))
print("RouteObstacles added")
for _ in range(10000):
    cur.execute("INSERT INTO information_schema.\"RouteStops\" (RouteStopID,RouteID,StopID) VALUES (%s,%s,%s);" ,(_+1,randint(1,routeNumber),randint(1,stopsNumber)))
print("RouteStops added")
for _ in range(800):
    cur.execute("INSERT INTO information_schema.\"LineRoutes\" (LineRouteID,RouteID,LineID) VALUES (%s,%s,%s);" ,(_+1,randint(1,routeNumber),randint(1,lineNumber)))
print("LineRoutes added")
for _ in range(scheduleNumber):
    fakeDate = fake.date_time_between(start_date='-5y', end_date='now')
    departure_time = fakeDate
    arrival_time = fakeDate - timedelta(minutes=randint(1, 5))

    # Ensure that departure_time is greater than arrival_time
    if departure_time <= arrival_time:
        arrival_time = departure_time - timedelta(minutes=randint(1, 5))
        

    cur.execute("INSERT INTO information_schema.\"Schedule\" (ScheduleID,StopID, LineID, DepartureTime, ArrivalTime) VALUES (%s,%s,%s,%s,%s);" ,(_+1,randint(1,stopsNumber),randint(1,lineNumber), departure_time, arrival_time))
print("Schedules added")
for _ in range(ticketNumber):
    cur.execute("INSERT INTO information_schema.\"Ticket\" (TicketID,LineID,Price) VALUES (%s,%s,%s);" ,(_+1,randint(1,lineNumber),randint(1,100)+randint(1,99)/100))
print("Tickets added")
for _ in range(journeyNumber):
    cur.execute("INSERT INTO information_schema.\"Journey\"(JourneyID,ScheduleID, TicketID, UserID) VALUES (%s,%s,%s,%s);" ,(_+1,randint(1,scheduleNumber),randint(1,ticketNumber),randint(1,userNumber)))
print("Journeys added")
for _ in range(10000):
    cur.execute("INSERT INTO information_schema.\"Transfer\"(TransferID,JourneyID, LineID, StopID, RouteID) VALUES (%s,%s,%s,%s,%s);" ,(_+1,randint(1,journeyNumber),randint(1,lineNumber),randint(1,stopsNumber),randint(1,routeNumber)))
print("Transfers added")
# for _ in range(100):  # You can adjust the number of rows you want to insert
#     # Insert data into the UserType table
#     cur.execute("INSERT INTO \"UserType\" (Name) VALUES (%s);", (fake.random_element(elements=('Admin', 'User', 'Guest')),))

#     # Insert data into the Carriers table
#     cur.execute("INSERT INTO Carriers (Name) VALUES (%s);", (fake.company(),))

#     # Insert data into the Line table
#     cur.execute("INSERT INTO Line (LineNumber) VALUES (%s);", (randint(100, 999),))

#     # Insert data into the VehicleType table
#     cur.execute("INSERT INTO VehicleType (Name) VALUES (%s);", (fake.random_element(elements=('Car', 'Bus', 'Truck')),))

#     # Insert data into the Amenities table
#     amenity_name = fake.word()
#     amenity_description = fake.sentence()
#     cur.execute("INSERT INTO Amenities (Name, Description) VALUES (%s, %s);", (amenity_name, amenity_description))

#     # Insert data into the Course table
#     cur.execute("INSERT INTO Course (CourseNumber) VALUES (%s);", (randint(1, 10),))

#     # Insert data into the Route table
#     route_name = fake.street_name()
#     route_description = fake.sentence()
#     cur.execute("INSERT INTO Route (Name, Description) VALUES (%s, %s);", (route_name, route_description))

#     # Insert data into the Obstacles table
#     obstacle_description = fake.sentence()
#     cur.execute("INSERT INTO Obstacles (Description) VALUES (%s);", (obstacle_description,))

# Commit the changes and close the connection
conn.commit()
print("Data inserted")
conn.close()