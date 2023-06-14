import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from recipeapp import mail


def save_picture(form_picture):
    # Saving pictures uniquely
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pictures', picture_fn)

    # Resizing pictures
    output_size = (125, 125)
    im = Image.open(form_picture)
    im.thumbnail(output_size)
    im.save(picture_path)

    return picture_fn




def meal_picture(form_avatar):
    # Saving pictures uniquely
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_avatar.filename)
    imageFile_fn = random_hex + f_ext
    imageFile_path = os.path.join(current_app.root_path, 'static/meal_pictures', imageFile_fn)

    # Resizing pictures
    output_size = (400, 400)
    im = Image.open(form_avatar)
    im.thumbnail(output_size)
    im.save(imageFile_path)

    '''if form.avatar.data:
        meal_image = meal_picture(form.avatar.data)
        recipe.user.avatar = meal_image

        recipe = Recipe.query.filter_by(user_id=current_user.user_id).first()#

        avatar = url_for('static', filename='meal_pictures/' + recipe.avatar)

        what to render , avatar=avatar'''
    return imageFile_fn



def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                    sender='noreply@demo.com',
                    recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request, simply ignore this email and no chnages will be made
'''
    mail.send(msg)
