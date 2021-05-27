from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

from flask_wtf import FlaskForm #m
from wtforms.ext.sqlalchemy.orm import model_form #m

app = Flask(__name__) #m
app.secret_key = 'XB32shoh4xai2Zohqu0o6rtg6' 
db = SQLAlchemy(app)

class Comic(db.Model): #m
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)

ComicForm = model_form(Comic, base_class=FlaskForm, db_session=db.session) #m

@app.before_first_request #m
def iniDb():
  db.create_all()

  comic = Comic(name="Superman")
  db.session.add(comic) #m

  comic = Comic(name="Donald Duck")
  db.session.add(comic) #m
  db.session.commit()

@app.route ("/add", methods=["GET", "POST"])
def newComic():
  form = ComicForm()

  if form.validate_on_submit():
    comic = Comic()
    form.populate_obj(comic)
    db.session.add(comic)
    db.session.commit()
    print("Jee")

  return render_template("add.html", form = form)

@app.route("/")
def index():
  comics = Comic.query.all()
  return render_template("index.html", comics = comics)

if __name__=="__main__": #m 
  app.run(debug=True)
