import csv
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

file = '3_days_data_Ryan.csv'
# file = '1_month_of_data_Ryan.csv'
# file = '3_months_of_data_Ryan.csv'
BG = list()
Completion_time = list()

with open(file, 'r') as data:
    csv_reader = csv.reader(data)

    for line in csv_reader:
        if len(line) >= 41 and line[2] != "BG":
            if line[2] == "" or line[6] == "":
                continue
            else:
                BG.append(int(line[2]))

                temp_str = ""
                temp_str = temp_str + line[6][0:10] + " " + line[6][11:] + ".0"
                date_time_obj = datetime.datetime.strptime(temp_str, '%Y-%m-%d %H:%M:%S.%f')
                Completion_time.append(date_time_obj)


plt.scatter(Completion_time[1:], BG[1:])
plt.plot(Completion_time[1:], BG[1:])

myFmt = mdates.DateFormatter('%H:%M')
plt.gca().xaxis.set_major_formatter(myFmt)

plt.title("BG level over Time in day")
plt.xlabel("Time in day")
plt.ylabel("Blood Glucose level (BG)")

plt.show()
