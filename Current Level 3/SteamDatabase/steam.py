import sqlite3
import math

DATABASE_FILE = "steam.db"
ITEMS_PER_PAGE = 40
DASHES_FOR_SEPARATORS = 36


def display_pages(type, data):
    """Display large amounts of data as pages and switch between"""
    page = 1  # Because there's a lot of data
    max_pages = math.ceil((len(data))/ITEMS_PER_PAGE)
    continuing = True
    while continuing is True:
        amounts_min = (page-1)*ITEMS_PER_PAGE
        my_list = []
        for i in range(ITEMS_PER_PAGE):  # Just look at these of an amount
            my_list.append(data[amounts_min])
            if data[-1] == data[amounts_min]:
                break
            else:
                amounts_min = amounts_min + 1
        # Print the data in a block
        print("-"*DASHES_FOR_SEPARATORS)
        print(f"| {'ID':<7} | {type}")
        print("-"*DASHES_FOR_SEPARATORS)
        for item in my_list:
            print(f"| {item[0]:<7} | {item[1]}")
        print("-"*DASHES_FOR_SEPARATORS)

        # Page switching
        if page == 1 and page == max_pages:  # Only one page
            continuing = False
        elif page == max_pages:  # Last page
            while True:
                next = input("Type BACK for previous page, END to retrun to menu: ")
                if next == "BACK":
                    page = page - 1
                    break
                elif next == "END":
                    continuing = False
                    break
                else:
                    print("Invalid command, try again.")
        elif page == 1:  # First page
            while True:
                next = input("Type NEXT for next page, END to retrun to menu: ")
                if next == "NEXT":
                    page = page + 1
                    break
                elif next == "END":
                    continuing = False
                    break
                else:
                    print("Invalid command, try again.")
        else:  # All pages in between
            while True:
                next = input("Type NEXT for next page, BACK for previous page, END to retrun to menu: ")
                if next == "NEXT":
                    page = page + 1
                    break
                elif next == "BACK":
                    page = page - 1
                    break
                elif next == "END":
                    continuing = False
                    break
                else:
                    print("Invalid command, try again.")


def read_one(id):
    """Display all data for a specified game by id"""
    # Connect to database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # Collect data from game table
    cursor.execute("SELECT name, \
                           releasedate, \
                           windowscompat, \
                           maccompat, \
                           linuxcompat, \
                           minage, \
                           achievments, \
                           negreviews, \
                           posreviews, \
                           averageplaytime, \
                           medianplaytime, \
                           price, \
                           id \
                    FROM Game \
                    WHERE id = ?;", (id,))
    game_data = cursor.fetchone()
    # testing game exists
    if not game_data:
        print("That game doesn't exist")
    else:
        # Genre collection
        cursor.execute("SELECT Genre.name \
                        FROM Genre \
                            JOIN GameGenre ON GameGenre.genreid = Genre.id \
                        WHERE GameGenre.gameid = ?;", (id,))
        genre_data = cursor.fetchall()
        # Dev collection
        cursor.execute("SELECT Developer.name \
                        FROM Developer \
                            JOIN GameDeveloper ON GameDeveloper.devid = Developer.id \
                        WHERE GameDeveloper.gameid = ?;", (id,))
        dev_data = cursor.fetchall()
        # Publisher collection
        cursor.execute("SELECT Publisher.name \
                        FROM Publisher \
                            JOIN GamePublisher ON GamePublisher.publishid = Publisher.id \
                        WHERE GamePublisher.gameid =?;", (id,))
        publisher_data = cursor.fetchall()

        # Printing data
        # Name, release date, percentage
        percent_rating = "%.1f" % (100*(game_data[8]/(game_data[8]+game_data[7])))
        print()
        print("-"*30)
        print(f"{game_data[0]}   {percent_rating}%")
        print(f"Release date (yyyy-mm-dd): {game_data[1]}")

        # Minimum age
        if game_data[5] > 0:  # Only print if age restricited
            print(f"R{game_data[5]}")

        # Available achievements
        print(f"{game_data[6]} achievements available")

        # Price
        if game_data[11] == 0:
            print("FREE")
        else:
            if str(game_data[11])[-2] == ".":
                price = str(game_data[11]) + "0"
                print(f"${price}")
            else:
                print(f"${game_data[11]}")

        print()

        # Genres
        print("Genres:")
        for genre in genre_data:
            print(genre[0])

        print()

        # Developers
        print("Developers:")
        for dev in dev_data:
            print(dev[0])

        print()

        # Publishers
        print("Publishers:")
        for publisher in publisher_data:
            print(publisher[0])

        print()

        # Compatable systems
        compats = []  # Storing compatable systems
        if game_data[2] == 1:  # Check windows compatability
            compats.append("Windows")
        if game_data[3] == 1:  # Check mac compatability
            compats.append("Mac")
        if game_data[4] == 1:  # Check linux compatability
            compats.append("Linux")
        print("Compatable systems:")
        for system in compats:
            print(system)

        print()

        # Average and median playtimes
        if game_data[9] == 0:
            print("Average playtime unavailable")
        else:
            print(f"Average playtime: {game_data[9]} hours")
        if game_data[10] == 0:
            print("Median playtime unavailable")
        else:
            print(f"Median playtime: {game_data[10]} hours")

        print("-"*30)
    conn.close()  # Close connection to save efficiency


