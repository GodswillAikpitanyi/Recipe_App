from flask import render_template, request, Blueprint
from flask_login import login_required
from recipeapp.models import Recipe

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/landing_page", methods=['GET', 'POST'])
def landing_page():
    return render_template('landing_page.html', title='Landing Page')

@main.route("/home")
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    recipes = Recipe.query.order_by(Recipe.created_at.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', recipes=recipes)

@main.route("/about")
def about():
    return render_template('about.html', title='About')
