# COB Python script

import requests
import datetime
from datetime import timedelta
import pandas as pd
from pandas import DataFrame, read_csv

print(datetime.datetime.now())
d = timedelta(days = 30)# "30 days of cases"
cutoff = datetime.datetime.now() - d

# Open Data Portal URL with sql query parameter:
url1 = '''
https://data.boston.gov/api/3/action/datastore_search_sql
?sql=SELECT%20*%20from%20%222968e2c0-d479-49ba-a884-4ef523ada3c0%22%20
WHERE%20open_dt%20%3E%20%27
'''

# 30 day cutoff entered into query string
myday = str(cutoff)

url2 = '''
%27%20limit%2030000
'''
# url2 limits records to 30,000

url = url1 + myday + url2

r = requests.get(url)
myjson = r.json()
print(r)

# write selected json data to csv file
with open(r'caseFile.csv', 'a') as f:
    
    try:
        df = pd.read_csv("caseFile.csv")# reads existing records into df

        for i in myjson['result']['records']:
            recExists = df["case_enquiry_id"].isin([i["case_enquiry_id"]])
            # tests if id already present
            if df[recExists].empty:
                print("record did not exist")
                f.write(i["case_enquiry_id"] + "," + i["open_dt"] + "," + i["department"] + "\n")
                print(i["case_enquiry_id"], i["open_dt"])
            else: print("record already exists")


    except:
        # if read_csv fails, first time so read in all records
        f.write("case_enquiry_id" + "," + "open_dt" + "," + "department" + "\n")
        for i in myjson['result']['records']:
            f.write(i["case_enquiry_id"] + "," + i["open_dt"] + "," + i["department"] + "\n")
            print(i["case_enquiry_id"], i["open_dt"])