def show_genres():
    """Show list of all genres"""
    # Connect to database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT * \
                    FROM Genre \
                    ORDER BY name;")
    genres = cursor.fetchall()

    # Print the genres in a block
    print("-"*35)
    print(f"| {'ID':<4} | Genre")
    print("-"*35)
    for genre in genres:
        print(f"| {genre[0]:<4} | {genre[1]}")
    print("-"*35)

    conn.close()  # Close connection to save efficiency


def show_developers():
    """Show list of all developers"""
    # Connect to database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT * \
                    FROM Developer \
                    ORDER BY name;")
    developers = cursor.fetchall()

    display_pages("Developer", developers)

    conn.close()  # Close connection to save efficiency


def show_publishers():
    """Show list of all publishers"""
    # Connect to database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT * \
                    FROM Publisher \
                    ORDER BY name;")
    publishers = cursor.fetchall()

    display_pages("Publisher", publishers)

    conn.close()  # Close connection to save efficiency


def show_in_genre(id):
    """Show list of games within one genre"""
    # Connect to database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    
    cursor.execute("SELECT name \
                    FROM Genre \
                    WHERE id = ?", (id,))
    genre = cursor.fetchone()

    # test if exists
    if not genre:
        print("That genre doesn't exist")
    else:
        cursor.execute("SELECT Game.id, \
                            Game.name \
                        FROM Game \
                        JOIN GameGenre ON GameGenre.gameid = Game.id \
                        WHERE GameGenre.genreid = ? \
                        ORDER BY Game.name;", (id,))
        games = cursor.fetchall()

        print()
        print(f"Games in {genre[0]}")

        # Print list of games in a block as pages
        display_pages("Game", games)

    conn.close()  # Close connection to save efficiency


def show_in_dev(id):
    """Show list of games by one developer"""
    # Connect to database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT name \
                    FROM Developer \
                    WHERE id = ?", (id,))
    developer = cursor.fetchone()

    # test if exists
    if not developer:
        print("That developer doesn't exist")
    else:
        cursor.execute("SELECT Game.id, \
                            Game.name \
                        FROM Game \
                        JOIN GameDeveloper ON GameDeveloper.gameid = Game.id \
                        WHERE GameDeveloper.devid = ? \
                        ORDER BY Game.name;", (id,))
        games = cursor.fetchall()

        print()
        print(f"Games by {developer[0]}")

        # Print list of games in a block as pages
        display_pages("Game", games)

    conn.close()  # Close connection to save efficiency


def show_in_publisher(id):
    """Show list of games by one publisher"""
    # Connect to database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT name \
                    FROM Publisher \
                    WHERE id = ?", (id,))
    publisher = cursor.fetchone()

    # test if exists
    if not publisher:
        print("That publlisher doesn't exist")
    else:
        cursor.execute("SELECT Game.id, \
                            Game.name \
                        FROM Game \
                        JOIN GamePublisher ON GamePublisher.gameid = Game.id \
                        WHERE GamePublisher.publishid = ? \
                        ORDER BY Game.name;", (id,))
        games = cursor.fetchall()

        print()
        print(f"Games by {publisher[0]}")

        # Print list of games in a block as pages
        display_pages("Game", games)

    conn.close()  # Close connection to save efficiency


