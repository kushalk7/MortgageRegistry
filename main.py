import tkinter as tk

root = tk.Tk()
r = 0
c = 1
root.title("Mortgage Registry")
w = tk.Label(root, text="Hello Khandelwal!")
w.grid(row=r)

r = r + 1

tk.Label(root, text="Name").grid(row=r)
e1 = tk.Entry(root)
e1.grid(row=r, column=c)

r = r + 1

tk.Label(root, text="Phone").grid(row=r)
e2 = tk.Entry(root)
e2.grid(row=r, column=c)

r = r + 1

button = tk.Button(root, text='Stop', width=25, command=root.destroy)
button.grid(row=r)
root.mainloop()