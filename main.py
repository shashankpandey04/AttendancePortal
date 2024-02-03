from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector as msc
mycon=msc.connect(host='localhost',user='root',passwd='root',database='aws')
mycur=mycon.cursor()

app = Flask(__name__)
app.secret_key = 'any random string'
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/adduser', methods=['GET', 'POST'])
def adduser():
    if 'admin' not in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = request.form['admin']
        name = request.form['name']
        mycur.execute("INSERT INTO login (uname, passwd, admin, name) VALUES (%s, %s, %s, %s)", (username, password, admin, name))
        mycon.commit()
        return redirect(url_for('viewuser'))
    return render_template('add_user.html')

@app.route('/viewusers', methods=['GET', 'POST'])
def viewuser():
    if 'admin' not in session:
        return redirect(url_for('index'))
    if request.method == 'GET':
        search_username = request.args.get('search', '')
        if search_username:
            mycur.execute("SELECT * FROM login WHERE uname = %s", (search_username,))
            res = mycur.fetchall()
        else:
            mycur.execute("SELECT * FROM login")
            res = mycur.fetchall()
        return render_template('view_users.html', res=res, search_username=search_username)
    return render_template('view_users.html')

@app.route('/usermanagement')
def usermanagement():
    if 'admin' not in session:
        return redirect(url_for('index'))
    return render_template('usermanagement.html')

@app.route('/managemeet')
def managemeet():
    if 'admin' not in session:
        return redirect(url_for('index'))
    return render_template('managemeet.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['uname']
        passwd = request.form['passwd']
        try:
            mycur.execute(f"SELECT * FROM login WHERE uname='{uname}' AND passwd='{passwd}' AND admin='1'")
            admin_res = mycur.fetchone()
            if admin_res:
                session['uname'] = uname
                session['admin'] = True
                return redirect(url_for('dashboard'))
        except:
            pass 
        try:
            mycur.execute(f"SELECT * FROM login WHERE uname='{uname}' AND passwd='{passwd}'")
            user_res = mycur.fetchone()
            if user_res:
                session['uname'] = uname
                return redirect(url_for('dashboard'))
        except:
            pass 
        return render_template('index.html', msg='Invalid Username or Password')
    else:
        return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.route('/logout')
def logout():
    try:
        session.pop('admin',None)
    except:
        pass
    session.pop('uname',None)
    return redirect(url_for('index'))

app.run(debug=True)