#!/usr/bin/env python3
import SanyoProtocol as Sanyo

from flask import Flask, render_template, request


app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def main_control():
	#p1 = Sanyo.projector(port='/dev/ttyS0')
	#p2 = Sanyo.projector(port='/dev/ttyS1')
	p1 = Sanyo.projector(port='/dev/ttyUSB0')
	p2 = Sanyo.projector(port='/dev/ttyUSB1')
	statusP1 = p1.getStatusGeneral()
	#status = 'a'
	if request.method == 'GET':
		print("nom")
		return render_template('projector_control.html', statusP1 = statusP1)

	elif request.method == 'POST':
		print(request.form)
		action = request.form['submit']
		print(action)
		if action == 'powerOn':
			print("power on")

		return render_template('projector_control.html')

@app.route('/confirm', methods=['POST','GET'])
def show_confirmation():
	if request.method == 'POST':
		pass

	elif request.method == 'GET':
		return render_template()




@app.route('/login', methods=['POST'])
def process_login():
	_uname = request.form['username']
	_password = reqest.form['password']

@app.route('/lampHours')
def show_lamp_hours():
	return "lamp hours"


if __name__ == "__main__":
	app.run()
