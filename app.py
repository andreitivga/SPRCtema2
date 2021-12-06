from flask import Flask, jsonify
import pymongo
from pymongo import MongoClient

app = Flask(__name__)

def get_db():
	client = MongoClient(host='sprc_mongodb',
						 port=27017,
						 username='root',
						 password='pass',
						 authSource='admin')

	db = client["temp_db"]
	print(db)
	return db


@app.route('/')
def home():
	return("Hello")


@app.route('/get')
def get_info():
	db = get_db()

	_info = db.temp_db.find()
	info = [{'name':info['name']} for info in _info]
	return jsonify({"info": info})

@app.route('/post')
def post_info():

	db = get_db()
	list_to_insert = [
	{
		"name":"Andrei"
	},
	{
		"name":"Ana"
	},
	
	]

	db.temp_db.insert_many(list_to_insert)

	return "inserted"

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)