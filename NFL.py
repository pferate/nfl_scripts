from collections import OrderedDict

CONFERENCE_NAMES = {'nfc': 'National Football Conference',
                    'afc': 'American Football Conference'
                    }

PLAYOFF_STANDINGS_COLUMNS_MAPPING = OrderedDict([
    ('CONF RK', ' #'),
    ('NFC', 'TEAM'),
    ('AFC', 'TEAM'),
])
PLAYOFF_STANDINGS_COLUMNS = [' #', 'TEAM', 'W', 'L', 'T', 'PCT', 'DIV', 'CONF']

STANDINGS_COLUMNS_MAPPING = OrderedDict([
    ('NFC EAST', 'TEAM'),
    ('NFC NORTH', 'TEAM'),
    ('NFC SOUTH', 'TEAM'),
    ('NFC WEST', 'TEAM'),
    ('AFC EAST', 'TEAM'),
    ('AFC NORTH', 'TEAM'),
    ('AFC SOUTH', 'TEAM'),
    ('AFC WEST', 'TEAM'),
])
STANDINGS_COLUMNS = ['TEAM', 'W', 'L', 'T', 'PCT', 'DIV', 'PF', 'PA', 'STRK']

TEAM_SUBREDDIT_MAP = {
    # NFC East
    'Dallas': '[Cowboys](/r/cowboys)',
    'NY Giants': '[Giants](/r/nygiants)',
    'Philadelphia': '[Eagles](/r/eagles)',
    'Washington': '[Redskins](/r/redskins)',
    # NFC North
    'Chicago': '[Chicago](/r/chibears)',
    'Detroit': '[Lions](/r/detroitlions)',
    'Green Bay': '[Packers](/r/greenbaypackers)',
    'Minnesota': '[Vikings](/r/minnesotavikings)',
    # NFC South
    'Atlanta': '[Falcons](/r/falcons)',
    'Carolina': '[Panthers](/r/panthers)',
    'New Orleans': '[Saints](/r/saints)',
    'Tampa Bay': '[Buccaneers](/r/buccaneers)',
    # NFC West
    'Arizona': '[Cardinals](/r/azcardinals)',
    'San Francisco': '[49ers](/r/49ers)',
    'Seattle': '[Seahawks](/r/seahawks)',
    'St. Louis': '[Rams](/r/stlouisrams)',
    # AFC East
    'Buffalo': '[Bills](/r/nfl)',
    'Miami': '[Dolphins](/r/nfl)',
    'New England': '[Patriots](/r/nfl)',
    'NY Jets': '[Jets](/r/nfl)',
    # AFC North
    'Baltimore': '[Ravens](/r/nfl)',
    'Cincinnati': '[Bangals](/r/nfl)',
    'Cleveland': '[Browns](/r/nfl)',
    'Pittsburgh': '[Steelers](/r/nfl)',
    # AFC South
    'Houston': '[Texans](/r/nfl)',
    'Indianapolis': '[Colts](/r/nfl)',
    'Jacksonville': '[Jaguars](/r/nfl)',
    'Tennessee': '[Titans](/r/nfl)',
    # AFC West
    'Denver': '[Broncos](/r/nfl)',
    'Kansas City': '[Chiefs](/r/nfl)',
    'Oakland': '[Raiders](/r/nfl)',
    'San Diego': '[Chargers](/r/nfl)',
}

# Using the map here because when we check it later on,
# the cities will already translated to the subreddit link
PLAYOFF_ELIMINATED_TEAMS = [
    # NFC
    TEAM_SUBREDDIT_MAP['Chicago'],
    TEAM_SUBREDDIT_MAP['Minnesota'],
    TEAM_SUBREDDIT_MAP['New Orleans'],
    TEAM_SUBREDDIT_MAP['NY Giants'],
    TEAM_SUBREDDIT_MAP['Philadelphia'],
    TEAM_SUBREDDIT_MAP['San Francisco'],
    TEAM_SUBREDDIT_MAP['St. Louis'],
    TEAM_SUBREDDIT_MAP['Tampa Bay'],
    TEAM_SUBREDDIT_MAP['Washington'],
    # AFC
    TEAM_SUBREDDIT_MAP['Buffalo'],
    TEAM_SUBREDDIT_MAP['Cleveland'],
    TEAM_SUBREDDIT_MAP['Miami'],
    TEAM_SUBREDDIT_MAP['NY Jets'],
    TEAM_SUBREDDIT_MAP['Tennessee'],
    TEAM_SUBREDDIT_MAP['Jacksonville'],
    TEAM_SUBREDDIT_MAP['Oakland'],
]