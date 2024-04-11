import sqlite3

DATABASE = 'Tutorial\chinook.db'


def print_all_artists():
    with sqlite3.connect(DATABASE) as db:
        cursor = db.cursor()
        cursor.execute('SELECT * FROM artists')
        artists = cursor.fetchall()
        print("ID    Artist Name")
        for artist in artists:
            print(f"{artist[0]:<6}{artist[1]:<20}")
    #the context means it will automatically be closed- no need for db.close()


if __name__ == '__main__':
    print_all_artists()