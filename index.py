#!/usr/bin/python

'''
    index.py

    Carissa Knipe
    Oct 18, 2013

    Interacts primarily with htmlcreator.py to choose which page to display given which form was submitted.
'''


import cgi
import cgitb
import datasource
import htmlcreator

cgitb.enable()
# Get the user input
form = cgi.FieldStorage()
#animal = form['animal'].value
#badAnimal = form['badanimal'].value
# ***** SANITIZE USER INPUT HERE ****

data = datasource.DataSource()
html = htmlcreator.HTMLCreator()

print "Content-type: text/html\r\n\r\n"

if 'choosePlayer' in html.form:
    searchedPlayer = html.form['choosePlayer'].value
    resultsPage = html.playerPage(searchedPlayer) 
    print resultsPage

elif 'overallView' in html.form:
    overallView = html.form['overallView'].value
    resultsPage = html.overallPage(overallView)
    print resultsPage

elif 'mycroftSubmit' in html.form:
    print html.mycroftPage()


elif 'chooseTermRound' in html.form:
    termRound = html.form['chooseTermRound'].value
    resultsPage = html.roundPage(termRound)
    print resultsPage


elif 'initialPageSubmit' in html.form:
    print html.initialPage()

else:
    print html.initialPage()
