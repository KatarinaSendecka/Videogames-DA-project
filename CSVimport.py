from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

CSVname = "Video_Games_Sales.csv"
CSVname_clean = "Video_Games_Sales_clean.csv"
murders = "MurdersUSA.csv"
esport = "GeneralEsportData.csv"
esportNew = "GeneralEsportData_clean.csv"

# removing separator from the names of games
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

# add ID to Esport table
fileEsport = open(esport,encoding="latin-1")
fileEsport2 = open(esportNew ,"w",encoding="utf-8")

id = 1
header = "ID," + fileEsport.readline()
fileEsport2.write(header)

for row in fileEsport:
    row = str(id) + "," + row
    id += 1
    fileEsport2.write(row)

fileEsport.close()
fileEsport2.close()

# import Esport table
esportDf = pd.read_csv("GeneralEsportData_clean.csv", encoding="utf-8")

"""
print(esportDf['ReleaseDate'].describe())
print(esportDf['Game'].describe())
print(esportDf['Genre'].describe())
print(esportDf['TotalEarnings'].describe())
print(esportDf['OnlineEarnings'].describe())
print(esportDf['TotalTournaments'].describe())
"""
esportDfNew = esportDf.loc[:, ['ID','Game','ReleaseDate','Genre','TotalEarnings','OnlineEarnings','TotalPlayers','TotalTournaments']]
esportDfNew = esportDfNew.set_index('ID')
esportDfNew = esportDfNew.rename(columns={'Game': 'Name'})
# cleaning data
"""
esportDfNew.info()
print(esportDfNew.isnull().sum())
print(len(esportDfNew.Name.unique()))
"""
# import "Video_Games_Sales.csv"
df = pd.read_csv(CSVname_clean, sep=';',error_bad_lines=False)

# delete empty names
df.dropna(subset = ['Name'], inplace=True)
# creating 3 tables from "Video_Games_Sales.csv" : sales, critic, videoGames
sales = df.loc[:, ['ID','NA_Sales', 'EU_Sales', 'JP_Sales', 'Global_Sales']]
sales = sales.set_index('ID')
critic = df.loc[:, ['ID','Critic_Score', 'Critic_Count', 'User_Score', 'User_Count']]
critic = critic.set_index('ID')
videoGames = df.loc[: ,['ID', 'Name', 'Platform', 'Year_of_Release', 'Genre', 'Publisher', 'Developer']]
videoGames = videoGames.set_index('ID')
# cleaning of table sales
"""
sales.info()
print(sales.isnull().sum())
print(sales["Global_Sales"].describe())
print(sales["NA_Sales"].describe())
print(sales["EU_Sales"].describe())
print(sales["JP_Sales"].describe())
"""
#method below is not exact for showing missing values
# print("VideoGames: Percenta chybajucich hodnot v stlpcoch po vyplneni chybajucich rokov medianom:")
# for col in videoGames.columns:
#     pct_missing = np.mean(videoGames[col].isnull())
#     print('{} - {}%'.format(col, round(pct_missing*100)))

