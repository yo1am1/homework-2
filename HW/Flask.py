import csv

import flask
import requests
from faker import Faker
from flask import request

app = flask.Flask(__name__)


@app.route("/")
def index():
    return flask.render_template("index.html")


@app.route("/requirements/")
def text():
    with open("requirements.txt", "r+") as req:
        require = req.read()
    return flask.render_template("task1.html", text=require)


@app.route("/users/generate", methods=['GET'])
def fake_dictionary():
    fake, fakedict = Faker(), {}
    num = 100
    try:
        num = int(request.args['number'])
    except (Exception,):
        pass
    fakedict = {fake.name(): fake.ascii_company_email() for _ in range(num)}
    return flask.render_template("task2.html", dictionary=fakedict)


@app.route("/mean/")
def csv_file():
    with open("hw.csv", "r") as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)
        reader = list(reader)
        answer_h, answer_w = 0, 0
        for i in range(25000):
            num_h, num_w = float(reader[i][1].strip()), float(reader[i][2].strip())
            answer_h += num_h
            answer_w += num_w
    return flask.render_template(
        "task3.html",
        ans_h_cm=(answer_h * 2.54) / (len(reader) - 1),
        ans_w_kg=(answer_w * 0.45359237) / (len(reader) - 1),
        ans_h_inches=answer_h / (len(reader) - 1),
        ans_w_pounds=answer_w / (len(reader) - 1),
    )


@app.route("/space/")
def answer_json():
    r = requests.get("http://api.open-notify.org/astros.json")
    answer = r.json()["number"]
    return flask.render_template("task4.html", answer=answer)


@app.errorhandler(404)
def page_not_found(error):
    return flask.render_template("error.html"), 404


if __name__ == '__main__':
    app.run(debug=True)
