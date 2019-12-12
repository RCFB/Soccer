def team_wins_match(team_id, match):
  return  (match['team0'] == team_id and match['score0'] > match['score1']) or \
          (match['team1'] == team_id and match['score0'] < match['score1'])


def team_loses_match(team_id, match):
  return  (match['team0'] == team_id and match['score0'] < match['score1']) or \
          (match['team1'] == team_id and match['score0'] > match['score1'])

def team_makes_a_draw(team_id, match):
  return  (match['team0'] == team_id and match['score0'] == match['score1']) or \
          (match['team1'] == team_id and match['score0'] == match['score1'])


def goals_for(team_id, match):
  return match['score0'] if match['team0'] ==team_id else \
         match['score1'] if match['team1'] ==team_id else \
         0




def goals_against(team_id, match):
  return match['score1'] if match['team0'] == team_id else \
         match['score0'] if match['team1'] == team_id else \
         0


def ranking_row(team, matches):
  team_id = team['id']
  n_won_match_count = sum (team_wins_match(team_id, match) for match in matches)
  n_lost_match_count = sum (team_loses_match(team_id, match) for match in matches)
  n_draw_match_count = sum (team_makes_a_draw(team_id, match) for match in matches)
  n_match_played_count = n_won_match_count + n_lost_match_count + n_draw_match_count
  n_goals_for = sum (goals_for(team_id, match) for match in matches)
  n_goals_against = sum (goals_against(team_id, match) for match in matches)
  n_goal_difference = n_goals_for - n_goals_against
  n_points = 3*n_won_match_count + n_draw_match_count
  return {'team' : team,
  'stats': {
    'match_played_count': n_match_played_count,
    'points':             n_points,
    'won_match_count':    n_won_match_count, 
    'lost_match_count':   n_lost_match_count, 
    'draw_match_count':   n_draw_match_count, 
    'goals_for':          n_goals_for, 
    'goals_against':      n_goals_against, 
    'goal_difference':    n_goal_difference}}

def compare_key(row):
  return (row['stats']['points'], row['stats']['goal_difference'])

def ranking(teams, matches):
  rows = [ranking_row(team, matches) for team in teams]
  return sorted(rows, key=compare_key, reverse=True)


if __name__ == "__main__":
  from pprint import pprint
  from soccer_static_model import teams, matches
  pprint(ranking(teams(), matches()))
  