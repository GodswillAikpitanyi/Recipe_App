from datetime import datetime
from recipeapp import db

# Modules #

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Profile(db.Model):
    __tablename__ = 'profiles'
    profile_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    full_name = db.Column(db.String(120))
    bio = db.Column(db.Text)
    avatar_url = db.Column(db.String(255))
    user = db.relationship('User', backref=db.backref('profile', uselist=False))

    def __repr__(self):
        return f"Profile('{self.full_name}', '{self.bio}', '{self.avatar_url}')"

class Recipe(db.Model):
    __tablename__ = 'recipes'
    recipe_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    instructions = db.Column(db.Text)
    prep_time = db.Column(db.Integer)
    cook_time = db.Column(db.Integer)
    servings = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user = db.relationship('User', backref=db.backref('recipes'))

    def __repr__(self):
        return f"Recipe('{self.title}', '{self.description}', '{self.instructions}', '{self.prep_time}', '{self.cook_time}', '{self.servings}')"

class Ingredient(db.Model):
    __tablename__ = 'ingredients'
    ingredient_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Ingredient('{self.__tablename__}', '{self.name}')"

class Category(db.Model):
    __tablename__ = 'categories'
    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Category('{self.__tablename__}', '{self.name}')"

class RecipeIngredient(db.Model):
    __tablename__ = 'recipe_ingredients'
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.ingredient_id'), primary_key=True)
    quantity = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    recipe = db.relationship('Recipe', backref=db.backref('recipe_ingredients'))
    ingredient = db.relationship('Ingredient', backref=db.backref('recipe_ingredients'))

    def __repr__(self):
        return f"RecipeIngredient('{self.quantity}')"

class RecipeCategory(db.Model):
    __tablename__ = 'recipe_categories'
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id'), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    recipe = db.relationship('Recipe', backref=db.backref('recipe_categories'))
    category = db.relationship('Category', backref=db.backref('recipe_categories'))

class Favorite(db.Model):
    __tablename__ = 'favorites'
    favorite_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id'))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user = db.relationship('User', backref=db.backref('favorites'))
    recipe = db.relationship('Recipe', backref=db.backref('favorites'))