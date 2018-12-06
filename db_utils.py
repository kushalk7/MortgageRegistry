import sqlite3
import datetime
# from customer import customer, loan

class DB:
    def __init__(self, dbFile):
        self.dbFile = dbFile
        self.conn = sqlite3.connect(self.dbFile)
        self.cust_id = 0
        self.ln_id = 0

    def saveCustomer(self, cust):
        # print(cust)
        curr = self.conn.cursor()
        curr.execute("SELECT MAX( ID ) FROM Customer")
        res = curr.fetchone()
        if res[0]:
            id = res[0] + 1
        else:
            id = self.cust_id + 1
        print(f"ID: {id}")
        curr.execute(f"INSERT INTO Customer (ID, NAME, ADDRESS, PHONE) \
        VALUES ({id}, \'{cust.name}\', \'{cust.address}\', {cust.phone})")
        self.conn.commit()

    def saveLoan(self, loan):
        curr = self.conn.cursor()
        curr.execute("SELECT MAX( ID ) FROM Loan")
        res = curr.fetchone()
        if res[0]:
            id = res[0] + 1
        else:
            id = self.ln_id + 1
        print(f"ID: {id}")
        res = curr.execute(f"INSERT INTO Loan (ID, AMT, ITEMS, DATE, CUST_ID) \
        VALUES ({id}, {loan.amt}, \'{loan.items}\', \'{loan.date}\', {loan.cust.id})")
        print(f"save res: {res}")
        self.conn.commit()
        return
    
    def searchCustomer(self, name, city):
        curr = self.conn.cursor()
        if name and city:
            curr.execute(f"SELECT * from Customer WHERE \
            NAME LIKE \'{name}%\' and ADDRESS LIKE \'{city}%\'") 
        elif name:
            curr.execute(f"SELECT * from Customer WHERE \
            NAME LIKE \'{name}%\'")
        res = curr.fetchall()
        print(res)
        return res

    def searchLoan(self, name, city, date):
        if date:
            date = datetime.datetime.strptime(date, '%d-%m-%Y').date()
            print(f"date: {date}")
        curr = self.conn.cursor()
        if name and city and date:
            curr.execute(f"SELECT * FROM Loan WHERE CUST_ID IN \
            (SELECT ID from Customer WHERE \
            NAME LIKE \'{name}%\' and ADDRESS LIKE \'{city}%\') and DATE = \'{date}\'") 
        
        elif name and city:
            curr.execute(f"SELECT * FROM Loan WHERE CUST_ID IN \
            (SELECT ID from Customer WHERE \
            NAME LIKE \'{name}%\' and ADDRESS LIKE \'{city}%\')")

        elif date:
            curr.execute(f"SELECT * FROM Loan WHERE DATE = \'{date}\'")

        elif name:
            curr.execute(f"SELECT * FROM Loan WHERE CUST_ID IN \
            (SELECT ID from Customer WHERE \
            NAME LIKE \'{name}%\')")
        
        elif city:
            curr.execute(f"SELECT * FROM Loan WHERE CUST_ID IN \
            (SELECT ID from Customer WHERE \
            ADDRESS LIKE \'{city}%\')")

        res = curr.fetchall()
        print(f"serchLoan:: {res}")
        return res

    def getCustomer(self, id):
        curr = self.conn.cursor()
        curr.execute(f"SELECT * from Customer WHERE ID = {id}")
        res = curr.fetchone()
        print(f"getCustomer::id:{id}: {res}")
        return res
        