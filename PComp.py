from bs4 import BeautifulSoup
import pandas as pd
import os

##Get the absolute paths to this and parent directory, and initialize list of teams & stats structures
print("Preparing to compile player attributes. Estimated Time To Completion: 120 seconds ") 
dir = os.path.dirname(os.path.abspath(__file__))
main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NHL = ["ANA", "BOS", "BUF", "CAR", "CBS", "CGY", "CHI", "COL", "DAL", "DET", "EDM", "FLA", "LA", "MIN", "MTL", "NAS", "NJ", "NYI", "NYR", "OTT", "PHI", "PIT", "SJ", "STL", "TB", "TOR", "VAN", "VGK", "WPG", "WSH"]
# NHL = ["SJ"]

Player = {
	'Team' : [],
	'CP' : [],
	'Name' : [],
	'Pos' : [],
	'Age' : [],
	'Salary' : [],
	'Years' : [],
	'FI' : [],
	'SH' : [],
	'PL' : [],
	'ST' : [],
	'CH' : [],
	'PO' : [],
	'HI' : [],
	'SK' : [],
	'EN' : [],
	'PE' : [],
	'FA' : [],
	'LE' : [],
	'SR' : [],
	'OFF' : [],
	'DEF' : [],
	'OVE' : [],
}
PlayerStats = {
	'Rookie' : [],
	'Pos' : [],
	'Name' : [],
	'Team' : [],
	'GP' : [],
	'G' : [],
	'A' : [],
	'Pts' : [],
	'+/-' : [],
	'PIM' : [],
	'PPG' : [],
	'SHG' : [],
	'Shots' : [],
	'SH%' : [],
}
GoalieStats = {
	'Rookie' : [],
	'Pos' : [],
	'Name' : [],
	'Team' : [],
	'GP' : [],
	'G' : [],
	'A' : [],
	'Pts' : [],
	'W' : [],
	'L' : [],
	'OTL' : [],
	'L2' : [],
	'Pct' : [],
	'SO' : [],
	'GAA' : [],
}

print("Searching for attribute files in directory:")
print(main_dir)
print("Searching for stat files in directory:")
print(os.path.join(main_dir, 'html\\'))

