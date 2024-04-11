import sqlite3
DATABASE_FILE = "league.db"
def print_random_champion_from_role(role_id):
    #random champion from a selected role
    db = sqlite3.connect(DATABASE_FILE)
    cursor = db.cursor()
    sql = "SELECT champion_id, champion_name, release_date, difficulty FROM champion WHERE role_id = ? ORDER BY RANDOM() LIMIT 1"
    cursor.execute(sql, (role_id,))
    result = cursor.fetchone()
    
    if result:
        champion_id, champion_name, release_date, difficulty = result
        print(f"Random Champion under Role ID {role_id}:")
        print(f"Champion ID: {champion_id}, Name: {champion_name}, Released on: {release_date}, Champion difficiculty:{difficulty}")
    else:
        print(f"No champions found under Role ID {role_id}")
    
    db.close()

def show_roles():
    #function to shnow all the roles to user
    db = sqlite3.connect(DATABASE_FILE)
    cursor = db.cursor()
    sql = "SELECT * FROM role"
    cursor.execute(sql)
    results = cursor.fetchall()
   
    print("Here are all the available Roles:")
    for role in results:
        print(f"Role ID: {role[0]}, Role Name: {role[1]}")
   
    db.close()

def print_champions_by_role(role_id):
    #shows all the champions in a role given by the user
    db = sqlite3.connect(DATABASE_FILE)
    cursor = db.cursor()
    sql = "SELECT * FROM champion WHERE role_id = ?"
    cursor.execute(sql, (role_id,))
    results = cursor.fetchall()
   
    print(f"Champions under Role ID {role_id}:")
    for champion in results:
        print(f"Champion ID: {champion[0]}, Name: {champion[1]}, Released on: {champion[2]}, Difficulty: {champion[3]} ")
   
    db.close()

def print_old_to_new_champions():
#print out all champions starting oldest releast date to earliest
    db = sqlite3.connect(DATABASE_FILE)
    cursor = db.cursor()
    #getting all chanpion names
    sql = "SELECT * FROM champion ORDER BY release_date ASC;"
    cursor.execute(sql)
    results = cursor.fetchall()
    #prints prints out champion name, release date, and difficulty
    for champions in results:
        print(f"{champions[1]}, {champions[2]}, {champions[3]}")
    db.close()

def print_new_to_old_champions():
#print out all champions by release date new to old
    db = sqlite3.connect(DATABASE_FILE)
    cursor = db.cursor()
    #getting all chanpion names
    sql = "SELECT * FROM champion ORDER BY release_date DESC;"
    cursor.execute(sql)
    results = cursor.fetchall()
    #prints prints out champion name, release date, and difficulty
    for champions in results:
        print(f"{champions[1]}, {champions[2]}, {champions[3]}")
    db.close()


def print_easiest_champions():
#print out all champions starting at the top alphabetically
    db = sqlite3.connect(DATABASE_FILE)
    cursor = db.cursor()
    #getting all chanpion names
    sql = "SELECT * FROM champion ORDER BY difficulty ASC;"
    cursor.execute(sql)
    results = cursor.fetchall()
    #prints prints out champion name, release date, and difficulty
    for champions in results:
        print(f"{champions[1]}, {champions[2]}")
    db.close()

def print_hardest_champions():
#print out all championsstarting at the bottom alphabetically
    db = sqlite3.connect(DATABASE_FILE)
    cursor = db.cursor()
    #getting all chanpion names
    sql = "SELECT * FROM champion ORDER BY difficulty DESC;"
    cursor.execute(sql)
    results = cursor.fetchall()
    #prints out champion name, release date, and difficulty
    for champions in results:
        print(f"{champions[1]}, {champions[2]}")
    db.close()


def print_champions_asc():
#print out all champions descending
    db = sqlite3.connect(DATABASE_FILE)
    cursor = db.cursor()
    #getting all chanpion names
    sql = "SELECT champion_name FROM champion ORDER BY champion_name ASC;"
    cursor.execute(sql)
    results = cursor.fetchall()
    #prints out only champion name
    for champions in results:
        print(champions[0])
    db.close()

