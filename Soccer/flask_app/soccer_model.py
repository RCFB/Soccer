from .database import db, fetchall


def fill_db():
    from .soccer_static_model import teams, matches
    cursor = db.cursor()
    for team in teams():
        cursor.execute('''INSERT INTO teams(id, name)
        VALUES (:id, :name)''',team)

    for match in matches():
        cursor.execute('''INSERT INTO matches(id, date, team0, team1, score0, score1)
        VALUES (:id, :date, :team0, :team1, :score0, :score1)''',
        match)

    db.commit()

def team(team_id):
    cursor = db.cursor()
    cursor.execute('SELECT * FROM teams WHERE id = :id',
                { 'id' : team_id })
    result = fetchall(cursor)
    return result[0]

def teams():
    cursor = db.cursor()
    cursor.execute('SELECT * FROM teams')
    return fetchall(cursor)

def matches():
    cursor = db.cursor()
    cursor.execute('SELECT * FROM matches')
    return fetchall(cursor)


def matches_played_by(team_id):
    cursor = db.cursor()
    cursor.execute(
        '''SELECT * FROM matches_with_team_names
         WHERE team0 = :id OR team1 = :id
         ORDER BY date''',
         { 'id' : team_id })
    return fetchall(cursor)

