import csv
import datetime
from tracemalloc import start
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas
from GetData import *


file = '3_days_data_Ryan.csv'
#file = '1_month_of_data_Ryan.csv'
# file = '3_months_of_data_Ryan.csv'


CGM = list()
AVG = [0] * 288
cnt = [0] * 288

with open(file, 'r') as data:
    csv_reader = csv.reader(data)
    for line in csv_reader:
        if len(line) > 4:
            if line[2] == "EGV":
                temp_str = ""
                temp_str = temp_str + line[3][0:10] + " " + line[3][11:] + ".0"
                date_time_obj = datetime.datetime.strptime(
                    temp_str, '%Y-%m-%d %H:%M:%S.%f')
                CGM.append(
                    (convert_unix(line[3]), int(line[4]), date_time_obj))

# set the dates here, which are inclusive
startdate = datetime.datetime(2022, 1, 11, 0, 0, 0)
enddate = datetime.datetime(2022, 1, 13, 23, 59, 59)
range = enddate-startdate
range = range.days + 1
timeskips(CGM, 550)
anom(CGM)
timeplot = pandas.date_range("00:00", "23:59", freq="5min")


# add CGM to avg
for i in CGM:
    if i[2] > startdate and i[2] < enddate:

        minute = i[2].minute
        hour = i[2].hour
        minute = minute - minute % 5
        index = int(hour*12+minute/5)
        AVG[index] = AVG[index]+i[1]
        cnt[index] = cnt[index] + 1
# determine avg
for i, n in enumerate(AVG):

    AVG[i] = n/cnt[i]

for i, n in enumerate(cnt):
    if n < range:
        AVG[i] = (AVG[i-1] + AVG[i+1])/2

plt.scatter(timeplot, AVG)
plt.plot(timeplot, AVG, label="CGM")

myFmt = mdates.DateFormatter('%H:%M')
plt.gca().xaxis.set_major_formatter(myFmt)
plt.axhspan(100, 180, color='y', alpha=0.5, lw=0)
plt.title("Daily CGM Averages")
plt.xlabel("Time in day")

plt.legend()
plt.show()
