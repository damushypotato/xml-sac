import tkinter as tk
from tkinter import ttk, messagebox
import xml.etree.ElementTree as ET

class Laptop:
    def __init__(self, name, price, details):
        self.name = name
        self.price = price
        self.details = details

laptops = [
    Laptop("Lenovo Thinkpad IIe 5th Gen", 971.45, "15.6-inch FHD (1920 x 1080) IPS display, Intel Core i5-1135G7, 8GB RAM, 256GB SSD, Windows 10 Pro"),
    Laptop("Apple MacBook Air 13 - Silver", 1347.72, "13.3-inch Retina display, Apple M1 chip, 8GB RAM, 256GB SSD, macOS Big Sur"),
    Laptop("Asus Zephyrus G14", 2789.00, "14-inch WQHD (2560 x 1440) display, AMD Ryzen 9 5900HS, 16GB RAM, 1TB SSD, NVIDIA GeForce RTX 3060, Windows 10 Home"),
]

discounts = {
    "No Discount": 0,
    "Student Discount ($120)": 120,
}

def calculate_total(laptop, discount):
    if laptop not in [lap.name for lap in laptops]:
        raise ValueError("Invalid laptop selection")
    if discount not in discounts:
        raise ValueError("Invalid discount selection")
    
    l = [lap for lap in laptops if lap.name == laptop][0]
    d = discounts[discount]
    
    return l.price - d

def save_order(studentID, studentName, studentYearLevel, laptopOrder, discount):
    tree = ET.parse("orders.xml")
    root = tree.getroot()
    
    order = ET.Element("order")
    studentIDElement = ET.SubElement(order, "studentID")
    studentIDElement.text = studentID
    studentNameElement = ET.SubElement(order, "studentName")
    studentNameElement.text = studentName
    studentYearLevelElement = ET.SubElement(order, "studentYearLevel")
    studentYearLevelElement.text = studentYearLevel
    laptopOrderElement = ET.SubElement(order, "laptopOrder")
    laptopOrderElement.text = laptopOrder
    discountElement = ET.SubElement(order, "discount")
    discountElement.text = discount
    
    root.append(order)
    
    tree.write("orders.xml")

def view_orders():

    root = tk.Tk()
    root.title("Orders")
    
    tree = ttk.Treeview(root)
    tree["columns"] = ("studentID", "studentName", "studentYearLevel", "laptopOrder", "discount")
    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("studentID", anchor=tk.W, width=100)
    tree.column("studentName", anchor=tk.W, width=100)
    tree.column("studentYearLevel", anchor=tk.W, width=100)
    tree.column("laptopOrder", anchor=tk.W, width=200)
    tree.column("discount", anchor=tk.W, width=100)
    
    tree.heading("#0", text="", anchor=tk.W)
    tree.heading("studentID", text="Student ID", anchor=tk.W)
    tree.heading("studentName", text="Student Name", anchor=tk.W)
    tree.heading("studentYearLevel", text="Year Level", anchor=tk.W)
    tree.heading("laptopOrder", text="Laptop Order", anchor=tk.W)
    tree.heading("discount", text="Discount", anchor=tk.W)
    
    tree.grid(column=0, row=0, padx=10, pady=10)
    
    tree.delete(*tree.get_children())
    treeData = ET.parse("orders.xml")
    for order in treeData.getroot():
        studentID = order.find("studentID").text
        studentName = order.find("studentName").text
        studentYearLevel = order.find("studentYearLevel").text
        laptopOrder = order.find("laptopOrder").text
        discount = order.find("discount").text
        
        tree.insert("", tk.END, values=(studentID, studentName, studentYearLevel, laptopOrder, discount))
        
    searchFrame = ttk.Frame(root)
    
    searchLabel = ttk.Label(searchFrame, text="Search:")
    searchLabel.grid(column=0, row=0)
    
    searchEntry = ttk.Entry(searchFrame)
    searchEntry.grid(column=1, row=0)
    
    def search():
        query = searchEntry.get()
        tree.delete(*tree.get_children())
        for order in treeData.getroot():
            studentID = order.find("studentID").text
            studentName = order.find("studentName").text
            studentYearLevel = order.find("studentYearLevel").text
            laptopOrder = order.find("laptopOrder").text
            discount = order.find("discount").text
            
            if query in [studentID, studentName, studentYearLevel, laptopOrder, discount]:
                tree.insert("", tk.END, values=(studentID, studentName, studentYearLevel, laptopOrder, discount))
                
    searchButton = ttk.Button(searchFrame, text="Search", command=search)
    searchButton.grid(column=2, row=0)
    
    searchFrame.grid(column=0, row=1, padx=10, pady=10)
        
    root.mainloop()
    

