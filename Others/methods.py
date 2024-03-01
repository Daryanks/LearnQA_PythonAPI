import requests

url = "https://playground.learnqa.ru/ajax/api/compare_query_type"
methods = [requests.get, requests.post, requests.put, requests.delete, requests.head]
params = [None, "GET", "POST", "PUT", "DELETE", "HEAD"]

for method in methods:
    for data in params:
        if data == "GET":
            resp = method(url, params={ "method" : data })
        elif data is not None:
            resp = method(url, data={ "method" : data })
        else:
            resp = method(url)
        print(f"Method: {method}, Data: {data}, Response: {resp.text}")

