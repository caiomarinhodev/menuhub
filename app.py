import datetime
import os

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SECRET_KEY'] = 'mysecret'
Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


class Account(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name_restaurant = db.Column(db.String(255), nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<Account {}>'.format(self.name)


TYPE_CATEGORY = (
    ('entrada', 'Entrada'),
    ('principal', 'Principal'),
    ('sobremesa', 'Sobremesa')
)


class Dish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.Enum(*[x[0] for x in TYPE_CATEGORY], name='category'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<Dish {}>'.format(self.name)


@login_manager.user_loader
def load_user(id):
    return Account.query.get(int(id))


@app.route('/login/', methods=['POST', 'GET'], endpoint='login')
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        account = Account.query.filter_by(email=email, password=password).first()
        if not account:
            flash('Verifique seus detalhes de login e tente novamente.')
            return redirect(url_for('login'))

        if account:
            login_user(account)
            return redirect(url_for('index'))
    else:
        return render_template('login.html')


@app.route('/signup/', methods=['POST', 'GET'], endpoint='signup')
def signup():
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['password1']
            name_restaurant = request.form['name_restaurant']

            account = Account.query.filter_by(email=email).first()

            if account:
                flash('O endereço de e-mail já existe')
                return redirect(url_for('signup'))

            new_account = Account(email=email, password=password, name_restaurant=name_restaurant)
            db.session.add(new_account)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
        return redirect(url_for('login'))
    else:
        return render_template('register.html')


@app.route('/logout/', endpoint='logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/', endpoint='index')
@login_required
def index():
    context = {
        'name': current_user.name_restaurant
    }

    if 'q' in request.args:
        context['dishes'] = Dish.query.order_by(Dish.created.desc()).filter(Dish.name.like('%{}%'.format(request.args['q']))).all()
    else:
        context['dishes'] = Dish.query.order_by(Dish.created.desc()).all()
    return render_template('index.html', **context)


@app.route('/add/', methods=['POST', 'GET'], endpoint='add')
@login_required
def add():
    if request.method == 'POST':
        try:
            name = request.form['name']
            category = request.form['category']
            price = float(request.form['price'].replace(',', '.'))
            description = request.form['description']

            new_dish = Dish(account_id=current_user.id, name=name, category=category, price=price,
                            description=description)
            db.session.add(new_dish)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
        return redirect(url_for('index'))
    else:
        context = {
            'categories': TYPE_CATEGORY
        }
        return render_template('add.html', **context)


@app.route('/edit/<int:id>/', methods=['POST', 'GET'], endpoint='edit')
@login_required
def edit(id):
    dish = Dish.query.get_or_404(id)
    if request.method == 'POST':
        try:
            dish.name = request.form['name']
            dish.category = request.form['category']
            dish.price = request.form['price']
            dish.description = request.form['description']

            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
        return redirect(url_for('index'))
    else:
        context = {
            'dish': dish,
            'categories': TYPE_CATEGORY
        }
        return render_template('edit.html', **context)


@app.route('/delete/<int:id>/', endpoint='delete')
@login_required
def delete(id):
    dish = Dish.query.get_or_404(id)
    try:
        db.session.delete(dish)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
