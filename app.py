from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca = certifi.where()
client = MongoClient("mongodb+srv://project4-Empathy-Windows:Empathy@cluster0.z57zxvu.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=ca)
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
    'id' : id_receive,
    'pw' : pw_receive,
    'nick' : nick_receive
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

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)