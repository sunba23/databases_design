-- VehicleType Table
CREATE TABLE VehicleType (
    VehicleTypeID SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL UNIQUE,
);

-- UserType Table
CREATE TABLE UserType (
    UserTypeID SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL UNIQUE,
);

-- Carriers Table
CREATE TABLE Carriers (
    CarrierID SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL UNIQUE,
);

-- Line Table
CREATE TABLE Line (
    LineID SERIAL PRIMARY KEY,
    LineNumber INT

    CHECK (LineNumber >= 0),
);

-- User Table
CREATE TABLE "User" (
    UserID SERIAL PRIMARY KEY,
    Username VARCHAR(255) NOT NULL UNIQUE,
    Password VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL UNIQUE,
    CreatedAt TIMESTAMP NOT NULL DEFAULT NOW(),
    UserTypeID INT REFERENCES UserType(UserTypeID) DEFAULT 1 ON DELETE RESTRICT,


    CHECK (Email LIKE '%@%.%'),
);

-- Schedule Table
CREATE TABLE Schedule (
    ScheduleID SERIAL PRIMARY KEY,
    LineID INT REFERENCES Line(LineID) ON DELETE CASCADE,
    StopID INT NOT NULL UNIQUE REFERENCES Stop(StopID) ON DELETE RESTRICT ON UPDATE CASCADE,
    DepartureTime TIMESTAMP NOT NULL,
    ArrivalTime TIMESTAMP NOT NULL,

    CHECK (DepartureTime > ArrivalTime)
);

-- Stop Table
CREATE TABLE Stop (
    StopID SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL UNIQUE,
);

-- Vehicle Table
CREATE TABLE Vehicle (
    VehicleID SERIAL PRIMARY KEY,
    RegistrationNumber VARCHAR(255) NOT NULL UNIQUE,
    VehicleTypeID INT NOT NULL REFERENCES VehicleType(VehicleTypeID) ON DELETE RESTRICT,
);

-- Amenities Table
CREATE TABLE Amenities (
    AmenityID SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL UNIQUE,
    Description VARCHAR(255)
);

-- Journey Table
CREATE TABLE Journey (
    JourneyID SERIAL PRIMARY KEY,
    UserID INT REFERENCES "User"(UserID) ON DELETE CASCADE ON UPDATE RESTRICT,
    TicketID INT REFERENCES Ticket(TicketID) ON DELETE NO ACTION ON UPDATE RESTRICT,
    ScheduleID INT REFERENCES Schedule(ScheduleID)
);

-- Course Table
CREATE TABLE Course (
    CourseID SERIAL PRIMARY KEY,
    CourseNumber INT NOT NULL UNIQUE,

    CHECK (CourseNumber > 0),
);

-- Route Table
CREATE TABLE Route (
    RouteID SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL UNIQUE,
    Description VARCHAR(255)
);

-- Obstacles Table
CREATE TABLE Obstacles (
    ObstacleID SERIAL PRIMARY KEY,
    Description VARCHAR(255),
);

-- Ticket Table
CREATE TABLE Ticket (
    TicketID SERIAL PRIMARY KEY,
    Price DECIMAL(8, 2),
    LineID INT REFERENCES Line(LineID),

    CHECK (Price >= 0)
);

-- Transfer Table
CREATE TABLE Transfer (
    TransferID SERIAL PRIMARY KEY,
    RouteID INT REFERENCES Route(RouteID),
    StopID INT REFERENCES Stop(StopID),
    LineID INT REFERENCES Line(LineID),
    JourneyID INT REFERENCES Journey(JourneyID)
);

-- VehicleAmenity Table
CREATE TABLE VehicleAmenity (
    VehicleAmenityID SERIAL PRIMARY KEY,
    VehicleID INT REFERENCES Vehicle(VehicleID) ON DELETE CASCADE,
    AmenityID INT REFERENCES Amenities(AmenityID) ON DELETE CASCADE,
);

-- CarrierVehicle Table
CREATE TABLE CarrierVehicle (
    CarrierVehicleID SERIAL PRIMARY KEY,
    CarrierID INT REFERENCES Carriers(CarrierID) ON DELETE RESTRICT ON UPDATE CASCADE,
    VehicleID INT REFERENCES Vehicle(VehicleID) ON DELETE CASCADE ON UPDATE CASCADE,
);

-- LineRoutes Table
CREATE TABLE LineRoutes (
    LineRouteID SERIAL PRIMARY KEY,
    RouteID INT REFERENCES Route(RouteID) ON UPDATE CASCADE ON DELETE RESTRICT,
    LineID INT REFERENCES Line(LineID) ON UPDATE CASCADE ON DELETE CASCADE
);

-- RouteStops Table
CREATE TABLE RouteStops (
    RouteStopID SERIAL PRIMARY KEY,
    StopID INT REFERENCES Stop(StopID) ON DELETE RESTRICT ON UPDATE CASCADE,
    RouteID INT REFERENCES Route(RouteID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- RouteObstacles Table
CREATE TABLE RouteObstacles (
    RouteObstacleID SERIAL PRIMARY KEY,
    ObstacleID INT REFERENCES Obstacles(ObstacleID) ON UPDATE CASCADE ON DELETE CASCADE,
    RouteID INT REFERENCES Route(RouteID) ON UPDATE CASCADE ON DELETE CASCADE
);
