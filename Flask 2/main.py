from imghdr import tests

from flask import Flask, render_template, request, redirect
from sqlalchemy import create_engine, text

app = Flask(__name__)

conn_str = 'mysql://root:Cookiebear1@localhost/flask'
engine = create_engine(conn_str, echo = True)
conn = engine.connect()

#Create test
@app.route('/create_test', methods=['GET'])
def create_get_test():
    return render_template("create_test.html")

@app.route('/create_test', methods=['POST'])
def create_test():
    test_id = request.form.get("test_id")
    teacher_id = request.form.get("teacher_id")
    test_name = request.form.get("test_name")
    test_answer = request.form.get("test_answer")
    test_question = request.form.get("test_question")

    sql = text("INSERT INTO tests (test_id, teacher_id, test_name, test_answer) "
               "VALUES (:test_id, :teacher_id, :test_name, :test_answer)")
    conn.execute(sql, {"test_id": test_id, "teacher_id": teacher_id, "test_name": test_name, "test_answer": test_answer})

    sql = text("INSERT INTO questions (test_question) VALUES (:test_question)")
    conn.execute(sql, {"test_question": test_question})
    conn.commit()

    return render_template("create_test.html")

#homepage
@app.route('/')
def homepage():
    return render_template('create_acc.html')

#accounts
@app.route('/accounts_page', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        all_accounts = conn.execute(text("SELECT * FROM users")).fetchall()
        return render_template('accounts_page.html', info_type = all_accounts)
    elif request.method == 'POST':
        x = request.form['type']
        account_info = conn.execute(text("SELECT * FROM users WHERE type = :type"), {'type': x}).fetchall()
        return render_template('accounts_page.html', info_type=account_info)

#Filter
@app.route('/filter', methods=['GET'])
def searches():
    return render_template('filter.html', info_type=[])


@app.route('/filter', methods=['POST'])
def search_account():
    x = request.form['type']
    account_info = conn.execute(text(f"SELECT * FROM users WHERE type = :type"), {'type': x}).fetchall()
    return render_template('filter.html', info_type=account_info)


#create acc
@app.route('/create_acc', methods=['GET'])
def create_get_request():
    return render_template('create_acc.html')


@app.route('/create_acc', methods=['POST'])
def create_boats():
    conn.execute(text('INSERT into users Values (:user_id, :type, :name, :email, :username, :password)'), request.form)
    conn.commit()
    return render_template('create_acc.html')


#take test
@app.route('/take_test', methods=['GET'])
def refresh():
    return render_template('take_test.html')


@app.route('/take_test', methods=['POST'])
def get_test():
    x = request.form['test_id']
    boat = conn.execute(text(f'select * from tests where test_id = {x}'))
    conn.execute(text(f"select * from tests where test_id = {x}"), request.form)
    conn.commit()
    return render_template('take_test.html', test_info=boat)


#update
@app.route('/update_test', methods=['GET'])
def update():
    return render_template('update.html')


@app.route('/update_test', methods=['POST'])
def update_boat():
    x = request.form['test_id']
    name = request.form['teacher_id']
    boat_type = request.form['test_name']
    owner_id = request.form['test_answer']
    boat = conn.execute(text(f'select * from tests where test_id = {x}'))
    conn.execute(text(f"UPDATE tests SET test_id = :test_id, teacher_id = :teacher_id, test_name = :test_name WHERE {x} = :test_id "), request.form)
    conn.commit()
    return render_template('update.html')


#delete
@app.route('/delete_test', methods=["GET", "POST"])
def delete_boats():
    if request.method == "POST":
        conn.execute(text("DELETE FROM tests WHERE test_id = :test_id"), request.form)
        conn.commit()

        return redirect("/create_test")
    else:
        return render_template("delete_test.html")


if __name__ == '__main__':
    app.run(debug=True)

