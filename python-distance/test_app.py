import pytest
import requests
import json

stars_url = 'http://localhost:6000'
url = 'http://localhost:5000'

star = {'name': 'world', 'distance': 200}
headers = {'Content-Type': 'application/json'}

def test_should_return_healthy():
    r = requests.get(url + '/health')
    r.raise_for_status()
    assert r.json() == {'stars': 'healthy'}

def test_should_return_sum_of_distance():
    data = json.dumps(star)
    r = requests.post(stars_url + '/star', headers = headers, data = data)
    r = requests.get(url + '/distance')
    r.raise_for_status()
    assert r.json() == {'result': 200}
