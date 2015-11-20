from bs4 import BeautifulSoup
from collections import namedtuple
from pprint import pprint
import requests

import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, iplot


init_notebook_mode()

PANLTY_TRACKER_URL = 'http://www.nflpenalties.com/team/{team}?year={year}&view=games'

# using team_location_to_url_name() to dynamically get mapping.
TEAMS = {
    'Arizona': 'arizona-cardinals',
    'Atlanta': 'atlanta-falcons',
    'Baltimore': 'baltimore-ravens',
    'Buffalo': 'buffalo-bills',
    'Carolina': 'carolina-panthers',
    'Chicago': 'chicago-bears',
    'Cincinnati': 'cincinnati-bengals',
    'Cleveland': 'cleveland-browns',
    'Dallas': 'dallas-cowboys',
    'Denver': 'denver-broncos',
    'Detroit': 'detroit-lions',
    'Green Bay': 'green-bay-packers',
    'Houston': 'houston-texans',
    'Indianapolis': 'indianapolis-colts',
    'Jacksonville': 'jacksonville-jaguars',
    'Kansas City': 'kansas-city-chiefs',
    'Miami': 'miami-dolphins',
    'Minnesota': 'minnesota-vikings',
    'N.Y. Giants': 'new-york-giants',
    'N.Y. Jets': 'new-york-jets',
    'New England': 'new-england-patriots',
    'New Orleans': 'new-orleans-saints',
    'Oakland': 'oakland-raiders',
    'Philadelphia': 'philadelphia-eagles',
    'Pittsburgh': 'pittsburgh-steelers',
    'San Diego': 'san-diego-chargers',
    'San Francisco': 'san-francisco-49ers',
    'Seattle': 'seattle-seahawks',
    'St. Louis': 'st-louis-rams',
    'Tampa Bay': 'tampa-bay-buccaneers',
    'Tennessee': 'tennessee-titans',
    'Washington': 'washington-redskins',
}


Penalties = namedtuple('Penalties', ['against', 'beneficiary'])
GamePenalties = namedtuple('GamePenalties', ['opponent', 'date', 'week', 'outcome', 'total_count',
                                             'total_yards', 'off_count', 'off_yards', 'def_count',
                                             'def_yards', 'st_count', 'st_yards'])
TeamStats = namedtuple('TeamStats', ['team', 'url_name', 'url', 'penalties'])


def print_team_mappings():
    """
    Prints a `<Name>: <url-name>,` mapping of NFL teams.
    This was used to copy-paste team names for dictionary mapping.
    It is an additional GET request for each team, but it should work in case the site changes syntax.
    """
    r = requests.get('http://www.nflpenalties.com/?year=2015')
    soup = BeautifulSoup(r.text, 'html.parser')
    teams = {}
    for row in soup.find_all('tr'):
        links = row.find_all('a')
        if links:
            teams[links[0].string] = "'{}': '{}',".format(links[0].string,
                                                          links[0]['href'].split('?')[0].split('/')[2])
    # for team in sorted(teams.keys()):
    #     print(teams[team])


def team_location_to_url_name(team):
    """
    Look up team url name from a team location name.
    The lookup name is the city/state name of the team, except for 'N.Y. Giants' and 'N.Y. Jets'.

    Raises a KeyError when team cannot be found.
    """
    # r = requests.get('http://www.nflpenalties.com/?year=2015')
    # soup = BeautifulSoup(r.text, 'html.parser')
    # for row in soup.find_all('tr'):
    #     links = row.find_all('a')
    #     if links and links[0].string.lower() == team.lower():
    #         return links[0]['href'].split('?')[0].split('/')[2]
    # raise KeyError('Team not found.', team)
    return TEAMS[team]


def sanitize_header(header):
    """
    Sanitize header.
    Converts UPPERCASE to lowercase and spaces to underscores.
    """
    return header.lower().replace(' ', '_')


def sanitize_column(data):
    """"
    Sanitize column.
    Converts integer strings to int.
    """
    if data and data.isdigit():
        return int(data)
    return data


def process_table(table):
    penalty_header = []
    for header in table.find_all('th'):
        penalty_header.append(header.string)
    game_outcomes = {}
    for game in table.find_all('tr'):
        row_data = [sanitize_column(i.string) for i in game.find_all('td')]
        if row_data and row_data[0] != 'Totals':
            # print(dict(zip(penalty_header, row_data)))
            # game_penalties = GamePenalties._make(row_data)
            # game_outcomes[game_penalties.week] = game_penalties
            game_penalties = dict(zip(penalty_header, row_data))
            # print(game_penalties)
            game_outcomes[game_penalties['Week']] = game_penalties
    return game_outcomes


def get_all_penalties(penalty_tables):
    return Penalties(process_table(penalty_tables[0]), process_table(penalty_tables[1]))


def get_team_stats(team):
    team_url_name = team_location_to_url_name(team)
    team_url = PANLTY_TRACKER_URL.format(team=team_url_name, year='2015')
    r = requests.get(team_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    penalty_tables = soup.find_all('table')

    team_stats = TeamStats(team, team_url_name, team_url, get_all_penalties(penalty_tables))

    return team_stats


def plot_penalty_total_count(team_stats):
    bar_title = []
    against = []
    beneficiary = []
    for i in range(1, 17):
        penalties_against = team_stats.penalties.against.get(i)
        penalties_beneficiary = team_stats.penalties.beneficiary.get(i)
        if penalties_against:
            bar_title.append(penalties_against['Opponent'])
            against.append(penalties_against['Total Count'])
            beneficiary.append(penalties_beneficiary['Total Count'])
        else:
            bar_title.append('')
            against.append(0)
            beneficiary.append(0)
    trace0 = go.Bar(
        x=bar_title,
        y=against,
        name='Against {}'.format(team_stats.team),
        marker=dict(
            color='rgb(49,130,189)'
        )
    )
    trace1 = go.Bar(
        x=bar_title,
        y=beneficiary,
        name='Benefitting {}'.format(team_stats.team),
        marker=dict(
            color='rgb(204,204,204)',
        )
    )
    data = [trace0, trace1]
    layout = go.Layout(
        xaxis=dict(
            # set x-axis' labels direction at 45 degree angle
            tickangle=-45,
        ),
        barmode='group',
    )
    fig = dict(data=data, layout=layout)
    return iplot(fig)
    # fig = go.Figure(data=data, layout=layout)
    # plot_url = py.plot(fig, filename='2015 NFL Penalties/{}'.format(team_stats.team), auto_open=False)
    # return plot_url


def plot_all_teams():
    for team in TEAMS.keys():
        # print(team, end='\t')
        plot_url = plot_penalty_total_count(get_team_stats(team))
        # print(plot_url)


if __name__ == '__main__':
    # this_team = 'Seattle'

    # all_team_stats = {}

    # all_team_stats[this_team] = get_team_stats(this_team)

    # for week, game_penalties in all_team_stats[this_team].penalties.against.items():
    #     print(week, game_penalties['Opponent'])
    #     all_team_stats[game_penalties['Opponent']] = get_team_stats(game_penalties['Opponent'])
    # pprint(all_team_stats)

    # for team in all_team_stats:
    #     plot_penalty_total_count(all_team_stats[team])

    # from plotly import __version__
    # print(__version__)
    # init_notebook_mode()

    for team in TEAMS.keys():
        print(team, end="\t")
        plot_url = plot_penalty_total_count(get_team_stats(team))
        print(plot_url)
