from flask import Flask, views, redirect, url_for, request, render_template

from other import User

app = Flask(__name__)

@app.route('/1')
def test_flask_filter():
    data = {
            'Python': '编程语言',
            'Flask': 'Web 框架',
            'Jinja2': '模板引擎',
            'HTML': '前端语言'
        }
    SomePath = {'SomePath': '<h1 style="color:blue">SomePath</h1>'}
    return render_template('test_filter.html', data=data, SomePath=SomePath)

@app.route('/')
def test_flask_filter2():
    user1 = User('nacy',18,'female')
    user2 = User('bill', 18,'male')
    user3 = User('jack', 20,'male')
    user4 = User('lily', 25, 'female')
    users = [user1,user2,user3,user4]

    return render_template('test_filter2.html',users = users)

if __name__ == '__main__':
    app.debug = True
    app.run()


#app.add_url_rule(rule=访问的url,endpoint=路由别名,view_func=视图名称,methods=[允许访问的方法])

    # app.run(host='0.0.0.0', port=8000, debug=True)
