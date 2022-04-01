import csv
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates



file = '3_days_data_Ryan.csv'
#file = '1_month_of_data_Ryan.csv'
# file = '3_months_of_data_Ryan.csv'
#Just insuline delivered against time, daily tracking
'''
Insuline deliver against carb, with dataframe of just a meal 
'''


IOB = list()
BG = list()
InsulinDelivered = list()
Completion_time = list()


with open(file, 'r') as data:
    csv_reader = csv.reader(data)

    for line in csv_reader:
        if len(line) >= 41 and line[3] != "IOB" and line[7] != "InsulinDelivered":
            if line[3] == "" or line[6] == "" or line[7] == "":
                continue
            IOB.append(float(line[3]))
            InsulinDelivered.append(float(line[7]))
            temp_str = ""
            temp_str = temp_str + line[6][0:10] + " " + line[6][11:] + ".0"
            date_time_obj = datetime.datetime.strptime(temp_str, '%Y-%m-%d %H:%M:%S.%f')
            Completion_time.append(date_time_obj)



plt.scatter(Completion_time, IOB)
plt.scatter(Completion_time, InsulinDelivered)

plt.plot(Completion_time, IOB, label="IOB")
plt.plot(Completion_time, InsulinDelivered, label="Insulin Delivered")

myFmt = mdates.DateFormatter('%H:%M')
plt.gca().xaxis.set_major_formatter(myFmt)

plt.title("IOB and Insulin Delivered over Time in day")
plt.xlabel("Time in day")

plt.legend()
plt.show()