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

# router
from flask_jwt_extended import JWTManager
from datetime import timedelta
from server import auth

app.register_blueprint(auth.account)

app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['JWT_SECRET_KEY'] = 'secret'
jwt = JWTManager(app)


## 회원가입 페이지 경로
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


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

    nicknames = list(user_db.empathy.find({}, {'_id': False}))
    for a in nicknames:
        nickname = a['nick']

    musics = list(user_db.music.find({}, {'_id': False}))
    for b in musics:
        music_name = b['title']
    doc = {
        'nickname': nickname,
        'num': count,
        'comment': comment_receive,
        'date': date_receive,
        'music_name': music_name,
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
    comment_num_receive = request.form['num_give']
    print(type(comment_num_receive))
    user_db.comments.update_one({'num': int(comment_num_receive)}, {'$set': {'comment': comment_receive}})
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



