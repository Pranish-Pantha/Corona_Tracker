import git
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib import rcParams

rcParams.update({'figure.autolayout': True})
plt.style.use('fivethirtyeight')
plt.rcParams["figure.figsize"] = [16,9]

#runner path

path = str(os.getcwd()) + "/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/"

class coronaTracker:
    def __init__(self, isGlobal, isLight = True):
        #instance variables
        self.imageID = 0
        self.isLight = isLight
        self.isGlobal = isGlobal
        self.dailyReports = {}

        git.Git(str(os.getcwd()) + "/COVID-19").pull("https://github.com/CSSEGISandData/COVID-19.git")
        for file in os.listdir(path):
            if file[0] != "R":
                if file[:-4] not in list(self.dailyReports.keys()):
                    data = pd.read_csv(path + file)
                    self.dailyReports.update({ file[:-4] : data})

    # work in progress
    def updateDataset(self):
        # get daily COVID data from Johns Hopkins github
        git.Git(str(os.getcwd()) + "/COVID-19").pull("https://github.com/CSSEGISandData/COVID-19.git")
        for file in os.listdir(path):
            if file[0] != "R":
                if file[:-4] not in list(self.dailyReports.keys()):
                    data = pd.read_csv(path + file)
                    self.dailyReports.update({ file[:-4] : data})
        return list(self.dailyReports.keys())[-1]

    def graph(self, metric, region="all", isLogscale = False):
        if self.isGlobal:
            listMetricPerDay = []
            listDate = []
            listNumericalDate = []
            # regions are countries
            currentNumericalDate = 0

            for index, date in enumerate(self.dailyReports):
                if index%2 == 1 or (index == (len(self.dailyReports) - 1)):
                    data = self.dailyReports.get(date)

                    if region == "all":  # Collects global data
                        totalCases = 0
                        for index, row in data.iterrows():
                            totalCases += row[metric]
                        listMetricPerDay.append(totalCases)
                        listDate.append(date)
                        print("list is", listDate)
                    else:
                        new_data = data.loc[data["Province/State"] == region].get(metric)
                        listMetricPerDay.append(new_data)
                        listDate.append(date)

                    listNumericalDate.append(currentNumericalDate)
                    currentNumericalDate += 1
            # graph data
            plt.clf()
            plt.plot(listNumericalDate, listMetricPerDay)
            if isLogscale:
                plt.yscale("log")
            if self.isGlobal:
                placeWord = "Global"
            else:
                placeWord = "United States"


            f = lambda x : "(log-scaled)" if (isLogscale) else ""

            plt.title(placeWord + " COVID-19 " + metric + " in " + region + " region(s)")
            plt.xlabel("Days since " + listDate[1])
            plt.ylabel(str(metric) + f(isLogscale))
            #plt.show()
            plt.savefig('Graphs/' + str(self.imageID) + '.png')

            self.imageID += 1
            return (self.imageID-1, listDate[-1], listMetricPerDay[-1], metric)

        else:
            pass
            # regions are states


object = coronaTracker(True)
print(object.graph("Confirmed"))
print(object.graph("Deaths", isLogscale=True))
