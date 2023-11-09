import sqlite3
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from collections import OrderedDict, Counter


conn = sqlite3.connect("FloatFry.db")

UsernameData = pd.read_sql_query("SELECT username FROM Accounts ", conn)
material_data = pd.read_sql_query("SELECT MaterialName FROM Materials ", conn)
#counts the amount of specfic item
UserAmount  = pd.DataFrame(UsernameData)['Username'].count()


#list of user names being listed out
usernamelist=UsernameData.values


#empty array for data to be stored in 
test = []
for name in usernamelist:
    test.append(name)

#numpy list being printed out as a single list so it can be fed into the graphs(variable nameswill change )
a = np.array(test).ravel()


#prints amount of Usernames(testing purposes)
#print ("amount of users:", UserAmount)

#///////////////////////////////////////////////////////////////P I E/////////////////////////////C H A R T/////////////////////////////////////////////////////////////////////////////
#for loop for most ordered material
PieChart = pd.read_sql_query("SELECT MaterialName FROM Materials",conn)
MaterialNameList = material_data.values
#print (PieChart)
PieArray=[]
for name in MaterialNameList:
    PieArray.append(name)

#https://stackoverflow.com/questions/51737245/how-to-sort-a-numpy-array-by-frequency
class OrderedCounter(Counter, OrderedDict):
    pass
L = list(np.array(PieArray).ravel())
c = OrderedCounter(L)
keys = list(c)
res = sorted(c, key=lambda x: (-c[x], keys.index(x)))


#function  for pop out if the amount of elements change 
Pop_Out_List = [0.18]
for x in range (0,len(list(res))-1):
    Pop_Out_List.append(0)


PieChartPercentage = PieChart.value_counts(normalize=True) #variable for material names in percentage form 
PieChartPercentage_value = list((np.array(PieChartPercentage.values)))
#print (PieChartPercentage_value)

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#getting order price for histogram 
Histogram_Data = pd.read_sql_query("SELECT OrderPrice FROM Orders", conn)

Histogram_Data_Values = Histogram_Data.values
Histogram_Data_Values_list = list(np.array(Histogram_Data_Values).ravel())


#pie chart for most ordered material (percentage form)
def pie_chart():

    x = 5
    #to be replaced with variable responsible for ording the percentage data in a list
    pie_chart = PieChartPercentage_value #percentages
    label= res
    PopOut = Pop_Out_List
    plt.pie(pie_chart, labels= label, explode= PopOut,shadow= True)
    plt.show()

#change in orders over time
def Users_Graph():

    #dates along the XAXIS
    XAxis = [
        datetime(2023,1,1),
        datetime(2023,12,31)
    ]
    #varables for orders
    YAxis = np.array ([0,1000])
    plt.plot(XAxis,YAxis)
    
    #labels for axis
    plt.xlabel("DATES")
    plt.ylabel("ORDERS")
    plt.title("ORDERS OVER TIME")

    #Grid styling
    plt.grid(color = 'red', linestyle = '--', linewidth = 0.5)

    #(https://www.geeksforgeeks.org/matplotlib-pyplot-plot_date-function-in-python/) for formatting date

    # Changing the format of the date using dateformatter class
    format_date = matplotlib.dates.DateFormatter('%d-%m-%Y')
 
    # getting the accurate current axes using gca()
    plt.gca().xaxis.set_major_formatter(format_date)

    plt.show()

#order price histogram
def OrderPrice_Histogram():
    #https://www.geeksforgeeks.org/matplotlib-pyplot-hist-in-python/

    Histogram = Histogram_Data_Values_list

    plt.hist(Histogram, color='Green')

    plt.title("ORDER-PRICE HISTOGRAM")
    plt.xlabel("PRICE")
    plt.ylabel("# OF ORDERS")

    plt.show()

#(https://stackoverflow.com/questions/902408/how-to-use-variables-in-sql-statement-in-python)
def Real_Time_Orders(var1, var2, var3, var4, var5):#(orderID,CustomerID,OrderedDate,OrderPrice,OrderStatus=BOOL)
    
    #conncecting to database
    connection = sqlite3.connect("FloatFry.db")
    cursor = connection.cursor()

    #putting data into the system
    cursor.execute("INSERT INTO Orders (OrderID,CustomerID,OrderedDate,OrderPrice,OrderStatus) VALUES (?, ?, ?, ?, ?)", (var1, var2, var3, var4, var5))

    #committing the changes
    connection.commit()
