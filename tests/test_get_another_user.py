import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestGetAnotherUser(BaseCase):
    def test_get_user_details_auth_another_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        response2 = requests.get(f"https://playground.learnqa.ru/api/user/93336",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid}
                                 )

        Assertions.assert_json_has_key(response2, "username")
        Assertions.assert_json_has_no_key(response2, "firstNane")
        Assertions.assert_json_has_no_key(response2, "lastNane")
        Assertions.assert_json_has_no_key(response2, "email")