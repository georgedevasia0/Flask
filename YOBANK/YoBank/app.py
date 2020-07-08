from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from datetime import datetime
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

app = Flask(__name__)
app.secret_key = "superdefrsecret45grkey"

# config mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'yobank'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# init mysql
mysql = MySQL(app)
@app.route("/login")
@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()
        result = cur.execute(
            "SELECT * FROM userstore WHERE id = %s", [username])
        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']
            role = data['role']
            if password == password_candidate:
                session['logged_in'] = True
                session['username'] = data['username']
                session['role'] = role
                return redirect(url_for('index'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
                # Close connection
                cur.close()
        else:
            error = 'Invalid Username or Password'
            return render_template('login.html', error=error)
    return render_template('login.html')


@app.route("/index")
def index():
    if session.get('username'):
        return render_template("home.html")
    else:
        return redirect(url_for('login'))


@app.route("/create_customer", methods=['GET', 'POST'])
def create_customer():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        age = request.form['age']
        address = request.form['address']
        state = request.form['state']
        city = request.form['city']
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO customer(ssn_id,name,age,address,state,city) VALUES(%s,%s,%s,%s,%s,%s)", (id, name, age, address, state, city))
        mysql.connection.commit()
        cur.close()
        flash("New Customer created Succesfully.")
        return redirect(url_for('create_customer'))
    else:
        return render_template("create_customer.html")


def getid():
    acc_id = ''
    cur = mysql.connection.cursor()
    result = cur.execute(
        "SELECT MAX(acc_id) from accounts")
    if result > 0:
        data = cur.fetchone()
        acc_id = data['MAX(acc_id)']
        acc_id += 1
    else:
        acc_id = 1000000
    return acc_id


def account(id, account_type):
    cur = mysql.connection.cursor()
    result = cur.execute(
        "SELECT * FROM accounts WHERE c_id = %s", [id])
    if result > 0:
        data = cur.fetchall()
        for d in data:
            if account_type in d['acc_type']:
                return False
        return True
    else:
        return True


def accountfind(id, account_type):
    cur = mysql.connection.cursor()
    result = cur.execute(
        "SELECT * FROM accounts WHERE acc_id = %s", [id])
    if result > 0:
        data = cur.fetchone()
        if account_type == data['acc_type']:
            return True
        return False
    else:
        return True


def cust_exits(id):
    cur = mysql.connection.cursor()
    result = cur.execute(
        "SELECT * FROM customer WHERE ssn_id = %s", [id])
    if result > 0:
        return True
    return False


def getaccount_data(accid):
    cur = mysql.connection.cursor()
    result = cur.execute(
        "SELECT * FROM accounts WHERE acc_id = %s", [accid])
    if result > 0:
        data = cur.fetchone()
        return data
    return


def getaccount_data1(custid):
    cur = mysql.connection.cursor()
    result = cur.execute(
        "SELECT * FROM accounts WHERE c_id = %s", [custid])
    if result > 0:
        data = []
        data_tup = cur.fetchall()
        for i in data_tup:
            data.append(i)
        return data
    return


def getcust_data(id):
    cur = mysql.connection.cursor()
    result = cur.execute(
        "SELECT * FROM customer WHERE ssn_id = %s", [id])
    if result > 0:
        data = []
        data_tup = cur.fetchall()
        for i in data_tup:
            data.append(i)
        return data
    return


def getname(c_id):
    cur = mysql.connection.cursor()
    result = cur.execute(
        "SELECT * FROM customer WHERE ssn_id = %s", [c_id])
    if result > 0:
        data = cur.fetchone()
        return data['name']
    return


def getcust_id(id):
    cur = mysql.connection.cursor()
    result = cur.execute(
        "SELECT * FROM accounts WHERE acc_id = %s", [id])
    if result > 0:
        data = cur.fetchone()
        return data['c_id']
    return


def getamount(accid):
    cur = mysql.connection.cursor()
    result = cur.execute(
        "SELECT * FROM accounts WHERE acc_id = %s", [accid])
    if result > 0:
        data = cur.fetchone()
        return data['amount']
    return


def accid_exits(accid):
    cur = mysql.connection.cursor()
    result = cur.execute(
        "SELECT * FROM accounts WHERE acc_id = %s", [accid])
    if result > 0:
        return True
    return False


@app.route("/create_account", methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        id = request.form['id']
        if cust_exits(id):
            account_type = request.form['account']
            amount = request.form['amount']
            if account(id, account_type):
                acc_id = getid()
                cur = mysql.connection.cursor()
                cur.execute(
                    "INSERT INTO accounts(acc_id,c_id,acc_type,amount) VALUES(%s,%s,%s,%s)", (acc_id, id, account_type, amount))
                mysql.connection.commit()
                cur.close()
                flash("New Account created Succesfully.")
            else:
                flash("Sorry, You already have a "+account_type + " account")
        else:
            flash("Invalid Customer ID, Check again")
        return redirect(url_for('create_account'))
    return render_template("create_account.html")


@app.route("/search_customer", methods=['GET', 'POST'])
def search_customer():
    if request.method == 'POST':
        id = request.form['id']
        aid = request.form['aid']
        if id == '' and aid == '':
            flash("Please Enter SSN ID or Account ID")
            return redirect(url_for('search_customer'))
        elif id != '':
            if cust_exits(id):
                flash("Yes")
                data = []
                cust_data = getcust_data(id)
                data = [cust_data]
                return render_template("customer_search.html", data=data)
            else:
                flash('Sorry, Customer ID not Found')
                return redirect(url_for('search_customer'))
        elif aid != '':
            if accid_exits(aid):
                flash("Yes")
                data = []
                acc_data = getaccount_data(aid)
                cust_id = getcust_id(acc_data['acc_id'])
                cust_data = getcust_data(cust_id)
                data = [cust_data]
                return render_template("customer_search.html", data=data)
            else:
                flash('Sorry, Account ID not Found')
                return redirect(url_for('search_customer'))
        return redirect(url_for('search_customer'))
    else:
        return render_template("customer_search.html")


@app.route("/srch_customer", methods=['GET', 'POST'])
def srch_customer():
    if request.method == 'POST':
        id = request.form['id']
        if cust_exits(id):
            cust_data = getcust_data(id)
            data = [cust_data]
            return render_template("update_customer.html", cust=data)
        else:
            flash('Customer doesnot exits')
            return redirect(url_for('update_customer'))
    return redirect(url_for('update_customer'))


@app.route("/search_cust", methods=['GET', 'POST'])
def search_cust1():
    if request.method == 'POST':
        id = request.form['cid']
        if id != '':
            if cust_exits(id):
                cust_data = getcust_data(id)
                data = [cust_data]
                return render_template("delete_customer.html", cust=data)
            else:
                flash('Customer doesnot exits')
                return redirect(url_for('delete_customer'))
        else:
            flash('Please Enter Customer SSN ID')
            return redirect(url_for('delete_customer'))
    return redirect(url_for('delete_customer'))


@app.route("/update_customer", methods=['GET', 'POST'])
def update_customer():
    if request.method == 'POST':
        id = request.form['id']
        newname = request.form['newname']
        age = request.form['age']
        address = request.form['address']
        if newname != '' and age != '' and address != '':
            message = "Account Updated"
            time = datetime.now()
            cur = mysql.connection.cursor()
            cur.execute(
                "UPDATE customer set name=%s,age=%s,address=%s,message=%s,last_updated=%s where ssn_id= %s", (newname, age, address, message, time, id))
            mysql.connection.commit()
            cur.close()
            flash("Customer Updated Succesfully.")
            return redirect(url_for('update_customer'))
        else:
            flash("Sorry, Couldn't update.")
            return redirect(url_for('update_customer'))
    else:
        return render_template("update_customer.html")


@app.route("/account_search", methods=['GET', 'POST'])
def account_search():
    if request.method == 'POST':
        accid = request.form['accid']
        custid = request.form['custid']
        if accid == '' and custid == '':
            flash("Please Enter Account ID or Customer ID")
            return redirect(url_for('account_search'))
        elif accid != '':
            if accid_exits(accid):
                flash("Yes")
                data = []
                acc_data = getaccount_data(accid)
                acc_holder = getname(acc_data['c_id'])
                data = [acc_data['acc_id'], acc_data['c_id'],
                        acc_data['acc_type'], acc_data['amount'], acc_holder]
                return render_template("account_search.html", data=data)
            else:
                flash('Sorry, Account ID not Found')
                return redirect(url_for('account_search'))
        elif custid != '':
            if cust_exits(custid):
                flash("Yes")
                data = []
                acc_data = getaccount_data1(custid)
                acc_holder = getname(acc_data[0]['c_id'])
                data = [acc_data, acc_holder]
                return render_template("account_search.html", data1=data)
            else:
                flash('Sorry, Customer ID not Found')
                return redirect(url_for('account_search'))
        return redirect(url_for('account_search'))
    else:
        return render_template("account_search.html")


@app.route("/delete_customer", methods=['GET', 'POST'])
def delete_customer():
    if request.method == 'POST':
        # Get Form Fields
        id = request.form['id']
        if cust_exits(id):
            cur = mysql.connection.cursor()
            result = cur.execute(
                "DELETE  FROM customer WHERE ssn_id = %s", [id])
            mysql.connection.commit()
            cur.close()
            if result:
                flash('Account Deleted Successfully')
                return redirect(url_for('delete_customer'))
            else:
                flash('Couldnt Delete Account.')
            return redirect(url_for('delete_customer'))
        else:
            flash('No Customer Found.')
            return redirect(url_for('delete_customer'))
    else:
        return render_template("delete_customer.html")


@app.route("/delete_account", methods=['GET', 'POST'])
def delete_account():
    if request.method == 'POST':
        accid = request.form['accid']
        if accid_exits(accid):
            acc_type = request.form['account']
            if accountfind(accid, acc_type):
                cur = mysql.connection.cursor()
                cur.execute(
                    "DELETE from accounts where acc_id = %s ", [accid])
                mysql.connection.commit()
                cur.close()
                flash(" Account deleted Succesfully.")
            else:
                flash('Account Not Found')
                return redirect(url_for('delete_account'))
        else:
            flash('Account Not Found')
            return redirect(url_for('delete_account'))
    return render_template("delete_account.html")


@app.route("/account_status", methods=['GET', 'POST'])
def account_status():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM accounts")
    if result > 0:
        d = []
        data = cur.fetchall()
        for i in data:
            d.append(i)
    return render_template("account_status.html", data=d)


@app.route("/customer_status")
def customer_status():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM accounts")
    if result > 0:
        d = []
        data = cur.fetchall()
        for i in data:
            d.append(i)
    return render_template("customer_status.html", data=d)


@app.route("/deposit_money", methods=['GET', 'POST'])
def deposit_money():
    if request.method == 'POST':
        if request.form['submit'] == 'getaccount':
            accid = request.form['accid']
            if accid_exits(accid):
                amt = request.form['amount']
                oldamt = getamount(accid)
                data = []
                acc_data = getaccount_data(accid)
                acc_holder = getname(acc_data['c_id'])
                data = [acc_data['acc_id'], acc_data['c_id'],
                        acc_data['acc_type'], acc_data['amount'], acc_holder, oldamt, amt]
                return render_template("deposit_money.html", data=data)
            else:
                flash('Account Not Found')
                return redirect(url_for('deposit_money'))

        elif request.form['submit'] == 'deposit':
            accid = request.form['accid']
            if accid_exits(accid):
                amt = request.form['amount']
                oldamt = getamount(accid)
                amt1 = int(amt)+int(oldamt)
                message = "Money deposited Successfully"
                time = datetime.now()
                cur = mysql.connection.cursor()
                cur.execute(
                    "UPDATE accounts set amount=%s,message=%s,last_updated=%s where acc_id=%s", (amt1, message, time, accid))
                cur.execute(
                    "INSERT into transactions(description,amount) values(%s,%s)", (
                        message, amt)
                )
                mysql.connection.commit()
                cur.close()
                data1 = []
                acc_data = getaccount_data(accid)
                acc_holder = getname(acc_data['c_id'])
                data1 = [acc_data['acc_id'], acc_data['c_id'],
                         acc_data['acc_type'], acc_data['amount'], acc_holder]
                btn = True
                flash('Money deposited Successfully')
                return render_template("deposit_money.html", btn=btn, data1=data1)
            else:
                flash('Account Not Found')
                return redirect(url_for('deposit_money'))
        return redirect(url_for('deposit_money'))
    else:
        return render_template("deposit_money.html")


@app.route("/transfer_money", methods=['GET', 'POST'])
def transfer_money():
    if request.method == 'POST':
        fid = request.form['fid']
        tid = request.form['tid']
        if accid_exits(fid):
            if accid_exits(tid):
                amt = request.form['amt']
                foldamt = getamount(fid)
                toldamt = getamount(tid)
                famt1 = int(foldamt)-int(amt)
                if famt1 >= 0:
                    tamt1 = int(amt)+int(toldamt)
                    message1 = "Money Transfered"
                    message2 = "Money Credited"
                    time = datetime.now()
                    cur = mysql.connection.cursor()
                    cur.execute(
                        "UPDATE accounts set amount=%s,message=%s,last_updated=%s where acc_id=%s", (famt1, message1, time, fid))
                    cur.execute(
                        "UPDATE accounts set amount=%s,message=%s,last_updated=%s where acc_id=%s", (tamt1, message2, time, tid))
                    cur.execute(
                        "INSERT into transactions(description,amount) values(%s,%s)", (message1, amt))
                    cur.execute(
                        "INSERT into transactions(description,amount) values(%s,%s)", (message2, amt))
                    mysql.connection.commit()
                    cur.close()
                    data1 = []
                    acc_data = getaccount_data(fid)
                    acc_holder = getname(acc_data['c_id'])
                    data1 = [acc_data['acc_id'], acc_data['c_id'],
                             acc_data['acc_type'], acc_data['amount'], acc_holder]
                    acc_data1 = getaccount_data(tid)
                    acc_holder1 = getname(acc_data['c_id'])
                    data2 = [acc_data1['acc_id'], acc_data1['c_id'],
                             acc_data1['acc_type'], acc_data1['amount'], acc_holder1]
                    btn = True
                    datax1 = [data1, data2]
                    flash('Money Transfered Succesfully')
                    return render_template("transfer_money.html", done=btn, data1=datax1)
                else:
                    flash('Insufficient Funds')
                    return redirect(url_for('transfer_money'))
            else:
                flash('To Account doesnt exits')
                return redirect(url_for('transfer_money'))
        else:
            flash('From Account doesnt exits')
            return redirect(url_for('transfer_money'))
    else:
        return render_template("transfer_money.html")


@app.route("/withdraw_money", methods=['GET', 'POST'])
def withdraw_money():
    if request.method == 'POST':
        if request.form['submit'] == 'getaccount':
            accid = request.form['accid']
            if accid_exits(accid):
                amt = request.form['amount']
                oldamt = getamount(accid)
                data = []
                acc_data = getaccount_data(accid)
                acc_holder = getname(acc_data['c_id'])
                data = [acc_data['acc_id'], acc_data['c_id'],
                        acc_data['acc_type'], acc_data['amount'], acc_holder, oldamt, amt]
                return render_template("withdraw_money.html", data=data)
            else:
                flash('Account Not Found')
                return redirect(url_for('withdraw_money'))

        elif request.form['submit'] == 'withdraw':
            accid = request.form['accid']
            if accid_exits(accid):
                amt = request.form['amount']
                oldamt = getamount(accid)
                amt1 = int(oldamt)-int(amt)
                if amt1 >= 0:
                    message = "Money Withdrawn Successfully"
                    time = datetime.now()
                    cur = mysql.connection.cursor()
                    cur.execute(
                        "UPDATE accounts set amount=%s,message=%s,last_updated=%s where acc_id=%s", (amt1, message, time, accid))
                    cur.execute(
                        "INSERT into transactions(description,amount) values(%s,%s)", (message, amt))
                    mysql.connection.commit()
                    cur.close()
                    data1 = []
                    acc_data = getaccount_data(accid)
                    acc_holder = getname(acc_data['c_id'])
                    data1 = [acc_data['acc_id'], acc_data['c_id'],
                             acc_data['acc_type'], acc_data['amount'], acc_holder]
                    btn = True
                    flash('Money Withdrawn Successfully')
                    return render_template("withdraw_money.html", btn=btn, data1=data1)
                else:
                    flash('Insufficient Funds')
                    return redirect(url_for('withdraw_money'))
            else:
                flash('Account Not Found')
                return redirect(url_for('withdraw_money'))
        return redirect(url_for('withdraw_money'))
    else:
        return render_template("withdraw_money.html")


@app.route("/print_statements", methods=['GET', 'POST'])
def print_statements():
    data = []
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM transactions")
    if result > 0:
        d = []
        data = cur.fetchall()
        for i in data:
            d.append(i)
    return render_template("print_statements.html", data=d)


@app.route("/logout")
def logout():
    session['logged_in'] = False
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    #session.init_app(app)
    app.debug = True
    app.run()