def print_champions_desc():
#print out all champions descending
    db = sqlite3.connect(DATABASE_FILE)
    cursor = db.cursor()
    #getting all chanpion names
    sql = "SELECT champion_name FROM champion ORDER BY champion_name DESC;"
    cursor.execute(sql)
    results = cursor.fetchall()
    #prints out only champion name
    for champions in results:
        print(champions[0])
    db.close()

def print_random_champion():
#print out a random champion
    db = sqlite3.connect(DATABASE_FILE)
    cursor = db.cursor()
    #random number from 1 to 154
    sql = "SELECT champion_name FROM champion ORDER BY RANDOM() LIMIT 1;"
    cursor.execute(sql)
    results = cursor.fetchall()
    #prints out only champion name
    for champions in results:
        print(champions[0])
    db.close()

def print_roles():
#print out all champions
    db = sqlite3.connect(DATABASE_FILE)
    cursor = db.cursor()
    #getting all chanpion names
    sql = "SELECT roles FROM role"
    cursor.execute(sql)
    results = cursor.fetchall()
    #prints out only champion name
    for champions in results:
        print(champions[0])
    db.close()


while True:
    try:
        #main menu
        user_input = int(input("\nWhat do you want to do?\n1. See champions\n2. See all roles\n3. Exit\n"))

        # Submenu for seeing champions
        if user_input == 1:
            champion_input = input("\nWhat do you want to do?\n\
1. See all champions\n\
2. See a random champion\n\
3. Go back\n")

            # Submenu for seeing all champions in different ways
            if champion_input == "1":
                champion_all_input = input("\n\
1. See all champions alphabetically\n\
2. See all champions in reverse alphabetical order\n\
3. See all champions in one role\n\
4. Exit\n")

                # All functions for champion input 1
                # See all champions alphabetically
                if champion_all_input == "1":
                    print_champions_asc()
                    break
                # See all champions in reverse alphabetical order
                elif champion_all_input == "2":
                    print_champions_desc()
                    break
                # Seeing every champion of one role
                elif champion_all_input == "3":
                    show_roles()
                    while True:
                        try:
                            champion_by_role_input = int(input("Which role do you want to see every champion of?\n"))
                            if champion_by_role_input in range(1, 14):
                                print_champions_by_role(champion_by_role_input)
                                break
                            else:
                                print("Invalid role ID. Please enter a valid role ID.")
                        except ValueError:
                            print("Invalid input. Please enter a valid role ID as a number.")
                        break
                # Exit
                elif champion_all_input == "4":
                    print("Exiting, Have a good day!")
                    break
                else:
                    print("Invalid input. Please enter a valid option (1, 2, 3, or 4).")

            # random champion submenu, champion input 2
            elif champion_input == "2":
                random_champion_input = input("\n\
1. See a random champion\n\
2. See a random champion from a selected role\n\
3. Exit\n")

                # print random champion
                if random_champion_input == "1":
                    print_random_champion()
                    break
                #random champion from a role
                elif random_champion_input == "2":
                    show_roles()
                    while True:
                        try:
                            random_champion_role_input = int(input("Which role do you want to select a random champion from?\n"))
                            if random_champion_role_input in range(1, 14):
                                print_random_champion_from_role(random_champion_role_input)
                                break
                            else:
                                print("Invalid role ID. Please enter a valid role ID.")
                        except ValueError:
                            print("Invalid input. Please enter a valid role ID as a number.")
                    break
                elif random_champion_input == "3":
                    print("Have a nice day!")
                    break
                else:
                    print("Invalid input. Please enter a valid option (1, 2, or 3).")

        # Show roles
        elif user_input == 2:
            show_roles()
            break
        # Exit
        elif user_input == 3:
            print("Have a nice day!")
            break
        else:
            print("Invalid input. Please enter a valid option (1, 2, or 3).")
            continue
    #when you type something and are clumsy
    # error detection   
    except ValueError:
        print("Invalid input. Please enter a valid option as a number.")
        continue
