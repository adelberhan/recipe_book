Flask Recipe Management Application
=================================

A full-stack recipe management system with user authentication, built with Flask backend and HTML/JavaScript frontend.

Features:
- User registration and login with session management
- Create, view, edit, and delete recipes
- RESTful API for all operations
- JSON data storage
- Responsive frontend

Requirements:
blinker==1.9.0
click==8.1.8
colorama==0.4.6
Flask==3.1.0
itsdangerous==2.2.0
Jinja2==3.1.6
MarkupSafe==3.0.2
Werkzeug==3.1.3

Project Structure:
flask-recipe-app/
├── app.py                # Main Flask application
├── data/
│   ├── recipes.json      # Recipe database
│   └── users.json        # User database
├── static/
│   └── js/               # Frontend JavaScript
│       ├── auth.js       # Authentication handlers
│       ├── recipes.js    # Recipe CRUD operations
│       └── ...
├── templates/            # HTML templates
│   ├── add_recipe.html   # Recipe creation form
│   ├── home.html         # Dashboard
│   ├── login.html        # Login page
│   └── ...
├── recipe.py             # Recipe model
├── user.py               # User model
└── requirements.txt

API Reference
------------

Authentication:
Endpoint          Method  Description                          Request Body
----------------  ------  -----------------------------------  -------------------------------
/register         GET     Registration page                    -
/api/register     POST    Register new user                    {username, password}
/login            GET     Login page                           -
/login            POST    Authenticate user                    {username, password}

Recipes:
Endpoint                Method  Description                          Request Body
----------------------  ------  -----------------------------------  -------------------------------
/recipes               GET     Recipes listing page                 -
/api/recipes           GET     Get all recipes                      -
/api/recipes           POST    Create new recipe                    {name, ingredients, instructions, prep_time, cook_time, created_by}
/recipes/<recipe_id>   GET     Recipe details page                  -
/api/recipes/<id>      GET     Get single recipe                    -
/recipes/edit/<id>     GET     Edit recipe page                     -
/api/recipes/<id>      PUT     Update recipe                        {name, ingredients, instructions, ...}
/api/recipes/<id>      DELETE  Delete recipe                        -

Pages:
Route          Method  Description
-------------  ------  -------------------
/              GET     Home page
/home          GET     User dashboard
/add-recipe    GET     Recipe creation form

Installation:
1. Clone the repository:
   git clone https://github.com/yourusername/flask-recipe-app.git
   cd flask-recipe-app

2. Set up virtual environment:
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate

3. Install dependencies:
   pip install -r requirements.txt

4. Initialize data files:
   mkdir data
   touch data/recipes.json data/users.json
   echo "[]" > data/recipes.json
   echo "[]" > data/users.json

Running the Application:
flask run
Access the application at http://localhost:5000

Configuration:
Create .env file with:
FLASK_APP=app.py
FLASK_ENV=development
