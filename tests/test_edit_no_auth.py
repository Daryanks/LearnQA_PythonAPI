import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestEditUserNoAuth(BaseCase):

    def test_edit_created_user(self):

        # Register
        register_data = self.prepare_registration_date()
        response = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

        user_id = self.get_json_value(response, "id")

        new_name = "Change name"
        response1 = requests.put(f"https://playground.learnqa.ru/api/user/{user_id}",
                                 headers={"x-csrf-token": None},
                                 cookies={"auth_sid":None},
                                 data={"firstName": new_name}
                                 )

        Assertions.assert_code_status(response1, 400)

    def test_edit_auth_another_user(self):

        # Register
        register_data = self.prepare_registration_date()
        response = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response,"id")

        # Login
        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        # Edit

        new_name = "Dasha"
        response2 = requests.put(f"https://playground.learnqa.ru/api/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                 data={"firstName": new_name}
                                 )

        Assertions.assert_code_status(response2, 400)



