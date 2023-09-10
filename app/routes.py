from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, New3DPrintForm, Edit3DPrintForm
from app.models import Users, Models


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    posts = Models.query.order_by(Models.timestamp.desc())
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/new3d', methods=['GET', 'POST'])
@login_required
def new3d():
    form = New3DPrintForm()
    if form.validate_on_submit():
        model = Models(Filename=form.titel.data, Content=form.content.data, Timestamp=datetime.utcnow(), User_ID=current_user.ID_User, Model_ID=id)
        db.session.add(model)
        db.session.commit()
        return redirect(url_for('index', id=id))

@app.route('/edit3d', methods=['GET', 'POST'])
@login_required
def edit3d():
    form = Edit3DPrintForm()
    model = Models.query.filter_by(ID_Models=id).first()
    if form.validate_on_submit():
        model.Name = form.name.data
        model.Status = form.status.data
        model.Quality = form.quality.data
        db.session.commit()
        return redirect(url_for('index', id=id))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))