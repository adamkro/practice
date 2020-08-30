from flask import Flask, render_template, request
import os
import sys
from flask_sqlalchemy import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
#from models import *
#class name 



app = Flask(__name__, template_folder=r"C:\Users\adamk\gitpractice\practice")
app.config["SQLALCHEMY_DATABASE_URI"] = "LOCALHOST"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

engine = create_engine("LOCALHOST")
db = scoped_session(sessionmaker(bind=engine))
db.init_app(app)
    

#db.create_all()
#with_app context ?()


@app.route("/")
def index():
  #  names = db.execute("SELECT * FROM names").fetchall()
    return render_template("firstpage.html", names = names)


@app.route("/another")
def inner():
    return render_template("secondpage.html")
    
@app.route("/hello", methods=["POST","GET"])
def hello():
    name = request.form.get("name")
    db.session.add(name)
    db.session.commit()
    return render_template("hi.html", name=name)
    
    
  