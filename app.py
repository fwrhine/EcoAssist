import os
from flask import Flask, render_template
from pymongo import MongoClient


app = Flask(__name__)

# client = MongoClient(os.environ["DB_PORT_27017_TCP_ADDR"], 27017)
# db = client.appdb

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
