import sqlite3
import csv
import os

def printQuery(query):
      cars_conn = sqlite3.connect('CarRental.db')
      c = cars_conn.cursor()
      c.execute(query)
      print("\nQuery:")
      for item in c.fetchall():
            print(str(item))
      cars_conn.close()

def addColumn(table_name, column_name, column_def):
      cars_conn = sqlite3.connect('CarRental.db')
      c = cars_conn.cursor()
      c.execute(" ALTER TABLE " + table_name + " ADD " + column_name + " " + column_def )
      cars_conn.commit()
      cars_conn.close()

def modifyReturned():
      cars_conn = sqlite3.connect('CarRental.db')
      c = cars_conn.cursor()
      c.execute('''UPDATE RENTAL 
                   SET Returned = CASE
                        WHEN PaymentDate = 'NULL' THEN 0
                        ELSE 1
                   END''')
      cars_conn.commit()
      cars_conn.close()


# #CREATE TABLES STATEMENTS
cars_conn = sqlite3.connect('CarRental.db')
c = cars_conn.cursor()
c.execute(''' CREATE TABLE Customer( 
                CustID int,Name varchar(25), 
                Phone varchar(25), 
                PRIMARY KEY(CustID)); ''')
c.execute('''CREATE TABLE Vehicle( 
                VehicleID varchar(25),
                Description varchar(25), 
                Year int,
                Type int,
                Category int,
                PRIMARY KEY(VehicleID) ); ''')
c.execute('''CREATE TABLE RATE( 
                Type int,
                Category int, 
                Weekly int, 
                Daily int);''')
c.execute('''CREATE TABLE Rental(
                CustID int REFERENCES Customer (CustID) ON DELETE CASCADE,
                VehicleID varchar(25) REFERENCES Vehicle (VehicleID) ON DELETE CASCADE, 
                StartDate varchar(15),
                OrderDate varchar(15),
                RentalType int,
                Qty int,
                ReturnDate varchar(15),
                TotalAmount int,
                PaymentDate varchar(15));''')

#INSERT CSV DATA
customer_file = open('./data/CUSTOMER.csv', 'r')
rate_file = open('./data/RATE.csv', 'r')
rental_file = open('./data/RENTAL.csv', 'r')
vehicle_file = open('./data/VEHICLE.csv', 'r')
files = []
files.append(customer_file)
files.append(rate_file)
files.append(rental_file)
files.append(vehicle_file)
for file in files:
      data = csv.reader(file)
      next(data)
      if(os.path.basename(file.name) == "CUSTOMER.csv"):
            insert_records = "INSERT INTO Customer VALUES(?, ?, ?)"
      elif(os.path.basename(file.name) == "RATE.csv"):
            insert_records = "INSERT INTO Rate VALUES(?, ?, ?, ?)"
      elif(os.path.basename(file.name) == "RENTAL.csv"):
            insert_records = "INSERT INTO Rental VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)"
      elif(os.path.basename(file.name) == "VEHICLE.csv"):
            insert_records = "INSERT INTO Vehicle VALUES(?, ?, ?, ?, ?)"
      c.executemany(insert_records, data)
cars_conn.commit()
cars_conn.close()

#Code to print each table and check values
printQuery('''SELECT * FROM Customer''')
printQuery('''SELECT * FROM Rate''')
printQuery('''SELECT * FROM Rental''')
printQuery('''SELECT * FROM Vehicle''')
printQuery('''SELECT COUNT(*) FROM CUSTOMER''')
printQuery('''SELECT COUNT(*) FROM Rate''')
printQuery('''SELECT COUNT(*) FROM Rental''')
printQuery('''SELECT COUNT(*) FROM Vehicle''')

#Task 1 Query 1
addColumn("RENTAL", "Returned", "int")
modifyReturned()
printQuery('''SELECT * FROM Rental''')

cars_conn = sqlite3.connect('CarRental.db')
c = cars_conn.cursor()
vRentalInfo=''' CREATE VIEW vRentalInfo AS 
      SELECT 
      OrderDate,
      StartDate,
      ReturnDate,
      RentalType * qty AS TotalDays,
      V.VehicleID AS VIN,
      V.Description as Vehicle,
      CASE
      WHEN V.Type=1 THEN 'Compact'
      WHEN V.Type=2 THEN 'Medium'
      WHEN V.Type=3 THEN 'Large'
      WHEN V.Type=4 THEN 'SUV'
      WHEN V.Type=5 THEN 'Truck'
      WHEN V.Type=6 THEN 'VAN'
      END AS Type,
      CASE
      WHEN V.Category=0 THEN 'Basic'
      WHEN V.Category=1 THEN 'Luxury'
      END AS Category,
      C.CustID AS CustomerID,
      Name AS CustomerName,
      TotalAmount AS OrderAmount,
      CASE 
      WHEN PaymentDate='NULL' THEN TotalAmount
      WHEN PaymentDate!='NULL' THEN 0
      END AS RentalBalance
      FROM Rental,VEHICLE AS V, CUSTOMER AS C
      WHERE C.CustID=Rental.CustID 
      AND V.VehicleID=Rental.VehicleID
      ORDER BY StartDate ASC'''
c.execute(vRentalInfo)
cars_conn.commit()
cars_conn.close()