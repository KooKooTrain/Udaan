-- ================================================
-- UDAAN - AIRPORT MANAGEMENT SYSTEM
-- This is to create SQL Table if it doesnt exist
-- ================================================

CREATE DATABASE IF NOT EXISTS udaan;
USE udaan;


-- ================== ADMIN TABLE ==================
CREATE TABLE IF NOT EXISTS Admin (
    AdminID   INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName  VARCHAR(50),
    Email     VARCHAR(100),
    Phone     VARCHAR(15)
);


-- ================== EMPLOYEES TABLE ==================
CREATE TABLE IF NOT EXISTS Employees (
    EmpID     INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName  VARCHAR(50),
    Role      VARCHAR(50),
    Email     VARCHAR(100),
    Phone     VARCHAR(15)
);


-- ================== PASSENGERS TABLE ==================
CREATE TABLE IF NOT EXISTS Passengers (
    PID         INT PRIMARY KEY,
    FirstName   VARCHAR(50),
    LastName    VARCHAR(50),
    Age         INT,
    Gender      VARCHAR(10),
    Nationality VARCHAR(50),
    PhoneNumber BIGINT,
    PassportNo  VARCHAR(20),
    password    VARCHAR(50)
);


-- ================== FLIGHTS TABLE ==================
CREATE TABLE IF NOT EXISTS Flights (
    FlightID  VARCHAR(10) PRIMARY KEY,
    Airline   VARCHAR(50),
    Departure VARCHAR(50),
    Arrival   VARCHAR(50),
    DD        VARCHAR(20),
    DT        VARCHAR(10),
    Gate      VARCHAR(5)
);


-- ================== TICKETS TABLE ==================
CREATE TABLE IF NOT EXISTS Tickets (
    TicketID    INT PRIMARY KEY,
    PassengerID INT,
    FlightID    VARCHAR(10),
    Seat        VARCHAR(5),
    Class       VARCHAR(20),
    Price       INT,
    FOREIGN KEY (PassengerID) REFERENCES Passengers(PID),
    FOREIGN KEY (FlightID)    REFERENCES Flights(FlightID)
);


-- ================== SAMPLE DATA ==================

-- Sample flights
INSERT IGNORE INTO Flights VALUES ('AI101', 'Air India', 'Mumbai', 'Delhi', '2026-12-01', '10:00', 'B4');
INSERT IGNORE INTO Flights VALUES ('6E202', 'IndiGo', 'Bangalore', 'Hyderabad', '2026-12-05', '14:30', 'A2');


-- Sample passenger
-- User ID: 101   Password: test123
INSERT IGNORE INTO Passengers VALUES (101, 'Test', 'Jungkook', 20, 'Male', 'Indian', 9999999999, 'P1234567', 'test123');
