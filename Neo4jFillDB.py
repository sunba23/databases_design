from datetime import datetime, timedelta
import random
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

        # Create a VehicleType

        vehicle_type = VehicleType()
        vehicle_type.VehicleTypeID = i % 3 + 1  # Assuming three types for demonstration
        vehicle_type.Name = fake.word()
        graph.push(vehicle_type)

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

# Function to create relationships with more randomness
def create_user_user_type_relationship(graph, count=100):
    all_users = list(User.match(graph))
    all_user_types = list(UserType.match(graph))

    for i in range(count):
        selected_user = random.choice(all_users)
        selected_user_type = random.choice(all_user_types)
        selected_user.user_type.add(selected_user_type)
        graph.push(selected_user)
        print(f"Created BELONGS_TO_TYPE relationship between User {selected_user.UserID} and UserType {selected_user_type.UserTypeID}")

def create_vehicle_vehicle_type_relationship(graph, count=100):
    all_vehicles = list(Vehicle.match(graph))
    all_vehicle_types = list(VehicleType.match(graph))

    for i in range(count):
        selected_vehicle = random.choice(all_vehicles)
        selected_vehicle_type = random.choice(all_vehicle_types)
        selected_vehicle.vehicle_type.add(selected_vehicle_type)
        graph.push(selected_vehicle)
        print(f"Created IS_TYPE relationship between Vehicle {selected_vehicle.VehicleID} and VehicleType {selected_vehicle_type.VehicleTypeID}")

def create_vehicle_carrier_relationship(graph, count=100):
    all_vehicles = list(Vehicle.match(graph))
    all_carriers = list(Carrier.match(graph))

    for i in range(count):
        selected_vehicle = random.choice(all_vehicles)
        selected_carrier = random.choice(all_carriers)
        selected_vehicle.carrier.add(selected_carrier)
        graph.push(selected_vehicle)
        print(f"Created OPERATED_BY relationship between Vehicle {selected_vehicle.VehicleID} and Carrier {selected_carrier.CarrierID}")

def create_vehicle_line_relationship(graph, count=100):
    all_vehicles = list(Vehicle.match(graph))
    all_lines = list(Line.match(graph))

    for i in range(count):
        selected_vehicle = random.choice(all_vehicles)
        selected_line = random.choice(all_lines)
        selected_vehicle.line.add(selected_line)
        graph.push(selected_vehicle)
        print(f"Created HAS_COURSE relationship between Vehicle {selected_vehicle.VehicleID} and Line {selected_line.LineID}")

def create_amenity_vehicle_relationship(graph, count=100):
    all_amenities = list(Amenity.match(graph))
    all_vehicles = list(Vehicle.match(graph))

    for i in range(count):
        selected_amenity = random.choice(all_amenities)
        selected_vehicle = random.choice(all_vehicles)
        selected_amenity.vehicle.add(selected_vehicle)
        graph.push(selected_amenity)
        print(f"Created OFFERS relationship between Amenity {selected_amenity.AmenityID} and Vehicle {selected_vehicle.VehicleID}")

def create_journey_user_relationship(graph, count=100):
    all_journeys = list(Journey.match(graph))
    all_users = list(User.match(graph))

    for i in range(count):
        selected_journey = random.choice(all_journeys)
        selected_user = random.choice(all_users)
        selected_journey.user.add(selected_user)
        graph.push(selected_journey)
        print(f"Created TAKEN_BY relationship between Journey {selected_journey.JourneyID} and User {selected_user.UserID}")

def create_journey_schedule_relationship(graph, count=100):
    all_journeys = list(Journey.match(graph))
    all_schedules = list(Schedule.match(graph))

    for i in range(count):
        selected_journey = random.choice(all_journeys)
        selected_schedule = random.choice(all_schedules)
        selected_journey.schedule.add(selected_schedule)
        graph.push(selected_journey)
        print(f"Created FOLLOWS_SCHEDULE relationship between Journey {selected_journey.JourneyID} and Schedule {selected_schedule.ScheduleID}")

