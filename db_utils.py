import sqlite3
# from customer import customer, loan

class DB:
    def __init__(self, dbFile):
        self.dbFile = dbFile
        self.conn = sqlite3.connect(self.dbFile)
        self.cust_id = 0

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
    
    def search(self, name, city, date):
        curr = self.conn.cursor()
        if name and city and date:
            curr.execute(f"SELECT * FROM Loan WHERE CUST_ID IN \
            (SELECT ID from Customer WHERE \
            NAME LIKE \'{name}\' and ADDRESS LIKE \'{city}\') and DATE = \'{date}\'") 
        
        elif name and city:
            curr.execute(f"SELECT * FROM Loan WHERE CUST_ID IN \
            (SELECT ID from Customer WHERE \
            NAME LIKE \'{name}\' and ADDRESS LIKE \'{city}\')")

        elif date:
            curr.execute(f"SELECT * FROM Loan WHERE DATE = \'{date}\'")

        elif name:
            curr.execute(f"SELECT * FROM Loan WHERE CUST_ID IN \
            (SELECT ID from Customer WHERE \
            NAME LIKE \'{name}\')")
        
        elif city:
            curr.execute(f"SELECT * FROM Loan WHERE CUST_ID IN \
            (SELECT ID from Customer WHERE \
            ADDRESS LIKE \'{city}\')")

        res = curr.fetchall()
        print(res)
        return res


        