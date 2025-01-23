import mysql.connector
from config import MYSQL_CONFIG

db_connection = mysql.connector.connect(**MYSQL_CONFIG)
cursor = db_connection.cursor(dictionary=True)

def fetch_suppliers():
    """
    Fetch all suppliers from the database.
    """
    try:
        query = "SELECT * FROM Suppliers"
        cursor.execute(query)
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error fetching suppliers: {err}")
        return []

def fetch_products():
    """
    Fetch all products from the database, including supplier information.
    """
    try:
        query = """
            SELECT Products.ID, Products.name, Products.brand, Products.price, Products.category, 
                   Products.description, Suppliers.name AS supplier_name 
            FROM Products
            INNER JOIN Suppliers ON Products.supplier_ID = Suppliers.ID
        """
        cursor.execute(query)
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error fetching products: {err}")
        return []

def insert_supplier(name, contact_info, categories):
    """
    Insert a new supplier into the database.
    """
    try:
        query = """
            INSERT INTO Suppliers (name, contact_info, categories) 
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (name, contact_info, categories))
        db_connection.commit()
        return f"Supplier '{name}' added successfully."
    except mysql.connector.Error as err:
        print(f"Error inserting supplier: {err}")
        db_connection.rollback()
        return f"Failed to add supplier '{name}'."

def insert_product(name, brand, price, category, description, supplier_id):
    """
    Insert a new product into the database.
    """
    try:
        query = """
            INSERT INTO Products (name, brand, price, category, description, supplier_ID) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (name, brand, price, category, description, supplier_id))
        db_connection.commit()
        return f"Product '{name}' added successfully."
    except mysql.connector.Error as err:
        print(f"Error inserting product: {err}")
        db_connection.rollback()
        return f"Failed to add product '{name}'."

def close_connection():
    """
    Close the cursor and the database connection.
    """
    try:
        cursor.close()
        db_connection.close()
    except mysql.connector.Error as err:
        print(f"Error closing database connection: {err}")
