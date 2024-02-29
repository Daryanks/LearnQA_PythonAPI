import json

import pytest
import requests

class TestUserAgent:

    user_agents = [
        {
            "agent": "Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
            "expected": {'platform': 'Mobile', 'browser': 'No', 'device': 'Android'}
        },
        {
            "agent": 'Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1',
            "expected": {'platform':'Mobile', 'browser': 'Chrome', 'device': 'iOS'}
        },
        {
            "agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
            "expected": {'platform': 'Googlebot', 'browser': 'Unknown', 'device': 'Unknown'}
        },
        {
            "agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0",
            "expected": {'platform': 'Web', 'browser': 'Chrome', 'device': 'No'}
        },
        {
            "agent": "Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
            "expected": {'platform': 'Mobile', 'browser': 'No', 'device': 'iPhone'}
        },
    ]

    @pytest.mark.parametrize('user_agents', user_agents)
    def test_user_agent(self, user_agents):

        url = "https://playground.learnqa.ru/ajax/api/user_agent_check"

        response = requests.get(url,headers={"User-Agent": user_agents['agent']})

        agent_value = json.loads(response.text)
        check_agent_value = {}
        check_agent_value.update(platform=agent_value['platform'], browser=agent_value['browser'], device=agent_value['device'])
        print(check_agent_value)

        assert check_agent_value['platform'] == user_agents['expected']['platform'], "Incorrect value of platform"
        assert check_agent_value['browser'] == user_agents['expected']['browser'], "Incorrect value of browser"
        assert check_agent_value['device'] == user_agents['expected']['device'], "Incorrect value of device"