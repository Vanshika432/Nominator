import datetime
from flask import Blueprint, render_template, redirect, request, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from app import db 
from models import Candidate, Company
import views
from sqlalchemy.exc import IntegrityError

auth = Blueprint('auth', __name__)


@auth.route('/select_auth')
def login_choice():
    return render_template('login.html')


@auth.route('/signup-candidate', methods=['GET', 'POST'])
def signup_candidate():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        resume = request.files.get('resume')
        linkedin = request.form.get('linkedin')
        github = request.form.get('github')
        if resume:
            resume.save(resume.filename)
            has_resume = True
        else:
            has_resume = False
        user = Candidate.query.filter_by(username=username).first()

        if user:
            flash('Username already exist.')
            return redirect(url_for('login_candidate'))
        try:
            user = Candidate(email=email, username=username, password=generate_password_hash(password, method='sha256'),
                             firstname=firstname, lastname=lastname, resume=has_resume, linkedin=linkedin, github=github)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash(f"Successfully registered candidate, {firstname}")
            return redirect(url_for('home'))
        except IntegrityError:
            flash('Given Field(s) should satisfy all the requirements. Field(s) not unique.', 'error')

    return render_template('signupcandidate.html')


@auth.route('/login-candidate', methods=['GET', 'POST'])
def login_candidate():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        candidate = Candidate.query.filter_by(username=username).first()
        if candidate:
            if check_password_hash(candidate.password, password):
                login_user(candidate)
                flash(f"Successfully logged in as {candidate.username}", 'success')
                return redirect(url_for('home'))
            else:
                flash(f"Username or password is incorrect. Please try again!", 'error')
        else:
            flash(f"User {username} does not exist.", 'error')
    return render_template('logincandidate.html')


@auth.route('/signup-company', methods=['GET', 'POST'])
def signup_company():
    if request.method == "POST":
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        company_name = request.form.get('company_name')
        website = request.form.get('website')
        description = request.form.get('desc')
        founder = request.form.get('founder')
        founded_on = datetime.datetime.strptime(request.form.get('founded_on'), '%Y-%m-%d').date()
        try:
            user = Company(email=email, username=username, password=generate_password_hash(password, method='sha256'),
                           company_name=company_name, website=website, desc=description, founded_on=founded_on,
                           founder=founder)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash(f"Successfully registered {company_name}")
            return redirect(url_for('home'))
        except IntegrityError as e:
            print("Error in company signup.")
            print(e)
            flash('Given Field(s) should satisfy all the requirements. Field(s) not unique.', 'error')

    return render_template('signupcompany.html')


@auth.route('/login-company', methods=['GET', 'POST'])
def login_company():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        company = Company.query.filter_by(username=username).first()
        if company:
            if check_password_hash(company.password, password):
                login_user(company)
                flash(f"Successfully logged in as {company.company_name}", 'success')
                return redirect(url_for('home'))
            else:
                flash(f"Username or password is incorrect. Please try again!", 'error')
        else:
            flash(f"User {username} does not exist.", 'error')
    return render_template('logincompany.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login_choice'))
