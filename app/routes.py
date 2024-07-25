"""
здесь вся логика работы
"""
from flask import render_template, request, redirect, url_for, flash
from app import app, db, bcrypt
from app.models import User
from app.forms import LoginForm, RegistrationForm
from flask_login import login_user, logout_user, current_user, login_required

# декоратор главной страницы открывается только
# для регистрированного пользователя и в аккаунте
@app.route('/')
@login_required
def index():
    return render_template('index.html')

# точно ли пользователь в системе
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        # направить на индекс
        return redirect(url_for('index'))
    # создать объект
    form = RegistrationForm()
    # точно ли нажата кнопка
    if form.validate_on_submit():
        # зашифровать пароль
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # создать объект юзера
        user = User(username=form.username.data, password=hashed_password)
        # добавить сессию
        db.session.add(user)
        db.session.commit()
        # вывести надпись
        flash('Вы успешно зарегистрировались!', 'success')
        return redirect(url_for('login'))
    return render_template("register.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        # найти юзера по имени
        user = User.query.filter_by(username=form.username.data).first()
        # сравнение пароля с формы и из БД
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # совпадает
            login_user(user)
            return redirect(url_for('index'))
        else:
            # сообщение
            flash('Неверно введены данные аккаунта', 'danger')
    return render_template("login.html", form=form)

# выйти из аккаунта
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

# логика кликера только для залогиненного пользователя
@app.route('/click')
@login_required
def click():
    # увеличить число кликов
    current_user.clicks += 1
    db.session.commit()
    # для обновления кликов
    return redirect(url_for('index'))