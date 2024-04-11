import sqlite3
DATABASE  = "steam.db"
DATABASE_FILE = "steam.db"


#code written by Zeke Stephenson




#GAME DATABASE CODE

#function to show all games
def show_games(connection):
    '''using the connection to the database it prints out all the games from the game table'''
    try:
        cursor = connection.cursor()
        #Sql statement
        sql = "SELECT * FROM game"
        cursor.execute(sql)
        #executes SQL statement
        results = cursor.fetchall()
        #takes all data from database
        print(f"{'game_name':<20}")
        for item in results:
            print(item[1])
    except:
        print("Something went wrong with the connection")
#function to add game
def add_game(connection, game_name, platform_id, genre_id):
    '''uses the database connection along with game_name, platform_id and genre_id user inputs to add new games to the game table'''
    try:
        cursor = connection.cursor()
        #Sql statement
        sql = "INSERT INTO game (game_name, platform_id, genre_id) VALUES (?,?,?)"
        cursor.execute(sql,(game_name, platform_id, genre_id))
        #executes SQL statement
        connection.commit()
        #saves the changes to sql database
        print(f"{game_name} has been added")
    except:
        print("Item couldn't be added")
#function to delete game
def delete_game(connection, game_name):
    '''uses the connection to the database and a game_name user input to delete a selected game from the game table'''
    cursor = connection.cursor()
    #Sql statement
    sql = "DELETE FROM game WHERE game_name = ?"
    cursor.execute(sql,(game_name,))
    #executes SQL statement
    num_rows_affected = cursor.rowcount
    if num_rows_affected == 0:
        print("couldn't find item")
        return
    else:
        connection.commit()
        #saves the changes to sql database
        print(f"{game_name} has been deleted")
#function to print games by platform
def print_games_by_platform(connection, platform_id):
    '''uses the database connection and a platform_id user input to print out all games from the game table from a selected platform_id'''
    cursor = connection.cursor()
    #Sql statement
    sql = "select * from game where platform_id is (?)"
    cursor.execute(sql,(platform_id,))
    #executes SQL statement
    results = cursor.fetchall()
    #takes all data from database
    print(f"{'game_name':<20}")
    for item in results:
        print(item[1])







#GENRE DATABASE CODE


#function to print all genres
def show_genres(connection):
 '''uses the database connection to print all of the genres from the genre table'''
 try:
     cursor = connection.cursor()
     #Sql statement
     sql = "SELECT * FROM genre"
     cursor.execute(sql)
     #executes SQL statement
     results = cursor.fetchall()
     #takes all the data from a specific database
     print(f"{'genre_name':<20}{'genre_id' :<30}")
     for item in results:
          print(f"{item[1]:<20}{item[0]:<20}")
 except:
     print("Something went wrong with the connection")
#function to add genre
def add_genre(connection, genre_name):
    '''uses the connection and genre_name user input to add a genre to the genre table'''
    try:
        cursor = connection.cursor()
        #Sql statement
        sql = "INSERT INTO genre (genre_name) VALUES (?)"
        cursor.execute(sql,(genre_name,))
        #executes SQL statement
        connection.commit()
        #saves changes to sql databse
        print(f"{genre_name} has been added")
    except:
        print("Item couldn't be added")
#function to delete genres
def delete_genre(connection, genre_name):
    '''uses the connection and genre_name user input to delete a genre from the genre table'''
    cursor = connection.cursor()
    #Sql statement
    sql = "DELETE FROM genre WHERE genre_name = ?"
    cursor.execute(sql, (genre_name,))
    #executes SQL statement
    num_rows_affected = cursor.rowcount
    if num_rows_affected == 0:
        print("couldn't find item")
        return
    else:
        connection.commit()
        #saves changes made to sql database
        print(f"{genre_name} has been deleted")










#PLATFORM DATABASE CODE


#function to show platforms
def show_platforms(connection):
    '''uses the connection to  print out all the platforms from the platform table'''
    try:
        cursor = connection.cursor()
        #Sql statement
        sql = "SELECT * FROM platform"
        cursor.execute(sql)
        #executes SQL statement
        results = cursor.fetchall()
        #takes all data from specific database
        print(f"{'platform_name':<20}{'platform_id':<20}")
        for item in results:
            print(f"{item[1]:<20}{item[0]:<20}")
    except:
        print("Something went wrong with the connection")
