from flask import Flask, request, jsonify, send_from_directory,render_template, session
import os
import json
from recipe import Recipe
from user import User



app = Flask(__name__, static_folder="static")


app.secret_key = 'adel' 


def get_html(page_name):
    # html_file = open(page_name + ".html")
    with open(f"templates/{page_name}.html" ) as html_file:
        content = html_file.read()
        # content = html_file.close()
    return content

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
    return send_from_directory('templates', 'home.html')

@app.route('/<path:path>')
def send_template(path):
    return send_from_directory('templates', path)


@app.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')


@app.route('/api/register', methods=['GET','POST'])
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

# @app.route('/api/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         # استخدم request.form للحصول على البيانات المرسلة من الـ form
#         username = request.form.get('username')
#         password = request.form.get('password')

#         # التأكد من وجود البيانات المطلوبة
#         if not username or not password:
#             return jsonify({"success": False, "message": "Username and password are required"}), 400

#         # التأكد من عدم وجود مستخدم بنفس الاسم
#         existing_user = User.get_by_username(username)
#         if existing_user:
#             return jsonify({"success": False, "message": "Username already exists"}), 400

#         # إنشاء مستخدم جديد
#         user = User(username=username, password=password)
#         user.save()

#         return jsonify({"success": True, "user": {"username": user.username, "id": user.id}}), 201

#     return "Invalid request method", 405



# @app.route('/add-recipe', methods=['GET'])
# def add_recipe():
#     if 'user_id' not in session:
#         return login_page()
#     return jsonify({"success": False, "message": "User not logged in"}), 401
#     return render_template('add_recipe.html')

@app.route('/add-recipe', methods=['GET'])
def add_recipe():
    if 'user_id' not in session:
        return login_page()  # or redirect(url_for('login_page'))

    return render_template('add_recipe.html')  # only reached if user is logged in



@app.route('/login', methods=['GET','post'])  
def login_page():
    if request.method == 'GET':
        return render_template('login.html') 
    
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"success": False, "message": "Username and password are required"}), 400
    
    user = User.get_by_username(username)
    if not user or not user.verify_password(password):
        return jsonify({"success": False, "message": "Invalid username or password"}), 401
    
    # Save user ID in session
    session['user_id'] = user.id
    
    return jsonify({
        "success": True,
        "user": {
            "username": user.username,
            "id": user.id
        },
            
    })
    


# @app.route('/api/login', methods=['GET','POST'])
# def login():
#     data = request.get_json()
#     username = data.get('username')
#     password = data.get('password')
    
#     if not username or not password:
#         return jsonify({"success": False, "message": "Username and password are required"}), 400
    
#     user = User.get_by_username(username)
#     if not user or not user.verify_password(password):
#         return jsonify({"success": False, "message": "Invalid username or password"}), 401
    
#     return jsonify({
#         "success": True,
#         "user": {
#             "username": user.username,
#             "id": user.id
#         },

#          "redirect_url": "/home"
#     })

@app.route('/logout', methods=['GET'])
def logout():
    # Clear the session
    session.pop('user_id', None)
    return jsonify({"success": True, "message": "Logged out successfully"}), 200


@app.route("/home",methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    recipes = Recipe.get_all()
    return jsonify([recipe.to_dict() for recipe in recipes])

@app.route("/recipes")
def recipes():
    return render_template('recipes.html')

@app.route('/api/recipes/<recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    recipe = Recipe.get_by_id(recipe_id)
    if not recipe:
        return jsonify({"success": False, "message": "Recipe not found"}), 404
    return jsonify(recipe.to_dict())


@app.route("/recipes/<recipe_id>")
def recipe_detail(recipe_id):
    recipe = Recipe.get_by_id(recipe_id)
    if not recipe:
        return jsonify({"success": False, "message": "Recipe not found"}), 404
    return render_template('recipe_detail.html', recipe=recipe.to_dict())

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

# Edit Recipe Page
@app.route('/recipes/edit/<recipe_id>')
def edit_recipe_page(recipe_id):
    recipe = Recipe.get_by_id(recipe_id)
    if not recipe:
        return "Recipe not found", 404
    return render_template("add_recipe.html", recipe_json=recipe.to_dict())


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


# @app.route('/api/recipes/<recipe_id>', methods=['DELETE'])
# def delete_recipe(recipe_id):
#     recipe = Recipe.get_by_id(recipe_id)
    
#     if not recipe:
#         return jsonify({"success": False, "message": "Recipe not found"}), 404
    
#     recipe.delete()
    
#     return jsonify({"success": True})

@app.route('/api/recipes/<recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    if 'user_id' not in session:
        recipe = Recipe.get_by_id(recipe_id)
    
    if not recipe:
        return jsonify({"success": False, "message": "Recipe not found"}), 404
    
    recipe.delete()
    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(debug=True)
    
# CORS(app)