""" #histograms
sns.set_theme(style="whitegrid")
boxGS = sns.boxplot(x=sales["Global_Sales"])
plt.show()
boxNAS = sns.boxplot(x=sales["NA_Sales"])
plt.show()
boxEUS = sns.boxplot(x=sales["EU_Sales"])
plt.show()
boxJPS = sns.boxplot(x=sales["JP_Sales"])
plt.show()
"""
sales.dropna(subset = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Global_Sales'], inplace=True)
"""
print(sales['Global_Sales'].idxmax())
print(sales.loc[1])
print(videoGames.loc[1])
"""
# cleaning of table critic
"""
critic.info()
print(critic.isnull().sum())
print(critic['Critic_Score'].describe())
print(critic['Critic_Count'].describe())
print(critic['User_Score'].describe())
print(critic['User_Count'].describe())
"""
critic.dropna(subset = ['Critic_Score', 'Critic_Count', 'User_Score', 'User_Count'], inplace=True)
""" #histohrams
sns.displot(critic, x="Critic_Score")
plt.show()
sns.displot(critic, x="User_Score")
plt.show()
"""
#cleaning of table videoGames
"""
videoGames.info()
print(videoGames.isnull().sum())
print(videoGames.Platform.unique())
print(videoGames.Genre.unique())
print(videoGames.Publisher.unique())
print(videoGames['Year_of_Release'].describe())
"""
med = videoGames['Year_of_Release'].median()
videoGames['Year_of_Release'] = videoGames['Year_of_Release'].fillna(med)
videoGames['Year_of_Release'] = videoGames['Year_of_Release'].astype(np.int64)
"""
sns.displot(videoGames, x="Year_of_Release")
plt.show()
"""
# replace empty rows with unknown
videoGames['Platform'] = videoGames['Platform'].replace(np.nan, 'Unknown')
videoGames['Genre'] = videoGames['Genre'].replace(np.nan, 'Unknown')
videoGames['Publisher'] = videoGames['Publisher'].replace(np.nan, 'Unknown')

#print(videoGames[videoGames['Year_of_Release'] == 2020])
videoGames.at[5937,'Year_of_Release'] = 2009 #rewriting of bad year

# import Murders dataset
murdersDf = pd.read_csv(murders, sep=';',error_bad_lines=False, dtype=object)

# cleaning of table Murders
murdersNew = murdersDf.loc[:, ['Record ID','State', 'Year', 'Month', 'Perpetrator Age', 'Weapon']]
murdersNew = murdersNew.set_index('Record ID')
"""
murdersNew.info()
print(murdersNew.isnull().sum())
print(murdersNew.Weapon.unique())
print(murdersNew.State.unique())
"""
murdersNew['Perpetrator Age'] = murdersNew['Perpetrator Age'].replace(' ', np.nan)
murdersNew['Perpetrator Age'] = murdersNew['Perpetrator Age'].replace(0, np.nan)
murdersNew['Perpetrator Age'] = murdersNew['Perpetrator Age'].replace('0', np.nan)
med2 = murdersNew['Perpetrator Age'].median()
murdersNew['Perpetrator Age'] = murdersNew['Perpetrator Age'].fillna(med2)
murdersNew['Perpetrator Age'] = murdersNew['Perpetrator Age'].astype(np.int64)
murdersNew['Year'] = murdersNew['Year'].astype(np.int64)
"""
print(murdersNew.isna().sum())
print(murdersNew['Year'].describe())
print(murdersNew['Perpetrator Age'].describe())
print(murdersNew[murdersNew['Perpetrator Age'] == 1])
"""
murdersNew = murdersNew[murdersNew['Perpetrator Age'] >= 6] #deleting of murders below age of 6

# exporting the tables to csv
sales.to_csv('GameSales.csv')
critic.to_csv('gameCritic.csv')
videoGames.to_csv('videoGames.csv')
murdersNew.to_csv('Murders_clean.csv')
esportDfNew.to_csv('esportDfNew.csv')

# exporting the tables to sql database
"""
engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres', echo=False) #prepoklada sa, ze databaza bezi, pre spustenie v terminali zavolat ./pgDocker.bat
videoGames.to_sql("VideoGames", engine)
critic.to_sql("Critic", engine)
sales.to_sql("Sales", engine)
murdersNew.to_sql("Murders", engine)
esportDfNew.to_sql("Esport", engine)
"""
#Developer table
czechDevelopers = videoGames[videoGames['Developer'] == 'Bohemia Interactive']
czechDevelopers = czechDevelopers.append(videoGames[videoGames['Developer'] == '2K Czech'])
czechDevelopers = czechDevelopers.append(videoGames[videoGames['Developer'] == 'Amanita Design'])
czechDevelopers = czechDevelopers.append(videoGames[videoGames['Developer'] == 'SCS Software'])
print(czechDevelopers)
