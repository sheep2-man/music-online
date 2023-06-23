# 视图文件，路由和视图函数就写在这里
import bdb
from functools import wraps
import requests
from flask import request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash

from app.home import home

from flask import render_template
from app.models import *
#管理员用户名密码分别为zyg 123
def user_login(f):
    @wraps(f)
    def decorate_fuction(*args,**kwargs):
        if 'username' not in session:
            return "<script>alert('');history.go(-1)</script>"
        return f(*args,**kwargs)
    return decorate_fuction

def admin_login(f):
    @wraps(f)
    def decorate_fuction(*args, **kwargs):
        if session['username']!='zyg':
            return redirect(url_for('home.index'))
        return f(*args, **kwargs)
    return decorate_fuction


@home.route('/')
def index():

    return render_template('home/index.html')

@home.route('/contentFrame')
def contentFrame():
    hot_artist = Artist.query.filter_by(isHot=1).limit(12).all()


    hot_song = Song.query.order_by(Song.hits.desc()).limit(10).all()

    return render_template('home/contentFrame.html',hot_artist=hot_artist,hot_song=hot_song)

@home.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':

        username=request.form['username']
        pwd=request.form['pwd']
        user=User.query.filter_by(username=username).first()
        print(user.pwd)
        res={}
        if user!=None:
              # if user.pwd==pwd:
              if user.check_pwd(pwd):
                  session['username']=username
                  session['user_id']=user.id

                  res['status']=1
                  res['message']='登陆成功'
                  return jsonify(res)

              else:
                  res['status']=-2
                  res['message']=" 登陆失败，请检查用户名和密码"
                  return jsonify(res)
        else:
            res['status']=-1
            res['message']=' 登陆失败，用户不存在'
            return  jsonify(res)
        return render_template('home/index.html')


    return render_template('home/login.html')

@home.route('/modifyPassword',methods=['GET','POST'])
def modifyPassword():
    if request.method=='POST':
        new_pwd=request.form['new_pwd']
        old_pwd=request.form['old_pwd']
        res={}
        user=User.query.filter_by(username=session['username']).first()
        if user.check_pwd(old_pwd):
           try:
               user.pwd=generate_password_hash(new_pwd)
               db.session.commit()
               res['status']=3
               res['message']='密码修改成功'
               return jsonify(res)

           except:
                db.session.rollback()
                res['status'] = -1
                res['message'] = '密码修改失败,网络异常'
                return jsonify(res)
        else:
            res['status'] = -1
            res['message'] = '密码输入错误'
            return jsonify(res)
    return render_template('home/modifyPassword.html')


@home.route('/logout')
def logout():

    session.pop('username',None)
    return redirect(url_for('home.index'))



@home.route('/register',methods=['GET','POST'])
def register():
    # 注册
    if request.method == 'POST':
        username=request.form['username']
        pwd=request.form['pwd']
        user=User.query.filter_by(username=username).first()
        res = {}
        from werkzeug.security import generate_password_hash
        pwd = generate_password_hash(pwd)
        if user is None:
            try:
                new_user=User()
                new_user.username=username
                new_user.pwd=pwd
                db.session.add(new_user)
                db.session.commit()
                res['status']=2
                res['message']='注册成功'
                return jsonify(res)
            except:
                db.session.rollback()
                res['status'] = -1
                res['message'] = '注册失败'
                return jsonify(res)
        else:
            res['status'] = -2
            res['message'] = '用户名已存在'
            return jsonify(res)

    return render_template('home/register.html')

@home.route('/manageArtist')
@admin_login
def manageArtist():

    page=request.args.get('page',type=int)
    page_data=Artist.query.paginate(page=page,per_page=9)
    return render_template('home/manageArtist.html',page_data=page_data)

@home.route('/manageSong')
def manageSong():
    page = request.args.get('page', type=int)
    page_data=Song.query.paginate(page=page,per_page=9)
    return  render_template('home/manageSong.html',page_data=page_data)


@home.route('/manageArtistAdd',methods=['GET','POST'])
def manageArtistAdd():
    if request.method=='POST':
        artistName=request.form['artistName']
        imgUrl=request.form['imgURL']
        style=request.form['style']
        isHot=request.form['isHot']
        res={}
        artist=Artist.query.filter_by(artistName=artistName).first()
        if artist:
            res['status']=-2
            res['message']='歌手已存在'
            return jsonify(res)
        else:
            try:
                new_artist=Artist()
                new_artist.artistName=artistName
                new_artist.style=style
                new_artist.isHot=bool(isHot)
                new_artist.imgURL=imgUrl
                db.session.add(new_artist)
                db.session.commit()
                res['status']=4
                res['message']='添加成功'
                return jsonify(res)
            except:
                res['status']=-1
                res['message']='添加失败,网络异常'
                return jsonify(res)

    return  render_template('home/manageArtistAdd.html')


@home.route('/manageArtistEdit',methods=['GET','POST'])
def manageArtistEdit():
    id=request.values['id']
    artist=Artist.query.filter_by(id=id).first()
    res={}
    if request.method == 'POST':
        if artist:
            try:
                artist.imgURL=request.form['imgURL']
                artist.style=request.form['style']
                isHot=request.form['isHot']
                artist.isHot=bool(isHot)
                artist.artistName=request.form['artistName']

                db.session.commit()
                res['status'] = 6
                res['message'] = '修改成功'
                return jsonify(res)

            except:
                res['status'] = -2
                res['message'] = '网络异常,失败'
                return jsonify(res)
        else:
            res['status']=-1
            res['message']='歌手不存在'
            return jsonify(res)

    return  render_template('home/manageArtistEdit.html',artist=artist)


