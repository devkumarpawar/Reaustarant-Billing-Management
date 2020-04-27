from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pymysql


window = Tk()
window.geometry("900x600")
window.title("Billing")

#!=====field listner=========!#
def quantityfieldlistner(a,b,c):
    global quantityVariable
    global costVariable
    global itemRate
    quantity = quantityVariable.get()
    if quantity != "":
        try:
            quantity = float(quantity)
            cost = quantity*itemRate
            quantityVariable.set(".%2f"%quantity)
            costVariable.set(".%2f"%cost)
        except ValueError:
           quantity = quantity[:-2]
           quantityVariable.set(".%2f"%quantity)
    else:
        quantity = 0
        quantityVariable.set("%.2f"%quantity)

def costfieldlistner(a,b,c):
    global quantityVariable
    global costVariable
    global itemRate
    cost = costVariable.get()
    if cost != "":
        try:
            cost = float(cost)
            quantity = cost/itemRate
            quantityVariable.set(".%2f"%quantity)
            costVariable.set(".%2f"%cost)
        except ValueError:
           cost = cost[:-1]
           costVariable.set(cost)
    else:
        cost = 0
        costVariable.set(cost)


#!========global variable for entries========!
#!======login variable=======!

usernameVar = StringVar()
passwordVar = StringVar()

#!=====main window variable=======!

options = []
rateDict = []
ItemVariable = StringVar()
quantityVariable = StringVar()
quantityVariable.trace("w",quantityfieldlistner)
itemRate = 2
rateVariable = StringVar()
rateVariable.set("%.2f"%itemRate)
costVariable = StringVar()
costVariable.trace("w", costfieldlistner)
#!======Main Tree View========!
billsTV = ttk.Treeview(height=15,column=("Item Name","Quantity","Cost"))

#!===== add item variable======!
storeOption=["Frozen","Fresh"]
addItemNameVar = StringVar()
addItemTypeVar = StringVar()
addItemRateVar = StringVar()
addStoredVar = StringVar()
addStoredVar.set(storeOption[0])

#======== function to generate bill=======#

def generate_bill():
    global itemVariable
    global quantityVariable
    global itemRate
    global costVariable
    itemName = itemVariable.get()
    quantity = quantityVariable.get()
    rate = itemRate
    cost = costVariable.get()
    conn = pymysql.connect(host="localhost", user="root", password="", db="billservice")
    cursor = conn.cursor()

    query = "insert into bills (name,quantity,rate,cost) values'()','()','()','()'".format(itemName,quantity,itemRate,cost)
    cursor.execute(query)
    conn.commit()
    conn.close()
    quantityVariable.set("0")
    costVariable.set("0")
#======= function to Logout=======#
def Logout():
    remove_all_widgets()
    Loginwindow()


#==========functions to read data from list of item =====#
def readAllData():
    global options
    global rateDict
    global  itemVariable
    global itemRate
    global rateVar
    options = []
    rateDict = []
    conn = pymysql.connect(host="localhost", user="root", password="", db="billservice")
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    query = "select ' from itemlist"
    cursor.execute(query)
    data = cursor.fetchall()
    count = 0

    for row in data():
        count+=1
        options.append(row["nameid"])
        rateDict[row["nameid"]]=row("rate")
        ItemVariable.set(options[0])
        itemRate = int(rateDict[options[0]])
    conn.close()
    rateVar.set("%.2f"%itemRate)
    if count == 0:
        remove_all_widgets()
        ItemAddWindow()
    else:
        remove_all_widgets()
        ItemAddWindow()

def optionMenuListener(event):
    global  itemVariable
    global rateDict
    global itemRate
    item = itemVariable.get()
    itemRate = int(rateDict[item])
    rateVariable.set("%.2f" % itemRate)

#====== function to remove all widgets=====#
def remove_all_widgets():
    global window
    for widget in window.winfo_children():
        widget.grid_remove()


# =======admin login function======#
def adminLogin():
    global usernameVar
    global passwordVar

    username = usernameVar.get()
    password = passwordVar.get()

    conn = pymysql.connect(host="localhost",user="root",password="",db="billservice")
    cursor = conn.cursor()

    query = "select from users where username='[]' and password='()'".format(username,password)
    cursor.execute(query)
    data = cursor.fetchall()
    admin = False
    for row in data :
        admin = True
    conn.close()
    if admin:
        readAllData()
        mainwindow()
    else:
        messagebox.showerror("invalid user","credential enters are invalid")

def addItemListener():
    remove_all_widgets()
    ItemAddWindow()


def addItem():
    global addItemNameVar
    global addItemRateVar
    global addItemTypeVar
    global addStoredVar
    name = addItemNameVar.get()
    rate = addItemRateVar.get()
    type = addItemTypeVar.get()
    storedtype = addStoredVar.get()
    nameid = name.replace("","")

    conn = pymysql.connect(host="localhost", user="root", password="", db="billservice")
    cursor = conn.cursor()
    query = "insert into itemlist (name,nameid,rate,type,storedtype) value('()','()','()','()','()')".format(name,nameid,rate,type,storedtype)
    cursor.execute(query)
    conn.commit()
    conn.close()
    addItemNameVar.set("")
    addItemRateVar.set("")
    addItemTypeVar.set("")




