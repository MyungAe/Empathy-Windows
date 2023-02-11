from flask import Blueprint, request, jsonify, render_template

from pymongo import MongoClient
import certifi

from werkzeug.security import generate_password_hash, check_password_hash
import jwt, datetime
from pytz import timezone, utc

ca = certifi.where()
client = MongoClient('mongodb+srv://project4-Empathy-Windows:Empathy@cluster0.z57zxvu.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.empathy

# app.py : app.register_blueprint(auth.account)
account = Blueprint('auth', __name__, url_prefix="/account/")


@account.route('/signin', methods=["POST"])
def signin():
    user_id = request.form['user_id']
    user_password = request.form['user_password']
    # print(user_id, user_password)

    # 검증
    user_account = db.sample_account.find_one({'id': user_id}, {'_id': False})
    # print(user_account)
    if not user_account:
        return jsonify({'msg': '아이디가 잘못되었습니다.'})

    method = 'pbkdf2:sha256'
    salt = user_account['salt']
    hashed_value = user_account['password']
    hashed_password = method + '$' + salt + '$' + hashed_value

    is_login = check_password_hash(hashed_password, user_password)
    # print(is_login)

    if not is_login:
        return jsonify({'msg': '비밀번호가 잘못되었습니다.'})

    kst = timezone('Asia/Seoul')
    utc_time = datetime.datetime.utcnow()
    kst_time = kst.localize(utc_time)

    print(utc_time, kst_time)

    # JWT
    # header = {
    #     'typ': 'JWT',
    #     'alg': 'HS512'
    # }
    # payload = {
    #     'iss': 'Empathy-Windows',
    #     'aud': user_id,
    #     'exp': datetime.datetime.now(tz=datetime.timezone.utc),
    #     'iat': datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=60),
    # }
    #
    # secret = 'secret'
    #
    # print(header, payload, secret)

    return jsonify({'msg': '로그인이 성공했습니다.'})


@account.route("/signup", methods=["POST"])
def signup():
    user_id = request.form['user_id']
    user_password = request.form['user_password']
    user_nickname = request.form['user_nickname']
    # print('user id : ', user_id)
    # print('user pw : ', user_password)
    # print('user nickname : ', user_nickname)

    method, salt, hashed_pw = generate_password_hash(user_password, method='pbkdf2:sha256').split('$')
    # print('hashed pw : ', hashed_password)
    # print(method, salt, hashed_pw)
    # print('pw and hashed is same? : ', check_password_hash(hashed_password, user_password))
    # method : pbkdf2:sha256

    user_account = {
        'id': user_id,
        'salt': salt,
        'password': hashed_pw,
        'nickname': user_nickname
    }

    db.sample_account.insert_one(user_account)

    return jsonify({'msg': '회원가입 요청이 정상적으로 처리되었습니다.'})
