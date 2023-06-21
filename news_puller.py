from GoogleNews import GoogleNews
from newspaper import Article
import pandas as pd
import time
import re

#media_list = ["Crisis24","Security Magazine","The Washington Post","Tech Monitor ","SecurityWeek","SC Magazine ","Reuters","HomelandSecurity Today","CNBC","US-CERT","The Straits Times","The Record by Recorded Future","Thales","Security Boulevard","International Airport Review","Infosecurity Magazine","ICAO","IATA","HackRead","Dark Reading","Cyber Security Hub","CISA","BBC","AirportTechnology","AirCargo News","ABC News","AOPA","BangkokPost","The Hacker News","CSO Online","Naked Security","Cyber Magazine","Infopoint Security"]

#year_list = [2012, 2013 , 2014 , 2015 , 2016 , 2017 , 2018, 2019 , 2020 , 2021 , 2022, 2023]
#year_list = [2012, 2013 , 2014 , 2015 , 2016]
topic = "airline"

year_list = [2023]

year_list.reverse()

df_filter_list = []

for year in year_list:

    output_filepath = "C:\\Users\\ongye\\Downloads\\cyber news\\April_2023\\" + str(topic) + "_cyber_incident_" + str(year) + ".xlsx"

    start_date = "01/01/" + str(year)
    end_date = "12/31/" + str(year)

    print(str(start_date) + " to " + str(end_date))

    #googlenews = GoogleNews(start='02/01/2020',end='02/28/2020')
    news = GoogleNews(start=start_date,end=end_date)

    search_string = str(topic) + " cyber incident"
    print(search_string)

    news.search(search_string)

    result = news.result()
    page1_df = pd.DataFrame.from_dict(result)

    page_df_list = []
    page_df_list.append(page1_df)

    time.sleep(5)

    for page in range(2,11):

        print("processing page #" + str(page))

        page_result = news.page_at(page)
        page_df = pd.DataFrame.from_dict(page_result)
        page_df_list.append(page_df)

        time.sleep(2)

    appended_df = pd.concat(page_df_list)
    appended_df.drop(columns = ["img"])

    #mask = appended_df.media.apply(lambda x: any(item for item in media_list if item in x))
    #df1 = appended_df[mask]

    df_dedup = appended_df.drop_duplicates('title', keep='last')

    row_list = []
    period_list = []
    for index, row in df_dedup.iterrows():
        regex_string = topic + "|" + "cyber" + "|" + "incident"
        x = re.findall(regex_string, row["desc"])

        #if topic in x:
        if topic in x and "cyber" in x:

            row_list.append(row)
            period_list.append(year)

        else:

            error = "error"

    df_filter = pd.DataFrame(row_list)
    df_filter["period"] = period_list
    df_filter["Country"] = ""
    df_filter["Sector"] = ""
    df_filter["Incident"] = ""
    df_filter["Attack"] = ""
    df_filter["Type"] = ""
    df_filter["Attacker"] = ""
    df_filter["Motivation"] = ""
    df_filter["Impact"] = ""

    df_output = df_filter.drop(['img'], axis=1)
    #df_output = df_filter.reset_index(drop=True).style.set_properties(**{"border": "1px solid black"})
    df_output.to_excel(output_filepath,  index=False)

    time.sleep(5)
#df_final = pd.concat(df_filter_list)

#df_final.to_excel(output_filepath)



"""
#print(len(result))
#result2 = news.page_at(2)
#print(len(result2))
#print(news.total_count())


data = pd.DataFrame.from_dict(result)
data = data.drop(columns=["img"])


for res in result:
  print("Date : " , res["date"])
  print("media : ", res["media"])
  print("Title : ",res["title"])
  print("News : ",res["desc"])
  print("Detailed news : ",res["link"])
"""