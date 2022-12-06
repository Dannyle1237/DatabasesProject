from tkinter import *
from tkinter import ttk

import sqlite3

import random
import string
from datetime import datetime
import locale

root = Tk()

root.title('Address Book')

root.geometry("800x600")

#Hashmaps for type and category
type_hmap ={
      "Compact" : 1,
      "Medium" : 2,
      "Large" : 3,
      "SUV" : 4,
      "Truck" : 5,
      "VAN" : 6
}
category_hmap = {
      "Basic" : 0,
      "Luxury" : 1
}
#options for type and category, mainly for dropdown lists
type_options ={
      "Compact",
      "Medium",
      "Large",
      "SUV",
      "Truck",
      "VAN"
}
category_options ={
      "Basic",
      "Luxury"
}


# For tabs
notebook = ttk.Notebook(root)
notebook.grid()

add_customer = Frame(notebook,width=800,height=600)
add_vehicle = Frame(notebook,width=800,height=600)
add_rental = Frame(notebook,width=800,height=600)
return_rental = Frame(notebook,width=800,height=600)
search_customer = Frame(notebook,width=800,height=600)
search_vehicle = Frame(notebook, width=800,height=600)

add_customer.pack(fill="both",expand=1)
add_vehicle.pack(fill="both",expand=1)
add_rental.pack(fill="both",expand=1)
return_rental.pack(fill="both",expand=1)
search_customer.pack(fill="both",expand=1)
search_vehicle.pack(fill="both",expand=1)

notebook.add(add_customer,text="ADD Customer")
notebook.add(add_vehicle,text="ADD Vehicle")
notebook.add(add_rental,text="ADD Rental")
notebook.add(return_rental,text="Return Rental")
notebook.add(search_customer,text="Search Customer")
notebook.add(search_vehicle,text="Search Vehicle")


#Requirment 1
def add_newcustomer():
      cu_conn = sqlite3.connect('CarRental.db')
      cu_cur = cu_conn.cursor()
    
      cu_cur.execute( """INSERT INTO CUSTOMER (Name,Phone,CustID)
      VALUES(?,?,(SELECT MAX(CustID)
      FROM CUSTOMER)+1)""",(Customer_name.get(),Customer_phone.get()))

      cu_conn.commit()
      cu_conn.close()


Customer_name = Entry(add_customer,width=20)
Customer_name.grid(row = 0, column = 1,)
type_label1 = Label(add_customer, text = 'Name:').grid(row =0, column = 0)
Customer_phone = Entry(add_customer,width=20)
Customer_phone.grid(row = 3, column = 1,)
type_label1 = Label(add_customer, text = 'phone:').grid(row =3, column = 0)
Submit =  Button(add_customer,text="Submit",command=add_newcustomer).grid(row =6, column = 0)

#Requirement 2
def insert_vehicle():
      if(len(str(vehicle_year.get()))!= 4):
            print("Cannot submit: Invalid Year")
            return False
      cars_conn = sqlite3.connect('CarRental.db')
      cars_cur = cars_conn.cursor()

      #Generate 17 digit code not in DB already
      cars_cur.execute('''SELECT VehicleID FROM Vehicle''')
      curr_vIDs = cars_cur.fetchall()
      vID = ''.join(random.choices(string.ascii_uppercase + string.digits, k=17))
      while(curr_vIDs.count(vID) != 0):
            vID = ''.join(random.choices(string.ascii_uppercase + string.digits, k=17))

      cars_cur.execute(''' INSERT INTO VEHICLE
      VALUES(?,?,?,?,?)''',(vID, vehicle_description.get(), vehicle_year.get(), type_hmap[type_selected.get()], category_hmap[category_selected.get()]))
      cars_conn.commit()
      cars_conn.close()
#GUI 
title = Label(add_vehicle, text="Add Vehicle Information").grid(row=0, column=5)
vehicle_description = Entry(add_vehicle, width=10, justify="left")
vehicle_description.grid(sticky=W, row = 1, column = 1)
description_label = Label(add_vehicle, text = 'Enter Description:', justify="left").grid(sticky = W, row =1, column = 0)
vehicle_year = Entry(add_vehicle, width=4, justify="left")
vehicle_year.grid(sticky=W, row = 2, column = 1)
year_label = Label(add_vehicle, text = 'Enter Year:', justify="left").grid(sticky = W, row =2, column = 0)

type_selected = StringVar()
type_selected.set("Compact")
type_dropdown_menu = OptionMenu(add_vehicle, type_selected, *type_options)
type_label = Label(add_vehicle, text='Select Type:', justify="left").grid(sticky = W, row=3, column=0)
type_dropdown_menu.grid(sticky=W, row=3, column=1)
category_selected = StringVar()

category_selected.set("Basic")
category_dropdown_menu = OptionMenu(add_vehicle, category_selected, *category_options)
category_label = Label(add_vehicle, text='Select Category:', justify="left").grid(sticky=W, row=4, column=0)
category_dropdown_menu.grid(row=4, column=1)

