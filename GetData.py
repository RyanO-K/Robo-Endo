import csv
from ipaddress import v4_int_to_packed
import time
import datetime
from xml.etree.ElementPath import xpath_tokenizer
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import pandas as pd
import sys
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
import numpy as np
from mealtime import *


# file = '3_days_data_Ryan.csv'
# file = '1_month_of_data_Ryan.csv'
# file = '3_months_of_data_Ryan.csv'
# convert date in YYYY-MM-DDTHH:MM:SS to unix timestamp in local time

def convert_unix(s_date):
    try:
        year = int(s_date[0:4:1])
        month = int(s_date[5:7:1])
        day = int(s_date[8:10:1])
        t = s_date[11:19:1]
    except ValueError:
        return 0

    dt = datetime.datetime(year, month, day)
    u_date = dt.timestamp()
    u_date += int(t[0:2]) * 3600 + int(t[3:5]) * 60 + int(t[6:8])

    return u_date


def peakdet(v, thresh):
    maxthresh = []
    IOB_anomalies = []

    for i, elem in enumerate(v):
        if elem[1] > thresh:
            maxthresh.append(i)

    for i in maxthresh:
        try:
            if (v[i - 1][1] < v[i][1]) & (v[i + 1][1] < v[i][1]):
                IOB_anomalies.append(v[i])
        except Exception:
            pass

    return IOB_anomalies


def anomI(IOBA, carb):
    anI = []
    i = 0
    while i < len(IOBA):
        relevant_carbs = [[IOBA[i][0] - x[0], x[1], x[2]] for x in carb if
                          0 <= IOBA[i][0] - x[0] < 14400]  # grab all carbs within four hours of high
        recent_carbs = [[IOBA[i][0] - x[0], x[1], x[2]] for x in carb if
                        0 <= IOBA[i][0] - x[0] < 7200]  # grab all carbs within two hours of high
        relevant_total = np.sum([x[1] for x in relevant_carbs])
        recent_total = np.sum([x[1] for x in recent_carbs])

        if len(recent_carbs) == 0 and relevant_total <= 20:
            anI.append((IOBA[i][0] - 14400, IOBA[i][1], 0))
            curr_index = i
            # toss out any IOB_anomalies occuring the the next 2 hours
            while IOBA[curr_index + 1][0] - IOBA[i][0] < 7200:
                curr_index += 1
            i = curr_index

        elif len(relevant_carbs) == 0:
            anI.append((IOBA[i][0], IOBA[i][1], 1))
        i += 1
    print(anI)
    return anI


def timeskips(data, time):
    timeSkip = []
    i = 0
    while i < len(data):
        if i+1 < len(data):
            nextTime = data[i+1][0]
            elem = data[i]
            # time minutes without input = timeskip
            if nextTime - elem[0] > time:
                avg = float((nextTime + elem[0])/2)

                timeSkip.append(
                    (avg, int((data[i+1][1] + elem[1])/2)))
                data.insert(
                    i+1, (avg, int((data[i+1][1] + elem[1])/2), datetime.datetime.fromtimestamp(avg)))
                i = i-1

        i = i + 1

    return timeSkip


def anom(CGM):
    outlier = []
    i = 0
    while i < len(CGM):
        curr = CGM[i][1]
        if i > 0 and i+1 < len(CGM):
            prev = CGM[i-1][1]
            nextVal = CGM[i+1][1]
            # jump/dip that does not follow trend within 5 minutes
            if (prev < curr and curr > nextVal) or (prev > curr and curr < nextVal):
                if abs(prev-curr) > 10 and abs(nextVal-curr) > 10:
                    outlier.append((CGM[i][0], curr))
                    CGM.remove(CGM[i])
                    continue
            # jump/dip of 30 blood sugar in short period of time
            elif abs(prev-curr) > 30:
                outlier.append((CGM[i][0], curr))
                CGM.remove(CGM[i])
                timeskips(CGM, 600)
                continue

        i = i + 1
    return outlier


def plotBG(file, BG, Completion_time, frame5=None):
    figure = plt.figure()
    figure = plt.scatter(Completion_time[1:], BG[1:])
    figure = plt.plot(Completion_time[1:], BG[1:])

    myFmt = mdates.DateFormatter('%H:%M')
    plt.gca().xaxis.set_major_formatter(myFmt)

    plt.title("BG level over Time in day")
    plt.xlabel("Time in day")
    plt.ylabel("Blood Glucose level (BG)")
    figure = plt.title('BG over time')
    BG_time = FigureCanvasTkAgg(figure, frame5)
    BG_time.get_tk_widget().pack()
    return BG


