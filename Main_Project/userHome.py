import os
import re
import time
from tabulate import tabulate
import conn
from datetime import datetime
from dateutil.relativedelta import relativedelta

current_date = datetime.now()

class UserHome:

    balance=0

    def __init__(self,plan,username,firstname):
        self.plan=plan
        self.username=username
        self.firstname=firstname
        UserHome.mainmenu(self)

    def fav_books(self):
        while True:
            print("""\n                                                     
                                                -------------------------
                                                        SAVED BOOKS 
                                                -------------------------      
                   """)
            conn.login.execute('SELECT b.bookid, b.book_name, a.author_name, g.genre_name, b.coins, b.rating, b.days FROM favouritebooks f JOIN book b ON '
                     'f.bookid = b.bookid JOIN author a ON b.authorid = a.authorid JOIN '
                     'genre g ON b.genreid = g.genreid WHERE f.username =%s',(self.username,))
            query_result = conn.login.fetchall()
            # Checks if there are any results returned by the query.
            if query_result:
                print(
                    # Uses the tabulate function from the tabulate library to format the query results into a table.
                    tabulate(query_result,
                             headers=["BookId", "Book Name", "Author Name", "Genre Name", "Coins", "Rating", "Days"]))
                print(f"""\n                                            
                                                     Choose an option :
                                                      1.Buy 
                                                      2.Remove
                                                      3.Go Back""")
                choice = input("""                Enter a number from above list : """)
                if choice == '3':
                    print("Back to Previous Menu")
                    break
                while True:
                    bookid = input("Enter the book Id to do actions: ")
                    if " " not in bookid:
                        conn.login.execute("SELECT * FROM book WHERE bookid = %s", (int(bookid),))
                        result = conn.login.fetchone()
                        if result:
                            break  # Book ID exists, break the loop
                        else:
                            print("INVALID!!! Book ID does not exist. Please enter a valid book ID.")
                    else:
                        print("INVALID!!! Book ID should not contain spaces.")

                if choice == '1':
                    UserHome.buy(self,bookid)
                elif choice == '2':
                    conn.login.execute("DELETE FROM favouritebooks WHERE bookid = %s", (int(bookid),))
                    conn.databaseobj.commit()
                else:
                    print("Invalid choice")

            else:
                print("No Saved Books.")
                break

    def available_book(self):
        print("""\n                                                     
                                            ----------------------------------
                                              CURRENTLY AVAILABLE RENT BOOKS 
                                            ----------------------------------      
                """)
        query = 'SELECT b.bookid, b.book_name, a.author_name, g.genre_name, b.coins, b.rating, b.days FROM book b JOIN author a ON b.authorid = a.authorid JOIN genre g ON b.genreid = g.genreid'
        conn.login.execute(query)
        query_result = conn.login.fetchall()
        # Checks if there are any results returned by the query.
        if query_result:
            print(
                # Uses the tabulate function from the tabulate library to format the query results into a table.
                tabulate(query_result,
                         headers=["BookId", "Book Name", "Author Name", "Genre Name", "Coins", "Rating", "Days"]))
            while True:
                print(f"""\n                                            
                                                     Choose an option :
                                                      1.Buy 
                                                      2.Save
                                                      3.Go Back""")
                choice = input("""                Enter a number from above list : """)
                if choice == '3':
                    print("Back to Previous Menu")
                    break
                while True:
                    bookid = input("Enter the book Id to do actions: ")
                    if " " not in bookid:
                        conn.login.execute("SELECT * FROM book WHERE bookid = %s", (int(bookid),))
                        result = conn.login.fetchone()
                        if result:
                            break  # Book ID exists, break the loop
                        else:
                            print("INVALID!!! Book ID does not exist. Please enter a valid book ID.")
                    else:
                        print("INVALID!!! Book ID should not contain spaces.")

                if choice == '1':
                    UserHome.buy(self, bookid)
                elif choice == '2':
                    conn.login.execute("SELECT * FROM favouritebooks WHERE bookid = %s and username=%s", (int(bookid),self.username))
                    result = conn.login.fetchone()
                    if result:
                        print("Already Saved!!")
                    else:
                        conn.login.execute("INSERT INTO favouritebooks(bookid,username) VALUES (%s,%s)", (int(bookid),self.username))
                        conn.databaseobj.commit()
                else:
                    print("Invalid choice")
        else:
            print("The book is empty.")

    def buy(self,bookid):
        conn.login.execute("SELECT * FROM rentbooks WHERE bookid = %s and username=%s",(int(bookid), self.username))
        result = conn.login.fetchone()
        if result:
            print("Already Bought!!")
        else:
            conn.login.execute("SELECT coins FROM book WHERE bookid = %s",(int(bookid),))
            result1 = conn.login.fetchone()
            conn.login.execute("SELECT balance,validitydate FROM user WHERE username = %s", (self.username,))
            result2 = conn.login.fetchone()
            if result2 and result2[1]:
                balance = float(result2[0]) - float(result1[0])
                validity_date = datetime.strptime(result2[1], "%d-%m-%Y")
                # checking if the validitydate has not expired:
                if validity_date >= current_date:
                    dayc = int(self.plan) * 10
                    while True:
                        confirm = input(f"Extra Day Count: {dayc} days as per plan. Need to add or not (Y/N): ").upper()
                        if confirm == 'Y':
                            while True:
                                confirm = input(" Confirming Need to add more days or not (Y/N): ").upper()
                                print("Resultant coins will be rejected from balance = no of days * 2coins")
                                if confirm == 'Y':
                                    adddays = int(input("\nEnter the no of days to add: "))
                                    balance = balance - (adddays*2)
                                    dayc = dayc + adddays
                                    break
                                elif confirm == 'N':
                                    print("Fear ayo..")
                                    break
                                else:
                                    print("Invalid input. Please enter 'Y' or 'N'.")
                            break
                        elif confirm == 'N':
                            print("Wow!!")
                            break
                        else:
                            print("Invalid input. Please enter 'Y' or 'N'.")
                    if balance >= 0:
                        enddate = current_date + relativedelta(days=int(dayc))
                        conn.login.execute(
                            "INSERT INTO rentbooks(bookid, username, startdate, enddate) VALUES (%s, %s, %s, %s)",
                            (int(bookid), self.username, current_date.strftime("%d-%m-%Y"), enddate.strftime("%d-%m-%Y"))
                        )
                        conn.databaseobj.commit()
                        conn.login.execute("UPDATE user SET balance = %s WHERE username = %s",(int(balance),self.username))
                        conn.databaseobj.commit()
                    else:
                        print("Insufficient Balance...!!!")
                else:
                    print("The user's validity date has expired.Recharge!!")
            else:
                print("Invalid user or no validity date found.")

    def view_rent_book(self):
        print("""\n                                                     
                                                        -------------------------
                                                            VIEW RENTED BOOKS 
                                                        -------------------------      
                           """)

        conn.login.execute('SELECT b.bookid, b.book_name, a.author_name, g.genre_name, b.coins, b.rating, r.startdate, r.enddate '
            'FROM rentbooks r JOIN book b ON r.bookid = b.bookid JOIN author a ON b.authorid = a.authorid JOIN genre g ON b.genreid = g.genreid '
            'WHERE r.username = %s AND STR_TO_DATE(r.enddate, "%d-%m-%Y") >= CURRENT_DATE',(self.username,))
        query_result = conn.login.fetchall()
        # Checks if there are any results returned by the query.
        # If query_result is not empty (i.e., there are phonebook entries), the if block is executed.
        if query_result:
            print(
                # Uses the tabulate function from the tabulate library to format the query results into a table.
                # The headers for the table are specified as "Phone_id", "Name", "Number", "Address", "Email id."
                tabulate(query_result,
                         headers=["BookId", "Book Name", "Author Name", "Genre Name", "Coins", "Rating", "Start Date","End Date"]))
            while True:
                book_id = input("Enter the book id to view: ")
                conn.login.execute("SELECT b.file_name FROM rentbooks r "
                                   "JOIN book b ON r.bookid = b.bookid WHERE r.username = %s;", (self.username,))
                result = conn.login.fetchone()
                if book_id == "":
                    print("This book id field cannot be empty.")
                elif book_id.isalpha():
                    print("Enter only number here")
                elif result is None:
                    print("Bookid is not found!!")
                else:
                    break
            os.chdir("D:\\Tinupy\\camp4\\mp\\books")
            print("Opening", end="")
            for _ in range(7):
                time.sleep(0.3)
                print(".", end="")
            time.sleep(1)
            os.startfile(result[0])
        else:
            print("No Rented Books. Explore!!")
    def accountSub(self):
        conn.login.execute("SELECT  p.plan_name,u.balance, u.validitydate FROM user u "
                           "JOIN plan p ON u.planid = p.planid WHERE u.username = %s;",(self.username,))
        result = conn.login.fetchone()
        print("""\n    
                                              ------------------
                                                 COIN BALANCE
                                              ------------------      
                          """)
        print("Plan Name:",result[0])
        print("Balance:",result[1])
        print("Validity Date:",result[2])
        print("Extra Days to Read Count:", int(self.plan) * 10)

    def book_review(self):
        print("""\n                                                     
                                                                -------------------------
                                                                    ADD BOOK REVIEWS 
                                                                -------------------------      
                                   """)

        conn.login.execute(
            'SELECT b.bookid, b.book_name, a.author_name, g.genre_name, b.coins, b.rating '
            'FROM rentbooks r JOIN book b ON r.bookid = b.bookid JOIN author a ON b.authorid = a.authorid JOIN genre g ON b.genreid = g.genreid '
            'WHERE r.username = %s', (self.username,))
        query_result = conn.login.fetchall()
        # Checks if there are any results returned by the query.
        # If query_result is not empty (i.e., there are phonebook entries), the if block is executed.
        if query_result:
            print(
                # Uses the tabulate function from the tabulate library to format the query results into a table.
                # The headers for the table are specified as "Phone_id", "Name", "Number", "Address", "Email id."
                tabulate(query_result,
                         headers=["BookId", "Book Name", "Author Name", "Genre Name", "Coins", "Rating"]))
            while True:
                book_id = input("Enter the book id: ")
                conn.login.execute("SELECT b.file_name FROM rentbooks r "
                                   "JOIN book b ON r.bookid = b.bookid WHERE r.username = %s;", (self.username,))
                result = conn.login.fetchone()
                if book_id == "":
                    print("This book id field cannot be empty.")
                elif book_id.isalpha():
                    print("Enter only number here")
                elif result is None:
                    print("Book id is not found!!")
                else:
                    break
            while True:
                rating = input("Enter the rating out of 10: ")
                if rating == "":
                    print("This rating field cannot be empty.")
                elif rating.isalpha():
                    print("Enter only number here")
                elif int(rating) > 10:
                    print("Rating is greater than 10")
                else:
                    break
            while True:
                review = input("Enter the review: ")
                if review == "":
                    print("This rating field cannot be empty.")
                elif review.isdigit():
                    print("Number not allowed")
                else:
                    break
            conn.login.execute("insert into bookreview values(%s,%s,%s,%s)", (review,int(rating),int(book_id),self.username))
            conn.databaseobj.commit()
            conn.login.execute('SELECT AVG(r.rating) FROM bookreview r WHERE r.bookid = %s', (int(book_id),))
            average_rating = conn.login.fetchone()[0]

            # Update the book table with the calculated average rating
            conn.login.execute('UPDATE book SET rating = %s WHERE bookid = %s', (average_rating, int(book_id)))
            conn.databaseobj.commit()
            print("Thanks for giving review\nHave a nice day!!!")


    def enquiry(self):
        while True:
            print("""\n                                          --------------------------
                                                 MANAGE ENQUIRIES 
                                          --------------------------      
                       Choose an option :
                      1.Add Enquiry
                      2.View all Enquiry
                      3.Remove Enquiry  
                      4.Go Back""")
            choice = input("""                Enter a number from above list : """)

            if choice == '1':
                UserHome.add_enquiry(self)
            elif choice == '2':
                UserHome.viewd_enquiry(self)
            elif choice == '3':
                UserHome.viewd_enquiry(self,1)
            elif choice == '4':
                break
            else:
                print("Invalid choice")


    def viewd_enquiry(self,d=0):
        print("""\n                                                     
                                                                --------------------------
                                                                   VIEW ENQUIRY HISTORY 
                                                                --------------------------      
                                      """)
        query = 'select enquiry_id, subject, description, enquiry_date, response from enquiry where username=%s'
        conn.login.execute(query,(self.username,))
        query_result = conn.login.fetchall()
        # Checks if there are any results returned by the query.
        if query_result:
            formatted_result = (
                (enquiry_id, subject, description, enquiry_date, response if response else "Processing..")
                for enquiry_id, subject, description, enquiry_date, response in query_result
            )
            print(
                # Uses the tabulate function from the tabulate library to format the query results into a table.
                tabulate(formatted_result, headers=["Enquiry_id", "Subject", "Description", "Enquiry_date","Response"]))
            if d==1:
                while True:
                    c=input("Do u want to delete or not:(Y/N) ").upper()
                    if c=='Y':
                        while True:
                            id=input("Enter the Enquiry id: ")
                            conn.login.execute("SELECT * FROM enquiry WHERE username = %s and enquiry_id=%s",(self.username,int(id)))
                            result = conn.login.fetchone()
                            if id == "":
                                print("This enquiry id field cannot be empty.")
                            elif id.isalpha():
                                print("Enter only number here")
                            elif result is None:
                                print("Enquiry id  is not found!!")
                            else:
                                break
                        query = 'delete from enquiry where username=%s and enquiry_id=%s'
                        conn.login.execute(query, (self.username,int(id)))
                        conn.databaseobj.commit()
                        print("\nDeleted successfully")
                        break
                    elif c=='N':
                        print("Thanks for the confirmation...")
                        break
                    else:
                        print("Invalid choice")

        else:
            print("No enquiries found.")
    def add_enquiry(self):
        while True:
            subject = input("Enter the subject to enquiry: ")
            if not subject=="":
                break
            else:
                print("This subject field cannot be empty.")
        while True:
            description = input("Enter the description: ")
            if not description=="":
                break
            else:
                print("This description field cannot be empty.")
        conn.login.execute("insert into enquiry(subject, description, username, enquiry_date) values(%s,%s,%s,%s)"
                           ,(subject, description, self.username, current_date.strftime("%d-%m-%Y")))
        conn.databaseobj.commit()
        print("\nInserted successfully")


    def mainmenu(self):
        while True:
            print(f"""\n               
                                          --------------------------
                                               WELCOME {self.firstname} 
                                          --------------------------      
                       Choose an option :
                      1.Favourite Books 
                      2.View all Read Books
                      3.Available Rent Books 
                      4.My Subscription
                      5.Book Review
                      6.Enquiry
                      7.Sign Out""")
            choice = input("""                Enter a number from above list : """)

            if choice == '1':
                UserHome.fav_books(self)
            elif choice == '2':
                UserHome.view_rent_book(self)
            elif choice == '3':
                UserHome.available_book(self)
            elif choice == '4':
                UserHome.accountSub(self)
            elif choice == '5':
                UserHome.book_review(self)
            elif choice == '6':
                UserHome.enquiry(self)
            elif choice == '7':
                print("Successfully logged out",end="")
                for _ in range(5):
                    time.sleep(0.3)
                    print(".", end="")
                time.sleep(0.5)
                print("Back to Login")
                break
            else:
                print("Invalid choice")


