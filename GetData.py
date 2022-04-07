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
import numpy as np
import datetime


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
    minthresh = []
    IOB_anomalies = []
    valleys = []

    for i, elem in enumerate(v):
        if elem[1] > thresh:
            maxthresh.append(i)
            print("maxthrest")

    for i in maxthresh:
        try:
            if (v[i - 1][1] < v[i][1]) & (v[i + 1][1] < v[i][1]):
                IOB_anomalies.append(v[i])
                print("added peak")
        except Exception:
            pass

    return IOB_anomalies


def timeskips(data, time):
    timeSkip = []
    i = 0
    while i < len(data):
        if i > 0 and i + 1 < len(data):
            nextTime = data[i + 1][0]
            elem = data[i]
            # 10 minutes without input = timeskip
            if nextTime - elem[0] > time:
                timeSkip.append(
                    (float((nextTime + elem[0]) / 2), int((data[i + 1][1] + elem[1]) / 2)))
                data.insert(
                    i + 1, (float((nextTime + elem[0]) / 2), int((data[i + 1][1] + elem[1]) / 2)))
                i = i - 1

        i = i + 1

    return timeSkip


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


def plotCGM(file, CGM, skips, anC, carb, frame4=None):
    X = []
    Y = []
    XS = []
    YS = []
    XA = []
    YA = []
    XC = []
    YC = []
    for i, elem in enumerate(CGM):
        if i > 0 and i + 1 < len(CGM):
            if elem[1] - CGM[i - 1][1] < 0 and elem[1] - CGM[i + 1][1] < 0 and CGM[2] == -1:
                elem[1] = min(abs(elem[1] - CGM[i - 1][1]),
                              abs(CGM[i + 1][1] - elem[1]))
            X.append(datetime.datetime.fromtimestamp(elem[0]))
            Y.append(elem[1])

    for i in skips:
        XS.append(datetime.datetime.fromtimestamp(i[0]))
        YS.append(i[1])
    for i in anC:
        XA.append(datetime.datetime.fromtimestamp(i[0]))
        print(datetime.datetime.fromtimestamp(i[0]))
        YA.append(i[1])
        print(i[1])
    figure = plt.figure()
    myFmt = mdates.DateFormatter('%H:%M')
    plt.gca().xaxis.set_major_formatter(myFmt)
    CGM_time = FigureCanvasTkAgg(figure, frame4)
    CGM_time.get_tk_widget().pack()
    figure = plt.scatter(X, Y, s=1)
    figure = plt.scatter(XS, YS, color="orange")
    figure = plt.scatter(XA, YA, color="red")
    figure = plt.title('CGM over time')

    # plt.show()
    return CGM_time


def plotAnCGM(file, CGM, skips, anC, IOB_anomalies, carb, frame2):
    outlier = []
    X = []
    Y = []
    XS = []
    YS = []
    XO = []
    YO = []
    XP = []
    YP = []
    XC = []
    YC = []
    i = 0
    while i < len(CGM):
        curr = CGM[i][1]
        X.append(datetime.datetime.fromtimestamp(CGM[i][0]))
        Y.append(curr)
        if i > 0 and i + 2 < len(CGM):
            prev = CGM[i - 1][1]
            nextVal = CGM[i + 1][1]
            nextVal2 = CGM[i + 1][1]
            if abs(curr - nextVal) > 30:
                outlier.append((CGM[i + 1][0], nextVal))
                CGM.remove(CGM[i])
                anC = anC + timeskips(CGM, 600)

            elif prev < curr and curr > nextVal:
                if abs(prev - curr) > 10 and abs(nextVal - curr) > 10:
                    outlier.append((CGM[i][0], curr))
                    CGM.remove(CGM[i])
                    anC = anC + timeskips(CGM, 600)
        i = i + 1

    for i in skips:
        XS.append(datetime.datetime.fromtimestamp(i[0]))
        YS.append(i[1])
    for i in outlier:
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
    # for i in IOB_anomalies:
    # plt.axvline(x=datetime.datetime.fromtimestamp(i[0]), ymin=0, ymax=0.20, color='b',
    #            label='IOB IOB_anomalies')
    figure = plt.title('CGM over time')
    figure = plt.scatter(XO, YO, color="red", marker='x')
    figure = plt.scatter(XC, YC, marker='P', color="red")

    # plt.show()

    return CGM_anomalies


