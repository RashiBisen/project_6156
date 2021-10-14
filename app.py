from flask import Flask, jsonify
import json
from flask import request
import aws_controller

app = Flask(__name__)

@app.route('/users', methods=['GET'])
def get_all_users():
	return jsonify(aws_controller.get_all_users())

@app.route('/user', methods=['GET', 'PUT'])
def get_user():
    if request.method == 'GET':
        uni = request.args.get('uni')
        return jsonify(aws_controller.get_user(uni))
    else:
        uni = request.form['uni']
        data = request.get_json()
        aws_controller.update_item(uni, data)
        return jsonify({'status':'OK'})


if __name__ == "__main__":
	app.run()
