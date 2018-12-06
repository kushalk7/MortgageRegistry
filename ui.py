import tkinter as tk                # python 3
from tkinter import font as tkfont  # python 3
from db_utils import DB
from customer import *
import tkSimpleDialog
from tkintertable import TableCanvas, TableModel

db = DB("loan.db")

class MortgageUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Mortgage Registry")
        self.title_font = tkfont.Font(
            family='Helvetica', size=18, weight="bold")

        x = (self.winfo_screenwidth() - self.winfo_reqwidth()) / 2
        y = (self.winfo_screenheight() - self.winfo_reqheight()) / 2
        self.geometry("+%d+%d" % (x, y))
        button = tk.Button(self, text="Home",
                           command=lambda: self.show_frame("StartPage"))
        button.pack(anchor="nw")
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)  # side="center",
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, AddCustomer, NewLoan, Search):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # label = tk.Label(self, text="This is the start page", font=controller.title_font)
        # label.pack(side="top", fill="x", pady=10)

        custBtn = tk.Button(self, text="New Customer",
                            command=lambda: controller.show_frame("AddCustomer"))
        loanBtn = tk.Button(self, text="New Loan",
                            command=lambda: controller.show_frame("NewLoan"))
        searchBtn = tk.Button(self, text="Search",
                              command=lambda: controller.show_frame("Search"))
        custBtn.pack(pady=5)
        loanBtn.pack(pady=5)
        searchBtn.pack(pady=5)