#function to add a platform
def add_platform(connection, platform_name):
    '''uses the database connection and the platform_name user input the add new platforms to the platform table'''
    try:
        cursor = connection.cursor()
        #Sql statement
        sql = "INSERT INTO platform (platform_name) VALUES (?)"
        cursor.execute(sql, (platform_name,))
        #executes SQL statement
        connection.commit()
        #saves any changes made to SQL database
        print(f"{platform_name} has been added")
    except:
        print("Item couldn't be added")
#function to delete platform
def delete_platform(connection, platform_name):
    '''uses the connection and platform_name user input to delete a platform from the platform table'''
    cursor = connection.cursor()
    #Sql statement
    sql = "DELETE FROM platform WHERE platform_name = (?)"
    cursor.execute(sql, (platform_name,))
    #executes SQL statement
    num_rows_affected = cursor.rowcount
    if num_rows_affected == 0:
        print("couldn't find item")
        return
    else:
        connection.commit()
        #saves any changes made to sql database
        print(f"{platform_name} has been deleted")









#USER INTERFACE CODE



with sqlite3.connect(DATABASE_FILE) as connection:
    '''creates a connection to the DATABASE_FILE to edit or print out tables from the database'''
    while True:
        #asks user which table they want to edit
        user_input2 = input("\nWhich Table do you want to edit?\n1. game Database\n2. genre Database\n3. platform Database\n")
        #informs user how to cancel certain code actions
        print("to go back to menu when adding/deleting enter game/genre/platform name as 'back'")
        #asks user what they want to do with their game database
        if user_input2 == "1":
            while True:
                user_input = input("\nWhat do you want to do?\n1. Print All \n2. Delete games\n3. Add games\n4. Show games by platform \n5. Exit\n")
                if user_input == "1":
                   show_games(connection)
                elif user_input == "3":
                    print("Make Sure You Input the correct Id for your platform/genre when adding a new game. Check platform/genre ID via printing them on the genre and platform databases.")
                    game_name = input("game Name: \n")
                    if game_name == "back":
                        break
                    show_genres(connection)
                    genre_name = input("Which genre Produced?(via ID): \n")
                    show_platforms(connection)                    
                    platform_name = input("platform ID: \n")
                    
                    add_game(connection,game_name,genre_name, platform_name)
                elif user_input == "2":
                    game_name = input("game Name: \n")
                    if game_name == "back":
                        break
                    delete_game(connection, game_name)
                elif user_input == "5":
                    break
                #goes back to main menu
                elif user_input == "4":
                    show_platforms(connection)  
                    platform_id = input("platform ID?")       
                    print_games_by_platform(connection, platform_id)
                    
        #Asks user what they want to do with their genre database
        if user_input2 == "2":
            while True:
                user_input3 = input("\nWhat do you want to do?\n1. Print All genres\n2. Add genre\n3. Delete genre\n4. Exit\n")
                if user_input3 == "1":
                   show_genres(connection)
                elif user_input3 == "2":
                    genre_name = input("genre Name: \n")
                    add_genre(connection,genre_name)
                    if genre_name == "back":
                        break
                elif user_input3 == "3":
                    genre_name = input("genre Name: \n")
                    if genre_name == 'back':
                        break
                    delete_genre(connection, genre_name)
                elif user_input3 == "4":
                    #go back to main menu
                    break
        #asks user what they want to do with their platform database
        if user_input2 == "3":
            while True:
                user_input4 = input("\nWhat do you want to do?\n1. Print All platforms\n2. Add platform\n3. Delete platform\n4. Exit\n")
                if user_input4 == "1":
                   show_platforms(connection)
                elif user_input4 == "2":
                    platform_name = input("platform Name: \n")
                    if platform_name == 'back':
                        break
                    add_platform(connection,platform_name)
                elif user_input4 == "3":
                    platform_name = input("platform Name: \n")
                    if platform_name == 'back':
                        break
                    delete_platform(connection, platform_name)
                elif user_input4 == "4":
                    #goes back to main menu
                    break