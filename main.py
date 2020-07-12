import connexion
from datetime import datetime
import flask
from flask import jsonify

app = flask.Flask(__name__)


def profit(data):
    res = {'movies': [], 'profit': 0}
    count = 0
    previous_date = 0
    for movies in data:

        if count == 0:
            res['movies'].append(movies)
            previous_date = datetime.strptime(movies['end_date'], '%d %b')
            count += 1
            continue
        current_date = datetime.strptime(movies['start_date'], '%d %b')
        if current_date > previous_date:
            res['movies'].append(movies)
            previous_date = datetime.strptime(movies['end_date'], '%d %b')
            count += 1
    res['profit'] = str(count) + " Crores"
    return res


def errors(data):
    err = {"references": []}
    for da in data['movies']:

        temp = {"original_data": {}, "error_type": []}
        if not da:
            temp['original_data'] = da
            temp['error_type'].append("No data found")
        else:
            if len(da) < 3:
                temp['original_data'] = da
                temp['error_type'].append("Incomplete Data")
            else:
                if len(da['movie_name'].strip()) == 0:
                    temp['original_data'] = da
                    temp['error_type'].append(" invalid movie name ")

                try:
                    if len(da['start_date'].strip()) != 0 and len(da['end_date'].strip()) != 0:
                        start = datetime.strptime(da['start_date'], '%d %b')
                        end = datetime.strptime(da['end_date'], '%d %b')
                        if start > end:
                            temp['original_data'] = da
                            temp['error_type'].append("start time greater than end time")
                    else:
                        temp['original_data'] = da
                        temp['error_type'].append("no date given")
                except ValueError:
                    temp['original_data'] = da
                    temp['error_type'].append(" invalid date format ")
        if len(temp['error_type']) != 0:
            err["references"].append(temp)
    return err


@app.route("/", methods=["POST"])
def max_profit():
    if flask.request.method == "POST":
        if connexion.request.is_json:
            body = connexion.request.get_json()
        if len(body) == 0:
            return jsonify('empty request'), 400
        if len(body['movies']) == 0:
            return jsonify({"error": "There are no movies in the list"}), 400
        error_list = errors(body)
        if len(error_list['references']) > 0:
            return jsonify(error_list), 400

        sorted_date = sorted(body['movies'], key=lambda x: datetime.strptime(x['end_date'], '%d %b'))
        answer = profit(sorted_date)
    return jsonify(answer), 200


if __name__ == "__main__":
    app.run(host="localhost", debug=True, port=8080)
