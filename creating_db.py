import sqlite3
import json

with open('data.json', 'r') as h:
    data = json.load(h)
    db_conn = sqlite3.connect('girlies.db')
    cur = db_conn.cursor()
    # cоздаем первую таблицу с исполнителем и его айди
    cur.execute('''CREATE TABLE IF NOT EXISTS artists
                      (artist_id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL)''')
    artists = [
        {'artist_id': 1, 'name': 'Gracie Abrams'},
        {'artist_id': 2, 'name': 'Olivia Rodrigo'},
        {'artist_id': 3, 'name': 'Taylor Swift'}
    ]
    for artist in artists:
        cur.execute('INSERT INTO artists (artist_id, name) VALUES (?, ?)', (artist['artist_id'], artist['name']))

    # вторая таблица с песнями исполнителей, информация из файла джисон:
    cur.execute('''CREATE TABLE IF NOT EXISTS songs
                      (song_id INTEGER PRIMARY KEY,
                       artist_id INTEGER NOT NULL,
                       song_name TEXT NOT NULL,
                       song_lyrics TEXT NOT NULL,
                       release_date TEXT,
                       genius_link TEXT NOT NULL,
                       pic TEXT NOT NULL,
                       FOREIGN KEY (artist_id) REFERENCES artists(artist_id))''')  # соединяем таблицы через айди
    # исполнителя

    for song in data:
        cur.execute('INSERT INTO songs (artist_id, song_name, song_lyrics, release_date, genius_link, pic) '
                    'VALUES (?, ?, ?, ?, ?, ?)', (song['artist_id'], song['song_name'], song['song_lyrics'],
                                                  song['release_date'], song['genius_link'], song['pic']))

db_conn.commit()
db_conn.close()
