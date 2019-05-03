import os
import uuid


from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from routes import *

from models.user import User
from werkzeug.datastructures import FileStorage


main = Blueprint('setting', __name__)


@main.route("/")
def index():
    user = current_user()
    token = new_csrf_token()
    return render_template("setting.html", user=user, token=token)


@main.route("/name", methods=["POST"])
@csrf_required
def name():
    token = new_csrf_token()
    user = current_user()
    form = request.form
    User.update(id=user.id, username=form['username'], sign=form['sign'])
    u = User.one(id=user.id)
    return render_template("setting.html", user=u, token=token)


@main.route("/password", methods=["POST"])
@csrf_required
def password():
    token = new_csrf_token()
    user = current_user()
    form = request.form
    old = User.salted_password(form['old_pass'])
    new = User.salted_password(form['new_pass'])
    if User.one(id=user.id, password=old) is not None:
        User.update(id=user.id, password=new)
        u = User.one(id=user.id)
    else:
        return redirect(url_for('index.index'))

    return render_template("setting.html", user=u, token=token)


@main.route("/avatar", methods=["POST"])
@csrf_required
def avatar():
    token = new_csrf_token()
    file: FileStorage = request.files['avatar']
    suffix = file.filename.split('.')[-1]
    filename = '{}.{}'.format(str(uuid.uuid4()), suffix)
    path = os.path.join('images', filename)
    file.save(path)
    u = current_user()
    User.update(u.id, image='/images/{}'.format(filename))
    u = User.one(id=u.id)
    return render_template("setting.html", user=u, token=token)
