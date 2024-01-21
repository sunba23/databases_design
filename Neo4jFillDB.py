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
    journey = RelatedFrom("Journey", "TAKEN_BY")
    ticket = RelatedFrom("Ticket", "PURCHASED_BY")

class Vehicle(GraphObject):
    __primarykey__ = "VehicleID"
    VehicleID = Property()
    RegistrationNumber = Property()
    vehicle_type = RelatedTo("VehicleType", "IS_TYPE")
    carrier = RelatedTo("Carrier", "OPERATED_BY")
    line = RelatedTo("Line", "HAS_COURSE")
    amenity = RelatedTo("Amenity", "OFFERS")

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
    vehicles = RelatedFrom("Vehicle", "OPERATED_BY")

#amenity
class Amenity(GraphObject):
    __primarykey__ = "AmenityID"
    AmenityID = Property()
    Name = Property()
    vehicle = RelatedFrom("Vehicle", "OFFERS")

# course
class Course(GraphObject):
    __primarykey__ = "CourseID"
    CourseID = Property()

# journey
class Journey(GraphObject):
    __primarykey__ = "JourneyID"
    JourneyID = Property()
    user = RelatedTo("User", "TAKEN_BY")
    schedule = RelatedTo("Schedule", "FOLLOWS_SCHEDULE")
    transfer = RelatedTo("Transfer", "HAS_TRANSFER")

# line
class Line(GraphObject):
    __primarykey__ = "LineID"
    LineID = Property()
    LineNumber = Property()
    transfer = RelatedFrom("Transfer", "CONNECTS_LINE")
    route = RelatedTo("Route", "FOLLOWS")
    vehicle = RelatedFrom("Vehicle","HAS_COURSE")
    swapMax = RelatedFrom("Swap", "HAS_MAX_STOP")
    swapMin = RelatedFrom("Swap", "HAS_MIN_STOP")
    swap = RelatedFrom("Line", "HAS_ORIGIN_LINE")
    newSwap = RelatedFrom("Swap", "HAS_NEW_LINE")


# obstacle
class Obstacle(GraphObject):
    __primarykey__ = "ObstacleID"
    ObstacleID = Property()
    Description = Property()
    route = RelatedFrom("Route", "FACES_OBSTACLE")

# route
class Route(GraphObject):
    __primarykey__ = "RouteID"
    RouteID = Property()
    Description = Property()
    Name = Property()
    transfer = RelatedFrom("Transfer", "CONNECTS_ROUTE")
    obstacle = RelatedTo("Obstacle", "FACES_OBSTACLE")
    stop = RelatedTo("Route", "STOPS_AT")
    line = RelatedFrom("Line", "FOLLOWS")

# schedule
class Schedule(GraphObject):
    __primarykey__ = "ScheduleID"
    ScheduleID = Property()
    DepartureTime = Property()
    ArrivalTime = Property()
    journey = RelatedFrom("Journey", "FOLLOWS_SCHEDULE")

# stop
class Stop(GraphObject):
    __primarykey__ = "StopID"
    StopID = Property()
    Name = Property()
    transfer = RelatedFrom("Transfer", "CONNECTS_STOP")
    route = RelatedFrom("Route", "STOPS_AT")
    
# swap
class Swap(GraphObject):
    __primarykey__ = "SwapID"
    SwapID = Property()
    ticket = RelatedFrom("Ticket", "ELIGIBLE_FOR")
    maxline = RelatedTo("Line", "HAS_MAX_STOP")
    minline = RelatedTo("Line", "HAS_MIN_STOP")
    line = RelatedTo("Line", "HAS_ORIGIN_LINE")
    newLine = RelatedTo("Line", "HAS_NEW_LINE")
    
# ticket
class Ticket(GraphObject):
    __primarykey__ = "TicketID"
    TicketID = Property()
    Price = Property()
    swap = RelatedTo("Swap", "ELIGIBLE_FOR")
    user = RelatedTo("User", "PURCHASED_BY")

    
