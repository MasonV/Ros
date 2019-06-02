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
file_name = 'Hidden Data/staff.ehm'


Staff = {
	'PS' : [],
	'DI' : [],
	'DPR' : [],
	'EO' : [],
	'ED' : [],
	'EG' : [],
	'HT' : [],
	'MP' : [],
	'RE' : [],
	'Reliabililty' : [],
	'Nationality' : [],
	'Birthday' : [],
	'Unknown 1' : [],
	'Unknown 2' : [],
	'Scouting Team' : [],
	'Shortlist' : [],
	'Scouting Country' : [],
	'Team' : [],
	'Salary' : [],
	'Position' : [],
	'Prerferred' : [],
	'Unkown 3' : [],
	'Wins' : [],
	'Loses' : [],
	'Ties' : [],
	'Reputaiton' : [],
	'Cups Won' : [],
	'Cotnract Years' : [],
	'Name' : [],
	'Unknown 4' : [],
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
	"23" : "PIT",
	"24" : "SJ",
	"25" : "STL",
	"26" : "TBL",
	"27" : "TOR",
	"28" : "VAN",
	"29" : "WSH",
	"30" : "WIN",
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

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1
	
NumLines = int(file_len(file_name))

with open(file_name) as f:
    lines = f.readlines()
	

print("Processing " + str(NumLines) + " Staff members.")
	
batchline = 0
linecount = 0
for line in lines:
	if linecount%100 == 0:
		print(str(linecount) + " / " + str(NumLines) + " processed.")
		
	#Processing batch line by line.
	if batchline > 12:
		batchline = 0
	
	# print(line)
	
	data = line.rstrip("\n").split()
	# print("Batchline: " + str(batchline) + ". & Data: " + str(data))
	try:
		if batchline == 0: 
			Staff['PS'].append(int(data[0]))
			Staff['DI'].append(int(data[1]))
			Staff['DPR'].append(int(data[2]))
			Staff['EO'].append(int(data[3]))
		if batchline == 1:
			Staff['ED'].append(int(data[0]))
			Staff['EG'].append(int(data[1]))
			Staff['HT'].append(int(data[2]))
			Staff['MP'].append(int(data[3]))
		if batchline == 2:
			Staff['RE'].append(int(data[0]))
			Staff['Reliabililty'].append(int(data[1]))
			Staff['Unknown 1'].append(data[2])
			Staff['Unknown 2'].append(data[3])
		if batchline == 3:
			Staff['Nationality'].append(Countries.get(data[0]))
			BDayString = data[1] + " " + data[2] + " " + data[3]
			Bday = dt.strptime(BDayString,"%Y  %m %d") 
			Staff['Birthday'].append(Bday)
		if batchline == 4:
			Staff['Scouting Team'].append(data[0])
			Staff['Shortlist'].append(data[1])
			Staff['Scouting Country'].append(data[2])
		if batchline == 5:
			Staff['Team'].append(Teams.get(data[0]))
			Staff['Salary'].append(data[1])
			Staff['Position'].append(data[2])
			Staff['Prerferred'].append(data[3])
			Staff['Unkown 3'].append(data[4])
		if batchline == 6:
			Staff['Wins'].append(data[0])
			Staff['Loses'].append(data[1])
			Staff['Ties'].append(data[2])
		if batchline == 7:
			Staff['Reputaiton'].append(data[0])
			Staff['Cups Won'].append(data[1])
			Staff['Cotnract Years'].append(data[2])
		if batchline == 8:
			Name = data[0] + " " + data[1]
			Name = Name.decode('latin-1').encode('ascii','ignore')
			Staff['Name'].append(Name)
		if batchline == 9:
			Staff['Unknown 4'].append(data[0])
	except: 
		print("Batchline: " + str(batchline) + ". & Data: " + str(data))
		break
	
	batchline += 1
	linecount += 1

print("Commiting data to tables.")
StaffTable = pd.DataFrame(Staff)


print("Exporting data to .html file")
StaffTable.to_html(os.path.join(reports_dir,"Staff.html"),index = False, columns = ['Name', 'Team', 'Salary', 'Position', 'Prerferred', 'PS', 'DI', 'DPR', 'EO', 'ED', 'EG', 'HT', 'MP', 'RE', 'Birthday', 'Reliabililty', 'Nationality', 'Scouting Team', 'Shortlist', 'Scouting Country', 'Wins', 'Loses', 'Ties', 'Reputaiton', 'Cups Won', 'Cotnract Years', 'Unknown 1', 'Unknown 2', 'Unkown 3', 'Unknown 4'])

print("Formating Reports")
file = os.path.join(os.path.join(reports_dir,"Staff.html"))
with open(file) as f:
	soup = str(BeautifulSoup(f, "html5lib"))
	
staff_header = """ <HTML><HEAD><TITLE>World Wide Hockey Staff</TITLE></HEAD>
<CENTER><FONT SIZE=16>World Wide Hockey Staff</FONT><P><P><P>
"""
staff_footer = """</CENTER></HTML>"""
staff_report_html = staff_header + soup + staff_footer

with open(file,'w') as f:
	f.write(staff_report_html)


print("Staff compilation complete")