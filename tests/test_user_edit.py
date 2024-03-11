
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import json
import allure

@allure.feature("LearnQA")
@allure.epic("Edit user cases")
class TestUserEdit(BaseCase):

    @allure.description("This test create user and successful edit his firstName")
    def test_edit_created_user(self):


        register_data = self.prepare_registration_date()
        response = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response,"id")


        login_data = {
            'email': email,
            'password': password
        }
        response1 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")


        new_name = "Change name"

        response2 = MyRequests.put(f"/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                 data={"firstName": new_name}
                                 )
        Assertions.assert_code_status(response2,200)


        response3 = MyRequests.get(f"/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                 )
        Assertions.assert_json_value_by_name(
            response3,
            "firstName",
            "Change name",
            "Wrong name user after edit"
        )

    @allure.description("This test create user and edit his firstName for short value")
    def test_edit_user_short_name(self):


        register_data = self.prepare_registration_date()
        response = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response, "id")


        login_data = {
            'email': email,
            'password': password
        }
        response1 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")


        new_name = "l"

        response2 = MyRequests.put(f"/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                 data={"firstName": new_name}
                                 )

        Assertions.assert_code_status(response2, 400)
        assert json.loads(response2.content.decode("utf-8"))['error'] == f"The value for field `firstName` is too short", f'Unexpected content {response.content}'

    @allure.description("This test create user and edit his email for incorrect")
    def test_edit_user_incorrect_email(self):


        register_data = self.prepare_registration_date()
        response = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response, "id")


        login_data = {
            'email': email,
            'password': password
        }
        response1 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")



        email = "learnqa.example.com"

        response2 = MyRequests.put(f"/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                 data={"email": email}
                                 )

        Assertions.assert_code_status(response2, 400)
        assert json.loads(response2.content.decode("utf-8"))['error'] == f"Invalid email format", f'Unexpected content {response.content}'

    @allure.description("This test create user and edit his firstName without authorize")
    def test_edit_created_user_no_auth(self):


        register_data = self.prepare_registration_date()
        response = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

        user_id = self.get_json_value(response, "id")


        new_name = "Change name"
        response1 = MyRequests.put(f"/user/{user_id}",
                                 headers={"x-csrf-token": None},
                                 cookies={"auth_sid":None},
                                 data={"firstName": new_name}
                                 )

        Assertions.assert_code_status(response1, 400)

    @allure.description("This test create user and edit his firstName with authorize another user id=2")
    def test_edit_auth_another_user(self):

        register_data = self.prepare_registration_date()
        response = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")


        user_id = self.get_json_value(response,"id")


        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")



        new_name = "Dasha"
        response2 = MyRequests.put(f"/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                 data={"firstName": new_name}
                                 )

        Assertions.assert_code_status(response2, 400)