def create_journey_transfer_relationship(graph, count=100):
    all_journeys = list(Journey.match(graph))
    all_transfers = list(Transfer.match(graph))

    for i in range(count):
        selected_journey = random.choice(all_journeys)
        selected_transfer = random.choice(all_transfers)
        selected_journey.transfer.add(selected_transfer)
        graph.push(selected_journey)
        print(f"Created HAS_TRANSFER relationship between Journey {selected_journey.JourneyID} and Transfer {selected_transfer.TransferID}")

def create_line_transfer_relationship(graph, count=100):
    all_lines = list(Line.match(graph))
    all_transfers = list(Transfer.match(graph))

    for i in range(count):
        selected_line = random.choice(all_lines)
        selected_transfer = random.choice(all_transfers)
        selected_line.transfer.add(selected_transfer)
        graph.push(selected_line)
        print(f"Created CONNECTS_LINE relationship between Line {selected_line.LineID} and Transfer {selected_transfer.TransferID}")

def create_line_route_relationship(graph, count=100):
    all_lines = list(Line.match(graph))
    all_routes = list(Route.match(graph))

    for i in range(count):
        selected_line = random.choice(all_lines)
        selected_route = random.choice(all_routes)
        selected_line.route.add(selected_route)
        graph.push(selected_line)
        print(f"Created FOLLOWS relationship between Line {selected_line.LineID} and Route {selected_route.RouteID}")

def create_line_vehicle_relationship(graph, count=100):
    all_lines = list(Line.match(graph))
    all_vehicles = list(Vehicle.match(graph))

    for i in range(count):
        selected_line = random.choice(all_lines)
        selected_vehicle = random.choice(all_vehicles)
        selected_line.vehicle.add(selected_vehicle)
        graph.push(selected_line)
        print(f"Created HAS_COURSE relationship between Line {selected_line.LineID} and Vehicle {selected_vehicle.VehicleID}")

def create_line_swap_relationships(graph, count=100):
    all_lines = list(Line.match(graph))
    all_swaps = list(Swap.match(graph))

    for i in range(count):
        selected_line = random.choice(all_lines)
        selected_swap_max = random.choice(all_swaps)
        selected_swap_min = random.choice(all_swaps)
        selected_swap_origin = random.choice(all_swaps)
        selected_swap_new = random.choice(all_swaps)

        selected_line.swapMax.add(selected_swap_max)
        selected_line.swapMin.add(selected_swap_min)
        selected_line.swap.add(selected_swap_origin)
        selected_line.newSwap.add(selected_swap_new)

        graph.push(selected_line)
        print(f"Created HAS_MAX_STOP, HAS_MIN_STOP, HAS_ORIGIN_LINE, and HAS_NEW_LINE relationships for Line {selected_line.LineID}")


def create_obstacle_route_relationship(graph, count=100):
    all_obstacles = list(Obstacle.match(graph))
    all_routes = list(Route.match(graph))

    for i in range(count):
        selected_obstacle = random.choice(all_obstacles)
        selected_route = random.choice(all_routes)
        selected_route.obstacle.add(selected_obstacle)
        graph.push(selected_route)
        print(f"Created FACES_OBSTACLE relationship between Route {selected_route.RouteID} and Obstacle {selected_obstacle.ObstacleID}")

def create_route_transfer_relationship(graph, count=100):
    all_routes = list(Route.match(graph))
    all_transfers = list(Transfer.match(graph))

    for i in range(count):
        selected_route = random.choice(all_routes)
        selected_transfer = random.choice(all_transfers)
        selected_route.transfer.add(selected_transfer)
        graph.push(selected_route)
        print(f"Created CONNECTS_ROUTE relationship between Route {selected_route.RouteID} and Transfer {selected_transfer.TransferID}")

def create_route_stop_relationship(graph, count=100):
    all_routes = list(Route.match(graph))
    all_stops = list(Stop.match(graph))

    for i in range(count):
        selected_route = random.choice(all_routes)
        selected_stop = random.choice(all_stops)
        selected_route.stop.add(selected_stop)
        graph.push(selected_route)
        print(f"Created STOPS_AT relationship between Route {selected_route.RouteID} and Stop {selected_stop.StopID}")

def create_schedule_journey_relationship(graph, count=100):
    all_schedules = list(Schedule.match(graph))
    all_journeys = list(Journey.match(graph))

    for i in range(count):
        selected_schedule = random.choice(all_schedules)
        selected_journey = random.choice(all_journeys)
        selected_schedule.journey.add(selected_journey)
        graph.push(selected_schedule)
        print(f"Created FOLLOWS_SCHEDULE relationship between Schedule {selected_schedule.ScheduleID} and Journey {selected_journey.JourneyID}")

