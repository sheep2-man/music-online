# 这个文件里面专门写项目的一些 配置
# 写配置文件的时候，变量名都是用大写

import os.path


# 创建一个 工程项目 的基本类
class Config(object):
    # 秘钥
    # SECRET_KEY = 'flasd234r43479996'
    SECRET_KEY ='228858fc24ff'
    # 数据库追踪更新
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # 设置 DEBUG = False
    DEBUG = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    # 添加数据库的 路径
    BASE_URL = os.path.dirname(os.path.abspath(__file__))
    print(BASE_URL)
    # C:\Users\17146\Desktop\pythonWEB_test_onlineMusic\train_flask_onlineMusic
    DATA_URL = os.path.join(BASE_URL,'onlineMusic.db')
    print(DATA_URL)
    # 数据库连接追踪更新
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATA_URL


config = {
    'develop': DevelopmentConfig
}