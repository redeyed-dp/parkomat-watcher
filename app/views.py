from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.models import Admin
from app.forms import LoginForm, AdminForm

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        try:
            admin = db.session.query(Admin).filter(Admin.login == form.login.data).one()
            if admin.check_password(form.password.data):
                login_user(admin, remember=form.remember_me.data)
                next_page = request.args.get('next')
                if not next_page or url_parse(next_page).netloc != '':
                    next_page = url_for('index')
                return redirect(next_page)
            flash('Неверный логин или пароль')
        except:
            flash('Неверный логин или пароль')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/admins/", methods=['GET', 'POST'])
@login_required
def admins():
    form = AdminForm()
    if form.validate_on_submit():
        admin = Admin(login=form.login.data, name=form.name.data)
        admin.set_password(form.password.data)
        db.session.add(admin)
        db.session.commit()
        flash(f"Добавлен администратор { admin.login }")
        return redirect(url_for("admins"))
    admins = db.session.query(Admin).all()
    return render_template("admins.html", admins=admins, form=form)

@app.route("/admins/del/<int:id>")
@login_required
def admins_del(id):
    admin = db.session.query(Admin).filter(Admin.id==id).one()
    db.session.delete(admin)
    db.session.commit()
    flash(f"Учетная запись администратора { admin.login } удалена")
    return redirect(url_for("admins"))