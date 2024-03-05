from random import random

import requests
import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestCreateUser:
    params = ['password', 'username', 'firstName', 'lastName', 'email']
    def test_create_user_with_incorrect_email(self):
        email = 'dkarazanova.examle.com'
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format", f'Unexpected content {response.content}'

    def test_create_user_with_short_name(self):
        username = 'l'
        data = {
            'password': '123',
            'username': username,
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': 'dkarazanova@examle.com'
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'username' field is too short", f'Unexpected content {response.content}'

    def test_create_user_with_long_name(self):
        username = ''
        for i in range(0, 255, 1):
             username = username + 'l'
        #print(len(username))
        data = {
            'password': '123',
            'username': username,
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': 'dkarazanova@examle.com'
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"The value of 'username' field is too long", f'Unexpected content {response.content}'

    @pytest.mark.parametrize('params', params)
    def test_create_user_without_one_field(self, params):
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': 'dkarazanova@examle.com'
        }

        del data[params]
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"The following required params are missed: {params}", f'Unexpected content {response.content}'

