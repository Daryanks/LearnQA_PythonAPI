import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect")
for h in response.history:
    print(h.url)
