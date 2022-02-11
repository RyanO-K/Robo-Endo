import csv
import time
import datetime
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
    plt.show()
    return BG


def plotCGM(file, CGM, frame4=None):

    X = []
    Y = []
    for i, elem in enumerate(CGM):
        if i > 0 and i+1 < len(CGM):
            if elem[1]-CGM[i-1][1] < 0 and elem[1]-CGM[i+1][1] < 0 and CGM[2] == -1:
                elem[1] = min(abs(elem[1]-CGM[i-1][1]),
                              abs(CGM[i+1][1]-elem[1]))
            X.append(elem[0])
            Y.append(elem[1])

    figure = plt.figure()
    CGM_time = FigureCanvasTkAgg(figure, frame4)
    CGM_time.get_tk_widget().pack()
    figure = plt.scatter(X, Y, s=1)
    figure = plt.title('CGM over time')

    plt.show()
    return CGM_time


def plotAnCGM(file, CGM, frame2):
    # outlier detection of EGV
    df = pd.DataFrame(CGM, columns=['time', 'CGM'])
    outliers_fraction = 0.05
    model = IsolationForest(contamination=outliers_fraction)
    pdf = pd.DataFrame(CGM, columns=['time', 'CGM'])
    model.fit(pdf.values)
    pdf['anomaly2'] = pd.Series(model.predict(pdf.values))
    # visualization of EGV outliers
    df['anomaly2'] = pd.Series(pdf['anomaly2'].values, index=df.index)
    a = df.loc[df['anomaly2'] == -1]  # anomaly
    figure = plt.figure()
    CGM_anomalies = FigureCanvasTkAgg(figure, frame2)
    CGM_anomalies.get_tk_widget().pack()
    figure = plt.plot(df['CGM'], color='blue', label='Normal')
    figure = plt.plot(a['CGM'], linestyle='none', marker='X',
                      color='red', markersize=12, label='Anomaly')
    figure = plt.xlabel('Time')
    figure = plt.ylabel('CGM')
    figure = plt.title('CGM Anomalies')
    figure = plt.legend(loc='best')
    CGM = df.values.tolist()
    return CGM_anomalies


def plotAnIOB(file, IOB, frame1):
    # outlier detection of IOB
    df = pd.DataFrame(IOB, columns=['time', 'IOB'])
    outliers_fraction = 0.05
    model = IsolationForest(contamination=outliers_fraction)
    pdf = pd.DataFrame(IOB, columns=['time', 'IOB'])
    model.fit(pdf.values)
    pdf['anomaly2'] = pd.Series(model.predict(pdf.values))
    # visualization of IOB outliers
    df['anomaly2'] = pd.Series(pdf['anomaly2'].values, index=df.index)
    a = df.loc[df['anomaly2'] == -1]  # anomaly
    figure = plt.figure()
    IOB_anomalies = FigureCanvasTkAgg(figure, frame1)
    IOB_anomalies.get_tk_widget().pack(expand=True)

    figure = plt.plot(df['IOB'], color='blue', label='Normal')
    figure = plt.plot(a['IOB'], linestyle='none', marker='X',
                      color='red', markersize=12, label='Anomaly')
    figure = plt.xlabel('Time')
    figure = plt.ylabel('IOB')
    figure = plt.title('IOB Anomalies')
    figure = plt.legend(loc='best')
    return IOB_anomalies


def plotIOB(file, IOB, frame3=None):

    # lists for data points for plot
    X = []
    Y = []

    for i in IOB:
        X.append(i[0])
        Y.append(i[1])

    figure = plt.figure()
    IOB_Time = FigureCanvasTkAgg(figure, frame3)
    IOB_Time.get_tk_widget().pack()

    figure = plt.scatter(X, Y, s=1)
    figure = plt.title('IOB over time')

    plt.show()

    return IOB_Time


def plot(file, frame1=None, frame2=None, frame3=None, frame4=None, frame5=None):
    IOB = []
    CGM = []
    BG = list()
    Completion_time = list()
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
                if line[2] == "" or line[6] == "":
                    continue
                else:
                    BG.append(int(line[2]))

                    temp_str = ""
                    temp_str = temp_str + \
                        line[6][0:10] + " " + line[6][11:] + ".0"
                    date_time_obj = datetime.datetime.strptime(
                        temp_str, '%Y-%m-%d %H:%M:%S.%f')
                    Completion_time.append(date_time_obj)

    return plotIOB(file, IOB, frame3=None), plotAnCGM(file, CGM, frame2=None), plotCGM(file, CGM, frame4=None), plotAnIOB(file, IOB, frame1=None)


if __name__ == "__main__":
    plot(sys.argv[1])
