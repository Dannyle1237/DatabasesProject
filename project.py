#Quick tips(VSCode):
#To quickly uncomment( highlight lines and HOLD CTRL then press
#                       K -> U)
#To quickly comment( highlight lines and HOLD CTRL then press
#                       K -> C)

from tkinter import *
from tkinter import ttk


import csv
import sqlite3
import os

from datetime import date
from datetime import datetime

root = Tk()

root.title('Address Book')

root.geometry("600x600")


#Statement to quickly print our queries (ex: query='''SELECT * From Customer''')
def printQuery(query):
      cars_conn = sqlite3.connect('cars.db')
      c = cars_conn.cursor()
      c.execute(query)
      print("\nQuery:")
      for item in c.fetchall():
            print(str(item))
      cars_conn.close()

def addColumn(table_name, column_name, column_def):
      cars_conn = sqlite3.connect('cars.db')
      c = cars_conn.cursor()
      c.execute(" ALTER TABLE " + table_name + " ADD " + column_name + " " + column_def )
      cars_conn.commit()
      cars_conn.close()

def modifyReturned():
      cars_conn = sqlite3.connect('cars.db')
      c = cars_conn.cursor()
      c.execute('''UPDATE RENTAL 
                   SET Returned = CASE
                        WHEN PaymentDate = 'NULL' THEN 0
                        ELSE 1
                   END''')
      cars_conn.commit()
      cars_conn.close()






# For tabs
notebook = ttk.Notebook(root)
notebook.grid()

add_customer = Frame(notebook,width=600,height=600)
add_vehicle = Frame(notebook,width=600,height=600)
add_rental = Frame(notebook,width=600,height=600)

add_customer.pack(fill="both",expand=1)
add_vehicle.pack(fill="both",expand=1)
add_rental.pack(fill="both",expand=1)

notebook.add(add_customer,text="ADD Customer")
notebook.add(add_vehicle,text="ADD Vehicle")
notebook.add(add_rental,text="ADD Rental")



#Query3
def available_cars():
      ac_conn = sqlite3.connect('cars.db')
      ac_cur = ac_conn.cursor()
      ac_cur.execute( """SELECT Distinct Vehicle.VehicleID, Description, 
      Vehicle.Year,Vehicle.Type,Vehicle.Category 
      FROM Vehicle,Rental WHERE VEHICLE.Type = ? AND 
      Vehicle.Category = ? AND (( ? > Rental.ReturnDate) 
      OR (? < Rental.StartDate));""",(vehicle_type.get(),vehicle_category.get(),
      start_date.get(),end_date.get(),))
      
      query = ac_cur.fetchall()

      for rental in query:
            car_list.insert(0,rental)

     
      ac_conn.commit()
      ac_conn.close()

def make_rental():
      row = car_list.get(car_list.curselection())

      start = datetime.strptime(start_date.get(), "%Y-%m-%d").date()
      end = datetime.strptime(end_date.get(), "%Y-%m-%d").date()
      days =  (end - start).days

      
      today_date = datetime.today().strftime('%Y-%m-%d')
      
      rental_type = weekly.get()
      if rental_type == 1:
            if days % 7 != 0:
                  rental_type = 1
            else:
                  rental_type = 7
                  days = days/7
                  
      else:
            rental_type = 1

      mr_conn = sqlite3.connect('cars.db')
      mr_cur = mr_conn.cursor()

      mr_cur.execute("""SELECT Weekly,Daily FROM RATE WHERE TYPE = ? AND CATEGORY = ?""",(row[3],row[4]))
      rate_amount = mr_cur.fetchall()
   
      
      if rental_type == 7:
            amount = rate_amount[0][0]*days
      else:
            amount = rate_amount[0][1]*days
      payment_date = str(today_date) if which_payment.get() else end_date.get()
      mr_cur.execute(""" INSERT INTO Rental(CustID,VehicleID,StartDate,OrderDate,
      RentalType,Qty,ReturnDate,TotalAmount,PaymentDate,Returned) VALUES (?,?,?,?,?,?,?,?,?,?);""",(int(cust_id.get()),row[0],start_date.get(),
      today_date,rental_type,days,end_date.get(),amount,payment_date,0))

      mr_conn.commit()
      mr_conn.close()


