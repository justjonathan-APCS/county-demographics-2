from flask import Flask, request, Markup, render_template, flash, Markup
import os
import json

app = Flask(__name__)

@app.route("/")
def render_main():
    with open('county_demographics.json') as demographics_data:
        demographicData = json.load(demographics_data)
    return render_template('home.html', states = get_state_options(demographicData), fact = '')

@app.route("/reply")
def render_reply():
    with open('county_demographics.json') as demographics_data:
        demographicData = json.load(demographics_data)
    return render_template('home.html', states = get_state_options(demographicData), county = get_county_options(demographicData, request.args['states']), fact = '')

@app.route("/secondReply")
def render_second_reply():
    with open('county_demographics.json') as demographics_data:
        demographicData = json.load(demographics_data)
    return render_template('home.html', states = get_state_options(demographicData), fact = get_fact(demographicData, request.args['county']))

def get_state_options(counties):
    listOfStates = []
    option = ''
    for data in counties:
        if (data['State'] not in listOfStates):
            listOfStates.append(data['State'])
    for state in listOfStates:
        option = option + Markup("<option value=\"" + state + "\">" + state + "</option>")      """useing th Markup("<option value=\"" + s + "\">" + s + "</option>")"""
    return option

def get_county_options(counties, states):
    listOfCounties = []
    option = ''
    for data in counties:
        if (data['County'] not in listOfCounties) and data['State'] == states:
            listOfCounties.append(data['County'])
    for county in listOfCounties:
            option = option + Markup("<option value=\"" + county + "\">" + county + "</option>")
    return option

def get_fact(counties, county):
     counter = 0
     for data in counties:
        if data['County'] == county:
            counter = data['Age']['Percent Under 18 Years']
     fact = 'Fun Fact: ' + str(county) + ' has ' + str(counter) + ' percent of their population above the age of 18.'
     return fact

if __name__=="__main__":
    app.run(debug=False)
