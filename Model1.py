import requests

def result_based_on_table(home_team, away_team):
    data = requests.get('https://www.skysports.com/premier-league-table')
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
