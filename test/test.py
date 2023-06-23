from flask import Flask, redirect, url_for, request, session, render_template, abort, flash,views

app = Flask(__name__)

@app.route('/test')
def test(username):

    if username=='zyg':
        return 'success'
    return render_template('test.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        name=request.form['name']
        pd=request.form['passwd']

        if name=='zyg' and pd=='1':
            # return 'success'
            return redirect(url_for('test',username='zyg'))
        else:
            return 'error'
    else:
        return render_template('login.html')

if __name__ == '__main__':
    app.debug = True
    app.run()


