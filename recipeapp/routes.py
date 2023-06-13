# Imports #
import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from recipeapp import app, db, bcrypt
from recipeapp.forms import RegistrationForm, LoginForm, UpdateAccountForm, RecipeCreationForm
from recipeapp.models import User, Recipe, Category, Ingredient, RecipeIngredient, RecipeCategory, Favorite
from flask_login import login_user, current_user, logout_user, login_required



# Routes #

@app.route("/")
@app.route("/landing_page", methods=['GET', 'POST'])
def landing_page():
    return render_template('landing_page.html', title='Landing Page')

@app.route("/home")
@login_required
def home():
    recipe = Recipe.query.all()
    return render_template('home.html', recipe=recipe)

@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account has been created! Kindly log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    # Saving pictures uniquely
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pictures', picture_fn)

    # Resizing pictures
    output_size = (125, 125)
    im = Image.open(form_picture)
    im.thumbnail(output_size)
    im.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.avatar = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    avatar = url_for('static', filename='profile_pictures/' + current_user.avatar)
    return render_template('account.html', title='Account', avatar=avatar, form=form)


def meal_picture(form_image_file):
    # Saving pictures uniquely
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_image_file.filename)
    imageFile_fn = random_hex + f_ext
    imageFile_path = os.path.join(app.root_path, 'static/meal_pictures', imageFile_fn)

    # Resizing pictures
    output_size = (400, 400)
    im = Image.open(form_image_file)
    im.thumbnail(output_size)
    im.save(imageFile_path)

    return imageFile_fn


@app.route("/recipe/new", methods=['GET', 'POST'])
@login_required
def new_recipe():
    recipe = Recipe.query.filter_by(user_id=current_user.user_id).first()
    form = RecipeCreationForm()
    if form.validate_on_submit():
        if form.image_file.data:
            meal_image = meal_picture(form.image_file.data)
            recipe.user.image_file = meal_image
        recipe = Recipe(
            title=form.title.data,
            description=form.description.data,
            instructions=form.instructions.data,
            prep_time=form.prep_time.data,
            cook_time=form.cook_time.data,
            servings=form.servings.data
        )
        db.session.add(recipe)
        db.session.commit()
        flash('Your recipe has been created!!', 'success')
        return redirect(url_for('home'))
    image_file = url_for('static', filename='meal_pictures/' + recipe.current_user.image_file)
    return render_template('create_recipe.html', title='Create Recipe', form=form, legend='New Recipe', image_file=image_file)


@app.route("/recipe/<int:recipe_id>")
def recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template('recipe.html', title=recipe.title, recipe=recipe)


@app.route("/recipe/<int:recipe_id>/update", methods=['GET', 'POST'])
@login_required
def update_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.user != current_user:
        abort(403)
    form = RecipeCreationForm()
    if form.validate_on_submit():
        recipe.title = form.title.data
        recipe.description = form.description.data
        recipe.instructions = form.instructions.data
        recipe.prep_time = form.prep_time.data
        recipe.cook_time = form.cook_time.data
        recipe.servings = form.servings.data
        db.session.commit()
        flash('Your recipe has been updated!', 'success')
        return redirect(url_for('recipe', recipe_id=recipe.id))
    elif request.method == 'GET':
        form.title.data = recipe.title
        form.description.data = recipe.description
        form.instructions.data = recipe.instructions
        form.prep_time.data = recipe.prep_time
        form.cook_time.data = recipe.cook_time
        form.servings.data = recipe.servings
    return render_template('create_recipe.html', title='Update Recipe',
                           form=form, legend='Update Recipe')


@app.route("/recipe/<int:recipe_id>/delete", methods=['POST'])
@login_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.user != current_user:
        abort(403)
    db.session.delete(recipe)
    db.session.commit()
    flash('Your recipe has been deleted!', 'success')
    return redirect(url_for('home'))
