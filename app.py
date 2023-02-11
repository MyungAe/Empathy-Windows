# Flask 서버 사용을 위한 import
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# 크롤링을 위한 import
import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200', headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

# MongoDB 사용을위한 import
from pymongo import MongoClient
import certifi

ca = certifi.where()
client = MongoClient(
    "mongodb+srv://project4-Empathy-Windows:Empathy@cluster0.z57zxvu.mongodb.net/?retryWrites=true&w=majority",
    tlsCAFile=ca)

user_db = client.empathy


## 회원가입 페이지 경로
@app.route('/')
def home():
    return render_template('index.html')


## 회원가입 페이지 경로
@app.route('/account/signup2')
def account_signup2():
    return render_template('signup.html')


## 회원가입 DB저장 경로
@app.route('/account/signup2check', methods=["POST"])
def account_signup2_check():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    nick_receive = request.form['nick_give']

    doc = {
        'id': id_receive,
        'pw': pw_receive,
        'nick': nick_receive
    }
    user_db.empathy.insert_one(doc)

    return jsonify({'msg': '회원가입성공'})


## 로그인 DB확인 및 승인
@app.route('/account/signin2', methods=["POST"])
def account_signin2():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    print(id_receive, pw_receive)

    return jsonify({'msg': '로그인성공'})


# 음악 창구 홈페이지 불러오기
@app.route('/musics')
def music():
    return render_template('musicpage.html')


# 음악 보여주기
musicLists = soup.select('#body-content > div.newest-list > div > table > tbody > tr')
for musicList in musicLists:
    a = musicList.select_one('td.info > a.title.ellipsis').text.strip().lstrip()
    if a is not None:
        rank = musicList.select_one('td.number').text[0:2].strip()
        singer = musicList.select_one('td.info > a.artist.ellipsis').text
        title = a
        doc = {
            'rank': rank,
            'singer': singer,
            'title': title
        }
        user_db.music.insert_one(doc)

@app.route("/music", methods=["GET"])
def music_get():
    musicList = list(user_db.music.find({}, {'_id': False}))

    return jsonify({'music': musicList[:20]})


# 댓글 저장
@app.route("/music/comment", methods=["POST"])
def comment_post():
    comment_receive = request.form['comment_give']
    date_receive = request.form['date_give']

    comment_list = list(user_db.comments.find({}, {'_id': False}))
    count = len(comment_list) + 1

    # 회원정보들 = list(db.'회원정보들'.find({}, {'_id': False}))
    # for 회원정보 in 회원정보들:
    #     nickname = 회원정보['nickname']
    #
    # 음악목록들 = list(db.'음악목록들'.find({}, {'_id': False}))
    # for 음악목록 in 음악목록들:
    #     music_name  = 회원정보['music_name ']

    doc = {
        'nickname': 'ksg',
        'num': count,
        'comment': comment_receive,
        'date': date_receive,
        'music_name': 'human',
    }

    user_db.comments.insert_one(doc)

    return jsonify({'msg': '등록 완료!!!'})


# 댓글 조회
@app.route("/music/comment", methods=["GET"])
def comment_get():
    comment_list = list(user_db.comments.find({}, {'_id': False}))

    return jsonify({'comments': comment_list})


# 댓글 수정
@app.route("/music/comment", methods=["PATCH"])
def comment_update():
    comment_receive = request.form["comment_give"]
    print(comment_receive)
    user_db.comments.update_one({'name': 'Mercedes Tyler'}, {'$set': {'text': comment_receive}})
    return jsonify({'msg': '수정되었습니다!'})


