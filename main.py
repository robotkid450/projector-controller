#!/usr/bin/env python3
import SanyoProtocol as Sanyo

from flask import Flask, render_template, request, redirect


app = Flask(__name__)

#p1 = Sanyo.projector(port='/dev/ttyS0')
#p2 = Sanyo.projector(port='/dev/ttyS1')
#p1 = Sanyo.projector(port='/dev/ttyUSB0')
#p2 = Sanyo.projector(port='/dev/ttyUSB1')
p1 = Sanyo.projector(port='/dev/pts/7')
p2 = Sanyo.projector(port='/dev/pts/9')


def render_main(projector1, projector2):
	# get general status
	genstatP1 = projector1.getStatusGeneral()
	if genstatP1 != '00':
		powerColP1 = "red"
	else:
		powerColP1 = "green"
		
	genstatP2 = projector2.getStatusGeneral()
	if genstatP2 != '00':
		powerColP2 = "red"
	else:
		powerColP2 = "green"
		
		
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
		
	# get lamp hours
	lamphourL1P1, lamphourL2P1 = projector1.getLampHour()
	lamphourL1P2, lamphourL2P2 = projector2.getLampHour()
	
	# render the page
	return render_template('projector_control.html', statusP1 = genstatP1, statusP2 = genstatP2, l1hoursP1 = lamphourL1P1, l2hoursP1 = lamphourL2P1, l1hoursP2 = lamphourL1P2, l2hoursP2 = lamphourL2P2, powerColorP1 = powerColP1, powerColorP2 = powerColP2, DVIP1 = dviP1, VGAP1 = vgaP1, AVP1 = avP1, DVIP2 = dviP2, VGAP2 = vgaP2, AVP2 = avP2)

@app.route('/', methods=['POST', 'GET'])
def main_control():
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
		




#@app.route('/login', methods=['POST'])
#def process_login():
#	_uname = request.form['username']
#	_password = reqest.form['password']

#@app.route('/lampHours')
#def show_lamp_hours():
#	return "lamp hours"


if __name__ == "__main__":
	app.run(host='0.0.0.0')
