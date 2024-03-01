import requests

class TestCookie:
    def test_cookie(self):
        url = "https://playground.learnqa.ru/api/homework_cookie"
        response = requests.get(url)
        print(response.cookies)

        assert response.cookies.get('HomeWork') == 'hw_value', "Incorrect cookie value"