from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)


DB_FILE = 'db.json'

@app.route('/')
def home():
    return jsonify({"message": "Welcome to Zoo Management API!"}), 200


def load_data():
    if not os.path.exists(DB_FILE):
        return {"employees": [], "animals": []}  
    with open(DB_FILE, 'r') as file:
        try:
            content = file.read().strip()
            if not content:  
                return {"employees": [], "animals": []}
            return json.loads(content)  
        except json.JSONDecodeError:
            return {"employees": [], "animals": []}  


def save_data(data):
    with open(DB_FILE, 'w') as file:
        json.dump(data, file, indent=4)  

# ========================= Employees API =========================


@app.route('/employees', methods=['POST'])
def add_employees():
    data = request.get_json()
    if not data or not isinstance(data, list):
        return jsonify({"error": "Invalid input, must be a list of employees"}), 400

   
    db = load_data()
    employees = db.get('employees', [])

    added_employees = []
    for employee in data:
        if 'name' not in employee or 'position' not in employee:
            return jsonify({"error": "Each employee must have a name and position"}), 400

        employee_id = len(employees) + 1
        employee['id'] = employee_id
        employees.append(employee)
        added_employees.append(employee)

   
    db['employees'] = employees
    save_data(db)

    return jsonify(added_employees), 201 


@app.route('/employees', methods=['GET'])
def get_employees():
    db = load_data()
    return jsonify(db.get('employees', []))


@app.route('/employees/<int:id>', methods=['GET'])
def get_employee(id):
    db = load_data()
    employees = db.get('employees', [])
    
    employee = next((emp for emp in employees if emp['id'] == id), None)
    if employee is None:
        return jsonify({"error": "Employee not found"}), 404
    return jsonify(employee)


@app.route('/employees', methods=['PUT'])
def update_employees():
    data = request.get_json()
    if not data or not isinstance(data, list):
        return jsonify({"error": "Invalid input, must be a list of employees"}), 400

    db = load_data()
    employees = db.get('employees', [])

    updated_employees = []
    for employee in data:
        employee_id = employee.get('id')
        existing_employee = next((emp for emp in employees if emp['id'] == employee_id), None)
        if existing_employee is None:
            return jsonify({"error": f"Employee with id {employee_id} not found"}), 404

        existing_employee.update(employee)
        updated_employees.append(existing_employee)


    db['employees'] = employees
    save_data(db)

    return jsonify(updated_employees)


@app.route('/employees', methods=['DELETE'])
def delete_employees():
    ids = request.get_json()
    if not ids or not isinstance(ids, list):
        return jsonify({"error": "Invalid input, must be a list of ids"}), 400

    db = load_data()
    employees = db.get('employees', [])


    employees = [emp for emp in employees if emp['id'] not in ids]


    db['employees'] = employees
    save_data(db)

    return jsonify({"message": "Employees deleted successfully"}), 204

# ========================= Animals API =========================


@app.route('/animals', methods=['POST'])
def add_animals():
    data = request.get_json()
    if not data or not isinstance(data, list):
        return jsonify({"error": "Invalid input, must be a list of animals"}), 400

    db = load_data()
    animals = db.get('animals', [])

    added_animals = []
    for animal in data:
        if 'species' not in animal or 'name' not in animal or 'age' not in animal:
            return jsonify({"error": "Each animal must have a species, name, and age"}), 400

        animal_id = len(animals) + 1
        animal['id'] = animal_id
        animals.append(animal)
        added_animals.append(animal)


    db['animals'] = animals
    save_data(db)

    return jsonify(added_animals), 201  

# GET endpoint to retrieve all animals
@app.route('/animals', methods=['GET'])
def get_animals():
    db = load_data()
    return jsonify(db.get('animals', []))


@app.route('/animals/<int:id>', methods=['GET'])
def get_animal(id):
    db = load_data()
    animals = db.get('animals', [])
    
    animal = next((ani for ani in animals if ani['id'] == id), None)
    if animal is None:
        return jsonify({"error": "Animal not found"}), 404
    return jsonify(animal)


@app.route('/animals', methods=['PUT'])
def update_animals():
    data = request.get_json()
    if not data or not isinstance(data, list):
        return jsonify({"error": "Invalid input, must be a list of animals"}), 400

    db = load_data()
    animals = db.get('animals', [])

    updated_animals = []
    for animal in data:
        animal_id = animal.get('id')
        existing_animal = next((ani for ani in animals if ani['id'] == animal_id), None)
        if existing_animal is None:
            return jsonify({"error": f"Animal with id {animal_id} not found"}), 404

        existing_animal.update(animal)
        updated_animals.append(existing_animal)


    db['animals'] = animals
    save_data(db)

    return jsonify(updated_animals)


@app.route('/animals', methods=['DELETE'])
def delete_animals():
    ids = request.get_json()
    if not ids or not isinstance(ids, list):
        return jsonify({"error": "Invalid input, must be a list of ids"}), 400

    db = load_data()
    animals = db.get('animals', [])


    animals = [ani for ani in animals if ani['id'] not in ids]


    db['animals'] = animals
    save_data(db)

    return jsonify({"message": "Animals deleted successfully"}), 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
