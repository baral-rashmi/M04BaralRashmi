from flask import Flask
app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(80), unique=True, nullable=False)
    author = db.Column(db.String(100))
    publisher = db.Column(db.String(140))

    def __repr__(self):
        return f"{self.book_name} - {self.author} - {self.publisher}"


@app.route("/")
def index():
    return 'Hello'


@app.route('/books')
def get_books():
    books = Books.query.all()

    output = []
    for book in books:
        book_data = {'name': book.book_name, 'author': book.author, 'publisher': book.publisher}

        output.append(book_data)

    return {"books": output}


@app.route('/books/<id>')
def get_book(id):
    book = Books.query.get_or_404(id)
    return {'name': book.book_name, 'author': book.author, 'publisher': book.publisher}


@app.route('/books', methods=['POST'])
def add_book():
    book = Books(book_name=request.json['book_name'],
                  author=request.json['author'],
                  publisher=request.json['publisher'])
    db.session.add(book)
    db.session.commit()
    return {'id': book.id}


@app.route('/books/<id>', methods=['DELETE'])
def delete_book(id):
    book = Books.query.get(id)
    if book is None:
        return {"error": "book not found"}
    db.session.delete(book)
    db.session.commit()
    return {"message": "book deleted!"}


    