# 댓글 삭제
@app.route("/music/comment", methods=["DELETE"])
def comment_del():
    num_receive = request.form['num_give']
    print(type(num_receive))
    user_db.comments.delete_one({'num': int(num_receive)})
    return jsonify({'msg': '삭제 완료!!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)




###

# from flask import Flask, render_template
# from flask_jwt_extended import JWTManager

# from datetime import timedelta

# # router
# from server import auth


# app = Flask(__name__)

# # router
# app.register_blueprint(auth.account)

# # jwt config
# app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
# app.config['JWT_SECRET_KEY'] = 'secret'
# jwt = JWTManager(app)


# @app.route('/', methods=['GET'])
# def home():
#     return render_template('index.html')



# if __name__ == '__main__':
#     app.run('0.0.0.0', port=5001, debug=True)

# from flask import Flask, render_template, request, jsonify

# ca = certifi.where()
# client = MongoClient(
#     'mongodb+srv://project4-Empathy-Windows:Empathy@cluster0.z57zxvu.mongodb.net/?retryWrites=true&w=majority',
#     tlsCAFile=ca)
# db = client.empathy



# @app.route('/music')
# def music():
#     return render_template('index.html')

# @app.route('/comment')
# def comment():
#     return render_template('comment.html')







# # 댓글 저장
# @app.route("/music/comment", methods=["POST"])
# def comment_post():
#     comment_receive = request.form['comment_give']
#     date_receive = request.form['date_give']

#     comment_list = list(db.comments.find({}, {'_id': False}))
#     count = len(comment_list) + 1

#     # 회원정보들 = list(db.'회원정보들'.find({}, {'_id': False}))
#     # for 회원정보 in 회원정보들:
#     #     nickname = 회원정보['nickname']
#     #
#     # 음악목록들 = list(db.'음악목록들'.find({}, {'_id': False}))
#     # for 음악목록 in 음악목록들:
#     #     music_name  = 회원정보['music_name ']

#     doc = {
#         'nickname': 'ksg',
#         'num': count,
#         'comment': comment_receive,
#         'date': date_receive,
#         'music_name': 'human',
#     }

#     db.comments.insert_one(doc)

#     return jsonify({'msg': '등록 완료!!!'})


# # 댓글 조회
# @app.route("/music/comment", methods=["GET"])
# def comment_get():
#     comment_list = list(db.comments.find({}, {'_id': False}))

#     return jsonify({'comments': comment_list})


# # 댓글 삭제
# @app.route("/music/comment", methods=["DELETE"])
# def comment_de():
#     num_receive = request.form['num_give']
#     db.comments.delete_one({'num': num_receive})
#     return jsonify({'msg': '삭제 완료!!'})

# # Flask 서버 사용을 위한 import
# from flask import Flask, render_template, request, jsonify

# app = Flask(__name__)

# # 크롤링을 위한 import
# import requests
# from bs4 import BeautifulSoup

# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
# data = requests.get('https://www.genie.co.kr/chart/top200', headers=headers)

# soup = BeautifulSoup(data.text, 'html.parser')

# # MongoDB 사용을위한 import
# from pymongo import MongoClient
# import certifi

# ca = certifi.where()
# client = MongoClient(
#     "mongodb+srv://project4-Empathy-Windows:Empathy@cluster0.z57zxvu.mongodb.net/?retryWrites=true&w=majority",
#     tlsCAFile=ca)

# user_db = client.empathy


# ## 회원가입 페이지 경로
# @app.route('/')
# def home():
#     return render_template('index.html')


# ## 회원가입 페이지 경로
# @app.route('/account/signup2')
# def account_signup2():
#     return render_template('signup.html')


# ## 회원가입 DB저장 경로
# @app.route('/account/signup2check', methods=["POST"])
# def account_signup2_check():
#     id_receive = request.form['id_give']
#     pw_receive = request.form['pw_give']
#     nick_receive = request.form['nick_give']

#     doc = {
#         'id': id_receive,
#         'pw': pw_receive,
#         'nick': nick_receive
#     }
#     user_db.empathy.insert_one(doc)

#     return jsonify({'msg': '회원가입성공'})


# ## 로그인 DB확인 및 승인
# @app.route('/account/signin2', methods=["POST"])
# def account_signin2():
#     id_receive = request.form['id_give']
#     pw_receive = request.form['pw_give']
#     print(id_receive, pw_receive)

#     return jsonify({'msg': '로그인성공'})


# # 홈페이지 불러오기
# @app.route('/musics')
# def music():
#     return render_template('musicpage.html')


# # 보여주기
# musicLists = soup.select('#body-content > div.newest-list > div > table > tbody > tr')
# for musicList in musicLists:
#     a = musicList.select_one('td.info > a.title.ellipsis').text.strip().lstrip()
#     if a is not None:
#         rank = musicList.select_one('td.number').text[0:2].strip()
#         singer = musicList.select_one('td.info > a.artist.ellipsis').text
#         title = a
#         doc = {
#             'rank': rank,
#             'singer': singer,
#             'title': title
#         }
#         user_db.music.insert_one(doc)


# @app.route("/music", methods=["GET"])
# def music_get():
#     musicList = list(user_db.music.find({}, {'_id': False}))

#     return jsonify({'music': musicList[:20]})


# # 수정하기
# @app.route("/music/comment/", methods=["FATCH"])
# def comment_update():
#     comment_receive = request.form["comment_give"]
#     print(comment_receive)
#     db.comments.update_one({'name': 'Mercedes Tyler'}, {'$set': {'text': comment_receive}})
#     return jsonify({'msg': '수정되었습니다!'})
