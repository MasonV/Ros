import os
import re
import pandas as pd

Draftee = {
	'Rank' : [],
	'Name' : [],
	'Pos' : [],
	'Shot' : [],
	'Age' : [],
	'DoB' : [],	
	'Height' : [],
	'Weight' : [],
	'Country' : [],
	'Team' : [],
	'Leaugue' : [],
	'GP' : [],
	'G' : [],
	'A' : [],
	'Pts' : [],
	'+/-' : [],
	'PIM' : [],
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

def colour_rating(value):
	if 'A' in str(value):
		result = "color: red"
	elif 'B' in str(value): 
		result = "color: blue"
	elif 'C' in str(value): 
		result = "color: grey"
	else:
		result = "color: black"
	
	return result

def colour_offense(value):
	return "background-color: purple"
def colour_defense(value):
	return "background-color: orange"
def colour_overall(value):
	return "background-color: green"
	


print("Preparing to compile CSB. ") 
dir = os.path.dirname(os.path.abspath(__file__))
main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fname = os.path.join(main_dir,"Data Exporters\Hidden Data\CSB.txt")


with open(fname) as f:
    content = f.readlines()

# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content] 

print("Analyzing CSB text")
for line in content:
	text = line.split()
	if "#" in line:
		##start of a new player
		line_num = 1
	if line_num == 1:
		Draftee['Rank'].append(int(line[1:line.find(text[1])-1]))
		Name = str(text[1] + " " + text[2]).decode('utf-8').encode('ascii','ignore')
		Draftee['Name'].append(Name)
		Draftee['Pos'].append(text[3])
		Draftee['Shot'].append(text[4][5:])	
	elif line_num == 2:
		Draftee['Age'].append(int(text[1]))
		Draftee['DoB'].append(text[3])
		Draftee['Height'].append(text[5])
		Draftee['Weight'].append(text[7])
	elif line_num == 3:
		Country = line.find("Country: ")
		Team = line.find("Team: ")
		League = line.find("League: ")
		Draftee['Country'].append(line[Country+len("Country: "):Team-1])
		Draftee['Team'].append(line[Team+len("Team: "):League-1])
		Draftee['Leaugue'].append(line[League+len("League: "):])
	elif line_num == 4:	
		Draftee['GP'].append((int(text[1])))
		Draftee['G'].append((int(text[3])))
		Draftee['A'].append((int(text[5])))
		Draftee['Pts'].append((int(text[7])))
		Draftee['+/-'].append((int(text[9])))
		Draftee['PIM'].append(text[11])
	# elif line_num == 5:	
		#skip
	elif line_num == 6:
		Draftee['SH'].append(text[1])
		Draftee['PL'].append(text[3])
		Draftee['ST'].append(text[5])
		Draftee['CH'].append(text[7])
		Draftee['PO'].append(text[9])
		Draftee['HI'].append(text[11])
	elif line_num == 7:
		Draftee['SK'].append(text[1])
		Draftee['EN'].append(text[3])
		Draftee['PE'].append(text[5])
		Draftee['FA'].append(text[7])
		Draftee['LE'].append(text[9])
		Draftee['SR'].append(text[11])
		Draftee['FI'].append(text[13])
	elif line_num == 8 :
		Draftee['OFF'].append(text[1])
		Draftee['DEF'].append(text[3])
		Draftee['OVE'].append(text[5])
	# elif line_num > 9 :
		#skip
	elif line_num > 12:
		print("INFINITE LOOP OR SOMETHING! AHHHHHHHHHHHHHH!!!!!!!!")
		break
	
	line_num += 1
	
	
print("Committing data to tables.")
Draft = pd.DataFrame(Draftee)
Draft = Draft[['Rank', 'Name', 'Pos', 'Shot', 'Age', 'DoB', 'Height', 'Weight', 'Country', 'Team', 'Leaugue', 'GP', 'G', 'A', 'Pts', '+/-', 'PIM', 'FI', 'SH', 'PL', 'ST', 'CH', 'PO', 'HI', 'SK', 'EN', 'PE', 'FA', 'LE', 'SR', 'OFF', 'DEF', 'OVE']]

Draft = Draft.sort_values(by=['Rank'], ascending = True)
html = (Draft.style.\
	set_properties(**{'border-width' : 'thin', 'border-color' : 'black'}).\
	applymap(colour_offense, subset=['SH', 'PL', 'ST', 'OFF']).\
	applymap(colour_defense, subset=['CH', 'PO', 'HI', 'DEF']).\
	applymap(colour_overall, subset=['SK', 'EN', 'PE', 'FA', 'LE', 'SR', 'OVE']).\
	applymap(colour_rating, subset=['SH', 'PL', 'ST', 'OFF', 'CH', 'PO', 'HI', 'DEF', 'SK', 'EN', 'PE', 'FA', 'LE', 'SR', 'OVE']).render())
# Draft.style


print("Exporting data to .html file")
reports_dir = os.path.join(main_dir,'Reports')
if not os.path.exists(reports_dir):
    os.makedirs(reports_dir)

with open(os.path.join(reports_dir,'Draft.html'), 'w') as f:
    f.write(html)
	
# Draft.to_html(os.path.join(reports_dir,'Draft.html'),index = False, columns = ['Rank', 'Name', 'Pos', 'Shot', 'Age', 'DoB', 'Height', 'Weight', 'Country', 'Team', 'Leaugue', 'GP', 'G', 'A', 'Pts', '+/-', 'PIM', 'FI', 'SH', 'PL', 'ST', 'CH', 'PO', 'HI', 'SK', 'EN', 'PE', 'FA', 'LE', 'SR', 'OFF', 'DEF', 'OVE'])