vehicle_submit = Button(add_vehicle,text="Submit",command=(insert_vehicle))
vehicle_submit.grid(row =5, column = 5)

#Requirement 3
def available_cars():
      ac_conn = sqlite3.connect('CarRental.db')
      ac_cur = ac_conn.cursor()
      ac_cur.execute( """SELECT Distinct Vehicle.VehicleID, Description, 
      Vehicle.Year,Vehicle.Type,Vehicle.Category 
      FROM Vehicle,Rental WHERE VEHICLE.Type = ? AND 
      Vehicle.Category = ? AND (( ? > Rental.ReturnDate) 
      OR (? < Rental.StartDate));""",( type_hmap[rental_type_selected.get()],category_hmap[rental_category_selected.get()],
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

      mr_conn = sqlite3.connect('CarRental.db')
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

rental_type_selected = StringVar()
rental_type_selected.set("Compact")
vehicle_type = OptionMenu(add_rental, rental_type_selected, *type_options)
vehicle_type.grid(sticky=W, row = 0, column = 1)
type_label = Label(add_rental, text = 'Type:', justify="right").grid(sticky=W, row =0, column = 0)

rental_category_selected = StringVar()
rental_category_selected.set("Basic")
vehicle_category = OptionMenu(add_rental, rental_category_selected, *category_options)
vehicle_category.grid(sticky=W, row = 0, column = 3)
category_label = Label(add_rental, text = 'Category:', justify="right").grid(sticky=W, row =0, column = 2)

start_date = Entry(add_rental,width=10, justify="left")
start_date.grid(sticky=W, row = 1, column = 1)
start_label = Label(add_rental, text = 'Start Date:', justify="left").grid(sticky=W, row =1, column = 0)
end_date = Entry(add_rental,width=10, justify="left")
end_date.grid(row = 1, column = 3)
end_label = Label(add_rental, text = 'Return Date:', justify="left").grid(sticky=W, row =1, column = 2)
format =  Label(add_rental, text = 'Format: year-mm-dd').grid(row =1, column = 4)
Search = Button(add_rental,text="Search",command=available_cars).grid(row =2, column = 1)
car_list = Listbox(add_rental,width=50)
car_list.grid(row =3,column=0, columnspan=3)

which_payment = IntVar()
weekly = IntVar()

check_pay = Checkbutton(add_rental,text = "Pay Now?",variable=which_payment)
check_pay.grid(row=4,column=0)
check_weekly= Checkbutton(add_rental,text = "Weekly Rate?",variable=weekly)
check_weekly.grid(row=4,column=1)

cust_id = Entry(add_rental,width=10, justify="left")
cust_id.grid(sticky=W, row = 5, column = 1)
cust_label = Label(add_rental, text = 'CustID:', justify="left").grid(sticky=W, row =5, column = 0)

Submit =  Button(add_rental,text="Submit",command=make_rental, justify="center").grid(row =6, column = 0, columnspan=3)

# END of requirement 3

#Requiement 4
def pay_rental(amount):
      ga_conn = sqlite3.connect('CarRental.db')
      ga_cur = ga_conn.cursor()
      ga_cur.execute("""UPDATE Rental SET returned = 1 WHERE CustID = ?
      AND VehicleID = ? AND ReturnDate = ?; """,(amount[0][1],amount[0][2],return_date.get()))
      finshed_label = Label(return_rental,text="Finished Paying ")
      finshed_label.grid(row=5,column=0)
      ga_conn.commit()
      ga_conn.close()

def get_amount():
      ga_conn = sqlite3.connect('CarRental.db')
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
rd_label = Label(return_rental, text = 'Return Date:', justify="left").grid(sticky=W, row =0, column = 0)

cust_name = Entry(return_rental,width=10)
cust_name.grid(sticky=W, row = 0, column = 3)
name_label = Label(return_rental, text = 'Name:').grid(sticky=W,row =0, column = 2)

veh_description = Entry(return_rental,width=10)
veh_description.grid(row = 1, column = 1)
vd_label = Label(return_rental, text = 'Vehicle Type:', justify="left").grid(sticky=W,row =1, column = 0)

veh_year = Entry(return_rental,width=6)
veh_year.grid(sticky=W, row = 1, column =3)
year_label = Label(return_rental, text = 'Vehicle Year:', justify="left").grid(sticky=W, row =1, column = 2)
search =  Button(return_rental,text="Search",command=get_amount, justify="center").grid(sticky=W,row =2, column = 0)

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
      fc_conn = sqlite3.connect('CarRental.db')
      fc_cur = fc_conn.cursor()

      try:
            fc_cur.execute("""DROP View vRentalInfo;""")
      except:
            pass
      query2()
     
      # try:
      #       destroy_labels()
      # except:
      #       pass

      percent = "%"
      if name_search.get() == "":
            like_name = None
      else:
            like_name = percent +name_search.get() + percent
      
      try:
            id_val = int(id_search.get())
      except:
            id_val = None
      
      if like_name == None and id_val == None:
            like_name = "%%"
      fc_cur.execute("""SELECT CustomerID, CustomerName, RentalBalance FROM vRentalInfo Where CustomerID=? OR CustomerName LIKE ? ORDER BY RentalBalance DESC;""",
      (id_val,like_name))

      customers_searched = fc_cur.fetchall()
      print(customers_searched)
      cust_search_list = ttk.Treeview(search_customer, column=("c1", "c2", "c3"), show='headings', height=20)
      cust_search_list.column("# 1", anchor=W)
      cust_search_list.heading("# 1", text="CustID")
      cust_search_list.column("# 2", anchor=W)
      cust_search_list.heading("# 2", text="Name")
      cust_search_list.column("# 3", anchor=W)
      cust_search_list.heading("# 3", text="Rental Balance")
      count = 1
      
      for i in customers_searched:
            if i[2] == None:
                 cust_search_list.insert('', 'end', text=str(count), values=(str(i[0]), str(i[1]), "$0.00"))
            else:
                  cust_search_list.insert('', 'end', text=str(count), values=(str(i[0]), str(i[1]), "$" + str(i[2])))
            count+=1
      cust_search_list.grid(row=2, column=0, columnspan = 3)
      fc_conn.commit()
      fc_conn.close()

search_name_label = Label(search_customer, text = 'Name:', justify="left").grid(sticky = W, row =0, column = 0)
name_search = Entry(search_customer,width=15, justify="left")
name_search.grid(sticky = W, row = 0, column = 1)

id_search_label = Label(search_customer, text = 'ID:', justify="left").grid(sticky=W, row =1, column = 0)
id_search = Entry(search_customer,width=10, justify="left")
id_search.grid(sticky = W, row = 1, column = 1)

search_customer_button =  Button(search_customer,text="Search",command=find_customer).grid(row =1, column = 2)

#End of Requirement 5a

#Requirement 5b
def search_vehicles():
      locale.setlocale(locale.LC_ALL, '')
      fv_conn = sqlite3.connect('CarRental.db')
      fv_cur = fv_conn.cursor()

      try:
            fv_cur.execute("""DROP View vRentalInfo;""")
      except:
            pass
      query2()

      percent = "%"
      if description_search.get() == "":
            like_desc = None
      else:
            like_desc = percent +description_search.get() + percent
      
      if vin_search.get() == "":
            vin_val = None
      else:
            vin_val = vin_search.get()
      
      if like_desc == None and vin_val == None:
            like_desc = "%%"
      fv_cur.execute("""SELECT VIN, Vehicle,
      (SELECT ROUND(SUM(Averages)/Count(Averages), 2) FROM 
      (SELECT (CAST(R.TotalAmount as REAL)/(R.Qty*R.RentalType)) as Averages FROM Rental as R WHERE R.VehicleID=VR.VIN)) as Average
      FROM vRentalInfo as VR Where VIN=? OR Vehicle LIKE ?;""",
      (vin_val,like_desc))

      vehicles_searched = fv_cur.fetchall()
      #print(vehicles_searched)
      vehicle_search_list = ttk.Treeview(search_vehicle, column=("c1", "c2", "c3"), show='headings', height=20)
      vehicle_search_list.column("# 1", anchor=W)
      vehicle_search_list.heading("# 1", text="VIN")
      vehicle_search_list.column("# 2", anchor=W)
      vehicle_search_list.heading("# 2", text="Description")
      vehicle_search_list.column("# 3", anchor=W)
      vehicle_search_list.heading("# 3", text="Daily")
      
      count = 1
      for vehicle in vehicles_searched:
            vehicle_search_list.insert('', 'end', text=str(count), values=(str(vehicle[0]), str(vehicle[1]), "$" + str(vehicle[2])))
            count += 1
      vehicle_search_list.grid(row=3, column=0, columnspan=5)
      fv_conn.commit()
      fv_conn.close()

vehicle_search_title = Label(search_vehicle, text="Search Vehicle", justify="center").grid(row=0, column=0)

vin_search_label = Label(search_vehicle, text="Vin", justify="left").grid(sticky=W, row=1, column=0)
vin_search = Entry(search_vehicle, width=20)
vin_search.grid(row=1, column=1)

description_search_label = Label(search_vehicle, text="Description", justify="left").grid(sticky=W,row=2, column=0)
description_search = Entry(search_vehicle, width=20)
description_search.grid(row=2, column=1)

submit_vehicle_search = Button(search_vehicle, text="Search", command=search_vehicles, justify="left").grid(sticky=W,row= 2, column=2)

#query 2
def query2():
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
      cars_conn.commit()
      c.execute(vRentalInfo)
      cars_conn.close()

#end of query 2

root.mainloop()
