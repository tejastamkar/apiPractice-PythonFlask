import json
import time
from addfunc import add
from flask import *

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/add/<int:x>&<int:y>")
def calingAdd(x, y):
    return add(x, y)


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
    app.run(debug=True ,host='0.0.0.0', port=5000)
