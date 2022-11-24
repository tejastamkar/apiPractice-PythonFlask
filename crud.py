import os
from flask import *
from firebase_admin import firestore

from firebase import connection
app = Flask(__name__)

connection()


@app.route("/users/<string:collectionName>", methods=["GET", "POST"])
def users(collectionName):
    db = firestore.client()
    users = []
    if request.method == 'GET':
        docs = db.collection(collectionName).get()
        for doc in docs:
            users.append(doc.to_dict())
        if users is not None:
            return jsonify(users), 200
    if request.method == 'POST':
        _username = request.form['username']
        _age = int(request.form['age'])
        ref = db.collection(collectionName).add({"name": _username, "age": _age})
        db.collection(collectionName).document(ref[1].id).update({"id": ref[1].id})
        return f"the new Doc with id: {ref[1].id} is created", 200


@app.route("/user/<string:collectionName>/<string:id>", methods=["GET", "PUT", "DELETE"])
def getUser(collectionName,id):
    db = firestore.client()
    user = []
    if request.method == 'GET':
        doc = db.collection(collectionName).document(id).get()
        user.append(doc.to_dict())
        if user is not None:
            return jsonify(user), 200
        else:
            return "User not Fount", 404
    if request.method == 'PUT':
        _username = request.form['username']
        _age = int(request.form['age'])
        db.collection(collectionName).document(id).update(
            {"name": _username, "age": _age})
        obj = {
            "id": id,
            "Username": _username,
            "Age": _age
        }
        return f"The User with id: {id} is update: \n{jsonify(obj)}"
    if request.method == 'DELETE':
        db.collection(collectionName).document(id).delete()
        return f"The Book with id: {id} has been deleted", 200



port = int(os.environ.get("PORT", 5000))
if __name__ == "__main__":
        app.run(host='0.0.0.0', port=port, debug=True)
