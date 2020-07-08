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
app.config['MYSQL_DB'] = 'mhs'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)
@app.route("/")
@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']
        # Create cursor
        cur = mysql.connection.cursor()
        result = cur.execute(
            "SELECT * FROM userstore WHERE username = %s", [username])
        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']
            role = data['stakeholder']
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


@app.route("/index", methods=['GET', 'POST'])
def index():
    if session.get('username'):
        if request.method == 'POST':
            id = request.form['id']
            name = request.form['name']
            age = request.form['age']
            date = request.form['date']
            bed = request.form['bed']
            address = request.form['address']
            state = request.form['state']
            city = request.form['city']
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO patients(ssn_id,name,age,adm_date,bed_type,address,state,city) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)", (id, name, age, date, bed, address, state, city))
            mysql.connection.commit()
            cur.close()
            flash("New Patient created Succesfully.")
            return redirect(url_for('index'))
        return render_template('patient_reg.html')
    else:
        return redirect(url_for('login'))


def getpat_data(id):
    cur = mysql.connection.cursor()
    result = cur.execute(
        "SELECT * FROM patients WHERE id = %s", [id])
    if result > 0:
        data = []
        data_tup = cur.fetchall()
        for i in data_tup:
            data.append(i)
        return data
    return


def med_data(id):
    cur = mysql.connection.cursor()
    result = cur.execute(
        "SELECT * FROM medicine_master WHERE m_id = %s", [id])
    if result > 0:
        mdata = []
        data_tup = cur.fetchall()
        for i in data_tup:
            mdata.append(i)
        return mdata
    return


def getmed_data(id):
    cur = mysql.connection.cursor()
    result = cur.execute(
        "SELECT * FROM user_medicines WHERE p_id = %s", [id])
    if result > 0:
        mdata = []
        data_tup = cur.fetchall()
        for i in data_tup:
            med = med_data(i['med_id'])
            med.append(i['quantity'])
            mdata.append(med)
        return mdata
    return


def getdia_data(id):
    cur = mysql.connection.cursor()
    result = cur.execute(
        "SELECT * FROM diagnostics WHERE p_id = %s", [id])
    if result > 0:
        mdata = []
        data_tup = cur.fetchall()
        for i in data_tup:
            mdata.append(i)
        return mdata
    return


def getall_data():
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT * FROM patients")
    data = []
    data_tup = cur.fetchall()
    for i in data_tup:
        data.append(i)
    return data


def pat_exits(id):
    cur = mysql.connection.cursor()
    result = cur.execute(
        "SELECT * FROM patients WHERE id = %s", [id])
    if result > 0:
        return True
    return False


@app.route("/src_patient", methods=['GET', 'POST'])
def src_patient():
    if session.get('username'):
        if request.method == 'POST':
            id = request.form['id']
            if id != '':
                if pat_exits(id):
                    pat_data = getpat_data(id)
                    data = [pat_data]
                    flash('Patient Found Succesfully')
                    return render_template("patient_update.html", dta=data)
                else:
                    flash('Patient doesnot exits')
                    return redirect(url_for('update_pat'))
            else:
                flash('Please Enter Patient ID')
                return redirect(url_for('update_pat'))
        return redirect(url_for('update_pat'))
    else:
        return redirect(url_for('login'))


@app.route("/srch_patient1", methods=['GET', 'POST'])
def srch_patient1():
    if session.get('username'):
        if request.method == 'POST':
            id = request.form['id']
            if id != '':
                if pat_exits(id):
                    pat_data = getpat_data(id)
                    data = [pat_data]
                    flash('Patient Found Succesfully')
                    return render_template("search_patient.html", data=data)
                else:
                    flash('Patient doesnot exits')
                    return redirect(url_for('search_pat'))
            else:
                flash('Please Enter Patient ID')
                return redirect(url_for('search_pat'))
        return redirect(url_for('search_pat'))
    else:
        return redirect(url_for('login'))


@app.route("/update_pat", methods=['GET', 'POST'])
def update_pat():
    if session.get('username'):
        if request.method == 'POST':
            id = request.form['id']
            newname = request.form['newname']
            age = request.form['age']
            bed = request.form['bed']
            state = request.form['state']
            city = request.form['city']
            address = request.form['address']
            if newname == '':
                newname = request.form['oldname']
            if age == '':
                age = request.form['oldage']
            if bed == '':
                bed = request.form['oldbed']
            if address == '':
                address = request.form['oldaddress']
            if state == '':
                state = request.form['oldstate']
            if city == '':
                city = request.form['oldcity']
            cur = mysql.connection.cursor()
            cur.execute(
                "UPDATE patients set name=%s,age=%s,bed_type=%s,address=%s,state=%s,city=%s where id= %s", (newname, age, bed, address, state, city, id))
            mysql.connection.commit()
            cur.close()
            flash("Patient Updated Succesfully.")
            return redirect(url_for('update_pat'))
        else:
            return render_template('patient_update.html')
    else:
        return redirect(url_for('login'))


