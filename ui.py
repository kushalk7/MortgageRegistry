import tkinter as tk                # python 3
from tkinter import font  as tkfont # python 3
from db_utils import DB
from customer import *

db = DB("loan.db")

class MortgageUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Mortgage Registry")
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold")

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
        container.pack(fill="both", expand=True) #side="center", 
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
        cust = customer(self.nameEt.get(), self.addressEt.get(), self.phoneEt.get())
        db.saveCustomer(cust)
        print(f"Saved successfully: \n {cust}")
        self.nameEt.delete(0, 'end')
        self.addressEt.delete(0, 'end')
        self.phoneEt.delete(0, 'end')
    


class NewLoan(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

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
        command=lambda: self.search())
        button.grid(row=r)

        r = r + 1

        self.searchlist = tk.Listbox(self)
        self.searchlist.grid(row=r, sticky="nsew", columnspan=3)

        for i in range(r):
            self.grid_rowconfigure(i, weight=1)
            self.grid_columnconfigure(i, weight=1)

    def search(self):
        res = db.search(self.nameEt.get(), self.addressEt.get(), 
        datetime.datetime.strptime(self.dateEt.get(), '%d-%m-%Y').date())
        for l in res:
            self.searchlist.insert(tk.END, l)


if __name__ == "__main__":
    app = MortgageUI()
    app.mainloop()