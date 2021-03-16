import pandas as pd
from pathlib import Path
import os
from glob import glob

file = "C:/Users/donal/Documents/Internship/COMM_3 2019-06-13_report.txt"
folder = "C:/Users/donal/Documents/Internship/"
x=glob(folder)
for dir in x:
    for file in Path(dir).glob('*.txt'):
        df= pd.read_fwf(file)
        for row in range(0,len(df.index)):
            if df.iloc[row,3] > 30: #Pressure Checking
                print(f"Pressure Error at Gauge {df.iloc[row, 2]} at row {row}. File name is {os.path.basename(file)}")
            if df.iloc[row,4] >= 200 or df.iloc[row,4] <= 180:
                print(f"Temperature Error at Gauge {df.iloc[row, 2]} at row {row}. File name is {os.path.basename(file)}")
            if df.iloc[row,5]==0:
                print(f"RawP Error at Gauge {df.iloc[row, 2]} at row {row}. File name is {os.path.basename(file)}")
            if df.iloc[row, 6] == 0:
                print(f"RawT Error at Gauge {df.iloc[row, 2]} at row {row}. File name is {os.path.basename(file)}")
            if row==8 or row==9:
                if df.iloc[row,7]!= "A000":
                    print(f"Status Error at Gauge {df.iloc[row, 2]} at row {row}. File name is {os.path.basename(file)}")
            if df.iloc[row,8]<=.8:
                print(f"CommRate Error at Gauge {df.iloc[row, 2]} at row {row}. File name is {os.path.basename(file)}")


