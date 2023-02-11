from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
import certifi
ca = certifi.where()
client = MongoClient('mongodb+srv://project4-Empathy-Windows:Empathy@cluster0.z57zxvu.mongodb.net/cluster0?retryWrites=true&w=majority',tlsCAFile=ca)
db = client.empathy


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/music/comment", methods=["POST"])
def comment_post():
    comment_receive = request.form['comment_give']
    date_receive = request.form['date_give']


    comment_list = list(db.comments.find({}, {'_id': False}))
    count = len(comment_list) + 1

    # 회원정보들 = list(db.'회원정보들'.find({}, {'_id': False}))
    # for 회원정보 in 회원정보들:
    #     nickname = 회원정보['nickname']
    #
    # 음악목록들 = list(db.'음악목록들'.find({}, {'_id': False}))
    # for 음악목록 in 음악목록들:
    #     music_name  = 회원정보['music_name ']

    doc = {
        # 'nickname' : nickname,
        'num': count,
        'comment': comment_receive,
        'date': date_receive,
        # 'music_name' : music_name,
    }

    db.comments.insert_one(doc)

    return jsonify({'msg': '등록 완료!!!'})

@app.route("/music/comment", methods=["GET"])
def bucket_get():
    comment_list = list(db.comments.find({}, {'_id': False}))

    return jsonify({'comments': comment_list})

@app.route("/music/comment", methods=["DELETE"])
def movie_de():
    title_receive = request.form['title_give']

    db.movies2.delete_one({'title': title_receive})


    return jsonify({'msg':'삭제 완료!!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)