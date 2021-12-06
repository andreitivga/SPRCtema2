from flask import Flask, jsonify, Response, request
import pymongo
from pymongo import MongoClient
import mongoengine
from mongoengine import Document, FloatField, StringField, IntField, DateTimeField, ReferenceField, connect
from structure import Tari, Orase, Temperaturi
from datetime import datetime

app = Flask(__name__)

client = MongoClient(host='sprc_mongodb',
					 port=27017,
					 username='root',
					 password='pass',
					 authSource='admin')

db = client["temp_db"]
connect(
	db="temp_db",
	host='sprc_mongodb',
	username='root',
	password='pass',
	authentication_source='admin'
	)

def get_db(col):
	db = client["temp_db"]
	return db


@app.route('/')
def home():
	return("Hello")


@app.route('/api/countries', methods=["POST"])
def post_country():
	body = request.json

	if 'nume' not in body:
		return Response(status=400)

	if 'lat' not in body:
		return Response(status=400)

	if 'lon' not in body:
		return Response(status=400)

	nume_tara = body['nume']
	latitudine = body['lat']
	longitudine = body['lon']

	tara = Tari(nume_tara=nume_tara, latitudine=latitudine, longitudine=longitudine)

	try:
		tara.save()

	except mongoengine.errors.ValidationError:
		return Response(status=400)

	except mongoengine.errors.NotUniqueError:
		return Response(status=409)

	return jsonify({'id':str(tara.pk)}), 201


@app.route('/api/countries', methods=["GET"])
def get_countries():
	resp_list = []

	for doc in Tari.objects:
		resp = {'id': str(doc.pk), 'nume':doc.nume_tara, 'lat':doc.latitudine, 'lon':doc.longitudine} 
		resp_list.append(resp)

	return jsonify(resp_list), 200

	
@app.route('/api/countries/<id_tara>', methods=["PUT"])
def put_countries(id_tara):
	body = request.json

	if 'id' not in body:
		return Response(status=400)

	if 'nume' not in body:
		return Response(status=400)

	if 'lat' not in body:
		return Response(status=400)

	if 'lon' not in body:
		return Response(status=400)

	nume_tara = body['nume']
	latitudine = body['lat']
	longitudine = body['lon']

	try:
		tara = Tari.objects(pk=id_tara).get()
		tara.update(nume_tara=nume_tara, latitudine=latitudine, longitudine=longitudine)

	except mongoengine.errors.NotUniqueError:
		return Response(status=409)

	except mongoengine.errors.DoesNotExist:
		return Response(status=404)

	except mongoengine.errors.ValidationError:
		return Response(status=400)

	return Response(status=200)


@app.route('/api/countries/<id_tara>', methods=["DELETE"])
def del_country(id_tara):

	for doc in Tari.objects:
		if str(doc.pk) == id_tara:
			try:			
				doc.delete()
			except:
				return Response(status=400)

			return Response(status=200)

	return Response(status=404)


@app.route('/api/cities', methods=["POST"])
def post_city():
	body = request.json

	if 'idTara' not in body:
		return Response(status=400)

	if 'nume' not in body:
		return Response(status=400)

	if 'lat' not in body:
		return Response(status=400)

	if 'lon' not in body:
		return Response(status=400)

	id_tara = body['idTara']
	nume_oras = body['nume']
	latitudine = body['lat']
	longitudine = body['lon']

	try:
		tara = Tari.objects(pk=id_tara).get()

	except mongoengine.errors.ValidationError:
		return Response(status=400)

	except mongoengine.errors.DoesNotExist:
		return Response(status=400)


	oras = Orase(id_tara=tara, nume_oras=nume_oras, latitudine=latitudine, longitudine=longitudine)

	try:
		oras.save()

	except mongoengine.errors.ValidationError:
		return Response(status=400)

	except mongoengine.errors.NotUniqueError:
		return Response(status=409)

	return jsonify({'id':str(oras.pk)}), 201


