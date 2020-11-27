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
InsertDb = False

######  ENGINE DOCKER  ######

engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres', echo=False)

def insert_db(df, table_name, engine):
    if InsertDb:
        df.to_sql(table_name, engine)

######  ORIGINAL VIDEOGAMES DATASET  ######

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

######  ADDING ID TO TABLE  ######

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

###### DIVIDING AND CLEANING VIDEOGAMES DATASET ######

def transform_videogames_dataset(CSVname_clean):
    df = pd.read_csv(CSVname_clean, sep=';',error_bad_lines=False)
    clean_videogames_dataset(df)
    sales = df.loc[:, ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Global_Sales']]
    critic = df.loc[:, ['Critic_Score', 'Critic_Count', 'User_Score', 'User_Count']]
    videoGames = df.loc[: ,['Name', 'Platform', 'Year_of_Release', 'Genre', 'Publisher', 'Developer']]
    return critic, sales, videoGames

def clean_videogames_dataset(df):
    df = df.set_index('ID')
    df.dropna(subset = ['Name'], inplace=True)
    df = df.drop_duplicates()


######  VIDEOGAMES TABLE  ######

def process_videogames(engine, enable_print = False):
    sanitize_videogames(videoGames)
    videoGames.to_csv('videoGames.csv')
    print_videogames(videoGames, enable_print)
    insert_db(videoGames, "VideoGames", engine)
    return videoGames

def print_videogames(videoGames, print_enabled):
    if print_enabled:
        videoGames.info()
        print(videoGames.isnull().sum())
        print(videoGames.Platform.unique())
        print(videoGames.Genre.unique())
        print(videoGames.Publisher.unique())
        print(videoGames['Year_of_Release'].describe())

        sns.displot(videoGames, x="Year_of_Release")
        plt.show()

def sanitize_videogames(videoGames):
    med = videoGames['Year_of_Release'].median()
    videoGames['Year_of_Release'] = videoGames['Year_of_Release'].fillna(med)
    videoGames['Year_of_Release'] = videoGames['Year_of_Release'].astype(np.int64)
    videoGames['Platform'] = videoGames['Platform'].replace(np.nan, 'Unknown')
    videoGames['Genre'] = videoGames['Genre'].replace(np.nan, 'Unknown')
    videoGames['Publisher'] = videoGames['Publisher'].replace(np.nan, 'Unknown')
    videoGames.at[5937,'Year_of_Release'] = 2009

######  SALES TABLE ######

def process_sales(engine, enable_print = False):
    sales.dropna(subset = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Global_Sales'], inplace=True)
    sales.to_csv('GameSales.csv')
    print_sales(sales, enable_print)
    insert_db(sales, "Sales", engine)
    return sales

def print_sales(sales, print_enabled):
    if print_enabled:
        sales.info()
        print(sales.isnull().sum())
        print(sales["Global_Sales"].describe())
        print(sales["NA_Sales"].describe())
        print(sales["EU_Sales"].describe())
        print(sales["JP_Sales"].describe())
        
        sns.set_theme(style="whitegrid")
        boxGS = sns.boxplot(x=sales["Global_Sales"])
        plt.show()
        boxNAS = sns.boxplot(x=sales["NA_Sales"])
        plt.show()
        boxEUS = sns.boxplot(x=sales["EU_Sales"])
        plt.show()
        boxJPS = sns.boxplot(x=sales["JP_Sales"])
        plt.show()

######  CRITIC TABLE  ######

def process_critic(engine, enable_print = False):
    critic.dropna(subset = ['Critic_Score', 'Critic_Count', 'User_Score', 'User_Count'], inplace=True)
    critic.to_csv('gameCritic.csv')
    print_critic(critic, enable_print)
    insert_db(critic, "Critic", engine)
    return critic

def print_critic(critic, print_enabled):
    if print_enabled:
        critic.info()
        print(critic.isnull().sum())
        print(critic['Critic_Score'].describe())
        print(critic['Critic_Count'].describe())
        print(critic['User_Score'].describe())
        print(critic['User_Count'].describe())

        sns.displot(critic, x="Critic_Score")
        plt.show()
        sns.displot(critic, x="User_Score")
        plt.show()

######  ESPORT DATASET  ######

def process_esport_csv(engine, enable_print = False):
    esportDf = pd.read_csv(esportNew, encoding="utf-8")
    esportDf = sanitize_esport(esportDf)
    esportDf.to_csv('esportDfNew.csv')
    print_esport(esportDf, enable_print)
    insert_db(esportDf, "Esport", engine)
    return esportDf

def print_esport(esportDf, print_enabled):
    if print_enabled:
        print(esportDf['ReleaseDate'].describe())
        print(esportDf['Game'].describe())
        print(esportDf['Genre'].describe())
        print(esportDf['TotalEarnings'].describe())
        print(esportDf['OnlineEarnings'].describe())
        print(esportDf['TotalTournaments'].describe())
        esportDf.info()
        print(esportDf.isnull().sum())
        print(len(esportDf.Name.unique()))

def sanitize_esport(esportDf):
    esportDf = esportDf.loc[:, ['ID','Game','ReleaseDate','Genre','TotalEarnings','OnlineEarnings','TotalPlayers','TotalTournaments']]
    esportDf = esportDf.set_index('ID')
    esportDf = esportDf.rename(columns={'Game': 'Name'}) 
    esportDf.to_csv('esportDfNew.csv')
    return esportDf

######  HISTORICAL ESPORT DATASET ######

def process_historical_esport_csv(engine, enable_print = False):
    HistoricalEsportDf = pd.read_csv(HistoricalEsportNew, encoding="utf-8")
    HistoricalEsportDf = sanitize_historical(HistoricalEsportDf)
    HistoricalEsportDf.to_csv('HistoricalEsportNew.csv')
    print_historical(HistoricalEsportDf, enable_print)
    insert_db(HistoricalEsportDf, "HistoricalEsport", engine)
    return HistoricalEsportDf

def print_historical(HistoricalEsportDf, print_enabled):
    if print_enabled:
        print(HistoricalEsportDf['Game'].describe())
        print(HistoricalEsportDf['Earnings'].describe())
        print(HistoricalEsportDf['Players'].describe())
        print(HistoricalEsportDf['Tournaments'].describe())

def sanitize_historical(HistoricalEsportDf):
    HistoricalEsportDf = HistoricalEsportDf.loc[:, ['ID','Date','Game','Earnings','Players','Tournaments']]
    HistoricalEsportDf = HistoricalEsportDf.set_index('ID')
    HistoricalEsportDf['Date'] = pd.to_datetime(HistoricalEsportDf['Date'])
    return HistoricalEsportDf

########  MURDERS DATASET  ######

def process_murders_csv(engine, enable_print = False):
    murdersDf = pd.read_csv(murders, sep=';',error_bad_lines=False, dtype=object)
    murdersDf = sanitize_murders(murdersDf)
    murdersDf.to_csv('Murders_clean.csv')
    print_murders(murdersDf, enable_print)
    insert_db(murdersDf, "Murders", engine)
    return murdersDf

def print_murders(murdersDf, print_enabled):
    if print_enabled:
        murdersDf.info()
        print(murdersDf.isnull().sum())
        print(murdersDf.Weapon.unique())
        print(murdersDf.State.unique())
        print(murdersDf.isna().sum())
        print(murdersDf['Year'].describe())
        print(murdersDf['Perpetrator Age'].describe())
        print(murdersDf[murdersDf['Perpetrator Age'] == 1])

def sanitize_murders(murdersDf):
    murdersDf = murdersDf.set_index('Record ID')
    murdersDf = murdersDf.loc[:, ['State', 'Year', 'Month', 'Perpetrator Age', 'Weapon']]
    murdersDf['Perpetrator Age'] = murdersDf['Perpetrator Age'].replace(' ', np.nan)
    murdersDf['Perpetrator Age'] = murdersDf['Perpetrator Age'].replace(0, np.nan)
    murdersDf['Perpetrator Age'] = murdersDf['Perpetrator Age'].replace('0', np.nan)
    med2 = murdersDf['Perpetrator Age'].median()
    murdersDf['Perpetrator Age'] = murdersDf['Perpetrator Age'].fillna(med2)
    murdersDf['Perpetrator Age'] = murdersDf['Perpetrator Age'].astype(np.int64)
    murdersDf['Year'] = murdersDf['Year'].astype(np.int64)
    murdersDf = murdersDf[murdersDf['Perpetrator Age'] >= 4]
    return murdersDf

######  CORRELATION COEFFICIENT  ######

def correlation_coefficients(enable_print = False):
    dataMurders = murdersDf.loc[:, ['Year', 'State']]
    dataMurders = dataMurders.groupby('Year').count()
    corCoef1 = corCoefMurdersGames(dataMurders, videoGames)
    corCoef2 = corCoefMurdersSales(dataMurders, videoGames, sales)
    print_coroef(corCoef1, corCoef2, enable_print)

def print_coroef(corCoef1, corCoef2, print_enabled):
    if print_enabled:
        print(f"\n{corCoef1}\n\n{corCoef2}\n")

def corCoefMurdersGames(dataMurders, videoGames):
    dataGames = videoGames.loc[:, ['Name', 'Year_of_Release']]
    dataGames = dataGames.groupby('Year_of_Release').count()
    corDataGamesMurders = dataGames.merge(dataMurders, left_index=True, right_index=True)
    corDataGamesMurders = corDataGamesMurders.rename(columns={"Name": "Games", "State": "Murders"})
    return corDataGamesMurders.corr()

def corCoefMurdersSales(dataMurders, videoGames, sales):
    dataSales = videoGames.merge(sales, left_index=True, right_index=True)
    dataSales = dataSales.loc[:, ['NA_Sales', 'Year_of_Release']]
    dataSales = dataSales.groupby('Year_of_Release').sum()
    corDataSalesMurders = dataSales.merge(dataMurders, left_index=True, right_index=True)
    corDataSalesMurders = corDataSalesMurders.rename(columns={"State": "Murders"})
    return corDataSalesMurders.corr()

videogames_clean_csv(CSVname, CSVname_clean)

critic, sales, videoGames = transform_videogames_dataset(CSVname_clean)

videoGames = process_videogames(engine, enable_print = False)

sales = process_sales(engine, enable_print = False)

critic = process_critic(engine, enable_print = False)

addID_to_table(esport, esportNew)

addID_to_table(HistoricalEsport, HistoricalEsportNew)

esportDF = process_esport_csv(engine, enable_print = False)

HistoricalEsportDf = process_historical_esport_csv(engine, enable_print = False)

murdersDf = process_murders_csv(engine, enable_print = False)

correlation_coefficients(enable_print = True)