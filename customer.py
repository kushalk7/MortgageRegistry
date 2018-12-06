import datetime

class customer:
    def __init__ (self, name, address, phone):
        self.name = name
        self.address = address
        self.phone = phone
        self.loans = None
    
    def __str__(self):
        return f"Name: {self.name} \n Address: {self.address} \n Phone: {self.phone}"
    
class loan:
    def __init__ (self, amt, items, date):
        self.amt = amt
        self.items = items
        self.date = datetime.datetime.strptime(date, '%d-%m-%Y').date()

    