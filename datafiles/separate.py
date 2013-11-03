''' 
    separate.py

    Carissa Knipe
    Oct 18, 2013

    Normalizes the tables, separating the one table (created by fixData.py) into several:
1. Kills
2. Players
3. Deathcauses
4. Rounds
5. Terms
6. Locations

'''
import xlrd
import re
# import xlwt


def main():
	global lastDay
	lastDay = ""

	dataSource = "webApp_newData_oct18.xls"
	allkillsFile = open("webApp_allkills.csv", "w")
	playersFile = open("webApp_players.csv", "w")
	deathcausesFile = open("webApp_deathcauses.csv", "w")
	termsFile = open("webApp_terms.csv", "w")
	roundsFile = open("webApp_rounds.csv", "w")
	locationsFile = open("webApp_locations.csv", "w")

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
		f[5] = addToDict(term + " - " + round, rounds)
		f[6] = addToDict(location, locations)
		f[7] = addToDict(winner, players)

		allkillsFile.write(f[0] + "," + f[1] + "," + f[2] + "," + f[3] + "," + f[4] + "," + f[5] + "," + f[6] + "," + f[7] + "\n")

	for player in players:
		playerID = players[player]
		playersFile.write(playerID + "," + player + "\n")
		# print "(", playerID, ", ", player, ")"

	for deathcause in deathcauses:
		deathcauseID = deathcauses[deathcause]
		deathcausesFile.write(deathcauseID + "," + deathcause + "\n")
		print "(", deathcauseID, ", ", deathcause, ")"

	for term in terms:
		termID = terms[term]
		termsFile.write(termID + "," + term + "\n")
		# print "(", termID, ", ", term, ")"

	for round in rounds:
		roundID = rounds[round]
		roundsFile.write(roundID + "," + round + "\n")
		# print "(", roundID, ", ", round, ")"

	for location in locations:
		locationID = locations[location]
		locationsFile.write(locationID + "," + location + "\n")


def addToDict(entry, dictionary):
	if entry == "":
		return entry
	if entry not in dictionary:
		dictionary[entry] = str(len(dictionary))
	return dictionary[entry]


if __name__ == "__main__":
	main()