def plotCGM(file, CGM, skips, anC, carb, meal, frame4=None):

    X = []
    Y = []
    # carb
    XC = []
    YC = []
    for i in CGM:
        X.append(datetime.datetime.fromtimestamp(i[0]))
        Y.append(i[1])
    for i in meal:
        XC.append(i[1])
        YC.append(i[0])
    figure = plt.figure()
    myFmt = mdates.DateFormatter('%H:%M')
    plt.gca().xaxis.set_major_formatter(myFmt)

    CGM_time = FigureCanvasTkAgg(figure, frame4)
    CGM_time.get_tk_widget().pack()
    figure = plt.scatter(X, Y, s=1)
    figure = plt.plot(X, Y)
    figure = plt.axhspan(70, 180, color='y', alpha=0.5, lw=0)
    figure = plt.title('CGM over time')
    figure = plt.scatter(XC, YC, marker='P', color="blue")

    return CGM_time


def plotAnCGM(file, CGM, skips, anC, IOB_anomalies, carb, meal, frame2):
    X = []
    Y = []
    # skips
    XS = []
    YS = []
    # outlier
    XO = []
    YO = []
    # carbs
    XC = []
    YC = []

    for i in CGM:
        X.append(datetime.datetime.fromtimestamp(i[0]))
        Y.append(i[1])

    for i in skips:
        XS.append(datetime.datetime.fromtimestamp(i[0]))
        YS.append(i[1])
    for i in anC:
        XO.append(datetime.datetime.fromtimestamp(i[0]))
        YO.append(i[1])
    for i in meal:
        XC.append(i[1])
        YC.append(i[0])
    figure = plt.figure()
    myFmt = mdates.DateFormatter('%H:%M')
    plt.gca().xaxis.set_major_formatter(myFmt)
    CGM_anomalies = FigureCanvasTkAgg(figure, frame2)
    CGM_anomalies.get_tk_widget().pack()
    figure = plt.scatter(X, Y, s=1)
    figure = plt.scatter(XS, YS, color="orange")
    figure = plt.title('CGM over time')
    figure = plt.scatter(XO, YO, color="red", marker='x')
    figure = plt.scatter(XC, YC, marker='P', color="blue")

    return CGM_anomalies


def plotAnIOB(file, IOB, ID, skips, anI, frame1):

    figure = plt.figure()
    IOB_anomalies = FigureCanvasTkAgg(figure, frame1)
    IOB_anomalies.get_tk_widget().pack(expand=True)
    X = []
    Y = []
    # skips
    XS = []
    YS = []
    # injections
    XC = []
    YC = []

    for i in IOB:
        X.append(datetime.datetime.fromtimestamp(i[0]))
        Y.append(i[1])

    IDX = []
    IDY = []
    for i, elem in enumerate(ID):
        IDX.append(datetime.datetime.fromtimestamp(elem[0]))
        IDY.append(elem[1])
    for i in skips:
        XS.append(datetime.datetime.fromtimestamp(i[0]))
        YS.append(i[1])
    for i in anI:
        if i[2] == 1:  # machine failure
            figure = plt.scatter(datetime.datetime.fromtimestamp(
                i[0]), i[1], color="red", marker='x')
        if i[2] == 0:  # insufficient basil
            plt.axvspan(datetime.datetime.fromtimestamp(
                i[0]), datetime.datetime.fromtimestamp(i[0]+14000), color='y', alpha=0.5, lw=0)

    figure = plt.scatter(X, Y, s=1)
    figure = plt.plot(X, Y)
    figure = plt.scatter(XS, YS, color="orange")
    figure = plt.title('IOB over time')
    figure = plt.scatter(IDX, IDY, color='yellow')
    figure = plt.plot(IDX, IDY, color='yellow')
    return IOB_anomalies


def plotIOB(file, IOB, ID, skips, carb, frame3=None):
    X = []
    Y = []
    # carb
    XC = []
    YC = []
    # injection

    for i in IOB:
        X.append(datetime.datetime.fromtimestamp(i[0]))
        Y.append(i[1])

    figure = plt.figure()
    myFmt = mdates.DateFormatter('%H:%M')
    plt.gca().xaxis.set_major_formatter(myFmt)
    IOB_Time = FigureCanvasTkAgg(figure, frame3)
    IOB_Time.get_tk_widget().pack()

    figure = plt.scatter(X, Y, s=1)
    figure = plt.title('IOB over time')
    IDX = []
    IDY = []
    for i in carb:
        XC.append(datetime.datetime.fromtimestamp(i[0]))
        YC.append(10)
    for i, elem in enumerate(ID):
        IDX.append(datetime.datetime.fromtimestamp(elem[0]))
        IDY.append(elem[1])
    figure = plt.scatter(IDX, IDY, color='yellow')
    figure = plt.plot(IDX, IDY, color='yellow')
    #figure = plt.scatter(XC, YC, marker='P', color="red")

    return IOB_Time


