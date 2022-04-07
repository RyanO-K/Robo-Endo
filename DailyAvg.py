import csv
import datetime
from tracemalloc import start
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas


file = '3_days_data_Ryan.csv'
#file = '1_month_of_data_Ryan.csv'
# file = '3_months_of_data_Ryan.csv'


def convert_unix(s_date):
    year = int(s_date[0:4:1])
    month = int(s_date[5:7:1])
    day = int(s_date[8:10:1])
    t = s_date[11:19:1]

    dt = datetime.datetime(year, month, day)
    u_date = dt.timestamp()
    u_date += int(t[0:2])*3600 + int(t[3:5])*60 + int(t[6:8])

    return u_date


CGM = list()
AVG = [0] * 288

with open(file, 'r') as data:
    csv_reader = csv.reader(data)
    for line in csv_reader:
        if len(line) > 4:
            if line[2] == "EGV":
                temp_str = ""
                temp_str = temp_str + line[3][0:10] + " " + line[3][11:] + ".0"
                date_time_obj = datetime.datetime.strptime(
                    temp_str, '%Y-%m-%d %H:%M:%S.%f')
                CGM.append((date_time_obj, int(line[4])))


# set the dates here, which are inclusive
startdate = datetime.datetime(2022, 1, 11)
enddate = datetime.datetime(2022, 1, 13)
range = enddate-startdate
range = range.days + 1

timeplot = pandas.date_range("00:00", "23:59", freq="5min")


# find values with date within range, select average
for i in CGM:
    if i[0] > startdate and i[0] < enddate:
        hour = i[0].hour
        minute = i[0].minute
        minute = minute - minute % 5
        time = datetime.time(i[0].hour, minute)
        index = int(hour*12+minute/5)
        AVG[index] = AVG[index]+i[1]
for i in AVG:
    i = i/range

plt.scatter(timeplot, AVG)


plt.plot(timeplot, AVG, label="CGM")

myFmt = mdates.DateFormatter('%H:%M')
plt.gca().xaxis.set_major_formatter(myFmt)

plt.title("Daily CGM Averages")
plt.xlabel("Time in day")

plt.legend()
plt.show()
