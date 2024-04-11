''' code made by daniel streletsky 25/5/23'''
import sqlite3

DATABASE_FILE = "betting.db"

# Function for checking if the user exists in the database
def check_user(connection, name):
    with connection:
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM user WHERE name = '{name}'")
        result = cursor.fetchone()
        return result is not None

# Function for checking user balance
def check_balance(connection, name):
    with connection:
        cursor = connection.cursor()
        cursor.execute(f"SELECT balance FROM user WHERE name = '{name}'")
        result = cursor.fetchone()
        return result[0] if result else 0

# Function for getting the sports name from the database
def sports_name(connection):
    with connection:
        cursor = connection.cursor()
        cursor.execute("SELECT sports_name FROM sport")
        results = cursor.fetchall()
        sports = [result[0] for result in results]
        return sports

# Function for defining team name
def team_name(connection, sport_id):
    with connection:
        cursor = connection.cursor()
        cursor.execute(f"SELECT teamname FROM team WHERE team_id = {sport_id}")
        results = cursor.fetchall()
        teams = [result[0] for result in results]
        return teams

# Function for updating the user's balance
def update_balance(connection, name, amount):
    with connection:
        balance = check_balance(connection, name)
        new_balance = balance + amount
        if new_balance < 0:
            print("Balance can't go below 0")
        elif new_balance > 10000:
            print("Too much money")
        else: #update the account when a bet has been made and will apper in the update history 
            cursor = connection.cursor()
            cursor.execute(f"UPDATE user SET balance = balance + {amount} WHERE name = '{name}'")
            cursor.execute(f"INSERT INTO betting_history (user_id, date, amount) VALUES ('{name}', DATE('now'), {amount})")
   #displays account history         
def display_betting_history(connection, name):
    with connection:
        cursor = connection.cursor()
        cursor.execute(f"SELECT date, amount FROM betting_history WHERE user_id = '{name}'")
        results = cursor.fetchall()
        if results:# displays the data nicely 
            print("Account History")
            print("Date\t\t Amount")
            for result in results:
                date,amount = result
                print(f"{date}\t{amount}")
        else:
            print("No betting history found.")




# Connection with the database
with sqlite3.connect(DATABASE_FILE) as connection:
    while True:
        user_input = input("\nHello, welcome to high school betting\n1. Enter\n2. Exit\n")
        if user_input == "1":
            name = input("Please enter your name: ")
            if check_user(connection, name):
                balance = check_balance(connection, name)
                print("Hello " + name + ", your balance is $" + str(balance))
                while True:
                    user = input("\nWhat would you like to do?\n1. Bet\n2. Update account\n3. See Balance\n4. Account History\n5. Exit\n")
                    if user == "2":
                        amount = int(input("How much money would you like to put in your account? "))
                        update_balance(connection, name, amount)
                        balance = check_balance(connection, name)
                        print("Your new balance is $" + str(balance))
                    elif user == "3":
                        show_amount = check_balance(connection, name)
                        print("Your Current balance is $" + str(balance))
                    elif user == "4":
                        display_betting_history(connection, name)
                    elif user == "5":
                        print("Goodbye")
                        break
                    elif user == "1":
                        sports = sports_name(connection)
                        print("\nAvailable sports")
                        for index, sport_name in enumerate(sports, start=1):
                            print(f"{index}. {sport_name}")
                        selected_sport_index = input("Select the sport by entering the number: ")
                        try: #Display the sports choice nicley and doesent crash if an invalid input is entered
                            selected_sport_index = int(selected_sport_index) - 1
                            if 0 <= selected_sport_index < len(sports):
                                sport_id = selected_sport_index + 1
                                teams = team_name(connection, sport_id)
                                # See the vailable teams for the sport 
                                print(f"\n teams for {sports[selected_sport_index]}")
                                for team in teams:
                                    print(team)
                                bet_amount = int(input("How much would you like to bet on this team? "))
                                balance = check_balance(connection, name)
                                if bet_amount <= balance:
                                    update_balance(connection, name, -bet_amount)  # Deduct the bet amount from the balance
                                    print("Bet placed successfully.")
                                    # The else are for somthing that goes wrong they will print invaild input or somthing else
                                else:
                                    print("Insufficient balance to place the bet.")
                            else:
                                print("Invalid sport selection.")
                        except ValueError:
                            print("Invalid input. Please enter a number.")
            else:
                print("User not found. Please try again.")
                