def laptop_order_form():
    root = tk.Tk()
    root.title("Laptop Order")

    frame = tk.Frame(root)
    frame.grid(column=0, row=0, padx=25, pady=25)

    ttk.Label(frame, text="Laptop Selection", font=("Arial", 20)).grid(column=0, row=0, pady=25)

    form=ttk.Frame(frame)
    form.grid(column=0, row=1, padx=25)
    
    studentID = tk.StringVar()
    studentName = tk.StringVar()
    studentYearLevel = tk.StringVar()
    laptopOrder = tk.StringVar()
    discount = tk.StringVar()
    
    def submit():
        if studentID.get() == "" or studentName.get() == "" or studentYearLevel.get() == "Select Year Level" or laptopOrder.get() == "Select Laptop" or discount.get() == "Select Discount":
            messagebox.showerror("Error", "Please fill out all fields")
            return
        
        save_order(studentID.get(), studentName.get(), studentYearLevel.get(), laptopOrder.get(), discount.get())
        
        messagebox.showinfo("Success", "Order has been submitted")
        
        studentID.set("")
        studentName.set("")
        studentYearLevel.set("Select Year Level")
        laptopOrder.set("Select Laptop")
        discount.set("Select Discount")
        total.set("")
        detailsLabel.config(text="")
        detailsLabel.grid_forget()
        detailsButton["text"] = "Show Details"
        totalLabel.config(relief=tk.FLAT, borderwidth=0)

    def calculate(event):
        if laptopOrder.get() == "Select Laptop" or discount.get() == "Select Discount":
            totalLabel.config(relief=tk.FLAT, borderwidth=0)
            total.set("Please select all options")
            return
        try:
            totalLabel.config(relief=tk.RAISED, borderwidth=2)
            laptop_ = laptopOrder.get()
            discount_ = discount.get()
            
            laptop = [lap for lap in laptops if lap.name == laptopOrder.get()][0]
            global laptopDetails_
            laptopDetails_ = laptop.details.replace(",", "\n")
            
            if detailsButton["text"] == "Hide Details":
                detailsLabel.config(text=laptopDetails_)
            
            total.set(f"${calculate_total(laptop_, discount_):.2f}")
        except ValueError as e:
            totalLabel.config(relief=tk.FLAT, borderwidth=0)
            total.set("Please select all options")
        

    ttk.Label(form, text="Student ID:").grid(column=0, row=0, padx=10, pady=10, sticky=tk.W)
    ttk.Entry(form, textvariable=studentID).grid(column=1, row=0, padx=10, pady=10, sticky=tk.W)
    
    ttk.Label(form, text="Student Name:").grid(column=0, row=1, padx=10, pady=10, sticky=tk.W)
    ttk.Entry(form, textvariable=studentName).grid(column=1, row=1, padx=10, pady=10, sticky=tk.W)

    ttk.Label(form, text="Year Level:").grid(column=0, row=2, padx=10, pady=10, sticky=tk.W)
    studentYearLevel.set("Select Year Level")
    yearLevelCombo = ttk.Combobox(form, textvariable=studentYearLevel, width=10, state="readonly")
    yearLevelCombo['values'] = list(range(1, 13))
    yearLevelCombo.grid(column=1, row=2, padx=10, pady=10, sticky=tk.W)
    
    ttk.Label(form, text="Laptop Order:").grid(column=0, row=3, padx=10, pady=10, sticky=tk.W)
    laptopOrder.set("Select Laptop")
    laptopCombo = ttk.Combobox(form, textvariable=laptopOrder, width=30, state="readonly")
    laptopCombo.bind("<<ComboboxSelected>>", calculate)
    laptopCombo['values'] = [laptop.name for laptop in laptops]
    laptopCombo.grid(column=1, row=3, padx=10, pady=10, sticky=tk.W)
    
    def button_toggle_details():
        if laptopOrder.get() == "Select Laptop":
            return
        if discount.get() == "Select Discount":
            return
        
        if detailsButton["text"] == "Show Details":
            detailsButton["text"] = "Hide Details"
            detailsLabel.config(text=laptopDetails_)
            detailsLabel.grid(column=1, row=4, padx=10, pady=10, sticky=tk.W)
        else:
            detailsButton["text"] = "Show Details"
            detailsLabel.config(text="")
            detailsLabel.grid_forget()
        
    detailsButton = ttk.Button(form, text="Show Details", command=button_toggle_details)
    detailsButton.grid(column=2, row=3, padx=10, pady=10, sticky=tk.W)
    
    detailsLabel = ttk.Label(form, text="")
    detailsLabel.grid(column=1, row=4, padx=10, pady=10, sticky=tk.W)
    
    
    ttk.Label(form, text="Discount:").grid(column=0, row=5, padx=10, pady=10, sticky=tk.W)
    discount.set("Select Discount")
    discountCombo = ttk.Combobox(form, textvariable=discount, width=30, state="readonly")
    discountCombo.bind("<<ComboboxSelected>>", calculate)
    discountCombo['values'] = list(discounts.keys())
    discountCombo.grid(column=1, row=5, padx=10, pady=10, sticky=tk.W)

    ttk.Label(form, text="Total:").grid(column=0, row=6, padx=10, pady=10, sticky=tk.W)
    total = tk.StringVar()
    totalLabel = ttk.Label(form, textvariable=total)
    totalLabel.grid(column=1, row=6, padx=10, pady=10, sticky=tk.W)
    
    ttk.Button(frame, text="Submit", command=submit).grid(column=0, row=2, pady=10)
    
    ttk.Button(frame, text="View Orders", command=view_orders).grid(column=0, row=3, pady=10)
    
    root.mainloop()
    


laptop_order_form()