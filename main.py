from flask import Flask
from data import db_session
from data.users import User
from data.news import News
from data.users_to_lessions import U_t_L
from data.lessions import Lession
from data.schedule import Less_in_sch
from flask import render_template
from forms.user import RegisterForm, LoginForm
from forms.news import NewsForm
from forms.sub_info import TSub, SSub
from flask_login import login_user, login_required, logout_user, current_user
from flask import redirect
from flask_login import LoginManager
from flask import request
from flask import abort

app = Flask(__name__)
with open('s_k.txt', 'r', encoding='utf8') as f:
    s_k = f.read()
app.config['SECRET_KEY'] = s_k

login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        news = db_sess.query(News)
    else:
        news = db_sess.query(News).filter(News.is_private != True)
    return render_template("index.html", news=news)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/page/<int:id>', methods=['GET', 'POST'])
def page(id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(
        User.id == id).first()
    lessions_obj = db_sess.query(U_t_L).filter(id == U_t_L.user_id).all()
    lessions = []
    for l in lessions_obj:
        les_name = db_sess.query(Lession).filter(Lession.id == l.lession_id).first()
        lessions.append(les_name.name)
    return render_template('page.html', user=user, lessions=lessions)


@app.route('/schedule')
def schedule():
    return render_template('schedule.html', classes=['5А', '5Б', '6А'])


@app.route('/schedule/<string:klass>', methods=['GET', 'POST'])
def schedule2(klass):
    db_sess = db_session.create_session()
    schedule = db_sess.query(Less_in_sch).filter(Less_in_sch.klass == klass).all()
    schedule.sort(key=lambda x: (x.day, x.place))
    return render_template('schedule.html', classes=['5А', '5Б', '6А'], schedule=schedule)


@app.route('/mainteachers')
def mainteachers():
    db_sess = db_session.create_session()
    data = []
    users = db_sess.query(U_t_L).filter((U_t_L.lession_id == 0) | (U_t_L.lession_id == 1)).all()
    for i in users:
        l = db_sess.query(Lession).filter(Lession.id == i.lession_id).first()
        t = db_sess.query(User).filter(User.id == i.user_id).first()
        data.append((t.name, l.name, int(t.id)))
    return render_template('mainteachers.html', data=data)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = NewsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user
                                          ).first()
        if news:
            form.title.data = news.title
            form.content.data = news.content
            form.is_private.data = news.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user
                                          ).first()
        if news:
            news.title = form.title.data
            news.content = form.content.data
            news.is_private = form.is_private.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('news.html',
                           title='Редактирование новости',
                           form=form
                           )


@app.route('/news',  methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = News()
        news.title = form.title.data
        news.content = form.content.data
        news.is_private = form.is_private.data
        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('news.html', title='Добавление новости',
                           form=form)


@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == id,
                                      News.user == current_user
                                      ).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        id = user.id
        if user.about == 3 or user.about == 4:
            return redirect(f'/register2/{int(id)}')
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/register2/<int:id>', methods=['GET', 'POST'])
def register2(id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == id).first()
    if user.about == 3:
        form = TSub()
        if request.method == 'POST':
            datadict = form.sub_info.data[0]
            data = datadict['checkmath'], datadict['checkrus'], datadict['checkphys']
            for les_id in range(len(data)):
                if data[les_id]:
                    utl = U_t_L()
                    utl.user_id = user.id
                    lession = db_sess.query(Lession).filter(Lession.id == les_id).first()
                    utl.lession_id = lession.id
                    db_sess.add(utl)
            db_sess.commit()
            return redirect('/login')
        return render_template('register2.html', title='Регистрация', form=form)
    elif user.about == 4:
        form = SSub()
        if request.method == 'POST':
            datadict = form.sub_info.data[0]
            user.sub_info = datadict['radioclass']
            db_sess.commit()
            return redirect('/login')
        return render_template('register2.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def main():
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    db_sess.commit()
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()
