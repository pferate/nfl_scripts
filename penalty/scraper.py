from bs4 import BeautifulSoup
from collections import namedtuple
from pprint import pprint
import requests

import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, iplot

import numpy as np
import matplotlib.pyplot as plt


# init_notebook_mode()

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
    against = {'Total Count': [], 'Off Count': [], 'Def Count': [], 'ST Count': []}
    beneficiary = {'Total Count': [], 'Off Count': [], 'Def Count': [], 'ST Count': []}
    for i in range(1, 17):
        penalties_against = team_stats.penalties.against.get(i)
        penalties_beneficiary = team_stats.penalties.beneficiary.get(i)
        if penalties_against:
            bar_title.append(penalties_against['Opponent'])
            for category in against.keys():
                against[category].append(penalties_against[category])
            for category in beneficiary.keys():
                beneficiary[category].append(penalties_beneficiary[category])
        else:
            bar_title.append('')
            for category in against.keys():
                against[category].append(0)
            for category in beneficiary.keys():
                beneficiary[category].append(0)
    print(bar_title)
    pprint(against)
    pprint(beneficiary)
    print(max(against['Total Count']))
    print(max(beneficiary['Total Count']))
    max_penalty_count = max(against['Total Count'] + beneficiary['Total Count'])
    print(max_penalty_count)
    ceiling = (((max_penalty_count // 5) + 1) * 5) + 1
    print('ceiling: ', ceiling)

    ind = np.arange(16)
    width = 0.35

    pa1 = plt.bar(ind, against['Off Count'], width, color='#FF0000')
    pa2 = plt.bar(ind, against['Def Count'], width, color='#660000', bottom=against['Off Count'])
    pa3 = plt.bar(ind, against['ST Count'], width, color='#CC0000',
                  bottom=[x + y for x, y in zip(against['Off Count'], against['Def Count'])])

    pb1 = plt.bar(ind + width, beneficiary['Off Count'], width, color='#33FF00')
    pb2 = plt.bar(ind + width, beneficiary['Def Count'], width, color='#006600', bottom=beneficiary['Off Count'])
    pb3 = plt.bar(ind + width, beneficiary['ST Count'], width, color='#00CC00',
                  bottom=[x + y for x, y in zip(beneficiary['Off Count'], beneficiary['Def Count'])])

    plt.ylabel('Penalties')
    plt.title('Penalties Against {}'.format(team_stats.team))
    plt.xticks(ind + width / 2., bar_title, rotation=90)
    plt.yticks(np.arange(0, ceiling, 5))
    plt.legend((pa1[0], pa2[0], pa3[0], pb1[0], pb2[0], pb3[0]),
               ('Off', 'Def', 'ST', 'Opp. Off', 'Opp. Def', 'Opp. ST'))

    print(plt.margins())
    plt.subplots_adjust(bottom=0.25)
    # plt.margins(y=0.5)
    # print(plt.margins())

    # plt.show()
    plt.savefig('foo.png')

    # trace0 = go.Bar(
    #     x=bar_title,
    #     y=against,
    #     name='Against {}'.format(team_stats.team),
    #     marker=dict(
    #         color='rgb(49,130,189)'
    #     )
    # )
    # trace1 = go.Bar(
    #     x=bar_title,
    #     y=beneficiary,
    #     name='Benefitting {}'.format(team_stats.team),
    #     marker=dict(
    #         color='rgb(204,204,204)',
    #     )
    # )
    # data = [trace0, trace1]
    # layout = go.Layout(
    #     xaxis=dict(
    #         # set x-axis' labels direction at 45 degree angle
    #         tickangle=-45,
    #     ),
    #     barmode='group',
    # )
    # fig = dict(data=data, layout=layout)
    # return iplot(fig)
    # # fig = go.Figure(data=data, layout=layout)
    # # plot_url = py.plot(fig, filename='2015 NFL Penalties/{}'.format(team_stats.team), auto_open=False)
    # # return plot_url


def plotly_penalty_total_count(team_stats):
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

    TEAMS = {'Seattle': 'seattle-seahawks', }
    for team in TEAMS.keys():
        print(team, end="\t")
        plot_url = plot_penalty_total_count(get_team_stats(team))
        print(plot_url)
