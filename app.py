from flask import Flask

import secret
import config
from models.base_model import db
import time
from models.user import User
from models.topic import Topic
from models.reply import Reply

from routes.index import main as index_routes
from routes.topic import main as topic_routes
from routes.reply import main as reply_routes
from routes.board import main as board_routes
from routes.message import main as mail_routes, mail
from routes.homepage import main as homepage_routes
from routes.setting import main as setting_routes


def count(input):
    print('count using jinja filter')
    return len(input)


def format_time(unix_timestamp):
    f = '%Y-%m-%d %H:%M:%S'
    value = time.localtime(unix_timestamp)
    formatted = time.strftime(f, value)
    return formatted


def image1(t_user_id):
    u = User.one(id=t_user_id)
    return u.image


def name1(t_user_id):
    u = User.one(id=t_user_id)
    return u.username


def configured_app():
    # web framework
    # web application
    # __main__
    app = Flask(__name__)
    app.secret_key = secret.secret_key

    uri = 'mysql+pymysql://root@127.0.0.1/websx?charset=utf8mb4&unix_socket=/var/run/mysqld/mysqld.sock'
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    app.config['MAIL_SERVER'] = 'smtp.exmail.qq.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = config.admin_mail
    app.config['MAIL_PASSWORD'] = secret.mail_password

    mail.init_app(app)

    register_routes(app)
    app.template_filter()(count)
    app.template_filter()(format_time)
    app.template_filter()(image1)
    app.template_filter()(name1)
    return app


def register_routes(app):
    app.register_blueprint(index_routes)
    app.register_blueprint(topic_routes, url_prefix='/topic')
    app.register_blueprint(reply_routes, url_prefix='/reply')
    app.register_blueprint(board_routes, url_prefix='/board')
    app.register_blueprint(mail_routes, url_prefix='/mail')
    app.register_blueprint(homepage_routes, url_prefix='/homepage')
    app.register_blueprint(setting_routes, url_prefix='/setting')


# 运行代码
if __name__ == '__main__':
    app = configured_app()
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.jinja_env.auto_reload = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    config = dict(
        debug=True,
        host='localhost',
        port=2000,
        threaded=True,
    )
    app.run(**config)