def Loginwindow():
    titleLabel = Label(window,text="P&E Billing System",font="lucida 40 bold",fg="red")
    titleLabel.grid(row=0,column=0,columnspan=4,padx=(40,0),pady=(10,0))

    passwordLabel = Label(window,text="Password")
    passwordLabel.grid(row=3,column=2,padx=20,pady=5)

    loginLabel = Label(window,text="Admin Login",font="Arial 30")
    loginLabel.grid(row=1,column=2,columnspan=2,padx=(50,0),pady=10)

    usernameLabel = Label(window,text="Username")
    usernameLabel.grid(row=2,column=2,padx=20,pady=5)

    usernameEntry = Entry(window,textvariable=usernameVar)
    usernameEntry.grid(row=2,column=3,padx=20,pady=5)

    passwordEntry = Entry(window,textvariable=passwordVar,show="*")
    passwordEntry.grid(row=3,column=3,padx=20,pady=5)

    loginButton = Button(window,text="Login",width=10,height=2,command="Lambda:adminLogin()")
    loginButton.grid(row=4,column=2,columnspan=2)




def mainwindow():
    titleLabel = Label(window, text="P&E Billing System", font="lucida 30 bold", fg="red")
    titleLabel.grid(row=0, column=1, columnspan=3, pady=(10,0))

    addMinItem = Button(window,text="Add Item",width=20,height=2)
    addMinItem.grid(row=1,column=0,padx=(10,0),pady=(10,0))

    LogoutButton = Button(window,text="Logout",width=20,height=2,command = lambda:Logout())
    LogoutButton.grid(row=1,column=4,pady=(10,0))

    ItemLabel = Label(window,text="Select Item")
    ItemLabel.grid(row=2,column=0,padx=(5,0),pady=(10,0))

    ItemDropDown = OptionMenu(window,ItemVariable,"options",command = "optionMenuListener" )
    ItemDropDown.grid(row=2,column=1,padx=(10,0),pady=(10,0))

    rateLabel = Label(window,text="Rate")
    rateLabel.grid(row=2,column=2,padx=(10,0),pady=(10,0))

    rateValue = Label(window,textvariable="rateVar")
    rateValue.grid(row=2,column=3,padx=(10,0),pady=(10,0))


    quantityLabel = Label(window,text="Quantity")
    quantityLabel.grid(row=3,column=0,padx=(5,0),pady=(10,0))

    quantityEntry = Entry(window,textvariable="quantityVar")
    quantityEntry.grid(row=3,column=1,padx=(5,0),pady=(10,0))

    costLabel = Label(window,text="Cost")
    costLabel.grid(row=3,column=2,padx=(10,0),pady=(10,0))

    costEntry = Entry(window,textvariable="costVar")
    costEntry.grid(row=3,column=3,padx=(10,0),pady=(10,0))

    buttonBill = Button(window,text="Generate Bill",width=15,command = lambda:generate_bill())
    buttonBill.grid(row=3,column=4,padx=(5,0),pady=(10,0))

    billsLabel = Label(window,text="Bills",font="lucida 25 ")
    billsLabel.grid(row=4,column=2)
    billsTV.grid(row=5,column=0,columnspan=5)

    scrollBar = Scrollbar(window,orient="vertical",command=billsTV.yview)
    scrollBar.grid(row=5,column=4,sticky="NSE")

    billsTV.configure(yscrollcommand =scrollBar.set)
    billsTV.heading("#0",text="Item Name")
    billsTV.heading("#1", text="Rate")
    billsTV.heading("#2", text="Quantity")
    billsTV.heading("#3", text="Cost")


def ItemAddWindow():
    backButton = Button(window,text="Back",width=20,height=2,command=lambda:"readAllData()")
    backButton.grid(row=0,column=1)

    titleLabel = Label(window, text="P&E Billing System",width="50",font="lucida 30 bold", fg="red")
    titleLabel.grid(row=0, column=1, columnspan=4, pady=(10, 0))

    itemNameLabel = Label(window,text="Name")
    itemNameLabel.grid(row=1,column=1,pady=(10,0))

    itemNameEntry = Entry(window,textvariable="addItemNameVar")
    itemNameEntry.grid(row=1,column=2,pady=(10,0))

    itemRateLabel = Label(window, text="Rate")
    itemRateLabel.grid(row=1, column=3, pady=(10, 0))

    itemRateEntry = Entry(window, textvariable="addItemRateVar")
    itemRateEntry.grid(row=1, column=4, pady=(10, 0))

    itemTypeLabel = Label(window, text="Type")
    itemTypeLabel.grid(row=2, column=1, pady=(10, 0))

    itemTypeEntry = Entry(window, textvariable="addItemTypeVar")
    itemTypeEntry.grid(row=2, column=2, pady=(10, 0))

    StoredTypeLabel = Label(window, text="Stored Type")
    StoredTypeLabel.grid(row=2, column=3, pady=(10, 0))

    StoredEntry = OptionMenu(window, addStoredVar,"storeOption")
    StoredEntry.grid(row=2, column=3, pady=(10, 0))

    AddItemButton = Button(window,text="Add Item",width=20,height=2,command="lambda:addItem()")
    AddItemButton.grid(row=3,column=3,pady=(10,0))

#ItemAddWindow()
mainwindow()
#Loginwindow()
#adminLogin()

window.mainloop()