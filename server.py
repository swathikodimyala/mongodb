from bottle import Bottle, run, route, static_file, request, response, template, redirect
from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId
import json
import pymongo
import time
import os


app = Bottle(__name__)

client = MongoClient('mongodb://ocl:ocl@13.126.64.71/ocl_test')
db = client.ocl_test


@app.route('/')
def root():
    cur = db.web_demo.find({'user':"Santosh"})
    data = json.loads(dumps(cur))
    
    return template('templates/index.tpl', res=data)

@app.route('/add')
def add_data():
    return static_file('form.html', root='templates')

@app.post('/add')
def add_data():
    img = request.forms.get('img')
    name = request.forms.get('name')

    cur = db.web_demo.insert({'img': img, 'name': name, 'user':"Santosh"})

    redirect('/')


@app.route('/del/<oid_data>')
def del_data(oid_data):
    cur = db.web_demo.remove({'_id': ObjectId(str(oid_data))})

    return {'status': 'ok'}	

@app.route('/manifest')
def manifest():
    return static_file('manifest.json', root='')

# Static Routes
@app.route('/<filename:re:.*\.html>')
def javascripts(filename):
    return static_file(filename, root='templates')

@app.route('/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='static')

@app.route('/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='static')

@app.route('/<filename:re:.*\.(jpg|png|gif|ico|svg)>')
def images(filename):
    return static_file(filename, root='static')

@app.route('/<filename:re:.*\.(eot|ttf|woff|svg)>')
def fonts(filename):
    return static_file(filename, root='static')

@app.route('/<filename:re:.*\.html>')
def javascripts(filename):
    return static_file(filename, root='static')

@app.hook('after_request')
def enable_cors():
	response.headers['Access-Control-Allow-Origin'] = '*'
	response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
	response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'