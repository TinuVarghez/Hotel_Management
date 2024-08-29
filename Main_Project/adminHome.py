import conn
from tabulate import tabulate


class AdminHome:

    def __init__(self):
        AdminHome.mainmenu(self)

    # view contacts
    def view_members(self):
        query = 'SELECT u.username,u.first_name,u.last_name,u.email_id,u.phone_number,l.password FROM user u join login l where u.username=l.username and l.role="user"'
        conn.login.execute(query)
        query_result = conn.login.fetchall()
        # Checks if there are any results returned by the query.
        # If query_result is not empty (i.e., there are phonebook entries), the if block is executed.
        if query_result:
            print(
                # Uses the tabulate function from the tabulate library to format the query results into a table.
                # The headers for the table are specified as "Phone_id", "Name", "Number", "Address", "Email id."
                tabulate(query_result,
                         headers=["Username", "First_name", "Last_name", "Email_id", "PhoneNumber", "Password"]))
        else:
            print("The members is not found.")

    def ag(self, status, a=0 , m=0):
        while True:  # Keep the function in a loop to handle multiple actions in one go
            if m == 1:
                print(f"""\n                                          
                                                          --------------------------
                                                                 MANAGE {status.title()}s 
                                                          -------------------------- 
                            """)
            query = 'select * from {}'.format(status)
            conn.login.execute(query)
            query_result = conn.login.fetchall()

            if query_result:
                print(tabulate(query_result, headers=["{}id".format(status), "{}_name".format(status)]))
            else:
                print(f"The {status} table is empty.")

            print(f"""              
                                    1. Add {status.title()}
                                    2. Update {status.title()} Name
                                    3. Go Back""")
            if a == 1:
                print(f"""                                    4. Update {status.title()} In Book
                                  """)
            if m == 1:
                print(f"""                                    4. Remove {status.title()}
                                  """)
            choice = input("Enter the choice: ")

            if choice == '1':
                id = input(f"Enter the new {status} ID: ")
                name = input(f"Enter the new {status} Name: ")
                query = 'insert into {} values(%s,%s)'.format(status)
                conn.login.execute(query, (int(id), name))
                conn.databaseobj.commit()
                print(f"{status} details have been added.")

            elif choice == '2':
                id = input(f"Enter the {status} ID to update: ")
                name = input(f"Enter the {status} Name: ")
                query = f'update {status} set {status}_name=%s where {status}id=%s'
                conn.login.execute(query, (name, int(id)))
                conn.databaseobj.commit()
                print(f"{status} details have been updated successfully.")

            elif choice == '3':
                print("\nBack to the previous menu.")
                break  # Exit the loop to go back

            elif choice == '4' and a == 1:
                bookid = input(f"Enter the Book ID to update the {status} details: ")
                id = input(f"Enter the {status} ID to insert: ")
                query = f'update Book set {status}id=%s where bookid=%s'
                conn.login.execute(query, (int(id), int(bookid)))
                conn.databaseobj.commit()
                break

            elif choice == '4' and m == 1:
                id = input(f"Enter the {status} ID to remove from {status} details: ")
                query = f'delete from {status} where {status}id=%s'
                conn.login.execute(query, (int(id),))
                conn.databaseobj.commit()
                print(f"{status} details have been removed successfully.")

            else:
                print("Invalid choice. Please enter a valid option.")

    def manage_book(self):
        while True:
            print("""\n                                          --------------------------
                                                 MANAGE BOOKS 
                                          --------------------------      
                       Choose an option :
                      1.Add a new book
                      2.Update an existing book
                      3.View all books
                      4.Remove a book
                      5.Go Back""")
            choice = input("""                Enter a number from above list : """)

            if choice == '1':
                AdminHome.add_book(self)
            elif choice == '2':
                AdminHome.update_book(self)
            elif choice == '3':
                print("""\n                                                     
                                                        --------------------------
                                                              CURRENT BOOKS 
                                                        --------------------------      
                      """)
                AdminHome.view_book(self)
            elif choice == '4':
                AdminHome.delete_book(self)
            elif choice == '5':
                AdminHome()
            else:
                print("Invalid choice")

    def view_book(self):
        query = 'SELECT b.bookid, b.book_name, a.author_name, g.genre_name, b.coins, b.rating , b.days, b.file_name FROM book b JOIN author a ON b.authorid = a.authorid JOIN genre g ON b.genreid = g.genreid'
        conn.login.execute(query)
        query_result = conn.login.fetchall()
        # Checks if there are any results returned by the query.
        # If query_result is not empty (i.e., there are phonebook entries), the if block is executed.
        if query_result:
            print(
                # Uses the tabulate function from the tabulate library to format the query results into a table.
                # The headers for the table are specified as "Phone_id", "Name", "Number", "Address", "Email id."
                tabulate(query_result,
                         headers=["BookId", "Book Name", "Author Name", "Genre Name", "Coins", "Rating", "Days","File_Name"]))

        else:
            print("The book is empty.")

    def update_book(self):
        headers = ["BookId", "Book_Name", "Author Name", "Genre Name", "Coins", "Rating", "Days","File_Name"]
        while True:
            print("""\n                                                      --------------------------
                                                        UPDATE CURRENTLY BOOKS 
                                                      -------------------------- """)
            AdminHome.view_book(self)
            print("""                                               
                                   Choose an option :
                                  1.Continue Updating 
                                  2.Go Back""")
            choice = input("""                Enter a number from above list : """)
            if choice == '1':
                index = int(input("Enter the Column no of the Table to Update: "))
                if headers[index - 1] == "Author Name":
                    AdminHome.ag(self, "author", 1)
                elif headers[index - 1] == "Genre Name":
                    AdminHome.ag(self, "genre", 1)
                elif headers[index - 1] != "Author Name" or headers[index - 1] != "Genre Name":
                    bookid = input(f"Enter the Book ID to update the {headers[index - 1]}: ")
                    value = input(f"Enter the {headers[index - 1]} to update: ")
                    conn.login.execute(f"Update book set {headers[index - 1]}=%s where bookid=%s", (value, int(bookid)))
                    conn.databaseobj.commit()
                else:
                    print("Invalid number")
                print(f"{headers[index - 1]} updated successfully!!!\n")
            if choice == '2':
                break

    def add_book(self):
        try:
            book_name = input("Enter the Book Name")
            if book_name == "":
                raise Exception("This Book Name field cannot be empty !!")
            AdminHome.ag(self, "author")
            authorid = input("Enter the Author Id:")
            if authorid == "":
                raise Exception("\nThis Author Id field cannot be empty !!")
            AdminHome.ag(self, "genre")
            genreid = input("Enter the Genre Id:")
            if genreid == "":
                raise Exception("\nThis Genre Id field cannot be empty !!")
            coins = float(input("Enter the Coins:"))
            rating = float(input("Enter the Rating:"))
            days = float(input("Enter the Day Count Giving:"))
            file_name = input("Enter the File Name:")
            if file_name == "":
                raise Exception("\nThis File Name field cannot be empty !!")
            insert_query = "insert into book (book_name,authorid,genreid,coins,rating,days,file_name)values(%s,%s,%s,%s,%s,%s,%s)"
            conn.login.execute(insert_query, (book_name, int(authorid), int(genreid), coins, rating ,days,file_name))
            conn.databaseobj.commit()
            print("You have successfully added your new book... :)")
        except Exception as e:
            print(e)
            AdminHome.add_book(self)

    def delete_book(self):
        global phone_id
        AdminHome.view_book(self)
        while True:
            book_id = input("Enter the book id to be deleted : ")
            if book_id == "":
                print("This book id field cannot be empty.")
            elif book_id.isalpha():
                print("Enter only number here")
            else:
                break
        while True:
            print("""Are you sure you want to delete this book?
            1.Yes
            2.No""")
            choice = input("Enter an option from above choice : ")
            if choice == "1":
                query = ("delete from book where bookid={} ").format(int(book_id))
                conn.login.execute(query)
                conn.databaseobj.commit()
                print("""\n\n
                                        ----------------------------Book Deleted Successfully :)----------------------------
                        \n""")
                break
            elif choice == "2":
                break
            else:
                print("INVALID!!!Enter an option from above [1 or 2]")

    def view_plan(self):
        conn.login.execute('Call UpdatePlanUserCount')
        query = 'SELECT * FROM plan'
        conn.login.execute(query)
        query_result = conn.login.fetchall()
        # Checks if there are any results returned by the query.
        if query_result:
            print(
                # Uses the tabulate function from the tabulate library to format the query results into a table.
                tabulate(query_result,
                         headers=["PlanId", "Plan_name", "Description","Duration", "Price", "Coins","UserCount Sub"]))
        else:
            print("The plan is empty.")

    def remove_plan(self):
        while True:
            print("""\n                                                      --------------------------
                                                        DISCARD CURRENTLY PLANS 
                                                      -------------------------- """)
            AdminHome.view_plan(self)
            print("""                                               
                                   Choose an option :
                                  1.Continue Removing 
                                  2.Go Back""")
            choice = input("""                Enter a number from above list : """)
            if choice == '1':
                planid = input(f"Enter the Plan ID to remove: ")
                conn.login.execute("delete from plan where planid=%s", (int(planid),))
                conn.databaseobj.commit()
                print("""\n\n
                                        ----------------------------Plan Deleted Successfully----------------------------
                        \n""")
            if choice == '2':
                break

    def update_plan(self):
        headers = ["PlanId", "Plan_name", "Description","Duration", "Price", "Coins"]
        while True:
            print("""\n                                                      --------------------------
                                                        UPDATE CURRENTLY PLANS 
                                                      -------------------------- """)
            AdminHome.view_plan(self)
            print("""                                               
                                   Choose an option :
                                  1.Continue Updating 
                                  2.Go Back""")
            choice = input("""                Enter a number from above list : """)
            if choice == '1':
                index = int(input("Enter the Column no of the Table to Update: "))
                if headers[index - 1]:
                    planid = input(f"Enter the Plan ID to update the {headers[index - 1]}: ")
                    value = input(f"Enter the {headers[index - 1]} to update: ")
                    conn.login.execute(f"Update plan set {headers[index - 1]}=%s where planid=%s", (value, int(planid)))
                    conn.databaseobj.commit()
                else:
                    print("Invalid number")
                print(f"{headers[index - 1]} updated successfully!!!\n")
            if choice == '2':
                break


    def add_plan(self):
        try:
            plan_name = input("Enter the Plan Name: ")
            if plan_name == "":
                raise Exception("This Plan Name field cannot be empty !!")
            description = input("Enter the Description of the Plan: ")
            if description == "":
                raise Exception("\nThis Description field cannot be empty !!")
            duration = input("Enter the duration: ")
            if duration == "":
                raise Exception("This duration field cannot be empty !!")
            price = float(input("Enter the Price: "))
            coins = float(input("Enter the Coins: "))

            insert_query = "insert into plan (plan_name, description, duration, price, coins)values(%s,%s,%s,%s,%s)"
            conn.login.execute(insert_query, (plan_name, description, duration, price, coins))
            conn.databaseobj.commit()
            print("""\n\n
                                    ----------------------------Successfully Added New Plan----------------------------
                    \n""")
        except Exception as e:
            print(e)
            AdminHome.add_plan(self)

    def manage_plan(self):
        while True:
            print("""\n                                          --------------------------
                                                 MANAGE PLANS 
                                          --------------------------      
                       Choose an option :
                      1.Add Plan
                      2.Update Plan 
                      3.View all Plan
                      4.Remove Plan  
                      5.Go Back""")
            choice = input("""                Enter a number from above list : """)

            if choice == '1':
                AdminHome.add_plan(self)
            elif choice == '2':
                AdminHome.update_plan(self)
            elif choice == '3':
                print("""\n                                                     
                                                        --------------------------
                                                              CURRENT PLANS 
                                                        --------------------------      
                      """)
                AdminHome.view_plan(self)
            elif choice == '4':
                AdminHome.remove_plan(self)
            elif choice == '5':
                AdminHome()
            else:
                print("Invalid choice")

    def view_rental(self):
        print("""\n                                                     
                                                        --------------------------
                                                           VIEW RENTAL HISTORY 
                                                        --------------------------      
                              """)
        query = 'select  b.bookid,b.book_name,r.username,r.startdate,r.enddate from rentbooks r join book b on r.bookid=b.bookid'
        conn.login.execute(query)
        query_result = conn.login.fetchall()
        # Checks if there are any results returned by the query.
        if query_result:
            print(
                # Uses the tabulate function from the tabulate library to format the query results into a table.
                tabulate(query_result, headers=["Book_id", "Book_name", "Username","Start Date","End Date"]))
        else:
            print("The history is empty.")

    def view_bill(self):
        print("""\n                                                     
                                                    --------------------------
                                                      VIEW PLAN BILL HISTORY 
                                                    --------------------------      
                              """)
        query = 'SELECT b.name, b.bill_date, b.mode, p.plan_name, b.username FROM bill b JOIN plan p ON b.planid = p.planid'
        conn.login.execute(query)
        query_result = conn.login.fetchall()
        # Checks if there are any results returned by the query.
        if query_result:
            print(
                # Uses the tabulate function from the tabulate library to format the query results into a table.
                tabulate(query_result, headers=["Name", "Bill Date", "Mode","Plan Name","User Name"]))
        else:
            print("The history is empty.")


    def view_enquiry(self,r=0):
        if r == 1:
            query = 'select * from enquiry where response IS NULL'
        else:
            query = 'select * from enquiry'
        print("""\n                                                     
                                                                --------------------------
                                                                       VIEW ENQUIRY  
                                                                --------------------------      
                                      """)
        conn.login.execute(query)
        query_result = conn.login.fetchall()
        # Checks if there are any results returned by the query.
        if query_result:
            formatted_result = (
                (enquiry_id, subject, description, username,enquiry_date, response if response else "Action Required")
                for enquiry_id, subject, description, username,enquiry_date, response in query_result
            )
            print(
                # Uses the tabulate function from the tabulate library to format the query results into a table.
                tabulate(formatted_result, headers=["Enquiry_id", "Subject", "Description", "Username","Enquiry_date","Response"]))
            if r==1:
                while True:
                    c=input("Do u want to response or not:(Y/N) ").upper()
                    if c=='Y':
                        while True:
                            id=input("Enter the Enquiry id: ")
                            conn.login.execute("SELECT * FROM enquiry WHERE enquiry_id=%s",(int(id),))
                            result = conn.login.fetchone()
                            if id == "":
                                print("This enquiry id field cannot be empty.")
                            elif id.isalpha():
                                print("Enter only number here")
                            elif result is None:
                                print("Enquiry id  is not found!!")
                            else:
                                break
                        while True:
                            response = input("Enter the response:")
                            if not response == "":
                                break
                            else:
                                print("This response field cannot be empty !!")
                        query = 'update enquiry set response=%s where enquiry_id=%s'
                        conn.login.execute(query, (response,int(id),))
                        conn.databaseobj.commit()
                        print("""\n\n
                                                    ----------------------------Added successfully----------------------------
                                    \n""")
                        break
                    elif c=='N':
                        print("Thanks for the confirmation...")
                        break
                    else:
                        print("Invalid choice")
            if r==2:
                while True:
                    c=input("Do u want to delete or not:(Y/N) ").upper()
                    if c=='Y':
                        while True:
                            id=input("Enter the Enquiry id: ")
                            conn.login.execute("SELECT * FROM enquiry WHERE enquiry_id=%s",(int(id),))
                            result = conn.login.fetchone()
                            if id == "":
                                print("This enquiry id field cannot be empty.")
                            elif id.isalpha():
                                print("Enter only number here")
                            elif result is None:
                                print("Enquiry id  is not found!!")
                            else:
                                break
                        query = 'delete from enquiry where enquiry_id=%s'
                        conn.login.execute(query, (int(id),))
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

    def enquiry(self):
        while True:
            print("""\n                                          --------------------------
                                                 MANAGE ENQUIRIES 
                                          --------------------------      
                       Choose an option :
                      1.View all Enquiry
                      2.Actions
                      3.Remove Enquiry  
                      4.Go Back""")
            choice = input("""                Enter a number from above list : """)

            if choice == '1':
                AdminHome.view_enquiry(self)
            elif choice == '2':
                AdminHome.view_enquiry(self,1)
            elif choice == '3':
                AdminHome.view_enquiry(self,2)
            elif choice == '4':
                break
            else:
                print("Invalid choice")

    def mainmenu(self):
        while True:
            print("""\n                                          --------------------------
                                            WELCOME ADMINISTRATOR 
                                          --------------------------      
                       Choose an option :
                      1.List All Members
                      2.Manage Books
                      3.Manage Authors
                      4.Manage Genres
                      5.Manage Plan Details
                      6.View Rental History
                      7.View Bill History
                      8.Enquiry
                      9.Exit""")
            choice = input("""                Enter a number from above list : """)

            if choice == '1':
                AdminHome.view_members(self)
            elif choice == '2':
                AdminHome.manage_book(self)
            elif choice == '3':
                AdminHome.ag(self,"author",0,1)
            elif choice == '4':
                AdminHome.ag(self,"genre",0,1)
            elif choice == '5':
                AdminHome.manage_plan(self)
            elif choice == '6':
                AdminHome.view_rental(self)
            elif choice == '7':
                AdminHome.view_bill(self)
            elif choice == '8':
                AdminHome.enquiry(self)
            elif choice == '9':
                print("Exiting the system")
                exit()
            else:
                print("Invalid choice")


class AdminLogin:
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
        select_query = "select * from login where username=%s COLLATE utf8mb4_bin and password=%s COLLATE utf8mb4_bin and role = 'admin'"
        conn.login.execute(select_query, (userid, password))
        result = conn.login.fetchone()
        if result != None:
            print("""\n\n
                                    ----------------------------Successfully Logged In----------------------------
                    \n""")
            AdminHome()
        else:
            print("Incorrect userid or password!!!... :-(")

    def main(self):
        while True:
            print("""                                      -----------------------------------------------------
                                          WELCOME TO ONLINE LIBRARY MANAGEMENT BACKEND
                                      ------------------------------------------------------      
                  ->Choose an option :
                  1.Login
                  2.Exit""")
            number = input("Enter a number from above list : ")
            if number == "1":
                AdminLogin.login(self)
            elif number == "2":
                print("""\n               ----------------------------
                Thanks for using this app :)
                ---------------------------""")
                exit()
            else:
                print("invalid!!! Enter numbers from 1 or 2 only...")


obj = AdminLogin()
obj.main()
