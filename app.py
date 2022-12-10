from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

import random

from pymongo import MongoClient
import certifi
ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.n5f9qy4.mongodb.net/cluste0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/todo", methods=["POST"])
def todo_post():
    todo_receive = request.form['todo_give']

    todo_list = list(db.todo.find({}, {'_id': False}))
    count = random.randrange(1,1000)

    doc = {
        'todo': todo_receive,
        'num': count,
        'done': 0
    }

    db.todo.insert_one(doc)

    return jsonify({'msg': '등록완료!'})

@app.route("/todo/done", methods=["POST"])
def todo_done():
    num_receive = request.form['num_give']
    db.todo.update_one({'num': int(num_receive)}, {'$set': {'done': 1}})
    return jsonify({'msg': '투두완료!'})

@app.route("/todo/cancel", methods=["POST"])
def todo_cancel():
    num_receive = request.form['num_give']
    db.todo.update_one({'num': int(num_receive)}, {'$set': {'done': 0}})
    return jsonify({'msg': '취소완료!'})

@app.route("/todo/empty", methods=["POST"])
def todo_empty():
    num_receive = request.form['num_give']
    db.todo.delete_one({'num': int(num_receive)})
    return jsonify({'msg': '삭제완료!'})

@app.route("/todo", methods=["GET"])
def todo_get():
    todo_list = list(db.todo.find({}, {'_id': False}))
    return jsonify({'todos': todo_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
