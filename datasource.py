'''
    datasource.py

    Carissa Knipe
    Oct 18, 2013

    Opens a connection to database, does several specific queries used by htmlcreator.py
'''

import psycopg2
import re

class DataSource:
    def __init__(self):
        '''Opens a connection and a cursor'''
        self.database = "knipec"
        self.user = "knipec"
        self.password = "purr625catnip"
        self.connection = None
        self.cursor = None
        try:
            self.connection = psycopg2.connect(database=self.database, user=self.user, password=self.password)
        except Exception, e:
            print "Connection error: ", e
            print "</body>\n</html>"
            exit()
        try:
            self.cursor = self.connection.cursor()
        except Exception, e:
            print "Cursor error", e


    def playerExists(self, player):
        '''Check if the given player exists'''
        query = "SELECT players.player FROM players WHERE players.player='" + player + "';"
        self.cursor.execute(query)
        return len(self.cursor.fetchall()) > 0

    
    def getPlayerKillInfo(self, player):
        '''Returns list of 5-tuples (name of player killed, deathcause, round, term, time killed) for each kill made by the player'''
        if not self.playerExists(player):
            return None
        else:
            killList = []
            query = """
SELECT p2.player, deathcauses.deathcause, terms.term, rounds.round, a.time 
FROM allkills a, players p1, players p2, terms, rounds, deathcauses  
WHERE a.killer=p1.id
AND p1.player='""" + player + """'
AND a.killed=p2.id
AND a.term=terms.id AND a.round=rounds.id AND a.deathcause=deathcauses.id;"""
            self.getData(query)
            result = self.cursor.fetchall()
            for row in result:
                killList.append((row[0], row[1], row[2], row[3], self.formatTime(row[4])))
            return killList


    def getPlayerDeathInfo(self, player):
        '''Returns list of 5-tuples (name of killer, deathcause, round, term, time killed) for each time the player died'''
        if not self.playerExists(player):
            return None
        else:
            deathList = []
            query = """
SELECT p2.player, deathcauses.deathcause, terms.term, rounds.round, a.time 
FROM allkills a, players p1, players p2, terms, rounds, deathcauses 
WHERE a.killed=p1.id
AND p1.player='""" + player + """'
AND a.killer=p2.id
AND a.term=terms.id AND a.round=rounds.id AND a.deathcause=deathcauses.id;"""
            self.getData(query)
            result = self.cursor.fetchall()
            for row in result:
                deathList.append((row[0], row[1], row[2], row[3], self.formatTime(row[4])))
            return deathList


    def getPlayerKDRatio(self, player):
        '''Given a player, returns a string of their kill to death ratio'''
        playerKills = len(self.getPlayerKillInfo(player))
        playerDeaths = len(self.getPlayerDeathInfo(player))
        if playerDeaths < 1:
            return """INFINITY!!!"""
        else:
            ratio = (float(playerKills)/playerDeaths)
            return '%0.3f' % (ratio)
        

    def getPlayerRounds(self, player):
        '''Returns a list of the names of rounds that the player played'''
        allPlayersAndRounds = self.getPlayersAndRoundsPlayed()
        for playerRounds in allPlayersAndRounds:
            if playerRounds[0] == player:
                return playerRounds[1]
        return []


    def getListOfPlayers(self):
        '''Returns a list of the names of all players who have been in any round in alphabetical order'''
        playersList = []
        query = "SELECT players.player FROM players"
        self.getData(query)
        result = self.cursor.fetchall()
        for row in result:
            playersList.append(row[0])
        playersList.sort()
        return playersList


    def getListOfDeathMethods(self):
        '''Returns a list of methods of death and how many times they happened in the history of Assassins'''
        query = "SELECT deathcauses.deathcause FROM deathcauses, allkills WHERE deathcauses.id=allkills.deathcause"
        self.getData(query)
        deathDict = {}
        deathList = []
        result = self.cursor.fetchall()
        if len(result) > 0:
            for row in result:
                if row[0] not in deathDict:
                    deathDict[row[0]] = 1
                else:
                    deathDict[row[0]] += 1
        for death in deathDict:
            deathList.append((death,deathDict[death]))
            deathList.sort(key=lambda x: x[1], reverse=True)
        return deathList

    
    def getPlayersAndTotalKills(self):
        '''Returns a list of tuples (players and their number of total kills)'''
        playerKillDict = {}
        playerKillList = []
        for player in self.getListOfPlayers():
            playerKillDict[player] = 0
        query = """
SELECT players.player
FROM players, allkills
WHERE players.id=allkills.killer;"""
        self.getData(query)
        result = self.cursor.fetchall()
        if len(result) > 0:
            for row in result:
                playerKillDict[row[0]] += 1
        for killer in playerKillDict:
            playerKillList.append((killer, playerKillDict[killer]))
        playerKillList.sort(key=lambda x: x[1], reverse=True)
        # If k players have the same number of kills, order them alphabetically
        startIndex = 0
        for index in range(len(playerKillList)):
            if playerKillList[index][1] != playerKillList[startIndex][1]:
                subList = playerKillList[startIndex:index]
                subList.sort()
                playerKillList[startIndex:index] = subList
                startIndex = index
        return playerKillList


    def getPlayersAndRoundsPlayed(self):
        '''Returns a list of players and number of rounds played in'''
        playerRoundsDict = {}
        playerRoundsList = []
        query = """
SELECT p1.player, p2.player, p3.player, rounds.round, terms.term
FROM players p1, players p2, players p3, allkills, rounds, terms
WHERE p1.id=allkills.killed 
AND p2.id=allkills.killer 
AND p3.id=allkills.winner
AND rounds.id=allkills.round
AND terms.id=allkills.term;"""
        self.getData(query)
        result = self.cursor.fetchall()
        if len(result) > 0:
            for row in result:
                if row[0] not in playerRoundsDict:
                    playerRoundsDict[row[0]] = [(row[3], row[4])]
                elif (row[3], row[4]) not in playerRoundsDict[row[0]]:
                    playerRoundsDict[row[0]].append((row[3], row[4]))
                if row[1] not in playerRoundsDict:
                    playerRoundsDict[row[1]] = [(row[3], row[4])]
                elif (row[3], row[4]) not in playerRoundsDict[row[1]]:
                    playerRoundsDict[row[1]].append((row[3], row[4]))                
                if row[2] not in playerRoundsDict:
                    playerRoundsDict[row[2]] = [(row[3], row[4])]
                elif (row[3], row[4]) not in playerRoundsDict[row[2]]:
                    playerRoundsDict[row[2]].append((row[3], row[4]))
        for player in self.getListOfPlayers():
            pass
        for player in playerRoundsDict:
            playerRoundsList.append((player, playerRoundsDict[player]))
        playerRoundsList.sort(key=lambda x: len(x[1]), reverse=True)
        # If k players have the same number of kills, order them alphabetically
        startIndex = 0
        for index in range(len(playerRoundsList)):
            if len(playerRoundsList[index][1]) != len(playerRoundsList[startIndex][1]):
                subList = playerRoundsList[startIndex:index]
                subList.sort()
                playerRoundsList[startIndex:index] = subList
                startIndex = index
        return playerRoundsList


    def getPlayersAndKDRatios(self):
        '''Returns list of tuples including (player, K/D ratio) for all players, sorted by K/D ratio'''
        players = []
        for player in self.getListOfPlayers():
            players.append((player, self.getPlayerKDRatio(player)))
        players.sort(key=lambda x: x[1], reverse=True) 
        return players


    def getWinners(self):
        '''Returns list of 3-tuples including (winner name, term won, round won)'''
        winnerDict = {}
        winnerList = []
        query = """
SELECT players.player, terms.term, rounds.round
FROM allkills, players, terms, rounds
WHERE allkills.winner=players.id
AND allkills.term=terms.id
AND allkills.round=rounds.id;"""
        self.getData(query)
        result = self.cursor.fetchall()
        if len(result) > 0:
            for row in result:
                if row[0] not in winnerDict:
                    winnerDict[row[0]] = [(row[1], row[2])]
                elif (row[1], row[2]) not in winnerDict[row[0]]:
                    winnerDict[row[0]].append((row[1], row[2]))
        for winner in winnerDict:
            for roundWon in winnerDict[winner]:
                winnerList.append((winner, roundWon[0], roundWon[1]))
        return winnerList



    def getTermsAndRounds(self):
        '''Returns list of tuples including (term, round)'''
        roundsTermsList = []
        query = """
SELECT terms.term, rounds.round
FROM allkills, terms, rounds
WHERE allkills.term=terms.id
AND allkills.round=rounds.id;"""
        self.getData(query)
        result = self.cursor.fetchall()
        if len(result) > 0:
            for row in result:
                if (row[0], row[1]) not in roundsTermsList:
                    roundsTermsList.append((row[0], row[1]))
        return roundsTermsList


    def getRoundKills(self, term, round):
        '''Returns list of 4-element lists including [killed, killer, death cause, time of death] for a given round and term'''
        roundList = []
        query = """
SELECT p1.player, p2.player, deathcauses.deathcause, allkills.time
FROM players p1, players p2, deathcauses, allkills, terms, rounds
WHERE allkills.killed=p1.id
AND allkills.killer=p2.id
AND allkills.deathcause=deathcauses.id
AND allkills.term=terms.id
AND allkills.round=rounds.id
AND terms.term='""" + term + """'
AND rounds.round='""" + round + """';"""
        self.getData(query)
        result = self.cursor.fetchall()
        if len(result) > 0:
            for row in result:
                roundList.append([row[0], row[1], row[2], row[3]])
        roundList.sort(key=lambda x: x[3])
        for index in range(len(roundList)):
            roundList[index][3] = self.formatTime(roundList[index][3])
        return roundList

    
    def getRoundWinners(self, term, round):
        '''Returns list of winners for a given round and term. Usually will just be one player'''
        winnerSet = set()
        winnerList = []
        query = """
SELECT players.player
FROM allkills, players, terms, rounds
WHERE allkills.winner=players.id
AND allkills.term=terms.id
AND allkills.round=rounds.id
AND rounds.round='""" + round + """'
AND terms.term='""" + term + """';"""
        self.getData(query)
        result = self.cursor.fetchall()
        if len(result) > 0:
            for row in result:
                winnerSet.add(row[0])
        for winner in winnerSet:
            winnerList.append(winner)
        return winnerList


    def addZeros(self, time):
        '''Adds leading zeros to one-digit hours or minutes for formatTime'''
        if len(time) < 2:
            return "0" + time
        else:
            return time

    def formatTime(self, time):
        '''Times are formatted as total_hours:minutes where minute is the last 2 digits and hours the first n-2 digits. This is to convert that format into "Day hour_of_day:minutes"'''
        if time == "" or time == 'None' or time == None:
            return "n/a"
        hours = int(time)/60
        minutes = time - hours*60
        if hours/24 <= 0:
            day = "Sat"
        elif hours/24 <= 1:
            day = "Sun"
        elif hours/24 <= 2:
            day = "Mon"
        elif hours/24 <= 3:
            day = "Tue"
        elif hours/24 <= 4:
            day = "Wed"
        elif hours/24 <= 5:
            day = "Thu"
        elif hours/24 <= 6:
            day = "Fri"
        elif hours/24 <= 7:
            day = "Sat (2nd)"
        elif hours/24 <= 8:
            day = "Sun (2nd)"
        timeString = self.addZeros(str(hours%24)) + ":" + self.addZeros(str(minutes)) + " " + day 
        return timeString

    def getKillTimes(self):
        '''Returns a list of times and how many people died at that time'''
        timeDict = {}
        timeList = []
        query = """
SELECT allkills.time
FROM allkills;"""
        self.getData(query)
        result = self.cursor.fetchall()
        if len(result) > 0:
            for row in result:
                if row[0] not in timeDict:
                    timeDict[row[0]] = 1
                else:
                    timeDict[row[0]] += 1
        for time in timeDict:
            timeList.append([time, timeDict[time]])
        timeList.sort()
        for index in range(len(timeList)):
            timeList[index][0] = self.formatTime(timeList[index][0])
        return timeList


    def getData(self, query):
        try:
            self.cursor.execute(query)
        except Exception, e:
            print "Cursor error", e
        
   
    def closeConnection(self):
        self.connection.close()
