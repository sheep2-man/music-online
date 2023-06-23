# 程序启动入口
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell

from app.models import *

from app import create_app, db

app = create_app('develop')

manager = Manager(app)
migrate = Migrate(app,db)   #迁移  数据操作  绑定app对象和db（sqlalchemy对象）


def make_shell_context():
    return dict(app=app,db=db)


manager.add_command('shell',Shell(make_context=make_shell_context))
manager.add_command('db',MigrateCommand)    #一系列的数据库迁移命令
#  init(初始化)  /  migrate(迁移)  /  upgrade(写入数据库)
# python manage.py db init
# python manage.py db migrate
# python manage.py db upgrade

if __name__ == '__main__':
    manager.run()
