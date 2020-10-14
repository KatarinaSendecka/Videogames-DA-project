import pandas as pd

data = pd.read_csv("Video_Games_Sales_as_at_22_Dec_2016.csv", error_bad_lines=False)

data.head()
print(data)