#Iterates through each team stat file, and then iterates through the stats table and puts the stats in a table. 
for team in NHL:
	print("Analyzing team: " + team + ".")
	AttFile = os.path.join(main_dir, team + ".html")
	StatFile = os.path.join(main_dir, 'html\\', team + ".html")
	AttPage = open(AttFile).read()
	StatPage = open(StatFile).read()

	AttSoup = BeautifulSoup(AttPage, "html5lib")
	StatSoup = BeautifulSoup(StatPage, "html5lib")

	NHLTable = AttSoup.find_all('table')[0] #The first table is just a table with the title of the page
	NHLRows = NHLTable.find_all('tr')[1:]
	AHLTable = AttSoup.find_all('table')[1]
	AHLRows = AHLTable.find_all('tr')[1:]
	ProspectTable = AttSoup.find_all('table')[2]
	ProspectRows = ProspectTable.find_all('tr')[1:]
	
	pTable = StatSoup.find_all('table')[1] #The first table is just a table with the title of the page
	pRows = pTable.find_all('tr')[1:]
	gTable = StatSoup.find_all('table')[2]
	gRows = gTable.find_all('tr')[1:]
	

	for row in NHLRows:
		cols = row.find_all('td')
		if cols[1].get_text() != "": #There are some empty rows in the tables, this ignores them
			Player['Team'].append(team)
			Player['CP'].append('NHL')
			Player['Name'].append(cols[0].get_text()) #Some weird names out there which need to be encoded. Encoding page destroys the structure and you can't find the tables easily.
			Player['Pos'].append(cols[1].get_text())
			
			col_index = 2
			for key in ['Age', 'Salary', 'Years', 'FI', 'SH', 'PL', 'ST', 'CH', 'PO', 'HI', 'SK', 'EN', 'PE', 'FA', 'LE', 'SR', 'OFF', 'DEF', 'OVE']:
				Player[key].append(int(cols[col_index].get_text()))		
				col_index += 1

	for row in AHLRows:
		cols = row.find_all('td')
		if cols[1].get_text() != "": #There are some empty rows in the tables, this ignores them
			Player['Team'].append(team)
			Player['CP'].append('AHL')
			Player['Name'].append(cols[0].get_text()) #Some weird names out there which need to be encoded. Encoding page destroys the structure and you can't find the tables easily.
			Player['Pos'].append(cols[1].get_text())
			
			col_index = 2
			for key in ['Age', 'Salary', 'Years', 'FI', 'SH', 'PL', 'ST', 'CH', 'PO', 'HI', 'SK', 'EN', 'PE', 'FA', 'LE', 'SR', 'OFF', 'DEF', 'OVE']:
				Player[key].append(int(cols[col_index].get_text()))		
				col_index += 1

	for row in ProspectRows:
		cols = row.find_all('td')
		if cols[1].get_text() != "": #There are some empty rows in the tables, this ignores them
			Player['Team'].append(team)
			Player['CP'].append('Minors')
			Player['Name'].append(cols[0].get_text()) #Some weird names out there which need to be encoded. Encoding page destroys the structure and you can't find the tables easily.
			Player['Pos'].append(cols[1].get_text())

			
			col_index = 2
			for key in ['Age', 'Salary', 'Years', 'FI', 'SH', 'PL', 'ST', 'CH', 'PO', 'HI', 'SK', 'EN', 'PE', 'FA', 'LE', 'SR', 'OFF', 'DEF', 'OVE']:
				Player[key].append(int(cols[col_index].get_text()))
				col_index += 1


	for row in pRows:
		cols = row.find_all('td')
		if cols[1].get_text() != "": #There are some empty rows in the tables, this ignores them
			PlayerStats['Pos'].append(cols[0].get_text())
			if "*" in cols[1].get_text():
				PlayerStats['Rookie'].append(True)
				PlayerStats['Name'].append(cols[1].get_text()[1:]) #Names with * are rookies, ex: *Jon Omeara
			else:
				PlayerStats['Name'].append(cols[1].get_text())
				PlayerStats['Rookie'].append(False)
			PlayerStats['Team'].append(cols[2].get_text())
			PlayerStats['GP'].append(int(cols[3].get_text()))
			PlayerStats['G'].append(int(cols[4].get_text()))
			PlayerStats['A'].append(int(cols[5].get_text()))
			PlayerStats['Pts'].append(int(cols[6].get_text()))
			PlayerStats['+/-'].append(int(cols[7].get_text()))
			PlayerStats['PIM'].append(int(cols[8].get_text()))
			PlayerStats['PPG'].append(int(cols[9].get_text()))
			PlayerStats['SHG'].append(int(cols[10].get_text()))
			PlayerStats['Shots'].append(int(cols[11].get_text()))
			PlayerStats['SH%'].append(round(float(cols[12].get_text()),2))

	for row in gRows:
		cols = row.find_all('td')
		if (cols[1].get_text() != "") and (cols[13].get_text() != "N/A"):
			GoalieStats['Pos'].append(cols[0].get_text())
			if "*" in cols[1].get_text():
				GoalieStats['Rookie'].append(True)
				GoalieStats['Name'].append(cols[1].get_text()[1:]) #Some weird names out there which need to be encoded. Encoding page destroys the structure and you can't find the tables easily.
			else:
				GoalieStats['Name'].append(cols[1].get_text()) #Some weird names out there which need to be encoded. Encoding page destroys the structure and you can't find the tables easily.
				GoalieStats['Rookie'].append(False)
			GoalieStats['Team'].append(cols[2].get_text())
			GoalieStats['GP'].append(int(cols[3].get_text()))
			GoalieStats['G'].append(int(cols[4].get_text()))
			GoalieStats['A'].append(int(cols[5].get_text()))
			GoalieStats['Pts'].append(int(cols[6].get_text()))
			GoalieStats['W'].append(int(cols[7].get_text()))
			GoalieStats['L'].append(int(cols[8].get_text()))
			GoalieStats['OTL'].append(int(cols[9].get_text()))
			GoalieStats['L2'].append(int(cols[10].get_text()))
			GoalieStats['Pct'].append(round(float(cols[11].get_text()),3))
			GoalieStats['SO'].append(int(cols[12].get_text()))
			GoalieStats['GAA'].append(round(float(cols[13].get_text()),2))
			
