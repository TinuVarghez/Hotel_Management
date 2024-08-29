import mysql.connector

databaseobj = mysql.connector.connect(
        host="localhost",
        user="root",
        password="TinuFi",
)

login = databaseobj.cursor()

# creating database Library_db
login.execute("create database if not exists Library_db")

# using database Library_db
login.execute("use Library_db")

login.execute("create table if not exists author (authorid int primary key,author_name varchar(30))")

login.execute("create table if not exists genre (genreid int primary key,genre_name varchar(30))")

login.execute("create table if not exists book ("
              "bookid int primary key auto_increment,"
              "book_name varchar(30),"
              "authorid int,"
              "genreid int,"
              "coins decimal(10,2),"
              "rating int,"
              "days int,"
              "file_name varchar(50),"
              "foreign key(authorid) references author(authorid) ON DELETE CASCADE,"
              "foreign key(genreid) references genre(genreid) ON DELETE CASCADE)")

login.execute("create table if not exists login ("
              "username varchar(50) primary key,"
              "password varchar(50),"
              "role varchar(20)"
              ")")

login.execute("create table if not exists plan ("
              "planid int primary key auto_increment,"
              "plan_name varchar(30),"
              "description varchar(50),"
              "duration varchar(30),"
              "price decimal(10,2),"
              "coins decimal(10,2),"
              "usercount int)")

login.execute("create table if not exists rentbooks ("
              "bookid int,"
              "username varchar(50),"
              "startdate varchar(45),"
              "enddate varchar(45),"
              "foreign key(bookid) references book(bookid) ON DELETE CASCADE,"
              "foreign key(username) references login(username) ON DELETE CASCADE)")

login.execute("create table if not exists favouritebooks ("
              "bookid int ,"
              "username varchar(50),"
              "foreign key(bookid) references book(bookid) ON DELETE CASCADE,"
              "foreign key(username) references login(username) ON DELETE CASCADE)")

login.execute("create table if not exists user ("
              "username varchar(50),"
              "first_name varchar(30),"
              "last_name varchar(30),"
              "email_id varchar(30),"
              "phone_number varchar(30),"
              "planid int,"
              "balance decimal(10,2),"
              "validitydate varchar(50),"
              "foreign key(username) references login(username) ON DELETE CASCADE,"
              "foreign key(planid) references plan(planid) ON DELETE SET NULL"
              ")")

login.execute("create table if not exists bookreview("
              "review varchar(50),"
              "rating int,"
              "bookid int,"
              "username varchar(50),"
              "foreign key(bookid) references book(bookid) ON DELETE CASCADE,"
              "foreign key(username) references login(username) ON DELETE CASCADE)")

login.execute("create table if not exists bill("
              "name varchar(30),"
              "bill_date varchar(50),"
              "mode varchar(30),"
              "planid int,"
              "username varchar(50),"
              "foreign key(planid) references plan(planid) ON DELETE SET NULL,"
              "foreign key(username) references login(username) ON DELETE CASCADE)")

login.execute("create table if not exists enquiry("
              "enquiry_id int primary key auto_increment,"
              "subject varchar(30),"
              "description varchar(100),"
              "username varchar(50),"
              "enquiry_date varchar(30),"
              "response varchar(100),"
              "foreign key(username) references login(username) ON DELETE CASCADE)")

login.execute("DROP PROCEDURE IF EXISTS UpdatePlanUserCount")

login.execute("""CREATE PROCEDURE `UpdatePlanUserCount`()
                BEGIN
                    UPDATE plan p
                    JOIN (
                        SELECT planid, COUNT(*) AS user_count
                        FROM user
                        GROUP BY planid
                    ) u ON p.planid = u.planid
                    SET p.usercount = u.user_count;
                END""")
