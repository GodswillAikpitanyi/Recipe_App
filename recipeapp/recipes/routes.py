from flask import (render_template, url_for, flash,
                    redirect, request,abort, Blueprint)
from flask_login import current_user, login_required
from recipeapp import db
from recipeapp.models import Recipe
from recipeapp.recipes.forms import RecipeCreationForm


recipes = Blueprint('recipes', __name__)

@recipes.route("/recipe/new", methods=['GET', 'POST'])
@login_required
def new_recipe():
    form = RecipeCreationForm()
    if form.validate_on_submit():
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
        return redirect(url_for('main.home'))
    return render_template('create_recipe.html', title='New Recipe', form=form, legend='New Recipe')


@recipes.route("/recipe/<int:recipe_id>")
def recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template('recipe.html', title=recipe.title, recipe=recipe)


@recipes.route("/recipe/<int:recipe_id>/update", methods=['GET', 'POST'])
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
        return redirect(url_for('recipes.recipe', recipe_id=recipe.id))
    elif request.method == 'GET':
        form.title.data = recipe.title
        form.description.data = recipe.description
        form.instructions.data = recipe.instructions
        form.prep_time.data = recipe.prep_time
        form.cook_time.data = recipe.cook_time
        form.servings.data = recipe.servings
    return render_template('create_recipe.html', title='Update Recipe',
                           form=form, legend='Update Recipe')


@recipes.route("/recipe/<int:recipe_id>/delete", methods=['POST'])
@login_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.user != current_user:
        abort(403)
    db.session.delete(recipe)
    db.session.commit()
    flash('Your recipe has been deleted!', 'success')
    return redirect(url_for('main.home'))
