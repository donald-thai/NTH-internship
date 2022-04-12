import pandas as pd
from xlwt import Workbook
from pathlib import Path
import numpy as np
import os
from glob import glob

folder = ""
file = ""

x = ""
y = 10000000000000000000000
df = pd.read_csv(file)


def write(s, r, value, index):
    # list= ["Min", "Max"]
    min = value[0]
    max = value[1]
    if isinstance(min, (np.int64)):  # Converts from np.int64 to an int
        val = np.int64(min)
        pyval = val.item()
        min = int(pyval)
    if isinstance(max, (np.int64)):
        val = np.int64(max)
        pyval = val.item()
        max = int(pyval)
    if (index == 7):  # When we write status, uppercase the hexadecimal
        min = str(hex(min)).upper()[2:]
        max = str(hex(max)).upper()[2:]
    s.write(r, 0, f"Min {names[count]}")  # Write name of minimum row in workbook
    s.write(r, 1, value[2])  # Write min time in min row
    s.write(r, 2, value[4])  # Write gauge name
    s.write(r, index, min)  # Write the min value
    r += 1
    s.write(r, 0, f"Max {names[count]}")  # Write ame of max row
    s.write(r, 1, value[3])  # Write max time
    s.write(r, 2, value[4])  # Write gauge name
    s.write(r, index, max)  # Write max value in correct column


chunksize = 400000
folder = "";
x = glob(folder)
for dir in x:  # Goes through COMM folders
    for file in Path(dir).glob('*.csv'):  # Goes through csv files
        wb = Workbook()
        s = wb.add_sheet('Sheet 1', cell_overwrite_ok=True)  # Sets up the excel workbook with a sheet
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
        for chunk in pd.read_csv(file, chunksize=chunksize):  # Breaks data into chunks
            for row in range(0, len(chunk.index)):  # Go through each row in the chunk
                count = 0;  # Used to go through array index
                for type in sensor:  # Go through the columns of each row to check min/max
                    ind = sensor_index[count]  # Column number
                    if ind == 8:  # Deals with the hex number in column 8
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
                        if chunk.iloc[row, ind] < type[0]:  # Checks if it is less than the current minimum and if it is then replace min value in array
                            type[0] = chunk.iloc[row, ind]
                            type[2] = chunk.iloc[row, 0]
                            type[4] = chunk.iloc[row, 1]
                        else:
                            if chunk.iloc[row, ind] > type[1]:  # If less than min, then check if it could be max
                                type[1] = chunk.iloc[row, ind]
                                type[3] = chunk.iloc[row, 0]
                                type[4] = chunk.iloc[row, 1]
                    count += 1
        names = ["Pressure", "Temp", "RawP", "RawT", "Status", "CommRate"] #Used to write in the workbook. See method at the start
        report_index = [3, 4, 5, 6, 7, 8]

        comm = os.path.basename(os.path.dirname(os.path.dirname(file))) #Get the COMM of the file

        count = 0
        for type in sensor: #Create excel containing min max data
            write(s, r, value=type, index=report_index[count])
            r += 2
            count += 1

        x = comm+ " "+ os.path.basename(file) #Write file name and saves the excel file
        name = x[0:len(x) - 3] + "xls"
        wb.save(name)

        with open(x[0:len(x) - 4] + "_report.txt", 'w') as file2: #Read excel file and copy contents to a text file.
            df2 = pd.read_excel(name)
            df2 = df2.rename({'Unnamed: 0': ''}, axis='columns') #Empty boxes that have unnamed in it because they were empty in the excel file
            df2.to_string(file2, index=False, na_rep="")
