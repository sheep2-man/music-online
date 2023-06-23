# 创建了一个名为 home 的蓝图子程序
from flask import Blueprint

home = Blueprint('home',__name__)

from app.home.views import *
