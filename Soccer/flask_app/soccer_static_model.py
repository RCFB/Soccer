import random
from datetime import datetime, timedelta
from collections import deque


def teams():
    return [{'id': 1, 'name': 'Paris'},
            {'id': 2, 'name': 'Marseille'},
            {'id': 3, 'name': 'Lyon'},
            {'id': 4, 'name': 'Toulouse'},
            {'id': 5, 'name': 'Nice'},
            {'id': 6, 'name': 'Nantes'},
            {'id': 7, 'name': 'Strasbourg'},
            {'id': 8, 'name': 'Montpellier'},
            {'id': 9, 'name': 'Bordeaux'},
            {'id': 10, 'name': 'Lille'},
            {'id': 11, 'name': 'Rennes'},
            {'id': 12, 'name': 'Reims'},
            {'id': 13, 'name': 'Le Havre'},
            {'id': 14, 'name': 'Gap'},
            {'id': 15, 'name': 'Toulon'},
            {'id': 16, 'name': 'Grenoble'},
            {'id': 17, 'name': 'Dijon'},
            {'id': 18, 'name': 'Angers'},
            {'id': 19, 'name': 'Nîmes'},
            {'id': 20, 'name': 'Villeurbanne'}]

def team(team_id):
    for team in teams():
        if team['id'] == team_id:
            return team

def autumn_dates():
    year = datetime.utcnow().year
    if datetime(year, 8, 4) >= datetime.now():
        year = year - 1
    date = datetime(year, 8, 4)
    date = date - timedelta(days=date.weekday())
    dates = []
    for _ in range(len(teams())-1):
        dates.append(date)
        date = date + timedelta(days=7)
    return dates


def spring_dates():
    year = datetime.utcnow().year
    if datetime(year, 8, 4) <= datetime.now():
        year = year + 1
    date = datetime(year, 1, 1)
    date = date - timedelta(days=date.weekday())
    dates = []
    for _ in range(len(teams())-1):
        dates.append(date)
        date = date + timedelta(days=7)
    return dates


def dates():
    return autumn_dates() + spring_dates()


def match(id, date, teams):
    return {
        'id': id,
        'team0': teams[0]['id'],
        'team1': teams[1]['id'],
        'team0_name' : teams[0]['name'],
        'team1_name' : teams[1]['name'],
        'score0': random.randint(0, 5),
        'score1': random.randint(0, 5),
        'date': date
    }


def matches():
    random.seed(1)
    matches = []
    teams_list = teams()
    teams1 = deque(teams_list[0:len(teams_list) // 2])
    teams2 = deque(teams_list[len(teams_list) // 2:len(teams_list)])
    random.shuffle(teams1)
    random.shuffle(teams2)
    swap = False
    for date in dates():
        last1 = teams1.pop()
        teams2.append(last1)
        first2 = teams2.popleft()
        first1 = teams1.popleft()
        teams1.appendleft(first2)
        teams1.appendleft(first1)
        swap = not swap
        for opponents in zip(teams1, teams2) if swap else zip(teams2, teams1):
            matches.append(match(len(matches), date, opponents))
    return matches



def matches_played_by(team_id):
    return [match for match in matches() if match['team0']==team_id or match['team1']==team_id]

def matchesPlayed(team_id):
    return [match for match in matches() if match['team0']==team_id or match['team1']==team_id]

if __name__ == "__main__":
    print(matches())
