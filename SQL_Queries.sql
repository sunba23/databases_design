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
WHERE S1.Name = 'Pierwszy_przystanek' AND S2.Name = 'Drugi_przystanek';

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
AND EXTRACT(YEAR FROM s.DepartureTime) = 2020
AND TO_CHAR(s.DepartureTime, 'Month') = 'June';


-- Pokazanie linii do przejazdu z przystanku A do B
SELECT DISTINCT L.LineID, L.LineNumber
FROM "RouteStops" AS RS1
INNER JOIN "RouteStops" AS RS2 ON RS1.RouteID = RS2.RouteID
INNER JOIN "LineRoutes" AS LR ON RS1.RouteID = LR.RouteID
INNER JOIN "Line" AS L ON LR.LineID = L.LineID
INNER JOIN "Stop" AS S1 ON RS1.StopID = S1.StopID
INNER JOIN "Stop" AS S2 ON RS2.StopID = S2.StopID
WHERE S1.Name = 'Nazwa_pierwszego_przystanku' AND S2.Name = 'Nazwa_drugiego_przystanku';

-- Szukanie połączenia z przystanku A do B z 1 przesiadką
SELECT DISTINCT L1.LineID AS LineID1, L1.LineNumber AS LineNumber1,
                L2.LineID AS LineID2, L2.LineNumber AS LineNumber2
FROM "RouteStops" AS RS1
INNER JOIN "RouteStops" AS RS2 ON RS1.RouteID = RS2.RouteID
INNER JOIN "LineRoutes" AS LR1 ON RS1.RouteID = LR1.RouteID
INNER JOIN "Line" AS L1 ON LR1.LineID = L1.LineID
INNER JOIN "LineRoutes" AS LR2 ON RS2.RouteID = LR2.RouteID
INNER JOIN "Line" AS L2 ON LR2.LineID = L2.LineID
WHERE RS1.StopID = (SELECT StopID FROM "Stop" WHERE Name = 'Rodriguez Crescent Isle 16')
AND RS2.StopID = (SELECT StopID FROM "Stop" WHERE Name = 'Osborn Estates Camp 23')
AND L1.LineID = L2.LineID;

-- Sumaryczna kwota wydana przez użytkownika na bilety w danym roku
SELECT SUM(T.Price) AS TotalAmountSpent
FROM "Journey" AS J
JOIN "Ticket" AS T ON J.TicketID = T.TicketID
JOIN "Schedule" AS S ON J.ScheduleID = S.ScheduleID
WHERE J.UserID = 1
AND EXTRACT(YEAR FROM S.DepartureTime) = 2023;

-- Liczba pojazdów danego przewoźnika z podziałem na typ pojazdu

SELECT C.Name AS CarrierName, VT.Name AS VehicleTypeName, COUNT(V.VehicleID) AS VehicleCount
FROM "Carriers" AS C
INNER JOIN "CarrierVehicle" AS CV ON C.CarrierID = CV.CarrierID
INNER JOIN "Vehicle" AS V ON CV.VehicleID = V.VehicleID
INNER JOIN "VehicleType" AS VT ON V.VehicleTypeID = VT.VehicleTypeID
GROUP BY C.Name, VT.Name
ORDER BY C.Name, VT.Name;