def search_game_by_name():
    """Search game by name rather than id, shows list of all possibilities"""
    # Connect to database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    search = input("Search games by name: ")
    search = f"%{search}%"  # format so it searches correctly
    if len(search) > 200:
        print("Search input is too long")
    else:
        cursor.execute("SELECT id, \
                            name \
                        FROM Game \
                        WHERE name LIKE ? \
                        ORDER BY name;", (search,))
        games = cursor.fetchall()

        if len(games) > 0:
            display_pages("Game", games)
        else:
            print("No results")

    conn.close()  # Close connection to save efficiency


def search_dev_by_name():
    """Search developer by name rather than id, shows list of all possibilities"""
    # Connect to database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    search = input("Search developers by name: ")
    search = f"%{search}%"  # format so it searches correctly
    if len(search) > 200:
        print("Search input is too long")
    else:
        cursor.execute("SELECT id, \
                            name \
                        FROM Developer \
                        WHERE name LIKE ? \
                        ORDER BY name;", (search,))
        devs = cursor.fetchall()

        if len(devs) > 0:
            display_pages("Developer", devs)
        else:
            print("No results")

    conn.close()  # Close connection to save efficiency


def search_publisher_by_name():
    """Search publisher by name rather than id, shows list of all possibilities"""
    # Connect to database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    search = input("Search publishers by name: ")
    search = f"%{search}%"  # format so it searches correctly
    if len(search) > 200:
        print("Search input is too long")
    else:
        cursor.execute("SELECT id, \
                            name \
                        FROM Publisher \
                        WHERE name LIKE ? \
                        ORDER BY name;", (search,))
        publishers = cursor.fetchall()

        if len(publishers) > 0:
            display_pages("Publisher", publishers)
        else:
            print("No results")

    conn.close()  # Close connection to save efficiency


def add_dev():
    """Add a new developer to the database"""
    # Connect to database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    dev_name = input("Name of developer (Type / to cancel): ")
    if dev_name != "/":
        cursor.execute("SELECT id FROM Developer WHERE name = ?;", (dev_name,))
        test = cursor.fetchone()
        if not test:
            cursor.execute("INSERT INTO Developer (name) VALUES (?);", (dev_name,))
            conn.commit()
        else:
            print(f"That developer already exists, id {test[0]}")
    conn.close()  # Close connection to save efficiency


def add_publisher():
    """Add a new publisher to the database"""
    # Connect to database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    publisher_name = input("Name of publisher (Type / to cancel): ")
    if publisher_name != "/":
        cursor.execute("SELECT id FROM Publisher WHERE name = ?;", (publisher_name,))
        test = cursor.fetchone()
        if not test:
            cursor.execute("INSERT INTO Publisher (name) VALUES (?);", (publisher_name,))
            conn.commit()
        else:
            print(f"That publisher already exists, id {test[0]}")
    conn.close()  # Close connection to save efficiency


def add_genre():
    """Add a new genre to the database"""
    # Connect to database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    genre_name = input("Name of genre (Type / to cancel): ")
    if genre_name != "/":
        cursor.execute("SELECT id FROM Genre WHERE name = ?;", (genre_name,))
        test = cursor.fetchone()
        if not test:
            cursor.execute("INSERT INTO Genre (name) VALUES (?);", (genre_name,))
            conn.commit()
        else:
            print(f"That genre already exists, id {test[0]}")
    conn.close()  # Close connection to save efficiency


