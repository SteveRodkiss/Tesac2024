import sqlite3


if __name__ == '__main__':
    #connect to the chinook code file- 
    # NB. it's relative to the folder I have open in VSCODE!!!!
    db = sqlite3.connect('Tutorial\chinook.db')
    #get cursor
    cursor = db.cursor()
    #execute a simple SQL statement on it
    cursor.execute('SELECT * FROM tracks')
    #get all the results
    results = cursor.fetchall()
    #print them- to see if it worked
    print(results)