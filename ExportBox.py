from bs4 import BeautifulSoup
import pandas as pd
import os
import re

##Get the absolute paths to this and parent directory, and initialize list of teams & stats structures
print("Preparing to compile league stats. Estimated Time To Completion: 60 seconds ") 
dir = os.path.dirname(os.path.abspath(__file__))
main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
reports_dir = os.path.join(main_dir,'Reports')

Months = ["September", "October", "November", "December", "January", "February", "March", "April"]
# Months = ["January"]

GameData = {
	'Date' : [],
	# 'Team1' : [],
	# 'Team2' : [],
	'Goalie1' : [],
	'Goalie2' : [],
	'GoalieB1' : [],
	'GoalieB2' : [],
	'SVG1' : [],
	'SVG2' : [],
	'SVB1' : [],
	'SVB2' : [],
	'GAG1' : [],
	'GAG2' : [],
	'GAB1' : [],
	'GAB2' : [],	
}

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


print("Searching for stat files in directory:")
print(os.path.join(main_dir, 'html\\'))


for month in Months:
	batchline = 0
	linecount = 0
	GoalieBatch = 0
	International = False
	GameSection = "Start"
	print("Analyzing Month: " + month + ".")
	file_name = os.path.join(main_dir, 'html\\', month + ".html")
	NumLines = int(file_len(file_name))

	with open(file_name) as f:
		lines = f.readlines()

	
	for line in lines:
		if line != "": #won't add to line counts and stuff if its an empty line
			#Processing batch line by line.

			if linecount%1000 == 0: #Progress Update
				print(str(linecount) + " / " + str(NumLines) + " processed.")
				
			if re.search('([0-9]){1,2}\.([0-9]){1,2}\.([0-9]){4}',line.rstrip("\n")) != None:
				GameSection = "Header"
				batchline = 0
			elif "Ticket income: 0" in line:
				International = True
			elif International == False:
				if "BOXSCORE" in line:
					GameData['Date'].append(date)
					GameSection = "BoxScore"			
					batchline = 0
				elif "Penalty" in line:
					GameSection = "PenaltySummary"				
					batchline = 0
				elif "scoring" in line:
					if GameSection != "Score":
						GameSection = "Score"
						batchline = 0
				elif "Three stars of the game" in line:
					GameSection = "Stars"					
					batchline = 0
				elif "Notes for" in line:
					GameSection = "Notes"					
					batchline = 0
			
			# print("Section: " + str(GameSection) + " | " + line)
				
			if GameSection == "Header":
				try:
					if batchline == 0: 
						date = line.replace("<h2>","").replace("</h2>","").rstrip("\n")
					# if batchline == 1: 
						# data = line.rstrip("\n").split()
						# GameData['Team1'].append(data[0]+" "+data[1])
						# GameData['Team2'].append(data[4]+" "+data[5])
					# if batchline == 2: #skip the rest for now
				except: 
					print("Batchline: " + str(batchline) + ". & Data: " + str(data))
					break
				batchline += 1

			# if GameSection == "BoxScore": #Skip 
				# try:
					# if batchline == 0: 
						# GameData['Date'].append(line.rstrip("\n"))
				# except: 
					# print("Batchline: " + str(batchline) + ". & Data: " + str(data))
					# break
				# batchline += 1

			# if GameSection == "PenaltySummary": #Skip 
				# try:
					# if batchline == 0: 
						# GameData['Date'].append(line.rstrip("\n"))
				# except: 
					# print("Batchline: " + str(batchline) + ". & Data: " + str(data))
					# break
				# batchline += 1


			if GameSection == "Score": 
				try:
					data = line.rstrip("\n").split()
					if line.startswith("G "):
						if GoalieBatch == 0:
							GameData['Goalie1'].append(data[1]+' '+data[2])
							GameData['SVG1'].append(data[-5])
							GameData['GAG1'].append(data[-7])
							GoalieBatch += 1
						elif GoalieBatch == 1:
							GameData['GoalieB1'].append(data[1]+' '+data[2])
							GameData['SVB1'].append(data[-5])
							GameData['GAB1'].append(data[-7])
							GoalieBatch += 1
						elif GoalieBatch == 2:
							GameData['Goalie2'].append(data[1]+' '+data[2])
							GameData['SVG2'].append(data[-5])
							GameData['GAG2'].append(data[-7])
							GoalieBatch += 1
						elif GoalieBatch == 3:
							GameData['GoalieB2'].append(data[1]+' '+data[2])
							GameData['SVB2'].append(data[-5])
							GameData['GAB2'].append(data[-7])
							GoalieBatch = 0								
				except: 
					print("Batchline/GoalieBatch: " + str(batchline) + "/" + str(GoalieBatch) + ". & Data: " + str(line))
					break
				batchline += 1
					
		linecount += 1
	print('Date' + " : " + str(len(GameData['Date'])))
	print('Goalie1' + " : " + str(len(GameData['Goalie1'])))
	print('Goalie2' + " : " + str(len(GameData['Goalie2'])))
	print('GoalieB1' + " : " + str(len(GameData['GoalieB1'])))
	print('GoalieB2' + " : " + str(len(GameData['GoalieB2'])))
	print('SVG1' + " : " + str(len(GameData['SVG1'])))
	print('SVG2' + " : " + str(len(GameData['SVG2'])))
	print('SVB1' + " : " + str(len(GameData['SVB1'])))
	print('SVB2' + " : " + str(len(GameData['SVB2'])))
	print('GAG1' + " : " + str(len(GameData['GAG1'])))
	print('GAG2' + " : " + str(len(GameData['GAG2'])))
	print('GAB1' + " : " + str(len(GameData['GAB1'])))
	print('GAB2' + " : " + str(len(GameData['GAB2'])))
		
	

			
			
			
print("Commiting data to tables.")
# print(GameData)




GameTable = pd.DataFrame(GameData)

print("Exporting data to .html file")
# GameTable.to_html(os.path.join(reports_dir,"BoxScore.html"),index = False, columns = ['Date', 'Team1', 'Team2', 'Goalie1', 'Goalie2', 'GoalieB1', 'GoalieB2', 'SVG1', 'SVG2', 'SVB1', 'SVB2', 'GAG1', 'GAG2', 'GAB1', 'GAB2'])
GameTable.to_html(os.path.join(reports_dir,"BoxScore.html"),index = False, columns = ['Date',  'Goalie1', 'Goalie2', 'GoalieB1', 'GoalieB2', 'SVG1', 'SVG2', 'SVB1', 'SVB2', 'GAG1', 'GAG2', 'GAB1', 'GAB2'])



print("Stats compilation complete")