print("Committing data to tables.")
AllPlayersTable = pd.DataFrame(Player) ##Attributes
AllPlayersTable = AllPlayersTable.sort_values(by=['Team','CP','Name'], ascending = True)


PlayerTable = pd.DataFrame(PlayerStats) ##Stats
GoalieTable = pd.DataFrame(GoalieStats)
PlayerTable = PlayerTable.sort_values(by=['Pts'], ascending = False)
GoalieTable = GoalieTable.sort_values(by=['Pct'], ascending = False)



print("Exporting data to .html file")
reports_dir = os.path.join(main_dir,'Reports')
if not os.path.exists(reports_dir):
    os.makedirs(reports_dir)

#Exporting Attributes without a bloody header for easy copy & pastage.
AllPlayersTable.to_html(os.path.join(reports_dir,'Players.html'),index = False, columns = ['Team', 'CP', 'Name', 'Pos', 'Age', 'Salary', 'Years', 'FI', 'SH', 'PL', 'ST', 'CH', 'PO', 'HI', 'SK', 'EN', 'PE', 'FA', 'LE', 'SR', 'OFF', 'DEF', 'OVE'])
# RookieStatus = (PlayerTable[['Name', 'Team', 'Rookie']].copy()).append(GoalieTable[['Name', 'Team', 'Rookie']].copy())
# FinalPlayersTable = pd.merge(AllPlayersTable, RookieStatus, on=['Name', 'Team'], how='inner')

PlayerTable.to_html(os.path.join(reports_dir,'PlayerStats.html'),index = False, columns = ['Pos', 'Rookie', 'Name', 'Team', 'GP', 'G', 'A', 'Pts', '+/-', 'PIM', 'PPG', 'SHG', 'Shots', 'SH%'])
GoalieTable.to_html(os.path.join(reports_dir,'GoalieStats.html'),index = False, columns = ['Pos', 'Rookie', 'Name', 'Team', 'GP', 'G', 'A', 'Pts', 'W', 'L', 'OTL', 'L2', 'Pct', 'SO', 'GAA'])


# # THE GLORIOUS! Combines NHL Goalie & Player attributes and stats into 1 table.

del PlayerTable['Pos']# these are dropped as its easier than converting all "L" --> LW & "R"-->"RW"
del GoalieTable['Pos']

NHLGoalies = pd.merge(AllPlayersTable, GoalieTable, on=['Name', 'Team'], how='inner')
NHLPlayers = pd.merge(AllPlayersTable, PlayerTable, on=['Name', 'Team'], how='inner')

NHLGoalies.to_html(os.path.join(reports_dir,'NHLGoalies.html'),index = False, columns = ['Team', 'CP', 'Rookie', 'Name', 'Pos', 'Age', 'Salary', 'Years', 'FI', 'SH', 'PL', 'ST', 'CH', 'PO', 'HI', 'SK', 'EN', 'PE', 'FA', 'LE', 'SR', 'OFF', 'DEF', 'OVE', 'GP', 'G', 'A', 'Pts', 'W', 'L', 'OTL', 'L2', 'Pct', 'SO', 'GAA'])
NHLPlayers.to_html(os.path.join(reports_dir,'NHLPlayers.html'),index = False, columns = ['Team', 'CP', 'Rookie', 'Name', 'Pos', 'Age', 'Salary', 'Years', 'FI', 'SH', 'PL', 'ST', 'CH', 'PO', 'HI', 'SK', 'EN', 'PE', 'FA', 'LE', 'SR', 'OFF', 'DEF', 'OVE', 'GP', 'G', 'A', 'Pts', '+/-', 'PIM', 'PPG', 'SHG', 'Shots', 'SH%'])



print("Stats compilation complete")