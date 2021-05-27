from flask  import Flask, render_template
from flask_sqlalchemy import SQLAlchemy #m
from flask_wtf import FlaskForm #m
from wtforms.ext.sqlalchemy.orm import model_form #m

app = Flask(__name__)
app.secret_key = 'kei2shoh4xai2Zohqu0o6ahsh'
db = SQLAlchemy(app)

class Book(db.Model): #m
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  author = db.Column(db.String, nullable=False)

BookForm = model_form(Book, base_class=FlaskForm, db_session=db.session) #m

@app.before_first_request #m
def initDatab():
  db.create_all()

  book = Book(name="Tom Sawyer", author="Mark Twain")
  db.session.add(book)

  book = Book(name="Tuntematon Sotilas", author="Väinö Linna")
  db.session.add(book)

  db.session.commit()

@app.route("/add", methods=["GET", "POST"])
def newBook():
  form = BookForm()

  if form.validate_on_submit():
    book = Book()
    form.populate_obj(book)
    db.session.add(book)
    db.session.commit()
    print("lisätty")

  return render_template("add.html", form=form) #m

@app.route("/")
def index ():
  books = Book.query.all() #m
  return render_template("index.html", books=books) #m

if __name__ == "__main__": #m
  app.run(debug=True)
