from flask import Flask, jsonify
import json
from flask import request, Response
from Services.PortalService import portal_svc
from Middleware import secure_auth
import os
from dotenv import dotenv_values
from flask import  redirect, url_for
from flask_dance.contrib.google import make_google_blueprint, google


app = Flask(__name__)

config = dotenv_values("google_key.env")
app.config["GOOGLE_OAUTH_CLIENT_ID"] = config["GOOGLE_OAUTH_CLIENT_ID"]
app.config["GOOGLE_OAUTH_CLIENT_SECRET"] = config["GOOGLE_OAUTH_CLIENT_SECRET"]
app.secret_key = "some key"
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

blueprint = make_google_blueprint(
    client_id=app.config["GOOGLE_OAUTH_CLIENT_ID"],
    client_secret=app.config["GOOGLE_OAUTH_CLIENT_SECRET"],
    reprompt_consent=True,
    scope=["profile", "email"]
)

app.register_blueprint(blueprint, url_prefix="/login")
google_bp = app.blueprints.get("google")

@app.before_request
def before_request_func():
    result_ok = secure_auth.check_auth(request, google, google_bp)
    if not result_ok:
        return redirect(url_for('google.login'))

@app.route('/login')
def login():
    return redirect(url_for('google.login'))



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
        rsp = portal_svc.update_student(uni, data)
        if rsp is not None:
            rsp = Response("UPDATED", status=201, content_type="text/plain")
        else:
            rsp = Response("UNPROCESSABLE ENTITY", status=422, content_type="text/plain")
    else:
        rsp = Response("NOT IMPLEMENTED", status=501)
    return rsp

@app.route('/users/<uni>/skills', methods={'GET', 'PUT'})
def get_skills_all(uni):
    if request.method == 'GET':
        rsp = portal_svc.find_skill(uni)
        rsp = json.dumps(rsp, default=str)
        rsp = Response(rsp, status=200, content_type="application/JSON")
        
    elif request.method == 'PUT':
        data = request.get_json()
        data.pop('uni', None)
        rsp = portal_svc.update_student_skill(uni, data)
        if rsp is not None:
            rsp = Response("UPDATED", status=201, content_type="text/plain")
        else:
            rsp = Response("UNPROCESSABLE ENTITY", status=422, content_type="text/plain")
    else:
        rsp = Response("NOT IMPLEMENTED", status=501)
    return rsp


@app.route('/users/<uni>/skills/<skill>', methods={'GET'})
def get_skill(uni, skill):
    template = {"Skills.skill":skill}
    rsp =  portal_svc.find_skill(uni, template)
    res = []
    for item in rsp:
        if item['skill'] == skill:
            res.append(item)
    
    rsp = json.dumps(res, default=str)
    rsp = Response(rsp, status=200, content_type="application/JSON")
    return rsp

if __name__ == "__main__":
	app.run()
