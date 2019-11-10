from flask import Flask, render_template, Blueprint, send_file, request, session
import sqrlserver
import nacl.utils
from io import StringIO
from mapartothequeClass import *
from globalVar import *

client = ndb.Client()

from pyqrcode import pyqrcode

bp = Blueprint('loginApi', __name__, url_prefix='/')
key = nacl.utils.random(32)

@bp.route('/auth/login')
def login():
    #url = sqrlserver.Url('mapartotheque.net', 'Ma Partotheque')
    url = sqrlserver.Url('localhost:8080', 'Ma Partotheque')
    urlstr = url.generate('/auth/sqrl', key=key, counter=1)
    qrcode = pyqrcode.create(urlstr)
    imageAsString = qrcode.png_as_base64_str(scale="5")
    return render_template("login.html", url=urlstr, qrcode=imageAsString)

@bp.route('/auth/sqrl', methods=['POST', 'GET'])
def sqrl():
    postparams = request.args
    req = pyqrcode.Request(key, 'Ma partotheque', postparams)
    assert req.state == 'NEW'
    req.handle()
    count = 0
    while req.state != "COMPLETE" or count > 5:

        if req.action[0][0] == "find":
            user = User.request(User.sqrlId==req.action[0][0])
            if user :
                req.handle({"found": [True]})
            else :
                user.sqrlId = req.action[0][0]
                user = User.p
                req.handle({""})
    req.handle({'found': [True]})
    response = req.finalize(counter=101)
    return response.toString()