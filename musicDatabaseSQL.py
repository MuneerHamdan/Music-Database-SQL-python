import sqlite3

conn = sqlite3.connect("data.db")
cursor = conn.cursor()

# cursor.execute("DROP TABLE Artist")
cursor.execute('''CREATE TABLE Artist (
    artist_id INTEGER PRIMARY KEY,
    artist_name TEXT UNIQUE NOT NULL
);
''')

# cursor.execute("DROP TABLE Genre")
cursor.execute('''CREATE TABLE Genre (
    genre_id INTEGER PRIMARY KEY,
    genre_name TEXT UNIQUE NOT NULL
);
''')

# cursor.execute("DROP TABLE Song")
cursor.execute('''CREATE TABLE Song (
    song_id INTEGER PRIMARY KEY,
    song_title TEXT NOT NULL,
    artist_id INTEGER,
    release_date DATE,
    FOREIGN KEY (artist_id) REFERENCES Artist(artist_id),
    UNIQUE (song_title, artist_id)
);
''')

# cursor.execute("DROP TABLE SongGenre")
cursor.execute('''CREATE TABLE SongGenre (
    song_id INTEGER,
    genre_id INTEGER,
    PRIMARY KEY (song_id, genre_id),
    FOREIGN KEY (song_id) REFERENCES Song(song_id),
    FOREIGN KEY (genre_id) REFERENCES Genre(genre_id)
);
''')

# cursor.execute("DROP TABLE Album")
cursor.execute('''CREATE TABLE Album (
    album_id INTEGER PRIMARY KEY,
    album_name TEXT NOT NULL,
    artist_id INTEGER,
    release_date DATE,
    FOREIGN KEY (artist_id) REFERENCES Artist(artist_id),
    UNIQUE (album_name, artist_id)
);
''')

# cursor.execute("DROP TABLE User")
cursor.execute('''CREATE TABLE User (
    user_id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL
);
''')

# cursor.execute("DROP TABLE Playlist")
cursor.execute('''CREATE TABLE Playlist (
    playlist_id INTEGER PRIMARY KEY,
    playlist_title TEXT NOT NULL,
    creation_datetime DATETIME NOT NULL,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    UNIQUE (playlist_title, user_id)
);
''')

# cursor.execute("DROP TABLE PlaylistSong")
cursor.execute('''CREATE TABLE PlaylistSong (
    playlist_id INTEGER,
    song_id INTEGER,
    PRIMARY KEY (playlist_id, song_id),
    FOREIGN KEY (playlist_id) REFERENCES Playlist(playlist_id),
    FOREIGN KEY (song_id) REFERENCES Song(song_id)
);
''')

# cursor.execute("DROP TABLE Rating")
cursor.execute('''CREATE TABLE Rating (
    rating_id INTEGER PRIMARY KEY,
    rating_value INTEGER CHECK (rating_value BETWEEN 1 AND 5) NOT NULL,
    rating_date DATE NOT NULL,
    user_id INTEGER,
    album_id INTEGER,
    song_id INTEGER,
    playlist_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (album_id) REFERENCES Album(album_id),
    FOREIGN KEY (song_id) REFERENCES Song(song_id),
    FOREIGN KEY (playlist_id) REFERENCES Playlist(playlist_id),
    UNIQUE (user_id, album_id, song_id, playlist_id, rating_date)
);
''')

conn.commit()

cursor.execute("SELECT G.genre_name, COUNT(SG.song_id) AS number_of_songs FROM SongGenre SG JOIN Genre G ON SG.genre_id = G.genre_id GROUP BY SG.genre_id ORDER BY number_of_songs DESC LIMIT 3; ")

cursor.execute("SELECT DISTINCT A.artist_name FROM Artist A JOIN Song S ON A.artist_id = S.artist_id WHERE EXISTS (SELECT 1 FROM Album WHERE artist_id = A.artist_id ) AND EXISTS (SELECT 1 FROM Song WHERE artist_id = A.artist_id AND release_date IS NULL ); ")

cursor.execute("SELECT album_name, AVG(rating_value) AS average_user_rating FROM Rating R JOIN Album A ON R.album_id = A.album_id WHERE rating_date BETWEEN '1990-01-01' AND '1999-12-31' GROUP BY A.album_id ORDER BY average_user_rating DESC, album_name LIMIT 10;")

cursor.execute("SELECT G.genre_name, COUNT(R.song_id) AS number_of_song_ratings FROM Genre G JOIN SongGenre SG ON G.genre_id = SG.genre_id JOIN Rating R ON SG.song_id = R.song_id WHERE rating_date BETWEEN '1991-01-01' AND '1995-12-31' GROUP BY G.genre_id ORDER BY number_of_song_ratings DESC LIMIT 3;")

cursor.execute("SELECT U.username, P.playlist_title, AVG(R.rating_value) AS average_playlist_rating FROM User U JOIN Playlist P ON U.user_id = P.user_id LEFT JOIN Rating R ON P.playlist_id = R.playlist_id GROUP BY U.user_id, P.playlist_id HAVING AVG(R.rating_value) >= 4.0;")

cursor.execute("SELECT U.username, COUNT(R.rating_id) AS number_of_ratings FROM User U JOIN Rating R ON U.user_id = R.user_id GROUP BY U.user_id ORDER BY number_of_ratings DESC LIMIT 5;")

cursor.execute("SELECT A.artist_name, COUNT(S.song_id) AS number_of_songs FROM Artist A LEFT JOIN Song S ON A.artist_id = S.artist_id WHERE S.release_date BETWEEN '1990-01-01' AND '2010-12-31' OR S.release_date IS NULL GROUP BY A.artist_id ORDER BY number_of_songs DESC LIMIT 10;")

cursor.execute("SELECT S.song_title, COUNT(PS.playlist_id) AS number_of_playlists FROM Song S LEFT JOIN PlaylistSong PS ON S.song_id = PS.song_id GROUP BY S.song_id ORDER BY number_of_playlists DESC, S.song_title LIMIT 10;")

cursor.execute("SELECT S.song_title, A.artist_name, COUNT(R.rating_id) AS number_of_ratings FROM Song S JOIN Artist A ON S.artist_id = A.artist_id LEFT JOIN Rating R ON S.song_id = R.song_id WHERE S.release_date IS NULL GROUP BY S.song_id ORDER BY number_of_ratings DESC LIMIT 20;")

cursor.execute("SELECT DISTINCT A.artist_name FROM Artist A WHERE NOT EXISTS (SELECT 1 FROM Song WHERE artist_id = A.artist_id AND release_date > '1993-12-31') AND NOT EXISTS (SELECT 1 FROM Album WHERE artist_id = A.artist_id AND release_date > '1993-12-31');")
