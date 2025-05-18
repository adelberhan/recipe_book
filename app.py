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
    return get_html("add_recipe.html", recipe_json=recipe.to_dict())

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
    