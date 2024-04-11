import sqlite3
#so uhhh this is definitely my first assignment when it comes to programming in general.
#first thing i need to do is get the data from my database.
database = "limbusdatabase.db"
#now that i can get the data now, this string shows you the data is a simple way.
'''functions'''
def gametable(connection, tabletoread):
    cursor = connection.cursor()
    sqlgame = f"select * from {tabletoread}"
    cursor.execute(sqlgame)
    results = cursor.fetchall()
    print(f"{'name':<50}{'release_date':<30}{'rating':<20}")
    for item in results:
        print(f"{item[1]:<50}{item[2]:<30}{item[3]:<20}")

with sqlite3.connect(database) as connection:
    tables = input("Which table would you like to select from?")
    gametable(connection, tables)
#in time, i will make a better version of this with more stuff to do. for now, this will make do.