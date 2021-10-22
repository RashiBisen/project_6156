from flask import Flask, jsonify
import json
from flask import request, Response
from Services.PortalService import portal_svc

app = Flask(__name__)

@app.route('/users', methods=['GET', 'POST'])
def get_users_all():
    if request.method == 'GET':
        template = request.args
        rsp =  portal_svc.find_student()
        rsp = json.dumps(rsp, default=str)
        rsp = Response(rsp, status=200, content_type="application/JSON")
    elif request.method == 'POST':
        data = request.get_json()
        key = 'uni'
        if key not in data:
            rsp =  Response("UNI needs to be specified", status=406)
        else:
            # authenticate user with flask_dance
            res = portal_svc.create_student(data)
            if res == False:
                rsp = Response("UNI already present", status =409)
            else:
                rsp = Response("Successful", status=200)
    else:
        rsp = Response("NOT IMPLEMENTED", status=501)
    return rsp

@app.route('/users/<uni>', methods=['GET', 'PUT'])
def get_user(uni):
    if request.method == 'GET':
        rsp = portal_svc.find_student(uni)
        rsp = json.dumps(rsp, default=str)
        rsp = Response(rsp, status=200, content_type="application/JSON")
        
    elif request.method == 'PUT':
        data = request.get_json()
        data.pop('uni', None)
        rsp = db.update_student(uni, data)
        if rsp is not None:
            rsp = Response("UPDATED", status=201, content_type="text/plain")
        else:
            rsp = Response("UNPROCESSABLE ENTITY", status=422, content_type="text/plain")
    else:
        rsp = Response("NOT IMPLEMENTED", status=501)
    return rsp

if __name__ == "__main__":
	app.run()
