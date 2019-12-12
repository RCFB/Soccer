
from . import app
from . import soccer_ranking, soccer_model
from flask import render_template

@app.route('/')
@app.route('/ranking')
def show_ranking():
    teams = soccer_model.teams()
    matches = soccer_model.matches()
    ranking = soccer_ranking.ranking(teams, matches)
    return render_template('ranking.html', ranking=ranking)


@app.route('/team/<int:team_id>')
def show_team(team_id):
    team = soccer_model.team(team_id)
    matches = soccer_model.matches()
    row = soccer_ranking.ranking_row(team, matches)
    played_matches = soccer_model.matches_played_by(team_id)
    return render_template('team.html', 
                                team=team,
                                row=row,
                                played_matches=played_matches)

