import csv
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

file = '3_days_data_Ryan.csv'
#file = '1_month_of_data_Ryan.csv'
# file = '3_months_of_data_Ryan.csv'

'''
Insuline deliver against carb, with dataframe of just a meal 
'''

InsulinDelivered = list()
Completion_time = list()
Carb_size = list()


with open(file, 'r') as data:
    csv_reader = csv.reader(data)

    for line in csv_reader:
        if len(line) >= 41 and line[24] != "BolusType" and line[7] != "InsulinDelivered":
            if line[24] == "Carb" and line[6] != "":
                InsulinDelivered.append(float(line[7]))
                Carb_size.append(int(line[28]))
                temp_str = ""
                temp_str = temp_str + line[6][0:10] + " " + line[6][11:] + ".0"
                date_time_obj = datetime.datetime.strptime(temp_str, '%Y-%m-%d %H:%M:%S.%f')
                Completion_time.append(date_time_obj)






plt.scatter(Completion_time, InsulinDelivered)
plt.plot(Completion_time, InsulinDelivered, label="Insulin Delivered")
#plt.bar(Completion_time, Carb_size, width=.025)

myFmt = mdates.DateFormatter('%m-%d %H:%M')
plt.gca().xaxis.set_major_formatter(myFmt)

plt.title("Insulin Delivered over Every Meal in Multiple days")
plt.xlabel("Time in day")

plt.xticks(rotation = 70)


plt.legend()
plt.show()