vehicle_type = Entry(add_rental,width=1)
vehicle_type.grid(row = 0, column = 1,)
type_label = Label(add_rental, text = 'Type:').grid(row =0, column = 0)
vehicle_category = Entry(add_rental,width=1)
vehicle_category.grid(row = 0, column = 3)
category_label = Label(add_rental, text = 'Category:').grid(row =0, column = 2)
start_date = Entry(add_rental,width=10)
start_date.grid(row = 1, column = 1)
start_label = Label(add_rental, text = 'Start Date:').grid(row =1, column = 0)
end_date = Entry(add_rental,width=10)
end_date.grid(row = 1, column = 3)
end_label = Label(add_rental, text = 'Return Date Date:').grid(row =1, column = 2)
format =  Label(add_rental, text = 'Format: year-mm-dd').grid(row =1, column = 4)
Search = Button(add_rental,text="Search",command=available_cars).grid(row =2, column = 0)
car_list = Listbox(add_rental,width=50)
car_list.grid(row =3,column=0)

which_payment = IntVar()
weekly = IntVar()

check_pay = Checkbutton(add_rental,text = "Pay Now?",variable=which_payment)
check_pay.grid(row=4,column=0)
check_weekly= Checkbutton(add_rental,text = "Weekly Rate?",variable=weekly)
check_weekly.grid(row=4,column=1)

cust_id = Entry(add_rental,width=3)
cust_id.grid(row = 5, column = 1)
cust_label = Label(add_rental, text = 'CustID:').grid(row =5, column = 0)

Submit =  Button(add_rental,text="Submit",command=make_rental).grid(row =6, column = 0)

# END of query 3



# #CREATE TABLES STATEMENTS
# cars_conn = sqlite3.connect('cars.db')
# c = cars_conn.cursor()
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

# #INSERT CSV DATA
# customer_file = open('./data/CUSTOMER.csv', 'r')
# rate_file = open('./data/RATE.csv', 'r')
# rental_file = open('./data/RENTAL.csv', 'r')
# vehicle_file = open('./data/VEHICLE.csv', 'r')
# files = []
# files.append(customer_file)
# files.append(rate_file)
# files.append(rental_file)
# files.append(vehicle_file)
# for file in files:
#       data = csv.reader(file)
#       next(data)
#       if(os.path.basename(file.name) == "CUSTOMER.csv"):
#             insert_records = "INSERT INTO Customer VALUES(?, ?, ?)"
#       elif(os.path.basename(file.name) == "RATE.csv"):
#             insert_records = "INSERT INTO Rate VALUES(?, ?, ?, ?)"
#       elif(os.path.basename(file.name) == "RENTAL.csv"):
#             insert_records = "INSERT INTO Rental VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)"
#       elif(os.path.basename(file.name) == "VEHICLE.csv"):
#             insert_records = "INSERT INTO Vehicle VALUES(?, ?, ?, ?, ?)"
#       c.executemany(insert_records, data)
# cars_conn.commit()
# cars_conn.close()

#Code to print each table and check values
# printQuery('''SELECT * FROM Customer''')
# printQuery('''SELECT * FROM Rate''')
# printQuery('''SELECT * FROM Rental''')
# printQuery('''SELECT * FROM Vehicle''')
# printQuery('''SELECT COUNT(*) FROM CUSTOMER''')
# printQuery('''SELECT COUNT(*) FROM Rate''')
# printQuery('''SELECT COUNT(*) FROM Rental''')
# printQuery('''SELECT COUNT(*) FROM Vehicle''')

#Task 1 Query 1
# addColumn("RENTAL", "Returned", "int")
# modifyReturned()
# printQuery('''SELECT * FROM Rental''')

root.mainloop()