def plotAnIOB(file, IOB, ID, skips, carb, frame1):
    figure = plt.figure()
    IOB_anomalies = FigureCanvasTkAgg(figure, frame1)
    IOB_anomalies.get_tk_widget().pack(expand=True)
    X = []
    Y = []
    XS = []
    YS = []
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
    figure = plt.scatter(X, Y, s=1)
    figure = plt.scatter(XS, YS, color="orange")
    figure = plt.title('IOB anomalies over time')
    figure = plt.scatter(IDX, IDY, marker='P')
    return IOB_anomalies


def plotMealTime(file, CGM, frame, time_frame):
    """
    :param file:
    :param CGM:
    :param frame:
    :param time_frame: 0 for all, 1 for night, 2 morning, 3 afternoon, 4 evening
    :return:
    """
    meal_size = list()
    parsed_meal_size = list()
    temp_count = 0

    with open(file, 'r') as data:
        csv_reader = csv.reader(data)

        for index, item in enumerate(csv_reader):
            if len(item) >= 41 and item[24] != "BolusType":
                if item[24] != "Carb":
                    temp_str = ""
                    temp_str = temp_str + item[22][0:10] + " " + item[22][11:] + ".0"
                    date_time_obj = datetime.datetime.strptime(temp_str, '%Y-%m-%d %H:%M:%S.%f')
                    meal_size.append((temp_count, convert_unix(item[22])))
                    temp_count = 0
                if item[28] != '0' and item[24] == "Carb":
                    temp_count += float(item[28])

    for i in range(0, len(meal_size)):
        if meal_size[i][0] == 0:
            continue
        if meal_size[i][0] != 0:
            parsed_meal_size.append(meal_size[i])

    X = []
    Y = []
    NewCGM = list()
    dataFreq = list()
    for i in range(0, 48):
        dataFreq.append(0)
    index = 0
    for i in range(0, 14400, 300):
        j = i, 0
        NewCGM.append(list(j))
    for meal in range(0, len(parsed_meal_size)):
        for elem in CGM:
            if elem[0] > parsed_meal_size[meal][1] and elem[0] < (parsed_meal_size[meal][1] + 14400):
                i = ((elem[0] - parsed_meal_size[meal][1]) - ((elem[0] - parsed_meal_size[meal][1]) % 300)), elem[1]
                for e in NewCGM:
                    if e[0] == i[0]:
                        e[1] += i[1]
                        dataFreq[int(i[0] / 300)] += 1

    for i in range(0, len(NewCGM)):
        NewCGM[i][1] = NewCGM[i][1] / dataFreq[i]

    for i in range(1, len(NewCGM)):
        NewCGM[i][1] = (NewCGM[i][1] - NewCGM[0][1])
    NewCGM[0][1] = 0

    for i, elem in enumerate(NewCGM):
        if i > 0 and i + 1 < len(NewCGM):
            if elem[1] - NewCGM[i - 1][1] < 0 and elem[1] - NewCGM[i + 1][1] < 0 and NewCGM[2] == -1:
                elem[1] = min(abs(elem[1] - NewCGM[i - 1][1]),
                              abs(NewCGM[i + 1][1] - elem[1]))
            X.append(datetime.datetime.fromtimestamp(elem[0]))
            Y.append(elem[1])

    figure = plt.figure()
    myFmt = mdates.DateFormatter('%H:%M')
    plt.gca().xaxis.set_major_formatter(myFmt)
    CGM_time = FigureCanvasTkAgg(figure, frame)
    CGM_time.get_tk_widget().pack()
    figure = plt.scatter(X, Y, s=1)
    figure = plt.title('CGM Change 4 hours post meal')

    #plt.show()

    return CGM_time



