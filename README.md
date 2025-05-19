# MY FINAL PROJECT: 🥘 Book Application

This is a Flask-based web application that allows users to register, login, and manage their recipe collection. The new feature implemented is a complete user authentication system with session management and localStorage integration for persistent client-side state, along with a robust recipe management system.

---
## Key Features

- **User Authentication**:
  - Secure registration and login system
  - Password hashing using FNV-1a algorithm
  - Session management
- **Recipe Management**:
  - Create, read, update, and delete recipes
  - Automatic ID generation and tracking
  - Timestamp tracking (created_at, updated_at)
- **Data Persistence**:
  - JSON-based storage for recipes
  - Text file storage for users
  - Automatic file and directory creation

---
## Prerequisites

- Flask
- Python 3.x

## 📁 Project Structure

```
Recipe-app/
├── app.py                 # Main Flask application
├── data/
│   ├── recipes.json       # Recipe data
│   └── users.json         # User credentials
├── static/
│   └── js/
│       ├── auth.js        # Authentication logic
│       ├── recipes.js     # Recipe CRUD operations
├── templates/
│   ├── add_recipe.html    # Recipe form
│   ├── home.html          # Dashboard
│   ├── login.html         # Login page
├── recipe.py              # Recipe model
├── user.py                # User model
└── requirements.txt
```

---

## Project Checklist

- [✅] It is available on GitHub.
- [✅] It uses the Flask web framework. (app.py)
- [✅] It uses at least one module from the Python Standard Library other than the random module.
  - Module name: `os` (used in app.py, recipe.py, and user.py for file operations)
  - Module name: `json` (used throughout for data serialization)
- [✅] It contains at least one class written by you that has both properties and methods.
  - File name for the class definition: `recipe.py`
    - Line number(s) for the class definition: 6-79
    - Name of two properties: `name`, `ingredients`
    - Name of two methods: `save()`, `update()`
    - File name and line numbers where the methods are used: `app.py` (lines 81, 226)
- [✅] It makes use of JavaScript in the front end and uses the localStorage of the web browser.
  - File: `add_recipe.js` (line 19)
- [✅] It uses modern JavaScript (for example, let and const rather than var).
  - File: `add_recipe.js` (uses `const` throughout)
- [✅] It makes use of the reading and writing to the same file feature.
- [✅] It contains conditional statements.
  - File name: `recipe.py`
    - Line number(s): 26 (if "user_id" in session:), 70-72 (if data_file.exists())
- [✅] It contains loops.
  - File name: `recipe.py`
    - Line number(s): 191-199 (for recipe_data in data).
- [✅] It lets the user enter a value in a text box at some point.
- [✅] It doesn't generate any error message even if the user enters a wrong input.
- [✅] It is styled using your own CSS.
- [✅] The code follows the code and style conventions as introduced in the course, is fully documented using comments and doesn't contain unused or experimental code.
- [✅] All exercises have been completed as per the requirements and pushed to the respective GitHub repository.

---

## 📡 API Reference

### 🔐 Authentication

| Endpoint       | Method | Description              | Request Body              |
|----------------|--------|--------------------------|---------------------------|
| `/register`    | GET    | Registration page         | –                         |
| `/api/register`| POST   | Register new user         | `{username, password}`    |
| `/login`       | GET    | Login page                | –                         |
| `/login`       | POST   | Authenticate user         | `{username, password}`    |
| `/logout`      | GET    | Logout user               | –                         |

### 📖 Recipes

| Endpoint               | Method | Description                 | Request Body                              |
|------------------------|--------|-----------------------------|-------------------------------------------|
| `/api/recipes`         | GET    | Get all recipes             | –                                         |
| `/api/recipes`         | POST   | Create new recipe           | `{name, ingredients, instructions, ...}`  |
| `/api/recipes/<id>`    | GET    | Get single recipe           | –                                         |
| `/api/recipes/<id>`    | PUT    | Update recipe               | `{name, ingredients, ...}`                |
| `/api/recipes/<id>`    | DELETE | Delete recipe               | –                                         |

### 🗺️ Pages

| Route               | Method | Description               |
|---------------------|--------|---------------------------|
| `/`                 | GET    | Home page                 |
| `/home`             | GET    | Landing page              |
| `/recipes`          | GET    | Recipe listing            |
| `/add-recipe`       | GET    | Recipe creation form      |
| `/recipes/<id>`     | GET    | Recipe details            |
| `/recipes/edit/<id>`| GET    | Recipe edit form          |

---

## How to Run the Project

1. Install requirements: `pip install flask`
2. Run the application: `python app.py`
3. Access in browser at: `http://localhost:5000`


## 🚀 Installation

1. **Clone the repository**  
```bash
git clone https://github.com/yourusername/flask-recipe-app.git  
cd flask-recipe-app
```

2. **Set up a virtual environment**  
```bash
python -m venv venv  
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**  
```bash
pip install -r requirements.txt
```

4. **Initialize data files**  
```bash
mkdir data  
echo "[]" > data/recipes.json  
echo "[]" > data/users.json
```

---

## 🧑‍🍳 Running the Application

```bash
flask run
```

Open your browser at: [http://localhost:5000](http://localhost:5000)

---

## ⚙️ Configuration

Create a `.env` file in the root directory with:

```
FLASK_APP=app.py  
FLASK_ENV=development
```
