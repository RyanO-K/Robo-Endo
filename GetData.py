import csv
import time
import datetime
import matplotlib.pyplot as plt

file = '3_days_data_Ryan.csv'
#file = '1_month_of_data_Ryan.csv'
#file = '3_months_of_data_Ryan.csv'

#convert date in YYYY-MM-DDTHH:MM:SS to unix timestamp in local time
def convert_unix(s_date):
    year = int(s_date[0:4:1])
    month = int(s_date[5:7:1])
    day = int(s_date[8:10:1])
    t = s_date[11:19:1]

    dt = datetime.datetime(year, month, day)
    u_date = dt.timestamp()
    u_date += int(t[0:2])*3600 + int(t[3:5])*60 + int(t[6:8])

    return u_date

with open(file, 'r') as data:
    csv_reader = csv.reader(data)
    
    CGM_BGM = []
    IOB = []
    for line in csv_reader:
        if len(line) > 4 :
            if line[2] == "EGV":
                CGM_BGM.append((convert_unix(line[3]), int(line[4])))
        if len(line) > 3:
            if line[0] == "IOB":
                convert_unix(line[2])
                IOB.append((convert_unix(line[2]), float(line[3])))
    
    #lists for data points for plot
    X=[]
    Y=[]
    for i in IOB:
        X.append(i[0])
        Y.append(i[1])

    plt.scatter(X, Y, s=1)
    plt.title('IOB over time')
    plt.show()

    


