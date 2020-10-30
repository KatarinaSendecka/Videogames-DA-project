from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import argparse

# H E L P E R   F U N C T I O N S

def fill_db(engine, tableName, data, long_execution=False):
    if InitDb:
        message = '\nFilling Database table "' + tableName + '".' 
        if long_execution:
            message += ' This may take a few minutes.'

        print(message)
        data.to_sql(tableName, engine)
        print('complete')

    else:
        print('\n' + tableName + ': Filling Database table skipped...')


def print_data(df):
    if PrintData:
        print(df)


def str_replace_char(string, idx, new_char):
    return string[:idx] + new_char + string[idx+1:]


def print_missing_values(name, table):
    print("\n" + name + ": missing value percentages in columns:")
    for col in table.columns:
        pct_missing = np.mean(table[col].isnull())
        print('{} - {}%'.format(col, round(pct_missing*100)))



# V I D E O   G A M E   S A L E S   C S V


def process_video_game_sales_csv():
    df = load_video_game_sales()
    sales = build_sales(df)
    critic = build_critic(df)
    video_games = build_video_games(df)


def load_video_game_sales():
    csv_name = "Video_Games_Sales.csv"
    csv_name_clean = "Video_Games_Sales_clean.csv"

    filecsv = open(csv_name,encoding='utf-8')
    filecsv2 = open(csv_name_clean ,"w",encoding='utf-8')

    header = "ID;" + filecsv.readline()
    filecsv2.write(header)

    id = 1
    for row in filecsv: 
        for i in range(0, len(row)):
            if row[i] == ";" and row[i+1] ==" ":
                row = str_replace_char(row, i, ',')

        row = str(id) + ";" + row
        filecsv2.write(row)
        id += 1
   
    filecsv.close()
    filecsv2.close()

    return pd.read_csv(csv_name_clean, sep=';',error_bad_lines=False)


def build_sales(df):
    sales = df.loc[:, ['ID','NA_Sales', 'EU_Sales', 'JP_Sales', 'Global_Sales']]
    sales = sales.set_index('ID')
    sales.to_csv('GameSales.csv')
    print_data(sales)
    fill_db(engine, "Sales", sales)


def build_critic(df):
    critic = df.loc[:, ['ID','Critic_Score', 'Critic_Count', 'User_Score', 'User_Count']]
    critic = critic.set_index('ID')
    critic.dropna(subset = ['Critic_Score', 'Critic_Count', 'User_Score', 'User_Count'], inplace=True)

    print_missing_values("Critic", critic)

    critic.to_csv('gameCritic.csv')
    print_data(critic)
    fill_db(engine, "Critic", critic)


def build_video_games(df):
    videoGames = df.loc[: ,['ID', 'Name', 'Platform', 'Year_of_Release', 'Genre', 'Publisher', 'Developer']]
    videoGames = videoGames.set_index('ID')

    print_missing_values("VideoGames", videoGames)

    med = videoGames['Year_of_Release'].median()
    videoGames['Year_of_Release'] = videoGames['Year_of_Release'].fillna(med)
    videoGames['Year_of_Release'] = videoGames['Year_of_Release'].astype(np.int64)

    print_missing_values("VideoGames (with median applied)", videoGames)
    videoGames.to_csv('videoGames.csv')
    print_data(videoGames)
    fill_db(engine, "VideoGames", videoGames)



# M U R D E R S   C S V

def process_murders():
    df = load_murders()
    build_murders(df)


def load_murders():
    csv_name = "MurdersUSA.csv"
    return pd.read_csv(csv_name, sep=';', error_bad_lines=False, dtype={'Perpetrator Age': 'string'})


def build_murders(df):
    murders = df.loc[:, ['Record ID','State', 'Year', 'Month', 'Perpetrator Age', 'Weapon']]
    murders = murders.set_index('Record ID')
    murders['Perpetrator Age'] = murders['Perpetrator Age'].replace(' ', np.nan)
    murders['Perpetrator Age'] = murders['Perpetrator Age'].replace(0, np.nan)
    murders['Perpetrator Age'] = murders['Perpetrator Age'].replace('0', np.nan)

    print_missing_values("Murders", murders)

    med = murders['Perpetrator Age'].median()
    murders['Perpetrator Age'] = murders['Perpetrator Age'].fillna(med)
    murders['Perpetrator Age'] = murders['Perpetrator Age'].astype(np.int64)
    murders['Year'] = murders['Year'].astype(np.int64)
    print_missing_values("Murders (with median applied)", murders)

    murders.to_csv('Murders_clean.csv')
    print_data(murders)
    fill_db(engine, "Murders", murders, long_execution=True)



# M A I N

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="CSV conversion script for the Czechitas DA project.")
    parser.add_argument("--init-db", help="If specified, the database will be filled with the CSV data. "
                                          "The database must be running and available on port 5432. "
                                          "Use the ./pgDocker.bat (win) or ./pgDocker.sh (unix) command to start the database. "
                                          "Docker is required to run the db initiation commands.",
                        action="store_true")
    parser.add_argument("--print-data", help="If specified, the table data preview will be printed out.",
                        action="store_true")
    args = parser.parse_args()
    InitDb = args.init_db
    PrintData = args.print_data
    # It iprepoklada sa, ze databaza bezi, pre spustenie v terminali zavolat ./pgDocker.bat
    engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres', echo=False) if InitDb else None

    process_video_game_sales_csv()
    process_murders()