def plotIOB(file, IOB, ID, skips, carb, frame3=None):
    # lists for data points for plot
    X = []
    Y = []
    XS = []
    YS = []
    XC = []
    YC = []

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
    # figure = plt.scatter(XC, YC, marker='P', color="red")
    figure = plt.scatter(XS, YS, color="orange")

    # plt.show()

    return IOB_Time


def get_recommendations(IOB, ID, skipsI, carb, CGM, skipsC, anC, IOB_anomalies):
    recommendations = ["Sample Recommendation", "Generic Recommendation!"]

    num_highs_from_carbs = 0
    num_lows_from_carbs = 0
    probable_machine_failure = 0

    i = 0
    while i < len(IOB_anomalies):
        relevant_carbs = [[IOB_anomalies[i][0] - x[0], x[1], x[2]] for x in carb if
                          0 <= IOB_anomalies[i][0] - x[0] < 14400]  # grab all carbs within four hours of high IOB
        recent_carbs = [[IOB_anomalies[i][0] - x[0], x[1], x[2]] for x in carb if
                        0 <= IOB_anomalies[i][0] - x[0] < 7200]  # grab all carbs within two hours of high IOB

        recent_total = np.sum([x[1] for x in recent_carbs])

        if len(relevant_carbs) == 0:
            probable_machine_failure += 1
        curr_index = i + 1
        try:
            while IOB_anomalies[i][0] - IOB_anomalies[curr_index][0] < 14400:
                curr_index += 1
        except IndexError as e:
            # only hits if the remainder of the reading are too close
            break
        i = curr_index

    i = 0
    CGM_highs = [x for x in CGM if x[1] > 250]
    CGM_lows = [x for x in CGM if x[1] < 60]


    start_night = datetime.datetime.strptime("0:00:00", "%H:%M:%S").time()
    start_morning = datetime.datetime.strptime("6:00:00", "%H:%M:%S").time()
    start_afternoon = datetime.datetime.strptime("12:00:00", "%H:%M:%S").time()
    start_evening = datetime.datetime.strptime("18:00:00", "%H:%M:%S").time()

    night_highs = 0
    morning_highs = 0
    afternoon_highs = 0
    evening_highs = 0

    night_lows = 0
    morning_lows = 0
    afternoon_lows = 0
    evening_lows = 0

    while i < len(CGM_highs):
        relevant_carbs = [[CGM_highs[i][0] - x[0], x[1], x[2]] for x in carb if 0 <= CGM_highs[i][0] - x[0] < 14400]
        # grab all carbs within four hours of high BS
        relevant_total = np.sum([x[1] for x in relevant_carbs])

        if relevant_total > 100:
            num_highs_from_carbs += 1

        if relevant_total < 20:  # if there are less than 20 relevant carbs

            converted_time = datetime.datetime.fromtimestamp(CGM_highs[i][0]).time()

            if converted_time > start_evening:
                evening_highs += 1
                try:
                    while datetime.datetime.fromtimestamp(
                            CGM_highs[i + 1][0]).time() > start_evening:  # toss out any CGM readings until the next segment
                        i += 1
                except IndexError as e:
                    # only hits if the remainder of hte readings are high
                    break
            elif converted_time > start_afternoon:
                afternoon_highs += 1
                try:
                    while start_evening > datetime.datetime.fromtimestamp(
                            CGM_highs[i + 1][0]).time() > start_afternoon:  # toss out any CGM readings until the next segment
                        i += 1
                except IndexError as e:
                    # only hits if the remainder of the readings are high
                    break
            elif converted_time > start_morning:
                morning_highs += 1
                try:
                    while start_afternoon > datetime.datetime.fromtimestamp(
                            CGM_highs[i + 1][0]).time() > start_morning:  # toss out any CGM readings until the next segment
                        i += 1
                except IndexError as e:
                    # only hits if the remainder of hte readings are high
                    break
            elif converted_time > start_night:
                night_highs += 1
                try:
                    while datetime.datetime.fromtimestamp(
                            CGM_highs[i + 1][0]).time() < start_morning:  # toss out any CGM readings until the next segment
                        i += 1
                except IndexError as e:
                    # only hits if the remainder of hte readings are high
                    break

        i += 1

    i=0
    while i < len(CGM_lows):
        relevant_carbs = [[CGM_lows[i][0] - x[0], x[1], x[2]] for x in carb if 0 <= CGM_lows[i][0] - x[0] < 14400]
        # grab all carbs within four hours of high BS
        relevant_total = np.sum([x[1] for x in relevant_carbs])

        if relevant_total > 100:
            num_lows_from_carbs += 1

        if relevant_total < 20:  # if there are less than 20 relevant carbs

            converted_time = datetime.datetime.fromtimestamp(CGM_lows[i][0]).time()

            if converted_time > start_evening:
                evening_lows += 1
                try:
                    while datetime.datetime.fromtimestamp(
                            CGM_lows[i + 1][0]).time() > start_evening:  # toss out any CGM readings until the next segment
                        i += 1
                except IndexError as e:
                    # only hits if the remainder of hte readings are high
                    break
            elif converted_time > start_afternoon:
                afternoon_lows += 1
                try:
                    while start_evening > datetime.datetime.fromtimestamp(
                            CGM_lows[i + 1][0]).time() > start_afternoon:  # toss out any CGM readings until the next segment
                        i += 1
                except IndexError as e:
                    # only hits if the remainder of hte readings are high
                    break
            elif converted_time > start_morning:
                morning_lows += 1
                try:
                    while start_afternoon > datetime.datetime.fromtimestamp(
                            CGM_lows[i + 1][0]).time() > start_morning:  # toss out any CGM readings until the next segment
                        i += 1
                except IndexError as e:
                    # only hits if the remainder of hte readings are high
                    break
            elif converted_time > start_night:
                night_lows += 1
                try:
                    while datetime.datetime.fromtimestamp(
                            CGM_lows[i + 1][0]).time() < start_morning:  # toss out any CGM readings until the next segment
                        i += 1
                except IndexError as e:
                    # only hits if the remainder of hte readings are high
                    break

        i += 1

    if night_highs > 0:
        recommendations += [f"You had {night_highs} unexplained highs at night."]
    if morning_highs > 0:
        recommendations += [f"You had {morning_highs} unexplained morning highs."]
    if afternoon_highs > 0:
        recommendations += [f"You had {afternoon_highs} unexplained highs in the afternoon."]
    if evening_highs > 0:
        recommendations += [f"You had {evening_highs} unexplained highs in the evening."]
    if night_lows > 0:
        recommendations += [f"You had {night_lows} unexplained lows at night."]
    if morning_lows > 0:
        recommendations += [f"You had {morning_lows} unexplained morning lows."]
    if afternoon_lows > 0:
        recommendations += [f"You had {afternoon_lows} unexplained lows in the afternoon."]
    if evening_lows > 0:
        recommendations += [f"You had {evening_lows} unexplained lows in the evening."]

    if probable_machine_failure > 0:
        recommendations += [f"You had {probable_machine_failure} machine failures."]
    if num_highs_from_carbs > 0:
        recommendations += [f"You went high from eating a large meal {num_highs_from_carbs} times."]
    if num_lows_from_carbs > 0:
        recommendations += [f"You went low from eating a large meal {num_lows_from_carbs} times."]
    # TODO: Get average number of failures per day

    return recommendations


def plot(file, frame1=None, frame2=None, frame3=None, frame4=None):
    IOB = []
    CGM = []
    # insulin delivered
    ID = []
    BG = []
    carb = []
    # anamoly corrections
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
                    carb.append((convert_unix(line[6]), int(line[28]), override))
                if line[2] == "":
                    continue
                if line[6] != "":
                    BG.append((convert_unix(line[6]), int(line[2])))
                if line[7] != "" and line[6] != "":
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
