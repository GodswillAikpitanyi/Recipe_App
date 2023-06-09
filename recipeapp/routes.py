# Imports #
from flask import render_template, url_for, flash, redirect, request
from recipeapp import app, db, bcrypt
from recipeapp.forms import RegistrationForm, LoginForm
from recipeapp.models import User, Profile, Recipe, Category, Ingredient, RecipeIngredient, RecipeCategory, Favorite
from flask_login import login_user, current_user, logout_user, login_required


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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account has been created! kindly log in', 'success')
        return redirect(url_for('home'))
    return (render_template('register.html', title='Register', form=form))

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful, Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')
