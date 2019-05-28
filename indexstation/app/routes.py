# -*- coding: utf-8 -*-
import re

from flask import render_template, flash, redirect, url_for, jsonify, request, abort
from flask_login import current_user, login_user, logout_user, login_required

from app import app, models, DB_MANAGER
from app.forms.login import LoginForm
from app.forms.send_params import ParamForm
from app.forms.registration import RegistrationForm
from app.forms.user_update import PasswordUpdateForm

pdfs = [None, 
        {'id' :  3,  'pdf_link' : 'https://zagorie.ru/upload/iblock/4ea/4eae10bf98dde4f7356ebef161d365d5.pdf', 'times' : 0},
        {'id' :  2, 'pdf_link' : '/static/pdf.pdf', 'times' : 0},
        {'id' :  1, 'pdf_link' : '/static/pdf2.pdf', 'times' : 0}]
#TODO: Нужно делать нормальную очередь раздачи

users = {}


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html', title = 'Главная страница', params=ParamForm)

@app.route('/stat', methods=['POST', 'GET'])
@login_required
def stat():
    if current_user.username != 'admin':
        return abort(404)
    return render_template('stat.html', title = 'Статистика')

@app.route('/get_params', methods=['POST'])
@login_required
def get_params():
    '''
    params = request.form.to_dict()
    param_name = list(params.keys())
    # Запись полученных параметров в бд
    u = current_user
    d = models.Doc.query.filter_by(id=pdfs[-users[u.username]]['id']).first()
    for i in range(len(params) // 2):
        name = param_name[i]
        param_pos = params[param_name[-i-1]]
        p = models.Param.query.filter_by(name = name).first()
        start = 0
        end = 0
        if (param_pos != ''):
            pos = re.findall(r'\d+', param_pos)
            start = pos[0]
            end = pos[1]
        res = models.Result(author=u, doc=d, param=p, value=params[name], start_symb=int(start), stop_symb=int(end))
        DB_MANAGER.session.add(res)
        DB_MANAGER.session.commit()

    '''
    return jsonify({'status' : 'OK'})

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неправильное имя пользователя или пароль')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Вход', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/user', methods=['GET', 'POST'])
@login_required
def user():
    form = PasswordUpdateForm()
    if form.validate_on_submit():
        current_user.set_password(form.password_new1.data)
        DB_MANAGER.session.commit()
        flash('Пароль успешно изменен.')
    return render_template('user.html', title='Профиль', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = models.User(username=form.username.data, rating=10)
        user.set_password(form.password.data)
        DB_MANAGER.session.add(user)
        DB_MANAGER.session.commit()
        flash('Регистрация успешно завершена!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Регистрация', form=form)

@app.route('/next_doc', methods=['GET'])
@login_required
def get_next_document():
    if not users.get(current_user.username):
        users[current_user.username] = 1
    else:
        users[current_user.username] = users[current_user.username] + 1
    i = -users[current_user.username]
    if not pdfs[i]: # пустой документ.
        # выгрузить кол-во правильных ответов в бд
        users[current_user.username] -= 1
        return jsonify({'name' : 'Нет документов в очереди', 'text': '', 'pdf' : ''})
    if pdfs[i]['times'] == 5:
        pdfs.pop()
    pdfs[i]['times'] += 1
    return jsonify({'name' : models.Doc.query.filter_by(id=pdfs[i]['id']).first().name, 'pdf' : pdfs[i]['pdf_link']})

@app.route('/add_doc', methods=['POST'])
def add_document():
    try:
        data = request.get_json(force=True)
        pdfs.insert(1, {"id" : data["id"],
                        "pdf_link" : data["url"],
                        "times" : 0})
        return jsonify({"result" : "ok"})
    except:
        return jsonify({"result" : "error"})

@app.route('/results', methods=['GET']) # фильтры()
def results():
    res = []
    for r in models.Result.query.all():
        res.append({"id" : r.id,
                    "doc_name" : r.doc.name,
                    "param_name" : r.param.name,
                    "value" : r.value})
    return jsonify(res)
