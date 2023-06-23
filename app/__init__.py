from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import config

# 创建一个数据库连接
db = SQLAlchemy()


# 定义工厂函数：
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    from app.home import home
    app.register_blueprint(home)

    return app