import pandas as pd

filecsv = open("Video_Games_Sales.csv",encoding='utf-8')
filecsv2 = open("Video_Games_Sales_clean.csv","w",encoding='utf-8')

for bad_row in filecsv:
    
    for i in range(0, len(bad_row)):
        if bad_row[i] == ";" and bad_row[i+1] ==" ":
            bad_row = bad_row[:i] + "," + bad_row[i+1:]

    filecsv2.write(bad_row)
    
filecsv.close()
filecsv2.close()





