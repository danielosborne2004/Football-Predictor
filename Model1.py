import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO

def result_based_on_table(home_team, away_team):
    data = requests.get('https://www.bbc.com/sport/football/premier-league/table')
    if data.status_code != 200:
        print("Failed to fetch league table")
        return

    #Iterates through all lines in file
    for line in data:
        #Manipulates file into a readable format and strips leading or trailing white space
        line = line.decode('utf-8').strip()

        #Allots home team as winner and breaks out of loop if name detected first
        if home_team.lower() in line.lower():
            print(f"It is likelier that {home_team} will win")
            return

            #Allots away team as winner and breaks out of loop if name detected first
        elif away_team.lower() in line.lower():
            print(f"It is likelier that {away_team} will win")
            return

    #Tells user if neither team was found in table and returns
    print("Neither team was found in table")
    return


def result_based_on_table_version_2(home_team, away_team):
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
        win_odds = round(1 / (win_percentage / 100), 3)
        print(
            f"{away_team} is likelier to win with a win percentage of {win_percentage}% and betting odds of {win_odds}")
        return win_odds
    else:
        win_percentage = 2 * (away_count - home_count) + 35
        win_odds = round(1 / (win_percentage / 100), 3)
        print(
            f"{home_team} is likelier to win with a win percentage of {win_percentage}% and betting odds of {win_odds}")
        return win_odds

# def result_based_on_table_version_2(home_team, away_team):
#     data = requests.get('https://www.bbc.com/sport/football/premier-league/table')
#     if data.status_code != 200:
#         print("Failed to fetch league table")
#         return
#
#     count = 0
#
#     # Iterates through all lines in file
#     for line in data:
#         # Manipulates file into a readable format and strips leading or trailing white space
#         line = line.decode('utf-8').strip()
#
#         # Allots home team as winner
#         if home_team.lower() in line.lower():
#             home_count = count
#
#
#             # Allots away team as winner and breaks out of loop if name detected first
#         elif away_team.lower() in line.lower():
#             away_count = count
#
#         count += 1
#
#     if home_team > away_team:
#         win_percentage = 2*(home_count - away_count) + 35
#         win_odds = round(1/(win_percentage / 100), 2)
#         print(f"{home_team} is likelier to win with a win percentage of {win_percentage} and betting odds of {win_odds}")
#         return win_odds
#
#     else:
#         win_percentage = 2 * (away_count - home_count) + 35
#         win_odds = round(1/(win_percentage / 100), 2)
#         print(f"{away_team} is likelier to win with a win percentage of {win_percentage}% and betting odds of {win_odds}")
#         return win_odds



# def result_considering_home_team(home_team, away_team):
#