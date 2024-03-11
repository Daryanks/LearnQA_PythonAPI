
import pytest
import json
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure

@allure.feature("LearnQA")
@allure.epic("Create user cases")
class TestCreateUser(BaseCase):
    params = ['password', 'username', 'firstName', 'lastName', 'email']

    @allure.description("This test create user with incorrect email without @")
    def test_create_user_with_incorrect_email(self):
        email = 'dkarazanova.examle.com'
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format", f'Unexpected content {response.content}'

    @allure.description("This test create user with short name")
    def test_create_user_with_short_name(self):
        username = 'l'
        data = {
            'password': '123',
            'username': username,
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': 'dkarazanova@examle.com'
        }

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert json.loads(response.content.decode("utf-8"))['error'] == f"The value of 'username' field is too short", f'Unexpected content {response.content}'

    @allure.description("This test create user with long name")
    def test_create_user_with_long_name(self):
        username = ''
        for i in range(0, 255, 1):
             username = username + 'l'

        data = {
            'password': '123',
            'username': username,
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': 'dkarazanova@examle.com'
        }

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"The value of 'username' field is too long", f'Unexpected content {response.content}'

    @allure.description("This test create user without one fields")
    @pytest.mark.parametrize('params', params)
    def test_create_user_without_one_field(self, params):
        allure.dynamic.parameter('params', '{params}')
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': 'dkarazanova@examle.com'
        }

        del data[params]
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"The following required params are missed: {params}", f'Unexpected content {response.content}'

