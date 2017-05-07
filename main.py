#!/usr/bin/env python3
import SanyoProtocol as Sanyo

from flask import Flask, render_template, request, redirect, flash, session, abort
import os
import time

statusMsgs = {'00' : 'ON',
 	'80' : 'Standby',
	'40' : 'Warming',
	'20' : 'Cooling',
	'10' : 'Power Failure',
	'28' : 'Cooling : HIGH TEMP.',
	'02' : 'resend stat cmd',
	'24' : 'PM cool down',
	'04' : 'PM status',
	'21' : 'Cooling : Lamp Failure',
	'81' : 'Standby : Lamp Failure',
	'88' : 'Standby : HIGH TEMP'
	}



app = Flask(__name__)
app.secret_key = os.urandom(12)

#p1 = Sanyo.projector(port='/dev/ttyS0')
#p2 = Sanyo.projector(port='/dev/ttyS1')
#p1 = Sanyo.projector(port='/dev/ttyUSB0')
#p2 = Sanyo.projector(port='/dev/ttyUSB1')
p1 = Sanyo.projector(port='/dev/pts/2')
p2 = Sanyo.projector(port='/dev/pts/4')


processing_delay = .5

def render_main(projector1, projector2):
	# allow projcessing of previous commands
	time.sleep(processing_delay)

	# get general status
	genstatP1 = projector1.getStatusGeneral()
	if genstatP1 == '00':
		powerColP1 = "green"

	elif genstatP1 == '80':
		powerColP1 = "red"
	else:
		powerColP1 = "orange"

	#statusMsgP1 = statusMsgs[genstatP1]
	if genstatP1 in statusMsgs:
		statusMsgP1 = statusMsgs[genstatP1]
	else:
		statusMsgP1 = 'No connection'

	genstatP2 = projector2.getStatusGeneral()
	if genstatP2 == '00':
		powerColP2 = "green"

	elif genstatP2 == '80':
		powerColP2 = "red"
	else:
		powerColP2 = "orange"

	#statusMsgP2 = statusMsgs[genstatP2]
	if genstatP2 in statusMsgs:
		statusMsgP2 = statusMsgs[genstatP2]
	else:
		statusMsgP2 = 'No connection'


	# give projector time to process
	time.sleep(processing_delay)

	vidInputP1 = projector1.getInput()
	print('vidInputP1: ', vidInputP1)
	if vidInputP1 == 1:
		dviP1 = "green"
		vgaP1 = ""
		avP1 = ""

	elif vidInputP1 == 2:
		dviP1 = ""
		vgaP1 = "green"
		avP1 = ""

	elif vidInputP1 == 3:
		dviP1 = ""
		vgaP1 = ""
		avP1 = "green"

	else:
		dviP1 = ""
		vgaP1 = ""
		avP1 = ""

	vidInputP2 = projector2.getInput()
	print('vidInputP2: ', vidInputP2)
	if vidInputP2 == 1:
		dviP2 = "green"
		vgaP2 = ""
		avP2 = ""

	elif vidInputP2 == 2:
		dviP2 = ""
		vgaP2 = "green"
		avP2 = ""

	elif vidInputP2 == 3:
		dviP2 = ""
		vgaP2 = ""
		avP2 = "green"

	else:
		dviP2 = ""
		vgaP2 = ""
		avP2 = ""

	# give projector time to process
	time.sleep(processing_delay)

	# get lamp hours
	lamphourL1P1, lamphourL2P1 = projector1.getLampHour()
	lamphourL1P2, lamphourL2P2 = projector2.getLampHour()

	# render the page
	return render_template('projector_control.html', statusP1 = statusMsgP1, statusP2 = statusMsgP2, l1hoursP1 = lamphourL1P1, l2hoursP1 = lamphourL2P1, l1hoursP2 = lamphourL1P2, l2hoursP2 = lamphourL2P2, powerColorP1 = powerColP1, powerColorP2 = powerColP2, DVIP1 = dviP1, VGAP1 = vgaP1, AVP1 = avP1, DVIP2 = dviP2, VGAP2 = vgaP2, AVP2 = avP2)

@app.route('/', methods=['POST', 'GET'])
def main_control():
	if request.method == 'GET':
		if not session.get('logged_in'):
			return render_template('login.html')
		return render_main(p1, p2)

	elif request.method == 'POST':
		action = request.form['submit']
		# projector 1
		if action == 'powerOnP1':
			print("power on P1")
			p1.powerOn()

		elif action == 'powerOffP1':
			print("power Off P1")
			return redirect('/confirm', code=307)

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
			return redirect('/confirm', code=307)

		elif action == 'Input1P2':
			print("input 1 P2")
			p2.setInput(1)

		elif action == 'Input2P2':
			print("input 2 P2")
			p2.setInput(2)

		elif action == 'Input3P2':
			print("input 2 P2")
			p2.setInput(3)


		# both projectors
		if action == 'Input1B':
			print("input 1 B")
			p1.setInput(1)
			p2.setInput(1)

		elif action == 'Input2B':
			print("input 2 2")
			p1.setInput(2)
			p2.setInput(2)

		elif action == 'Input3B':
			print("input 2 B")
			p1.setInput(3)
			p2.setInput(3)


		return render_main(p1, p2)


@app.route('/confirm', methods=['POST'])
def show_confirmation():
	action = request.form['submit']

	print(action)


	if action == 'powerOffP1':
		return render_template('confirm.html', projector = 'left', proJ = '1')

	elif action == 'powerOffP2':
		return render_template('confirm.html', projector = 'right', proJ = '2')

	elif action == 'confirmP1':
		p1.powerOff()
		return redirect('/', code=302)

	elif action == 'confirmP2':
		p2.powerOff()
		return redirect('/', code=302)

	elif action == 'cancel':
		return redirect('/', code=302)





@app.route('/login', methods=['POST'])
def process_login():
	if request.form['password'] == 'password' and request.form['username'] == 'admin':
		session['logged_in'] = True

	else:
		flash("wrong username / password")

	return redirect('/', code=302)


if __name__ == "__main__":
	app.secret_key = os.urandom(12)
	app.run(host='0.0.0.0', port=8080)
