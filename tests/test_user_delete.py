
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import json
import allure

@allure.feature("LearnQA")
@allure.epic("Delete user cases")
class TestUserDelete(BaseCase):

    @allure.description("This test delete user with id=2")
    def test_delete_user_2(self):
        # Login
        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response, "auth_sid")
        token = self.get_header(response, "x-csrf-token")
        user_id = self.get_json_value(response, "user_id")

        # Delete User(id=2)
        response1 = MyRequests.delete(f"/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid}
                                 )
        Assertions.assert_code_status(response1, 400)
        assert json.loads(response1.content.decode("utf-8"))[
                   'error'] == f"Please, do not delete test users with ID 1, 2, 3, 4 or 5.", f'Unexpected content {response.content}'

    @allure.description("This test successful delete new user")
    def test_user_delete_successful(self):
        # Register
        register_data = self.prepare_registration_date()
        response = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response, "id")

        # Login
        login_data = {
                'email': email,
                'password': password
        }
        response1 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        # Delete user
        response2 = MyRequests.delete(f"/user/{user_id}",
                                        headers={"x-csrf-token": token},
                                        cookies={"auth_sid": auth_sid}
                                        )
        Assertions.assert_code_status(response2, 200)
        assert json.loads(response2.content.decode("utf-8"))['success'] == f"!", f'Unexpected content {response.content}'

        # Get User detailes
        response3 = MyRequests.get(f"/user/{user_id}",
                                    headers={"x-csrf-token": token},
                                    cookies={"auth_sid": auth_sid}
                                    )
        Assertions.assert_code_status(response3, 404)
        assert response3.content.decode("utf-8") == f"User not found", f'Unexpected content {response.content}'

    @allure.description("This test delete user with authorize another used id=2")
    def test_user_delete_auth_another_user(self):
        # Register
        register_data = self.prepare_registration_date()
        response = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

        user_id = self.get_json_value(response, "id")

        # Login
        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        # Delete User with Auth another user(id=2)
        response2 = MyRequests.delete(f"/user/{user_id}",
                                    headers={"x-csrf-token": token},
                                    cookies={"auth_sid": auth_sid}
                                    )
        Assertions.assert_code_status(response2, 400)
        assert json.loads(response2.content.decode("utf-8"))[
                   'error'] == f"Please, do not delete test users with ID 1, 2, 3, 4 or 5.", f'Unexpected content {response.content}'


