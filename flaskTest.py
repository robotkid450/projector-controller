#!/usr/bin/env python3

from flask import Flask, render_template, request


app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def show_login():
	if request.method == 'GET':
		print("nom")
		return render_template('projector control.html')
	
	elif request.method == 'POST':
		action = request.form['submit']
		
		if action == 'powerOn':
			return "power on"
		
    
@app.route('/login', methods=['POST'])
def process_login():
	_uname = request.form['username']
	_password = reqest.form['password']
	
@app.route('/lampHours')
def show_lamp_hours():
	return "lamp hours"
    
    
if __name__ == "__main__":
    app.run()
