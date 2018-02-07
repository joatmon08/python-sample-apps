import pytest
import requests
import json

url = 'http://localhost:5000'

stars = [{'name': 'hello', 'distance': 100},
        {'name': 'world', 'distance': 200}]
headers = {'Content-Type': 'application/json'}

def test_should_return_sum_of_distance():
    data = json.dumps(stars)
    r = requests.post(url + '/distance', headers = headers, data = data)
    r.raise_for_status()
    assert r.json() == {'result': 300}
