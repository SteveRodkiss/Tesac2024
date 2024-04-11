import sqlite3

DATABASE_FILE = "songs.db"

def show_songs():
    '''show all songs'''
    cursor = connection.cursor()
    sql = "SELECT * FROM song ORDER BY release_year"
    cursor.execute(sql) 
    results = cursor.fetchall()
    print (f"{'song_name':<20}{'artist_id' :<60}")
    for item in results:
        print (f"{item[1] :<20}{item[2] :<60}")




        with sqlite3.connect(DATABASE_FILE) as connection:
            show_songs(connection)