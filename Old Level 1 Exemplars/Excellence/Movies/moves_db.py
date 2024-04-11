'''movie database including the movie's name, the release year, length in minutes, the rating and the genre.
created by Kyle Bass on 1/06/2023'''

import sqlite3

DATABASE_FILE = "Movies.db"

def print_all():
    #print all the information about every movie
    cursor = connection.cursor()
    #select every movie's name, their release year, their length and their rating from the movie database
    sql = "SELECT movie.movie_name,movie.release_year,movie.length,movie.rating,genre.genre_name FROM movie INNER JOIN genre ON movie.genre_id=genre.genre_id"
    #ececute the sql query
    cursor.execute(sql)
    results = cursor.fetchall()
    #print the headings for each column
    print(f"{'Name' :50}{'Release year':20}{'Length (minutes)':20}{'Rating':20}{'Genre':20}")
    #print all of the selected contents neatly so that all of the items are in a line.
    for result in results:
        print(f"{result[0]:<50}{result[1]:<20}{result[2]:<20}{result[3]:<20}{result[4]}")

def print_specific(request_movie):
    #print the information about one movie that the user requested.
    cursor = connection.cursor()
    sql = "SELECT movie.movie_name,movie.release_year,movie.length,movie.rating,genre.genre_name FROM movie INNER JOIN genre ON movie.genre_id=genre.genre_id WHERE movie_id = ?\n"
    cursor.execute(sql,(request_movie,))
    results = cursor.fetchall()
    #make sure that the id the user inputed is available
    if len(results) == 0:
        print("That is not an available ID")
    else:
        print(f"{'Name' :50}{'Release year':20}{'Length (minutes)':20}{'Rating':20}{'Genre':20}")
        #print all of the selected contents neatly so that all of the items are in a line.
        for result in results:
            print(f"{result[0]:<50}{result[1]:<20}{result[2]:<20}{result[3]:<20}{result[4]}")

def print_name_and_id():
    #print all the id and the name of every movie so the user knows what the id is for each movie when they request the information for a specific movie.
    cursor = connection.cursor()
    sql = "SELECT movie_id, movie_name FROM movie"
    cursor.execute(sql)
    results = cursor.fetchall()
    print(f"{'ID':<10}{'Name':10}")
    for result in results:
        print(f"{result[0]:<10}{result[1]:10}")

def print_highest_to_lowest():
    #print all of the movies in order from highest rated to lowest rated
    cursor = connection.cursor()
    #select all the movie names, their release year, their length and rating and show them in order from highest rated to lowest rated
    sql = "SELECT movie.movie_name,movie.release_year,movie.length,movie.rating,genre.genre_name FROM movie INNER JOIN genre ON movie.genre_id=genre.genre_id ORDER BY movie.rating DESC"
    cursor.execute(sql)
    results = cursor.fetchall()
    print(f"{'Name' :50}{'Release year':20}{'Length (minutes)':20}{'Rating':20}{'Genre':20}")
    #print all of the selected contents neatly so that all of the items are in a line.
    for result in results:
        print(f"{result[0]:<50}{result[1]:<20}{result[2]:<20}{result[3]:<20}{result[4]}")

def print_order_by_release_year():
    #print all of the movie from the newest to the oldest.
    cursor = connection.cursor()
    sql = "SELECT movie.movie_name,movie.release_year,movie.length,movie.rating,genre.genre_name FROM movie INNER JOIN genre ON movie.genre_id=genre.genre_id ORDER BY movie.release_year DESC"
    cursor.execute(sql)
    results = cursor.fetchall()
    print(f"{'Name' :50}{'Release year':20}{'Length (minutes)':20}{'Rating':20}{'Genre':20}")
    for result in results:
        print(f"{result[0]:<50}{result[1]:<20}{result[2]:<20}{result[3]:<20}{result[4]}")    

def add_item(connection, movie_name, movie_release_year, movie_length, movie_rating,genre_id):
    #people who know the password can add movies to the database
    '''add item to backpack database'''
    try:
        cursor = connection.cursor()
        #insert a new movie into the database
        sql = "INSERT INTO movie (movie_name,release_year,length,rating ,genre_id) VALUES (?,?,?,?,?)"
        cursor.execute(sql,(movie_name, movie_release_year, movie_length, movie_rating,genre_id))
        connection.commit()
    except:
        print("Couldn't add movie")

def delete_item(connection, movie_name):
    '''delete an item by name from database'''
    try:
        cursor = connection.cursor()
        sql = "DELETE FROM movie WHERE movie_name = (?)"
        #sql = "DELETE FROM contents WHERE name = ?"
        cursor.execute(sql,(movie_name,))
        num_rows_affected = cursor.rowcount
        if num_rows_affected == 0:
            print("Couldn't find movie")
        else:
            print("Deleted movie")
        connection.commit()
    except:
        print("item does not exist")

def add_genre(connection,genre_name):
    #add a new genre
    try:
        cursor = connection.cursor()
        sql = "INSERT INTO genre (genre_name) VALUES (?)"
        cursor.execute(sql,(genre_name,))
        connection.commit()
        print("Successfuly added genre.")
    except:
        print("That genre is already in the table")

