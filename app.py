from flask import Flask, render_template, flash, redirect, request, url_for, session, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField
from passlib.hash import sha256_crypt
import random
from functools import wraps


app = Flask(__name__)
app.secret_key='some secret key'


#Config MySQL
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='alihamza000786'
app.config['MYSQL_DB']='bloodbank'
app.config['MYSQL_CURSORCLASS']='DictCursor'
#init MySQL
mysql =  MySQL(app)


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/contact', methods=['GET','POST'])
def contact():
    if request.method == 'POST':
        bgroup = request.form["bgroup"]
        bpackets = request.form["bpackets"]
        fname = request.form["fname"]
        adress = request.form["adress"]

        #create a cursor
        cur = mysql.connection.cursor()

        #Inserting values into tables
        cur.execute("INSERT INTO CONTACT(B_GROUP,C_PACKETS,F_NAME,ADRESS) VALUES(%s, %s, %s, %s)",(bgroup, bpackets, fname, adress))
        cur.execute("INSERT INTO NOTIFICATIONS(NB_GROUP,N_PACKETS,NF_NAME,NADRESS) VALUES(%s, %s, %s, %s)",(bgroup, bpackets, fname, adress))
        #Commit to DB
        mysql.connection.commit()
        #close connection
        cur.close()
        flash('Your request is successfully sent to the Blood Bank','success')
        return redirect(url_for('notifications'))

    return render_template('contact.html')


class RegisterForm(Form):
    name = StringField('Name', [validators.DataRequired(),validators.Length(min=1,max=25)])
    email = StringField('Email',[validators.DataRequired(),validators.Length(min=10,max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm',message='Password do not match')
    ])
    confirm = PasswordField('Confirm Password')

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm(request.form)
    if request.method  == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))
        e_id = name+str(random.randint(1111,9999))
        #Create cursor
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO RECEPTION(E_ID,NAME,EMAIL,PASSWORD) VALUES(%s, %s, %s, %s)",(e_id, name, email, password))
        #Commit to DB
        mysql.connection.commit()
        #close connection
        cur.close()
        flashing_message = "Success! You can log in with Employee ID " + str(e_id)
        flash( flashing_message,"success")

        return redirect(url_for('login'))

    return render_template('register.html',form = form)

#login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        e_id = request.form["e_id"]
        password_candidate = request.form["password"]

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM RECEPTION WHERE E_ID = %s", [e_id])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['PASSWORD']

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['e_id'] = e_id

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'Employee ID not found'
            return render_template('login.html', error=error)

    return render_template('login.html')

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login!', 'danger')
            return redirect(url_for('login'))
    return wrap

#Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('index'))

@app.route('/dashboard')
@is_logged_in
def dashboard():
    cur = mysql.connection.cursor()
    cur.callproc('BLOOD_DATA')
    details = cur.fetchall()

    if len(details) > 0:
        return render_template('dashboard.html', details=details)
    else:
        msg = ' Blood Bank is Empty '
        return render_template('dashboard.html', msg=msg)
    #close connection
    cur.close()

@app.route('/donate', methods=['GET', 'POST'])
@is_logged_in
def donate():
    if request.method  == 'POST':
        # Get Form Fields
        dname = request.form["dname"]
        sex = request.form["sex"]
        age = request.form["age"]
        weight = request.form["weight"]
        bloodgroup=request.form["bloodgroup"]
        disease =  request.form["disease"]
        address = request.form["address"]
        demail = request.form["demail"]

        #create a cursor
        cur = mysql.connection.cursor()

        #Inserting values into tables
        cur.execute("INSERT INTO DONOR(DNAME,SEX,AGE,WEIGHT,DISEASE,ADDRESS,DEMAIL,BLOODGROUP) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",(dname , sex, age, weight, disease, address, demail,bloodgroup))
        #Commit to DB
        mysql.connection.commit()
        #close connection
        cur.close()
        flash('Success! Donor details Added.','success')
        return redirect(url_for('donorlogs'))

    return render_template('donate.html')

@app.route('/donorlogs')
@is_logged_in
def donorlogs():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM DONOR")
    logs = cur.fetchall()

    if result>0:
        return render_template('donorlogs.html',logs=logs)
    else:
        msg = ' No logs found '
        return render_template('donorlogs.html',msg=msg)
    #close connection
    cur.close()