class UserLogin:
    def login(self):
        while True:
            userid = input("Enter the user id : ")
            if userid == "":
                print("This field cannot be empty.")
            else:
                break
        while True:
            password = input("Enter the password : ")
            if password == "":
                print("This field cannot be empty.")
            else:
                break
        select_query = """SELECT u.planid,u.username,u.first_name FROM login l JOIN user u ON l.username = u.username WHERE l.username = %s COLLATE utf8mb4_bin 
            AND l.password = %s COLLATE utf8mb4_bin AND l.role = 'user'"""
        conn.login.execute(select_query, (userid, password))
        result = conn.login.fetchone()
        if result != None:
            print("Logging",end="")
            for _ in range(7):
                time.sleep(0.3)
                print(".", end="")
            time.sleep(0.5)
            print("""\n\n
                        ----------------------------Successfully Logged In----------------------------
                  """)
            UserHome(result[0], result[1], result[2])
        else:
            print("Incorrect userid or password!!!... :-(")


    def register(self):
        while True:
            try:
                global userid, vdate
                print("Register your details here. ")
                while True:
                    first_name = input("Enter the first name : ")
                    if re.fullmatch("[A-Za-z]{2,25}", first_name):
                        break
                    else:
                        print("INVALID!!!Enter only alphabets of length 2 to 25.")
                while True:
                    last_name = input("Enter the last name : ")
                    if re.fullmatch("[A-Za-z]{1,25}", last_name):
                        break
                    else:
                        print("INVALID!!!Enter only alphabets of length 1 to 25.")
                while True:
                    userid = input("Create an user name : ")
                    if " " not in userid:
                        if re.fullmatch(r'^(?=.*[A-Za-z])(?=.*\d).{6,16}$', userid):
                            break
                        else:
                            print("INVALID!!!Should be an alpha-numeric character "
                                  "of length 6 to 25.")
                    else:
                        print("INVALID!!!UserId should not contain space...")
                while True:
                    password = input("Enter the password : ")
                    if " " not in password:
                        if re.fullmatch(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%^&+!_]).{6,16}$', password):
                            break
                        else:
                            print("""The password should contain atleast 
                            -a capital letter
                            -a small letter 
                            -a number
                            -a special character [ @ # $ % ^ & + ! _ ]
                            Also should contain minimum length of 6 characters to maximum 16 characters.""")
                    else:
                        print("INVALID!!!password should not contain space...")
                while True:
                    email = input("Enter the email Address : ")
                    if " " not in email:
                        if re.fullmatch(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                            break
                        else:
                            print("INVALID!!! Please enter a valid email address.")
                    else:
                        print("INVALID!!! Email should not contain spaces.")
                while True:
                    phone_no = input("Enter the phone number: ")
                    if " " not in phone_no:
                        if re.fullmatch(r'^\+?[6-9]\d{1,10}$', phone_no):
                            break
                        else:
                            print("INVALID!!! Please enter a valid phone number.")
                    else:
                        print("INVALID!!! Phone number should not contain spaces.")

                query = 'SELECT planid, plan_name, description, duration, price, coins FROM plan'
                conn.login.execute(query)
                query_result = conn.login.fetchall()
                # Checks if there are any results returned by the query.
                if query_result:
                    print(
                        # Uses the tabulate function from the tabulate library to format the query results into a table.
                        tabulate(query_result,
                                 headers=["PlanId", "Plan_name", "Description", "Duration", "Price", "Coins"]))
                else:
                    print("The plan is empty.")

                while True:
                    planid = input("Enter plan id : ")
                    if " " not in planid:
                        conn.login.execute('select * from plan where planid=%s',(int(planid),))
                        planid_checker = conn.login.fetchone()
                        if planid_checker:
                            break
                        else:
                            print("Plan Id is not Found")
                    else:
                        print("INVALID!!!Plan Id should not contain space...")

                print("Confirming to plan",planid_checker[1], end="")
                for _ in range(7):
                    time.sleep(0.3)
                    print(".", end="")

                l_insert_query = "insert into login(username,password,role)" \
                                 "values(%s,%s,'user')"
                conn.login.execute(l_insert_query, (userid, password))
                conn.databaseobj.commit()

                print(f"""\n                
                                       Choose an Payment method :
                                      1.Credit Card
                                      2.UPI ID
                                      3.Back to Login""")
                choice = input("""                Enter a number from above list : """)

                if choice == '1':
                    while True:
                        holder_name = input("Enter the Card Holder Name: ")
                        if holder_name.isalpha():  # Check if the name contains only alphabets
                            break
                        else:
                            print("Invalid name. Please enter a valid name using only letters.")

                    while True:
                        credit_no = input("Enter the Credit Card Number: ")
                        if credit_no.isdigit() and len(credit_no) == 16:  # Check if the card number is 16 digits
                            break
                        else:
                            print("Invalid card number. Please enter a 16-digit number.")

                    while True:
                        cvv = input("Enter the CVV: ")
                        if cvv.isdigit() and len(cvv) == 3:  # Check if the CVV is 3 digits
                            break
                        else:
                            print("Invalid CVV. Please enter a 3-digit number.")
                    conn.login.execute('insert into bill(name,bill_date,mode,planid,username) values(%s,%s,%s,%s,%s)',(holder_name,current_date.strftime("%d-%m-%Y"),'Credit Card',planid,userid))
                    conn.databaseobj.commit()

                elif choice == '2':
                    while True:
                        upi_id = input("Enter the UPI Id: ")
                        # Regex to validate UPI ID
                        if re.match(r'^[a-zA-Z0-9.\-_]{2,}@[a-zA-Z]{2,}$', upi_id):
                            name = upi_id.split('@')[0]
                            break
                        else:
                            print("Invalid UPI ID. Please enter a valid UPI ID (e.g., yourname@bank).")
                    conn.login.execute('insert into bill(name,bill_date,mode,planid,username) values(%s,%s,%s,%s,%s)',(name,current_date.strftime("%d-%m-%Y"),'UPI',planid,userid))
                    conn.databaseobj.commit()

                elif choice == '3':
                    print("Back to Login")
                    break

                else:
                    print("Invalid choice")

                print("Payment processing...", end="")
                for _ in range(7):
                    time.sleep(0.3)
                    print(".", end="")
                print("\nPayed Successfully")

                if planid_checker[3] == "3M":
                    vdate = current_date + relativedelta(months=3)
                if planid_checker[3] == "6M":
                    vdate = current_date + relativedelta(months=6)
                if planid_checker[3] == "1Y":
                    vdate = current_date + relativedelta(years=1)
                if planid_checker[3] == "2Y":
                    vdate = current_date + relativedelta(years=2)
                u_insert_query = "insert into user(username, first_name, last_name, email_id, phone_number, planid, balance, validitydate)" \
                                 "values(%s,%s,%s,%s,%s,%s,%s,%s)"
                conn.login.execute(u_insert_query, (userid, first_name, last_name, email, phone_no, planid, int(planid_checker[5]),vdate.strftime("%d-%m-%Y")))
                conn.databaseobj.commit()
                print("\nYou have successfully registered!!!...:)")
                break
            except Exception as e:
                print(e)
                print("User Id already exist!!")
    def main(self):
        while True:
            print("""    
                                      ------------------------------------------
                                         WELCOME TO ONLINE LIBRARY MANAGEMENT
                                      ------------------------------------------      
                  ->Choose an option :
                  1.Login
                  2.New User? Register Here
                  3.Exit""")
            number = input("Enter a number from above list : ")
            if number == "1":
                UserLogin.login(self)
            elif number == "2":
                UserLogin.register(self)
            elif number == "3":
                print("""        
                ----------------------------
                Thanks for using this application :)
                ---------------------------
                """)
                break
            else:
                print("invalid!!! Enter numbers from 1 to 3 only...")


obj = UserLogin()
obj.main()