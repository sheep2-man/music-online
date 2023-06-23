from . import db   # 与form app import db 有什么区别

# 用户表
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(100),unique=True,nullable=False)
    pwd = db.Column(db.String(128),nullable=False)
    flag = db.Column(db.Boolean,default=0)    # 用户标识，0：普通用户，1：管理员

    def __repr__(self):
        return '<User %r>' % self.username

    def check_pwd(self,other_pwd):
        '''
        检测密码是否正确   https://blog.csdn.net/JENREY/article/details/86671552/
        :param other_pwd:用户登录输入的密码
        :return:布尔值
        '''
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd ,other_pwd)

# 歌手表
class Artist(db.Model):
    __tablename__ = 'artist'
    id = db.Column(db.Integer,primary_key=True)
    artistName = db.Column(db.String(100))   # 歌手的名字
    style = db.Column(db.Integer)            # 歌手的类型
    imgURL = db.Column(db.String(100))       # 歌手头像地址
    isHot = db.Column(db.Boolean)            # 是否热门

# 歌曲表
class Song(db.Model):
    __tablename__ = 'song'
    id = db.Column(db.Integer,primary_key=True)
    songName = db.Column(db.String(100)) # 歌曲的名字
    singer = db.Column(db.String(100))   # 歌手
    fileURL = db.Column(db.String(100))  # 歌曲的路径
    hits = db.Column(db.Integer,default=0) # 歌曲的点击量
    style = db.Column(db.Integer)         # 歌曲类型 0:全部  1:华语  2:欧美  3:日语  4:韩语  5:其他
    collects = db.relationship('Collect',backref='song')
    # 对于一个Song实例，属性collects返回与该Song相关联的所有Collect对象列表

class Collect(db.Model):
    __tablename__ = 'collect'
    id = db.Column(db.Integer,primary_key=True)
    song_id = db.Column(db.Integer,db.ForeignKey('song.id'))
    user_id = db.Column(db.Integer)