def add_game():
    """Add new game to database and add to bridging tables"""
    # Connect to database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # Lists
    game_table_stuff = []

    functions = [ask_name_for_add_game,
                 ask_release_year_add_game,
                 ask_release_month_add_game,
                 ask_release_day_add_game,
                 ask_devs_add_game,
                 ask_publishers_add_game,
                 ask_genres_add_game,
                 ask_windows_compatablity,
                 ask_mac_compatability,
                 ask_linux_compatability,
                 ask_min_age,
                 ask_achievements,
                 ask_pos_reviews,
                 ask_neg_reviews,
                 ask_median_playtime,
                 ask_average_playtime,
                 ask_price]

    print("Make sure you know the ID of the genres, publishers and developers before starting.")
    for func in functions:
        if func == ask_release_day_add_game:
            goal, cont = ask_release_day_add_game(month)
            game_table_stuff.append(goal)
        elif func == ask_devs_add_game:  # Developers in seperate list
            developers, cont = ask_devs_add_game()
        elif func == ask_publishers_add_game:  # Publishers in seperate list
            publishers, cont = ask_publishers_add_game()
        elif func == ask_genres_add_game:  # Genres in seperate list
            genres, cont = ask_genres_add_game()
        else:
            goal, cont = func()
            game_table_stuff.append(goal)
        # Check if continuing
        if cont is False:
            break
        elif func == ask_release_month_add_game:  # to save month
            month = goal

    if cont is True:  # didn't cancel
        release_date = f"{game_table_stuff[1]}-{game_table_stuff[2]}-{game_table_stuff[3]}"  # format date
        cursor.execute("INSERT INTO Game (name, \
                                          releasedate, \
                                          windowscompat, \
                                          maccompat, \
                                          linuxcompat, \
                                          minage, \
                                          achievments, \
                                          negreviews, \
                                          posreviews, \
                                          averageplaytime, \
                                          medianplaytime, \
                                          price) \
                                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (game_table_stuff[0],  # name
                        release_date,  # release date
                        game_table_stuff[4],  # windows
                        game_table_stuff[5],  # mac
                        game_table_stuff[6],  # linux
                        game_table_stuff[7],  # age
                        game_table_stuff[8],  # achievements
                        game_table_stuff[10],  # neg reviews
                        game_table_stuff[9],  # pos reviews
                        game_table_stuff[12],  # average pt
                        game_table_stuff[11],  # median pt
                        game_table_stuff[13]))  # price
        conn.commit()
        cursor.execute("SELECT id FROM Game WHERE name = ?;", (game_table_stuff[0],))
        game_id = cursor.fetchone()
        game_id = str(game_id[0])

        for genre in genres:
            genre = str(genre)
            cursor.execute("INSERT INTO GameGenre VALUES (?, ?);", (game_id, genre))
            conn.commit()

        for dev in developers:
            dev = str(dev)
            cursor.execute("INSERT INTO GameDeveloper VALUES (?, ?);", (game_id, dev))
            conn.commit()

        for publisher in publishers:
            publisher = str(publisher)
            cursor.execute("INSERT INTO GamePublisher VALUES (?, ?);", (game_id, publisher))
            conn.commit()
        
        print(f"\nThe ID of the game is {game_id}.")

        read_one(game_id)

    conn.close()  # Close connection to save efficiency


def ask_name_for_add_game():
    """ask the game's name to add a new game"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cont = True
    game_name = input("Name of game (Type / at any time to cancel): ")
    if game_name != "/":  # cancel
        # Test if game aready exists
        cursor.execute("SELECT id FROM Game WHERE name = ?;", (game_name,))
        test = cursor.fetchone()
        if test:  # Exists already
            print(f"Game already exists, id {test[0]}")
            cont = False
    else:
        cont = False
    conn.close()
    return game_name, cont


def ask_release_year_add_game():
    """ask game's year to add into game"""
    cont = True
    while True:  # until proper formatting
        try:  # Not a number
            release_year = input("Release year: ")
            if release_year != "/":  # cancel
                release_year = int(release_year)
                if len(str(release_year)) != 4 or release_year < 1:
                    print("That is not a valid year, the year should have 4 digits.")
                else:
                    release_year = str(release_year)
                    break
            else:
                cont = False
                break
        except ValueError:
            print("That is not a year")
    return release_year, cont


def ask_release_month_add_game():
    """ask game's month to add into game"""
    cont = True
    while True:  # until proper formatting
        try:  # not a number
            release_month = input("Release month (number not name): ")
            if release_month != "/":  # cancel
                release_month = int(release_month)
                if len(str(release_month)) > 2 or release_month > 12 or release_month < 1:
                    print("That is not a valid month")
                elif len(str(release_month)) == 1:
                    release_month = f"0{release_month}"
                    break
                else:
                    release_month = str(release_month)
                    break
            else:
                cont = False
                break
        except ValueError:
            print("That is not a month in the form of a number")
    return release_month, cont