@app.route('/api/cities', methods=["GET"])
def get_cities():
	resp_list = []

	for doc in Orase.objects:
		resp = {'id': str(doc.pk), 'idTara':str(doc.id_tara.pk), 'nume':doc.nume_oras, 'lat':doc.latitudine, 'lon':doc.longitudine} 
		resp_list.append(resp)

	return jsonify(resp_list), 200


@app.route('/api/cities/country/<id_tara>', methods=["GET"])
def get_cities_from_country(id_tara):
	resp_list = []

	try:
		tara = Tari.objects(pk=id_tara).get()
	except:
		return jsonify(resp_list), 200


	for doc in Orase.objects:
		if doc.id_tara == tara:
			resp = {'id': str(doc.pk), 'idTara':str(doc.id_tara.pk), 'nume':doc.nume_oras, 'lat':doc.latitudine, 'lon':doc.longitudine} 
			resp_list.append(resp)

	return jsonify(resp_list), 200


@app.route('/api/cities/<id_oras>', methods=["PUT"])
def put_cities(id_oras):
	body = request.json

	if 'id' not in body:
		return Response(status=400)

	if 'idTara' not in body:
		return Response(status=400)

	if 'nume' not in body:
		return Response(status=400)

	if 'lat' not in body:
		return Response(status=400)

	if 'lon' not in body:
		return Response(status=400)

	nume_oras = body['nume']
	latitudine = body['lat']
	longitudine = body['lon']

	try:
		oras = Orase.objects(pk=id_oras).get()
		oras.update(nume_oras=nume_oras, latitudine=latitudine, longitudine=longitudine)

	except mongoengine.errors.NotUniqueError:
		return Response(status=409)

	except mongoengine.errors.DoesNotExist:
		return Response(status=404)

	except mongoengine.errors.ValidationError:
		return Response(status=400)

	return Response(status=200)


@app.route('/api/cities/<id_oras>', methods=["DELETE"])
def del_city(id_oras):

	for doc in Orase.objects:
		if str(doc.pk) == id_oras:
			try:			
				doc.delete()
			except:
				return Response(status=400)

			return Response(status=200)

	return Response(status=404)


@app.route('/api/temperatures', methods=["POST"])
def post_temp():
	body = request.json

	if 'id_oras' not in body:
		return Response(status=400)

	if 'valoare' not in body:
		return Response(status=400)

	id_oras = body['id_oras']
	valoare = body['valoare']

	try:
		oras = Orase.objects(pk=id_oras).get()

	except mongoengine.errors.ValidationError:
		return Response(status=400)

	except mongoengine.errors.DoesNotExist:
		return Response(status=400)

	timestamp = datetime.now()

	temp = Temperaturi(id_oras=oras, valoare=valoare, timestamp=timestamp)

	try:
		temp.save()

	except mongoengine.errors.ValidationError:
		return Response(status=400)

	except mongoengine.errors.NotUniqueError:
		return Response(status=409)

	return jsonify({'id':str(temp.pk)}), 201


@app.route('/api/temperatures', methods=["GET"])
def get_temps():

	lat = request.args.get('lat') 
	lon = request.args.get('lon')
	start_date = request.args.get('from')
	end_date = request.args.get('until')

	start_date_obj = datetime.strptime("1000-01-01", '%Y-%m-%d')
	end_date_obj = datetime.strptime('2100-12-31', '%Y-%m-%d')

	if start_date:
		start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')

	if end_date:
		end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')

	if not lat and not lon:
		resp_list = []
		for doc in Temperaturi.objects(timestamp__gte=start_date_obj, timestamp__lte=end_date_obj):
			resp = {'id': str(doc.pk), 'id_oras':str(doc.id_oras.pk), 'valoare':doc.valoare, 'time':doc.timestamp} 
			resp_list.append(resp)

		return jsonify(resp_list), 200

	if lat and not lon: 
		resp_list = [] 
		for doc in Temperaturi.objects(timestamp__gte=start_date_obj, timestamp__lte=end_date_obj):
			oras = doc.id_oras
			if float(lat) == oras.latitudine:
				resp = {'id': str(doc.pk), 'id_oras':str(doc.id_oras.pk), 'valoare':doc.valoare, 'time':doc.timestamp} 
				resp_list.append(resp)

		return jsonify(resp_list), 200

	if lon and not lat: 
		resp_list = []
		for doc in Temperaturi.objects(timestamp__gte=start_date_obj, timestamp__lte=end_date_obj):
			oras = doc.id_oras
			if float(lon) == oras.longitudine:
				resp = {'id': str(doc.pk), 'id_oras':str(doc.id_oras.pk), 'valoare':doc.valoare, 'time':doc.timestamp} 
				resp_list.append(resp)

		return jsonify(resp_list), 200 

	if lon and lat: 
		resp_list = []
		for doc in Temperaturi.objects(timestamp__gte=start_date_obj, timestamp__lte=end_date_obj):
			oras = doc.id_oras
			if float(lon) == oras.longitudine and float(lat) == oras.latitudine:
				resp = {'id': str(doc.pk), 'id_oras':str(doc.id_oras.pk), 'valoare':doc.valoare, 'time':doc.timestamp} 
				resp_list.append(resp)

		return jsonify(resp_list), 200


