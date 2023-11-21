import matplotlib.pyplot as plt
import os
import sqlite3

def fetch_sales_data():
    conn = sqlite3.connect("/Users/muhammadusman/Downloads/django/JustInTime/Floatfry.db")
    cursor = conn.cursor()
    cursor.execute("SELECT SalesDate, SalesPrice FROM Sales")
    rows = cursor.fetchall()

    sales_date = []
    sales_price = []

    for row in rows:
        sales_date.append(row[0])  # Assuming SalesDate is the fifth column after SalesID
        sales_price.append(row[1])  # Assuming SalesPrice is the sixth column in your table

    conn.close()
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

    output_path = os.path.join(output_folder, 'sales_graph.png')
    plt.savefig(output_path)
    plt.close()

if __name__ == '__main__':
    save_sales_graph()
