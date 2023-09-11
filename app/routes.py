# Übernommen aus den Beispielen
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, New3DPrintForm, Edit3DPrintForm
from app.models import Users, Models

# Übernommen aus den Beispielen
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    models = Models.query.all() #order_by(Models.Timestamp.desc())
    return render_template('index.html', title='Home', models=models)

# Übernommen aus den Beispielen
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(Username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

# Übernommen aus den Beispielen
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# Übernommen aus den Beispielen
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(Username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# Eigenentwicklung
@app.route('/new3d', methods=['GET', 'POST'])
@login_required
def new3d():
    form = New3DPrintForm()
    if form.validate_on_submit():
        model = Models(Name=form.name.data, Description=form.description.data, Timestamp=datetime.utcnow(), User_ID=current_user.ID_User, Quality=form.quality.data, Status=form.status.data)
        db.session.add(model)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template("new3d.html", title="New 3D-Model", form=form)

# Eigenentwicklung
@app.route('/edit3d/<id>', methods=['GET', 'POST'])
@login_required
def edit3d(id):
    form = Edit3DPrintForm()
    model = Models.query.filter_by(ID_Model=id).first()
    if form.validate_on_submit():
        model.Name = form.name.data
        model.Description = form.description.data
        model.Status = form.status.data
        model.Quality = form.quality.data
        db.session.commit()

        return redirect(url_for('index', id=id))

    form.name.data = model.Name
    form.description.data = model.Description
    form.status.data = model.Status
    form.quality.data = model.Quality
    return render_template("edit3d.html", model=model, form=form)

# Eigenentwicklung
@app.route("/delete3d/<id>", methods=['GET', 'POST'])
@login_required
def delete3d(id):
    delete = Models.query.filter_by(ID_Model=id).first()
    db.session.delete(delete)
    db.session.commit()
    return redirect(url_for('index'))

# Eigenentwicklung
@app.route("/generateapikey", methods=['GET', 'POST'])
@login_required
def generateapikey():
    Users.get_token(current_user)
    return redirect(url_for('api'))

# Eigenentwicklung
@app.route("/api", methods=['GET', 'POST'])
@login_required
def api():
    return render_template("api.html", title="API")