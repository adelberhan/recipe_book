import json
import os
import datetime
from pathlib import Path

class Recipe:
    _last_id = 0  # Class variable to keep track of last used ID
    
    def __init__(self, name, ingredients, instructions, prep_time, cook_time, 
                 image_url=None, id=None, created_by=None, 
                 created_at=None, updated_at=None):
        self.id = id if id is not None else self._get_next_id()
        self.name = name
        self.ingredients = ingredients
        self.instructions = instructions
        self.prep_time = prep_time
        self.cook_time = cook_time
        self.image_url = image_url
        self.created_by = created_by
        self.created_at = created_at if created_at else datetime.datetime.now().isoformat()
        self.updated_at = updated_at if updated_at else datetime.datetime.now().isoformat()
    
    @classmethod
    def _get_next_id(cls):
        # Generate the next sequential ID # 
        if cls._last_id == 0:
            # Initialize with the highest existing ID + 1
            recipes = cls.get_all()
            if recipes:
                cls._last_id = max(int(r.id) for r in recipes)
        cls._last_id += 1
        return str(cls._last_id)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "ingredients": self.ingredients,
            "instructions": self.instructions,
            "prep_time": self.prep_time,
            "cook_time": self.cook_time,
            "image_url": self.image_url,
            "created_by": self.created_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            ingredients=data.get("ingredients"),
            instructions=data.get("instructions"),
            prep_time=data.get("prep_time"),
            cook_time=data.get("cook_time"),
            image_url=data.get("image_url"),
            created_by=data.get("created_by"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    @classmethod
    def get_all(cls):
        recipes = []
        data_file = Path("data/recipes.json")
        if data_file.exists():
            with open(data_file, "r") as f:
                try:
                    data = json.load(f)
                    for recipe_data in data:
                        recipes.append(cls.from_dict(recipe_data))
                except json.JSONDecodeError:
                    # Handle empty or invalid JSON file
                    pass
        return recipes
    
    @classmethod
    def get_by_id(cls, recipe_id):
        recipes = cls.get_all()
        for recipe in recipes:
            if recipe.id == str(recipe_id):  # Ensure string comparison
                return recipe
        return None
    
    def save(self):
        recipes = self.get_all()
        recipes.append(self)
        self._save_all_recipes(recipes)
        return self
    
    def update(self):
        recipes = self.get_all()
        for i, recipe in enumerate(recipes):
            if recipe.id == self.id:
                self.updated_at = datetime.datetime.now().isoformat()
                recipes[i] = self
                break
        self._save_all_recipes(recipes)
        return self
    
    def delete(self):
        recipes = self.get_all()
        recipes = [recipe for recipe in recipes if recipe.id != self.id]
        self._save_all_recipes(recipes)
    
    def _save_all_recipes(self, recipes):
        os.makedirs("data", exist_ok=True)
        with open("data/recipes.json", "w") as f:
            json.dump([recipe.to_dict() for recipe in recipes], f, indent=2)