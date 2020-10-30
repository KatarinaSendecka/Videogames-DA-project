from sqlalchemy import create_engine
import pandas as pd
import numpy as np


CSVname = "Video_Games_Sales.csv"
CSVname_clean = "Video_Games_Sales_clean.csv"
murders = "MurdersUSA.csv"

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

sales = df.loc[:, ['ID','NA_Sales', 'EU_Sales', 'JP_Sales', 'Global_Sales']]
sales = sales.set_index('ID')
critic = df.loc[:, ['ID','Critic_Score', 'Critic_Count', 'User_Score', 'User_Count']]
critic = critic.set_index('ID')
critic.dropna(subset = ['Critic_Score', 'Critic_Count', 'User_Score', 'User_Count'], inplace=True)

print("Critic: Percenta chybajucich hodnot v stlpcoch:")
for col in critic.columns:
    pct_missing = np.mean(critic[col].isnull())
    print('{} - {}%'.format(col, round(pct_missing*100)))

videoGames = df.loc[: ,['ID', 'Name', 'Platform', 'Year_of_Release', 'Genre', 'Publisher', 'Developer']]
videoGames = videoGames.set_index('ID')

med = videoGames['Year_of_Release'].median()
videoGames['Year_of_Release'] = videoGames['Year_of_Release'].fillna(med)
videoGames['Year_of_Release'] = videoGames['Year_of_Release'].astype(np.int64)

print("VideoGames: Percenta chybajucich hodnot v stlpcoch po vyplneni chybajucich rokov medianom:")
for col in videoGames.columns:
    pct_missing = np.mean(videoGames[col].isnull())
    print('{} - {}%'.format(col, round(pct_missing*100)))

sales.to_csv('GameSales.csv')
critic.to_csv('gameCritic.csv')
videoGames.to_csv('videoGames.csv')

murdersDf = pd.read_csv(murders, sep=';',error_bad_lines=False)

murdersNew = murdersDf.loc[:, ['Record ID','State', 'Year', 'Month', 'Perpetrator Age', 'Weapon']]
murdersNew = murdersNew.set_index('Record ID')
murdersNew['Perpetrator Age']=murdersNew['Perpetrator Age'].replace(' ',0)
murdersNew['Perpetrator Age']=murdersNew['Perpetrator Age'].replace(0, np.nan)
murdersNew['Perpetrator Age']=murdersNew['Perpetrator Age'].replace('0', np.nan)
med2 = murdersNew['Perpetrator Age'].median()
murdersNew['Perpetrator Age'] = murdersNew['Perpetrator Age'].fillna(med2)
murdersNew['Perpetrator Age'] = murdersNew['Perpetrator Age'].astype(np.int64)


murdersNew['Year'] = murdersNew['Year'].astype(np.int64)
#print(murdersNew.isna().sum())
murdersNew.to_csv('Murders_clean.csv')

"""
engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres', echo=False) #prepoklada sa, ze databaza bezi, pre spustenie v terminali zavolat ./pgDocker.bat
videoGames.to_sql("VideoGames", engine)
critic.to_sql("Critic", engine)
sales.to_sql("Sales", engine)
murdersNew.to_sql("Murders", engine)
"""