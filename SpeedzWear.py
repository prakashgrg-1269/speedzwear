import datetime
def load_products():
    """Load every product details from inventory.txt as list of lists"""
    products = []
    try:   # Error handling for missing file
        with open("inventory.txt", "r") as file:   #opening file on read mode to retrieve data
            for line in file:          #go through each line in file
                products.append(line.strip().split(",")) #each line is split by ',' and added to list
    except FileNotFoundError:
        print("\nError !!! file not found")  #if filepath not found, alerts user
        return
    if not products:  # check if file is empty
        print(f"{file} is empty")
        return
    return products   # return a list or empty

def update_inventory(products):
    """Save the updated products list to inventory.txt"""
    try:
        with open("inventory.txt", "w") as file: #try opening file in write mode
            for p in products:
                for i in range(len(p)):
                    file.write(p[i])              #write each product detail one by one     
                    if i < len(p)-1:                  
                        file.write(",")           #seperate each details of a product by a comma
                file.write("\n")                  #new line for every product
    except Exception as e:
        print("Error updating inventory:", e)

def display():
    """Display every shoe details in tabular form"""
    products=load_products()   #retieve shoe details from inventory.txt
    print("\n")
    print("====================   list of all products   ======================")
    print(f"{'Shoe type':<20}{'Brand':<14}{'Stock':<10}{'price(Rs)':<11}{'Origin'}")  #table headers
    print("====================================================================")
    for shoe in products:
        print(f"{shoe[0]:<20}{shoe[1]:<14}{shoe[2]:<10}{shoe[3]:<11}{shoe[4]}")  #prints every product details with proper format
        print("--------------------------------------------------------------------")

# Buying product
def purchase_Product():
    """carryout sales"""
    products=load_products()   #retrieve shoe details from list inventory.txt
    if not products:   #goto main menu if file is empty
        return
    invoices=[]
    customer = input("Enter customer name: ")  #ask for customer name
    if customer.strip() == "":                 # check if customer name is empty
        print("Customer name cannot be empty.")
        return
    display()
    total = 0
    total_discount = 0
    while(True):                 #continuous loop
        choice = input("Enter shoe type to buy or 'DONE' to go to main menu:") 
        if choice.strip().lower()=="done":
            break                #beaks the while loop
        try:                   #make sure quantity is an integer
            qty_buy = int(input("Enter quantity: "))  #takes only integer as input
            if qty_buy <= 0:                          #show error if quantity is 0 or negative
                print("Quantity must be greater than 0")
                continue                               
        except ValueError:
            print("Invalid quantity. Quantity can only be an integer")
            continue
        found = False
        for product in products:         #go through every product in list
            shoe=product[0]
            brand=product[1]
            qty=int(product[2])
            price=float(product[3])
            origin=product[4]
            
            if shoe.strip().lower() == choice.lower():   #check if shoe exists
                found=True
                if qty_buy <= qty:         #make sure there is enough stock
                    subtotal = price * qty_buy
                    discount=0
                    if qty_buy > 10:       #check if the purchase is eligibe for discount 
                        if origin.strip().lower() == "international":
                            discount= subtotal*0.05
                        elif origin.strip().lower() == "domestic":
                            discount= subtotal*0.07
                             
                    total +=subtotal
                    total_discount+=discount
                    invoices.append(f"{shoe:<15}{brand:<10}{qty_buy:<8}{price:<8}{price * qty_buy}\n") #add to a list for billling purpose
                    product[2] = str(qty - qty_buy)      # Update stock
                
                else:
                    print("Not enough stock!")
                    continue
                break
        if not found:
            print("Product not found in the inventory")

    update_inventory(products) # Save updated stock to file(override the file)
    # Generate bill
    now = datetime.datetime.now()  #exxtract date and time
    filename = f"purchase_invoice_{customer}.txt"       
    file = open(filename,"a")           #created new file if file doesnot exists
    #create bill in tabular format
    file.write("=================== SpeedzWears ==================\n")
    file.write(f"Customer: {customer}\n")
    file.write(f"Date: {now}\n") 
    file.write(f"{'Shoe':<15}{'Brand':<10}{'Qty':<8}{'Rate (Rs)':<8}{'Total'}\n")  #table headers
    file.write("===================================================\n") 
    for line in invoices:
        file.write(line)      
    file.write("===================================================\n")
    file.write(f"Total: Rs{total}\n")
    file.write(f"Discount: Rs {total_discount}\n")
    file.write(f"Grand Total: Rs {total-total_discount}\n")
    file.write("===================================================\n")
    print("Invoice generated:",filename)
    print("Purchase complete . Thank you ")    #message to let user know purchase is successful
    file.close()

