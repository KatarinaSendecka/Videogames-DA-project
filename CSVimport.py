import pandas as pd

CSVname = "Video_Games_Sales.csv"
CSVname_clean = "Video_Games_Sales_clean.csv"

filecsv = open(CSVname,encoding='utf-8')
filecsv2 = open(CSVname_clean ,"w",encoding='utf-8')

id = 1
header = "ID;" + filecsv.readline()
filecsv2.write(header)

for bad_row in filecsv: 
    for i in range(0, len(bad_row)):
        if bad_row[i] == ";" and bad_row[i+1] ==" ":
            bad_row = bad_row[:i] + "," + bad_row[i+1:]

    bad_row = str(id) + ";" + bad_row
    id += 1
    filecsv2.write(bad_row)
    
filecsv.close()
filecsv2.close()

df = pd.read_csv(CSVname_clean, sep=';',error_bad_lines=False)

print(df)



