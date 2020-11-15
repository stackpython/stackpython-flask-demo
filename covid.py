import requests
import json


# Create a variable to store covid-19 data(Retrieve from API)
url  = requests.get("https://covid19.th-stat.com/api/open/today")
print(url.content.decode("utf-8"))

# Convert bytes into strings
converted_covid_data = url.content.decode("utf-8")
print(type(converted_covid_data))

# json.loads(), json.load(), json.dumps(), json.dump()
# Convert strings into Python dict
covid_obj = json.loads(converted_covid_data)
print(type(covid_obj))

# Save into any file formats you want e.g., .txt, .json
# In this case, save as a JSON file
with open("covid19.json", "w") as json_file:
    data = json.dump(covid_obj, json_file, indent=4)



