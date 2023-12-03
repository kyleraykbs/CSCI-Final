maps_directory="maps"

if [ ! -d "$maps_directory" ]; then
    chmod u=rwx,g=,o= maps
    mkdir "$maps_directory"
fi

if [ ! -f "players.db" ]; then
    sqlite3 players.db "CREATE TABLE players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        x INTEGER NOT NULL,
        y INTEGER NOT NULL,
        inventory TEXT,
        mapname TEXT NOT NULL
    );"
fi
