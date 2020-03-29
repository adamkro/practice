from flask import Flask, render_template, request

app = Flask(__name__, template_folder=r"C:\Users\adamk\gitpractice\practice")

@app.route("/")
def index():
    return render_template("firstpage.html")


@app.route("/another")
def inner():
    return render_template("secondpage.html")
    
@app.route("/hello", methods=["POST","GET"])
def hello():
    name = request.form.get("name")
    return render_template("hi.html", name=name)
    
  