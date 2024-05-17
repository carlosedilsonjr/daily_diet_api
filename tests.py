import pytest
import requests

BASE_URL = 'http://127.0.0.1:5000'
meals = []

def test_create_meal_without_name():
    new_meal = {
        'description': 'Stroganoff',
        'datetime': '16/05/2024 18:00:00'
    }
    response = requests.post(f'{BASE_URL}/meals', json=new_meal)
    assert response.status_code == 400
    response_json = response.json()
    assert 'error' in response_json
    assert response_json['error'] == 'payload incorrect'

def test_list_all_meals_when_empty():
    response = requests.get(f'{BASE_URL}/meals')
    assert response.status_code == 200
    response_json = response.json()
    assert 'meals' in response_json
    assert 'total_meals' in response_json
    assert response_json['meals'] == []
    assert response_json['total_meals'] == 0

def test_list_one_meal_that_not_exists():
    response = requests.get(f'{BASE_URL}/meals/1')
    assert response.status_code == 404
    response_json = response.json()
    assert 'message' in response_json
    assert response_json['message'] == 'Not Found'

def test_update_meal_that_not_exists():
    payload = {
        'name': 'Updated Meal',
        'description': 'Bread with cheese',
        'datetime': '17/05/2024 18:00:00',
        'diet': True
    }
    response = requests.put(f'{BASE_URL}/meals/1', json=payload)
    assert response.status_code == 404
    response_json = response.json()
    assert 'message' in response_json
    assert response_json['message'] == 'Not Found'

def test_delete_meal_that_not_exists():
    response = requests.delete(f'{BASE_URL}/meals/1')
    assert response.status_code == 404
    response_json = response.json()
    assert 'message' in response_json
    assert response_json['message'] == 'Not Found'

def test_create_meal():
    new_meal = {
        'name': 'My Meal',
        'description': 'Stroganoff',
        'datetime': '16/05/2024 18:00:00'
    }
    response = requests.post(f'{BASE_URL}/meals', json=new_meal)
    assert response.status_code == 200
    response_json = response.json()
    assert 'name' in response_json
    assert 'description' in response_json
    assert 'datetime' in response_json
    assert 'diet' in response_json
    assert new_meal['name'] in response_json['name']
    assert new_meal['description'] in response_json['description']
    assert new_meal['datetime'] in response_json['datetime']
    assert response_json['diet'] == False
    meals.append(response_json)

def test_list_all_meals():
    response = requests.get(f'{BASE_URL}/meals')
    assert response.status_code == 200
    response_json = response.json()
    assert 'meals' in response_json
    assert 'total_meals' in response_json
    assert response_json['meals'] == meals
    assert response_json['total_meals'] == len(meals)

def test_list_one_meal():
    meal_id = meals[0]['id']
    response = requests.get(f'{BASE_URL}/meals/{meal_id}')
    assert response.status_code == 200
    response_json = response.json()
    assert 'name' in response_json
    assert 'description' in response_json
    assert 'datetime' in response_json
    assert 'diet' in response_json
    assert meals[0]['name'] in response_json['name']
    assert meals[0]['description'] in response_json['description']
    assert meals[0]['datetime'] in response_json['datetime']
    assert response_json['diet'] == False

def test_update_meal():
    meal_id = meals[0]['id']
    payload = {
        'name': 'Updated Meal',
        'description': 'Bread with cheese',
        'datetime': '17/05/2024 18:00:00',
        'diet': True
    }
    response = requests.put(f'{BASE_URL}/meals/{meal_id}', json=payload)
    assert response.status_code == 200
    response_json = response.json()
    assert 'name' in response_json
    assert 'description' in response_json
    assert 'datetime' in response_json
    assert 'diet' in response_json
    assert payload['name'] in response_json['name']
    assert payload['description'] in response_json['description']
    assert payload['datetime'] in response_json['datetime']
    assert response_json['diet'] == True
    meals.remove(meals[0])
    meals.append(response_json)

def test_delete_meal():
    meal_id = meals[0]['id']
    response = requests.delete(f'{BASE_URL}/meals/{meal_id}')
    assert response.status_code == 200
    response_json = response.json()
    assert 'name' in response_json
    assert 'description' in response_json
    assert 'datetime' in response_json
    assert 'diet' in response_json
    assert meals[0]['name'] in response_json['name']
    assert meals[0]['description'] in response_json['description']
    assert meals[0]['datetime'] in response_json['datetime']
    assert response_json['diet'] == True
    test_list_all_meals_when_empty()