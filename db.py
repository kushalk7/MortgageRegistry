import sqlite3

conn = sqlite3.connect('loan.db')

print("Opened database successfully")

conn.execute('''CREATE TABLE Customer
         (ID INT PRIMARY KEY     NOT NULL,
         NAME           TEXT    NOT NULL,
         PHONE          INT     NOT NULL,
         ADDRESS        TEXT);''')
print("Customer table created successfully")

conn.execute('''CREATE TABLE Loan
         (ID INT PRIMARY KEY    NOT NULL,
         AMT           INT    NOT NULL,
         ITEMS         TEXT   NOT NULL,
         DATE          TEXT   NOT NULL,
         CUST_ID       INT    NOT NULL,
         FOREIGN KEY(CUST_ID) REFERENCES Customer(ID));''')

print("Loan table created successfully")

conn.close()