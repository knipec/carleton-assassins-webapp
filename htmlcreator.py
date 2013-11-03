'''
    htmlcreator.py

    Carissa Knipe
    Oct 18, 2013

    Returns HTML for pages (and elements within pages) that index.py requests.
    The different pages are:
    - initial page
    - player page
    - overall page
    - mycroft page
    - round page
'''

import cgi
import datasource
import mycroft

class HTMLCreator:
    def __init__(self):
        '''Has several methods to return HTML code for printing in index.py'''
        self.data = datasource.DataSource()
        self.form = cgi.FieldStorage()


    def formForPlayer(self, defaultPlayer=""):
        '''Returns HTML for the first form (player drop down). If form has just been filled out, defaultPlayer should be the submitted entry.'''
        form = """
     <p></p>
     <form>
     Select a player:
     <select name="choosePlayer">"""
        players = self.data.getListOfPlayers()
        for index in range(len(players)):
            if defaultPlayer == players[index]:
                form += """<option selected="selected" """
            else:
                form += """<option """
            form += """'> """ + players[index] 
        
        if defaultPlayer=="":
            form += """<option selected="selected" disabled="disabled">Select...</option>"""
        form += """<input type="submit" value="Go" name="playerSubmit" /></p>
     </select>
     </form>"""
        return form


    def formForOverall(self, defaultVal=""):
        '''Returns HTML for the second form (overall view drop down). If form has just been filled out, defaultVal should be the submitted entry.'''
        form = """
     <form>
     See overall view of:
     <select name="overallView">"""
        for val in range(1,7):
            if defaultVal == str(val):
                form += """<option selected="selected" """
            else:
                form += """<option """
            form += """value='""" + str(val) + """'>""" + self.overallValToTitle(str(val))

        if defaultVal == "":
            form += """<option selected="selected" disabled="disabled">Select...</option>"""
        form += """<input type="submit" value="Go" name="overallSubmit" /></p>
     </select>
     </form>"""
        return form


    def termRoundToString(self, termRoundTuple):
        return termRoundTuple[0] + " - " + termRoundTuple[1]


    def formForRound(self, defaultRound=""):
        '''Returns HTML for the form to view individual rounds'''
        form = """
     <form>
     Select a round:
     <select name="chooseTermRound">"""
        termsAndRounds = self.data.getTermsAndRounds()
        for index in range(len(termsAndRounds)):
            if defaultRound == self.termRoundToString(termsAndRounds[index]):
                form += """<option selected="selected" """
            else:
                form += """<option """
            form += """'> """ + self.termRoundToString(termsAndRounds[index]) 
        
        if defaultRound=="":
            form += """<option selected="selected" disabled="disabled">Select...</option>"""
        form += """<input type="submit" value="Go" name="roundSubmit" /></p>
     </select>
     </form>"""
        return form


    def formForMycroft(self):
        '''Returns HTML for the third form (Mycroft Order button)'''
        form = """
     <form>
     Click to see the
     <input type="submit" value="Mycroft Order" name="mycroftSubmit" /></button>
     </form>"""
        return form
    

    def formForInitialPage(self):
        '''Returns HTML for button that will take you back to the inital page'''
        form = """
     <form>
     <input type="submit" value="Return to menu" name="initialPageSubmit" /></button>
     </form>"""
        return form


    def formForReadme(self):
        '''Returns HTML for readme link'''
        form = """<p><a href="readme.html">README</a></p>"""
        return form


    def initialPage(self):
        '''Returns HTML for the front page'''
        frontPage = """<!DOCTYPE HTML>
 <html>
 <head>
     <title>Carleton Assassins</title>
 </head>
 <body>
     <h1><center>Carleton Assassins</center></h1>"""
        frontPage += """<center><img src="assassins.gif" alt="Carleton Assassins"></center>"""
        frontPage += self.formForPlayer()
        frontPage += self.formForOverall()
        frontPage += self.formForRound()
        frontPage += self.formForMycroft()
        frontPage += self.formForReadme()
        frontPage += """</body></html>"""
        return frontPage


    def playerTables(self, searchedPlayer):
        '''Returns HTML for tables off all kills and all deaths for a given player'''
        resultsPage = ""
        playerKills = self.data.getPlayerKillInfo(searchedPlayer)
        playerDeaths = self.data.getPlayerDeathInfo(searchedPlayer)
        if playerKills == None or playerDeaths == None:
            resultsPage += "Player does not exist"
        else:
            if searchedPlayer == "n/a":
                resultsPage += """<h3>n/a includes enforcement, incineration, and kills that no player can really take credit for.</h3>"""
            resultsPage += str(len(playerKills)) + " PLAYER KILLS:"
            resultsPage += """<table border="1">\n
    <tr><td><b>%s</b></td> <td><b>%s</b></td> <td><b>%s</b></td> <td><b>%s</b></td> <td><b>%s</b></td></tr>""" % ("Victim", "Manner of kill", "Term", "Round", "Time of kill (minutes)")
            for killInfo in playerKills:
                resultsPage += """<tr><td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td></tr>""" % (killInfo[0], killInfo[1], killInfo[2], killInfo[3], killInfo[4])
            resultsPage += '</table><p></p>'

            resultsPage +=  str(len(playerDeaths)) + " PLAYER DEATHS:"
            resultsPage += """<table border="1">\n 
    <tr><td><b>%s</b></td> <td><b>%s</b></td> <td><b>%s</b></td> <td><b>%s</b></td> <td><b>%s</b></td></tr>""" % ("Assassin", "Manner of death", "Term", "Round", "Time of death (minutes)")
            for deathInfo in playerDeaths:
                resultsPage += """<tr><td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td></tr>""" % (deathInfo[0], deathInfo[1], deathInfo[2], deathInfo[3], deathInfo[4])
            resultsPage += '</table>\n'
        return resultsPage


    def playerStats(self, searchedPlayer):
        '''Returns HTML for a non-tabular display of some player-specific data'''
        resultsPage = """<p>"""
        # Print Kill/Death ratio
        resultsPage += """<br><b>K/D Ratio: </b>"""
        resultsPage += self.data.getPlayerKDRatio(searchedPlayer)
        # Print rounds won
        winners = self.data.getWinners()
        resultsPage += """<br><b>Winner (last standing) of rounds: </b>"""
        hasWon = False
        for winner in winners:
            if searchedPlayer == winner[0]:
                resultsPage += """<br>""" +  winner[2] + " during term " + winner[1]
                hasWon = True
        if not hasWon:
            resultsPage += """None"""
        # Print rounds played
        rounds = self.data.getPlayerRounds(searchedPlayer)
        resultsPage += """<br><b>Rounds played (%d):</b>""" % (len(rounds))
        for round in rounds:
            resultsPage += "<br>""" + round[1] + """ - """ + round[0]
        resultsPage += """</p>"""


        return resultsPage

    def playerPage(self, searchedPlayer):
        '''Returns HTML for a single given player's specific info'''
        resultsPage = """<DOCTYPE HTML>
        <html>
        <head>
            <title>Carleton Assassins: %s</title>
        </head>
        <body>   
            <p><h1><center>Assassin: %s</center></h1></p>""" % (searchedPlayer, searchedPlayer)
        resultsPage += self.formForInitialPage()
        resultsPage += self.playerStats(searchedPlayer)
        resultsPage += self.playerTables(searchedPlayer)        
        resultsPage += self.formForPlayer(searchedPlayer)
        resultsPage += self.formForOverall()
        resultsPage += self.formForRound()
        resultsPage += self.formForMycroft()
        resultsPage += """</body>
        </html>"""
        return resultsPage


    def overallTable(self, overallView):
        '''Returns HTML for a specific view's table'''
        resultsPage = ""
        if overallView == '1':
            allDeaths = self.data.getListOfDeathMethods()
            resultsPage += '<table border="1">\n'
            resultsPage += "<tr><td><b>%s</b></td> <td><b>%s</b></td></tr>" % ("Death", "Instances")
            for death in allDeaths:
                resultsPage += '<tr><td>%s</td> <td>%d</td></tr>' % (death[0], death[1])
            resultsPage += '</table>\n'             

        if overallView == '2':
            playersList = self.data.getListOfPlayers()
            resultsPage += '<table border="1">\n'
            resultsPage += "<tr><td><b>%s</b></td></tr>" % ("Player")
            for player in playersList:
                resultsPage += '<tr><td>%s</td>' % (player)
            resultsPage += '</table>\n'             

        elif overallView == '3':
            rankedPlayersList = self.data.getPlayersAndTotalKills()
            resultsPage += '<table border="1">\n'
            resultsPage += "<tr><td><b>%s</b></td> <td><b>%s</b></td></tr>" % ("Player", "Number of kills")
            for player in rankedPlayersList:
                resultsPage += '<tr><td>%s</td> <td>%s</td>' % (player[0], player[1])
            resultsPage += '</table>\n'             

        elif overallView == '4':
            resultsPage += "<h2>(Out of %d total rounds)</h2>" % (len(self.data.getTermsAndRounds()))
            rankedPlayersList = self.data.getPlayersAndRoundsPlayed()
            resultsPage += '<table border="1">\n'
            resultsPage += "<tr><td><b>%s</b></td> <td><b>%s</b></td></tr>" % ("Player", "Number of rounds")
            for player in rankedPlayersList:
                resultsPage += '<tr><td>%s</td> <td>%s</td>' % (player[0], player[1])
            resultsPage += '</table>\n'

        elif overallView == '5':
            rankedPlayersList = self.data.getPlayersAndKDRatios()
            resultsPage += '<table border="1">\n'
            resultsPage += "<tr><td><b>%s</b></td> <td><b>%s</b></td></tr>" % ("Player", "K/D Ratio")
            for player in rankedPlayersList:
                resultsPage += '<tr><td>%s</td> <td>%s</td>' % (player[0], player[1])
            resultsPage += '</table>\n'

        elif overallView == '6':
            timesList = self.data.getKillTimes()
            resultsPage += '<table border="1">\n'
            resultsPage += "<tr><td><b>%s</b></td> <td><b>%s</b></td></tr>" % ("Time", "Number of deaths")
            for time in timesList:
                resultsPage += '<tr><td>%s</td> <td>%s</td>' % (time[0], str(time[1]))
            resultsPage += '</table>\n'


        return resultsPage


    def overallValToTitle(self, overallView):
        '''Given the value from the overall view form, returns the appropriate title'''
        if overallView == '1':
            title = "Coolest ways to die"
        elif overallView == '2':
            title = "All players (alphabetical)"
        elif overallView == '3':
            title = "All players (# of kills)"
        elif overallView == '4':
            title = "All players (# of rounds)"
        elif overallView == '5':
            title = "All players (K/D ratio)"
        elif overallView == '6':
            title = "Times of death"
        else:
            title = ""
        return title


    def overallPage(self, overallView):
        resultsPage = """<DOCTYPE HTML>
    <html>
    <head>
        <title>Carleton Assassins</title>
    </head>
    <body>
        <h1><center>%s</center></h1>""" % (self.overallValToTitle(overallView))
        resultsPage += self.formForInitialPage()
        resultsPage += self.overallTable(overallView)
        resultsPage += self.formForPlayer()
        resultsPage += self.formForOverall(overallView)
        resultsPage += self.formForRound()
        resultsPage += self.formForMycroft()
        resultsPage += """
        </body>
        </html>"""
        return resultsPage


    def mycroftPage(self):
        resultsPage = """<!DOCTYPE html>
<html  dir="ltr" lang="en" xml:lang="en">
<head>
    <title>Assassins Guild: Mycroft Order</title>
<body>
<h1><center>Mycroft Order of the Carleton Assassins Guild</center></h1>"""
        resultsPage += self.formForInitialPage()
        resultsPage += mycroft.mycroftHTML()
        resultsPage += self.formForPlayer()
        resultsPage += self.formForOverall()
        resultsPage += self.formForRound()
        return resultsPage

        
    def roundWinners(self, term, round):
        '''Returns HTML for winners of a given round and term'''
        winners = self.data.getRoundWinners(term, round)
        resultsPage = """<br><b>Last player(s) standing: </b>"""
        if len(winners) > 0:
            resultsPage += winners[0]
        for winner in winners[1:]:
            resultsPage += ", " + winner
        return resultsPage


    def roundTable(self, term, round):
        '''Returns HTML for table of all kills during a given round and term'''
        roundKills = self.data.getRoundKills(term, round)
        resultsPage = """<p><br>ALL KILLS DURING ROUND:"""
        resultsPage += '<table border="1">\n'
        resultsPage += "<tr><td><b>%s</b></td> <td><b>%s</b></td> <td><b>%s</b></td> <td><b>%s</b></td></tr>" % ("Poor soul", "Assassin", "Cause of death", "Time of death (min)")
        for kill in roundKills:
            resultsPage += '<tr><td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td></tr>' % (kill[0], kill[1], kill[2], kill[3])
        resultsPage += '</table>\n</p'             
        return resultsPage


    def roundPage(self, termRoundString):
        middleIndex = termRoundString.index("-")
        term = termRoundString[:middleIndex-1]
        round = termRoundString[middleIndex+2:]
        resultsPage = """<DOCTYPE HTML>
        <html>
        <head>
            <title>Carleton Assassins: %s %s</title>
        </head>
        <body>   
            <p><h1><center>Round: %s %s</center></h1></p>""" % (term, round, term, round)
        resultsPage += self.formForInitialPage()
        resultsPage += self.roundWinners(term, round)
        resultsPage += self.roundTable(term, round)
        resultsPage += self.formForPlayer()
        resultsPage += self.formForOverall()
        resultsPage += self.formForRound(self.termRoundToString((term, round)))
        resultsPage += self.formForMycroft()
        resultsPage += """
        </body>
        </html>"""
        return resultsPage
