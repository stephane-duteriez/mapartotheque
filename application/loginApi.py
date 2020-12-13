from flask import Flask, render_template, Blueprint, send_file, request, session, current_app
import application.sqrlserver as sqrlserver
import nacl.utils
from io import StringIO
from .mapartothequeClass import Tune, Session, Tune_in_session, Rythm, RythmForDisplay, User
from . import client, sess, redis_client, APPURL

from pyqrcode import pyqrcode

bp = Blueprint('loginApi', __name__, url_prefix='/')
key = redis_client.get("keySqrl")
if not key:
    key = nacl.utils.random(32)
    redis_client.set("keySqrl", str(key))

@bp.route('/auth/check')
def checkIsLogin():
    sqrlId = redis_client.get("idSession_" + session.sid)
    print("checkIsLogin :" + str(sqrlId))
    if sqrlId :
        session["username"] = sqrlId
        return "Ok"
    return "notOk"

@bp.route('/auth/logout')
def logout():
    redis_client.delete("idSession_" + session.sid)
    session["username"] = None
    return "You are now log out!"

@bp.route('/auth/sqrl', methods=['POST', 'GET'])
def sqrl():
    clientSqrl = request.form.get("client")
    serverSqrl = request.form.get("server")
    idsSqrl = request.form.get("ids")
    fromQrcode = request.args["typeSqrl"]
    nut = request.args.get("nut")
    req = sqrlserver.Request(key, {"nut":nut, "ids":idsSqrl, "server":serverSqrl, "client":clientSqrl})
    assert req.state == 'NEW'
    req.handle()
    count = 0
    print("sqrl")
    print("sqrl_login :" + req.state)
    while req.state != "COMPLETE" and count < 5:
        count += 1
        print("sqrl_login :" + str(req.action[0][0]) + ":" + str(req.action[0][1]))
        if req.action[0][0] == "find":
            with client.context() as context:
                user = User.query(User.sqrlId==req.action[0][1][0]).get()
                print("sqrl_login user: " + str(user))
                if user :
                    req.handle({"found": [True]})
                else :
                    req.handle({"found": [False]})
        elif req.action[0][0] == "auth":
            with client.context() as context:
                print("request sid :" + request.args["sid"])
                user = User.query(User.sqrlId==req.action[0][1]).get()
                if not user :
                    user = User()
                    user.sqrlId = req.action[0][1]
                    user.put()
                print("sqrlid = " + str(user.sqrlId))
                redis_client.set("idSession_" + request.args["sid"], user.sqrlId)
            req.handle({"authenticated" : True, "url" : "/auth/login"})
        elif req.action[0][0] == "confirm":
            if req.action[0][1][0] == "time":
                req.handle({"confirmed": True})
        print("sqrl_login :" + req.state)
    response = req.finalize(counter=101)
    return response.toString()

@bp.route('/auth/success')
def success():
    sqrlId = redis_client.get("idSession_" + session.sid)
    print("success :" + str(sqrlId))
    print("Session : " + str(session.sid))
    if sqrlId :
        session["username"] = sqrlId
    if "username" in session:
        return "Your are logged in"
    else :
        return "Your are not logged in"

@bp.route('/auth/login')
def login():
    url = sqrlserver.Url("localhost:8080", 'Ma Partotheque')
    urlstrQrcode = url.generate('/auth/sqrl', key=key, counter=1, query=[("sid" , session.sid), ("typeSqrl", "qrcode")])
    urlstrLink = url.generate('/auth/sqrl', key=key, counter=1, query=[("ids" , session.sid)], type="link")
    qrcode = pyqrcode.create(urlstrQrcode)
    imageAsString = qrcode.png_as_base64_str(scale="5")
    redis_client.set("sqrlId_" + url.nutstr, session.sid)
    return render_template("login.html", url=urlstrLink, qrcode=imageAsString)