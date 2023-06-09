# Imports #
from flask import render_template, url_for, flash, redirect
from recipeapp import app
from recipeapp.forms import RegistrationForm, LoginForm
from recipeapp.models import User, Profile, Recipe, Ingredient, Category, RecipeIngredient, RecipeCategory, Favorite


# Posts #
posts = [
    {
        'author': 'Mr Hamilton',
        'title': 'Initial recipe',
        'content': 'first post',
        'date_posted': 'May 30th, 2023'
    },
    {
        'author': 'Miss Kelly Piquet',
        'title': 'Subsequent recipe',
        'content': 'second post',
        'date_posted': 'May 31th, 2023'
    }
]


# Routes #
@app.route("/")
@app.route("/home")
def home():
    return (render_template('home.html', posts=posts))

@app.route("/landing_page", methods=['GET', 'POST'])
def landing_page():
    return (render_template('landing_page.html', title='Landing Page'))

@app.route("/about")
def about():
    return (render_template('about.html', title='About'))

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return (render_template('register.html', title='Register', form=form))

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful, Please check username and password', 'danger')
    return (render_template('login.html', title='Login', form=form))
