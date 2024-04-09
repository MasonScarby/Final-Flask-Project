from flask import Flask, render_template, request, redirect
from sqlalchemy import create_engine, text

app = Flask(__name__)

conn_str = 'mysql://root:Cookiebear1@localhost/flask'
engine = create_engine(conn_str, echo = True)
conn = engine.connect()

#homepage
@app.route('/')
def homepage():
    return render_template('index.html')


#show accounts
# @app.route("/accounts_page")
# def get_accounts():
#     users = conn.execute(text("select * from users")).all()
#     return render_template('accounts_page.html', user = users[:10])

#Filter
@app.route('/accounts_page', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        all_accounts = conn.execute(text("SELECT * FROM users")).fetchall()
        return render_template('accounts_page.html', info_type = all_accounts)
    elif request.method == 'POST':
        x = request.form['type']
        account_info = conn.execute(text("SELECT * FROM users WHERE type = :type"), {'type': x}).fetchall()
        return render_template('accounts_page.html', info_type=account_info)


# @app.route("/<name>")
# def welcome(name):
#     return render_template('user.html', username = name)

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
    return  render_template('create_acc.html')


@app.route('/create_acc', methods=['POST'])
def create_boats():
    conn.execute(text('INSERT into users Values (:type, :name, :email, :username, :password)'), request.form)
    conn.commit()
    return render_template('create_acc.html')



#update
@app.route('/update', methods=['GET'])
def update_request():
    return  render_template('update.html')

@app.route('/update', methods=['POST'])
def update():
    conn.execute(text('UPDATE users Set name = :name, type = :type, owner_id = :owner_id, rental_price = :rental_price WHERE id = :id'), request.form)
    conn.commit()
    return  render_template('update.html')

@app.route('/delete_boat', methods=["GET", "POST"])
def delete_boats():
    if request.method == "POST":
        conn.execute(text("DELETE FROM boats WHERE id = :id"), request.form)
        conn.commit()
        return redirect("/boats")
    else:
        return render_template("delete_boat.html")


if __name__ == '__main__':
    app.run(debug=True)