class AddCustomer(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        for i in range(3):
            self.grid_rowconfigure(i, weight=1)
            self.grid_columnconfigure(i, weight=1)

        r = 0
        c = 1
        tk.Label(self, text="Name").grid(row=r)
        self.nameEt = tk.Entry(self)
        self.nameEt.grid(row=r, column=c, sticky="ew")

        r = r + 1

        tk.Label(self, text="Address/City").grid(row=r)
        self.addressEt = tk.Entry(self)
        self.addressEt.grid(row=r, column=c, sticky="ew")

        r = r + 1

        tk.Label(self, text="Phone").grid(row=r)
        self.phoneEt = tk.Entry(self)
        self.phoneEt.grid(row=r, column=c, sticky="ew")

        r = r + 1

        button = tk.Button(self, text='Save', width=25,
                           command=lambda: self.save())
        button.grid(row=r)

    def save(self):
        cust = customer(self.nameEt.get(),
                        self.addressEt.get(), self.phoneEt.get())
        db.saveCustomer(cust)
        print(f"Saved successfully: \n {cust}")
        self.nameEt.delete(0, 'end')
        self.addressEt.delete(0, 'end')
        self.phoneEt.delete(0, 'end')


class NewLoan(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.lookupBtn = tk.Button(self, text='Lookup Customer', width=25,
                           command=lambda: Lookup(self, self.setCustomer))
        self.lookupBtn.grid(row=0)
        self.cust = None
        
        r = 1
        c = 1
        tk.Label(self, text="Name").grid(row=r)
        self.nameEt = tk.Entry(self)
        self.nameEt.grid(row=r, column=c, sticky="ew")

        r = r + 1

        tk.Label(self, text="Address/City").grid(row=r)
        self.addressEt = tk.Entry(self)
        self.addressEt.grid(row=r, column=c, sticky="ew")

        r = r + 1

        tk.Label(self, text="Phone").grid(row=r)
        self.phoneEt = tk.Entry(self)
        self.phoneEt.grid(row=r, column=c, sticky="ew")

        r = r + 1

        tk.Label(self, text="Date").grid(row=r)
        self.dateEt = tk.Entry(self)
        self.dateEt.grid(row=r, column=c, sticky="ew")
        
        r = r + 1

        tk.Label(self, text="Amount").grid(row=r)
        self.amtEt = tk.Entry(self)
        self.amtEt.grid(row=r, column=c, sticky="ew")

        r = r + 1

        tk.Label(self, text="Item/s").grid(row=r)
        self.itemEt = tk.Entry(self)
        self.itemEt.grid(row=r, column=c, sticky="ew")

        r = r + 1

        self.savebtn = tk.Button(self, text='Save', width=25,
                           command=lambda: self.save(), state=tk.DISABLED)
        self.savebtn.grid(row=r)

        self.amtEt.focus_set()

    def save(self):
        ln = loan(self.amtEt.get(),
                        self.itemEt.get(), self.dateEt.get(), self.cust)
        db.saveLoan(ln)
        print(f"Saved successfully: \n {ln}")
        self.nameEt.delete(0, 'end')
        self.addressEt.delete(0, 'end')
        self.phoneEt.delete(0, 'end')
        self.dateEt.delete(0, 'end')
        self.amtEt.delete(0, 'end')
        self.itemEt.delete(0, 'end')


    # Callback function to lookup customer
    def setCustomer(self, cust):
        self.cust = customer(cust['Name'], cust['Address'], cust['Phone'])
        self.cust.id = cust['ID']
        self.nameEt.insert(0, self.cust.name)
        self.addressEt.insert(0, self.cust.address)
        self.phoneEt.insert(0, self.cust.phone)
        # self.nameEt.config(state = "readonly")
        # self.addressEt.config(state = "readonly")
        # self.phoneEt.config(state = "readonly")
        self.savebtn.config(state = tk.NORMAL)
        print(f"Customer: \n {self.cust} ")


class Lookup(tkSimpleDialog.Dialog):

    def body(self, master):

        r = 0
        c = 1
        tk.Label(self, text="Name").grid(row=r)
        self.nameEt = tk.Entry(self)
        self.nameEt.grid(row=r, column=c, sticky="ew")

        r = r + 1

        tk.Label(self, text="Address/City").grid(row=r)
        self.addressEt = tk.Entry(self)
        self.addressEt.grid(row=r, column=c, sticky="ew")

        r = r + 1

        button = tk.Button(self, text='Search', width=25,
                           command=lambda: self.searchCustomer())
        button.grid(row=r)
        r = r + 1
        f = tk.Frame(self)
        self.f1 = tk.Frame(f)
        f.grid(row=r, sticky="nsew")
        self.f1.pack()
        # self.searchTbl = TableCanvas(f1, editable = False)
        # self.searchTbl.bind("<Double-Button-1>", self.OnDouble)
        # self.searchTbl.grid(row=r)
        # self.searchTbl.show()
        for i in range(r):
            # self.grid_rowconfigure(i, weight=1)
            self.grid_columnconfigure(i, weight=1)

        return self.nameEt



    def apply(self):
        # first = int(self.e1.get())
        # second = int(self.e2.get())
        # print (first, second) # or something
        return

    def OnDouble(self, event):
        widget = event.widget
        value=widget.model.getRecordAtRow(widget.getSelectedRow())
        print ("selection:: '%s'" % value)
        self.callback(value)
        self.searchTbl.destroy()
        self.f1.destroy()
        self.cancel()
        # self.destroy()
        return value
    
    def searchCustomer(self):
        res = db.searchCustomer(self.nameEt.get(), self.addressEt.get())
        data = {}
        col = ['ID', 'Name', 'Phone', 'Address']
        for i, l in enumerate(res):
            data[i] = {c[0]:c[1] for c in zip(col, l)}
        if data:
            self.searchTbl = TableCanvas(self.f1, editable = False, data=data)
            self.searchTbl.bind("<Double-Button-1>", self.OnDouble)
            # self.searchTbl.model.importDict(data) 
            # print (self.searchTbl.model.columnNames)
            # self.searchTbl.redraw()
            self.searchTbl.show()


class Search(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        r = 0
        c = 1
        tk.Label(self, text="Name").grid(row=r)
        self.nameEt = tk.Entry(self)
        self.nameEt.grid(row=r, column=c, sticky="ew")

        r = r + 1

        tk.Label(self, text="Address/City").grid(row=r)
        self.addressEt = tk.Entry(self)
        self.addressEt.grid(row=r, column=c, sticky="ew")

        r = r + 1

        tk.Label(self, text="Date").grid(row=r)
        self.dateEt = tk.Entry(self)
        self.dateEt.grid(row=r, column=c, sticky="ew")

        r = r + 1

        button = tk.Button(self, text='Search', width=25,
                           command=lambda: self.searchLoan())
        button.grid(row=r)

        r = r + 1
        f = tk.Frame(self)
        self.f1 = tk.Frame(f)
        f.grid(row=r, column=0, columnspan=10, sticky="nsew")
        self.f1.pack()
        
        for i in range(r):
            # self.grid_rowconfigure(i, weight=1)
            self.grid_columnconfigure(i, weight=1)
        
    def searchLoan(self):
        res = db.searchLoan(self.nameEt.get(), self.addressEt.get(), self.dateEt.get())
                        # datetime.datetime.strptime(self.dateEt.get(), '%d-%m-%Y').date())
        # ID, amt, items, date, cust_id
        data = {}
        col = ['ID', 'Name', 'Phone', 'Address', 'Date', 'Amt', 'Items']
        
        for i, l in enumerate(res):
            cust = db.getCustomer(l[4]) # id, name, phone, add
            val = [l[0], cust[1], cust[2], cust[3], l[3], l[1], l[2]]
            data[i] = {c[0]:c[1] for c in zip(col, val)}
        if data:
            self.searchTbl = TableCanvas(self.f1, editable = False, data=data)
            # self.searchTbl.bind("<Double-Button-1>", self.OnDouble)
            # self.searchTbl.model.importDict(data) 
            # print (self.searchTbl.model.columnNames)
            # self.searchTbl.redraw()
            self.searchTbl.show()

if __name__ == "__main__":
    app = MortgageUI()
    app.mainloop()




        # self.yScroll = tk.Scrollbar(self, orient=tk.VERTICAL)
        # self.yScroll.grid(row=r, column=1, sticky=tk.N+tk.S)
        # self.xScroll = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        # self.xScroll.grid(row=r+1, column=0, sticky=tk.E+tk.W)
        # self.searchlist = tk.Listbox(self,
        #                                 xscrollcommand=self.xScroll.set,
        #                                 yscrollcommand=self.yScroll.set)
        # self.searchlist.grid(row=r, sticky="nsew", columnspan=3)
        # self.xScroll['command'] = self.searchlist.xview
        # self.yScroll['command'] = self.searchlist.yview
        # self.searchlist.bind("<Double-Button-1>", self.OnDouble)


        # self.yScroll = tk.Scrollbar(self, orient=tk.VERTICAL)
        # self.yScroll.grid(row=r, column=1, sticky=tk.N+tk.S)
        # self.xScroll = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        # self.xScroll.grid(row=r+1, column=0, sticky=tk.E+tk.W)
        # self.searchlist = tk.Listbox(self,
        #                                 xscrollcommand=self.xScroll.set,
        #                                 yscrollcommand=self.yScroll.set)
        # self.searchlist.grid(row=r, sticky="nsew", columnspan=3)
        # self.xScroll['command'] = self.searchlist.xview
        # self.yScroll['command'] = self.searchlist.yview