def ask_release_day_add_game(month):
    """ask games's release day to add into game"""
    cont = True
    while True:  # until proper formatting
        try:  # not a number
            release_day = input("Release day: ")
            if release_day != "/":  # cancel
                release_day = int(release_day)
                if release_day < 1:
                    print("That is not a valid date")
                elif len(str(release_day)) > 2:
                    print("That is not a valid date")
                elif release_day > 31:
                    print("That is not a valid date")
                else:
                    if len(str(release_day)) == 1:
                        release_day = f"0{release_day}"
                        break
                    elif release_day > 28 and month == "02":  # february
                        print("That is not a valid date")
                    elif release_day > 31:  # short months
                        if month == "04" or month == "06" or month == "09" or month == "11":
                            print("That is not a valid date")
                        else:  # long months
                            release_day = str(release_day)
                            break
                    else:
                        release_day = str(release_day)
                        break
            else:
                cont = False
                break
        except ValueError:
            print("That is not a valid date")
    return release_day, cont


def ask_devs_add_game():
    """ask the devs for the add game function"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cont = True
    developers = []
    print("Type DONE when all developers are added")
    while True:
        try:
            this_dev = input("ID of developer: ")
            if this_dev == "DONE" and developers:
                break
            elif this_dev == "DONE" and not developers:
                print("You must add at least one developer.")
                print("If the intended developer doesn't exist in the database, cancel and add it.")
            elif this_dev == "/":
                cont = False
                break
            elif len(this_dev) > 9:
                print("That ID doesn't exist")
            else:
                this_dev = int(this_dev)
                cursor.execute("SELECT name FROM Developer WHERE id = ?;", (this_dev,))
                test = cursor.fetchone()
                if not test:  # No dev found
                    print("That ID doesn't exist")
                else:
                    developers.append(this_dev)
        except ValueError:
            print("That is not a valid id")
    conn.close()
    return developers, cont


def ask_publishers_add_game():
    """ask publishers for adding a game"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cont = True
    publishers = []
    print("Type DONE when all publishers are added")
    while True:
        try:
            this_publisher = input("ID of publisher: ")
            if this_publisher == "DONE" and publishers:
                break
            elif this_publisher == "DONE" and not publishers:
                print("You must add at least one publisher.")
                print("If the intended publisher doesn't exist in the database, cancel and add it.")
            elif this_publisher == "/":
                cont = False
                break
            elif len(this_publisher) > 9:
                print("That ID doesn't exist")
            else:
                this_publisher = int(this_publisher)
                cursor.execute("SELECT name FROM Publisher WHERE id = ?;", (this_publisher,))
                test = cursor.fetchone()
                if not test:  # No publisher found
                    print("That ID doesn't exist")
                else:
                    publishers.append(this_publisher)
        except ValueError:
            print("That is not a valid id")
    conn.close()
    return publishers, cont


