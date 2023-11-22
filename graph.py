import matplotlib.pyplot as plt
import os
import sqlite3
from users_database import get_db
#https://matplotlib.org/stable/tutorials/index
#https://www.geeksforgeeks.org/graph-plotting-in-python-set-1/
#https://stackoverflow.com/questions/9622163/save-plot-to-image-file-instead-of-displaying-it

def fetch_sales_data():

    cursor = get_db().cursor()
    cursor.execute("SELECT SalesDate, SalesPrice FROM Sales")
    rows = cursor.fetchall()

    sales_date = []
    sales_price = []

    for row in rows:
        sales_date.append(row[0])  
        sales_price.append(row[1])  

    get_db().close()
    return sales_date, sales_price

def save_sales_graph():
    sales_date, sales_price = fetch_sales_data()

    plt.figure(figsize=(10, 6))
    plt.plot(sales_date, sales_price, marker='o', linestyle='-', color='b')
    plt.title('Sales Data')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.xticks(rotation=45)
    plt.tight_layout()

    output_folder = 'graphs'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    folder = os.path.join(output_folder, 'sales_graph.png')
    plt.savefig(folder)
    plt.close()

def fetch_order_data():
    cursor = get_db().cursor()
    cursor.execute("SELECT OrderedDate, SUM(OrderPrice) FROM Orders GROUP BY OrderedDate")
    rows = cursor.fetchall()

    order_date = []
    total_order_amount = []

    for row in rows:
        order_date.append(row[0])  
        total_order_amount.append(row[1]) 

    get_db().close()
    return order_date, total_order_amount

def save_order_graph():
    order_date, total_order_amount = fetch_order_data()

    plt.figure(figsize=(10, 6))
    plt.bar(order_date, total_order_amount, color='black')  
    plt.title('Total Order Amount per Day')
    plt.xlabel('Date')
    plt.ylabel('Total Order Amount')
    plt.xticks(rotation=45)
    plt.tight_layout()

    output_folder = 'graphs'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    folder = os.path.join(output_folder, 'order_graph.png')
    plt.savefig(folder)
    plt.close()

def fetch_material_data():
    cursor = get_db().cursor()
    cursor.execute("SELECT MaterialName, Quantity FROM Materials")
    rows = cursor.fetchall()

    material_names = []
    quantities = []

    for row in rows:
        material_names.append(row[0]) 
        quantities.append(row[1]) 

    get_db().close()
    return material_names, quantities

def save_pie_chart():
    material_names, quantities = fetch_material_data()

    plt.figure(figsize=(8, 8))
    plt.pie(quantities, labels=material_names, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  
    plt.title('Material Quantity Distribution')

    plt.tight_layout()
    

    output_folder = 'graphs'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    folder = os.path.join(output_folder, 'materials_pie_day.png')
    plt.savefig(folder)
    plt.close()


def fetch_order_data():
    cursor = get_db().cursor()
    cursor.execute("SELECT p.ProductName, CAST(RANDOM() * 2 AS INTEGER) AS OrderCount FROM Products p;")
    rows = cursor.fetchall()

    product_names = []
    order_counts = []

    for row in rows:
        product_names.append(row[0])  
        order_counts.append(row[1])  

    get_db().close()
    return product_names, order_counts

def save_products_chart():
    product_names, order_counts = fetch_order_data()

    plt.figure(figsize=(10, 6))
    plt.bar(product_names, order_counts, color='skyblue')
    plt.title('Number of Orders per Product')
    plt.xlabel('Product Name')
    plt.ylabel('Number of Orders')
    plt.xticks(rotation=45, ha='right')
    plt.ylim(0, max(order_counts) + 5)

    plt.tight_layout()

    output_folder = 'graphs'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    folder = os.path.join(output_folder, 'products_chart.png')
    plt.savefig(folder)
    plt.close()

if __name__ == '__main__':
    save_sales_graph()
    save_order_graph()
    save_pie_chart()
    save_products_chart()

