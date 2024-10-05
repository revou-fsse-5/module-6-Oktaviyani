from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data structures
animals = []
employees = []

# POST endpoint to add multiple new animals
@app.route('/animals', methods=['POST'])
def add_animals():
    data = request.get_json()
    if not data or not isinstance(data, list):
        return jsonify({"error": "Invalid input, must be a list of animals"}), 400

    added_animals = []
    for animal in data:
        if 'species' not in animal:
            return jsonify({"error": "Each animal must have a species"}), 400

        animal_id = len(animals) + 1
        animal['id'] = animal_id
        animals.append(animal)
        added_animals.append(animal)

    return jsonify(added_animals), 201  # Return the added animals with a 201 status code

# GET endpoint to retrieve all animals
@app.route('/animals', methods=['GET'])
def get_animals():
    return jsonify(animals)

# GET endpoint to retrieve a specific animal by id
@app.route('/animals/<int:id>', methods=['GET'])
def get_animal(id):
    animal = next((animal for animal in animals if animal['id'] == id), None)
    if animal is None:
        return jsonify({"error": "Animal not found"}), 404
    return jsonify(animal)

# PUT endpoint to update multiple animals by id
@app.route('/animals', methods=['PUT'])
def update_animals():
    data = request.get_json()
    if not data or not isinstance(data, list):
        return jsonify({"error": "Invalid input, must be a list of animals"}), 400

    updated_animals = []
    for animal in data:
        animal_id = animal.get('id')
        existing_animal = next((a for a in animals if a['id'] == animal_id), None)
        if existing_animal is None:
            return jsonify({"error": f"Animal with id {animal_id} not found"}), 404

        existing_animal.update(animal)
        updated_animals.append(existing_animal)

    return jsonify(updated_animals)

# DELETE endpoint to delete multiple animals by id
@app.route('/animals', methods=['DELETE'])
def delete_animals():
    ids = request.get_json()
    if not ids or not isinstance(ids, list):
        return jsonify({"error": "Invalid input, must be a list of ids"}), 400

    global animals
    animals = [animal for animal in animals if animal['id'] not in ids]
    return jsonify({"message": "Animals deleted successfully"}), 204

# Sample endpoints for employee management (similar structure)
@app.route('/employees', methods=['POST'])
def add_employees():
    data = request.get_json()
    if not data or not isinstance(data, list):
        return jsonify({"error": "Invalid input, must be a list of employees"}), 400

    added_employees = []
    for employee in data:
        if 'name' not in employee:
            return jsonify({"error": "Each employee must have a name"}), 400

        employee_id = len(employees) + 1
        employee['id'] = employee_id
        employees.append(employee)
        added_employees.append(employee)

    return jsonify(added_employees), 201

# Similar GET, PUT, DELETE endpoints for employees...

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
