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

path = str(os.getcwd()) + "/coronadata/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/"


class coronaTracker:
    def __init__(self, isGlobal, isLight = True):
        #instance variables
        self.imageID = 0
        self.isLight = isLight
        self.isGlobal = isGlobal
        self.dailyReports = {}

        

        print(isLight)
        for file in os.listdir(path):
            if file[0] != "R":
                data = pd.read_csv(path + file)
                self.dailyReports.update({ file[:-4] : data})

    # work in progress
    def updateDataset(self):
        # get daily COVID data from Johns Hopkins github
        git.Git(path).clone("https://github.com/CSSEGISandData/COVID-19.git")


    def graph(self, metric, region="all", isLogscale = False):
        if self.isGlobal:
            listMetricPerDay = []
            listDate = []
            listNumericalDate = []
            # regions are countries
            currentNumericalDate = 0


            for index, date in enumerate(self.dailyReports):
                if index%3 == 1 or (index == (len(self.dailyReports) - 1)):
                    data = self.dailyReports.get(date)


                    if region == "all":
                        totalCases = 0
                        for index, row in data.iterrows():
                            totalCases += row[metric]
                        listMetricPerDay.append(totalCases)
                        listDate.append(date)

                    else:
                        new_data = data.loc[data["Province/State"] == region].get(metric)
                        listMetricPerDay.append(new_data)
                        listDate.append(date)

                    listNumericalDate.append(currentNumericalDate*3)
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