# transfer
class Transfer(GraphObject):
    __primarykey__ = "TransferID"
    TransferID = Property()
    line = RelatedTo("Line", "CONNECTS_LINE")
    route = RelatedTo("Route", "CONNECTS_ROUTE")
    stop = RelatedTo("Stop", "CONNECTS_STOP")
    journey = RelatedTo("Journey", "HAS_TRANSFER")


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

        # Create an Amenity
        amenity = Amenity()
        amenity.AmenityID = i
        amenity.Name = fake.word()
        graph.push(amenity)

        # Create a Course
        course = Course()
        course.CourseID = i
        graph.push(course)

        # Create a Carrier
        carrier = Carrier()
        carrier.CarrierID = i
        carrier.Name = fake.company()
        graph.push(carrier)

        # Create an Obstacle
        obstacle = Obstacle()
        obstacle.ObstacleID = i
        obstacle.Description = fake.sentence()
        graph.push(obstacle)

        # Create a Route
        route = Route()
        route.RouteID = i
        route.Description = fake.sentence()
        route.Name = fake.word()
        graph.push(route)

        # Create a Schedule
        schedule = Schedule()
        schedule.ScheduleID = i
        schedule.DepartureTime = fake.time()
        schedule.ArrivalTime = (datetime.now() + timedelta(hours=fake.random_int(1, 10))).time()
        graph.push(schedule)

        # Create a Stop
        stop = Stop()
        stop.StopID = i
        stop.Name = fake.word()
        graph.push(stop)

        # Create a Swap
        swap = Swap()
        swap.SwapID = i
        graph.push(swap)

        # Create a Ticket
        ticket = Ticket()
        ticket.TicketID = i
        ticket.Price = fake.random_int(10, 100)
        graph.push(ticket)

        # Create a Transfer
        transfer = Transfer()
        transfer.TransferID = i
        graph.push(transfer)

        # Create a Journey
        journey = Journey()
        journey.JourneyID = i
        graph.push(journey)

        # Create a Line
        line = Line()
        line.LineID = i
        line.LineNumber = fake.random_int(100, 999)
        graph.push(line)

        print(f"Created User, Vehicle, and UserType with ID {i}")

# Function to create relationships
def create_user_user_type_relationship(graph, count=100):
    for i in range(count):
        user = User.match(graph, i).first()
        user_type = UserType.match(graph, i % 3 + 1).first()
        user.user_type.add(user_type)
        graph.push(user)
        print(f"Created BELONGS_TO_TYPE relationship between User {i} and UserType {i % 3 + 1}")

def create_vehicle_vehicle_type_relationship(graph, count=100):
    for i in range(count):
        vehicle = Vehicle.match(graph, i).first()
        vehicle_type = VehicleType.match(graph, i % 3 + 1).first()
        vehicle.vehicle_type.add(vehicle_type)
        graph.push(vehicle)
        print(f"Created IS_TYPE relationship between Vehicle {i} and VehicleType {i % 3 + 1}")

def create_vehicle_carrier_relationship(graph, count=100):
    for i in range(count):
        vehicle = Vehicle.match(graph, i).first()
        carrier = Carrier.match(graph, i).first()
        vehicle.carrier.add(carrier)
        graph.push(vehicle)
        print(f"Created OPERATED_BY relationship between Vehicle {i} and Carrier {i}")

def create_vehicle_line_relationship(graph, count=100):
    for i in range(count):
        vehicle = Vehicle.match(graph, i).first()
        line = Line.match(graph, i).first()
        vehicle.line.add(line)
        graph.push(vehicle)
        print(f"Created HAS_COURSE relationship between Vehicle {i} and Line {i}")

def create_amenity_vehicle_relationship(graph, count=100):
    for i in range(count):
        amenity = Amenity.match(graph, i).first()
        vehicle = Vehicle.match(graph, i).first()
        amenity.vehicle.add(vehicle)
        graph.push(amenity)
        print(f"Created OFFERS relationship between Amenity {i} and Vehicle {i}")

def create_journey_user_relationship(graph, count=100):
    for i in range(count):
        journey = Journey.match(graph, i).first()
        user = User.match(graph, i).first()
        journey.user.add(user)
        graph.push(journey)
        print(f"Created TAKEN_BY relationship between Journey {i} and User {i}")

def create_journey_schedule_relationship(graph, count=100):
    for i in range(count):
        journey = Journey.match(graph, i).first()
        schedule = Schedule.match(graph, i).first()
        journey.schedule.add(schedule)
        graph.push(journey)
        print(f"Created FOLLOWS_SCHEDULE relationship between Journey {i} and Schedule {i}")

def create_journey_transfer_relationship(graph, count=100):
    for i in range(count):
        journey = Journey.match(graph, i).first()
        transfer = Transfer.match(graph, i).first()
        journey.transfer.add(transfer)
        graph.push(journey)
        print(f"Created HAS_TRANSFER relationship between Journey {i} and Transfer {i}")

