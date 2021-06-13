#!/usr/bin/python3
import matplotlib.pyplot as plt
import csv
import sys
import os
import cgi

def get_cmd():
  args = cgi.FieldStorage()
  cmd = args['cmd'].value
  return cmd

cmd = get_cmd()

#def find_largest(data):
#    largest = max(data.values())
#    for x,y in data.items():
#        if (y == largest):
#            return x

def line(data, title, x, y):
    # Data is a dictionary with the number of new deaths each day (Ex. Worldwide, USwide, Statewide) _/
    plt.plot(list(data.keys()), list(data.values()))
    plt.title(title)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.grid()

def bar(data,title,x,y):
    # Data is a dictionary with top 20 States with the most cases
    states = data.keys()
    states = sorted(states, reverse=True, key=lambda k: data[k])
    states = states[:min(20, len(states))]
    values = [data[k] for k in states]
    #new_data = {}
    #for i in range(0,20):
    #    key = find_largest(data)
    #    value = data.pop(key)
    #    new_data[key] = value
    plt.xlabel(x)
    plt.ylabel(y)
    plt.title(title)
    #plt.bar(new_data.keys(), new_data.values())
    plt.bar(states, values)

def state_bar(data,title,x,y):
    # Data is a dictionary with top 20 States with the most cases
    plt.title(title)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.bar(data.keys(), data.values())

def gender(men, women, label, y):
    # sorted dictionary of all number of cases in US based on age _/
    plt.bar(label, men, color = 'r')
    plt.bar(label, women, color = 'b')
    plt.legend(labels=['Men', 'Women'])
    plt.ylabel(y)
    
def unpack_data(csv_file):
    data = {}
    csv_reader = csv.reader(open(csv_file), delimiter=',')
    line = 0
    for row in csv_reader:
        if (line == 0):
            line += 1
        else:
            data[row[0]] = row[1]
    return data

def unpack_multiple_data(csv_file):
    cases = {}
    deaths = {}
    csv_reader = csv.reader(open(csv_file), delimiter=',')
    line = 0
    casesPos = 1
    deathsPos = 2
    for row in csv_reader:
        if (line == 0):
            if (row[0] == deaths):
                casesPos = 2
                deathsPos = 1
            line += 1
        else:
            cases[row[0]] = float(row[casesPos])
            deaths[row[0]] = float(row[deathsPos])
    return cases, deaths

def unpack_genders(file):
    men = csv.reader(open(file), delimiter=',')
    men_cases = []
    men_death = []
    labels = []
    line = 0
    for mens in men:
        if line == 0:
            line += 1
            continue
        labels.append(mens[0])
        men_death.append(int(mens[1]))
        men_cases.append(int(mens[2]))
    return men_cases, men_death, labels


print("Content-Type: image/png\n", flush=True)

# Both deaths and cases
if cmd in ['California', 'Georgia', 'Illinois', 'Ohio']:
    N = 2
    plt.subplots(N, 1, sharex=False, sharey=False, figsize=(15,13))
    cases, deaths = unpack_multiple_data(f"State_Data/{cmd}.csv")
    plt.subplot(N,1,1)
    state_bar(cases, "Cases by age", "Age", "Cases")
    plt.subplot(N,1,2)
    state_bar(cases, "Deaths by age", "Age", "Deaths")
    plt.savefig(sys.stdout.buffer)
# only deaths
if cmd in ['Florida', 'New_York', 'Pennsylvania']:
    deaths = unpack_data(f"State_Data/{cmd}.csv")
    state_bar(deaths, "Deaths by age", "Age", "Deaths")
    plt.savefig(sys.stdout.buffer)
# only cases
if cmd == 'North_Carolina':
    cases = unpack_data("State_Data/North_Carolina.csv")
    state_bar(cases, "Cases by age", "Age", "Cases")
    plt.savefig(sys.stdout.buffer)
# both death and case percentages
if cmd == 'Texas':
    N = 2
    plt.subplots(N, 1, sharex=False, sharey=False, figsize=(15,13))
    cases, deaths = unpack_multiple_data("State_Data/Texas.csv")
    plt.subplot(N,1,1)
    state_bar(cases, "Percent Cases by age", "Age", "Percent Cases")
    plt.subplot(N,1,2)
    state_bar(cases, "Percent Deaths by age", "Age", "Percent Deaths")
    plt.savefig(sys.stdout.buffer)
# only death percentage
if cmd == 'New_Jersey':
    data = unpack_data("State_Data/New_Jersey.csv")
    state_bar(data, "Death Percentages by Age", "Age", "Percentage")
    plt.savefig(sys.stdout.buffer)
# US only
if cmd == 'US':
    # top 20 states deaths and cases
    N = 9
    plt.subplots(N, 1, sharex=False, sharey=False, figsize=(21,50))

    state_cases, state_deaths = unpack_multiple_data("US_Data/Pop_Data.csv")
    plt.subplot(N,1,1)
    bar(state_cases, "Number of cases per 1,000,000 people", "state", "Cases")
    plt.xticks(rotation=45)

    plt.subplot(N,1,2)
    bar(state_deaths, "Number of deaths per 1,000,000 people", "state", "Deaths")
    plt.xticks(rotation=45)

    # line graph for deaths and cases per first day of month
    date_cases, date_deaths = unpack_multiple_data("US_Data/Dates_Data.csv")

    plt.subplot(N,1,3)
    line(date_cases, "Total cases per first day of month", "day", "cases")

    plt.subplot(N,1,4)
    line(date_deaths, "Total deaths per first day of month", "day", "deaths") 

    # gender and age graph
    women_cases, women_deaths, labels = unpack_genders("US_Data/Women_Data.csv")
    men_cases, men_deaths, labels = unpack_genders("US_Data/Men_Data.csv")

    plt.subplot(N,1,5)
    gender(men_cases, women_cases, labels, "cases")

    plt.subplot(N,1,6)
    gender(men_deaths, women_deaths, labels, "deaths")

    # fatality rate bar graph
    fatality_rate = unpack_data("US_Data/Fatality_Data.csv")
    plt.subplot(N,1,7)
    bar(fatality_rate, "Top 20 highest COVID-19 Fatality Rates", "state", "Fatality Rate")    
    plt.xticks(rotation=45)
    
    # line graph for deaths and cases per day
    date_cases, date_deaths = unpack_multiple_data("US_Data/unused_dates_data.csv")

    plt.subplot(N,1,8)
    line(date_cases, "Total cases per day", "day", "cases")

    plt.subplot(N,1,9)
    line(date_deaths, "Total deaths per day", "day", "deaths") 

    plt.savefig(sys.stdout.buffer)

