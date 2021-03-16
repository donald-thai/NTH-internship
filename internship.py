import pandas as pd
from xlwt import Workbook
from pathlib import Path
import numpy as np
import os
from glob import glob

folder = "C:/Users/donal/Documents/Data File/COMM_3/*/"
file = "C:/Users/donal/Documents/2020-06-13.csv"
file = "C:/Users/donal/Documents/Data File/COMM_3/06-2019/2019-06-13.csv"

x = ""
y = 10000000000000000000000
df = pd.read_csv(file)

def write(s, r, value, index):
    # list= ["Min", "Max"]
    min = value[0]
    max = value[1]
    if isinstance(min, (np.int64)):
        val = np.int64(min)
        pyval = val.item()
        min = int(pyval)
    if isinstance(max, (np.int64)):
        val = np.int64(max)
        pyval = val.item()
        max = int(pyval)
    if (index == 7):
        min = str(hex(min)).upper()[2:]
        max = str(hex(max)).upper()[2:]
    s.write(r, 0, f"Min {names[count]}")
    s.write(r, 1, value[2])
    s.write(r, 2, value[4])
    s.write(r, index, min)
    r += 1
    s.write(r, 0, f"Max {names[count]}")
    s.write(r, 1, value[3])
    s.write(r, 2, value[4])
    s.write(r, index, max)


chunksize = 400000
folder = "C:/Users/donal/Documents/Data File/*/*/"
x = glob(folder)
for dir in x:
    for file in Path(dir).glob('*.csv'):
        wb = Workbook()
        s = wb.add_sheet('Sheet 1', cell_overwrite_ok=True)
        s.write(0, 1, "Timestamp")
        s.write(0, 2, "Gauge Name")
        s.write(0, 3, "Pressure")
        s.write(0, 4, "Temperature")
        s.write(0, 5, "RawP")
        s.write(0, 6, "RawT")
        s.write(0, 7, "Status")
        s.write(0, 8, "CommRate")
        r = 1

        Pressure = [10000000000000, -10000000000000, "", "", ""]  # hold the min, max , min time, max time, gauge name
        Temp = [10000000000000, -10000000000000, "", "", ""]
        RawP = [10000000000000, -10000000000000, "", "", ""]
        RawT = [10000000000000, -10000000000000, "", "", ""]
        Status = [10000000000000, 10000000000000, "", "", ""]
        CommRate = [10000000000000, -10000000000000, "", "", ""]

        sensor_index = [4, 5, 6, 7, 8, 9]
        sensor = [Pressure, Temp, RawP, RawT, Status, CommRate]

        df = pd.read_csv(file)
        for chunk in pd.read_csv(file, chunksize=chunksize):
            for row in range(0, len(chunk.index)):
                count = 0;
                for type in sensor:
                    ind = sensor_index[count] #Column number
                    if ind == 8:
                        hex_int = int(df.iloc[row, ind], 16)
                        if hex_int < type[1]:
                            if hex_int != 0:
                                type[1] = hex_int
                                type[3] = chunk.iloc[row, 0]
                                type[4] = chunk.iloc[row, 1]
                        if hex_int == 0:
                            type[0] = 0
                            type[2] = chunk.iloc[row, 0]
                            type[4] = chunk.iloc[row, 1]
                        else:
                            if hex_int < type[0]:
                                type[0] = hex_int
                                type[2] = chunk.iloc[row, 0]
                                type[4] = chunk.iloc[row, 1]
                    else:
                        if chunk.iloc[row, ind] < type[0]:
                            type[0] = chunk.iloc[row, ind]
                            type[2] = chunk.iloc[row, 0]
                            type[4] = chunk.iloc[row, 1]
                        else:
                            if chunk.iloc[row, ind] > type[1]:
                                type[1] = chunk.iloc[row, ind]
                                type[3] = chunk.iloc[row, 0]
                                type[4] = chunk.iloc[row, 1]
                    count += 1
        names = ["Pressure", "Temp", "RawP", "RawT", "Status", "CommRate"]
        report_index = [3, 4, 5, 6, 7, 8]

        comm = os.path.basename(os.path.dirname(os.path.dirname(file)))

        count = 0
        for type in sensor:
            write(s, r, value=type, index=report_index[count])
            r += 2
            count += 1

        x = comm+ " "+ os.path.basename(file)
        name = x[0:len(x) - 3] + "xls"
        wb.save(name)

        with open(x[0:len(x) - 4] + "_report.txt", 'w') as file2:
            df2 = pd.read_excel(name)
            df2 = df2.rename({'Unnamed: 0': ''}, axis='columns')
            df2.to_string(file2, index=False, na_rep="")
