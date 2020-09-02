import requests
from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__, template_folder=r"C:\Users\adamk\gitpractice\practice\poli")

@app.route("/", methods=["GET"])
def index():
    cwd = os.getcwd()
    path = cwd + r'\static\assets'
    imgs = os.listdir(path)
    assets = ["assets/" + img for img in imgs]
    return render_template("index.html", assets=assets)

if __name__ == "__main__":
    app.run(debug=True)
