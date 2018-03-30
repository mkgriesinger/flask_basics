from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config.update(
    SECRET_KEY = "topsecret",
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:deepblue12@localhost/catalog_db",
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

db = SQLAlchemy(app)

@app.route('/index')
@app.route('/')
def hello_flask():
    return 'Hello flask!'


@app.route('/new/')
def query_strings(greeting='hello'):
    query_val = request.args.get('greeting', greeting)
    return '<h1> the greeting is: {0}</h1>'.format(query_val)


@app.route('/user/')
@app.route('/user/<name>')
def no_query_strings(name="mike"):
    return '<h1> Hello there ! {0}</h1>'.format(name)

@app.route('/temp/')
def using_templates():
    return render_template('hello.html')


@app.route('/watch/')
def movies_2017():
    movie_list = ['autopsy of jane doe',
                  'neon deamon',
                  'ghost in a shell',
                  'kong: skull island',
                  'john wick 2',
                  'spiderman - homecoming']
    return render_template('movies.html', movies=movie_list, name='Harry')


@app.route('/tables/')
def movies_plus():
    movies_dict = {'autopsy of jane doe': 02.14,
                   'neon demon': 3.20,
                   'ghost in a shell': 1.50,
                   'kong: skull island': 3.50,
                   'john wick 2': 02.52,
                   'spiderman -homecoming': 1.48
                   }
    return render_template('table_data.html', movies=movies_dict, name='Sally')

class Publication(db.Model):
    __tablename__ = 'publication'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "The Publisher is {}".format(self.name)

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False, index=True)
    author = db.Column(db.String(350))
    avg_rating = db.Column(db.Float)
    format = db.Column(db.String(50))
    image = db.Column(db.String(100), unique=True)
    num_pages = db.Column(db.Integer)
    pub_date = db.Column(db.DateTime)

    # Relationship
    pub_id = db.Column(db.Integer, db.ForeignKey('publication.id'))

    def __init__(self, title, author, avg_rating, book_format, image, num_pages, pub_id, pub_date=None):
        self.title = title
        self.author = author
        self.avg_rating = avg_rating
        self.format = book_format
        self.image = image
        self.num_pages = num_pages
        self.pub_id = pub_id
        self.pub_date = datetime.utcnow() if pub_date is None else pub_date

    def __repr__(self):
        return "{} by {}".format(self.title, self.author)

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)