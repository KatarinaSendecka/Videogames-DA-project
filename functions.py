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
    
critic, sales, videoGames = import_videogames(CSVname_clean)

def cleaning_sales_table():
    sales.dropna(subset = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Global_Sales'], inplace=True)
    sales.to_csv('GameSales.csv')


def cleaning_critic_table():
    critic.dropna(subset = ['Critic_Score', 'Critic_Count', 'User_Score', 'User_Count'], inplace=True)
    critic.to_csv('gameCritic.csv')

cleaning_critic_table()

