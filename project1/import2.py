from application import *
import csv

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
    
    def __repr__(self):
        return '<Rating %r>' % self.id
'''
with open('books.csv', encoding="utf8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count < 2380:
            line_count += 1
            continue
        book = Book(isbn = row[5], title = row[9] ,author = row[7], publication_year = row[8], img_url = row[-2])
        db.session.add(book)
        db.session.commit()
    #print(f'Processed {line_count} lines.')
'''
#db.create_all()