from py2neo import Graph
from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedFrom
from faker import Faker

# Node classes with relationships
class User(GraphObject):
    __primarykey__ = "UserID"
    UserID = Property()
    Username = Property()
    Email = Property()
    CreatedAt = Property()
    user_type = RelatedTo("UserType", "BELONGS_TO_TYPE")

class Vehicle(GraphObject):
    __primarykey__ = "VehicleID"
    VehicleID = Property()
    RegistrationNumber = Property()
    vehicle_type = RelatedTo("VehicleType", "IS_TYPE")

class UserType(GraphObject):
    __primarykey__ = "UserTypeID"
    UserTypeID = Property()
    Name = Property()
    users = RelatedFrom("User", "BELONGS_TO_TYPE")

class VehicleType(GraphObject):
    __primarykey__ = "VehicleTypeID"
    VehicleTypeID = Property()
    Name = Property()
    vehicles = RelatedFrom("Vehicle", "IS_TYPE")

class Carrier(GraphObject):
    __primarykey__ = "CarrierID"
    CarrierID = Property()
    Name = Property()

# Connection details
url = "neo4j+ssc://4ded0f22.databases.neo4j.io:7687"
username = "neo4j"
password = "W66d6QKJuhIc3mumAiRC4M48-ClHCgCI_pqSKzCUWdo"

# Establishing a connection to the Neo4j database
graph = Graph(url, auth=(username, password))

# Function to create fake data
fake = Faker()
def create_fake_data(graph, count=100):
    for i in range(count):
        # Create a User
        user = User()
        user.UserID = i  # It's better to use a unique identifier
        user.Username = fake.user_name()
        user.Email = fake.email()
        user.CreatedAt = fake.iso8601()
        graph.push(user)

        # Create a Vehicle
        vehicle = Vehicle()
        vehicle.VehicleID = i  # It's better to use a unique identifier
        vehicle.RegistrationNumber = fake.license_plate()
        graph.push(vehicle)

        # Create a UserType
        user_type = UserType()
        user_type.UserTypeID = i % 3 + 1  # Assuming three types for demonstration
        user_type.Name = fake.word()
        graph.push(user_type)

        print(f"Created User, Vehicle, and UserType with ID {i}")

# Function to create relationships
def create_user_user_type_relationship(graph, count=100):
    for i in range(count):
        user = User.match(graph, i).first()
        user_type = UserType.match(graph, i % 3 + 1).first()
        user.user_type.add(user_type)
        graph.push(user)
        print(f"Created BELONGS_TO_TYPE relationship between User {i} and UserType {i % 3 + 1}")

# Example usage
create_fake_data(graph, 100)
create_user_user_type_relationship(graph, 100)
