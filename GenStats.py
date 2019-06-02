from bs4 import BeautifulSoup
import pandas as pd
import os

##Get the absolute paths to this and parent directory, and initialize list of teams & stats structures
print("Preparing to compile league stats. Estimated Time To Completion: 60 seconds ") 
dir = os.path.dirname(os.path.abspath(__file__))
main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NHL = ["ANA", "BOS", "BUF", "CAR", "CBS", "CGY", "CHI", "COL", "DAL", "DET", "EDM", "FLA", "LA", "MIN", "MTL", "NAS", "NJ", "NYI", "NYR", "OTT", "PHI", "PIT", "SJ", "STL", "TB", "TOR", "VAN", "VGK", "WIN", "WSH"]

PlayerStats = {
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
print("Searching for stat files in directory:")
print(os.path.join(main_dir, 'html\\'))


#Iterates through each team stat file, and then iterates through the stats table and puts the stats in a table. 
for team in NHL:
	print("Analyzing team: " + team + ".")
	file = os.path.join(main_dir, 'html\\', team + ".html")
	localPage = open(file).read()
	soup = BeautifulSoup(localPage, "html5lib")
	
	pTable = soup.find_all('table')[1] #The first table is just a table with the title of the page
	pRows = pTable.find_all('tr')[1:]
	gTable = soup.find_all('table')[2]
	gRows = gTable.find_all('tr')[1:]

	for row in pRows:
		cols = row.find_all('td')
		if cols[1].get_text() != "": #There are some empty rows in the tables, this ignores them
			PlayerStats['Pos'].append(cols[0].get_text())
			PlayerStats['Name'].append(cols[1].get_text().encode('ascii','ignore')) #Some weird names out there which need to be encoded. Encoding page destroys the structure and you can't find the tables easily.
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
			GoalieStats['Name'].append(cols[1].get_text().encode('ascii','ignore'))
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
PlayerTable = pd.DataFrame(PlayerStats)
PlayerTable = PlayerTable.sort_values(by=['Pts'], ascending = False)
GoalieTable = pd.DataFrame(GoalieStats)
GoalieTable = GoalieTable.sort_values(by=['Pct'], ascending = False)

print("Exporting data to .html file")
reports_dir = os.path.join(main_dir,'Reports')
if not os.path.exists(reports_dir):
    os.makedirs(reports_dir)
PlayerTable.to_html(os.path.join(reports_dir,'PlayerStats.html'),index = False, columns = ['Pos', 'Name', 'Team', 'GP', 'G', 'A', 'Pts', '+/-', 'PIM', 'PPG', 'SHG', 'Shots', 'SH%'])
GoalieTable.to_html(os.path.join(reports_dir,'GoalieStats.html'),index = False, columns = ['Pos', 'Name', 'Team', 'GP', 'G', 'A', 'Pts', 'W', 'L', 'OTL', 'L2', 'Pct', 'SO', 'GAA'])

# Adds a title to the two reports, and centers it so it matches the other reports
	# The code has been grouped together rather than done one after the other for easy reading and modification
print("Formating Reports")
file1 = os.path.join(reports_dir,'PlayerStats.html')
file2 = os.path.join(reports_dir,'Goaliestats.html')
f1 = open(file1)
f2 = open(file2)
soup1 = str(BeautifulSoup(f1, "html5lib"))
soup2 = str(BeautifulSoup(f2, "html5lib"))

# This is the added headers and footers for the page.
player_header = """ <HTML><HEAD><TITLE>NHL Player Statistics</TITLE></HEAD>
<CENTER><FONT SIZE=16>NHL Player Statistics</FONT><P><P><P>"""
player_footer = """</CENTER></HTML>"""
goalie_header = """ <HTML><HEAD><TITLE>NHL Goalie Statistics</TITLE></HEAD>
<CENTER><FONT SIZE=16>NHL Goalie Statistics</FONT><P><P><P>"""
goalie_footer = """</CENTER></HTML>"""

player_report_html = player_header + soup1 + player_footer
goalie_report_html = goalie_header + soup2 + goalie_footer

f1.close
f1 = open(file1,'w')
f1.write(player_report_html)

f2.close
f2 = open(file2,'w')
f2.write(goalie_report_html)


print("Stats compilation complete")