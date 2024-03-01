import requests

class TestHeader:
    def test_header(self):
        url = "https://playground.learnqa.ru/api/homework_header"
        response = requests.get(url)
        print(response.headers)

        assert response.headers.get("x-secret-homework-header") == "Some secret value", "Incorrect secret value in header"