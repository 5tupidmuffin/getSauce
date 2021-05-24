#  file for user related actions
"""
to be done :
    add session functionality
"""

from flask import Blueprint, request, redirect, url_for, session, render_template, send_from_directory, current_app
from getSauce import db, logit
from models import *
from validation import passwordValidation, usernameValidation
from jsonexport import exportData


user = Blueprint('user', __name__)

def fetchAllResults(username):
    all_results = results.query.filter_by(username= username).all()
    return all_results

#  go to the login page
@user.route('/login', methods = ['GET', 'POST'])
def login():  # dummy login
    error = None
    if request.method == 'POST':

        user = request.form['username']
        password = request.form['password']
        if (user == "") or (password == ""):
            return render_template('./auth/login.html', msg = "Check for empty input fields")

        found_user = users.query.filter_by(username = user, password = password).first()  # check if user is in database
        if found_user:
            logit("User Logged In : " + user)
            session["ActiveUser"] = user  # setup a session for user
            return redirect(url_for('user.accountInfo'))  # if exists go to acc page
        else:
            return render_template('./auth/login.html', msg= 'whoa there, you entered wrong credentials!')  # if doesnt go to register page
    else:
        if 'ActiveUser' in session:
            return redirect(url_for('user.accountInfo'))
        logit('Displaying login Page')
        return render_template('./auth/login.html', msg = request.args.get('msg'))

#  create an account page
@user.route('/register', methods = ["GET", "POST"])
def register():
    if 'ActiveUser' in session:
        return redirect(url_for('user.accountInfo'))
    
    if request.method == 'POST':  # assuming username doesnt already exist in database
        user = request.form['username']
        password = request.form['password']
        emailid = request.form['emailid']

        if emailid == "":
            emailid = None
        print('email id =', emailid)


        if (user == "") or (password == ""):
            return render_template('./auth/register.html', error = "Check for empty input fields")

        if usernameValidation(user) != True:
            return render_template('./auth/register.html', error = usernameValidation(user))

        checkUser = users.query.filter_by(username = user).first()  # if username exists in db

        if checkUser:
            return render_template('./auth/register.html', error = "Username Already Exists")
        
        checkEmail = users.query.filter_by(email = emailid).first()  # if email already exists in database

        if (checkEmail) and (checkEmail.email is not None):
            return render_template('./auth/register.html', error = "Email Already Exists")

        if passwordValidation(password) == True:
            if usernameValidation(user) == True:
                newUser = users(user, password, emailid)
                print('email id =', emailid)
                db.session.add(newUser)  # add new user
                db.session.commit()
                logit("user created with username: " + user)
                session['ActiveUser'] = user
                return render_template('./auth/account.html')  # goto the account page
            else:
                return render_template('./auth/register.html', error = usernameValidation(user))
        else:
            return render_template('./auth/register.html', error = passwordValidation(password))

    else:
        if 'ActiveUser' in session:
            return redirect(url_for('user.accountInfo'))

        logit("Displaying Register Page")
        return render_template('./auth/register.html')

#  go to accunt info page
@user.route('/accountinfo')
def accountInfo():
    if 'ActiveUser' in session:
        allresults = fetchAllResults(session['ActiveUser'])
        if allresults is not None:
            logit("Displaying Account Page")
            return render_template('./auth/account.html', results= reversed(allresults))
        return render_template('./auth/account.html')
    else:
        return redirect(url_for('user.login', msg = "You need to log in first pal"))

@user.route('/logout')
def logout():
    if 'ActiveUser' in session:
        logit(session['ActiveUser'] + " :" + " Logged Out")
        session.pop('ActiveUser', None)
        return redirect(url_for('user.login', msg = "Logged Out"))
    else:
        return redirect(url_for('user.login', msg = "You Need To log In First pal"))

# send json export file to user
@user.route('/Export', methods= ['GET', 'POST'])
def export():
    exportData(session['ActiveUser'])
    logit("Exported data of : " + session['ActiveUser'])
    return send_from_directory(directory= current_app.root_path + '/ExportedJson', filename= 'ExportedJson.json')



