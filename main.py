#!/usr/bin/env python3
import SanyoProtocol as Sanyo

from flask import Flask, render_template, request


app = Flask(__name__)


def render_main(projector1, projector2):
	genstatP1 = projector1.getStatusGeneral()
	genstatP2 = projector2.getStatusGeneral()
	lamphourL1P1, lamphourL2P1 = projector1.getLampHour()
	#lamphour = projector1.getLampHour()
	return render_template('projector_control.html', statusP1 = genstatP1, statusP2 = genstatP2, l1hoursP1 = lamphourL1P1, l2hoursP1 = lamphourL2P1)

@app.route('/', methods=['POST', 'GET'])
def main_control():
	#p1 = Sanyo.projector(port='/dev/ttyS0')
	#p2 = Sanyo.projector(port='/dev/ttyS1')
	#p1 = Sanyo.projector(port='/dev/ttyUSB0')
	#p2 = Sanyo.projector(port='/dev/ttyUSB1')
	p1 = Sanyo.projector(port='/dev/pts/6')
	p2 = Sanyo.projector(port='/dev/pts/8')

	if request.method == 'GET':
		return render_main(p1, p2)

	elif request.method == 'POST':
		action = request.form['submit']
		# projector 1
		if action == 'powerOnP1':
			print("power on P1")
			p1.powerOn()
			
		elif action == 'powerOffP1':
			print("power Off P1")
			p1.powerOff()
			
		elif action == 'Input1P1':
			print("input 1 P1")
			p1.setInput(1)
		
		elif action == 'Input2P1':
			print("input 2 P1")
			p1.setInput(2)
		
		elif action == 'Input3P1':
			print("input 2 P1")
			p1.setInput(3)
		
		# projector 2
		if action == 'powerOnP2':
			print("power on P2")
			p2.powerOn()
			
		elif action == 'powerOffP2':
			print("power Off P2")
			p2.powerOff()
			
		elif action == 'Input1P2':
			print("input 1 P2")
			p2.setInput(1)
		
		elif action == 'Input2P2':
			print("input 2 P2")
			p2.setInput(2)
		
		elif action == 'Input3P2':
			print("input 2 P2")
			p2.setInput(3)


		return render_main(p1, p2)
		

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
