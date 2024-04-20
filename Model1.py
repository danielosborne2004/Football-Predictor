import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO


def result_based_on_table_version_1(home_team, away_team):
    '''
    Function just takes into account which team is higher on the table and returns that team as being more likely to
    win.

    First ever model
    Very happy with being able to get data straight off internet
    Data format very inconvenient - maybe can use pandas in the future ;)
    '''

    data = requests.get('https://www.bbc.com/sport/football/premier-league/table')
    if data.status_code != 200:
        print("Failed to fetch league table")
        return

    # Iterates through all lines in file
    for line in data:
        # Manipulates file into a readable format and strips leading or trailing white space
        line = line.decode('utf-8').strip()

        # Allots home team as winner and breaks out of loop if name detected first
        if home_team.lower() in line.lower():
            print(f"It is likelier that {home_team} will win")
            return

            # Allots away team as winner and breaks out of loop if name detected first
        elif away_team.lower() in line.lower():
            print(f"It is likelier that {away_team} will win")
            return

    # Tells user if neither team was found in table and returns
    print("Neither team was found in table")
    return


def result_based_on_table_version_2(home_team, away_team):
    '''
    Function takes into account only the preimier league table but looks at the distance apart from the home team and
    away team and bases the likelihood of a team winning on how far apart they are on this table. This formula of
    2 x spot dif + 35 is assuming equal teams have a 35% chance of winning and 30% chance of draw, along with the
    gradient value of 2 being based of an average from gathered data comparing % win given by betting odds with
    the gap between teams on the table.

    First implementation of pandas (SO OVERPOWERED!!)
    First model with odds added (Can start testing them more accurately)
    Model has limitation where it assumes the gap between teams on the table linearly predicts the winning percentage
    of that team - it also assumes that all teams have the same inital draw % of 35% but in reality this varies from
    team to team
    '''
    # Fetch HTML content from the URL
    url = 'https://www.bbc.com/sport/football/premier-league/table'
    response = requests.get(url)

    if response.status_code != 200:
        print("Failed to fetch league table")
        return

    # Parse HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table containing the league standings
    table = soup.find('table')

    if not table:
        print("Failed to find league table")
        return

    # Read the table into a DataFrame
    html_str = str(table)
    df = pd.read_html(StringIO(html_str))[0]

    home_count = None
    away_count = None

    # Iterate through the rows of the DataFrame to find the positions of the specified teams
    for index, row in df.iterrows():
        # Check if the home team is found
        if home_team.lower() in row['Team'].lower():
            home_count = index
        # Check if the away team is found
        elif away_team.lower() in row['Team'].lower():
            away_count = index
        if home_count is not None and away_count is not None:
            break

    if home_count is None or away_count is None:
        print("Failed to find both teams in the league table")
        return

    # Calculate win percentage and odds based on the team positions
    if home_count > away_count:
        win_percentage = 2 * (home_count - away_count) + 35
        win_odds = round(1 / (win_percentage / 100), 2)
        print(
            f"{away_team} is likelier to win with a win percentage of {win_percentage}% and betting odds of {win_odds}")
        return win_odds
    else:
        win_percentage = 2 * (away_count - home_count) + 35
        win_odds = round(1 / (win_percentage / 100), 2)
        print(
            f"{home_team} is likelier to win with a win percentage of {win_percentage}% and betting odds of {win_odds}")
        return win_odds


def result_based_on_table_version_3(home_team, away_team):
    '''
    doc string
    '''

    # Fetch HTML content from the URL
    url = 'https://www.bbc.com/sport/football/premier-league/table'
    response = requests.get(url)

    if response.status_code != 200:
        print("Failed to fetch league table")
        return

    # Parse HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table containing the league standings
    table = soup.find('table')

    if not table:
        print("Failed to find league table")
        return

    # Read the table into a DataFrame
    html_str = str(table)
    df = pd.read_html(StringIO(html_str))[0]

    home_count = None
    away_count = None
    draw_total = 0

    # Iterate through the rows of the DataFrame to find the positions of the specified teams
    for index, row in df.iterrows():
        # Check if the home team is found
        if home_team.lower() in row['Team'].lower():
            home_points = row['Points']
            home_gd = row['Goal Difference']
            home_draws = row['Drawn']
        # Check if the away team is found
        elif away_team.lower() in row['Team'].lower():
            away_points = row['Points']
            away_gd = row['Goal Difference']
            away_draws = row['Drawn']
        draw_total += row['Drawn']

    #From using stat that 1 in 4.2 (0.2381) prem games end in draw and factoring it based on teams frequency
    draw_avg = draw_total / 20
    draw_freq = ((home_draws + away_draws)/2) / draw_avg
    draw_percentage = draw_freq * 23.81

    print(draw_percentage)

def panda_table_test():
    #url = 'https://www.bbc.com/sport/football/premier-league/table'
    url = 'https://www.twtd.co.uk/league-tables/competition:premier-league/daterange/fromdate:2023-Jul-01/todate:2024-Jan-01/type:home-and-away/'
    response = requests.get(url)

    if response.status_code != 200:
        print("Failed to fetch league table")
        return

    # Parse HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table containing the league standings
    table = soup.find('table')

    if not table:
        print("Failed to find league table")
        return

    # Read the table into a DataFrame
    html_str = str(table)
    df = pd.read_html(StringIO(html_str))[0]

    for index, row in df.iterrows():
        print(f"{row['Team']}: {row['Pts']}")
