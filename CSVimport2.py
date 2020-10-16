import csv

subor = open('Video_Games_Sales_as_at_22_Dec_2016.csv', 'r', encoding="utf-8")
reader = csv.reader(subor)
videoData = [row for row in reader]
subor.close()

print(videoData)