def get_recommendations(IOB, ID, skipsI, carb, CGM, skipsC, anC, IOB_anomalies):
    recommendations = ["Sample Recommendation", "Generic Recommendation!"]

    num_highs_from_carbs = 0
    probable_machine_failure = 0
    insufficient_basal = []
    i = 0
    while i < len(IOB_anomalies):
        relevant_carbs = [[IOB_anomalies[i][0] - x[0], x[1], x[2]] for x in carb if
                          0 <= IOB_anomalies[i][0] - x[0] < 14400]  # grab all carbs within four hours of high
        recent_carbs = [[IOB_anomalies[i][0] - x[0], x[1], x[2]] for x in carb if
                        0 <= IOB_anomalies[i][0] - x[0] < 7200]  # grab all carbs within two hours of high
        relevant_total = np.sum([x[1] for x in relevant_carbs])
        recent_total = np.sum([x[1] for x in recent_carbs])

        if recent_total > 100:
            num_highs_from_carbs += 1

        if len(recent_carbs) == 0 and relevant_total <= 20:
            # TODO: convert to time of day
            insufficient_basal += [IOB_anomalies[i][0] - 14400]

            curr_index = i
            # toss out any IOB_anomalies occuring the the next 2 hours
            while IOB_anomalies[curr_index + 1][0] - IOB_anomalies[i][0] < 7200:
                curr_index += 1
            i = curr_index

        elif len(relevant_carbs) == 0:
            probable_machine_failure += 1
        i += 1

    # TODO: Move logic regarding basal to a loop iterating over CGM anomalies rather than IOB

    for time in insufficient_basal:
        # TODO: convert to time of day
        recommendations += [f"You went high at {time} despite not many carbs."]
    if probable_machine_failure > 0:
        recommendations += [
            f"You had {probable_machine_failure} machine failures."]
    if num_highs_from_carbs > 0:
        recommendations += [
            f"You went high from eating a large meal {num_highs_from_carbs} times."]

    # TODO: Get average number of failures per day

    return recommendations


def plot(file, frame1=None, frame2=None, frame3=None, frame4=None):
    IOB = []
    CGM = []
    # insulin delivered
    ID = []
    BG = []
    carb = []
    meal = []
    # machine failure: rapid jump/falls in Glucose
    anC = []

    with open(file, 'r') as data:
        csv_reader = csv.reader(data)
        for line in csv_reader:
            if len(line) > 3:
                if line[0] == "IOB":
                    convert_unix(line[2])
                    IOB.append((convert_unix(line[2]), float(line[3])))
            if len(line) > 4:
                if line[2] == "EGV":
                    CGM.append((convert_unix(line[3]), int(line[4])))
            if len(line) >= 41 and line[2] != "BG":
                if line[1] == "Automatic Bolus/Correction" or 'Extended' in line[1]:
                    continue
                if line[28] != "0":
                    # time, carb, override
                    override = False
                    if line[29] == '1':
                        override = True
                    carb.append(
                        (convert_unix(line[6]), int(line[28]), override))
                if line[2] == "":
                    continue
                if line[6] != "":
                    BG.append((convert_unix(line[6]), int(line[2])))
                if line[7] != "":
                    ID.append((convert_unix(line[6]), float(line[7])))

    skipsC = timeskips(CGM, 600)
    skipsI = timeskips(IOB, 900)
    IOB_anomalies = peakdet(IOB, 7)
    for i in IOB_anomalies:
        print(i[0])
        print(i[1])
    return IOB, ID, skipsI, carb, CGM, skipsC, anC, IOB_anomalies
    # return plotIOB(file, IOB, ID, skipsI, carb, frame3), plotAnCGM(file, CGM, skipsC, anC, IOB_anomalies, carb, frame2), plotCGM(file, CGM, skipsC, anC, carb, frame4), plotAnIOB(file, IOB, ID, skipsI, carb, frame1)


if __name__ == "__main__":
    plot(sys.argv[1])
