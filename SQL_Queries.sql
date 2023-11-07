-- Liczba pojazdów z udogodnieniami
SELECT a.Name, COUNT(va.VehicleID) AS "VehiclesCount"
FROM "Amenities" a
LEFT JOIN "VehicleAmenity" va ON a.AmenityID = va.AmenityID
GROUP BY a.Name;

-- Liczba biletów zakupionych na daną linię
SELECT l.LineID, COUNT(t.ticketID) AS "TicketCount"
FROM "Line" l
LEFT JOIN "Ticket" t ON l.LineID = t.LineID
GROUP BY l.LineID
ORDER BY "TicketCount" DESC;

-- Utrudnienia na trasie jadąc z przystanku na przystanek
SELECT DISTINCT R.Name AS RouteName
FROM "Route" AS R
INNER JOIN "RouteStops" AS RS1 ON R.RouteID = RS1.RouteID
INNER JOIN "RouteStops" AS RS2 ON R.RouteID = RS2.RouteID
INNER JOIN "RouteObstacles" AS RO ON R.RouteID = RO.RouteID
INNER JOIN "Stop" AS S1 ON RS1.StopID = S1.StopID
INNER JOIN "Stop" AS S2 ON RS2.StopID = S2.StopID
WHERE S1.Name = 'A' AND S2.Name = 'B';

-- Liczba przeybytych przez użytkownika podróży w danym roku/miesiącu
SELECT COUNT(*) AS NumberOfTrips
FROM "Journey" j
JOIN "Schedule" s ON j.ScheduleID = s.ScheduleID
WHERE j.UserID = 222
AND EXTRACT(YEAR FROM s.DepartureTime) = 2022;

SELECT COUNT(*) AS NumberOfTrips
FROM "Journey" j
JOIN "Schedule" s ON j.ScheduleID = s.ScheduleID
WHERE j.UserID = 1
AND EXTRACT(MONTH FROM s.DepartureTime) = 11;


SELECT COUNT(*) AS NumberOfTrips
FROM "Journey" j
JOIN "Schedule" s ON j.ScheduleID = s.ScheduleID
WHERE j.UserID = 1
AND EXTRACT(YEAR FROM s.DepartureTime) = 2022
AND EXTRACT(MONTH FROM s.DepartureTime) = 12;


-- Pokazanie linii do przejazdu z przystanku A do B
SELECT DISTINCT L.LineID, L.LineNumber
FROM "RouteStops" AS RS1
INNER JOIN "RouteStops" AS RS2 ON RS1.RouteID = RS2.RouteID
INNER JOIN "LineRoutes" AS LR ON RS1.RouteID = LR.RouteID
INNER JOIN "Line" AS L ON LR.LineID = L.LineID
INNER JOIN "Stop" AS S1 ON RS1.StopID = S1.StopID
INNER JOIN "Stop" AS S2 ON RS2.StopID = S2.StopID
WHERE S1.Name = 'A' AND S2.Name = 'B';

-- Szukanie połączenia z przystanku A do B z 1 przesiadką

WITH ROUTEA AS(
    SELECT RS.RouteID
FROM "RouteStops" AS RS
WHERE RS.StopID = (SELECT StopID FROM "Stop" WHERE Name = 'A')
),
ROUTEB AS(
    SELECT RS.RouteID
FROM "RouteStops" AS RS
WHERE RS.StopID = (SELECT StopID FROM "Stop" WHERE Name = 'C')
)
SELECT "Route".Name AS "RouteName"
FROM "Route"
WHERE "Route".RouteID IN (
    SELECT RouteID FROM ROUTEA
    UNION
    SELECT RouteID FROM ROUTEB
);


WITH DuplicateStops AS (
    WITH ROUTEA AS (
        SELECT RS.RouteID
        FROM "RouteStops" AS RS
        WHERE RS.StopID = (SELECT StopID FROM "Stop" WHERE Name = 'A')
    ),
    ROUTEB AS (
        SELECT RS.RouteID
        FROM "RouteStops" AS RS
        WHERE RS.StopID = (SELECT StopID FROM "Stop" WHERE Name = 'C')
    )
    SELECT RS.StopID AS "StopID", "Stop".Name AS "StopName", COUNT("Stop".Name) AS "StopCount"
    FROM "RouteStops" AS RS
    JOIN "Stop" ON RS.StopID = "Stop".StopID
    WHERE RS.RouteID IN (SELECT RouteID FROM ROUTEA)
    OR RS.RouteID IN (SELECT RouteID FROM ROUTEB)
    GROUP BY "Stop".Name, RS.StopID
    HAVING COUNT("Stop".Name) > 1
)
SELECT DS."StopName", SC.LineID, L.LineNumber
FROM DuplicateStops AS DS
JOIN "Schedule" AS SC ON SC.StopID = DS."StopID"
JOIN "Line" AS L ON SC.LineID = L.LineID
GROUP BY DS."StopName", SC.LineID, L.LineNumber;



