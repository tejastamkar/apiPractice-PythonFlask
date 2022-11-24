import json
import time
from addfunc import add, sub
from flask import *
from db import dbconnetion, createDb

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/add/<int:x>&<int:y>")
def calingAdd(x, y):
    return add(x, y)


@app.route("/sub/<int:x>&<int:y>")
def calingSub(x, y):
    return sub(x, y)


@app.route("/users/<string:name>")
def userName(name):
    return f"<h1>Hi {name}</h1>"


@app.route("/create")
def createTable():
    createDb()
    return "done"


@app.route("/books", methods=["GET", "POST"])
def books():
    conn = dbconnetion()
    cursor = conn.cursor()
    if request.method == 'GET':
        cursor = conn.execute("SELECT * FROM books")
        books = [
            dict(id=row[0], author=row[1], title=row[2])
            for row in cursor.fetchall()
        ]
        if books is not None:
            return jsonify(books)

    if request.method == 'POST':
        _author = request.form['author']
        _title = request.form['title']
        sql = """INSERT INTO books (author , title) VALUES (?,?)"""
        cursor = conn.execute(sql, (_author, _title))
        conn.commit()
        return f"Book with id:{cursor.lastrowid} is created", 201


@app.route("/book/<int:id>", methods=["GET", "PUT", "DELETE"])
def getBook(id):
    conn = dbconnetion()
    cursor = conn.cursor()
    if request.method == 'GET':
        cursor.execute("SELECT * FROM books WHERE id=?", (id,))
        row = cursor.fetchall()
        for r in row:
            book = r
            if book is not None:
                return jsonify(book), 200
            else:
                'Nothing Found', 404

    if request.method == 'PUT':
        sql = """UPDATE books SET title=?, author=? where id=?"""
        author = request.form['author']
        title = request.form['title']
        obj = {
            "id": id,
            "author": author,
            "title": title,
        }
        conn.execute(sql, (author, title, id))
        conn.commit()
        return jsonify(obj)
    if request.method == 'DELETE':
        sql = """DELETE FROM books where id=?"""
        conn.execute(sql , (id,))
        conn.commit()
        return f"The Book with id: {id} has been deleted" , 200


@app.route("/user/", methods=["GET"])
def getUser():
    userName = str(request.args.get("user"))  # /user/?user=USERNAME
    data = {
        "Request": True,
        "Message": f"Got the data user {userName}",
        "TimeStamp": f"{time.time()}"
    }
    return json.dumps(data)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
