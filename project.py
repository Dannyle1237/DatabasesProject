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
import locale

root = Tk()

root.title('Address Book')

root.geometry("800x600")


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

add_customer = Frame(notebook,width=800,height=600)
add_vehicle = Frame(notebook,width=800,height=600)
add_rental = Frame(notebook,width=800,height=600)
return_rental = Frame(notebook,width=800,height=600)
search_customer = Frame(notebook,width=800,height=600)

add_customer.pack(fill="both",expand=1)
add_vehicle.pack(fill="both",expand=1)
add_rental.pack(fill="both",expand=1)
return_rental.pack(fill="both",expand=1)
search_customer.pack(fill="both",expand=1)

notebook.add(add_customer,text="ADD Customer")
notebook.add(add_vehicle,text="ADD Vehicle")
notebook.add(add_rental,text="ADD Rental")
notebook.add(return_rental,text="Return Rental")
notebook.add(search_customer,text="Search Customer")


#Requirment 1
def add_newcustomer():
      cu_conn = sqlite3.connect('cars.db')
      cu_cur = cu_conn.cursor()
      cu_cur.execute( """INSERT INTO CUSTOMER (Name,Phone)
      VALUES(?,?)""",(Customer_name.get(),Customer_phone.get()))

      cu_conn.commit()
      cu_conn.close()


Customer_name = Entry(add_customer,width=20)
Customer_name.grid(row = 0, column = 1,)
type_label1 = Label(add_customer, text = 'Name:').grid(row =0, column = 0)
Customer_phone = Entry(add_customer,width=20)
Customer_phone.grid(row = 3, column = 1,)
type_label1 = Label(add_customer, text = 'phone:').grid(row =3, column = 0)
Submit =  Button(add_customer,text="Submit",command=add_newcustomer).grid(row =6, column = 0)


#Requirment 3
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

# END of requirement 3

#Requiement 4
def pay_rental(amount):
      ga_conn = sqlite3.connect('cars.db')
      ga_cur = ga_conn.cursor()
      ga_cur.execute("""UPDATE Rental SET returned = 1 WHERE CustID = ?
      AND VehicleID = ? AND ReturnDate = ?; """,(amount[0][1],amount[0][2],return_date.get()))
      finshed_label = Label(return_rental,text="Finished Paying ")
      finshed_label.grid(row=5,column=0)
      ga_conn.commit()
      ga_conn.close()

def get_amount():
      ga_conn = sqlite3.connect('cars.db')
      ga_cur = ga_conn.cursor()
      
      ga_cur.execute("""SELECT TotalAmount,Rental.CustID,VehicleID FROM Rental WHERE Rental.CustID = (Select 
      Customer.CustID FROM Customer Where Customer.Name = ?) AND Rental.VehicleID = (
            SELECT Vehicle.VehicleID FROM Vehicle WHERE Description = ? AND Year = ?) AND ReturnDate = ?
            AND Returned != 1; """
            ,(cust_name.get(),veh_description.get(),int(veh_year.get()),return_date.get()))

      amount = ga_cur.fetchall()
      print(amount)
      amount_label = Label(return_rental,text="Amount =" +str(amount[0][0]) )
      amount_label.grid(row=3,column=0)
      Button(return_rental,text="Pay",command=lambda: pay_rental(amount)).grid(row=4, column = 0)
      ga_conn.commit()
      ga_conn.close()

     
      
      


return_date = Entry(return_rental,width=10)
return_date.grid(row = 0, column = 1,)
rd_label = Label(return_rental, text = 'Return Date:').grid(row =0, column = 0)
cust_name = Entry(return_rental,width=10)
cust_name.grid(row = 0, column = 3)
name_label = Label(return_rental, text = 'Name:').grid(row =0, column = 2)
veh_description = Entry(return_rental,width=10)
veh_description.grid(row = 1, column = 1)
vd_label = Label(return_rental, text = 'Vehicle Type:').grid(row =1, column = 0)
veh_year = Entry(return_rental,width=4)
veh_year.grid(row = 1, column =4)
year_label = Label(return_rental, text = 'Vehicle Year:').grid(row =1, column = 3)
search =  Button(return_rental,text="Search",command=get_amount).grid(row =2, column = 0)

#End of Requirement 4

#Requirement 5a


amount_labels_arr = []

def destroy_labels():
      global amount_labels_arr
      for label in amount_labels_arr:
                  label.grid_forget()
                  label.destroy()
                  

def find_customer():
      locale.setlocale(locale.LC_ALL, '')
      fc_conn = sqlite3.connect('cars.db')
      fc_cur = fc_conn.cursor()

      try:
            fc_cur.execute("""DROP View vRentalInfo;""")
      except:
            pass
      query2()
     
      try:
            destroy_labels()
      except:
            pass

      percent = "%"
      like_name = percent +name_search.get() + percent
      id_val = None
      fc_cur.execute("""SELECT CustomerID, CustomerName, RentalBalance FROM vRentalInfo Where CustomerID=? OR CustomerName LIKE ? ORDER BY RentalBalance DESC;""",
      (id_val,like_name))

      customerBalance = fc_cur.fetchall()
      row_count = 2
      
      global amount_labels_arr
      for i in customerBalance:
            if i[2] == None:
                 amount_label = Label(search_customer,text ="$0.00")
                 amount_label.grid(row=row_count,column=0)
                 amount_labels_arr.append(amount_label)
            else:
                  query_str = str(i[0]) + " " + i[1] + " " + str(locale.currency(i[2], grouping=True))
                  amount_label = Label(search_customer,text = query_str )
                  amount_label.grid(row=row_count,column=0)
                  amount_labels_arr.append(amount_label)
            row_count+=1
      fc_conn.commit()
      fc_conn.close()
      
name_search = Entry(search_customer,width=15)
name_search.grid(row = 0, column = 1,)
search_name_label = Label(search_customer, text = 'Name:').grid(row =0, column = 0)
id_search = Entry(search_customer,width=3)
id_search.grid(row = 0, column = 3)
id_search_label = Label(search_customer, text = 'ID:').grid(row =0, column = 2)
search_customer_button =  Button(search_customer,text="Search",command=find_customer).grid(row =1, column = 0)

#End of Requirement 5a

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

#query 2

def query2():
      cars_conn = sqlite3.connect('cars.db')
      c = cars_conn.cursor()
      vRentalInfo=''' CREATE VIEW vRentalInfo AS 
      SELECT 
      OrderDate,
      StartDate,
      ReturnDate,
      RentalType * qty AS TotalDays,
      V.VehicleID AS VIN,
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

#end of query 2

root.mainloop()
