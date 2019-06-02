from bs4 import BeautifulSoup
import pandas as pd
import datetime
import os
import re
dt = datetime.datetime

##Get the absolute paths to this and parent directory, and initialize list of teams & stats structures
print("Preparing to compile staff information.")
dir = os.path.dirname(os.path.abspath(__file__))
main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
reports_dir = os.path.join(main_dir,'Reports')
file_name = os.path.join(main_dir,'players.ehm')


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
	'POT' : [],
	'CON' : [],
	'GRE' : [],
	'Click' : [],
	'Nationality' : [],
	'Birthday' : [],
	'Draft Year' : [],
	'Draft Round' : [],
	'Draft By' : [],
	'Rights' : [],
	'Week' : [],
	'Month' : [],
	'C_FI' : [],
	'C_SH' : [],
	'C_PL' : [],
	'C_ST' : [],
	'C_CH' : [],
	'C_PO' : [],
	'C_HI' : [],
	'C_SK' : [],
	'C_EN' : [],
	'C_PE' : [],
	'C_FA' : [],
	'C_LE' : [],
	'C_SR' : [],
}

Teams = { 
	"1" : "ANA",
	"2" : "VGK",
	"3" : "BOS",
	"4" : "BUF",
	"5" : "CGY",
	"6" : "CAR",
	"7" : "CHI",
	"8" : "COL",
	"9" : "CBS",
	"10" : "DAL",
	"11" : "DET",
	"12" : "EDM",
	"13" : "FLA",
	"14" : "LA",
	"15" : "MIN",
	"16" : "MTL",
	"17" : "NAS",
	"18" : "NJ",
	"19" : "NYI",
	"20" : "NYR",
	"21" : "OTT",
	"22" : "PHI",
	"23" : "WIN",
	"24" : "PIT",
	"25" : "SJ",
	"26" : "STL",
	"27" : "TB",
	"28" : "TOR",
	"29" : "VAN",
	"30" : "WSH",
} 

Countries = { 
	"1" : "Canada",
	"2" : "USA",
	"3" : "Russia",
	"4" : "Czech",
	"5" : "Sweden",
	"6" : "Finland",
	"7" : "Belarussia",
	"8" : "Slovakia",
	"9" : "Norway",
	"10" : "Germany",
	"11" : "Italy",
	"12" : "Austria",
	"13" : "Latvia",
	"14" : "Ukraine",
	"15" : "Solvenia",
	"16" : "Switzerland",
	"17" : "Poland",
	"18" : "France",
} 

Positions = { 
	"1" : "Head Coach",
	"2" : "Assistant Coach",
	"3" : "General Manager",
	"4" : "Scout",
	"5" : "Physio",
}


def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


NumLines = int(file_len(file_name))

with open(file_name) as f:
    lines = f.readlines()
	

print("Processing " + str(NumLines) + " Player members.")
	
batchline = 0
linecount = 0
for line in lines:
	if linecount%100 == 0:
		print(str(linecount) + " / " + str(NumLines) + " processed.")
		
	#Processing batch line by line.
	if batchline > 19:
		batchline = 0
	
	# print(line)
	
	data = line.rstrip("\n").split()
	# print("Batchline: " + str(batchline) + ". & Data: " + str(data))
	try:
		if batchline == 0: 
			Player['SH'].append(int(data[0]))
			Player['PL'].append(int(data[1]))
			Player['ST'].append(int(data[2]))
			Player['CH'].append(int(data[3]))
			Player['PO'].append(int(data[4]))
			Player['HI'].append(int(data[5]))
			Player['SK'].append(int(data[6]))
			Player['EN'].append(int(data[7]))
			Player['PE'].append(int(data[8]))
			Player['FA'].append(int(data[9]))
		if batchline == 1:
			Player['LE'].append(int(data[0]))
			Player['SR'].append(int(data[1]))
			Player['POT'].append(int(data[2]))
			Player['CON'].append(int(data[3]))
			Player['GRE'].append(int(data[4]))
			Player['FI'].append(int(data[5]))
			Player['Click'].append(int(data[6]))
			Player['Team'].append(int(data[7]))
			Player['Pos'].append(int(data[8]))
			Player['Nationality'].append(Countries.get(data[9]))
			Player['Pos'].append(int(data[10]))
		if batchline == 2:
			BDayString = data[0] + " " + data[3] + " " + data[1]
			Bday = dt.strptime(BDayString,"%Y  %m %d") 
			Player['Birthday'].append(Bday)
			Player['Salary'].append(int(data[3]))
			Player['Years'].append(int(data[4]))
			Player['Draft Year'].append(int(data[5]))
			Player['Draft Round'].append(int(data[6]))
			Player['Draft By'].append(Teams.get(data[7]))
			Player['Rights'].append(Teams.get(data[8]))
		if batchline == 3:
			Player['Week'].append(line.rstrip("\n"))
		if batchline == 4:
			Player['Month'].append(line.rstrip("\n"))
		# if batchline == 6:
		# if batchline == 7:
		# if batchline == 8:
		# if batchline == 9:
		# if batchline == 10:
		# if batchline == 11:
		# if batchline == 12:
		if batchline == 13:
			Name = data[0] + " " + data[1]
			Name = Name.decode('latin-1').encode('ascii','ignore')
			Staff['Name'].append(Name)
		# if batchline == 14:
		# if batchline == 15:
		if batchline == 16:
			Player['C_FI'].append(data[0])
			Player['C_SH'].append(data[1])
			Player['C_PL'].append(data[2])
			Player['C_ST'].append(data[3])
			Player['C_CH'].append(data[4])
			Player['C_PO'].append(data[5])
			Player['C_HI'].append(data[6])
			Player['C_SK'].append(data[7])
			Player['C_EN'].append(data[8])
			Player['C_PE'].append(data[9])
			Player['C_FA'].append(data[10])
			Player['C_LE'].append(data[11])
			Player['C_SR'].append(data[12])	
		# if batchline == 17:
		# if batchline == 18:
		# if batchline == 19:
	except: 
		print("Batchline: " + str(batchline) + ". & Data: " + str(data))
		break
	
	batchline += 1
	linecount += 1

print("Commiting data to tables.")
PlayerTable = pd.DataFrame(Player)

print("Exporting data to .html file")
PlayerTable.to_html(os.path.join(reports_dir,"AllData.html"),index = False, columns = ['Name', 'Team', 'Salary', 'Years', 'Position', 'Prerferred', 'PS', 'DI', 'DPR', 'EO', 'ED', 'EG', 'HT', 'MP', 'RE', 'Reliabililty','Birthday', 'Nationality', 'Wins', 'Loses', 'Ties', 'Reputaiton', 'Cups Won'])

print("Formating Reports")
file = os.path.join(os.path.join(reports_dir,"AllData.html"))
with open(file) as f:
	soup = str(BeautifulSoup(f, "html5lib"))
	
player_header = """ <HTML><HEAD><TITLE>World Wide Players</TITLE></HEAD>
<CENTER><FONT SIZE=16>World Wide Players</FONT><P><P><P>
"""
player_footer = """</CENTER></HTML>"""
player_report_html = player_header + soup + player_footer

with open(file,'w') as f:
	f.write(staff_report_html)


print("Player compilation complete")