@app.route('/bloodform', methods=['GET', 'POST'])
@is_logged_in
def bloodform():
    if request.method == 'POST':
        # Get Form Fields
        d_id = request.form["d_id"]
        packets = request.form["packets"]

        # Create a cursor
        cur = mysql.connection.cursor()

        # Fetch the blood group for the given donor ID
        cur.execute("SELECT bloodgroup FROM donor WHERE D_ID = %s", (d_id,))
        rec = cur.fetchone()

        if rec:
            blood_group = rec['bloodgroup']  # Correctly extract the blood group from the dictionary
        else:
            flash('The Donor with this ID does not exist', 'danger')
            return render_template('bloodform.html')

        # Check if the blood group exists in BLOODBANK
        cur.execute("SELECT * FROM BLOODBANK WHERE B_GROUP = %s", (blood_group,))
        record = cur.fetchone()

        if record:
            # Update the total packets if the blood group exists
            cur.execute("UPDATE BLOODBANK SET TOTAL_PACKETS = TOTAL_PACKETS + %s WHERE B_GROUP = %s", (packets, blood_group))
        else:
            # Insert a new record for the blood group if it doesn't exist
            cur.execute("INSERT INTO BLOODBANK(B_GROUP, TOTAL_PACKETS) VALUES(%s, %s)", (blood_group, packets))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('Success! Donor Blood details Added.', 'success')
        return redirect(url_for('dashboard'))

    return render_template('bloodform.html')



@app.route('/notifications')
@is_logged_in
def notifications():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM CONTACT WHERE STATUS=%s", ('fasle',))
    requests = cur.fetchall()

    if result>0:
        return render_template('notification.html',requests=requests)
    else:
        msg = ' No requests found '
        return render_template('notification.html',msg=msg)
    #close connection
    cur.close()

@app.route('/notifications/accept/<int:contact_id>', methods=['GET'])
def accept_request(contact_id):
    cur = mysql.connection.cursor()

    # Retrieve the request details
    cur.execute("SELECT B_GROUP, C_PACKETS FROM contact WHERE CONTACT_ID = %s", (contact_id,))
    request_details = cur.fetchone()
    print(f"Fetched request details: {request_details}")

    if request_details:
        blood_group=request_details['B_GROUP']
        requested_packets = request_details['C_PACKETS']

        # Retrieve the current packets in blood bank for the blood group
        cur.execute("SELECT TOTAL_PACKETS FROM BLOODBANK WHERE B_GROUP = %s", (blood_group,))
        bloodbank_details = cur.fetchone()
        if bloodbank_details:
            current_packets = bloodbank_details['TOTAL_PACKETS']

            # Check if enough packets are available
            if current_packets >= requested_packets:
                # Deduct the packets
                new_packets = current_packets - requested_packets
                cur.execute("UPDATE BLOODBANK SET TOTAL_PACKETS = %s WHERE B_GROUP = %s", (new_packets, blood_group))


                cur.execute("UPDATE CONTACT SET STATUS =%s WHERE CONTACT_ID = %s", ('true',contact_id,))
                # Commit the transaction
                mysql.connection.commit()

                flash('Blood request accepted and packets deducted from the blood bank.', 'success')
            else:
                flash('Not enough blood packets available.', 'danger')
        else:
            flash('Blood group not found in blood bank.', 'danger')
    else:
        flash('Blood request not found.', 'danger')

    cur.close()
    return redirect(url_for('acceptlogs'))






@app.route('/acceptlogs')
@is_logged_in
def acceptlogs():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM contact WHERE status=%s", ('true',))
    logs = cur.fetchall()

    if result>0:
        return render_template('acceptrequests.html',logs=logs)
    else:
        flash('No Accept Requests')
        return render_template('acceptrequests.html',logs=logs)
    #close connection
    cur.close()






@app.route('/notifications/decline/<int:contact_id>', methods=['GET', 'POST'])
@is_logged_in
def decline(contact_id):
    msg = 'Request Declined'
    flash(msg,'danger')
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM CONTACT WHERE CONTACT_ID = %s", (contact_id,))
    # Commit the transaction
    mysql.connection.commit()
    return redirect(url_for('notifications'))

if __name__ == '__main__':
    app.run(debug=True)