def ask_genres_add_game():
    """ask genres for add game"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cont = True
    genres = []
    print("Type DONE when all genres are added")
    while True:
        try:
            this_genre = input("ID of genre: ")
            if this_genre == "DONE" and genres:
                break
            elif this_genre == "DONE" and not genres:
                print("You must add at least one genre.")
                print("If the intended genre doesn't exist in the database, cancel and add it.")
            elif this_genre == "/":
                cont = False
                break
            elif len(this_genre) > 9:
                print("That ID doesn't exist")
            else:
                this_genre = int(this_genre)
                cursor.execute("SELECT name FROM Genre WHERE id = ?;", (this_genre,))
                test = cursor.fetchone()
                if not test:  # No genre found
                    print("That ID doesn't exist")
                else:
                    genres.append(this_genre)
        except ValueError:
            print("That is not a valid id")
    conn.close()
    return genres, cont


def ask_windows_compatablity():
    """ask compatability with windows for add game"""
    cont = True
    while True:
        windows_ask = input("Is the game compatable with Windows? Y or N: ")
        if windows_ask == "/":
            cont = False
            break
        elif windows_ask == "Y":
            windows = 1
            break
        elif windows_ask == "N":
            windows = 0
            break
        else:
            print("Not a valid answer")
    return windows, cont


def ask_mac_compatability():
    """ask compatability with mac for add game"""
    cont = True
    while True:
        mac_ask = input("Is the game compatable with Mac? Y or N: ")
        if mac_ask == "/":
            cont = False
            break
        elif mac_ask == "Y":
            mac = 1
            break
        elif mac_ask == "N":
            mac = 0
            break
        else:
            print("Not a valid answer")
    return mac, cont


def ask_linux_compatability():
    """ask compatability with linux for add game"""
    cont = True
    while True:
        linux_ask = input("Is the game compatable with Linux? Y or N: ")
        if linux_ask == "/":
            cont = False
            break
        elif linux_ask == "Y":
            linux = 1
            break
        elif linux_ask == "N":
            linux = 0
            break
        else:
            print("Not a valid answer")
    return linux, cont


def ask_min_age():
    """ask for minimum age for adding to game"""
    cont = True
    while True:
        try:
            age = input("Minimum age to play (0 if no restriction): ")
            if age == "/":
                cont = False
                break
            else:
                age = int(age)
                if age < 0:
                    print("Not a valid age")
                else:
                    break
        except ValueError:
            print("Not a valid age")
    return age, cont


def ask_achievements():
    """ask for achievements for adding to game"""
    cont = True
    while True:
        try:
            achievements = input("Amount of available achievements: ")
            if achievements == "/":
                cont = False
                break
            elif len(achievements) > 9:
                print("Not a valid number")
            else:
                achievements = int(achievements)
                if achievements < 0:
                    print("Not a valid number")
                else:
                    break
        except ValueError:
            print("Not a valid number")
    return achievements, cont


def ask_pos_reviews():
    """ask for positive reviews for adding to game"""
    cont = True
    while True:
        try:
            reviews = input("Amount of positive reviews: ")
            if reviews == "/":
                cont = False
                break
            elif len(reviews) > 9:
                print("Not a valid number")
            else:
                reviews = int(reviews)
                if reviews < 0:
                    print("Not a valid number")
                else:
                    break
        except ValueError:
            print("Not a valid number")
    return reviews, cont


def ask_neg_reviews():
    """ask for negative reviews for adding to game"""
    cont = True
    while True:
        try:
            reviews = input("Amount of negative reviews: ")
            if reviews == "/":
                cont = False
                break
            elif len(reviews) > 9:
                print("Not a valid number")
            else:
                reviews = int(reviews)
                if reviews < 0:
                    print("Not a valid number")
                else:
                    break
        except ValueError:
            print("Not a valid number")
    return reviews, cont


def ask_median_playtime():
    """ask for median playtime for adding to game"""
    cont = True
    while True:
        try:
            playtime = input("Median playtime (hours): ")
            if playtime == "/":
                cont = False
                break
            elif len(playtime) > 9:
                print("Not a valid number")
            else:
                playtime = int(playtime)
                if playtime < 0:
                    print("Not a valid number")
                else:
                    break
        except ValueError:
            print("Not a valid number")
    return playtime, cont


def ask_average_playtime():
    """ask for average playtime for adding to game"""
    cont = True
    while True:
        try:
            playtime = input("Average playtime (hours): ")
            if playtime == "/":
                cont = False
                break
            elif len(playtime) > 9:
                print("Not a valid number")
            else:
                playtime = int(playtime)
                if playtime < 0:
                    print("Not a valid number")
                else:
                    break
        except ValueError:
            print("Not a valid number")
    return playtime, cont


def ask_price():
    """ask for price for adding to game"""
    cont = True
    while True:
        try:
            price = input("Price (NZD): $")
            if price == "/":
                cont = False
                break
            elif len(price) > 9:
                print("Not a valid number")
            else:
                price = float("%.2f" % (float(price)))
                if price < 0:
                    print("Not a valid number")
                else:
                    break
        except ValueError:
            print("Not a valid number")
    return price, cont


def delete_game():
    """Delete a game and the associated rows in bridging tables"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cont = True
    print("Make sure you know the ID of the game, type / to cancel.")
    while True:
        try:  # in case not int
            game_id = input("ID of game: ")
            if game_id != "/":
                game_id = int(game_id)
                # test if it exists
                cursor.execute("SELECT name FROM Game WHERE id = ?;", (game_id,))
                test = cursor.fetchone()
                if not test:
                    print("That ID doesn't exist")
                else:
                    while True:
                        confirm = input(f"Are you sure you want to delete {test[0]}? Y/N: ")
                        if confirm == "Y":  # Yes delete
                            break
                        elif confirm == "N":  # Don't delete
                            break
                        else:
                            print("Invalid answer")
                    if confirm == "Y":
                        # genre
                        cursor.execute("DELETE FROM GameGenre WHERE gameid = ?;", (game_id,))
                        conn.commit()
                        # developer
                        cursor.execute("DELETE FROM GameDeveloper WHERE gameid = ?;", (game_id,))
                        conn.commit()
                        # publisher
                        cursor.execute("DELETE FROM GamePublisher WHERE gameid = ?;", (game_id,))
                        conn.commit()
                        # game
                        cursor.execute("DELETE FROM Game WHERE id = ?;", (game_id,))
                        conn.commit()
                    break
            else:
                break
        except ValueError:
            print("Not a valid ID")

    conn.close()


