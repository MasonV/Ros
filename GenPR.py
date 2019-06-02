from bs4 import BeautifulSoup
import pandas as pd
import os

##Get the absolute paths to this and parent directory, and initialize list of teams & stats structures
print("Preparing to compile player attributes. Estimated Time To Completion: 120 seconds ") 
dir = os.path.dirname(os.path.abspath(__file__))
main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NHL = ["ANA", "BOS", "BUF", "CAR", "CBS", "CGY", "CHI", "COL", "DAL", "DET", "EDM", "FLA", "LA", "MIN", "MTL", "NAS", "NJ", "NYI", "NYR", "OTT", "PHI", "PIT", "SJ", "STL", "TB", "TOR", "VAN", "PHO", "ATL", "WSH", "UFAs"]
# NHL = ["ANA", "BOS", "BUF", "CAR", "CBS", "CGY", "CHI", "COL", "DAL", "DET", "EDM", "FLA", "LA", "MIN", "MTL", "NAS", "NJ", "NYI", "NYR", "OTT", "PHI", "PIT", "SJ", "STL", "TB", "TOR", "VAN", "VGK", "WIN", "WSH"]
# NHL = ["ANA", "BOS", "BUF", "CAR", "CBS", "CGY", "CHI", "COL", "DAL", "DET", "EDM", "FLA", "LA", "MIN", "MTL", "NAS", "NJ", "NYI", "NYR", "OTT", "PHI", "PIT", "SJ", "STL", "TB", "TOR", "VAN", "VGK", "WIN", "WSH", "UFAs"]
# NHL = ["UFAs"]

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

print("Searching for attribute files in directory:")
print(os.path.join(main_dir, 'html\\'))


#Iterates through each team stat file, and then iterates through the stats table and puts the stats in a table. 
for team in NHL:
	print("Analyzing team: " + team + ".")
	file = os.path.join(main_dir, team + ".html")
	localPage = open(file).read()
	soup = BeautifulSoup(localPage, "html5lib")
	
	NHLTable = soup.find_all('table')[0] #The first table is just a table with the title of the page
	NHLRows = NHLTable.find_all('tr')[1:]
	try:
		AHLTable = soup.find_all('table')[1]
		AHLRows = AHLTable.find_all('tr')[1:]
		ProspectTable = soup.find_all('table')[2]
		ProspectRows = ProspectTable.find_all('tr')[1:]
	except:
		print("No AHLers to analyze, likely UFA list")
	
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

	try:
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
	except:
		print("No AHLers to analyze, likely UFA list")


	try:
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
	except:
		print("No AHLers to analyze, likely UFA list")
			
print("Committing data to tables.")
NHLTable = pd.DataFrame(Player)
AHLTable = pd.DataFrame(Player)
ProspectTable = pd.DataFrame(Player)
AllPlayers = [NHLTable, AHLTable, ProspectTable]
PlayersTable = pd.concat(AllPlayers)

NHLTable = NHLTable.sort_values(by=['Team','CP','Name'], ascending = True)
ProspectTable = ProspectTable.sort_values(by=['Team','CP','Name'], ascending = True)


print("Exporting data to .html file")
reports_dir = os.path.join(main_dir,'Reports')
if not os.path.exists(reports_dir):
    os.makedirs(reports_dir)
NHLTable.to_html(os.path.join(reports_dir,'Players.html'),index = False, columns = ['Team', 'CP', 'Name', 'Pos', 'Age', 'Salary', 'Years', 'FI', 'SH', 'PL', 'ST', 'CH', 'PO', 'HI', 'SK', 'EN', 'PE', 'FA', 'LE', 'SR', 'OFF', 'DEF', 'OVE'])
ProspectTable.to_html(os.path.join(reports_dir,'Prospects.html'),index = False, columns = ['Team', 'Name', 'Pos', 'Age', 'Salary', 'Years', 'FI', 'SH', 'PL', 'ST', 'CH', 'PO', 'HI', 'SK', 'EN', 'PE', 'FA', 'LE', 'SR', 'OFF', 'DEF', 'OVE'])

# Adds a title to the two reports, and centers it so it matches the other reports
	# The code has been grouped together rather than done one after the other for easy reading and modification
print("Formating Reports")
file1 = os.path.join(reports_dir,'Players.html')
file2 = os.path.join(reports_dir,'Prospects.html')
f1 = open(file1)
f2 = open(file2)
soup1 = str(BeautifulSoup(f1, "html5lib"))
soup2 = str(BeautifulSoup(f2, "html5lib"))

# This is the added headers and footers for the page.
player_header = """ <HTML><HEAD><TITLE>Player Attributes</TITLE></HEAD>
<CENTER><FONT SIZE=16>Player Attributes</FONT><P><P><P>"""
player_footer = """</CENTER></HTML>"""
prospect_header = """ <HTML><HEAD><TITLE>Prospect Attributes</TITLE></HEAD>
<CENTER><FONT SIZE=16>Prospect Attributes</FONT><P><P><P>"""
prospect_footer = """</CENTER></HTML>"""

player_report_html = player_header + soup1 + player_footer
prospect_report_html = prospect_header + soup2 + prospect_footer

f1.close
f1 = open(file1,'w')
f1.write(player_report_html)

f2.close
f2 = open(file2,'w')
f2.write(prospect_report_html)


print("Stats compilation complete")