def create_stop_transfer_relationship(graph, count=100):
    all_stops = list(Stop.match(graph))
    all_transfers = list(Transfer.match(graph))

    for i in range(count):
        selected_stop = random.choice(all_stops)
        selected_transfer = random.choice(all_transfers)
        selected_stop.transfer.add(selected_transfer)
        graph.push(selected_stop)
        print(f"Created CONNECTS_STOP relationship between Stop {selected_stop.StopID} and Transfer {selected_transfer.TransferID}")

def create_swap_ticket_relationship(graph, count=100):
    all_swaps = list(Swap.match(graph))
    all_tickets = list(Ticket.match(graph))

    for i in range(count):
        selected_swap = random.choice(all_swaps)
        selected_ticket = random.choice(all_tickets)
        selected_swap.ticket.add(selected_ticket)
        graph.push(selected_swap)
        print(f"Created ELIGIBLE_FOR relationship between Swap {selected_swap.SwapID} and Ticket {selected_ticket.TicketID}")

def create_ticket_user_relationship(graph, count=100):
    all_tickets = list(Ticket.match(graph))
    all_users = list(User.match(graph))

    for i in range(count):
        selected_ticket = random.choice(all_tickets)
        selected_user = random.choice(all_users)
        selected_ticket.user.add(selected_user)
        graph.push(selected_ticket)
        print(f"Created PURCHASED_BY relationship between Ticket {selected_ticket.TicketID} and User {selected_user.UserID}")

def create_transfer_line_relationship(graph, count=100):
    all_transfers = list(Transfer.match(graph))
    all_lines = list(Line.match(graph))

    for i in range(count):
        selected_transfer = random.choice(all_transfers)
        selected_line = random.choice(all_lines)
        selected_transfer.line.add(selected_line)
        graph.push(selected_transfer)
        print(f"Created CONNECTS_LINE relationship between Transfer {selected_transfer.TransferID} and Line {selected_line.LineID}")

def create_transfer_route_relationship(graph, count=100):
    all_transfers = list(Transfer.match(graph))
    all_routes = list(Route.match(graph))

    for i in range(count):
        selected_transfer = random.choice(all_transfers)
        selected_route = random.choice(all_routes)
        selected_transfer.route.add(selected_route)
        graph.push(selected_transfer)
        print(f"Created CONNECTS_ROUTE relationship between Transfer {selected_transfer.TransferID} and Route {selected_route.RouteID}")

def create_schedule_stop_relationship(graph,count=100):
    all_schedules = list(Schedule.match(graph))
    all_stops = list(Stop.match(graph))

    for i in range(count):
        selected_schedule = random.choice(all_schedules)
        selected_stop = random.choice(all_stops)
        selected_schedule.stop.add(selected_stop)
        graph.push(selected_schedule)
        print(f"Created STOPS_AT relationship between Schedule {selected_schedule.ScheduleID} and Stop {selected_stop.StopID}")

# Example usage
create_fake_data(graph, 100)
create_user_user_type_relationship(graph, 100)
create_vehicle_vehicle_type_relationship(graph, 100)
create_vehicle_carrier_relationship(graph, 100)
create_vehicle_line_relationship(graph, 100)
create_amenity_vehicle_relationship(graph, 100)
create_journey_user_relationship(graph, 100)
create_journey_schedule_relationship(graph, 100)
create_journey_transfer_relationship(graph, 100)
create_line_transfer_relationship(graph, 100)
create_line_route_relationship(graph, 100)
create_line_vehicle_relationship(graph, 100)
create_line_swap_relationships(graph, 100)
create_obstacle_route_relationship(graph, 100)
create_route_transfer_relationship(graph, 100)
create_route_stop_relationship(graph, 100)
create_schedule_journey_relationship(graph, 100)
create_stop_transfer_relationship(graph, 100)
create_swap_ticket_relationship(graph, 100)
create_ticket_user_relationship(graph, 100)
create_transfer_line_relationship(graph, 100)
create_transfer_route_relationship(graph, 100)
