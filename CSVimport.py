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
HistoricalEsport = "HistoricalEsportData.csv"
HistoricalEsportNew = "HistoricalEsportData_clean.csv"

def videogames_clean_csv(CSV_name, CSV_name_clean):
    filecsv = open(CSV_name,encoding='utf-8')
    filecsv2 = open(CSV_name_clean ,"w",encoding='utf-8')

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


def addID_to_table(file, file_new):
    file_table = open(file,encoding="latin-1")
    file_table_new = open(file_new,"w",encoding="utf-8")

    id = 1
    header = "ID," + file_table.readline()
    file_table_new.write(header)

    for row in file_table:
        row = str(id) + "," + row
        id += 1
        file_table_new.write(row)

    file_table.close()
    file_table_new.close()

def import_videogames(CSV_name_clean):
    df = pd.read_csv(CSV_name_clean, sep=';',error_bad_lines=False)
    df = df.set_index('ID')
    # delete empty names
    df.dropna(subset = ['Name'], inplace=True)
    #dropping duplicates
    df = df.drop_duplicates()
    # creating 3 tables from "Video_Games_Sales.csv" : sales, critic, videoGames
    sales = df.loc[:, ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Global_Sales']]
    critic = df.loc[:, ['Critic_Score', 'Critic_Count', 'User_Score', 'User_Count']]
    videoGames = df.loc[: ,['Name', 'Platform', 'Year_of_Release', 'Genre', 'Publisher', 'Developer']]
    return critic, sales, videoGames

def cleaning_videogames_table():
    med = videoGames['Year_of_Release'].median()

    videoGames['Year_of_Release'] = videoGames['Year_of_Release'].fillna(med)
    videoGames['Year_of_Release'] = videoGames['Year_of_Release'].astype(np.int64)
    videoGames['Platform'] = videoGames['Platform'].replace(np.nan, 'Unknown')
    videoGames['Genre'] = videoGames['Genre'].replace(np.nan, 'Unknown')
    videoGames['Publisher'] = videoGames['Publisher'].replace(np.nan, 'Unknown')
    videoGames.at[5937,'Year_of_Release'] = 2009
    videoGames.to_csv('videoGames.csv')

def cleaning_sales_table():
    sales.dropna(subset = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Global_Sales'], inplace=True)
    sales.to_csv('GameSales.csv')

def cleaning_critic_table():
    critic.dropna(subset = ['Critic_Score', 'Critic_Count', 'User_Score', 'User_Count'], inplace=True)
    critic.to_csv('gameCritic.csv')

def import_esport():
    esportDf = pd.read_csv(esportNew, encoding="utf-8")
    esportDfNew = esportDf.loc[:, ['ID','Game','ReleaseDate','Genre','TotalEarnings','OnlineEarnings','TotalPlayers','TotalTournaments']]
    esportDfNew = esportDfNew.set_index('ID')
    esportDfNew = esportDfNew.rename(columns={'Game': 'Name'}) 
    esportDfNew.to_csv('esportDfNew.csv')
    return esportDfNew

def import_historical_esport():
    HistoricalEsportDf = pd.read_csv(HistoricalEsportNew, encoding="utf-8")
    HistoricalEsportDfNew = HistoricalEsportDf.loc[:, ['ID','Date','Game','Earnings','Players','Tournaments']]
    HistoricalEsportDfNew = HistoricalEsportDfNew.set_index('ID')
    HistoricalEsportDfNew['Date'] = pd.to_datetime(HistoricalEsportDfNew['Date'])
    HistoricalEsportDfNew.to_csv('HistoricalEsportNew.csv')
    return HistoricalEsportDfNew

def import_murders():
    murdersDf = pd.read_csv(murders, sep=';',error_bad_lines=False, dtype=object)
    murdersDf = murdersDf.set_index('Record ID')
    murdersNew = murdersDf.loc[:, ['State', 'Year', 'Month', 'Perpetrator Age', 'Weapon']]
    murdersNew['Perpetrator Age'] = murdersNew['Perpetrator Age'].replace(' ', np.nan)
    murdersNew['Perpetrator Age'] = murdersNew['Perpetrator Age'].replace(0, np.nan)
    murdersNew['Perpetrator Age'] = murdersNew['Perpetrator Age'].replace('0', np.nan)
    med2 = murdersNew['Perpetrator Age'].median()
    murdersNew['Perpetrator Age'] = murdersNew['Perpetrator Age'].fillna(med2)
    murdersNew['Perpetrator Age'] = murdersNew['Perpetrator Age'].astype(np.int64)
    murdersNew['Year'] = murdersNew['Year'].astype(np.int64)
    murdersNew = murdersNew[murdersNew['Perpetrator Age'] >= 4]
    murdersNew.to_csv('Murders_clean.csv')
    return murdersNew

def correlation_coefficients_games_murders():
    corCoefData = videoGames.merge(sales, on='ID')
    corCoefData1 = corCoefData.loc[:, ['Name', 'Year_of_Release']]
    corData1 = corCoefData1.groupby('Year_of_Release').count()
    corData2 = murdersNew.loc[:, ['Year', 'State']]
    corData2 = corData2.groupby('Year').count()
    corDataGames = corData1.merge(corData2, left_index=True, right_index=True)
    corDataGames = corDataGames.rename(columns={"Name": "Games", "State": "Murders"})
    corCoef1 = corDataGames.corr()
    corCoefData2 = corCoefData.loc[:, ['NA_Sales', 'Year_of_Release']]
    corData3 = corCoefData2.groupby('Year_of_Release').sum()
    corDataSales = corData3.merge(corData2, left_index=True, right_index=True)
    corDataSales = corDataSales.rename(columns={"State": "Murders"})
    corCoef2 = corDataSales.corr()
    return print(f"\n{corCoef1}\n\n{corCoef2}\n")


# removing separator from the names of games
videogames_clean_csv(CSVname, CSVname_clean)
# creating od three separate tables
critic, sales, videoGames = import_videogames(CSVname_clean)

# cleaning of table sales
"""
sales.info()
print(sales.isnull().sum())
print(sales["Global_Sales"].describe())
print(sales["NA_Sales"].describe())
print(sales["EU_Sales"].describe())
print(sales["JP_Sales"].describe())
 
#histograms
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
cleaning_sales_table()
# cleaning of table critic
"""
critic.info()
print(critic.isnull().sum())
print(critic['Critic_Score'].describe())
print(critic['Critic_Count'].describe())
print(critic['User_Score'].describe())
print(critic['User_Count'].describe())

#histohrams
sns.displot(critic, x="Critic_Score")
plt.show()
sns.displot(critic, x="User_Score")
plt.show()
"""
cleaning_critic_table()

# add ID to Esport table
addID_to_table(esport, esportNew)

#add ID to historical esport table
addID_to_table(HistoricalEsport, HistoricalEsportNew)

# import Esport table
esportDfNew = import_esport()
"""
print(esportDf['ReleaseDate'].describe())
print(esportDf['Game'].describe())
print(esportDf['Genre'].describe())
print(esportDf['TotalEarnings'].describe())
print(esportDf['OnlineEarnings'].describe())
print(esportDf['TotalTournaments'].describe())

esportDfNew.info()
print(esportDfNew.isnull().sum())
print(len(esportDfNew.Name.unique()))
"""
# import HistoricalEsport table
HistoricalEsportDfNew = import_historical_esport()
"""
print(HistoricalEsportDf['Game'].describe())
print(HistoricalEsportDf['Earnings'].describe())
print(HistoricalEsportDf['Players'].describe())
print(HistoricalEsportDf['Tournaments'].describe())
"""

#cleaning of table videoGames
cleaning_videogames_table()
"""
videoGames.info()
print(videoGames.isnull().sum())
print(videoGames.Platform.unique())
print(videoGames.Genre.unique())
print(videoGames.Publisher.unique())
print(videoGames['Year_of_Release'].describe())
"""
#histograms of videogames
"""
sns.displot(videoGames, x="Year_of_Release")
plt.show()
"""

# import Murders dataset
murdersNew = import_murders()

# cleaning of table Murders
"""
murdersNew.info()
print(murdersNew.isnull().sum())
print(murdersNew.Weapon.unique())
print(murdersNew.State.unique())
print(murdersNew.isna().sum())
print(murdersNew['Year'].describe())
print(murdersNew['Perpetrator Age'].describe())
print(murdersNew[murdersNew['Perpetrator Age'] == 1])
"""
# exporting the tables to sql database
'''
engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres', echo=False) #prepoklada sa, ze databaza bezi, pre spustenie v terminali zavolat ./pgDocker.bat
videoGames.to_sql("VideoGames", engine)
critic.to_sql("Critic", engine)
sales.to_sql("Sales", engine)
murdersNew.to_sql("Murders", engine)
esportDfNew.to_sql("Esport", engine)
HistoricalEsportDfNew.to_sql("HistoricalEsport", engine)
'''
#calculating of correlation coffeicient
correlation_coefficients_games_murders()