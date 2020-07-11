import flask
import connexion
from datetime import datetime
from flask import jsonify
import json

app = flask.Flask(__name__)


def profit(data):
    res = []
    count = 0
    previous_date = 0
    for movies in data:

        if count == 0:
            res.append(movies)
            previous_date = datetime.strptime(movies['end_date'], '%d %b')
            count += 1
            continue
        current_date = datetime.strptime(movies['start_date'], '%d %b')
        if current_date > previous_date:
            res.append(movies)
            previous_date = datetime.strptime(movies['end_date'], '%d %b')
            count += 1
    res.append({"profit": count})
    return res


@app.route("/", methods=["POST"])
def max_profit():
    if flask.request.method == "POST":
        if connexion.request.is_json:
            body = connexion.request.get_json()
        sorted_date = sorted(body, key=lambda x: datetime.strptime(x['end_date'], '%d %b'))
        ans = profit(sorted_date)
    return jsonify(ans)


if __name__ == "__main__":
    app.run(host="localhost", debug=True, port=8080)