def update_game():
    """Update a part of the game data"""
    # should only need reviews, playtime, achievements, platforms, age + price
    # since the rest isn't subject to change
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cont = True

    print("Type / at any time to cancel")
    # asking game
    while True:
        try:
            game_id = input("ID of game: ")
            if game_id == "/":
                cont = False
                break
            else:
                game_id = int(game_id)
                cursor.execute("SELECT name FROM Game WHERE id = ?;", (game_id,))
                game_name = cursor.fetchone()
                if not game_name:
                    print("That game doesn't exist")
                else:
                    while True:  # ask confirmation
                        check = input(f"Are you sure you want to update {game_name[0]}? Y/N: ")
                        if check == "Y":
                            break
                        elif check == "N":
                            cont = False
                            break
                        else:
                            print("Not a valid command")
                    break
        except ValueError:
            print("Not a valid ID")

    if cont is True:
        print("-"*DASHES_FOR_SEPARATORS)
        print("1  - Windows compatability")
        print("2  - Mac compatability")
        print("3  - Linux compatability")
        print("4  - Age rating")
        print("5  - Achievements")
        print("6  - Negative reviews")
        print("7  - Postitive reviews")
        print("8  - Average playtime")
        print("9  - Median playtime")
        print("10 - Price")
        print("-"*DASHES_FOR_SEPARATORS)

        while True:  # until input valid command
            try:  # making into int
                ask = input("Which part must be updated: ")
                if ask == "/":
                    cont = False
                    break
                else:
                    ask = int(ask)
                    if ask < 1 or ask > 10:
                        print("Not a valid command")
                    else:
                        break
            except ValueError:
                print("Not a valid command")

        if cont is True:
            if ask == 1:  # windows compatability
                new, cont = ask_windows_compatablity()
                if cont is True:
                    cursor.execute("UPDATE Game \
                                    SET windowscompat = ? \
                                    WHERE id = ?;",
                                   (new, game_id))
                    conn.commit()
            elif ask == 2:  # mac compatability
                new, cont = ask_mac_compatability()
                if cont is True:
                    cursor.execute("UPDATE Game \
                                    SET maccompat = ? \
                                    WHERE id = ?;",
                                   (new, game_id))
                    conn.commit()
            elif ask == 3:  # linux compatability
                new, cont = ask_linux_compatability()
                if cont is True:
                    cursor.execute("UPDATE Game \
                                    SET linuxcompat = ? \
                                    WHERE id = ?;",
                                   (new, game_id))
                    conn.commit()
            elif ask == 4:  # min age
                new, cont = ask_min_age()
                if cont is True:
                    cursor.execute("UPDATE Game \
                                    SET minage = ? \
                                    WHERE id = ?;",
                                   (new, game_id))
                    conn.commit()
            elif ask == 5:  # achievements
                print("Please write new total, not how many more or less")
                new, cont = ask_achievements()
                if cont is True:
                    cursor.execute("UPDATE Game \
                                    SET achievments = ? \
                                    WHERE id = ?;",
                                   (new, game_id))
                    conn.commit()
            elif ask == 6:  # negative reviews
                print("Please write new total, not how many more")
                new, cont = ask_neg_reviews()
                if cont is True:
                    cursor.execute("UPDATE Game \
                                    SET negreviews = ? \
                                    WHERE id = ?;",
                                   (new, game_id))
                    conn.commit()
            elif ask == 7:  # positive reviews
                print("Please write new total, not how many more")
                new, cont = ask_pos_reviews()
                if cont is True:
                    cursor.execute("UPDATE Game \
                                    SET posreviews = ? \
                                    WHERE id = ?;",
                                   (new, game_id))
                    conn.commit()
            elif ask == 8:  # average playtime
                new, cont = ask_average_playtime()
                if cont is True:
                    cursor.execute("UPDATE Game \
                                    SET averageplaytime = ? \
                                    WHERE id = ?;",
                                   (new, game_id))
                    conn.commit()
            elif ask == 9:  # median playtime
                new, cont = ask_median_playtime()
                if cont is True:
                    cursor.execute("UPDATE Game \
                                    SET medianplaytime = ? \
                                    WHERE id = ?;",
                                   (new, game_id))
                    conn.commit()
            elif ask == 10:  # price
                new, cont = ask_price()
                if cont is True:
                    cursor.execute("UPDATE Game \
                                    SET price = ? \
                                    WHERE id = ?;",
                                   (new, game_id))
                    conn.commit()

    conn.close()


