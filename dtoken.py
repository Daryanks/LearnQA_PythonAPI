import requests
import json
import time

url = "https://playground.learnqa.ru/ajax/api/longtime_job"
response = requests.get(url)
data = json.loads(response.text)

response = requests.get(url, params={"token": data['token']})
check_data = json.loads(response.text)
print(check_data['status'])

time.sleep(data['seconds'])

response = requests.get(url, params={"token": data['token']})
data_result = json.loads(response.text)
print(data_result['status'])
if data_result['status'] == 'Job is ready':
     print(data_result['result'])


