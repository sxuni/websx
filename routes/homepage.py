from flask import (
    render_template,
    Blueprint,
)

from routes import current_user

from models.topic import Topic
from models.user import User
from models.reply import Reply

main = Blueprint('sx_homepage', __name__)


@main.route('/<int:id>')
def index(id):
    u = User.one(id=id)
    t1 = Topic.all(user_id=id)
    t = list(reversed(t1))
    r1 = Reply.all(user_id=id)
    r = list(reversed(r1))
    topic = []
    for each in r:
        one = Topic.one(id=each.topic_id)
        topic.append(one)
    return render_template("homepage.html", user=u, topic=t, topic2=topic)