@app.route('/api/temperatures/cities/<id_oras>', methods=["GET"])
def get_temps_city(id_oras):

	start_date = request.args.get('from')
	end_date = request.args.get('until')

	start_date_obj = datetime.strptime("1000-01-01", '%Y-%m-%d')
	end_date_obj = datetime.strptime('2100-12-31', '%Y-%m-%d')

	if start_date:
		start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')

	if end_date:
		end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')

	resp_list=[]
	try:
		oras = Orase.objects(pk=id_oras).get()
	except:
		return jsonify({'resp_list': resp_list}), 200

	for doc in Temperaturi.objects(timestamp__gte=start_date_obj, timestamp__lte=end_date_obj):
		if doc.id_oras == oras:
			resp = {'id': str(doc.pk), 'id_oras':str(doc.id_oras.pk), 'valoare':doc.valoare, 'time':doc.timestamp} 
			resp_list.append(resp)

	return jsonify(resp_list), 200


@app.route('/api/temperatures/countries/<id_tara>', methods=["GET"])
def get_temps_country(id_tara):

	start_date = request.args.get('from')
	end_date = request.args.get('until')

	start_date_obj = datetime.strptime("1000-01-01", '%Y-%m-%d')
	end_date_obj = datetime.strptime('2100-12-31', '%Y-%m-%d')

	if start_date:
		start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')

	if end_date:
		end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')

	resp_list = []
	try:
		tara = Tari.objects(pk=id_tara).get()
	except:
		return jsonify({'resp_list': resp_list}), 200

	for doc in Temperaturi.objects(timestamp__gte=start_date_obj, timestamp__lte=end_date_obj):
		oras = doc.id_oras
		tara_temp = oras.id_tara
		if tara_temp == tara:
			resp = {'id': str(doc.pk), 'id_oras':str(doc.id_oras.pk), 'valoare':doc.valoare, 'time':doc.timestamp} 
			resp_list.append(resp)

	return jsonify(resp_list), 200


@app.route('/api/temperatures/<id_temp>', methods=["PUT"])
def put_temps(id_temp):
	body = request.json

	if 'id' not in body:
		return Response(status=400)

	if 'idOras' not in body:
		return Response(status=400)

	if 'valoare' not in body:
		return Response(status=400)

	valoare = body['valoare']
	timestamp = datetime.now()

	try:
		temp = Temperaturi.objects(pk=id_temp).get()
		temp.update(valoare=valoare, timestamp=timestamp)

	except mongoengine.errors.DoesNotExist:
		return Response(status=404)

	except mongoengine.errors.ValidationError:
		return Response(status=400)

	return Response(status=200)


@app.route('/api/temperatures/<id_temp>', methods=["DELETE"])
def del_temps(id_temp):

	for doc in Temperaturi.objects:
		if str(doc.pk) == id_temp:
			try:			
				doc.delete()
			except:
				return Response(status=400)

			return Response(status=200)

	return Response(status=404)


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)