@home.route('/manageArtistDel')
def manageArtistDel():
    id = request.values['id']

    res = {}
    try:
            artist=Artist.query.get_or_404(id)
            db.session.delete(artist)
            db.session.commit()
            res['status']=7
            res['message']='删除成功'

    except:
            db.session.rollback()
            res['status'] = -1
            res['message'] = '删除失败'

    return jsonify(res)



@home.route('/manageSongEdit',methods=['GET','POST'])
def manageSongEdit():
    id = request.values['id']
    song = Song.query.filter_by(id=id).first()
    res = {}
    if request.method == 'POST':
        if song:
            try:
                song.style= request.form['style']
                song.singer = request.form['singer']
                song.fileURL=request.form['fileURL']
                song.songName = request.form['songName']

                db.session.commit()
                res['status'] = 8
                res['message'] = '修改成功'
                return jsonify(res)

            except:
                res['status'] = -2
                res['message'] = '网络异常,失败'
                return jsonify(res)
        else:
            res['status'] = -1
            res['message'] = '歌手不存在'
            return jsonify(res)


    return  render_template('home/manageSongEdit.html',song=song)


@home.route('/manageSongAdd',methods=['GET','POST'])
def manageSongAdd():
    if request.method == 'POST':
        songName = request.form['songName']
        fileURL = request.form['fileURL']
        style = request.form['style']
        singer = request.form['singer']
        res = {}
        song = Song.query.filter_by(songName=songName).first()
        if song:
            res['status'] = -2
            res['message'] = '歌曲已存在'
            return jsonify(res)
        else:
            try:
                new_song=Song(
                    songName=songName,
                    fileURL=fileURL,
                    singer=singer,
                    style=style,
                    hits=0
                )
                db.session.add(new_song)
                db.session.commit()
                res['status'] = 5
                res['message'] = '添加成功'
                return jsonify(res)
            except:
                res['status'] = -1
                res['message'] = '添加失败,网络异常'
                return jsonify(res)
    return  render_template('home/manageSongAdd.html')

@home.route('/manageSongDel')
def manageSongDel():
    id=request.args.get('id')

    res = {}
    try:
        song = Song.query.get_or_404(id)
        db.session.delete(song)
        db.session.commit()
        res['status'] = 9
        res['message'] = '删除成功'

    except:
        db.session.rollback()
        res['status'] = -1
        res['message'] = '删除失败'

    return jsonify(res)


@home.route('/artist')
def artist():

    id=request.args.get('id',type=int)

    song=Song.query.join(Artist,Artist.artistName==Song.singer).filter(Artist.id==id).all()

    hot_artlist=Artist.query.filter_by(isHot=1).limit(6).all()

    return render_template('home/artist.html',song=song,hot_artlist=hot_artlist)


@home.route('/search')
def search():

    name=request.args.get('keyword')
    print(name)

    page=request.args.get('page',type=int)

    if  name:
        page_data = Song.query.filter(Song.songName.like('%'+name+'%')).order_by(Song.hits.desc()).paginate(page, per_page=5)
        print(page_data)
    else:
        page_data = Song.query.order_by(Song.hits.desc()).paginate(page, per_page=8)

    return render_template('home/search.html',page_data=page_data,keyword=name)


@home.route('/collect')
def collect():
    song_id = request.args.get('id')
    user_id=session['user_id']
    collect = Collect.query.filter_by(user_id=user_id,song_id=song_id).first()
    if  collect:#歌曲已存在
        res = {}
        res['status'] = -1;
        res['message'] = '歌曲已收藏'

    else:
        new_collect = Collect()
        new_collect.user_id=user_id
        new_collect.song_id=song_id
        db.session.add(new_collect)
        db.session.commit()
        #添加新表到Collect
        res = {}
        res['status'] = 12
        res['message'] = '收藏成功'

    return jsonify(res)



@home.route('/collectList')
def collectList():
    user_id=session['user_id']
    page=request.args.get('page',type=int)
    page_data=Collect.query.filter_by(user_id=user_id).paginate(page, per_page=8)
    return render_template('home/collectList.html',page_data=page_data)

@home.route('/toplist')
def toplist():
    top_song = Song.query.order_by(Song.hits.desc()).limit(30).all()
    hot_artist = Artist.query.filter_by(isHot=1).limit(9).all()
    print(toplist)
    return render_template('home/toplist.html',top_song=top_song,hot_artist=hot_artist)

@home.route('/styleList')
def styleList():
    style = request.args.get('type', type=int)
    page = request.args.get('page', type=int)
    if style:
        page_data = Song.query.filter_by(style=style).order_by(Song.hits.desc()).paginate(page, per_page=10)
    else:
        page_data = Song.query.order_by(Song.hits.desc()).paginate(page, per_page=10)


    return render_template('home/styleList.html',type=style,page_data=page_data)

@home.route('/artistList')
def artistList():

    style=request.args.get('type',type=int)
    page=request.args.get('page',type=int)
    if style:
        page_data=Artist.query.filter_by(style=style).paginate(page,per_page=10)
    else:
        page_data=Artist.query.paginate(page,per_page=10)
    return render_template('home/artistList.html',type=style,page_data=page_data)

@home.route('/addHit')
def addHit():
    # 点击量+1
    id=request.args.get('id')
    song=Song.query.get_or_404(int(id))

    if not song:
      res={}
      res['status']=-1;
      res['message']='歌曲不存在'

    else:

        song.hits+=1
        # db.session.add(song)
        db.session.commit()
        res = {}
        res['status']=1
        res['message']='播放次数+1'

    return jsonify(res)
