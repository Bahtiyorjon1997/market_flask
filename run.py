from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


# initialization
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market_db.db'
# after writing this, on terminal run python
# then type from <py file> import db
# then type db.create_all()


db = SQLAlchemy(app)


@app.route('/')
@app.route('/home')
def home_page(key='home'):
    return render_template('home.html', name='that is the home page')


@app.route('/<key>')
def about(key='about'):
    return render_template('about.html', name='that is the about page')


@app.route('/market')
def market_page():
    items = Item.query.all()  # replaced by list of items hardocoded
    return render_template('market.html', name='that is the market page', items=items)


@app.route('/user/<name>')
def user(name):
    return f"<h1>Hello {name}</h1>"


# models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50),
                              nullable=False, unique=True)
    password_hash = db.Column(db.String(length=68), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    items = db.relationship('Item', backref="owned_user", lazy=True)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1024),
                            nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f"Item {self.name}"


if __name__ == '__main__':
    app.run(debug=True)
