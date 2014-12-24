from bs4 import BeautifulSoup
from collections import OrderedDict
from urllib.request import urlopen

from MarkdownOutput import MarkdownOutput
import NFL


def get_standings(playoffs=True):
    if playoffs:
        url = "http://espn.go.com/nfl/standings/_/type/playoffs"
        column_map = NFL.PLAYOFF_STANDINGS_COLUMNS_MAPPING
    else:
        url = "http://espn.go.com/nfl/standings"
        column_map = NFL.STANDINGS_COLUMNS_MAPPING
    page = urlopen(url).read()
    soup = BeautifulSoup(page)

    table = soup.find("table", {'class': 'tablehead'})

    # Parse Standings Table
    standings = {}
    conference = None

    for row in table.findAll("tr"):
        if row['class'][0] == 'stathead':
            conference = row.td.text
            standings[conference] = OrderedDict()
        elif row['class'][0] == 'colhead':
            stat_cols_raw = []
            stat_cols = []
            for col in row.findAll('td'):
                stat_cols_raw.append(col.text)
                stat_cols.append(column_map.get(col.text, col.text))
            if playoffs:
                team_container = standings[conference]
            else:
                division = stat_cols_raw[0]
                standings[conference][division] = OrderedDict()
                team_container = standings[conference][division]
        else:
            team_row = row.findAll('td')
            team_dict = {}
            for i in range(len(team_row)):
                team_dict[stat_cols[i]] = team_row[i].text.strip()
            # Split playoff prefixes to get the city name
            team_dict['TEAM'] = team_dict['TEAM'].split('-')[-1].strip()
            # Replace the city name for the subreddit link
            # team_dict['TEAM'] = NFL.TEAM_SUBREDDIT_MAP[team_dict['TEAM']]
            team_dict['TEAM'] = NFL.TEAM_SUBREDDIT_MAP.get(team_dict['TEAM'], team_dict['TEAM'])
            # team_container.append(team_dict)
            team_container[team_dict['TEAM']] = team_dict
    return standings


def get_conference_markdown(conference=None, playoff_standings=None, omit_eliminated=False):
    output = ''
    if not playoff_standings:
        playoff_standings = get_standings()
    for conf_name, conf_data in playoff_standings.items():
        output_array = []
        if conference and conf_name != conference:
            continue
        # Extract only wanted information
        conference_array = []
        for name, team in playoff_standings[conf_name].items():
            team_array = []
            for col in NFL.PLAYOFF_STANDINGS_COLUMNS:
                team_array.append(team[col].strip())
            conference_array.append(team_array)

        # Print the Markdown output
        # Only print the conference name if we are printing all conferences
        if not conference:
            output += '##{}\n'.format(conf_name)
        header_array = []
        for col in NFL.PLAYOFF_STANDINGS_COLUMNS:
            header_array.append(col)
        output_array.append(header_array)
        output_array.append([' ', '**Division Leaders**'])
        for team_array in conference_array[:4]:
            team_array[0] = MarkdownOutput.bold(team_array[0])
            team_array[1] = MarkdownOutput.bold(team_array[1])
            output_array.append(team_array)
        output_array.append([' ', '**Wild Cards**'])
        for team_array in conference_array[4:6]:
            team_array[0] = MarkdownOutput.bold_italicize(team_array[0])
            team_array[1] = MarkdownOutput.bold_italicize(team_array[1])
            output_array.append(team_array)
        output_array.append([' ', '**In the Hunt**'])
        for team_array in conference_array[6:]:
            if team_array[1] in NFL.PLAYOFF_ELIMINATED_TEAMS:
                if omit_eliminated:
                    continue
                team_array[0] = MarkdownOutput.strikethru(team_array[0])
                team_array[1] = MarkdownOutput.strikethru(team_array[1])
            output_array.append(team_array)
        output += MarkdownOutput.array2table(output_array, header_included=True, justification='centered')
        output += '\n\n'
    return output


def get_standings_markdown(conference=None, division=None, standings=None):
    output_array = []
    if not standings:
        standings = get_standings(playoffs=False)
    # Header
    header_array = []
    for col in NFL.STANDINGS_COLUMNS:
        header_array.append(col)
    for conf_name, divisions in standings.items():
        if not conference and not division:
            output_array.append('##' + conf_name)
        elif conf_name != conference and not division:
            continue
        for div_name, div_team_dict in divisions.items():
            if division and (div_name != division):
                continue
            # Only print the division name if we are printing all divisions
            if not division:
                output_array.append('###' + div_name)

            div_array = [header_array]
            for name, team in div_team_dict.items():
                # Extract only wanted information
                team_array = []
                for col in NFL.STANDINGS_COLUMNS:
                    team_array.append(team[col].strip())
                div_array.append(team_array)
            output_array.append(MarkdownOutput.array2table(div_array,
                                                           header_included=True,
                                                           justification='centered'))
            output_array.append("")
    return "\n".join(output_array)

if __name__ == '__main__':
    print(get_conference_markdown())
    print('\n' + '='*80 + '\n')
    print(get_standings_markdown())
    print('\n' + '='*100 + '\n')
    print('## 2014 NFC West Standings')
    print(get_standings_markdown(division='NFC WEST'))
    print('## 2014 NFC Playoff Picture')
    print(get_conference_markdown(NFL.CONFERENCE_NAMES['nfc']))
    print('\n' + '='*100 + '\n')