def addNewProduct(supplier):
    """to add new product no need to directly call the method"""
    shoe_type = input("Enter shoe type:")    
    brand = input("Enter brand:")
    try:   #make sure quantity and price is integer 
        qty = int(input("Enter quantity:"))
        if qty <= 0:   #check if quantity is less or equal to 0.
            print("Quantity must be greater than zero")
            return
        cost_price = float(input("Enter price:"))
        if cost_price <= 0: # check if price is negative or 0.
            print("Price must be greater than zero")
            return
    except ValueError:
        print("quantity and price values must be numeric")
    origin = input("Enter origin(domestic/international):")    
    if origin not in ("domestic", "international"):    #make sure the value of origin is either domestic or international
        print("Invalid input!!! Origin must be domestic/international")
        return

    newProduct= f"{shoe_type},{ brand},{ qty},{ cost_price*2},{ origin}\n"  
    # Open in append mode 
    try:                                              
        with open("inventory.txt", "a") as file:      #opening inventory.txt in append mode
            file.write(newProduct)                    #add new product detail in iventory
            print("New product added to inventory")
    except FileNotFoundError:
        print("\nError !!! file not found")
#generate bill on a file
    filename = f"restock_invoice_{supplier}.txt"
    with open(filename, "w") as file:
        file.write("================ New shoe stock ================\n")
        file.write(f"Vendor: {supplier}\n")
        file.write(f"Date: {datetime.datetime.now()}\n")
        file.write("=================================================\n")
        file.write(f"{'Shoe':<15}{'Brand':<10}{'Qty':<8}{'Rate':<8}{'Total'}\n")
        file.write("=================================================\n")
        file.write(f"{shoe_type:<15}{brand:<10}{qty:<8}{cost_price:<8}{qty*cost_price}\n")
        file.write("-------------------------------------------------\n")
        file.write(f"Grand Total:\t{cost_price*qty}\n")
        file.write("=================================================\n")

    print(" New stock invoice generated:", filename)
# Updating stock add product
def restock_product():
    """ restock existing product or add new porduct"""
    products =load_products()    #reads inventory.txt
    if not products:             #check if file is empty
        return
    supplier=input("enter name of vender / supplier: ")   #ask for supplier name
    if supplier.strip() == "":                            #check if the input is empty
        print("Supplier name cannot be empty")
        return
    invoices=[]
    # restock=0
    display()                           #display shoes
    while(True):                        #infinite loop until manually broken
        choice = input("Enter shoe type to buy or 'NEW' to add new product or 'DONE' to go to main menu:")
        if choice.strip().lower()=="done":
            break
        if choice.strip().lower()=="new":
            addNewProduct(supplier)     #call add new product function to add new product to stock
            return
        found=False
        #ask user for shoe name, qunatity and price 
        for product in products:
            shoeType=product[0]
            brand=product[1]
            qty=int(product[2])
            if shoeType.strip().lower() == choice.lower():
                try:                        #handles value error exception
                    add_qty = int(input("Enter quantity:"))
                    pricePerUnit = float(input("Enter price:"))
                    if add_qty <= 0: 
                        print("Quantity must be greater than zero")
                        continue
                    if pricePerUnit <= 0:   
                        print("Price must be greater than zero")
                        continue
                except ValueError:
                    print("quantity and price values must be numeric")
                    continue
                product[2] = str(qty + add_qty)
                print(f"{add_qty} units of {shoeType} restocked successfully!")
                total_price=add_qty*pricePerUnit
                invoices.append([shoeType,brand,add_qty,pricePerUnit, total_price])
                found=True
                break
        if not found:
            print("item not found in inventory")
    update_inventory(products)  #save updated list to inventory.txt
#generate bill as an invoice in a in fil
    if found:
        now = datetime.datetime.now()
        filename = f"restock_invoice_{supplier}.txt"
        with open(filename, "w") as file:
            file.write("============ Vendor Restock Invoice ============\n")
            file.write(f"Vendor: {supplier}\n")
            file.write(f"Date: {now}\n")
            file.write("=================================================\n")
            file.write(f"{'Shoe':<15}{'Brand':<10}{'Qty':<8}{'Rate':<8}{'Total'}\n")
            file.write("=================================================\n")

            grand_total = 0
            for r in invoices:
                shoe, brand, qty, rate, subtotal = r
                file.write(f"{shoe:<15}{brand:<10}{qty:<8}{rate:<8}{subtotal}\n")
                grand_total += subtotal

            file.write("-------------------------------------------------\n")
            file.write(f"Grand Total:\t{grand_total}\n")
            file.write("=================================================\n")

        print(" Restock invoice generated:", filename)

def exit_program():
    """exits the main loop (ends the program)"""
    print("\nThank you for shopping!!!\n")
    

while True:
    print("\n")
    print("""
╔══════════════════════════════════════╗
║          Welcome to Speedz Shoes     ║
╠══════════════════════════════════════╣
║  1. Display Products                 ║
║  2. Purchase Products                ║
║  3. Restock Products                 ║
║  4. Exit                             ║
╚══════════════════════════════════════╝
""")
    try:                                            #make sure the input is only an integer
        num=int(input("enter 1 ,2 ,3 or 4 :"))
    except ValueError:
        print("Error !!! you can only enter an integer from 1 to 4")
        continue        #re-run the loop
    if num==1:
        display()      #call display method
    elif num==2:
        purchase_Product()  #call purchase product method
    elif num==3:
        restock_product()   #call restock product method
    elif num==4:
        exit_program()      #call exit program method
        break
    else:
        print("Enter an interger :1 , 2 ,3 or 4") 

