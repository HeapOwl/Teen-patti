from flask import *
from flask_cors import CORS,cross_origin
import json
json_read = json.load(open('temp.json','r'))
mon=0
app=Flask(__name__)
CORS(app)
@app.route('/')
def clicker():
	#mon=0
	response = make_response(render_template('clicker.html', money = mon))
	response.headers['Access-Control-Allow-Origin']='http://localhost/'
	return response
@app.route('/add')
def add():
	global mon
	mon+=1
	return render_template('clicker.html',money = mon)
@app.route('/refresh')
def refresh():
	return render_template('clicker.html',money = mon)
if __name__=='__main__':
	app.run(debug=True)