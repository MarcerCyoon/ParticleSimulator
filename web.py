from flask import Flask, request, render_template
import numpy as np
import animation

app = Flask(__name__, static_folder='static')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/', methods=['POST'])
def visual():
	time = request.form.get("time", type=int)
	coeff = request.form.get("coeff", type=int)
	numParticles = request.form.get("numParticles", type=int)

	massArray = np.zeros(numParticles)
	velArray = np.zeros((numParticles, 2))
	posArray = np.zeros((numParticles, 2))

	for i in range(1, numParticles + 1):
		massArray[i - 1] = request.form.get("mass" + str(i), type=float)
		velArray[i - 1][0] = request.form.get("vel" + str(i) + "X", type=float)
		velArray[i - 1][1] = request.form.get("vel" + str(i) + "Y", type=float)
		posArray[i - 1][0] = request.form.get("pos" + str(i) + "X", type=float)
		posArray[i - 1][1] = request.form.get("pos" + str(i) + "Y", type=float)

	if coeff is None:
		coeff = 3

	fileName = animation.generate(numParticles, massArray, velArray, posArray, time, coeff)

	return render_template('visual.html', currentPath=fileName)
