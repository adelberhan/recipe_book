from flask import Flask, request, jsonify, render_template, session
import os
import json
from recipe import Recipe
from user import User

app = Flask(__name__, static_folder="static")
app.secret_key = "adel"

# -------------------- Utility Functions --------------------

def get_html(page_name):
    try:
        with open(f"templates/{page_name}") as html_file:
            return html_file.read()
    except FileNotFoundError:
        return "Page not found", 404

# -------------------- Authentication Routes --------------------

@app.route("/register", methods=["GET"])
def register_page():
    if "user_id" in session:
        return recipes()
    return get_html("register.html")

@app.route("/api/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400

        username = data.get("username", "").strip()
        password = data.get("password", "").strip()

        # Validation
        if not username or not password:
            return jsonify(
                {"success": False, "message": "Username and password are required"}
            ), 400

        if len(username) < 3:
            return jsonify(
                {"success": False, "message": "Username must be at least 3 characters"}
            ), 400

        if len(password) < 6:
            return jsonify(
                {"success": False, "message": "Password must be at least 6 characters"}
            ), 400

        # Check if user exists
        if User.get_by_username(username):
            return jsonify({"success": False, "message": "Username already exists"}), 400

        # Create and save user
        new_user = User(username=username, password=password)
        new_user.save()

        return jsonify({
            "success": True,
            "user": {
                "id": new_user.id,
                "username": new_user.username,
                "created_at": new_user.created_at,
            }
        }), 201

    except Exception as e:
        return jsonify(
            {"success": False, "message": "Registration failed", "error": str(e)}
        ), 500

@app.route("/login", methods=["GET", "POST"])
def login_page():
    if "user_id" in session:
        return recipes()
    elif request.method == "GET":
        return get_html("login.html")

    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify(
            {"success": False, "message": "Username and password are required"}
        ), 400

    user = User.get_by_username(username)
    if not user or not user.verify_password(password):
        return jsonify({"success": False, "message": "Invalid username or password"}), 401

    session["user_id"] = user.id
    return jsonify(
        {"success": True, "user": {"username": user.username, "id": user.id}}
    )

@app.route("/logout", methods=["GET"])
def logout():
    session.pop("user_id", None)
    return jsonify({"success": True, "message": "Logged out successfully"}), 200

# -------------------- Recipe Routes --------------------

@app.route("/add-recipe", methods=["GET"])
def add_recipe():
    if "user_id" not in session:
        return login_page()
    return get_html("add_recipe.html")

@app.route("/api/recipes", methods=["GET"])
def get_recipes():
    recipes = Recipe.get_all()
    return jsonify([recipe.to_dict() for recipe in recipes])

@app.route("/api/recipes/<recipe_id>", methods=["GET"])
def get_recipe(recipe_id):
    recipe = Recipe.get_by_id(recipe_id)
    if not recipe:
        return jsonify({"success": False, "message": "Recipe not found"}), 404
    return jsonify(recipe.to_dict())

@app.route("/api/recipes", methods=["POST"])
def create_recipe():
    data = request.get_json()
    required_fields = [
        "name",
        "ingredients",
        "instructions",
        "prep_time",
        "cook_time",
        "created_by",
    ]

    for field in required_fields:
        if field not in data:
            return jsonify(
                {"success": False, "message": f"Missing required field: {field}"}
            ), 400

    recipe = Recipe(
        name=data["name"],
        ingredients=data["ingredients"],
        instructions=data["instructions"],
        prep_time=data["prep_time"],
        cook_time=data["cook_time"],
        image_url=data.get("image_url"),
        created_by=data["created_by"],
    )
    recipe.save()
    return jsonify({"success": True, "recipe": recipe.to_dict()}), 201

@app.route("/api/recipes/<recipe_id>", methods=["PUT"])
def update_recipe(recipe_id):
    data = request.get_json()
    recipe = Recipe.get_by_id(recipe_id)
    if not recipe:
        return jsonify({"success": False, "message": "Recipe not found"}), 404

    recipe.name = data.get("name", recipe.name)
    recipe.ingredients = data.get("ingredients", recipe.ingredients)
    recipe.instructions = data.get("instructions", recipe.instructions)
    recipe.prep_time = data.get("prep_time", recipe.prep_time)
    recipe.cook_time = data.get("cook_time", recipe.cook_time)
    recipe.image_url = data.get("image_url", recipe.image_url)
    recipe.update()
    return jsonify({"success": True, "recipe": recipe.to_dict()})

@app.route("/api/recipes/<recipe_id>", methods=["DELETE"])
def delete_recipe(recipe_id):
    if "user_id" not in session:
        return jsonify({"success": False, "message": "Unauthorized"}), 403

    recipe = Recipe.get_by_id(recipe_id)
    if not recipe:
        return jsonify({"success": False, "message": "Recipe not found"}), 404

    recipe.delete()
    return jsonify({"success": True})

# -------------------- Page Routes --------------------

@app.route("/")
def index():
    return get_html("home.html")

@app.route("/home")
def home():
    return get_html("home.html")

@app.route("/recipes")
def recipes():
    return get_html("recipes.html")

@app.route("/recipes/<recipe_id>")
def recipe_detail(recipe_id):
    recipe = Recipe.get_by_id(recipe_id)
    if not recipe:
        return jsonify({"success": False, "message": "Recipe not found"}), 404
    return get_html("recipe_detail.html")

@app.route("/recipes/edit/<recipe_id>")
def edit_recipe_page(recipe_id):
    recipe = Recipe.get_by_id(recipe_id)
    if not recipe:
        return "Recipe not found", 404
    return render_template("add_recipe.html", recipe_json=recipe.to_dict())

# -------------------- Error Handling --------------------

@app.errorhandler(404)
def page_not_found(e):
    return get_html("404.html"), 404

if __name__ == "__main__":
    # Initialize data files on startup
    os.makedirs("data", exist_ok=True)
    if not os.path.exists("data/recipes.json"):
        with open("data/recipes.json", "w") as f:
            json.dump([], f)
    if not os.path.exists("data/users.txt"):
        with open("data/users.txt", "w") as f:
            f.write("")
    
    app.run(debug=True)
# --------------------------
# App Configuration
# --------------------------
# app = Flask(__name__, static_folder="static")
# app.secret_key = "adel"  # Should be moved to environment variable in production

# --------------------------
# File System Setup
# --------------------------
# DATA_DIR = "data"
# RECIPES_FILE = os.path.join(DATA_DIR, "recipes.json")
# USERS_FILE = os.path.join(DATA_DIR, "users.json")
# USERS_FILE = os.path.join(DATA_DIR, "users.json")


# def initialize_data_files():
#     """Ensure data directory and required files exist"""
#     os.makedirs(DATA_DIR, exist_ok=True)
#     for file_path in [RECIPES_FILE, USERS_FILE]:
#         if not os.path.exists(file_path):
#             with open(file_path, 'w') as f:
#                 json.dump([], f)

# initialize_data_files()


# DATA_DIR = "data"
# RECIPES_FILE = os.path.join(DATA_DIR, "recipes.json")  # Main recipes storage
# USERS_FILE = os.path.join(DATA_DIR, "users.json")  # User data
# USER_RECIPES = os.path.join(DATA_DIR, "user_recipes.txt")  # New tracking file


# def initialize_data_files():
#     """Ensure data directory and required files exist"""
#     os.makedirs(DATA_DIR, exist_ok=True)
#     for file_path in [RECIPES_FILE, USERS_FILE]:
#         if not os.path.exists(file_path):
#             with open(file_path, "w") as f:
#                 json.dump([], f)

#     # Initialize the new tracking file
#     if not os.path.exists(USER_RECIPES):
#         open(USER_RECIPES, "w").close()


# def save_recipe_data(username, recipe_data):
#     """
#     Save recipe to both JSON and text tracking file
#     Returns recipe ID
#     """
#     # Generate unique ID
#     recipe_id = str(uuid4())
#     recipe_data["id"] = recipe_id

#     # 1. Save to main recipes.json (your existing format)
#     with open(RECIPES_FILE, "r+") as f:
#         recipes = json.load(f)
#         recipes.append(recipe_data)
#         f.seek(0)
#         json.dump(recipes, f)

#     # 2. Save simplified info to user_recipes.txt
#     with open(USER_RECIPES, "a") as f:
#         f.write(
#             json.dumps(
#                 {
#                     "recipe_id": recipe_id,
#                     "recipe_name": recipe_data["name"],
#                     "username": username,
#                     # 'created_at': datetime.now().isoformat()
#                 }
#             )
#             + "\n"
#         )

#     return recipe_id


# # --------------------------
# # Helper Functions
# # --------------------------
# def get_html(page_name):
#     """Helper to serve HTML content"""
#     with open(f"templates/{page_name}") as f:
#         return f.read()


# def validate_required_fields(data, required_fields):
#     """Validate presence of required fields in request data"""
#     missing = [field for field in required_fields if field not in data]
#     if missing:
#         return (
#             jsonify(
#                 {
#                     "success": False,
#                     "message": f"Missing required fields: {', '.join(missing)}",
#                 }
#             ),
#             400,
#         )
#     return None


# # --------------------------
# # Authentication Routes
# # --------------------------


# # Route: Displays the registration page
# # Redirects to recipes if already logged in
# @app.route("/register", methods=["GET"])
# def register_page():
#     if "user_id" in session:
#         return recipes()
#     return get_html("register.html")


# # Route: Handles new user registration via API
# # Validates input and creates new user
# @app.route("/api/register", methods=["POST"])
# def register():
#     data = request.get_json()
#     if error := validate_required_fields(data, ["username", "password"]):
#         return error

#     if User.get_by_username(data["username"]):
#         return jsonify({"success": False, "message": "Username exists"}), 400

#     user = User(username=data["username"], password=data["password"])
#     user.save()
#     return (
#         jsonify({"success": True, "user": {"username": user.username, "id": user.id}}),
#         201,
#     )


# # Route: Displays login page or processes login
# # Redirects to recipes if already logged in
# @app.route("/login", methods=["GET", "POST"])
# def login_page():
#     if "user_id" in session:
#         return recipes()

#     if request.method == "GET":
#         return get_html("login.html")

#     data = request.get_json()
#     if error := validate_required_fields(data, ["username", "password"]):
#         return error

#     user = User.get_by_username(data["username"])
#     if not user or not user.verify_password(data["password"]):
#         return jsonify({"success": False, "message": "Invalid credentials"}), 401

#     session["user_id"] = user.id
#     return jsonify({"success": True, "user": user.to_dict()})


# # Route: Handles user logout
# # Clears session and returns success status
# @app.route("/logout", methods=["GET"])
# def logout():
#     session.pop("user_id", None)
#     return jsonify({"success": True, "message": "Logged out"})


# # --------------------------
# # Recipe Routes
# # --------------------------


# # Route: Handles both getting all recipes and creating new ones
# # GET: Returns list of all recipes
# # POST: Creates a new recipe with provided data
# @app.route("/api/recipes", methods=["GET", "POST"])
# def handle_recipes():
#     if request.method == "GET":
#         return jsonify([r.to_dict() for r in Recipe.get_all()])

#     # POST method
#     data = request.get_json()
#     required = [
#         "name",
#         "ingredients",
#         "instructions",
#         "prep_time",
#         "cook_time",
#         "created_by",
#     ]
#     if error := validate_required_fields(data, required):
#         return error

#     # Create and save the recipe (your existing code)
#     recipe = Recipe(
#         name=data["name"],
#         ingredients=data["ingredients"],
#         instructions=data["instructions"],
#         prep_time=data["prep_time"],
#         cook_time=data["cook_time"],
#         image_url=data.get("image_url"),
#         created_by=data["created_by"],
#     )
#     recipe.save()


#     # NEW: Also store in user_recipes.txt
#     with open(USER_RECIPES, "a") as f:
#         f.write(
#             json.dumps(
#                 {
#                     "recipe_id": recipe.id,  # Assuming your Recipe class has an id property
#                     "recipe_name": recipe.name,
#                     "username": data["created_by"],  # Using created_by as the username
#                 }
#             )
#             + "\n"
#         )

#     return (
#         jsonify(
#             {
#                 "success": True,
#                 "recipe": recipe.to_dict(),
#                 "message": "Recipe saved to both systems",
#             }
#         ),
#         201,
#     )

# # Edit Recipe Page
# @app.route("/recipes/edit/<recipe_id>")
# def edit_recipe_page(recipe_id):
#     recipe = Recipe.get_by_id(recipe_id)
#     if not recipe:
#         return "Recipe not found", 404
#     return render_template("add_recipe.html", recipe_json=recipe.to_dict())


# # Route: Handles individual recipe operations
# # GET: Returns single recipe details
# # PUT: Updates existing recipe
# # DELETE: Removes recipe
# @app.route("/api/recipes/<recipe_id>", methods=["GET", "PUT", "DELETE"])
# def handle_recipe(recipe_id):
#     # First check if recipe exists
#     recipe = Recipe.get_by_id(recipe_id)
#     if not recipe:
#         return jsonify({"success": False, "message": "Recipe not found"}), 404

#     if request.method == "GET":
#         return jsonify(recipe.to_dict())

#     elif request.method == "PUT":
#         data = request.get_json()

#         # Validate required fields for update
#         required_fields = ["name", "ingredients", "instructions", "prep_time", "cook_time"]
#         missing = [field for field in required_fields if field not in data]
#         if missing:
#             return jsonify({
#                 "success": False,
#                 "message": f"Missing required fields: {', '.join(missing)}"
#             }), 400

#         # Update the recipe
#         try:
#             recipe.update(data)
#             return jsonify({
#                 "success": True,
#                 "recipe": recipe.to_dict(),
#                 "message": "Recipe updated successfully"
#             })
#         except Exception as e:
#             return jsonify({
#                 "success": False,
#                 "message": f"Error updating recipe: {str(e)}"
#             }), 500

#     elif request.method == "DELETE":
#         try:
#             recipe.delete()
#             return jsonify({
#                 "success": True,
#                 "message": "Recipe deleted successfully"
#             })
#         except Exception as e:
#             return jsonify({
#                 "success": False,
#                 "message": f"Error deleting recipe: {str(e)}"
#             }), 500
# # --------------------------
# # Page Routes
# # --------------------------


# # Route: Main entry point - serves home page
# @app.route("/")
# def index():
#     return send_from_directory("templates", "home.html")


# # Route: Alternative home page route
# @app.route("/home")
# def home():
#     return get_html("home.html")


# # Route: Displays all recipes page
# @app.route("/recipes")
# def recipes():
#     return get_html("recipes.html")


# # Route: Shows detailed view for a single recipe
# @app.route("/recipes/<recipe_id>")
# def recipe_detail(recipe_id):
#     if not Recipe.get_by_id(recipe_id):
#         return jsonify({"success": False, "message": "Not found"}), 404
#     return get_html("recipe_detail.html")


# # Route: Displays recipe creation form
# # Protected route - requires login
# @app.route("/add-recipe")
# def add_recipe_page():
#     if "user_id" not in session:
#         return login_page()
#     return get_html("add_recipe.html")


# # --------------------------
# # Error Handling & Main
# # --------------------------


# # Route: Handles 404 errors with custom page
# @app.errorhandler(404)
# def page_not_found(e):
#     return get_html("404.html"), 404


# if __name__ == "__main__":
#     app.run(debug=True)
