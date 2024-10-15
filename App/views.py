from flask.views import MethodView
from flask import Blueprint, request, jsonify, make_response, render_template, redirect
from App.models import *
from App.exts import db

blue = Blueprint('user', __name__)

@blue.route('/')
def home():
    return render_template('home.html')

@blue.route('/login/', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        pass
        username = request.form.get('username')
        password= request.form.get('password')

    user=User.query.filter_by(username=username).first()
    if not user:
        return '账号不存在'
    if not user.password == password:
        return '密码错误'

    response=redirect('http://localhost:5173')
    response.set_cookie('user', username, max_age=3600*24)
    return response

@blue.route('/register/', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
    user = User().query.filter_by(username=username).first()
    if user:
        return '账号已存在'
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return redirect('/login/')




class BookApi(MethodView):
    def get(self, book_id=None):
        if not book_id:
            books = Book.query.all()
            results = [
                {
                    'id': book.id,
                    'book_number': book.book_number,
                    'book_name': book.book_name,
                    'book_type': book.book_type,
                    'book_price': book.book_price,
                    'author': book.author,
                    'book_publisher': book.book_publisher
                } for book in books
            ]
            return jsonify({
                'status': 'success',
                'message': 'ok',
                'results': results
            })
        else:
            book = Book.query.get(book_id)
            if book:
                return jsonify({
                    'status': 'success',
                    'message': 'ok',
                    'results': {
                        'id': book.id,
                        'book_number': book.book_number,
                        'book_name': book.book_name,
                        'book_type': book.book_type,
                        'book_price': book.book_price,
                        'author': book.author,
                        'book_publisher': book.book_publisher
                    }
                })
            else:
                return jsonify({'status': 'error', 'message': 'Book not found'})

    def post(self):
        form = request.json
        book = Book()
        book.book_number = form.get('book_number')
        book.book_name = form.get('book_name')
        book.book_type = form.get('book_type')
        book.book_price = form.get('book_price')
        book.author = form.get('author')
        book.book_publisher = form.get('book_publisher')
        db.session.add(book)
        db.session.commit()
        return jsonify({'status': 'success', 'message': '添加成功'})

    def delete(self, book_id):
        book = Book.query.get(book_id)
        if book:
            db.session.delete(book)
            db.session.commit()
            return jsonify({'status': 'success', 'message': '删除成功'})
        else:
            return jsonify({'status': 'error', 'message': 'Book not found'})

    def put(self, book_id):
        book = Book.query.get(book_id)
        if book:
            book.book_type = request.json.get('book_type')
            book.book_name = request.json.get('book_name')
            book.book_price = request.json.get('book_price')
            book.book_number = request.json.get('book_number')
            book.author = request.json.get('author')
            book.book_publisher = request.json.get('book_publisher')
            db.session.commit()
            return jsonify({'status': 'success', 'message': '修改成功'})
        else:
            return jsonify({'status': 'error', 'message': 'Book not found'})


    def options(self, book_id=None):
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.status_code = 200
        return response

book_view = BookApi.as_view('book_api')
blue.add_url_rule('/books/', view_func=book_view, defaults={'book_id': None}, methods=['GET', 'OPTIONS'])
blue.add_url_rule('/books/', view_func=book_view, methods=['POST', 'OPTIONS'])
blue.add_url_rule('/books/<int:book_id>/', view_func=book_view, methods=["GET", "PUT", "DELETE", "OPTIONS"])


