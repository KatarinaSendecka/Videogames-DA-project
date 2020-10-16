import pandas as pd

data = pd.read_csv("Video_Games_Sales_as_at_22_Dec_2016.csv", sep=';',error_bad_lines=False)

print(data)
