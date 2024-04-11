import sqlite3

DATABASE = 'Tutorial\chinook.db'


def print_artists_starting_with(first_letter):
    with sqlite3.connect(DATABASE) as db:
        cursor = db.cursor()
        cursor.execute('''SELECT * FROM artists
                       WHERE name LIKE ?''', (first_letter + '%',))
        artists = cursor.fetchall()
        print("ID    Artist Name")
        for artist in artists:
            print(f"{artist[0]:<6}{artist[1]:<20}")
    #the context means it will automatically be closed- no need for db.close()


def print_tracks_by_artist(id):
    with sqlite3.connect(DATABASE) as db:
        cursor = db.cursor()
        #cool query to get a specific artist's tracks
        #note the use of the question mark! This is to stop
        #anyone doing SQL injection- and the TUPLE is the 2nd
        #parameter of the execute function
        cursor.execute('''SELECT * FROM tracks
                        JOIN albums ON tracks.AlbumId=albums.AlbumId
                        WHERE albums.ArtistId = ? ''', (id,))
        tracks = cursor.fetchall()
        #print em nicely
        print("ID    Track Name")
        for track in tracks:
            print(f"{track[0]:<6}{track[1]:<20}")
    #the context means it will automatically be closed- no need for db.close()


if __name__ == '__main__':
    #ask the user to choose an artist
    first_letter = input('''
                         \nSearch for artist:
                         \nType First Letter of artist you'd like to find:''')
    print_artists_starting_with(first_letter)
    id = input("Type the ID of an artist you'd like to see the tracks for:\n")
    #do magic
    print_tracks_by_artist(id)