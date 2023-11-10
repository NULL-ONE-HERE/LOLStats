import pandas as pd
from bs4 import BeautifulSoup as bs
import matplotlib.pyplot as plt
import requests
import pandas as pd

def getChampData():
    # Ask user for which champion they want to see and what role
    champ = input("Which champion would you like to see? ").lower()
    role = input("Which role would you like to see? ").lower()

    # Get the data from the website
    url = 'https://u.gg/lol/champions/{champ}/build/{role}'.format(champ=champ, role=role)
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = bs(response.text, 'html.parser')

    # Get the champions stats
    champStats = soup.find('div', class_='champion-ranking-stats-normal')

    # Get all the stats labels and values
    champStatsLabels = champStats.find_all('div', class_='label')
    champStatsValues = champStats.find_all('div', class_='value')

    # Create a dictionary to store the stats
    champStatsDict = {}

    # Loop through the labels and values and add them to the dictionary
    for i in range(len(champStatsLabels)):
        champStatsDict[champStatsLabels[i].text] = champStatsValues[i].text

    # Display the stats and their labels
    for key, value in champStatsDict.items():
        print(key, value)

def GetAllChampList():
    # Get the data from the website
    url = 'https://u.gg/lol/champions'
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = bs(response.text, 'html.parser')

    # Get the champions table
    champTableRaw = soup.find('div', class_='champions-container')

    # Create a list to store the champions
    champList = []

    # Loop through the champions and add them to the list
    for champs in champTableRaw.find_all('div', class_='champion-name'):
        champList.append(champs.text)

    # Return the list of champions
    return champList

def GetChampCompare():
    # Ask user for which champions they want to compare and what role
    champ1 = input("Which champion would you like to compare? ").lower()
    champ2 = input("Which champion would you like to compare? ").lower()
    role = input("Which role would you like to compare? ").lower()

    try:
        # Get the data from the website
        url1 = 'https://u.gg/lol/champions/{champ1}/build/{role}'.format(champ1=champ1, role=role)
        response = requests.get(url1, headers={'User-Agent': 'Mozilla/5.0'})
        soup = bs(response.text, 'html.parser')

        # Store the champions stats
        champStats1 = soup.find('div', class_='champion-ranking-stats-normal')

        # Get all the stats labels and values
        champStatsLabels1 = champStats1.find_all('div', class_='label')
        champStatsValues1 = champStats1.find_all('div', class_='value')

        # Create a dictionary to store the stats
        champStatsDict1 = {}

        # Loop through the labels and values and add them to the dictionary
        for i in range(len(champStatsLabels1)):
            champStatsDict1[champStatsLabels1[i].text] = champStatsValues1[i].text

    except AttributeError:
        print("Seems to be no data for " + champ1 + " in " + role + " role.")

    try:
        # Get the data from the website
        url2 = 'https://u.gg/lol/champions/{champ2}/build/{role}'.format(champ2=champ2, role=role)
        response = requests.get(url2, headers={'User-Agent': 'Mozilla/5.0'})
        soup = bs(response.text, 'html.parser')

        # Store the champions stats
        champStats2 = soup.find('div', class_='champion-ranking-stats-normal')

        # Get all the stats labels and values
        champStatsLabels2 = champStats2.find_all('div', class_='label')
        champStatsValues2 = champStats2.find_all('div', class_='value')

        # Create a dictionary to store the stats
        champStatsDict2 = {}

        # Loop through the labels and values and add them to the dictionary
        for i in range(len(champStatsLabels2)):
            champStatsDict2[champStatsLabels2[i].text] = champStatsValues2[i].text

    except AttributeError:
        print("Seems to be no data for " + champ2 + " in " + role + " role.")

    # Ask user which stat they want to compare
    statCompare = input("Which stat would you like to compare? \nTier\nWin Rate\nRank\nPick Rate\nBan Rate\nMatches Played\n: ").lower()
    
    # Get the stats to compare and add to dictionary
    if statCompare == "tier":
        stat1 = champStatsDict1['Tier']
        stat2 = champStatsDict2['Tier']
    elif statCompare == "win rate":
        stat1 = champStatsDict1['Win Rate']
        stat2 = champStatsDict2['Win Rate']
    elif statCompare == "rank":
        stat1 = champStatsDict1['Rank']
        stat2 = champStatsDict2['Rank']
    elif statCompare == "pick rate":
        stat1 = champStatsDict1['Pick Rate']
        stat2 = champStatsDict2['Pick Rate']
    elif statCompare == "ban rate":
        stat1 = champStatsDict1['Ban Rate']
        stat2 = champStatsDict2['Ban Rate']
    elif statCompare == "matches played":
        stat1 = champStatsDict1['Matches']
        stat2 = champStatsDict2['Matches']
    else:
        print("Invalid stat")
        exit()

    # Strip the % and , from the stats if they are there
    stat1 = stat1.replace("%", "")
    stat1 = stat1.replace(",", "")
    stat2 = stat2.replace("%", "")
    stat2 = stat2.replace(",", "")

    print(stat1, stat2)

    if statCompare == "matches played" or statCompare == "win rate" or statCompare == "pick rate" or statCompare == "ban rate" or statCompare == "matches played":
        # Get the max stat and round up
        if float(stat1) > float(stat2):
            maxStat = float(stat1)
        else:
            maxStat = float(stat2)

        maxStat = round(float(maxStat) + 10)

        graphStatsCompare(stat1, stat2, champ1, champ2, statCompare, maxStat)

    else:
        print(champ1 + ": " + stat1)
        print(champ2 + ": " + stat2)

def graphStatsCompare(stat1, stat2, champ1, champ2, statCompare, maxStat):
    # Create a dataframe to store the data
    df = pd.DataFrame({'Champion': [champ1, champ2], 'Stat': [float(stat1), float(stat2)]})
    df.set_index('Champion', inplace=True)

    # Display the dataframe
    print(df)

    # Create a bar graph to display the data
    plt.bar(df.index, df['Stat'])
    plt.title(champ1 + " vs " + champ2)
    plt.xlabel("Champion")
    plt.ylabel(statCompare)
    plt.ylim(0, float(maxStat))
    plt.show()

'''getChampData()'''
GetChampCompare()