import flask
from flask import Flask, render_template, request, redirect, url_for, abort
from sqlalchemy import create_engine, text

app = flask.Flask(__name__)

conn_str = 'mysql://root:Cookiebear1@localhost/flask'
engine = create_engine(conn_str, echo = True)
conn = engine.connect()


@app.route('/create_test', methods=['GET'])
def create_test():
    return flask.render_template('create_test.html')

@app.route('/create_test', methods=['POST'])
def create_tests():
        conn.execute(text("INSERT INTO tests (test_id, teacher_id, test_name) VALUES (:test_id, :teacher_id, :test_name)"), flask.request.form)
        conn.commit()
        return flask.render_template('create_question.html')

#create question
@app.route('/create_question', methods = ['GET'])
def get_create_question():
    return flask.render_template('create_question.html')

@app.route('/create_question', methods=['POST'])
def create_question():
    conn.execute(text("INSERT INTO tests (test_id, test_question, answer) VALUES (:test_id, :test_question, :answer)"),
                 flask.request.form)
    conn.commit()
    return render_template('create_question.html')
#home
@app.route('/')
def homepage():
    return flask.render_template('create_acc.html')

#accounts
@app.route('/accounts_page', methods=['GET', 'POST'])
def search():
    if flask.request.method == 'GET':
        all_accounts = conn.execute(text("SELECT * FROM users")).fetchall()
        return flask.render_template('accounts_page.html', info_type = all_accounts)
    elif flask.request.method == 'POST':
        x = flask.request.form['type']
        account_info = conn.execute(text("SELECT * FROM users WHERE type = :type"), {'type': x}).fetchall()
        return flask.render_template('accounts_page.html', info_type=account_info)

#Filter
@app.route('/filter', methods=['GET'])
def searches():
    return flask.render_template('filter.html', info_type=[])


@app.route('/filter', methods=['POST'])
def search_account():
    x = flask.request.form['type']
    account_info = conn.execute(text(f"SELECT * FROM users WHERE type = :type"), {'type': x}).fetchall()
    return flask.render_template('filter.html', info_type=account_info)

#show tests
@app.route('/show_test')
def show_tests():
    tests = conn.execute(text('select * from tests')).all()
    return flask.render_template('show_tests.html', show_tests=tests)


#create acc
@app.route('/create_acc', methods=['GET'])
def create_get_request():
    return flask.render_template('create_acc.html')


@app.route('/create_acc', methods=['POST'])
def create_account():
    type = request.form.get('type')
    name = request.form.get('name')
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    conn.execute(text(
        'INSERT INTO users (type, name, email, username, password) VALUES (:type, :name, :email, :username, :password)'),
                 {'type': type, 'name': name, 'email': email, 'username': username, 'password': password})
    conn.commit()
    return flask.render_template("create_acc.html")


#take test
@app.route('/take_test', methods=['GET'])
def refresh():
    return render_template('take_test.html', test_info=[])

@app.route('/take_test', methods=['POST'])
def get_test():
    test_id = request.form.get('test_id')
    tester_id = request.form.get('tester_id')
    test_info = conn.execute(text('SELECT * FROM tests WHERE test_id = :id'), test_id=test_id).fetchall()
    return render_template('take_test.html', test_info=test_info)


#update
@app.route('/update_test', methods=['GET'])
def update():
    return flask.render_template('update.html')


@app.route('/update_test', methods=['POST'])
def update_boat():
    x = flask.request.form['test_id']
    name = flask.request.form['teacher_id']
    boat_type = flask.request.form['test_name']
    owner_id = flask.request.form['test_answer']
    boat = conn.execute(text(f'select * from tests where test_id = {x}'))
    conn.execute(text(f"UPDATE tests SET teacher_id = :teacher_id, test_name = :test_name, test_answer = test_answer WHERE {x} = :test_id "), flask.request.form)
    conn.commit()
    return flask.render_template('update.html')


#delete
@app.route('/delete_test', methods=["GET", "POST"])
def delete_boats():
    if flask.request.method == "POST":
        conn.execute(text("DELETE FROM tests WHERE test_id = :test_id"), flask.request.form)
        conn.commit()

        return flask.redirect("/create_test")
    else:
        return flask.render_template("delete_test.html")


if __name__ == '__main__':
    app.run(debug=True)

