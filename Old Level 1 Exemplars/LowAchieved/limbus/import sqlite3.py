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
    if tabletoread.casefold() == "games".casefold():
        print(f"{'id':<20}{'name':<50}{'release date':<15}{'rating':<10}{'genre':<40}{'platform':<20}")
        
        for item in results:
            print(f"{item[0]:<20}{item[1]:<50}{item[2]:<15}{item[3]:<10}{item[4]:<40}{item[5]:<20}")
    if tabletoread.casefold() == "critic_reviews".casefold():
        print(f"{'id':<20}{'reviewer name':<50}{'review date':<15}{'rating':<10}{'review text':<40}{'game id':<20}")
        
        for item in results:
            print(f"{item[0]:<20}{item[1]:<50}{item[2]:<15}{item[3]:<10}{item[4]:<40}{item[5]:<20}")
    if tabletoread.casefold() == "user_reviews".casefold():
        print(f"{'id':<20}{'reviewer name':<50}{'review date':<15}{'rating':<10}{'review text':<40}{'game id':<20}")
        
        for item in results:
            print(f"{item[0]:<20}{item[1]:<50}{item[2]:<15}{item[3]:<10}{item[4]:<40}{item[5]:<20}")
        
with sqlite3.connect(database) as connection:
    tables = input("Which table would you like to select from?")
    gametable(connection, tables)
#so the basics are done. now is the time to make it better!
#review text data is stupidly big, idk how to make it neat sorry!