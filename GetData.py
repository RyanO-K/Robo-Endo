import csv
from ipaddress import v4_int_to_packed
import time
import datetime
from xml.etree.ElementPath import xpath_tokenizer
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import pandas as pd
import sys
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates


# file = '3_days_data_Ryan.csv'
# file = '1_month_of_data_Ryan.csv'
# file = '3_months_of_data_Ryan.csv'

# convert date in YYYY-MM-DDTHH:MM:SS to unix timestamp in local time

def convert_unix(s_date):
    year = int(s_date[0:4:1])
    month = int(s_date[5:7:1])
    day = int(s_date[8:10:1])
    t = s_date[11:19:1]

    dt = datetime.datetime(year, month, day)
    u_date = dt.timestamp()
    u_date += int(t[0:2])*3600 + int(t[3:5])*60 + int(t[6:8])

    return u_date


def convert_datetime(line):
    temp_str = ""
    temp_str = temp_str + line[3][0:10] + " " + line[3][11:] + ".0"
    date_time_obj = datetime.datetime.strptime(
        temp_str, '%Y-%m-%d %H:%M:%S.%f')
    return date_time_obj


def peakdet(v, thresh):
    maxthresh = []
    peaks = []

    for i, elem in enumerate(v):
        if elem[1] > thresh:
            maxthresh.append(i)
            print("maxthrest")

    for i in maxthresh:
        try:
            if (v[i - 1][1] < v[i][1]) & (v[i + 1][1] < v[i][1]):
                peaks.append(v[i])
                print("added peak")
        except Exception:
            pass

    return peaks


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

        i = i+1

    return timeSkip


def anom(CGM):
    outlier = []
    i = 0
    while i < len(CGM):
        curr = CGM[i][1]
        if i > 0 and i+1 < len(CGM):
            prev = CGM[i-1][1]
            nextVal = CGM[i+1][1]
            # jump/dip of 30 blood sugar in short period of time
            if abs(prev-curr) > 30:
                outlier.append((CGM[i][0], curr))
                CGM.remove(CGM[i])
                timeskips(CGM, 600)
            # 10 blood sugar jump/dip not within trend
            elif (prev < curr and curr > nextVal) or (prev > curr and curr < nextVal):
                if abs(prev-curr) > 10 and abs(nextVal-curr) > 10:
                    outlier.append((CGM[i][0], curr))
                    CGM.remove(CGM[i])
                    timeskips(CGM, 600)
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
   # plt.show()
    return BG


def plotCGM(file, CGM, carb, frame4=None):

    X = []
    Y = []
    # carb
    XC = []
    YC = []
    for i in CGM:
        X.append(datetime.datetime.fromtimestamp(i[0]))
        Y.append(i[1])
    figure = plt.figure()
    myFmt = mdates.DateFormatter('%H:%M')
    plt.gca().xaxis.set_major_formatter(myFmt)
    CGM_time = FigureCanvasTkAgg(figure, frame4)
    CGM_time.get_tk_widget().pack()
    figure = plt.scatter(X, Y, s=1)
    figure = plt.axhspan(70, 180, color='y', alpha=0.5, lw=0)
    figure = plt.title('CGM over time')

    # plt.show()
    return CGM_time


def plotAnCGM(file, CGM, skipsC, anC, carb, frame2):
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

    for i in skipsC:
        XS.append(datetime.datetime.fromtimestamp(i[0]))
        YS.append(i[1])
    for i in anC:
        XO.append(datetime.datetime.fromtimestamp(i[0]))
        YO.append(i[1])
    for i in carb:
        XC.append(datetime.datetime.fromtimestamp(i[0]))
        YC.append(i[1])
    figure = plt.figure()
    myFmt = mdates.DateFormatter('%H:%M')
    plt.gca().xaxis.set_major_formatter(myFmt)
    CGM_anomalies = FigureCanvasTkAgg(figure, frame2)
    CGM_anomalies.get_tk_widget().pack()
    figure = plt.scatter(X, Y, s=1)
    figure = plt.scatter(XS, YS, color="orange")
    figure = plt.title('CGM over time')
    figure = plt.scatter(XO, YO, color="red", marker='x')
    figure = plt.scatter(XC, YC, marker='P', color="red")

    # plt.show()

    return CGM_anomalies


def plotAnIOB(file, IOB, ID, skipsI, carb, frame1):

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
    for i in skipsI:
        XS.append(datetime.datetime.fromtimestamp(i[0]))
        YS.append(i[1])
    figure = plt.scatter(X, Y, s=1)
    figure = plt.scatter(XS, YS, color="orange")
    figure = plt.title('IOB over time')
    figure = plt.scatter(IDX, IDY, marker='P')
    return IOB_anomalies


def plotIOB(file, IOB, ID, carb, frame3=None):

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
    figure = plt.scatter(IDX, IDY, marker='P')
    #figure = plt.scatter(XC, YC, marker='P', color="red")

   # plt.show()

    return IOB_Time


def get_recommendations(file):
    return ["Sample", "Recommendation"]


def plot(file, frame1=None, frame2=None, frame3=None, frame4=None):
    IOB = []
    CGM = []
    # insulin delivered
    ID = []
    BG = []
    carb = []
    target = []
    # anamoly corrections
    anC = []
    peaks = []
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
                if line[2] != "":
                    BG.append((convert_unix(line[6]), int(line[2])))
                if line[7] != "":
                    ID.append((convert_unix(line[6]), float(line[7])))
                if line[28] != "":
                    carb.append((convert_unix(line[6]), int(line[28])))
                if line[30] != "":
                    target.append((convert_unix(line[6]), int(line[30])))

    skipsC = timeskips(CGM, 600)
    skipsI = timeskips(IOB, 900)
    anC = anom(CGM)
    #peaks = peakdet(IOB, 7)
    i = 0
    while i < len(carb):
        if i+1 < len(carb):
            next = carb[i+1]
            elem = carb[i]
            # within 45 minutes = same meal
            if next[0] - elem[0] < 2450:
                carb.remove(carb[i+1])
                carb.remove(carb[i])
                carb.insert(i, (next[0], next[1]+elem[1]))
            else:  # discard anything less than 50 carbs after combined
                if carb[i][1] < 50:
                    carb.remove(carb[i])
                else:
                    i = i+1
        else:
            if carb[i][1] < 50:
                carb.remove(carb[i])
            break

    return plotIOB(file, IOB, ID, carb, frame3), plotAnCGM(file, CGM, skipsC, anC, carb, frame2), plotCGM(file, CGM, carb, frame4), plotAnIOB(file, IOB, ID, skipsI, carb, frame1)


if __name__ == "__main__":
    plot(sys.argv[1])
