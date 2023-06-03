from datetime import datetime
from recipeapp import db

# Modules #

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.TIMESTAMP)
    updated_at = db.Column(db.TIMESTAMP)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Profile(db.Model):
    __tablename__ = 'profiles'
    profile_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    full_name = db.Column(db.String(255))
    bio = db.Column(db.Text)
    avatar_url = db.Column(db.String(255))
    user = db.relationship('User', backref=db.backref('profile', uselist=False))

class Recipe(db.Model):
    __tablename__ = 'recipes'
    recipe_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    instructions = db.Column(db.Text)
    prep_time = db.Column(db.Integer)
    cook_time = db.Column(db.Integer)
    servings = db.Column(db.Integer)
    created_at = db.Column(db.TIMESTAMP)
    updated_at = db.Column(db.TIMESTAMP)
    user = db.relationship('User', backref=db.backref('recipes'))

class Ingredient(db.Model):
    __tablename__ = 'ingredients'
    ingredient_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.TIMESTAMP)
    updated_at = db.Column(db.TIMESTAMP)

class Category(db.Model):
    __tablename__ = 'categories'
    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.TIMESTAMP)
    updated_at = db.Column(db.TIMESTAMP)

class RecipeIngredient(db.Model):
    __tablename__ = 'recipe_ingredients'
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.ingredient_id'), primary_key=True)
    quantity = db.Column(db.String(255))
    created_at = db.Column(db.TIMESTAMP)
    updated_at = db.Column(db.TIMESTAMP)
    recipe = db.relationship('Recipe', backref=db.backref('recipe_ingredients'))
    ingredient = db.relationship('Ingredient', backref=db.backref('recipe_ingredients'))

class RecipeCategory(db.Model):
    __tablename__ = 'recipe_categories'
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id'), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), primary_key=True)
    created_at = db.Column(db.TIMESTAMP)
    updated_at = db.Column(db.TIMESTAMP)
    recipe = db.relationship('Recipe', backref=db.backref('recipe_categories'))
    category = db.relationship('Category', backref=db.backref('recipe_categories'))

class Favorite(db.Model):
    __tablename__ = 'favorites'
    favorite_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id'))
    created_at = db.Column(db.TIMESTAMP)
    user = db.relationship('User', backref=db.backref('favorites'))
    recipe = db.relationship('Recipe', backref=db.backref('favorites'))
