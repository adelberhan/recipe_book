from flask import Flask, request, jsonify, send_from_directory
import os
import json
from recipe import Recipe
from user import User

app = Flask(__name__, static_folder="static")

# Ensure data directory exists
os.makedirs("data", exist_ok=True)
if not os.path.exists("data/recipes.json"):
    with open("data/recipes.json", "w") as f:
        json.dump([], f)
if not os.path.exists("data/users.json"):
    with open("data/users.json", "w") as f:
        json.dump([], f)

@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')

@app.route('/<path:path>')
def send_template(path):
    return send_from_directory('templates', path)

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"success": False, "message": "Username and password are required"}), 400
    
    existing_user = User.get_by_username(username)
    if existing_user:
        return jsonify({"success": False, "message": "Username already exists"}), 400
    
    user = User(username=username, password=password)
    user.save()
    
    return jsonify({"success": True, "user": {"username": user.username, "id": user.id}}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"success": False, "message": "Username and password are required"}), 400
    
    user = User.get_by_username(username)
    if not user or not user.verify_password(password):
        return jsonify({"success": False, "message": "Invalid username or password"}), 401
    
    return jsonify({
        "success": True,
        "user": {
            "username": user.username,
            "id": user.id
        }
    })

@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    recipes = Recipe.get_all()
    return jsonify([recipe.to_dict() for recipe in recipes])

@app.route('/api/recipes/<recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    recipe = Recipe.get_by_id(recipe_id)
    if not recipe:
        return jsonify({"success": False, "message": "Recipe not found"}), 404
    return jsonify(recipe.to_dict())

@app.route('/api/recipes', methods=['POST'])
def create_recipe():
    data = request.get_json()
    
    required_fields = ['name', 'ingredients', 'instructions', 'prep_time', 'cook_time', 'created_by']
    for field in required_fields:
        if field not in data:
            return jsonify({"success": False, "message": f"Missing required field: {field}"}), 400
    
    recipe = Recipe(
        name=data['name'],
        ingredients=data['ingredients'],
        instructions=data['instructions'],
        prep_time=data['prep_time'],
        cook_time=data['cook_time'],
        image_url=data.get('image_url'),
        created_by=data['created_by']
    )
    recipe.save()
    
    return jsonify({"success": True, "recipe": recipe.to_dict()}), 201

@app.route('/api/recipes/<recipe_id>', methods=['PUT'])
def update_recipe(recipe_id):
    data = request.get_json()
    recipe = Recipe.get_by_id(recipe_id)
    
    if not recipe:
        return jsonify({"success": False, "message": "Recipe not found"}), 404
    
    recipe.name = data.get('name', recipe.name)
    recipe.ingredients = data.get('ingredients', recipe.ingredients)
    recipe.instructions = data.get('instructions', recipe.instructions)
    recipe.prep_time = data.get('prep_time', recipe.prep_time)
    recipe.cook_time = data.get('cook_time', recipe.cook_time)
    recipe.image_url = data.get('image_url', recipe.image_url)
    
    recipe.update()
    
    return jsonify({"success": True, "recipe": recipe.to_dict()})

@app.route('/api/recipes/<recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    recipe = Recipe.get_by_id(recipe_id)
    
    if not recipe:
        return jsonify({"success": False, "message": "Recipe not found"}), 404
    
    recipe.delete()
    
    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(debug=True)