from flask import Flask, jsonify, request
from models.meal import Meal
from database import db

app = Flask(__name__)
app.config['SECRET_KEY'] = "change for a enviroment password"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
db.init_app(app)

@app.route('/meals', methods=['POST'])
def create_meal():
    data = request.get_json()

    if not 'name' in data:
        return jsonify({'error': 'payload incorrect'}), 400

    new_meal = Meal(name=data['name'], description=data.get('description'), datetime=data.get('datetime'))
    db.session.add(new_meal)
    db.session.commit()
    return jsonify(new_meal.to_dict())

@app.route('/meals', methods=['GET'])
def list_all_meals():
    meals = Meal.query.all()
    list_meals = [meal.to_dict() for meal in meals]
    output = {
        'meals': list_meals,
        'total_meals': len(list_meals)
    }
 
    return jsonify(output)

@app.route('/meals/<int:id>', methods=['GET'])
def list_one_meal(id):
    meal = Meal.query.get(id)
    
    if not meal:
        return jsonify({'message': 'Not Found'}), 404
    
    return jsonify(meal.to_dict()), 200

@app.route('/meals/<int:id>', methods=['PUT'])
def update_meal(id):
    meal = Meal.query.get(id)

    if not meal:
        return jsonify({'message': 'Not Found'}), 404 
    
    data = request.get_json()
    if data['name']:
        meal.name = data['name']
    if data['description']:
        meal.description = data['description']
    if data['datetime']:
        meal.datetime = data['datetime']
    if data['diet']:
        meal.diet = data['diet']
    db.session.commit()

    return jsonify(meal.to_dict()), 200

@app.route('/meals/<int:id>', methods=['DELETE'])
def delete_meal(id):
    meal = Meal.query.get(id)
    
    if not meal:
        return jsonify({'message': 'Not Found'}), 404

    db.session.delete(meal)
    db.session.commit()
    return jsonify(meal.to_dict()), 200

if __name__ == '__main__':
    app.run(debug=True)