--Finałowa wersja
WITH DuplicateStops AS (
    WITH ROUTEA AS (
        SELECT RS.RouteID
        FROM "RouteStops" AS RS
        WHERE RS.StopID = (SELECT StopID FROM "Stop" WHERE Name = 'A')
    ),
    ROUTEB AS (
        SELECT RS.RouteID
        FROM "RouteStops" AS RS
        WHERE RS.StopID = (SELECT StopID FROM "Stop" WHERE Name = 'C')
    )
    SELECT RS.StopID AS "StopID", "Stop".Name AS "StopName", COUNT("Stop".Name) AS "StopCount"
    FROM "RouteStops" AS RS
    JOIN "Stop" ON RS.StopID = "Stop".StopID
    WHERE RS.RouteID IN (SELECT RouteID FROM ROUTEA)
    OR RS.RouteID IN (SELECT RouteID FROM ROUTEB)
    GROUP BY "Stop".Name, RS.StopID
    HAVING COUNT("Stop".Name) > 1
)
SELECT DS."StopName" AS "InputStopName", SC.LineID, L.LineNumber
FROM DuplicateStops AS DS
JOIN "Schedule" AS SC ON SC.StopID = DS."StopID"
JOIN "Line" AS L ON SC.LineID = L.LineID
WHERE EXISTS (
    SELECT 1
    FROM "Schedule" AS SC1
    JOIN "Stop" AS S1 ON SC1.StopID = S1.StopID
    WHERE SC1.LineID = L.LineID AND S1.Name = 'C'
)
GROUP BY DS."StopName", SC.LineID, L.LineNumber;







WITH ROUTEA AS (
    SELECT RS.RouteID
    FROM "RouteStops" AS RS
    WHERE RS.StopID = (SELECT StopID FROM "Stop" WHERE Name = 'A')
),
ROUTEB AS (
    SELECT RS.RouteID
    FROM "RouteStops" AS RS
    WHERE RS.StopID = (SELECT StopID FROM "Stop" WHERE Name = 'C')
)
SELECT "Stop".Name AS "StopName", COUNT("Stop".Name) AS "StopCount"
FROM "RouteStops" AS RS
JOIN "Stop" ON RS.StopID = "Stop".StopID
WHERE RS.RouteID IN (SELECT RouteID FROM ROUTEA)
OR RS.RouteID IN (SELECT RouteID FROM ROUTEB)
GROUP BY "Stop".Name
HAVING COUNT("Stop".Name) > 1;




-- Sumaryczna kwota wydana przez użytkownika na bilety w danym roku
SELECT SUM(T.Price) AS TotalAmountSpent
FROM "Journey" AS J
JOIN "Ticket" AS T ON J.TicketID = T.TicketID
JOIN "Schedule" AS S ON J.ScheduleID = S.ScheduleID
WHERE J.UserID = 1
AND EXTRACT(YEAR FROM S.DepartureTime) = 2022;

-- Liczba pojazdów danego przewoźnika z podziałem na typ pojazdu

SELECT C.Name AS CarrierName, VT.Name AS VehicleTypeName, COUNT(V.VehicleID) AS VehicleCount
FROM "Carriers" AS C
INNER JOIN "CarrierVehicle" AS CV ON C.CarrierID = CV.CarrierID
INNER JOIN "Vehicle" AS V ON CV.VehicleID = V.VehicleID
INNER JOIN "VehicleType" AS VT ON V.VehicleTypeID = VT.VehicleTypeID
GROUP BY C.Name, VT.Name
ORDER BY C.Name, VT.Name;



-- Najczęściej wybierana linia przez użytkownika

SELECT j.UserID, EXTRACT(YEAR FROM s.DepartureTime) AS Year,
       l.LineID, l.LineNumber, COUNT(*) AS NumberOfTrips
FROM "Journey" j
JOIN "Schedule" s ON j.ScheduleID = s.ScheduleID
JOIN "Line" l ON s.LineID = l.LineID
WHERE EXTRACT(YEAR FROM s.DepartureTime) = 2022
AND j.UserID = 1
GROUP BY EXTRACT(YEAR FROM s.DepartureTime), l.LineID,j.UserID, l.LineNumber;

-- Średnia liczba przebytych przystanków w podróżach

SELECT AVG(StopCount) AS AvgStopsPerJourney
FROM (
    SELECT J.JourneyID, COUNT(RS.StopID) AS StopCount
    FROM "Journey" AS J
    JOIN "Schedule" AS S ON J.ScheduleID = S.ScheduleID
    JOIN "RouteStops" AS RS ON S.LineID = RS.RouteID
    WHERE EXTRACT(YEAR FROM S.DepartureTime) = 2023
    GROUP BY J.JourneyID
) AS StopsPerJourney;
