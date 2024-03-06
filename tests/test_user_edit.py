import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import json

class TestUserEdit(BaseCase):
    def test_edit_created_user(self):

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
            'email': email,
            'password': password
        }
        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        # Edit
        new_name = "Change name"

        response2 = requests.put(f"https://playground.learnqa.ru/api/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                 data={"firstName": new_name}
                                 )
        Assertions.assert_code_status(response2,400)

        # Get User Details
        response3 = requests.get(f"https://playground.learnqa.ru/api/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                 )
        Assertions.assert_json_value_by_name(
            response3,
            "firstName",
            'learnqa',
            "Wrong name user after edit"
        )

    def test_edit_user_short_name(self):
        # Register
        register_data = self.prepare_registration_date()
        response = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response, "id")

        # Login
        login_data = {
            'email': email,
            'password': password
        }
        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        # Edit
        new_name = "l"

        response2 = requests.put(f"https://playground.learnqa.ru/api/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                 data={"firstName": new_name}
                                 )

        Assertions.assert_code_status(response2, 400)
        print(response2.content)
        assert json.loads(response2.content.decode("utf-8"))['error'] == f"Too short value for field firstName", f'Unexpected content {response.content}'

    def test_edit_user_incorrect_email(self):
        # Register
        register_data = self.prepare_registration_date()
        response = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response, "id")

        # Login
        login_data = {
            'email': email,
            'password': password
        }
        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        # Edit
        email = "learnqa.example.com"

        response2 = requests.put(f"https://playground.learnqa.ru/api/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                 data={"email": email}
                                 )

        Assertions.assert_code_status(response2, 400)
        assert response2.content.decode("utf-8") == f"Invalid email format", f'Unexpected content {response.content}'