def print_genre():
    #print everything in genre table
    cursor = connection.cursor()
    #select everything from the genre table
    sql = "SELECT * FROM genre"
    cursor.execute(sql)
    results = cursor.fetchall()
    print(f"{'ID':<10}{'Name':10}")
    for result in results:
        print(f"{result[0]:<10}{result[1]:10}")

def delete_genre(connection,genre_id):
    #delete a genre in the genre table
    try:
        cursor = connection.cursor()
        #delete a specific gerne
        sql = "DELETE FROM genre WHERE genre_id = (?)"
        cursor.execute(sql,(genre_id,))
        num_rows_affected = cursor.rowcount
        if num_rows_affected == 0:
            print("Couldn't find genre")
        else:
            print("Deleted genre")
        connection.commit()
    except:
        print("item does not exist")

def show_movie_with_genre(requested_genre):
    # Print all of the movies that have the genre that the user requested.
    cursor = connection.cursor()
    sql = "SELECT movie.movie_name, movie.release_year, movie.length, movie.rating FROM movie INNER JOIN genre ON movie.genre_id=genre.genre_id WHERE movie.genre_id = ?"
    # Convert the requested_genre to an integer
    genre_id = int(requested_genre)
    cursor.execute(sql, (genre_id,))
    results = cursor.fetchall()
    if len(results) == 0:
        print("No movies found for the requested genre")
    else:
        print(f"{'Name':50}{'Release year':20}{'Length (minutes)':20}{'Rating':20}")
        # Print all of the selected contents neatly so that all of the items are in a line.
        for result in results:
            print(f"{result[0]:<50}{result[1]:<20}{result[2]:<20}{result[3]}")

if __name__ == "__main__":
    #main program - get connection and ask for user input
    connection = sqlite3.connect("Movies.db")
    while True:
        action = input("What do you want to do?\n1. Show all movies\n2.Show the information for a specific movie\n3.Show in order from highest rated to lowest rated\n4.Show in order from newest to oldest\n5.Add movie(needs password)\n6.Delete movie(needs password)\n7.Add genre(needs password)\n8.Delete genre(needs password)\n9.Print all of the movies with a genre that you request\n10.Exit\n")
        if action == "1":
            '''show all games'''
            print_all()
        elif action == "2":
            #Show the information for a specific movie
            try:
                print_name_and_id()
                request_movie = int(input("What is the ID for the movie you want the informatino for?"))
                print_specific(request_movie)
            except:
                print("That's not a real id!")
        elif action == "3":
            #show all of the movies in order from the highest rated to the lowest rated
            print_highest_to_lowest()
        elif action == "4":
            #show all of the movies in order fromthe newest to the oldest
            print_order_by_release_year()
        elif action == "5":
            # add a movie to the movie table
            password = input("What is the password?(the password is 123)\n")
            if password != "123":   #the password needed to add a movie so only people who have the password can add movies
                print("That is not the password.")
            elif password == "123":
                movie_name= input("What is the name of the movie you want to add?\n")
                try:
                    movie_release_year = int(input("What year was the movie released?\n"))
                    movie_length = int(input("How long is your movie in minutes?\n"))
                    movie_rating = float(input("What is the rating of your movie out of 10?"))
                    print_genre()
                    genre_id = int(input("What is the id of the movie's genre?"))
                    # Check if the genre ID is valid
                    cursor = connection.cursor()
                    #Select a specific genre and its id
                    sql = "SELECT * FROM genre WHERE genre_id = (?)"
                    cursor.execute(sql, (genre_id,))
                    genre = cursor.fetchone()
                    if genre is None:
                        print("That is not a valid genre id")
                    else:
                        add_item(connection, movie_name, movie_release_year, movie_length, movie_rating,genre_id)
                        print("Added movie")
                except ValueError:
                    print("That is not a valid input")
                except:
                    print("couldn't add movie")
            else:
                print("Couldn't add movie")
        elif action == "6":
            #Delete a movie from the movie table
            password = input("What is the password?(the password is 123)\n")
            if password != "123":   #the password needed to delete a movie so only people hwo have the password can delete movies
                print("That is not the password.")
            elif password == "123":
                print_name_and_id()
                movie_name = input("Out of the movies above, what is the name of the one you want to delete?")
                delete_item(connection, movie_name)
            else:
                print("Couldn't delete movie")
        elif action == "7":
            #add a genre to the genre table
            password = input("What is the password?(the password is 123)\n")
            if password != "123":
                print("That is not the password.")
            else:
                print_genre()
                genre_name = input("What is the genre you want to add?\nPlease do not add a genre that is already in the table.\n")
                add_genre(connection,genre_name)
        elif action == "8":
            #delete a genre from the genre table
            password = input("What is the password?(the password is 123)\n")
            if password != "123":
                print("That is not the password.")
            else:
                print_genre()
                genre_id = input("What is the id of the genre you want to delete?\n")
                delete_genre(connection,genre_id)
        elif action == "9":
            #show all of the movies that have the same genre as the genre the user requested
            print_genre()
            requested_genre = input("Which genre is the one you want to request?\n")
            try:
                show_movie_with_genre(requested_genre)
            except:
                print("Could not show")
        elif action == "10":
            #leaves
            print("\nGoodbye\n")
            break
        else:
            print("That's not an option!")