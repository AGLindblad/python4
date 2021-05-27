from flask import Flask, render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy #m
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form #m

app = Flask(__name__) #m
app.secret_key = 'oa8aa2ahVif+aephohSa2cei'
db = SQLAlchemy(app)

class Customer(db.Model): #m
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  tele = db.Column(db.String, nullable=False)
  email = db.Column(db.String, nullable=False)
  company = db.Column(db.String, nullable=True)

CustomerForm = model_form(Customer, base_class=FlaskForm, db_session=db.session) #m

@app.before_first_request #m
def iniDb():
  db.create_all()

  customer = Customer(name="Harry Callahan", tele= "0041233355", email= "harry@dirty.com", company= "LAPD")
  db.session.add(customer) #m

  customer = Customer(name="John Matrix", tele= "004467884", email= "arnold@commando.com", company= "Mercenary Inc")
  db.session.add(customer) #m
  db.session.commit()

@app.route ("/<int:id>/edit", methods=["GET", "POST"]) #mmmm
@app.route ("/add", methods=["GET", "POST"])
def newCustomer(id=None):
  customer = Customer()
  if id:
    customer = Customer.query.get_or_404(id)

  form = CustomerForm(obj=customer)

  if form.validate_on_submit():
    form.populate_obj(customer)
    db.session.add(customer)
    db.session.commit()
    flash("Great success!")
    return redirect ("/")

  return render_template("add.html", form = form)

@app.route("/<int:id>/delete") #mmmm
def deleteCustomer(id):
  customer = Customer.query.get_or_404(id)
  db.session.delete(customer)
  db.session.commit()

  flash("Bye bye")
  return redirect("/")

@app.route("/")
def index():
  customers = Customer.query.all()
  return render_template("index.html", customers = customers)

if __name__=="__main__": #m
  app.run(debug=True)
