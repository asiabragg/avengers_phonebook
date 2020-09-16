from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from avengers_pkg import app, db
from avengers_pkg.forms import LoginForm, RegisterForm, RequestForm
from avengers_pkg.models import User, Requests
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
def index():
    show_heros = User.query.order_by(User.heroname).all()
    return render_template("index.html", title="Avengers Phonebook", 
    show_heros=show_heros)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(heroname=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid heroname or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        # Creates the After-Login Redirect Functinoality
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title="Login", form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(heroname=form.heroname.data, email=form.email.data, phone_number=form.phone_number.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title="Register", form=form)

@app.route('/user/<heroname>')
@login_required
def user(heroname):
    user = User.query.filter_by(heroname=heroname).first_or_404()
    return render_template('user.html', title="Profile", user=user)

@app.route('/requests')
@login_required
def requests():
    form = RequestForm()
    if form.validate_on_submit():
        request = Requests(title=form.title.data, body=form.body.data)
        db.session.add(request)
        db.session.commit()
        flash('Your request has been submitted!')
        return redirect(url_for('requests'))
    return render_template('requests.html', title="Hero Requests", form=form)