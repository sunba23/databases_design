-- Amenities table
CREATE UNIQUE INDEX idx_Amenities_AmenityID_hash ON "Amenities"(name);

-- VehicleType table
CREATE UNIQUE INDEX idx_VehicleType_VehicleTypeID_hash ON "VehicleType"(name);

-- UserType table
CREATE UNIQUE INDEX idx_UserType_UserTypeID_hash ON "UserType"(name);

-- Carriers table
CREATE UNIQUE INDEX idx_Carriers_CarrierID_hash ON "Carriers"(name);

-- Line table
CREATE INDEX idx_Line_LineID_hash ON "Line" USING hash (LineID);
CREATE INDEX idx_Line_LineNum ON "Line" using hash (linenumber);

-- User table


-- Route table
CREATE INDEX idx_Route_RouteID_hash ON "Route" USING hash (RouteID);

-- Obstacles table
CREATE UNIQUE INDEX idx_Obstacles_ObstacleID_hash ON "Obstacles"(description);

-- Ticket table


-- Schedule table


-- Vehicle table
CREATE INDEX idx_Vehicle_VehicleID_hash ON "Vehicle" USING hash (VehicleID);


-- Journey table


-- Course table
CREATE INDEX idx_Course_CourseID_hash ON "Course" using hash(courseid);

-- Transfer table

-- Stop table

CREATE INDEX idx_Stop_StopID_hash on "Stop" using hash(stopid);




