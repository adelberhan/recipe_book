# 🥘 Flask Recipe Book APP

A full-stack recipe management system with user authentication, built using a **Flask** backend and **HTML/JavaScript** frontend.

---

## ✨ Features

- 🔐 User registration and login with session management  
- 📋 Create, view, edit, and delete recipes  
- 🔁 RESTful API for all operations  
- 💾 JSON-based data storage (no database required)  
- 📱 Responsive and interactive frontend  

---

## 📦 Requirements

```
blinker==1.9.0  
click==8.1.8  
colorama==0.4.6  
Flask==3.1.0  
itsdangerous==2.2.0  
Jinja2==3.1.6  
MarkupSafe==3.0.2  
Werkzeug==3.1.3  
```

---

## 📁 Project Structure

```
flask-recipe-app/
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

## 📡 API Reference

### 🔐 Authentication

| Endpoint       | Method | Description              | Request Body              |
|----------------|--------|--------------------------|---------------------------|
| `/register`    | GET    | Registration page         | –                         |
| `/api/register`| POST   | Register new user         | `{ username, password }`  |
| `/login`       | GET    | Login page                | –                         |
| `/login`       | POST   | Authenticate user         | `{ username, password }`  |

### 📖 Recipes

| Endpoint                     | Method | Description                 | Request Body                                        |
|-----------------------------|--------|-----------------------------|-----------------------------------------------------|
| `/recipes`                  | GET    | Recipes listing page        | –                                                   |
| `/api/recipes`              | GET    | Get all recipes             | –                                                   |
| `/api/recipes`              | POST   | Create new recipe           | `{ name, ingredients, instructions, prep_time, cook_time, created_by }` |
| `/recipes/<recipe_id>`      | GET    | View recipe details page    | –                                                   |
| `/api/recipes/<id>`         | GET    | Get single recipe           | –                                                   |
| `/recipes/edit/<id>`        | GET    | Edit recipe page            | –                                                   |
| `/api/recipes/<id>`         | PUT    | Update recipe               | `{ name, ingredients, instructions, ... }`          |
| `/api/recipes/<id>`         | DELETE | Delete recipe               | –                                                   |

### 🗺️ Pages

| Route         | Method | Description               |
|---------------|--------|---------------------------|
| `/`           | GET    | Home page                 |
| `/home`       | GET    | User dashboard            |
| `/add-recipe` | GET    | Recipe creation form      |

---

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