def menu():
    """menu to access all other functions"""
    cont = True
    print("-"*DASHES_FOR_SEPARATORS)
    print("1  - View data on one game")
    print("2  - Show all genres")
    print("3  - Show all developers")
    print("4  - Show all publishers")
    print("5  - Show all games in one genre")
    print("6  - Show all games by one developer")
    print("7  - Show all games by one publisher")
    print("8  - Search game by name")
    print("9  - Search developer by name")
    print("10 - Search publisher by name")
    print("11 - Exit program")
    print("-"*DASHES_FOR_SEPARATORS)
    while True:
        command = input("\nInput command: ")
        if command == "1":  # View one game
            while True:
                try:
                    id = int(input("ID of game: "))
                    if len(str(id)) > 9:
                        print("Not a valid ID")
                    elif id < 1:
                        print("Not a valid ID")
                    else:
                        read_one(id)
                        break
                except ValueError:
                    print("Not a valid ID")
            break
        elif command == "2":  # Show genres
            show_genres()
            break
        elif command == "3":  # Show developers
            show_developers()
            break
        elif command == "4":  # Show publishers
            show_publishers()
            break
        elif command == "5":  # Show in genre
            while True:
                try:
                    id = int(input("ID of genre: "))
                    if len(str(id)) > 9:
                        print("Not a valid ID")
                    elif id < 1:
                        print("Not a valid ID")
                    else:
                        show_in_genre(id)
                        break
                except ValueError:
                    print("Not a valid ID")
            break
        elif command == "6":  # Show in dev
            while True:
                try:
                    id = int(input("ID of developer: "))
                    if len(str(id)) > 9:
                        print("Not a valid ID")
                    elif id < 1:
                        print("Not a valid ID")
                    else:
                        show_in_dev(id)
                        break
                except ValueError:
                    print("Not a valid ID")
            break
        elif command == "7":  # Show in publisher
            while True:
                try:
                    id = int(input("ID of publisher: "))
                    if len(str(id)) > 9:
                        print("Not a valid ID")
                    elif id < 1:
                        print("Not a valid ID")
                    else:
                        show_in_publisher(id)
                        break
                except ValueError:
                    print("Not a valid ID")
            break
        elif command == "8":  # search game by name
            search_game_by_name()
            break
        elif command == "9":  # search dev by name
            search_dev_by_name()
            break
        elif command == "10":  # search publisher by name
            search_publisher_by_name()
            break
        elif command == "11":  # exit program
            cont = False
            break
        else:
            print("Invalid command")
    return cont


if __name__ == "__main__":
    cont = True
    while cont is True:
        cont = menu()

# All the functions for copy-pasting
# read = input("Id of game: ")
# read_one(read)
# show_genres()
# show_developers()
# show_publishers()
# genre_id = int(input("Id of genre: "))
# show_in_genre(genre_id)
# dev_id = int(input("Id of developer: "))
# show_in_dev(dev_id)
# publisher_id = int(input("Id of publisher: "))
# show_in_publisher(publisher_id)
# search_game_by_name()
# search_dev_by_name()
# search_publisher_by_name()
# add_dev()
# add_publisher()
# add_genre()
# add_game()
# delete_game()
# update_game()