@app.route("/del_src_patient", methods=['GET', 'POST'])
def del_src_patient():
    if session.get('username'):
        if request.method == 'POST':
            id = request.form['id']
            if id != '':
                if pat_exits(id):
                    pat_data = getpat_data(id)
                    data = [pat_data]
                    flash('Patient Found Succesfully')
                    return render_template("patient_del.html", dta=data)
                else:
                    flash('Patient doesnot exits')
                    return redirect(url_for('delete_pat'))
            else:
                flash('Please Enter Patient ID')
                return redirect(url_for('delete_pat'))
        return redirect(url_for('delete_pat'))
    else:
        return redirect(url_for('login'))


@app.route("/delete_pat", methods=['GET', 'POST'])
def delete_pat():
    if session.get('username'):
        if request.method == 'POST':
            # Get Form Fields
            id = request.form['id']
            if pat_exits(id):
                cur = mysql.connection.cursor()
                result = cur.execute(
                    "DELETE  FROM patients WHERE id = %s", [id])
                mysql.connection.commit()
                cur.close()
                if result:
                    flash('Patient deletion initiated Successfully')
                    return redirect(url_for('delete_pat'))
                else:
                    flash('Couldnt Delete Account.')
                return redirect(url_for('delete_pat'))
            else:
                flash('No Patient Found.')
                return redirect(url_for('delete_pat'))
        else:
            return render_template("patient_del.html")
    else:
        return redirect(url_for('login'))


@app.route("/view_pat", methods=['GET', 'POST'])
def view_pat():
    if session.get('username'):
        data = getall_data()
        return render_template("view_patients.html", data=data)
    else:
        return redirect(url_for('login'))


@app.route("/search_pat", methods=['GET', 'POST'])
def search_pat():
    if session.get('username'):
        return render_template("search_patient.html")
    else:
        return redirect(url_for('login'))


@app.route("/issue_med", methods=['GET', 'POST'])
def issue_med():
    if session.get('username'):
        if request.method == 'POST':
            id = request.form['id']
            if id != '':
                if pat_exits(id):
                    pat_data = getpat_data(id)
                    data = [pat_data]
                    med_data = getmed_data(id)
                    flash('Patient Found Succesfully')
                    return render_template("issue_medicines.html", data=data, med=med_data)
                else:
                    flash('Patient doesnot exits')
                    return redirect(url_for('issue_med'))
            else:
                flash('Please Enter Patient ID')
                return redirect(url_for('issue_med'))
        else:
            return render_template("issue_medicines.html")
    else:
        return redirect(url_for('login'))


@app.route("/srch_patient_billing", methods=['GET', 'POST'])
def srch_patient_billing():
    if session.get('username'):
        if request.method == 'POST':
            id = request.form['id']
            if id != '':
                if pat_exits(id):
                    pat_data = getpat_data(id)
                    data = [pat_data]
                    med_data = getmed_data(id)
                    dia_data = getdia_data(id)
                    flash('Patient Found Succesfully')
                    return render_template("billing.html", data=data, med=med_data, d=dia_data)
                else:
                    flash('Patient doesnot exits')
                    return redirect(url_for('billing'))
            else:
                flash('Please Enter Patient ID')
                return redirect(url_for('billing'))
        return redirect(url_for('billing'))
    else:
        return redirect(url_for('login'))


@app.route("/billing", methods=['GET', 'POST'])
def billing():
    if session.get('username'):
        return render_template("billing.html")
    else:
        return redirect(url_for('login'))


@app.route("/srch_patient_dia", methods=['GET', 'POST'])
def srch_patient_dia():
    if session.get('username'):
        if request.method == 'POST':
            id = request.form['id']
            if id != '':
                if pat_exits(id):
                    pat_data = getpat_data(id)
                    data = [pat_data]
                    dia_data = getdia_data(id)
                    flash('Patient Found Succesfully')
                    return render_template("add_diagnostics.html", data=data, med=dia_data)
                else:
                    flash('Patient doesnot exits')
                    return redirect(url_for('add_diag'))
            else:
                flash('Please Enter Patient ID')
                return redirect(url_for('add_diag'))
        return redirect(url_for('add_diag'))
    else:
        return redirect(url_for('login'))


@app.route("/add_diag", methods=['GET', 'POST'])
def add_diag():
    if session.get('username'):
        return render_template("add_diagnostics.html")
    else:
        return redirect(url_for('login'))


@app.route("/logout")
def logout():
    session['logged_in'] = False
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    # session.init_app(app)
    app.debug = True
    app.run()