def create_line_transfer_relationship(graph, count=100):
    for i in range(count):
        line = Line.match(graph, i).first()
        transfer = Transfer.match(graph, i).first()
        line.transfer.add(transfer)
        graph.push(line)
        print(f"Created CONNECTS_LINE relationship between Line {i} and Transfer {i}")

def create_line_route_relationship(graph, count=100):
    for i in range(count):
        line = Line.match(graph, i).first()
        route = Route.match(graph, i).first()
        line.route.add(route)
        graph.push(line)
        print(f"Created FOLLOWS relationship between Line {i} and Route {i}")

def create_line_vehicle_relationship(graph, count=100):
    for i in range(count):
        line = Line.match(graph, i).first()
        vehicle = Vehicle.match(graph, i).first()
        line.vehicle.add(vehicle)
        graph.push(line)
        print(f"Created HAS_COURSE relationship between Line {i} and Vehicle {i}")

def create_line_swap_relationships(graph, count=100):
    for i in range(count):
        line = Line.match(graph, i).first()
        swap_max = Swap.match(graph, i).first()
        swap_min = Swap.match(graph, i).first()
        swap_origin = Swap.match(graph, i).first()
        swap_new = Swap.match(graph, i).first()

        line.swapMax.add(swap_max)
        line.swapMin.add(swap_min)
        line.swap.add(swap_origin)
        line.newSwap.add(swap_new)

        graph.push(line)
        print(f"Created HAS_MAX_STOP, HAS_MIN_STOP, HAS_ORIGIN_LINE, and HAS_NEW_LINE relationships for Line {i}")

def create_obstacle_route_relationship(graph, count=100):
    for i in range(count):
        obstacle = Obstacle.match(graph, i).first()
        route = Route.match(graph, i).first()
        route.obstacle.add(obstacle)
        graph.push(route)
        print(f"Created FACES_OBSTACLE relationship between Route {i} and Obstacle {i}")

def create_route_transfer_relationship(graph, count=100):
    for i in range(count):
        route = Route.match(graph, i).first()
        transfer = Transfer.match(graph, i).first()
        route.transfer.add(transfer)
        graph.push(route)
        print(f"Created CONNECTS_ROUTE relationship between Route {i} and Transfer {i}")

def create_route_stop_relationship(graph, count=100):
    for i in range(count):
        route = Route.match(graph, i).first()
        stop = Stop.match(graph, i).first()
        route.stop.add(stop)
        graph.push(route)
        print(f"Created STOPS_AT relationship between Route {i} and Stop {i}")

def create_schedule_journey_relationship(graph, count=100):
    for i in range(count):
        schedule = Schedule.match(graph, i).first()
        journey = Journey.match(graph, i).first()
        schedule.journey.add(journey)
        graph.push(schedule)
        print(f"Created FOLLOWS_SCHEDULE relationship between Schedule {i} and Journey {i}")

def create_stop_transfer_relationship(graph, count=100):
    for i in range(count):
        stop = Stop.match(graph, i).first()
        transfer = Transfer.match(graph, i).first()
        stop.transfer.add(transfer)
        graph.push(stop)
        print(f"Created CONNECTS_STOP relationship between Stop {i} and Transfer {i}")

def create_swap_ticket_relationship(graph, count=100):
    for i in range(count):
        swap = Swap.match(graph, i).first()
        ticket = Ticket.match(graph, i).first()
        swap.ticket.add(ticket)
        graph.push(swap)
        print(f"Created ELIGIBLE_FOR relationship between Swap {i} and Ticket {i}")

def create_ticket_user_relationship(graph, count=100):
    for i in range(count):
        ticket = Ticket.match(graph, i).first()
        user = User.match(graph, i).first()
        ticket.user.add(user)
        graph.push(ticket)
        print(f"Created PURCHASED_BY relationship between Ticket {i} and User {i}")

def create_transfer_line_relationship(graph, count=100):
    for i in range(count):
        transfer = Transfer.match(graph, i).first()
        line = Line.match(graph, i).first()
        transfer.line.add(line)
        graph.push(transfer)
        print(f"Created CONNECTS_LINE relationship between Transfer {i} and Line {i}")

def create_transfer_route_relationship(graph, count=100):
    for i in range(count):
        transfer = Transfer.match(graph, i).first()
        route = Route.match(graph, i).first()
        transfer.route.add(route)
        graph.push(transfer)
        print(f"Created CONNECTS_ROUTE relationship between Transfer {i} and Route {i}")

# Example usage
create_fake_data(graph, 100)
create_user_user_type_relationship(graph, 100)
