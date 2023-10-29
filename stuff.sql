-- Tabela PojazdUdogodnienie
CREATE TABLE PojazdUdogodnienie (
    PojazdUdogodnienieID INT PRIMARY KEY,
    PojazdID INT,
    UdogodnienieID INT
);

-- Tabela PrzewoznikPojazd
CREATE TABLE PrzewoznikPojazd (
    PrzewoznikPojazdID INT PRIMARY KEY,
    PrzewoznikID INT,
    PojazdID INT
);

-- Tabela Przewoznicy
CREATE TABLE Przewoznicy (
    PrzewoznikID INT PRIMARY KEY,
    Nazwa VARCHAR(255)
);

-- Tabela Linia
CREATE TABLE Linia (
    LiniaID INT PRIMARY KEY,
    NumerLinii INT
);

-- Tabela Uzytkownik
CREATE TABLE Uzytkownik (
    UserID INT PRIMARY KEY,
    Username VARCHAR(255),
    Password VARCHAR(255),
    Email VARCHAR(255),
    UserType VARCHAR(255),
    CreatedAt TIMESTAMP
);

-- Tabela RozkladJazdy
CREATE TABLE RozkladJazdy (
    RozkladID INT PRIMARY KEY,
    LiniaID INT,
    PrzystanekID INT,
    GodzinaOdjazdu TIMESTAMP,
    GodzinaPrzyjazdu TIMESTAMP
);

-- Tabela Przystanek
CREATE TABLE Przystanek (
    PrzystanekID INT PRIMARY KEY,
    Nazwa VARCHAR(255),
    TrasaID INT
);

-- Tabela Pojazd
CREATE TABLE Pojazd (
    PojazdID INT PRIMARY KEY,
    NumerRejestracyjny VARCHAR(255),
    TypPojazdu VARCHAR(255)
);

-- Tabela Udogodnienia
CREATE TABLE Udogodnienia (
    UdogodnienieID INT PRIMARY KEY,
    Nazwa VARCHAR(255),
    Opis VARCHAR(255)
);

-- Tabela Podroz
CREATE TABLE Podroz (
    PodrozID INT PRIMARY KEY,
    UzytkownikID INT,
    BiletID INT,
    RozkladID INT
);

-- Tabela Kurs
CREATE TABLE Kurs (
    KursID INT PRIMARY KEY,
    NumerKursu INT
);

-- Tabela Trasa
CREATE TABLE Trasa (
    TrasaID INT PRIMARY KEY,
    Nazwa VARCHAR(255),
    Opis VARCHAR(255)
);

-- Tabela Utrudnienia
CREATE TABLE Utrudnienia (
    UtrudnienieID INT PRIMARY KEY,
    Opis VARCHAR(255)
);

-- Tabela Bilet
CREATE TABLE Bilet (
    BiletID INT PRIMARY KEY,
    Cena DECIMAL(8, 2),
    LiniaID INT
);

-- Tabela Przesiadka
CREATE TABLE Przesiadka (
    PrzesiadkaID INT PRIMARY KEY,
    TrasaID INT,
    PrzystanekID INT,
    LiniaID INT,
    PodrozID INT
);

-- Tabela TrasyLinii
CREATE TABLE TrasyLinii (
    TrasaLiniiID INT PRIMARY KEY,
    TrasaID INT,
    LiniaID INT
);

-- Tabela PrzystankiTrasy
CREATE TABLE PrzystankiTrasy (
    PrzystanekTrasyID INT PRIMARY KEY,
    PrzystanekID INT,
    TrasaID INT
);

-- Tabela UtrudnieniaTrasy
CREATE TABLE UtrudnieniaTrasy (
    UtrudnienieTrasyID INT PRIMARY KEY,
    UtrudnienieID INT,
    TrasaID INT
);

-- Definicje kluczy obcych
ALTER TABLE Przesiadka
ADD FOREIGN KEY (TrasaID) REFERENCES Trasa(TrasaID);

ALTER TABLE Przesiadka
ADD FOREIGN KEY (PrzystanekID) REFERENCES Przystanek(PrzystanekID);

ALTER TABLE Przesiadka
ADD FOREIGN KEY (LiniaID) REFERENCES Linia(LiniaID);

ALTER TABLE Przesiadka
ADD FOREIGN KEY (PodrozID) REFERENCES Podroz(PodrozID);

ALTER TABLE PojazdUdogodnienie
ADD FOREIGN KEY (PojazdID) REFERENCES Pojazd(PojazdID);

ALTER TABLE PrzewoznikPojazd
ADD FOREIGN KEY (PrzewoznikID) REFERENCES Przewoznicy(PrzewoznikID);

ALTER TABLE Przystanek
ADD FOREIGN KEY (TrasaID) REFERENCES Trasa(TrasaID);

ALTER TABLE Bilet
ADD FOREIGN KEY (LiniaID) REFERENCES Linia(LiniaID);

ALTER TABLE RozkladJazdy
ADD FOREIGN KEY (PrzystanekID) REFERENCES Przystanek(PrzystanekID);

ALTER TABLE PojazdUdogodnienie
ADD FOREIGN KEY (UdogodnienieID) REFERENCES Udogodnienia(UdogodnienieID);

ALTER TABLE PrzewoznikPojazd
ADD FOREIGN KEY (PojazdID) REFERENCES Pojazd(PojazdID);

ALTER TABLE Trasa
ADD FOREIGN KEY (TrasaID) REFERENCES Bilet(BiletID);

ALTER TABLE Podroz
ADD FOREIGN KEY (UzytkownikID) REFERENCES Uzytkownik(UserID);

ALTER TABLE Kurs
ADD FOREIGN KEY (KursID) REFERENCES Pojazd(PojazdID);

ALTER TABLE Kurs
ADD FOREIGN KEY (KursID) REFERENCES Linia(LiniaID);

ALTER TABLE RozkladJazdy
ADD FOREIGN KEY (RozkladID) REFERENCES Linia(LiniaID);

ALTER TABLE Trasa
ADD FOREIGN KEY (TrasaID) REFERENCES Linia(LiniaID);

ALTER TABLE Przystanek
ADD FOREIGN KEY (PrzystanekID) REFERENCES PrzystankiTrasy(PrzystanekID);

ALTER TABLE Trasa
ADD FOREIGN KEY (TrasaID) REFERENCES PrzystankiTrasy(TrasaID);

ALTER TABLE Linia
ADD FOREIGN KEY (LiniaID) REFERENCES TrasyLinii(LiniaID);

ALTER TABLE Trasa
ADD FOREIGN KEY (TrasaID) REFERENCES TrasyLinii(TrasaID);

ALTER TABLE Utrudnienia
ADD FOREIGN KEY (UtrudnienieID) REFERENCES UtrudnieniaTrasy(UtrudnienieID);

ALTER TABLE Trasa
ADD FOREIGN KEY (TrasaID) REFERENCES UtrudnieniaTrasy(TrasaID);
