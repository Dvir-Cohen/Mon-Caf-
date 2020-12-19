
from repository import  repo


def printdb():
    print ("Activities")
    for line in repo.Activities.find_all():
        print(line.toString())

    print ("Coffee stands")
    for line in repo.Coffee_stands.find_all():
        print(line.toString())

    print("Employees")
    for line in repo.Employees.find_all():
        print(line.toString())
    print("Products")
    for line in repo.Products.find_all():
        print(line.toString())
    print("Suppliers")
    for line in repo.Suppliers.find_all():
        print(line.toString())
    print()
    print("Employees report")
    rows= repo.print_EmpReport()
    for row in rows:
        print(row[0] + " " +str(row[1]) + " "+row[2] + " "+ str(row[3]) )

    rows = repo.print_Activities()
    if rows.__len__()>0:
        print()
        print("Activities")
        for row in rows:
            if int(row[2])>0:
                print((*row[0:3], None, row[4]))
            else:
                print((*row[0:4], None))


if __name__ == "__main__":
    printdb()
