from flask import Flask, jsonify, request
from models.meal import Meal

app = Flask(__name__)

meals = []
meal_id_control = 1

@app.route('/meal', methods=['POST'])
def create_meal():
    global meal_id_control
    data = request.get_json()
    new_meal = Meal(id=meal_id_control, name=data['name'], description=data.get('description'), datetime=data.get('datetime'))
    meals.append(new_meal)
    meal_id_control += 1
    return jsonify(new_meal.to_dict())

@app.route('/meal', methods=['GET'])
def list_all_meals():
    list_meals = [meal.to_dict() for meal in meals]
    output = {
        'list_meals': list_meals,
        'total_meals': len(list_meals)
    }
 
    return jsonify(output)

@app.route('/meal/<int:id>', methods=['GET'])
def list_one_meal(id):
    founded_meal = None
    for meal in meals:
        if meal.id == id:
            founded_meal = meal
            break
    
    if not founded_meal:
        return jsonify({'message': 'Not Found'}), 404
    
    return jsonify(founded_meal.to_dict()), 200

@app.route('/meal/<int:id>', methods=['PUT'])
def update_meal(id):
    founded_meal = None
    for meal in meals:
        if meal.id == id:
            founded_meal = meal

    if not founded_meal:
        return jsonify({'message': 'Not Found'}), 404 
    
    index = meals.index(founded_meal)
    data = request.get_json()
    if data['name']:
        founded_meal.name = data['name']
    if data['description']:
        founded_meal.description = data['description']
    if data['datetime']:
        founded_meal.datetime = data['datetime']
    if data['diet']:
        founded_meal.diet = data['diet']

    meals[index] = founded_meal
    return jsonify(founded_meal.to_dict()), 200

@app.route('/meal/<int:id>', methods=['DELETE'])
def delete_meal(id):
    founded_meal = None
    for meal in meals:
        if meal.id == id:
            founded_meal = meal
            break
    
    if not founded_meal:
        return jsonify({'message': 'Not Found'}), 404

    meals.remove(founded_meal)
    return jsonify(founded_meal.to_dict()), 200

if __name__ == '__main__':
    app.run(debug=True)