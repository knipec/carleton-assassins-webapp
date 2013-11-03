''' 
	Separates the one table into multiple different tables

1. Kills
2. Players
3. Deathcauses
4. Rounds
5. Terms

'''
import xlrd
import re
# import xlwt


def main():
	global lastDay
	lastDay = ""

	dataSource = "webApp_newData_derp.xls"
	# allkillsFile = open("webApp_allkills.csv", "w")
	# playersFile = open("webApp_players.csv", "w")
	deathcausesFile = open("webApp_deathcauses.csv", "w")
	# termsFile = open("webApp_terms.csv", "w")
	# roundsFile = open("webApp_rounds.csv", "w")
	# locationsFile = open("webApp_locations.csv", "w")

	players = {}
	deathcauses = {}
	rounds = {}
	terms = {}
	locations = {}

	workbook = xlrd.open_workbook(dataSource)
	sheet = workbook.sheet_by_index(0)


	for row in range(sheet.nrows):
		if sheet.cell_value(row, 7) == "":
			lastDay = ""

		killed = sheet.cell_value(row, 0)
		killer = sheet.cell_value(row, 1)
		deathcause = sheet.cell_value(row, 3)
		term = sheet.cell_value(row, 4)
		round = sheet.cell_value(row, 5)
		location = sheet.cell_value(row, 6)
		winner = sheet.cell_value(row, 7)
		f = [None,None,None,None,None,None,None,None]
		f[0] = addToDict(killed, players)
		f[1] = addToDict(killer, players)
		f[2] = sheet.cell_value(row, 2)
		f[3] = addToDict(deathcause, deathcauses)
		f[4] = addToDict(term, terms)
		f[5] = addToDict(round, rounds)
		f[6] = addToDict(location, locations)
		f[7] = addToDict(winner, players)

		# allkillsFile.write(f[0] + "," + f[1] + "," + f[2] + "," + f[3] + "," + f[4] + "," + f[5] + "," + f[6] + "," + f[7] + "\n")

	# for player in players:
	# 	playerID = players[player]
	# 	playersFile.write(playerID + "," + player + "\n")
	# 	# print "(", playerID, ", ", player, ")"

	for deathcause in deathcauses:
		deathcauseID = deathcauses[deathcause]
		deathcausesFile.write(deathcauseID + "," + deathcause + "\n")
		print "(", deathcauseID, ", ", deathcause, ")"

	# for term in terms:
	# 	termID = terms[term]
	# 	termsFile.write(termID + "," + term + "\n")
	# 	# print "(", termID, ", ", term, ")"

	# for round in rounds:
	# 	roundID = rounds[round]
	# 	roundsFile.write(roundID + "," + round + "\n")
	# 	# print "(", roundID, ", ", round, ")"

	# for location in locations:
	# 	locationID = locations[location]
	# 	locationsFile.write(locationID + "," + location + "\n")


def addToDict(entry, dictionary):
	if entry == "":
		return entry
	if entry not in dictionary:
		dictionary[entry] = str(len(dictionary))
	return dictionary[entry]

def fixTime(time):
	global lastDay

	if time == "":
		return time

	hours = int(time[0:2] + time[3:5])
	day = time[6:]

	newTime = hours
	if day == "Sat" and lastDay == "":
		pass	
	elif day == "Sun":
		newTime += 2400 * 1
		lastDay = "Sun"
	elif day == "Mon":
		newTime += 2400 * 2
		lastDay = "Mon"
	elif day == "Tues" or day == "Tue":
		newTime += 2400 * 3
		lastDay = "Tue"
	elif day == "Wed":
		newTime += 2400 * 4
		lastDay = "Wed"
	elif day == "Thurs" or day == "Thur":
		newTime += 2400 * 5
		lastDay = "Thur"
	elif day == "Fri":
		newTime += 2400 * 6
		lastDay = "Fri"
	elif day == "Sat":
		newTime += 2400 * 7

	return str(newTime)

if __name__ == "__main__":
	main()