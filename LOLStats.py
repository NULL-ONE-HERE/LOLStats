import pandas as pd
from bs4 import BeautifulSoup as bs
import matplotlib.pyplot as plt
import requests

def start():
    userChoice = ""
    while userChoice != "exit":
        userChoice = input("What would you like to do? \n1. Get champion data\n2. Compare champions\n3. Get all champions\n4. Exit\n: ").lower()
        if userChoice == "1":
            role = input("Which role would you like to see? ").lower()
            for key, value in getChampData(role)[0].items():
                print(key + ": " + value)
        elif userChoice == "2":
            role = input("Which role would you like to see? ").lower()
            GetChampCompare(role)
        elif userChoice == "3":
            GetAllChampList()
        elif userChoice == "4":
            exit()
        else:
            print("Invalid choice")
        print("\n")

def getChampData(role):
    # Ask user for which champion they want to see and what role
    champ = input("Which champion would you like to see? ").lower()
    print("\n")

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

    return champStatsDict, champ

def GetAllChampList():
    print("\n")
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

    # Print the list of champions
    for i in range(len(champList)):
        print(champList[i])

def GetChampCompare(role):
    print("\n")
    try:
        champ1 = getChampData(role)
        champ2 = getChampData(role)

    except AttributeError:
        print("Seems to be no data")

    try:
        champStatsDict1 = {}
        dict1 = champ1[0]
        for key, value in dict1.items():
            champStatsDict1[key] = value

    except AttributeError:
        print("Seems to be no data for " + champ1[1] + " in " + role + " role.")

    try:
        champStatsDict2 = {}
        dict2 = champ2[0]
        for key, value in dict2.items():
            champStatsDict2[key] = value

    except AttributeError:
        print("Seems to be no data for " + champ2[1] + " in " + role + " role.")

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

    if statCompare == "matches played" or statCompare == "win rate" or statCompare == "pick rate" or statCompare == "ban rate" or statCompare == "matches played":
        # Get the max stat and round up
        if float(stat1) > float(stat2):
            maxStat = float(stat1)
        else:
            maxStat = float(stat2)

        maxStatAdd = 0

        print(maxStat)

        if maxStat < 10:
            maxStatAdd = 10
        elif maxStat > 10 and maxStat < 100:
            maxStatAdd = 100
        elif maxStat > 100 and maxStat < 1000:
            maxStatAdd = 1000
        elif maxStat > 1000 and maxStat < 10000:
            maxStatAdd = 10000
        elif maxStat > 10000 and maxStat < 100000:
            maxStatAdd = 100000
            
        print(maxStatAdd)

        maxStat = round(float(maxStat) + maxStatAdd)

        graphStatsCompare(stat1, stat2, champ1[1], champ2[1], statCompare, maxStat)

    else:
        print(champ1[1] + ": " + stat1)
        print(champ2[1] + ": " + stat2)

def graphStatsCompare(stat1, stat2, champ1, champ2, statCompare, maxStat):
    # Create a dataframe to store the data
    df = pd.DataFrame({'Champion': [champ1, champ2], 'Stat': [float(stat1), float(stat2)]})
    df.set_index('Champion', inplace=True)

    # Create a bar graph to display the data
    plt.bar(df.index, df['Stat'])
    plt.title(champ1 + " vs " + champ2)
    plt.xlabel("Champion")
    plt.ylabel(statCompare)
    plt.ylim(0, float(maxStat))
    plt.show()

start()
