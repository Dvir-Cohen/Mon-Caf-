import DTO
from DAO import _Employees, _Products, _Coffee_stands, _Suppliers, _Activities
import sqlite3
import atexit


# The Repository


class _Repository:
    def __init__(self):
        self._conn = sqlite3.connect('moncafe.db')
        self.Employees = _Employees(self._conn)
        self.Suppliers = _Suppliers(self._conn)
        self.Products = _Products(self._conn)
        self.Coffee_stands = _Coffee_stands(self._conn)
        self.Activities = _Activities(self._conn)

    def _close(self):
        self._conn.commit()
        self._conn.close()

    def create_tables(self, config):
        self._conn.executescript("""
                CREATE TABLE Employees (id INTEGER PRIMARY KEY,
                                        name TEXT NOT NULL,
                                        salary REAL NOT NULL,
                                      coffee_stand INTEGER REFERENCES Coffee_stand(id)
                );

                CREATE TABLE Suppliers (id INTEGER PRIMARY KEY,
                                        name TEXT NOT NULL,
                                        contact_information TEXT
                );

                CREATE TABLE Products (id INTEGER PRIMARY KEY,
                                    description TEXT NOT NULL,
                                    price REAL NOT NULL,
                                    quantity INTEGER NOT NULL
                );
                CREATE TABLE Coffee_stands (id INTEGER PRIMARY KEY,
                                            location TEXT NOT NULL,
                                            number_of_employees INTEGER
                );
                CREATE TABLE Activities (product_id INTEGER REFERENCES Product(id),
                                        quantity INTEGER NOT NULL,
                                        activator_id INTEGER NOT NULL, 
                                        date DATE NOT NULL 
                );
        """)
        text = open(config).readlines()
        for line in text:
            line = line.split(', ')

            for element in range(0, line.__len__()):
                line[element] = str(line[element]).replace("\n", '')

            if line[0] == "C":
                coffee = DTO.Coffe_stand(int(line[1]), line[2], int(line[3]))
                self.Coffee_stands.insert(coffee)
            elif line[0] == "S":
                sup = DTO.Supplier(int(line[1]), line[2], line[3])
                self.Suppliers.insert(sup)
            elif line[0] == "E":
                empl = DTO.Employee(int(line[1]), line[2], float(line[3]), int(line[4]))
                self.Employees.insert(empl)
            elif line[0] == "P":
                prod = DTO.Product(int(line[1]), line[2], float(line[3]), 0)
                self.Products.insert(prod)

    def insertActivities(self, config):
        text = open(config).readlines()
        for line in text:
            line.replace(" ", "")
            line = line.split(",")
            pro_id = int(line[0])
            units_quantity = int(line[1])
            if units_quantity > 0:
                act = DTO.Activity(pro_id, units_quantity, int(line[2]), line[3])
                self.Activities.insert(act)
                self.Products.updateQ(pro_id, units_quantity)
            elif units_quantity < 0:
                rows = self.Products.find_all()
                for row in rows:
                    row = row.toString()
                    if pro_id == row[0]:
                        if int(row[3]) + units_quantity >= 0:
                            act = DTO.Activity(int(line[0]), units_quantity, int(line[2]), line[3])
                            self.Activities.insert(act)
                            self.Products.updateQ(int(line[0]), units_quantity)
                            break

    def print_EmpReport(self):
        c = self._conn.cursor()
        c.execute("""SELECT 
    	                e.name, 	e.salary,	cs.location , 
                         COALESCE (SUM(p.price * (ac.quantity * -1)),0) as total
                        FROM Employees e
                        LEFT  JOIN [Coffee_stands] AS cs ON cs.id = e.coffee_stand
                        LEFT  JOIN  [Activities] AS ac ON ac.activator_id = e.id and ac.quantity < 0
                       LEFT JOIN  [Products]   AS p ON p.id = ac.product_id
                        GROUP BY e.id, 	e.salary,	cs.location 

                      """)
        report_rows = c.fetchall()
        return report_rows

    def print_Activities(self):
        c = self._conn.cursor()
        c.execute("""SELECT Activities.date, Products.description, Activities.quantity, Employees.name, 
        Suppliers.name FROM Activities JOIN Products ON Activities.product_id = Products.id LEFT JOIN Employees ON 
        Activities.activator_id = Employees.id LEFT JOIN Suppliers ON Activities.activator_id = Suppliers.id ORDER BY 
        Activities.date ASC 

         """)
        Activities_rows = c.fetchall()

        return Activities_rows


# the repository singleton
repo = _Repository()

atexit.register(repo._close)
