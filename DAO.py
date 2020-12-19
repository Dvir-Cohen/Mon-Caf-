from DTO import *
import sqlite3


# Data Access Objects:

class _Employees:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, Employee):
        self._conn.execute("INSERT INTO Employees (id, name, salary, coffee_stand) VALUES (?, ?, ?, ?)",
                           [Employee.id, Employee.name, Employee.salary, Employee.coffee_stand])

    def find(self, Employee_id):
        c = self._conn.cursor()
        c.execute("SELECT id, name, salary, coffee_stand FROM Employees WHERE id = ?",
                  [Employee_id])
        return Employee(*c.fetchone())

    def find_all(self):
        c = self._conn.cursor()
        all = c.execute("""
             SELECT * FROM Employees ORDER BY id ASC
         """).fetchall()
        return [Employee(*row) for row in all]




class _Suppliers:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, Supplier):
        self._conn.execute("""INSERT INTO Suppliers (id, name, contact_information )
                           VALUES (?, ?, ?)""",
                           [Supplier.id, Supplier.name, Supplier.contact_information])

    def find(self, id):
        c = self._conn.cursor()
        c.execute("""SELECT id, name, contact_information FROM Suppliers WHERE id = ?""",
                  [id])
        return Supplier(*c.fetchone())

    def find_all(self):
        c = self._conn.cursor()
        all = c.execute("""
             SELECT * FROM Suppliers ORDER BY id ASC
         """).fetchall()
        return [Supplier(*row) for row in all]



class _Products:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, Product):
        self._conn.execute("""
            INSERT INTO Products (id, description, price, quantity) VALUES (?, ?, ?, ?)
        """, [Product.id, Product.description, Product.price, Product.quantity])

    def find_all(self):
        c = self._conn.cursor()
        all = c.execute("""
            SELECT * FROM Products ORDER BY id ASC
        """).fetchall()

        return [Product(*row) for row in all]

    def find(self, id):
        c = self._conn.cursor()
        c.execute("""
            SELECT * FROM Products
            WHERE id=? 
        """, [id])

        return Product(*c.fetchone())


    def updateQ(self, proId, qu):
        c = self._conn.cursor()
        c.execute("UPDATE Products SET quantity = quantity + ?  WHERE id = ? ", (qu, proId))



class _Coffee_stands:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, Coffe_stand):
        self._conn.execute("""
             INSERT INTO Coffee_stands (id, location, number_of_employees) VALUES (?, ?, ?)
         """, [Coffe_stand.id, Coffe_stand.location, Coffe_stand.number_of_employees])

    def find_all(self):
        c = self._conn.cursor()
        all = c.execute("""
             SELECT * FROM Coffee_stands ORDER BY id ASC
         """).fetchall()
        return [Coffe_stand(*row) for row in all]

    def find(self, id):
        c = self._conn.cursor()
        c.execute("""
             SELECT * FROM Coffee_stands
             WHERE id=? 
         """, [id])

        return Coffe_stand(*c.fetchone())


class _Activities:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, Activity):
        self._conn.execute("""
             INSERT INTO Activities (product_id, quantity, activator_id, date ) VALUES (?, ?, ?, ?)
         """, [Activity.product_id, Activity.quantity, Activity.activator_id, Activity.date])


    def find_all(self):
        c = self._conn.cursor()
        all = c.execute("""
             SELECT * FROM Activities ORDER BY date ASC
         """).fetchall()
        return [Activity(*row) for row in all]
