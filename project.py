#Quick tips(VSCode):
#To quickly uncomment( highlight lines and HOLD CTRL then press
#                       K -> U)
#To quickly comment( highlight lines and HOLD CTRL then press
#                       K -> C)

from tkinter import *

import csv
import sqlite3
import os 

root = Tk()

root.title('Address Book')

root.geometry("600x600")

#Statement to quickly print our queries (ex: query='''SELECT * From Customer''')
def printQuery(query):
      cars_conn = sqlite3.connect('cars.db')
      c = cars_conn.cursor()
      c.execute(query)
      print("\nQuery:\n" + str(c.fetchall()))
      cars_conn.close()

cars_conn = sqlite3.connect('cars.db')
c = cars_conn.cursor()
#CREATE TABLES STATEMENTS
# c.execute(''' CREATE TABLE Customer( 
#                 CustID int,Name varchar(25), 
#                 Phone varchar(25), 
#                 PRIMARY KEY(CustID)); ''')
# c.execute('''CREATE TABLE Vehicle( 
#                 VehicleID varchar(25),
#                 Description varchar(25), 
#                 Year int,
#                 Type int,
#                 Category int,
#                 PRIMARY KEY(VehicleID) ); ''')
# c.execute('''CREATE TABLE RATE( 
#                 Type int,
#                 Category int, 
#                 Weekly int, 
#                 Daily int);''')
# c.execute('''CREATE TABLE Rental(
#                 CustID int REFERENCES Customer (CustID) ON DELETE CASCADE,
#                 VehicleID varchar(25) REFERENCES Vehicle (VehicleID) ON DELETE CASCADE, 
#                 StartDate varchar(15),
#                 OrderDate varchar(15),
#                 RentalType int,
#                 Qty int,
#                 ReturnDate varchar(15),
#                 TotalAmount int,
#                 PaymentDate varchar(15));''')

#INSERT CSV DATA
# customer_file = open('./data/CUSTOMER.csv')
# rate_file = open('./data/RATE.csv')
# rental_file = open('./data/RENTAL.csv')
# vehicle_file = open('./data/VEHICLE.csv')
# files = []
# files.append(customer_file)
# files.append(rate_file)
# files.append(rental_file)
# files.append(vehicle_file)
# for file in files:
#       data = csv.reader(file)
#       if(os.path.basename(file.name) == "CUSTOMER.csv"):
#             insert_records = "INSERT INTO Customer VALUES(?, ?, ?)"
#       elif(os.path.basename(file.name) == "RATE.csv"):
#             insert_records = "INSERT INTO Rate VALUES(?, ?, ?, ?)"
#       elif(os.path.basename(file.name) == "RENTAL.csv"):
#             insert_records = "INSERT INTO Rental VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)"
#       elif(os.path.basename(file.name) == "VEHICLE.csv"):
#             insert_records = "INSERT INTO Vehicle VALUES(?, ?, ?, ?, ?)"
#       c.executemany(insert_records, data)
      
printQuery('''SELECT * FROM Customer''')
printQuery('''SELECT * FROM Rate''')
printQuery('''SELECT * FROM Rental''')
printQuery('''SELECT * FROM Vehicle''')

cars_conn.commit()
cars_conn.close()

#executes tinker components
root.mainloop()
