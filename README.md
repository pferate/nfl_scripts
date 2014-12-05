NFL Scripts
===========

Python scripts for generating Markdown text for NFL Subreddits.  It is currently implemented in Python 3 (3.4).

This was originally a way to generate the 2014 NFC playoff picture for the [/r/seahawks](http://reddit.com/r/seahawks) subreddit, but it will probably grow to handle more things eventually.
 
I've expanded it to work with the Playoff picture of both conferences as well as the Divisional standings.

Right now, I am getting the data from ESPN's [NFL Standings](http://espn.go.com/nfl/standings) page.  If there are any major changes there, it could potentially break this library.
l
Currently, the majority of the logic is in Standings.py.
 
NFL.py contains various definitions used throughout the code.

 *   Column mappings between the column names on ESPN page and how to display them here
 *   The list and order of columns to display here
 *   A mapping of team city names to subreddit pages
 *   A list of teams that have been elimiated from Playoff Contention
 
I couldn't find any useful Markdown generation libraries, so I started one (MardownOutput.py).  I did happen to come across a lot of libraries for parsing Markdown, but not the other way around.

Sample Usage
============

Right now, you can either import the functions from the Standings module or put the following code snippets at the end of Standings.py and run it.

    from Standings import get_conference_markdown, get_standings_markdown
    
Printing the NFC West Standings

    print('## 2014 NFC West Standings')
    print(get_standings_markdown(division='NFC WEST'))

Printing the NFC Playoff Picture

    print('## 2014 NFC Playoff Picture')
    print(get_conference_markdown(NFL.CONFERENCE_NAMES['nfc']))

Printing the NFL Divisional Standings

    print(get_standings_markdown())
    
Printing the NFL Playoff Picture

    print('## 2014 NFL Playoff Picture')
    print(get_conference_markdown())
