# 这是一个示例 Python 脚本。

from flask import Flask, url_for
from werkzeug.utils import redirect

app = Flask(__name__)



def hello():
    return 'Hello World'

@app.route('/post/<int:post_id>')
def show_post(post_id):
     # 根据ID显示文章，ID是整型数据
     return 'Post ID: %d' % post_id

@app.route('/url/')
def to_url():
      # 跳转到show_post()视图函数
      #return redirect(url_for('book_name',str='我是'))
      return redirect(url_for('show_post',post_id=1))
      #url_for('show_post', post_id=10)

@app.route('/book/<str>')
def book_name(str):
    return f'书的名字是<<{str}>>'

if __name__ == '__main__':
    app.add_url_rule('/hello2','h1',hello,methods=['GET'])
    app.run(debug=True)
