from flask import Flask, render_template, request
from application import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = ("postgres://lqmsbfavabnpmo:b2337303395e7f3ed21db684e2d7d938f3b81291b28a884e09c75db8cac0e337@ec2-34-200-116-132.compute-1.amazonaws.com:5432/dat2dqd3j3qaeq")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    '''
    books = Book.query.all()
    for book in books:
        if len(book.publication_year) > 4:
            book.publication_year = book.publication_year[:-2]
            db.session.commit()          
                   
    reviews = Rating.query.filter_by(user_id = 2).all()
    print(reviews[0].user_id)
    #print(reviews.user_id)
    '''
    
    book_reviews = Rating.query.filter(Rating.book_id == 23).all()
    print(book_reviews)
    print(type(book_reviews))
    for rev in book_reviews:
        print(rev.user_id)



if __name__ == "__main__":
    with app.app_context():
        main()
        
        
       