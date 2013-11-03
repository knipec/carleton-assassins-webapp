'''
    fixData.py

    Carissa Knipe
    Oct 18, 2013

    Formats each entry of the original data's spreadsheet into another spreadsheet as desired.
'''


import xlrd
import xlwt
import re
# import dateutil

# Note: Rounds start at 00:00 Sat

def main():

	global lastDay
	lastDay = ""

	dataSource = "webApp_data.xlsx"
	writeTo = "webApp_newData_oct18.xls"
	sheetIndex = 0
	killed_col = 0
	killer_col = 1
	time_col = 2
	death_col = 3
	location_col = 6

	workbook_r = xlrd.open_workbook(dataSource)
	sheet_r = workbook_r.sheet_by_index(sheetIndex)

	workbook_w = xlwt.Workbook()
	sheet_w = workbook_w.add_sheet("0")


	for row in range(sheet_r.nrows):
		if sheet_r.cell_value(row, 7) == "":
			lastDay = ""

		killed = sheet_r.cell_value(row, killed_col)
		killer = sheet_r.cell_value(row, killer_col)
		time = sheet_r.cell_value(row, time_col)
		death = sheet_r.cell_value(row, death_col)
		location = sheet_r.cell_value(row, location_col)

		sheet_w.write(row, killed_col, fixPlayer(killed.strip()))
		sheet_w.write(row, killer_col, fixPlayer(killer.strip(), killed))
		sheet_w.write(row, time_col, fixTime(time, row))
		sheet_w.write(row, death_col, fixDeath(death.strip()))
		sheet_w.write(row, 4, sheet_r.cell_value(row, 4))
		sheet_w.write(row, 5, fixRound(sheet_r.cell_value(row, 5)))
		sheet_w.write(row, location_col, location.strip())
		sheet_w.write(row, 7, sheet_r.cell_value(row, 7))

	workbook_w.save(writeTo)

	evalNewData(writeTo)


def fixPlayer(name, killedName=""):
	if (name.lower() == "enforced") or (name.lower() == "incinerated") or (name.lower() == "incineration") or (name.lower() == "n/a"):
		return "n/a"
	elif (name.lower() == "self destruct"):
		return killedName
	elif (name == "The Police (round-specific)"):
		return "The Police"
	else:
		return name

def fixRound(name):
	if name == "0 Round":
		return "00 Round"
	else:
		return name


def fixTime(time_str, row):
	newTime = ""
	pattern1 = re.compile(r"([0-9]+)\s*hours\s*([a-zA-Z]+)")
	pattern2 = re.compile(r"([0-9]+)\s*([a-zA-Z]+)")

	a1 = re.search(pattern1, time_str)
	a2 = re.search(pattern2, time_str)

	if ":" in time_str:
		index = time_str.index(":")
		if index-2 < 0 or not time_str[index-2].isdigit():
			hours = int(time_str[index-1:index]+time_str[index+1:index+3])
			# print "a " + str(hours)
		else:
			hours = int(time_str[index-2:index]+time_str[index+1:index+3])
			# print "b " + str(hours)
		if "PM" in time_str or "pm" in time_str or "P.M." in time_str:
			hours += 1200
		if "12" in time_str:
				hours -= 1200
		dayPattern = re.compile(r"([a-zA-Z][a-zA-Z][a-zA-Z])")
		day = re.search(dayPattern, time_str).groups()[0]
		newTime = addZerosAndColon(str(hours)) + " " + day

	elif (a1):
		hours = a1.groups()[0]
		day = a1.groups()[1]
		newTime = addZerosAndColon(str(hours)) + " " + day
		# print "a1"

	elif (a2):
		hours = a2.groups()[0]
		day = a2.groups()[1]
		newTime = addZerosAndColon(str(hours)) + " " + day
		# print "a2"

	global lastDay
	if newTime == "":
		return newTime

	minutes = int(newTime[0:2])*60 +  int(newTime[3:5])
	day = newTime[6:]
	newTime = minutes
	if day == "Sat" and lastDay == "":
		pass
	elif day == "Sun":
		newTime += 24 * 1 * 60
		lastDay = "Sun"
	elif day == "Mon":
		newTime += 24 * 2 * 60
		lastDay = "Mon"
	elif day == "Tues":
		newTime += 24 * 3 * 60
		lastDay = "Tues"
	elif day == "Wed":
		newTime += 24 * 4 * 60
		lastDay = "Wed"
	elif day == "Thurs":
		newTime += 24 * 5 * 60
		lastDay = "Thurs"
	elif day == "Fri":
		newTime += 24 * 6 * 60
		lastDay = "Fri"
	elif day == "Sat":
		newTime += 24 * 7 * 60
	return str(newTime)


def addZerosAndColon(num):
	while len(num) < 4:
		num = "0" + num
	# print num + " = num"
	return num[0:2] + ":" + num[2:4]


def fixDeath(name):
	newName = name.lower().capitalize()
	if (name == "Shot in Duel"):
		newName = "Shot (duel)"
	elif (name == "Stabbing"):
		newName = "Stabbed"
	elif (name == "Incinerated"):
		newName = "Incineration"
	return newName

def evalNewData(writeTo):
	workbook = xlrd.open_workbook(writeTo)
	sheet = workbook.sheet_by_index(0)

	sheetIndex = 0
	killed_col = 0
	killer_col = 1
	time_col = 2
	death_col = 3
	location_col = 6

	players = set()
	deaths = set()
	locations = set()


	for row in range(sheet.nrows):
		killed = sheet.cell_value(row, killed_col)
		killer = sheet.cell_value(row, killer_col)
		time = sheet.cell_value(row, time_col)
		death = sheet.cell_value(row, death_col)
		location = sheet.cell_value(row, location_col)

		if killed != "":
			players.add(killed.strip())
		if killer != "":
			players.add(killer.strip())
		if death != "":
			deaths.add(death.strip())
		if location != "":
			locations.add(location.strip())


	print "PLAYERS:"
	printSet(players)
	print "\nDEATHS:"
	printSet(deaths)
	print "\nLOCATIONS:"
	printSet(locations)


def printSet(printingSet):
	printingList = list(printingSet)
	printingList.sort()
	for item in printingList:
		try:
			print item + "."
		except TypeError:
			print "ERROR",
			print item


if __name__ == "__main__":
	main()
