from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import requests
app = Flask(__name__, template_folder=r"C:\Users\adamk\gitpractice\practice\project1")
app.secret_key = 'super secret key'
app.config["SQLALCHEMY_DATABASE_URI"] = ("postgres://lqmsbfavabnpmo:b2337303395e7f3ed21db684e2d7d938f3b81291b28a884e09c75db8cac0e337@ec2-34-200-116-132.compute-1.amazonaws.com:5432/dat2dqd3j3qaeq")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    
    def __repr__(self):
        return '<User %r>' % self.name


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(120))
    title = db.Column(db.String(120))
    author = db.Column(db.String(120))
    publication_year = db.Column(db.String(10))
    img_url = db.Column(db.String(200))
    
    rating = db.relationship('Rating', backref='book', lazy=True)
    
    def __repr__(self):
        return '<Book %r>' % self.title

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    review = db.Column(db.String(140), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    user_id = db.Column(db.Integer)
    
    def __repr__(self):
        return '<Rating %r>' % self.id


@app.route("/", methods=["POST","GET"])
def login(): 
    session.clear()
    name = request.form.get("name")
    password = request.form.get("password")
    if name is None:
        return render_template("login.html")
    elif User.query.filter_by(name=name).first().password == password:
        session['user_id'] = User.query.filter_by(name=name).first().id
        return render_template("index.html")        
    else:
        return render_template("error.html")

      
@app.route("/register",methods=["POST","GET"])
def register():
    name = request.form.get("name")
    password = request.form.get("password")
    if name is None:
        return render_template("register.html")
    user = User(name=name, password=password)
    db.session.add(user)
    db.session.commit()
    return render_template("success.html")
    
@app.route("/changepw",methods=["POST","GET"])
def changepw():
    name = request.form.get("name")
    old_password = request.form.get("old_password")
    new_password = request.form.get("new_password")
    if name is None:
        return render_template("changepw.html")
    if User.query.filter_by(name=name).first().password == old_password:
        User.query.filter_by(name=name).first().password = new_password
        db.session.commit()
        return render_template("success.html")
    else:
        return render_template("error.html")

        

    
@app.route("/index", methods=["POST","GET"])
def index():
    txt = request.form.get("txt")
    books = Book.query.filter(db.or_(Book.title.ilike('%{}%'.format(txt)),Book.author.ilike('%{}%'.format(txt)),Book.isbn.ilike('%{}%'.format(txt)))).all()
    if len(books) == 0 and txt is not None:
        return render_template("error.html", message="No results found")
    else:
        return render_template("index.html", books=books)
    
@app.route("/<string:book_id>", methods=["POST","GET"])
def book_page(book_id):
    book = Book.query.get(book_id)    
    if book is None:
        return render_template("error.html", message="No such book")    
    if len(book.isbn) == 9:
        book.isbn = '0'+book.isbn
        db.session.commit()
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "U3uqCHQ1o8RHbLOuR6bA", "isbns": "{}".format(book.isbn)})    
    average_rating = 'no rating available'
    work_ratings_count = 'no rating available'
    reviews = Rating.query.filter_by(book_id = book.id).all()    
    if res.status_code == 200:    
        data = res.json()
        average_rating = data['books'][0]['average_rating']
        work_ratings_count = data['books'][0]['work_ratings_count']                      
    return render_template("book_page.html", book=book, average_rating=average_rating,work_ratings_count=work_ratings_count, reviews=reviews)

@app.route("/adding_review/<string:book_id>", methods=["POST","GET"])    
def add_review(book_id):
    book = Book.query.get(book_id)    
    review = request.form.get("review")    
    if review is not None:        
        if have_reviewed(book.id, session['user_id']) :
          #Second time posting a review
            return render_template("error_review.html", message="You already submited a review!", id=book.id)
        else:            
            #first review
            new_rev = Rating(review=review, book_id=book.id, user_id=session['user_id'])
            db.session.add(new_rev)
            db.session.commit()    
    return redirect(url_for('book_page',book_id = book.id))

def have_reviewed(book_id, user_id):
   #func checkes if a user has already posted a review
    book_reviews = Rating.query.filter(Rating.book_id == book_id).all()
    for review in book_reviews:
        if review.user_id == user_id:
            return True
    return False     
        

        
if __name__ == "__main__":  
    app.debug = True
    app.run()

