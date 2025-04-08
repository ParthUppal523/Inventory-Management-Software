import mysql.connector
connector=mysql.connector.connect(host="localhost", user="root", password="abcd@12345", database="CarManufacturers")
cursor=connector.cursor()


print("""Hello!
Welcome to  ABC Corporation 

\t 'Automotive Parts Just A Click Away'\n""")
uname=input("Enter Username: ")
pwd=input("Enter Password: ")
Choice="YES"
def CommonInputs():
    global make, model, modelyr, variant, part
    make=input("Enter Make: ")
    model=input("Enter Model: ")
    modelyr=input("Enter Model Year: ")
    variant=input("Enter Variant: ")
    part=input("Enter name of part: ")

def Purchase():
    global Choice
    while Choice=="YES":
        CommonInputs()
        qty=int(input("Enter quantity of the part selected to be purchased: "))
        s=f"SELECT * FROM {make} WHERE Model=%s AND Variant=%s AND Part=%s"
        t=(model, variant, part)
        cursor.execute(s,t)
        result=cursor.fetchall()
        print("Model", "Variant", "Part", "Quantity", "Unit Price", sep="\t ")
        for i in result:
            a, b, c, d, e=i
            print( a, b, c, d, e, sep="\t ")
            if qty <= d:
                print("Required quantity for ", part," of ", make, model, variant, modelyr, " is available as of now.")
                ans=input("Do you want to place order (Yes/No): ")
                choice=ans.upper()
                if choice=="YES":
                    amount=1.18*e*qty
                    print("Total Billing Amount: ",amount)
                    address=input("Please Enter Shipping/Billing Address: ")
                    print("""Thank you for placing the order.
Details of the order will be sent to your registered E-mail address.""")
                    up_qty_query=f"UPDATE {make} SET Qty=%s WHERE Model=%s AND Variant=%s AND Part=%s"
                    up_qty = d - qty
                    up_data = (up_qty, model, variant, part)
                    cursor.execute(up_qty_query, up_data)
                elif choice=="NO":
                    print("""Thank you.
Have a good day.""")
            else:
                print(d," quantity for ", part," of ", make, model, modelyr, variant, " is available as of now.")
                ans=input("Do you want to place order (Yes/No): ")
                choice=ans.upper()
                if choice=="YES":
                    newqty=int(input("Enter quantity to be purchased: "))
                    amount=1.18*e*newqty
                    print("Total Billing Amount: ",amount)
                    address=input("Please Enter Shipping/Billing Address: ")
                    print("""Thank you for placing the order.
Details of the order will be sent to your registered E-mail address.""")
                    up_qty_query=f"UPDATE {make} SET Qty=%s WHERE Model=%s AND Variant=%s AND Part=%s"
                    up_qty = d - newqty
                    up_data=(up_qty, model, variant, part)
                    cursor.execute(up_qty_query, up_data)
                elif choice=="NO":
                    print("""Thank you.
Have a good day.""")
        connector.commit()
        Answer=input("Do you want to proceed?: ")
        Choice=Answer.upper()

def CheckQuantity():
    s=f"SELECT * FROM {make} WHERE Model=%s AND Variant=%s AND Part=%s"
    t=(model, variant, part)
    cursor.execute(s,t)
    result=cursor.fetchall()
    print("Model", "Variant", "Part", "Quantity", "Unit Price", sep="\t ")
    for i in result:
       a, b, c, d, e=i
       print(a, b, c, d, e, sep="\t ")
    
if uname=="User" and pwd=="user":
    Purchase()            

elif uname=="Admin" and pwd=="admin":
    Choice="YES"
    while Choice=="YES":
        ans=int(input("""What do you want to do:
1. Purchase
2. Check the quantity
3. Update Stock
4. Exit\n"""))
        if ans==1:
            cname=input("Enter name of Customer: ")
            Purchase()
        
        elif ans==2:
            CommonInputs()
            CheckQuantity()
        
        elif ans==3:
            CommonInputs()
            sql_query=f"SELECT * FROM {make} WHERE Model=%s AND Variant=%s AND Part=%s"
            Data=(model, variant, part)
            cursor.execute(sql_query, Data)
            result=cursor.fetchall()
            print("Model", "Variant", "Part", "Quantity", "Unit Price", sep="\t ")
            for i in result:
                a, b, c, d, e=i
                print( a, b, c, d, e, sep="\t ")
            Ans=int(input("""What would you like to do:
1. Add new part
2. Delete a part
3. Update quantity
4. Update price"""))
            if Ans==1:
                CommonInputs()
                Quantity=int(input("Enter available quantity: "))
                Price=float(input("Enter price for the part: "))
                query=f"INSERT INTO {make} VALUES(%s, %s, %s, %s, %s)"
                data=(model, variant, part, Quantity, Price)
                cursor.execute(query, data)
                print("Added Part Successfully.")
                connector.commit()
                
            elif Ans==2:
                CommonInputs()
                del_query=f"DELETE FROM {make} WHERE Model=%s AND Variant=%s AND Part=%s"
                data==(model, variant, part)
                cursor.execute(del_query, data)
                print("Selected Part '", part,"' has been successfully deleted")
                connector.commit()
                
            elif Ans==3:
                CommonInputs()
                N_Qty=int(input("Enter new quantity: "))
                update_query=f"UPDATE {make} SET Qty=%s WHERE Model=%s AND Variant=%s AND Part=%s"
                data=(N_Qty, model, variant, part)
                cursor.execute(update_query, data)
                print("Quantity for the selected part '", part,"' has been successfully updated to: ",N_Qty)
                connector.commit()

            elif Ans==4:
                CommonInputs()
                N_Price=float(input("Enter new unit price: "))
                update_query=f"UPDATE {make} SET Price=%s WHERE Model=%s AND Variant=%s AND Part=%s"
                data=(N_Price, model, variant, part)
                cursor.execute(update_query, data)
                print("Price for the selected part '", part,"' has been successfully updated to: ",N_Price)
                connector.commit()
                
        elif ans==4:
            print("""Thank you.
Have A Good Day""")

        Answer=input("Want to proceed further? : ")
        Choice=Answer.upper()

else:
    print("Please check username and password.")
